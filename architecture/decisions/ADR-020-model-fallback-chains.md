# 20. Model fallback chains

Covers: D6, D9

Date: 2026-11-23

## Status

Accepted

## Context

ADR-011 and ADR-016 give each role one primary model and one fallback, and ADR-014 waits before the switch. On the fork, the Anthropic key had no credit, every Gemini key shared one project's free tier of about 20 requests per model per day, and OpenRouter's free tier allowed 1,000 requests per day for the whole account. A run that met any of these limits stopped even when another provider could still serve the role. Gemini's rate-limit message contains the words "billing details", so a check for billing text mistook a rate limit for a dead account. The splits of ADR-002 and ADR-011 must hold for every model a role may end up on. Some free models also allow fewer input tokens per minute than a single agent turn needs, and OpenRouter sometimes returns a 4xx when its upstream provider fails. This decision supersedes ADR-016 and amends the single fallback of ADR-014.

## Decision

We will give each role an ordered chain of models: Claude first, then free Gemini models, then free OpenRouter models. Each chain starts with the role's Claude model from ADR-016 (Opus 5.5 for the reviewer, Sonnet 5.5 for the requirements, design and testing agents, Haiku 5.5 for the judge), with ADR-016's prompt caching and output limit on Claude models. A call moves to the next model in the chain after its retries, or at once on a daily limit.

We will check the Anthropic key once per job with a one-token request, and skip a provider for the rest of the job when it answers with an authentication, permission or credit error. A rate limit never marks a provider dead.

We will expand each Gemini model into one entry per key from the secrets `GEMINI_API_KEY` and `GEMINI_API_KEY_2` to `GEMINI_API_KEY_5`. A rate-limited key moves the call to the next key for the same model, and a rejected key is skipped for the rest of the job.

We will keep the reviewer's chain disjoint from the chains of the design, implementation and testing roles, and let the judge skip the model the requirements agent ran on.

We will move to the next model at once when a model's per-minute input-token limit is smaller than one request (as with `gemma-4-26b-a4b-it`'s 16,000 tokens a minute), and when OpenRouter reports that the upstream provider failed the request.

We will read an optional `GEMINI_API_KEY_7`, for a key from a second Google project, which adds its own quota.

## Consequences

**Positive.** A run continues while any allowed model has quota. The reviewer never uses a model that wrote the code, and the judge never grades a spec with the model that wrote it, whichever model each role ends on.

**Negative.** The model that wrote an artifact can change within a run and between issues, so the results depend on which quotas were left when a stage ran, and issues are not comparable model for model. Keys from the same Google project share one quota, so extra keys help only when a key is rejected. Late in the chain sit weaker free models, which are more likely to stop on step caps than finish.

**Neutral.** Every artifact records the model that produced it, so the mix is visible in `state.json` and the run logs.
