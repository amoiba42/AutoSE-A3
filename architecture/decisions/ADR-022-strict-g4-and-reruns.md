# 22. Strict G4, re-runs

Covers: D2, D7

Date: 2026-11-23

## Status

Accepted

## Context

The brief's Stage 4 check is that all new and existing tests pass. G4 as built checked only that baseline tests still passed and that every criterion had a passing test, so a failing test written by the implementer reached the pull request and failed CI. ADR-003 lets a maintainer re-trigger a stopped run, but a re-run after a Release stop released the same diff again, a re-run after a review stop repeated Stages 1 to 4, and a re-run after a stop inside a review round lost the reviewer's findings because they were cleared when the run started. This decision amends ADR-003, ADR-004, ADR-007 and ADR-017.

## Decision

We will fail G4 when any test fails that did not fail at the base commit, and give the failing test names with the first line of each error.

We will restart at Stage 4 when the previous run stopped at Release, so the change is checked again before it is released again.

We will re-release the same change for a new review when the previous run stopped only in the review job.

We will keep the reviewer's findings in the send-back note until the stage they were sent to passes.

## Consequences

**Positive.** No pull request carries a failing test that the pipeline wrote; a failing test the implementer wrote goes back to Stage 3 before Release. A re-run after a review stop costs only CI and the review, so a review stopped by a model error does not repeat Stages 1 to 4. Review findings reach the stage they were sent to even when a run stops in between.

**Negative.** A Stage 4 re-check after a Release stop repeats work that already passed once. A test that fails for a reason outside the change, such as a flaky test, now blocks the run (G4 re-runs failed tests once to soften this).

**Neutral.** Where a re-run starts is decided from `state.json`, so the behaviour depends on the issue's state artifact (ADR-004) being present and current.
