# 27. Encoded secret redaction

Covers: D9

Date: 2026-11-23

## Status

Accepted

## Context

ADR-015 removes credential-shaped text and the values of the workflow's secret variables from every comment and explanation artifact. Release authenticates its push with a git header that holds the PAT in base64. When a push failed, the error message kept the whole git command, header included, so the encoded token reached a public explanation artifact. The redaction matched only the plain secret values, not their encoded forms. The fork is public, and a leaked token stays valid until it is revoked. The leaked token was removed from the artifact and rotated. This decision amends ADR-015.

## Decision

We will keep only the return code and git's own error output when a Release git command fails, never the command line or its headers.

We will redact each secret value in its plain form and in the base64 forms used in authentication headers, including the `x-access-token:<value>` form.

We will treat any secret found on a public page or artifact as leaked: delete the artifact and the comment, and rotate the token before the next run.

## Consequences

**Positive.** A failed push no longer carries the token into an error message, and an encoded token that reaches text by another path is still removed.

**Negative.** Redaction still covers only the encodings we know of; another encoding of a secret would pass through. Rotating a token means updating the repository secret by hand before the workflow can push again.

**Neutral.** The redaction is applied in one shared function, so every job that writes comments or artifacts gets it.
