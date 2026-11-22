# 2. Reviewer isolation from the implementer

Covers: D8

Date: 2026-11-22

## Status

Proposed

## Context

The reviewer must not simply agree with the implementer. It should see only the issue, the diff and the repository at the latest commit of the pull request, and it can run the code. It must not see the implementer's conversation or reasoning. It gets its own prompt and read and run permission, but no push. A different model is allowed but not required.

ADR-001 makes the reviewer a separate agent. `spec.md`, `design.md` and `test_report.md` contain implementer reasoning, and anything on the PR branch is visible to the reviewer. The PR body (`pr.md`) can also carry implementer details, and the issue's comment thread can carry workflow status and other comments.

A prompt rule relies on the model obeying it, while job permissions are enforced by GitHub. Models of the same family share blind spots. `test_report.md` is the tester's own claim. A reviewer can approve without checking anything.

## Decision

We will run the reviewer in its own job with `contents: read` and `pull-requests: write` permissions only. The job will not have `actions: read`.

We will give the reviewer only the issue title and body, the diff and the repository at the latest commit of the pull request. The issue's comment thread is not included. We will keep `spec.md`, `design.md` and `test_report.md` off the PR branch.

We will not give the reviewer `pr.md`. As a backstop, we will keep `pr.md` minimal: the issue link, the branch name, the list of changed files and the link to the Actions run.

We will use a different model for the reviewer from the agents that write code.

We will have the reviewer job run the tests itself, in a step with no secrets in its environment.

We will treat the diff and the repository as untrusted input in the reviewer's prompt, because the code under review can contain text aimed at the reviewer.

We will give the reviewer a skeptical prompt. Every finding and every approval must cite a `file:line` or a failing command, and an approval without evidence is invalid. Together with the isolated inputs, this stops easy approvals; the evidence rule matters most.

We will post the verdict as a PR comment plus a label (`autose-approved` or `autose-changes-requested`).

## Consequences

**Negative.** The reviewer does not see the spec or design, so it may reject a correct change because it does not know the intent.

**Neutral.** Isolation depends on the reviewer job never getting `actions: read`.
