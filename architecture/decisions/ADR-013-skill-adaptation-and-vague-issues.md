# 13. Adapted A1 skill

Covers: D1, D7

Date: 2026-11-22

## Status

Accepted

## Context

The requirements agent is aided by the A1 requirements skill (ADR-001). The workflow must reuse that skill in Stage 1.

The A1 skill was written for interactive use. It asks clarification questions in up to three rounds. It writes four Markdown files: an SRS, a register, a validation report and an evidence log. It gives each item a readiness state, and it returns a "not ready" verdict for a vague input. It also expects a fetch tool to look up external sources.

In the workflow, Stage 1 runs without a person who can answer. Its output is `spec.json`, which later stages and checks read (ADR-007). Agents have bash as their only tool (ADR-010), so there is no fetch tool. ADR-007 sends the testability of the acceptance criteria to a separate LLM judge.

A vague issue may leave open what the author wants. An issue may also be so vague that no testable behaviour can be stated without inventing the core goal.

## Decision

We will run the requirements agent with an adapted copy of the A1 skill, kept in `workflow/.github/autose/prompts/`. The copy keeps the original's sections and wording wherever they apply and replaces only the parts listed below. The original skill in the A1 repository stays unchanged.

The adapted copy keeps the skill's discipline: separate what the issue states from what is inferred, never invent values, and write Given/When/Then criteria. It differs in these ways:
- It runs non-interactively. Each question the skill would have asked becomes an entry in `assumptions`.
- It writes only `spec.json` (or `rejected.json`, below) and `attempt_summary.md`, in the format of ADR-007.
- It has no readiness states, no "not ready" verdict, no clarification protocol and no fetch section.
- It checks its own draft for consistency, but gives no readiness verdict; the testability judge of ADR-007 decides.
- It rejects an issue that is not a software problem or asks for a clearly harmful change, as the original skill does. Such a rejection is the same Stage 1 rejection verdict as in ADR-007.

We will apply ADR-007's two tiers for vague issues as follows:
- If the issue is open to more than one reading, the agent chooses the most reasonable reading, records it in `assumptions`, and writes the spec. The run continues.
- If the issue is very vague, meaning that no testable behaviour can be stated without inventing the core goal, the agent writes `rejected.json` with a reason and questions for the author, instead of `spec.json`. The run stops. The reason and the questions are posted as an issue comment.

The rejection is an LLM verdict. It is logged as an LLM verdict, as ADR-007 states.

Assumptions:
- The line between "open to several readings" and "very vague" can be drawn by the agent well enough for the issues in this study. Checked on the vague issue of the study (experiment issue 5, fork issue #6); no issue in the study tests the very vague tier.
- A non-interactive run with recorded assumptions is an acceptable substitute for clarification questions, because the study measures the pipeline, not the author's answers.

## Consequences

**Positive.** The run never waits for a person, so a maintainer can label an issue and walk away. A vague issue goes ahead with its readings recorded as assumptions, which a reader can check in the issue comment.

**Negative.** The workflow no longer uses the A1 skill as written: the clarification dialogue, the readiness states and the "not ready" verdict are gone, and this deviation has to be explained in the report. An assumption that misreads the issue is not caught by any script; it is caught only if the testability judge or the reviewer notices it. How well the agent draws the line between "open to several readings" and "very vague" depends on the model and is hard to test with few issues.

**Neutral.** The assumptions comment gives the issue author a place to correct a reading, but the workflow does not read replies, so a correction only takes effect through a maintainer's re-trigger.
