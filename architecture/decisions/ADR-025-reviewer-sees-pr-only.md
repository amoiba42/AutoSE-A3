# 25. Reviewer sees PR only

Covers: D8, D9

Date: 2026-11-23

## Status

Accepted

## Context

ADR-002 lets the reviewer see the issue, the diff and the repository at the pull request's latest commit, and nothing of the implementer's reasoning. The review job checks the branch out with its full history so that the diff against the base commit works (ADR-018). A full checkout also holds every other branch of the fork as git refs: other pull requests, the base branch with the workflow's own code, and branches that hold experiment data. A reviewer with a shell can read any of them with git. This decision amends ADR-002 and ADR-018.

## Decision

We will delete every git ref in the reviewer's workspace except the pull request's commit, and drop the objects that only those refs reached, before the reviewer starts.

We will keep the base commit, which the pull request's history still reaches, so the diff of ADR-018 still works.

## Consequences

**Positive.** The reviewer cannot read other branches, other pull requests or experiment notes through git, which closes a path around ADR-002.

**Negative.** Files in the pull request's own tree stay readable. Release merges the base branch into it (ADR-021), so the workflow's own code and prompts on the base branch are visible to the reviewer. Deleting refs and pruning objects adds a few seconds to the review job.

**Neutral.** The diff against the base commit still works, because the pull request's history reaches that commit.
