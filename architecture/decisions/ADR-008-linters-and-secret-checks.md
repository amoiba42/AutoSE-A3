# 8. Ruff and regex scan

Covers: D7, D9

Date: 2026-11-22

## Status

Accepted

## Context

ADR-007 runs `ruff` in the Stage 3 check. ADR-006 runs a regex secret scan on the diff before Release. Each run changes a small diff for a single issue. The target repo's test suite runs in under 5 minutes, and mutation testing reruns it many times.

Dedicated tools exist: `gitleaks` for secrets, `bandit` and `semgrep` for insecure code, `grimp` and `import-linter` for architecture rules, `mutmut` for test strength through mutation testing, and `diff-cover` for coverage of changed lines. 

## Decision

We will use `ruff` as the only linter and a regex scan as the only secret check.

We will not use `gitleaks`, `bandit`, `semgrep`, `grimp`, `import-linter`, `mutmut` or `diff-cover`. They add setup, run time and false positives. Mutation testing would multiply the test run time.

## Consequences

**Positive.** Fewer tools mean less setup and faster runs.

**Negative.** There is no security or architecture analysis beyond `ruff` and the regex scan, which we accept at the scale of this repo. Test strength is never measured, because mutation testing is not used.
