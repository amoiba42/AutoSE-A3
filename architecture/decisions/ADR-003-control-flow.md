# 3. Orchestrator-driven control flow across four jobs

Covers: D2

Date: 2026-11-22

## Status

Proposed

## Context

The six stages run in order, and a stage hands over only after its check passes. A stage that cannot pass its check explains why in its artifact and stops the run. Work can go back to an earlier stage: repeated test failures may need a new design, and a reviewer who disagrees with the approach sends work back to design. Review changes are limited to two rounds.

The workflow can be a fixed pipeline, an orchestrator with workers, a state machine, Actions jobs that trigger each other, or a planner that decides the next step. An LLM planner can skip a stage, accept a failing check, or keep looping, and its routing is hard to test.

Pushing and opening a pull request need a write token, and agents read untrusted issue text. ADR-001 defines four agents, with the tester separate from the implementer. ADR-002 runs the reviewer in its own job with `contents: read` and `pull-requests: write` only. Starting a new run through `workflow_dispatch` needs `actions: write`. Pushes made with `GITHUB_TOKEN` do not start other workflows, such as CI, while actions taken with a personal token do start them. A maintainer may push to the branch between rounds. Classifying a requested change needs judgment; routing it is a fixed lookup.

## Decision

We will control Stages 1 to 4 with a Python orchestrator, a state machine in one job. Only the orchestrator decides which stage runs next, when work goes back and when the run stops.

We will run Release (Stage 5) as a separate job with no agent. A script pushes the branch and opens the pull request with a fine-grained PAT or GitHub App token stored as a secret, limited to contents and pull requests on the fork and without workflow permission. The PAT is used only to push and open the pull request; all comments and labels use `GITHUB_TOKEN`. Release never force-pushes: if the branch has commits it did not make, the run stops. No agent will hold a write token.

We will run Review (Stage 6) in a third job, as ADR-002 decides.

We will have the reviewer classify each requested change as spec, design, code or test, and record it in the review artifact.

We will run a fourth job, Route, after Review:

- Route is a script with no agent, with only `actions: write` and `issues: write`.
- Route runs with `if: always()`, so it also runs when an earlier job fails, times out or is cancelled.
- Route reads the verdict and classification and applies a fixed lookup: spec to Stage 1, design to Stage 2, code to Stage 3, test to Stage 4. When findings have different classifications, Route picks the earliest stage.
- Route starts a new run at that stage through `workflow_dispatch`, on the same branch and pull request.
- When the run ends after review, Route comments on the issue.

## Consequences

**Negative.** Four jobs mean four fresh runners, which adds setup time. The PAT or GitHub App token used by Release is one more secret to manage.

**Neutral.** The orchestrator cannot adapt to unusual situations, and every route must be written in advance. This keeps control in our hands, but a missing or wrong route is a source of error. A re-entry is a new run, so one issue can have several run links. Each review round is kept separate in its own run.
