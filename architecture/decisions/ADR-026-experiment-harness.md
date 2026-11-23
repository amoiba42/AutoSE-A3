# 26. Experiment harness

Covers: D1, D6, D8

Date: 2026-11-23

## Status

Accepted

## Context

The assignment asks for two decision experiments that change one decision each. In the main workflow, the model behind a role depends on which free quotas are left (ADR-020), so two runs of the same variant can use different models. The main workflow also posts comments and labels, keeps per-issue state and opens pull requests, which an experiment run must not disturb. Experiment D8 gives the reviewer the implementer's notes in one variant; if those notes were stored on the base branch, they would reach pull request trees and the reviewer of the other variant. ADR-011 planned an experiment with a second model family for the reviewer, which ADR-016 kept.

## Decision

We will run decision experiments in a separate workflow, started by hand, with a read-only token, that posts nothing and keeps no issue state. Its results are workflow artifacts.

We will pin one model per role in every experiment run through `AUTOSE_PIN_MODEL_<ROLE>`, with no fallback chain.

We will keep the implementer notes for D8 on a separate branch that is never merged into the base branch, and check it out outside the sandbox.

We will run every run of one experiment on the same commit of the workflow.

We will run experiments on D1 and D8 and drop the model-family experiment of ADR-011.

## Consequences

**Positive.** Differences between variants come from the variant, not from the model chain or a changed prompt, so the results of the variants can be compared side by side. Experiment runs never post on issues or pull requests, so the seeded PRs and real issues stay clean.

**Negative.** A pinned model that runs out of quota or steps stops the run instead of falling back, so an experiment can need repeated attempts on a model with little quota. A pinned model also means the experiment speaks for that model only.

**Neutral.** Whether a reviewer from a second model family catches more defects stays untested.
