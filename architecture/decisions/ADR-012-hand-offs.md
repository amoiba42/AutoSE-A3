# 12. Full-artifact hand-offs with a two-phase tester

Covers: D3

Date: 2026-11-22

## Status

Proposed

## Context

Each stage saves an artifact, and the target repo is small. A summary of an artifact can lose detail or distort it. ADR-001 keeps design and implementation in one agent, while the Stage 2 check runs between them.

ADR-001 separates the tester so its tests do not fit the code already written, but ADR-010's scratch copy already contains that code. Tests written before the code exists still need the names of the files and functions to call, and `design.md` holds those names together with the implementer's reasoning. A tester that edits its tests after seeing the implementation can weaken assertions until they pass. After a Stage 4 failure, Stage 3 runs again in a workspace that would otherwise contain the tester's tests. An agent could also edit `ARCHITECTURE.md` to fit its own change.

## Decision

We will hand over full artifacts between stages, not summaries. There are two exceptions: the attempt summary from ADR-004, used in a send-back note, and the interface list given to the tester.

| Agent | Receives | Never receives |
|---|---|---|
| Requirements | issue title and body, A1 skill, the repository | |
| Design + implementation | issue, spec, `ARCHITECTURE.md`, the repository; on a send-back, the send-back note | |
| Testing, phase 1 | issue, spec, the interface list, a copy of the clean commit | the reasoning in `design.md`, the implementer's code, trajectory and attempt summary |
| Testing, phase 2 | its phase 1 tests, a copy with the implementation | the reasoning in `design.md`, the implementer's trajectory and attempt summary |
| Reviewer | as decided in ADR-002 | |

We will run the design + implementation agent as one conversation across Stages 2 and 3. The orchestrator pauses it after `design.md` for the Stage 2 check, and continues the same conversation if the check passes.

We will run the testing agent in two phases. In phase 1, it writes tests from the issue, the spec and the interface list in a copy of the clean commit. A script extracts the interface list from the design targets: file, function, signature and `EXISTING` or `NEW`. The tester never sees the reasoning in `design.md`. In phase 2, its tests are moved into a copy with the implementation, where it runs them and may fix only setup errors: imports, fixtures and paths. It may not change or remove `assert` lines. A script compares the assertions in phase 1 and phase 2 and fails the Stage 4 check if any changed. A failing assertion stays failing and goes back to Stage 3.

We will store the tester's tests as an artifact and apply them only for the Stage 4 check. A Stage 3 retry runs in a workspace without them, so the implementer never sees or changes the tester's tests.

Agents will read `ARCHITECTURE.md` and never change it in PR branches.

## Consequences

**Positive.** The tester gets only the interface list, not the design's reasoning, which is good practice. It requires the design to list its targets in a format a script can parse.

**Negative.** Full artifacts make prompts longer and use more tokens, as expected for any agentic workflow. If a phase 1 assertion misreads an acceptance criterion, nothing in the run can fix it: Stage 3 retries run out and the run stops. We accept this to keep the tester independent of the implementation.

**Neutral.** Phase 1 tests may not import correctly until phase 2. Both phases run in the same agent, so this does not matter.
