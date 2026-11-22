# 7. Script-decided checks with two explicit LLM verdicts

Covers: D7

Date: 2026-11-22

## Status

Proposed

## Context

Each stage hands over only after its check passes. An LLM can certify its own work wrongly, while a script gives the same answer every time but can only check what is measurable. Whether an acceptance criterion is testable needs judgment. Python has no compile step, so "the code builds" has to be defined.

Agents can change files outside the plan, including workflow files, configuration and `ARCHITECTURE.md`. Tests can be edited until they pass, deselected through `conftest.py`, or written so they pass without checking anything. Some tests may already fail at the pinned commit, and some may be flaky. A design can list many targets to widen what the scope guard allows. A vague issue may not hold enough information for testable acceptance criteria. ADR-002 requires evidence for every finding and approval, and ADR-006 scans the diff for secrets before Release.

## Decision

We will decide every check with a script and its exit code, except two LLM verdicts: the Stage 1 testability judgment, logged as an LLM verdict, and the Stage 6 review verdict.

| Stage | Check | Decided by |
|---|---|---|
| 1 | `spec.json` passes a structure check, and an LLM judges each acceptance criterion testable | script + LLM |
| 2 | at most 10 design targets; every design target is marked `EXISTING` or `NEW`; an `ast` check confirms each `EXISTING` file and function, and a path check confirms the parent module of each `NEW` one | script |
| 3 | the package installs and imports, `ruff` reports no problem that was not already in the file at the base commit, and the diff touches only files named in the design plus tests, never `.github/`, configuration, lockfiles, `conftest.py` or `ARCHITECTURE.md` | script |
| 4 | the set of passing test IDs includes every test that passes in `baseline.json`; failed tests are re-run once before the check fails; every acceptance criterion has at least one passing test marked `AC-n` that calls a design target and has a non-trivial `assert`; existing tests are unchanged (hash check); no `conftest.py` is added or changed | script |
| 5 | the pull request is open and `ci.yml` passes, polled for up to 10 minutes | script |
| 6 | the reviewer's verdict, after a script confirms that every finding and approval cites a `file:line` that exists or a command the reviewer actually ran; an approval must include the test command the reviewer ran, and is invalid if the job's own test step has failures beyond `baseline.json` | LLM + script |

We will make `spec.json` the source of truth for the spec; `spec.md` is rendered from it.

We will record `baseline.json` by running the test suite on the clean commit. Tests that already fail there do not block Stage 4.

We will treat a review verdict without valid evidence as invalid, and the run stops.

When the issue is vague, the requirements agent will proceed with assumptions. It records each assumption in `spec.json`, and the assumptions are posted as an issue comment for humans.

## Consequences

**Positive.** Tests that already fail at the pinned commit are recorded in `baseline.json` and do not block Stage 4, which is good practice.

**Negative.** On a vague issue, the reviewer never sees the recorded assumptions, because ADR-002 gives it only the issue title and body.

**Neutral.** The Stage 1 LLM judge is the one non-deterministic check before review. Vague issues pass with assumptions that may be wrong, which is natural for vague input.
