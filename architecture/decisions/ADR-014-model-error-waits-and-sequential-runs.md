# 14. Waits and sequential runs

Covers: D6, D9, D10

Date: 2026-11-22

## Status

Accepted. Amended by ADR-018 (at most three retries of at most 60 seconds) and ADR-020 (a chain of fallbacks instead of one).

## Context

The agents use free-tier Gemini models (ADR-011). Those models limit requests per minute, input tokens per minute and requests per day, and they sometimes answer with a 503 when demand is high. ADR-011 sends a rate-limit error to one fallback model, and ADR-006 stops the stage if that also fails. In the first runs on the fork, five issues started at once and shared one API key. Four of them stopped in Stage 1 on a 429 or a 503, and none reached Release.

A short fixed wait does not help when several runs start together, because they wait the same time and fail together again. A per-minute limit clears if a run waits. A per-day limit does not clear within a run, so waiting only delays the stop. The error text states which limit was hit and often how long to wait. A GitHub concurrency group keeps one pending run and cancels the others, so it cannot queue many issues. ADR-005 lets runs for different issues run in parallel. This decision amends ADR-005, ADR-006 and ADR-011.

## Decision

We will treat a 429 and a 503 from a model as transient errors and wait before the call is retried on the same model.

We will take the wait from the delay the error gives, and use at least an exponentially growing wait of 5, 10, 20 and 40 seconds. Each wait will be at most 90 seconds and will carry random jitter of 0 to 50 percent. We will retry a call at most four times on one model.

We will not retry when the error names a per-day limit. The call moves at once to the fallback model of ADR-011.

We will keep ADR-011's single fallback. When the fallback model also fails after its retries, the stage stops under ADR-006.

We will start issues one at a time with a script that dispatches the workflow, waits for the run to finish, and pauses 60 seconds before the next issue. We will not queue issues with a workflow-level concurrency group.

## Consequences

**Positive.** Short per-minute limits and brief overloads no longer end a run: the call waits and goes on. A daily limit skips the useless waiting and moves to the fallback at once.

**Negative.** Runs take longer, because a call can wait several times before it gives up. Starting issues one at a time keeps the per-minute limits clear but makes a batch of five issues take hours on free tiers. With one Gemini fallback, a daily limit on both Gemini models still stops a run.

**Neutral.** The wait is read from the provider's error text. If a provider changes that text, the call falls back to the exponential wait, which still works but may wait longer than needed.
