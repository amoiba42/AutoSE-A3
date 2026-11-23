# 24. Restart from stage

Covers: D2, D4, D10

Date: 2026-11-23

## Status

Accepted

## Context

ADR-003 resumes a stopped issue after its last passed stage, and ADR-004 keeps that progress in the issue's state artifact. On issue #2, the spec written by Stage 1 asked for a change that existing tests forbid. Every later stage built on that spec, so every implementation failed G4, and a re-trigger resumed after Stage 1 with the same spec. The only way to redo Stage 1 was a changed issue text, which ADR-004 handles. ADR-012 stores the tester's tests as an artifact, so a later run reused tests written for an old spec or design. This decision amends ADR-003, ADR-004, ADR-005 and ADR-012.

## Decision

We will add an optional `restart_from` input (a stage number from 1 to 4) to the manual dispatch of the workflow. The run then starts at that stage and treats every later stage as not passed.

We will drop the tester's stored tests on every restart.

We will keep every other trigger and its resume rule as in ADR-003 and ADR-005. An issue marked `done` stays finished; `restart_from` does not reopen it.

## Consequences

**Positive.** A wrong spec or design can be redone without editing the issue. Tests written for an old spec or design no longer come back after a restart.

**Negative.** A restart throws away the work of the stages it repeats, including any good parts. A restart gives an agent a second attempt, not a better model, so a hard issue can fail again.

**Neutral.** Only someone who can dispatch the workflow can restart, so the trigger rules of ADR-005 still decide who may start work.
