# 21. Release merges base

Covers: D2, D7

Date: 2026-11-23

## Status

Accepted

## Context

A push to an AutoSE branch runs the CI workflow stored on that branch. A branch created before a change to the CI workflow keeps running the old CI, so its checks can fail for reasons that the current base branch has already fixed. Rebasing or recreating the branch would rewrite commits that a reviewer or a person may already have seen, and ADR-003 does not allow a force-push. Upstream Python-Markdown has one test class that pytest cannot collect, and its test package turns that warning into an error, so a plain `pytest` exits with an error on every commit. The baseline and G4 (ADR-007) already record this collection error as an existing failure, while CI did not. This decision amends ADR-003 and ADR-007.

## Decision

We will merge the base branch into the AutoSE branch before every push. A merge conflict stops the release. The merge commit is Release's own, so ADR-003's check for foreign commits still compares the remote branch with the head Release last pushed.

We will run CI from its JUnit report and fail it on any failure or error except the one known upstream collection error, so CI and G4 judge the same tests.

## Consequences

**Positive.** CI on an AutoSE branch always runs the current workflow files, so a branch is never failed by an outdated CI file. CI and G4 now judge the same set of tests, so a change that passes G4 is not failed by CI for a known upstream problem.

**Negative.** Pull requests gain merge commits from the base branch, which makes their history longer. The allowlisted collection error must be revisited if the pinned upstream commit changes, or a new upstream failure with the same file name could be hidden.

**Neutral.** The review diff is taken from the merge base (ADR-018), so base-branch commits brought in by the merge do not appear in it. A merge conflict stops the release instead of being resolved, which leaves the decision to a person.
