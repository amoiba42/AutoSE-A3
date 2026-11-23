# 17. One re-ask

Covers: D2, D9

Date: 2026-11-23

## Status

Accepted. Amended by ADR-022 (review findings kept until their stage passes).

## Context

ADR-006 stops a run on any failed check except the Stage 3 and Stage 4 checks, and sends every Stage 4 failure back to Stage 3. In the runs on the fork, one weak acceptance criterion stopped a run at the G1 judge, and one design target the G2 check could not resolve stopped a run at Stage 2. In both cases the agent that made the mistake was still running, and it never saw why its output was rejected. The review job drops a whole review when one piece of evidence fails the G6 check.

Some Stage 4 failures come from the tester's own files: no test file written, a file that does not parse, or an assertion changed in phase 2. Sending these to Stage 3 asks the implementer to fix work it did not do and cannot see (ADR-012), so its retries run out. A schema re-ask already exists for agent outputs (ADR-006). This decision amends ADR-006, ADR-007 and ADR-012.

## Decision

We will re-ask the same agent once, with the check's message, when the G1 structure check, the G1 judge, the G2 design check or the G6 evidence check fails. The re-ask counts toward the agent's caps. A second failure stops the run as before.

We will call the judge a second time when its answer does not match its schema, then stop.

We will send a Stage 4 failure caused by the tester's own files back to the tester once, with a send-back note. A second such failure stops the run. Every other Stage 4 failure goes to Stage 3 as in ADR-006.

We will discard edits the tester makes to the repository's existing tests before any check runs, so such edits never count against the implementer.

We will keep the retry counters per run, so a maintainer's re-trigger after a stop starts with fresh retries.

## Consequences

**Positive.** One fixable mistake no longer ends a run. A reviewer that cites a line that does not exist can correct it instead of losing the whole review. Stage 4 failures caused by the tester's own files go back to the tester, so the implementer only receives failures it can act on.

**Negative.** Each re-ask costs one more agent turn and its tokens, and a run that will fail anyway takes a little longer to stop. Discarding the tester's edits to existing tests hides those edits from G4, so a tester that relies on such an edit loses that test silently (the discarded files are listed in an artifact).

**Neutral.** Because retry counters are per run, the caps bound one run, not one issue.
