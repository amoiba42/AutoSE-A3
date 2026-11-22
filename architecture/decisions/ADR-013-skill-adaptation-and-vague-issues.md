# 13. Non-interactive adaptation of the A1 skill and two-tier handling of vague issues

Covers: D1, D7

Date: 2026-11-22

## Status

Proposed

## Context

The requirements agent is aided by my A1 requirements skill (ADR-001). The workflow must reuse that skill in Stage 1.

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
- It rejects an issue that is not a software problem or asks for a clearly harmful change, as the original skill does.

We will handle vague issues in two tiers:
- If the issue is open to more than one reading, the agent chooses the most reasonable reading, records it in `assumptions`, and writes the spec. The run continues.
- If the issue is very vague, meaning that no testable behaviour can be stated without inventing the core goal, the agent writes `rejected.json` with a reason and questions for the author, instead of `spec.json`. The run stops. The reason and the questions are posted as an issue comment.

The rejection is an LLM verdict. It is logged as an LLM verdict, as ADR-007 states.

Assumptions:
- The line between "open to several readings" and "very vague" can be drawn by the agent well enough for the issues in this study. Checked on the vague issue (issue 5) and on one clearly empty issue before the main runs.
- A non-interactive run with recorded assumptions is an acceptable substitute for clarification questions, because the study measures the pipeline, not the author's answers.

## Consequences

TODO(me): List the positive, negative and neutral consequences. Start with these:
- The workflow no longer uses the A1 skill as written, so the deviation must be explained.
- A wrong rejection ends a run that could have worked; a missing rejection lets a wrong spec through.
- The line between "open to several readings" and "very vague" rests on the agent's judgment.
