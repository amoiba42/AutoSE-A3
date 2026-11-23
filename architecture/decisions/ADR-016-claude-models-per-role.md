# 16. Claude model tiers

Covers: D6

Date: 2026-11-23

## Status

Superseded by ADR-020. The Anthropic key had no credit, so these models never ran.

## Context

ADR-011 runs every role on free Gemini models. In the runs on the fork, the free tier's per-minute and per-day limits stopped every issue before Release, and ADR-014 and ADR-015 only made those stops shorter or easier to read. A paid Anthropic API key is now available to the workflow as the `ANTHROPIC_API_KEY` secret. ADR-010 calls models through LiteLLM, which reaches the Anthropic API with an `anthropic/` model prefix.

The roles differ in how much a weak answer costs. The reviewer is the last check before a human sees the pull request (ADR-002). The requirements, design, implementation and testing agents produce the artifacts that every later check depends on. The testability judge answers yes or no for each acceptance criterion. ADR-002 keeps the reviewer off every model used by an agent that writes code, and ADR-011 keeps the judge off the model that wrote the spec. Claude Opus 5.5 costs $4 and $20 per million input and output tokens, Claude Sonnet 5.5 $2 and $10, and Claude Haiku 5.5 $0.10 and $0.50.

## Decision

We will run the reviewer on Claude Opus 5.5.

We will run the requirements, design and implementation, and testing agents on Claude Sonnet 5.5.

We will run the testability judge on Claude Haiku 5.5.

We will keep one fallback per role, from a model the role's splits allow. The requirements agent falls back to Claude Haiku 5.5, the design and testing agents to the OpenRouter model in `AUTOSE_FALLBACK_MODEL`, the judge to `gemini-3.8-flash`, and the reviewer to `gemini-4-hydrogen`. When the requirements agent ends on the judge's model, the judge uses its own fallback, as in ADR-011.

We will turn on Anthropic prompt caching for agent conversations on Claude models and allow up to 16,000 output tokens per response.

We will keep variant B of experiment 1 as defined in ADR-011.

## Consequences

**Positive.** The tiering puts the strongest model where a mistake is costly (the reviewer) and the cheapest where the task is a yes/no judgment (the judge). The splits of ADR-002 and ADR-011 hold for every fallback.

**Negative.** Claude is paid per token, and the reviewer on Opus is the most expensive role per step. All primary agents in this plan share one model family, so the reviewer's independence would rest on its model tier, prompt and inputs rather than on a different provider.

**Neutral.** Every role depends on one provider's billing, so an empty account stops all roles at once.
