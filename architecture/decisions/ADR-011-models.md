# 11. Models per role

Covers: D6

Date: 2026-11-22

## Status

Proposed

## Context

ADR-001 defines four agents. ADR-002 requires the reviewer to use a different model from the agents that write code. ADR-007 uses an LLM for the Stage 1 testability judgment, and a judge that uses the spec author's model grades its own work. ADR-010 calls models through LiteLLM, so any provider works.

The project uses free model tiers only. Over 30 to 50 runs, the coding agents need roughly 1,500 to 5,000 requests. As checked on 2026-11-22:
- Google AI Studio lists `gemini-4-hydrogen`, `gemini-3.8-flash` and `gemini-3.5-flash-lite`. Free-tier limits apply per model and per project, reset daily, and are shown only in AI Studio. Long agent histories make the per-minute token limit the likely bottleneck.
- The Qwen text models on NVIDIA NIM's free hosted service are deprecated, and NIM's credit system ended in September 2025.
- OpenRouter's free Qwen models allow about 50 requests a day. Alibaba Model Studio gives about 1M tokens per model.

Models of the same family share blind spots, so a single-family setup weakens one of the reviewer's safeguards.

## Decision

We will use Gemini for every role in the baseline, with a different model per role.

| Role | Model (baseline) |
|---|---|
| Design + implementation | `gemini-3.8-flash` |
| Testing | `gemini-3.6-flash` |
| Stage 1 testability judge | `gemini-3.8-flash` |
| Requirements | `gemini-3.5-flash-lite` |
| Reviewer | `gemini-4-hydrogen` |

No agent that writes code uses the reviewer's model, and the Stage 1 judge does not use the requirements agent's model.

We will test a second family in an experiment. In that variant, the reviewer and the Stage 1 judge use a free Qwen model through OpenRouter, and every other role keeps its baseline model.

We will use free tiers only, with no billing account linked to any provider.

On a rate-limit error, we will fall back once to another free Gemini model that keeps both splits above. If the fallback is also limited, the stage stops under ADR-006.

TODO(me): Confirm in AI Studio that each baseline model, including `gemini-3.6-flash`, is on the free tier, and pin the exact OpenRouter Qwen model ID for the variant.

## Consequences

**Positive.** The workflow costs nothing to run.

**Negative.** Free-tier rate limits, especially per-minute token limits, can stop runs. Free models get retired, which hurts reproducibility. In the baseline every agent shares the Gemini family, so the reviewer's independence rests on its model, prompt and inputs, not on its family; the experiment measures what this costs.

**Neutral.** Free models are weaker than paid ones. This lets us test smaller models instead of state-of-the-art ones, which handled most tasks in small repos well in A2.
