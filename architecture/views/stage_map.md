# Stage map

One row per stage: who does the work, what it saves, and what check must pass before the next stage starts. Models are the ADR-011 baseline. Full input and output contracts are in [contracts.md](contracts.md).

| # | Stage | Agent (model) | Artifact(s) | Check before moving on | Decided by | Job |
|---|---|---|---|---|---|---|
| 1 | Requirements | Requirements agent (`gemini-3.5-flash-lite`), with the A1 skill | `spec.json` (source), `spec.md` (rendered), attempt summary | `spec.json` matches its schema, and an LLM judge (`gemini-3.8-flash`) rates every acceptance criterion testable | script + LLM judge (logged as an LLM verdict) | Orchestrator |
| 2 | Design | Design + implementation agent (`gemini-3.8-flash`), with `ARCHITECTURE.md` | `design.json` (source), `design.md` (rendered) | at most 10 targets; every target is `EXISTING` (file and symbol found by `ast`) or `NEW` (parent module exists) | script | Orchestrator |
| 3 | Implementation | same agent, same conversation | `diff.patch` (made by script with `git diff`), attempt summary | package installs and imports; `ruff` passes; diff touches only design targets and tests, never `.github/`, configuration, lockfiles, `conftest.py` or `ARCHITECTURE.md`; runs with no secrets | script | Orchestrator |
| 4 | Testing | Testing agent (`gemini-3.6-flash`), two phases in scratch copies | test files named `test_ac<n>_*`, `test_report.md` (made by script), attempt summary | passing test IDs include every baseline pass (failures re-run once); every AC has a passing `test_ac<n>_*` test that calls a design target with a non-trivial `assert`; existing tests unchanged; no `conftest.py` added; phase 2 left every `assert` unchanged; runs with no secrets | script | Orchestrator |
| 5 | Release | none (script) | `pr.md` (four fields only), PR link | regex secret scan passes; branch has no commits Release did not make (never force-push); PR is open; `ci.yml` passes within 10 minutes | script | Release |
| 6 | Review | Reviewer agent (`gemini-4-hydrogen`), bash in a container | `review.json` (source), `review.md` (rendered, posted as PR comment), label | every finding and approval cites a `file:line` that exists at PR HEAD, or a command the reviewer actually ran; an approval includes the reviewer's test command and is invalid if the job's test step fails beyond `baseline.json` | LLM verdict + script evidence check | Review |
| — | Route | none (script) | updated `state.json`, issue comment | verdict, classification and review round decide: human, re-entry or stop | script | Route |

Retry caps (ADR-006): Stage 3 check fails → Stage 3 at most twice, then stop. Stage 4 check fails → Stage 3 at most twice, then Stage 2 once, then stop. A schema error gets one re-ask, counted against the caps. Any other failed check stops the run. At most two review rounds.
