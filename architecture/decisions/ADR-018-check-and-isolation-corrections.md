# 18. Check and isolation fixes

Covers: D3, D5, D6, D7, D8, D9

Date: 2026-11-23

## Status

Accepted. Amended by ADR-025 (the reviewer's workspace keeps only the PR commit).

## Context

A review of the whole pipeline found places where the code did not do what earlier ADRs decided. The G2 check (ADR-007) resolved only top-level functions and classes and `Class.method`, so a legitimate target such as a class attribute or a module constant was reported as missing, and a non-Python target crashed the job. An issue-2 run that targeted `HashHeaderProcessor.RE` stopped at G2 for this reason. The G4 coverage check did not count `pytest.raises` as a check or a class imported with `from markdown import Markdown` as a call to the library. A test file that did not parse crashed the job instead of failing the check.

ADR-012 keeps the implementation and the design's reasoning from the tester in phase 1 and keeps the tester's tests from the implementer. The sandbox mounted every workspace, so the tester could read the implementation and `design.json`, and a Stage 3 retry could read the Stage 4 copies holding the tester's tests. ADR-002 gives the reviewer the diff of the pull request, but the diff was taken against the current base branch, so any later commit on that branch appeared as a reversed change.

ADR-006 requires an explanation for every stop, but an exception other than a planned stop ended the job without one. ADR-014's waits of up to 90 seconds counted inside the stage's wall-clock cap, so a stage hit by repeated overload errors could time out from waiting alone. Send-back notes named a failed check but not the failing tests or lint locations. This decision amends ADR-002, ADR-006, ADR-007, ADR-010, ADR-012, ADR-014 and ADR-015.

## Decision

We will resolve design targets by parsing the target file, including nested classes and functions, class attributes and module-level assignments, and check that each target's kind matches what it names. We will add `attribute` as a kind and require `module` for a non-Python file.

We will count `pytest.raises`, `pytest.warns` and their unittest forms as a check in G4, count names imported from the library as calls to it, and report an unparsable test file as a failed check.

We will empty the agents' output directory at the start of every stage, make the implementation and clean workspaces unreadable to the sandbox user during the tester's phases, and delete the Stage 4 copies before Stage 3 runs.

We will diff the pull request against its merge base with the base branch, which Release reports to the review job.

We will turn any unexpected exception in the orchestrator, Release or the review job into a stop with an explanation artifact.

We will put the failing test names with the first line of each error, and the location and message of each new lint problem, in send-back notes. The notes never contain the tester's test source.

We will change ADR-014's waits to at most three retries of at most 60 seconds each, also treat a 500 or 529 overloaded answer as transient, and keep the time spent waiting out of the stage's wall-clock cap.

We will keep one stop comment and one finished comment per issue and remove the stop comment once a later run gets past it.

## Consequences

**Positive.** Designs that touch class attributes, constants, nested functions or non-Python files can pass G2. Tests that check for an exception count as covering a criterion. An unexpected exception now ends in an explained stop instead of a bare job failure, and the reviewer's diff shows only AutoSE's change. Shorter waits that are kept out of the wall-clock cap stop stages from timing out on waiting alone.

**Negative.** The first line of a failing assertion can reveal an expected value to the implementer, although never the test source. Hiding workspaces from the tester relies on the sandbox commands running as a non-root user. Time spent inside a failing request still counts against the wall-clock cap, so a provider that keeps failing slowly can still time a stage out.

**Neutral.** Most of these correct how earlier ADRs were implemented. The `attribute` kind, the wider set of transient errors, the wait accounting and the removal of old stop comments are small additions. None of them changes the stage structure.
