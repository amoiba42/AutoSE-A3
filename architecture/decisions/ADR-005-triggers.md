# 5. Label and comment triggers

Covers: D10

Date: 2026-11-22

## Status

Accepted. Amended by ADR-014 (issues are started one at a time) and ADR-024 (a `restart_from` input on manual dispatch).

## Context

A maintainer starts the workflow by adding a label to an issue or by posting a comment. The fork is public, so anyone can open issues and post comments. An `issue_comment` run executes in the fork with its secrets, whoever wrote the comment. Only users with triage or write access can add labels. `labeled` fires for every label, not only ours.

Comments on pull requests also fire `issue_comment`, and there `issue.number` is the PR number. ADR-003 starts re-entry runs through `workflow_dispatch`, which has no issue in its event. Events created with `GITHUB_TOKEN` do not start new runs, except `workflow_dispatch`. ADR-004 resumes a restarted run from the last stage that passed.

GitHub concurrency groups allow one running and one pending run. A newer pending run replaces the older pending one.

## Decision

We will start the workflow on three events:

| Event | Condition | Who can start it |
|---|---|---|
| `issues: labeled` | the label is `autose` | users with triage or write access |
| `issue_comment: created` | the comment starts with `/autose`, is on an issue and not a pull request, `author_association` is OWNER, MEMBER or COLLABORATOR, and the author is not a Bot | owner, members and collaborators |
| `workflow_dispatch` | input `issue` holds the issue number | the workflow itself (ADR-003) and users with write access |

We will accept `/autose` only on issues.

We will run at most one run per issue, with `concurrency: group: autose-${{ github.event.issue.number || inputs.issue }}` and `cancel-in-progress: false`. Events that will not start a run (other labels, ordinary or unauthorised comments) get their own one-off concurrency group, so they can never replace a queued run. A second trigger for the same issue waits in the queue and then resumes from the last stage that passed. Runs for different issues run in parallel.

## Consequences

**Positive.** A second trigger for the same issue waits instead of running in parallel, so two runs never change the same branch at once.

**Neutral.** `/autose` on a pull request does nothing; maintainers comment on the issue instead. A `/autose` posted during review can replace Route's pending re-entry run, but the new run still starts from the target stage recorded in `state.json` (ADR-004).
