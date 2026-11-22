# 6. Least privilege, capped work and explained stops

Covers: D9

Date: 2026-11-22

## Status

Proposed

## Context

Anyone can write an issue, and its text reaches the agents. That text can contain instructions aimed at them. ADR-003 keeps write tokens away from agents, and ADR-005 limits who can start a run. An agent can also put a secret or token into the code it writes, and anything pushed to the public fork is visible to everyone. Event fields such as the issue title are written by untrusted users, and `${{ }}` expressions in a `run:` step are pasted into the shell before it runs. Install and test steps execute code the agents wrote.

Agents can loop, call tools repeatedly and spend tokens without a natural end. A GitHub Actions job stops after 6 hours by default, and the provider spending limit only stops all work at once. A stage can fail its check repeatedly, and retrying the same task rarely fits within the same cap.

Stop handling written inside a job does not run if that job crashes, times out or loses its runner. Dedicated scanners and injection classifiers exist, but they add setup, run time and false positives.

## Decision

We will wrap the issue title and body as delimited, untrusted input in every agent prompt, with a random delimiter for each run, and tell agents to treat it as data. We will not block or classify text with regex rules or a custom classifier.

We will set `permissions: {}` at the top level of the workflow. Each job will declare only the permissions it needs.

We will pass issue and comment fields to scripts only through environment variables, never through `${{ }}` expressions inside `run:` steps.

We will run every step that executes repository code, including the Stage 3 install and the Stage 4 tests, with no secrets in its environment.

We will run a regex secret scan on the diff before Release pushes it. A match stops the run.

We will give every agent stage a token cap, a wall-clock cap and a tool-call cap, and every run a total token cap. Every job will set `timeout-minutes` well below the 6-hour limit. Token use is logged per stage.

We will stop the run when a cap is reached. A breached cap is not retried.

We will cap retries. When the Stage 3 check fails, the orchestrator sends work back to Stage 3 at most twice, then stops. When the Stage 4 check fails, it sends work back to Stage 3 at most twice, then to Stage 2 once, then stops. When an agent's output fails its schema, the orchestrator asks the same agent once to fix the format, and this counts toward its caps. Any other failed check stops the run. After the second review round, the run ends and a human decides.

Every stop will upload its explanation artifact and post a comment on the issue that links to it. When a job crashes, times out or is cancelled, Route (ADR-003) detects it from the job results, updates the issue mirror (ADR-004) and posts the stop comment.

## Consequences

**Negative.** Caps can stop a run that was about to succeed. Delimiting the issue text does not fully stop prompt injection; safety relies on agents holding no tokens. A regex secret scan can miss secrets in unusual formats.
