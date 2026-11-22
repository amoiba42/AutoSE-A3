# 9. No SonarQube

Covers: D7

Date: 2026-11-22

## Status

Proposed

## Context

SonarQube combines static analysis, code smells, coverage, security hotspots and quality gates in one platform. A2 work describes the target repo, Python-Markdown, as very small: 33 Python files and about 9,000 lines in its package. ADR-008 already covers linting with `ruff` and secret checks with a regex scan.

## Decision

We will not use SonarQube. It is disproportionate to the size of the target repo.

## Consequences

**Positive.** Skipping SonarQube means less setup and faster runs. The missing platform-level analysis is acceptable at the scale of this repo.
