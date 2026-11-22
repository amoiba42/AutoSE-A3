# 1. Four-agent split of the six stages

Covers: D1

Date: 2026-11-22

## Status

Proposed

## Context

The workflow has six fixed stages: Requirements, Design, Implementation, Testing, Release and Review. The number of agents that carry them out is open. Two earlier inputs are available: my improved A1 requirements skill, and my A2 `ARCHITECTURE.md` for the target repo.

Every extra agent adds a hand-off and a separate context window. Splitting planning from coding can leave a gap between the plan and the code. The target repo is Python-Markdown at commit `3f2c551`: 33 Python files and about 9,000 lines in the `markdown` package, plus 37 test files. It is small enough for one agent to hold both. Tests written by the agent that wrote the code tend to follow its approach and overfit to that code. The A1 skill was built and tested as a standalone prompt, and a spec written alongside the design can bend toward the chosen solution.


## Decision

We will use four agents.

| Agent | Stages | Aided by | Artifact(s) |
|---|---|---|---|
| Requirements | 1 | A1 skill | `spec.md` |
| Design + implementation | 2, 3 | A2 `ARCHITECTURE.md` | `design.md`, `diff.patch` |
| Testing | 4 | | `test_report.md` |
| Reviewer | 6 | | `review.md` |

We will keep design and implementation in one agent. We will keep the testing agent separate from it. We will keep the reviewer separate from all other agents.

## Consequences

**Negative.** Four context windows add hand-off overhead and use more tokens than a single agent.

**Neutral.** After a send-back to design, the agent that wrote the code also redesigns it.
