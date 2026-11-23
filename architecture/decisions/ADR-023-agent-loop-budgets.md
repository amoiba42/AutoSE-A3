# 23. Agent loop budgets

Covers: D5, D9

Date: 2026-11-23

## Status

Accepted

## Context

ADR-006 caps each agent stage in tokens, tool calls and wall-clock time. With mini-swe-agent every command's output stays in the conversation and is sent again on every later step, so agents that print whole files used over 100,000 tokens per step and hit the token cap in under 30 steps. The earlier step caps were 25 for requirements and 60 for implementation. Free models needed many steps: one implementer finished its work at step 59 of 60, and in a pilot most requirements agents used all 25. On issue #2, a spec that was narrowed in its criteria still widened the scope through an assumption, every attempt broke existing tests that pin the current behaviour, and one implementer spent 40 steps re-checking a single criterion. This decision amends ADR-006 and ADR-010.

## Decision

We will keep at most 10,000 characters of one command's output in the conversation, the start and the end, with a note on how to read the rest.

We will raise the caps to 3 million tokens per stage, 15 million per run, 40 steps for requirements, 45 steps for design and 90 steps for implementation, and keep 40 steps for testing and review.

We will tell the requirements, design and implementation agents that existing tests define behaviour that must not change, ask the design agent to work in about 15 commands, and tell the implementer to check each criterion at most twice.

We will have the requirements agent give each behaviour that an existing test pins near the change its own criterion, with that test's input and expected output, and not write assumptions that widen the scope.

## Consequences

**Positive.** Cutting long command outputs keeps each step small, so a stage does not hit the token cap after a few file reads. The larger step caps let slower free models finish work they had nearly completed. The existing-tests rule keeps a spec to the cases the issue names.

**Negative.** An agent may need a second command to read the part of a long output it wants. Larger caps let a stuck agent run longer and spend more before it stops. Prompt rules rely on the model following them; an implementer can still make a general change that breaks tests pinning current behaviour.

**Neutral.** The caps are the same for every model in a role's chain, so a weaker model late in the chain gets no extra room.
