# 15. Comment hygiene

Covers: D9

Date: 2026-11-22

## Status

Accepted. Amended by ADR-018 (a stop comment is removed once a later run gets past it) and ADR-027 (redaction of encoded credentials).

## Context

The fork is public, so every comment the workflow posts on an issue is visible to everyone. ADR-006 posts a stop comment on every stop and ADR-004 keeps one status comment per issue. The stop comment held up to 3000 characters of the raw provider error, which can include request details. Nothing removed credential-shaped text before it was posted or uploaded.

Each stop and each re-run added a new comment, so one issue collected several near-identical stop comments and several assumption comments. The status comment lookup reads only the first 100 comments of an issue.

## Decision

We will remove credential-shaped text from every comment the workflow posts and from every explanation artifact. This covers the values of the workflow's own secret variables and strings shaped like API keys, tokens and bearer headers.

We will show one line of the provider's message in the stop comment, with the stage and a link to the run, and not the raw error body.

We will keep one stop comment and one assumptions comment per issue and edit it on each later stop, as the status comment already is.

We will page through all of an issue's comments when looking for the workflow's own comments.

## Consequences

**Positive.** Each issue shows one status comment, one assumptions comment and at most one stop comment, so a reader sees the current state without scrolling through repeats. Raw provider errors no longer reach a public page.

**Negative.** The issue shows only the latest stop; the history of earlier stops lives in the run pages and artifacts. Pattern-based redaction can miss a secret in an unusual format, such as an encoded token. A one-line stop message can leave out detail that helps debugging.

**Neutral.** The full explanation still exists as an artifact for each run, linked from the stop comment.
