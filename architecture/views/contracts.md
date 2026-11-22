# Agent contracts

What each agent receives, what it must produce, and who uses each output. Derived from ADR-001 to ADR-012. Rule of thumb: an agent gets what the next check or the next stage needs, and nothing that carries another agent's reasoning unless an ADR allows it.

## 1. Shared rules for every agent

- **Issue input:** the issue title and body **snapshot** stored in `state.json` on the first run (ADR-004), wrapped in a random per-run delimiter as untrusted data (ADR-006). Never the live issue, never the comment thread.
- **Tool:** bash only, through mini-swe-agent (ADR-010). Every command runs in the sandbox container, which holds no secrets and cannot see the runner's processes.
- **No GitHub token:** jobs that run agents check out with `persist-credentials: false`, so no token is left in `.git/config`. All GitHub actions are done by scripts (ADR-003, ADR-010).
- **Attempt summary:** every agent ends with `attempt_summary.md`: what it did and why, at most about 200 words. It is used only in a send-back note for the same stage (ADR-004).
- **Schema errors:** an output that fails its schema gets one re-ask to the same agent, counted against its caps (ADR-006).
- **Caps:** step limit and wall-clock limit in mini-swe-agent; token cap enforced by the orchestrator from each response's `usage` (ADR-006, ADR-010).

## 2. Contracts per agent

### Requirements agent (Stage 1)

| | |
|---|---|
| Receives | issue title + body; A1 skill as the system prompt; the repository at the clean commit (read only). On a send-back: the send-back note. |
| Must output | `spec.json` (schema below) and `attempt_summary.md`; or, only for a very vague issue, `rejected.json` (`{"reason", "questions"}`) instead of `spec.json`, which stops the run |
| Never receives | design, code, tests, review, other agents' summaries |

```json
{
  "issue": 3,
  "summary": "one paragraph restating the request",
  "acceptance_criteria": [
    {"id": "AC-1", "text": "Given ..., when ..., then ...", "verify_by": "unit test of markdown.markdown()"}
  ],
  "assumptions": ["only if the issue is vague"],
  "out_of_scope": ["..."]
}
```

Used by: the G1 structure check and judge (`acceptance_criteria`), the design agent (all), the tester (`acceptance_criteria`, `id`), the G4 coverage check (`id`), the issue comment (`assumptions`), `spec.md` (rendered for humans).

### Stage 1 testability judge (part of G1)

| | |
|---|---|
| Receives | `acceptance_criteria` only (id, text, verify_by). Not the issue, not the requirements agent's summary. |
| Must output | `judge.json`: `[{"id": "AC-1", "testable": true, "reason": "..."}]` |

G1 passes only if the schema is valid and every AC is `testable: true`. `judge.json` is logged as an LLM verdict.

### Design + implementation agent (Stages 2 and 3, one conversation)

| | |
|---|---|
| Receives | issue title + body; `spec.json`; `ARCHITECTURE.md`; the repository. On a send-back: the send-back note. |
| Must output (Stage 2) | `design.json` (schema below); `design.md` is rendered from it |
| Must output (Stage 3) | code changes in the working tree; `attempt_summary.md`. `diff.patch` is made by a script with `git diff`. |
| Never receives | tests written by the tester, `test_report.md`, review, the tester's summary (except inside a send-back note) |

```json
{
  "approach": "short prose plan",
  "targets": [
    {"file": "markdown/extensions/toc.py", "symbol": "TocTreeprocessor.run", "kind": "method",
     "signature": "def run(self, doc: etree.Element) -> None", "status": "EXISTING"}
  ]
}
```

Used by: G2 (`targets[].file`, `symbol`, `status`), the G3 scope guard (`targets[].file` is the allow list), the interface list for the tester (`file`, `symbol`, `kind`, `signature`, `status` only; `approach` is dropped).

### Testing agent (Stage 4, two phases)

| | Phase 1 | Phase 2 |
|---|---|---|
| Receives | issue title + body; `acceptance_criteria` from `spec.json`; the interface list; a scratch copy of the clean commit | its phase 1 tests; a scratch copy with the implementation |
| May change | new test files under `tests/` | imports, fixtures and paths in its own phase 1 files; never an `assert` line; no new files |
| Never receives | `approach` from `design.json`, the implementer's code (phase 1), trajectory, attempt summary | the implementer's trajectory and attempt summary |

Must output: test files whose test functions are named `test_ac<n>_<what>` (one or more per AC), each calling at least one interface symbol and containing a non-trivial `assert`, and `attempt_summary.md`. Only test files under `tests/` are kept, never `conftest.py`; anything else is discarded and logged (ADR-010). The tests are stored as an artifact and applied only for G4, so a Stage 3 retry never sees them (ADR-012). `test_report.md` is written by a script from the `pytest` JUnit XML and `baseline.json`, not by the agent.

