# 8. Lightweight linting and secret scanning

Covers: D7, D9

Date: 2026-11-22

## Status

Proposed

## Context

ADR-007 runs `ruff` in the Stage 3 check. ADR-006 runs a regex secret scan on the diff before Release. Each run changes a small diff for a single issue.

Dedicated tools exist: `gitleaks` for secrets, `bandit` and `semgrep` for insecure code, `grimp` and `import-linter` for architecture rules, `mutmut` for test strength through mutation testing, and `diff-cover` for coverage of changed lines. 

## Decision

We will use `ruff` as the only linter and a regex scan as the only secret check.

We will not use `gitleaks`, `bandit`, `semgrep`, `grimp`, `import-linter`, `mutmut` or `diff-cover`. They add setup, run time and false positives. Mutation testing can take longer than the 5-minute test budget of the target repo.

## Consequences

**Positive.** Fewer tools mean less setup and faster runs. There is no security or architecture analysis beyond `ruff` and the regex scan, which is acceptable at the scale of this repo.

**Negative.** Test strength is never measured, because mutation testing is not used.