Used by: G4 (test names map to AC ids; assertions compared across phases), Release (tests are part of the diff), `results.csv`.

### Reviewer agent (Stage 6)

| | |
|---|---|
| Receives | issue title + body; `git diff` of the PR; the repository at the PR's latest commit (inside a container); the JUnit result of the test step run in the same job with no secrets. The diff and repository are marked as untrusted input. |
| Never receives | `spec.*`, `design.*`, `test_report.md`, `pr.md`, attempt summaries, send-back notes, trajectories, `state.json`, the issue comment thread, the round number |
| Must output | `review.json` (schema below); `review.md` is rendered from it and posted as a PR comment by a script, with the label |

```json
{
  "verdict": "approve",
  "approval_evidence": [{"file": "markdown/extensions/toc.py", "line": 212}],
  "findings": [
    {"id": "F1", "classification": "code", "severity": "major",
     "evidence": {"command": "pytest tests/test_toc.py -k anchor", "excerpt": "AssertionError ..."},
     "explanation": "...", "drift_reference": "markdown/extensions/toc.py:198"}
  ]
}
```

- `verdict` is `approve` or `changes_requested`. `classification` is one of `spec`, `design`, `code`, `test`.
- `drift_reference` may point only at the issue, a `file:line`, or a section of `ARCHITECTURE.md` (ADR-004).

Used by: G6 (every `file:line` must exist at PR HEAD; every `command` must appear in the reviewer's own run log; an `approve` must include the reviewer's test command and is invalid if the job's test step failed beyond `baseline.json`), Route (`verdict`, `classification`), the send-back note (`findings` copied verbatim).

## 3. Script outputs

| Output | Written by | Contents | Read by |
|---|---|---|---|
| `state.json` | Orchestrator, Route | issue snapshot (title, body, `updated_at`), branch, current stage, last passed stage, target stage, review round, retry counters, run IDs, `done` flag, model ID per role, tokens per stage | Orchestrator, Release, Route; mirrored on the issue |
| send-back note | Orchestrator | attempt summary of the stage being redone + failed check output or `review.json` findings | the agent of the stage being redone |
| `pr.md` | Release | issue link, branch name, changed files, Actions run link | humans |
| commit message | Release | fixed template: `autose: issue #<n>, round <r>`; never force-pushed | humans (visible to the reviewer, so it carries no reasoning) |
| explanation artifact | the job that stopped, or Route on a crash | stage, check, exit code, output tail, caps reached | humans, issue comment |

**Route rule when findings have different classifications:** Route sends the work to the **earliest** stage named (spec before design before code before test), because the later stages run again anyway.

## 4. Visibility matrix

✓ = receives · — = never receives · N = only inside a send-back note

| Artifact | Requirements | Judge | Design + impl | Tester P1 | Tester P2 | Reviewer |
|---|---|---|---|---|---|---|
| Issue title + body | ✓ | — | ✓ | ✓ | — | ✓ |
| Issue comment thread | — | — | — | — | — | — |
| `spec.json` | own output | ACs only | ✓ | ACs only | — | — |
| `design.json` approach | — | — | own output | — | — | — |
| Interface list | — | — | — | ✓ | — | — |
| Implementation code | — | — | own output | — | ✓ | ✓ (diff + repo) |
| Tester's tests | — | — | — (not even on a Stage 3 retry) | own output | own output | ✓ (diff + repo) |
| `test_report.md` | — | — | N | — | — | — |
| `review.json` findings | N | — | N | N | — | own output |
| Attempt summaries | N (own) | — | N (own) | — | — | — |
| Trajectories | — | — | — | — | — | — |
| `pr.md` | — | — | — | — | — | — |

## 5. Workflow-level safety rules

- Event fields (issue title, body, comment) reach scripts only through `env:` variables, never `${{ }}` inside `run:` (ADR-006).
- Every step that runs repository code (install, tests, baseline, the reviewer's test step) has no secrets in its environment (ADR-006).
- The PAT is fine-grained: contents and pull requests on the fork only, no workflow permission. It is used only to push and open the PR; all comments and labels use `GITHUB_TOKEN`, so they cannot trigger runs (ADR-003).

## 6. Known residual leaks

- **Code comments and test names** are in the diff, so the reviewer can see them. Prompts tell agents to keep comments to what the code does, not why it was chosen. Test names carry only AC ids, not AC text.
- **Same-run artifacts:** the reviewer job has no `actions: read`, and its bash runs in a container without the runner's internal tokens, so it cannot download artifacts from the run.
