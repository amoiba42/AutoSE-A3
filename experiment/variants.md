# Decision experiments

Each experiment changes one decision and holds everything else fixed. Both run in the separate, manually started workflow
`autose-experiment.yml`, which posts nothing and keeps no issue state. Every model is pinned to one model per role,
so the main workflow's fallback chain cannot change models between variants (ADR-026).

Results: `results/experiments.csv`.

## Overview

| | D8: Reviewer independence | D1: Requirements prompt |
|---|---|---|
| Decision tested | ADR-002 | ADR-001, ADR-013 |
| What changes | Reviewer's input | Requirements agent's system prompt |
| Variants | blind, notes | skill, bare |
| Status | Complete (26 runs) | Minimal run on the vague issue: specs written, no judge verdict |

## D8: Reviewer independence

### Variants

| Variant | Reviewer receives |
|---|---|
| **blind** (as built) | Issue, diff, repository at the PR commit, test results |
| **notes** | Same as blind, plus the implementer's design and attempt summary |

### Setup

| Setting | Value |
|---|---|
| Commit | Tag `d8-experiment` (846d3f2) for all runs |
| Reviewer model | `gemini/gemini-3.5-flash-lite` |
| Subjects | Seeded S1–S5 (2 approve, 3 changes requested); AutoSE PRs #7, #8, #9 |
| Repetitions | 2 per subject and variant |
| Held fixed | Reviewer prompt, caps, G6 evidence check |
| Measures | Catch rate on the 3 defective seeds; false alarms on the 2 clean seeds; verdict agreement with blind; number and severity of findings; G6 evidence validity; tokens |

### Hypothesis

The reviewer that also reads the implementer's design and attempt summary (notes) approves more defective PRs than the blind reviewer. The notes give a plausible account of each change, and the reviewer accepts that account instead of checking the diff against the issue. If this holds, independence is worth its cost in context. If the two variants catch the same defects, the blind reviewer gives no advantage and ADR-002 should be reconsidered.

## D1: Requirements prompt (A1 skill)

### Variants

| Variant | Requirements agent's system prompt |
|---|---|
| **skill** (as built) | Adapted A1 skill (`prompts/a1_skill.md`) plus run instructions |
| **bare** | Two-sentence role statement (`prompts/requirements_bare_system.md`) |

### Setup

| Setting | Value |
|---|---|
| Scope | Stage 1 only |
| Subjects | Fork #20 (same text as vague #6) |
| Requirements model | `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` |
| Judge model | `gemini/gemini-3.8-flash` |
| Repetitions | 2 per variant (4 runs) |
| Held fixed | Task prompt (`prompts/requirements.md`), output schema, G1 structure check, testability judge |
| Measures | G1 outcome (passed, re-asked, stopped); testable count; criteria and assumptions count; vague-issue handling (rejected or specified with assumptions); criteria matched by hand to `experiment/hidden_tests/` |

### Status

| Item | State |
|---|---|
| Earlier attempt (OpenRouter pins) | Invalid: step caps and rate limits, logged as `D1-pilot` in `results/experiments.csv` |
| Test run (Gemini pins) | One run on fork #16 (same text as #2): stopped on Gemini 503 errors before a spec |
| Minimal run (4 runs, #20) | All four wrote a spec and none rejected the vague issue. skill: 5 and 5 criteria, 1 and 4 assumptions, 413k and 562k tokens. bare: 5 and 4 criteria, 3 and 2 assumptions, 311k and 456k tokens. The judge's daily free quota ran out, so no G1 verdict |
| Repeat on #20 (4 runs, reps 3–4) | All four stopped before a spec: the requirements agent hit OpenRouter's daily free-model limit |

### Hand match against hidden tests (`hidden_tests/test_issue5_vague_toc.py`)

Each spec's acceptance criteria were read against the 4 hidden tests. A test counts as covered when some criterion states the behaviour it checks.

| Hidden test | skill r1 | skill r2 | bare r1 | bare r2 |
|---|---|---|---|---|
| CJK ids distinct, not `_1`/`_2` | AC-1 | AC-1 | AC-1 | AC-1 |
| TOC links match heading ids | AC-1 | AC-1 | AC-4, AC-5 | AC-1 |
| ASCII heading unchanged (`hello-world`) | AC-2 | AC-5 | AC-2 | AC-4 |
| Duplicate CJK headings get unique ids | AC-4 | AC-2 | AC-4 | AC-2 |
| **Covered** | **4/4** | **4/4** | **4/4** | **4/4** |

All four specs chose the same reading: keep ASCII slugs, and fall back to Unicode ids when the ASCII slug would be empty. All four also pin extended-Latin headings to their current ASCII form (`theatre`). skill r2 adds one harder criterion: a mixed heading `# Hello 你好` must get `hello-你好`, which a plain empty-string fallback would not produce.

### Hypothesis

The A1 skill makes the requirements agent write more testable acceptance criteria and handle the vague issue more carefully than a bare role prompt, and it costs more tokens. If the skill gives no better spec for its extra cost, the Stage 1 prompt can be simplified without loss. The result matters because the brief asks Stage 1 to reuse the A1 skill, so any reason to drop it has to come from this test.

## Limits and rules learned while building

These are not experiments. Each change was made between runs, on a new commit, in response to one problem a run
showed. No run held everything else fixed, so the tables record what we saw and what we set, not a measured effect.
#n is a fork issue.

### Limits

| Limit | Before | After | What a run showed | Run | ADR |
|---|---|---|---|---|---|
| Issues started at once | all 5 | one at a time | Every issue stopped in Stage 1 or 2 on free-tier limits; none reached Release | [45049141883](https://github.com/amoiba42/markdown/actions/runs/45049141883) to [45051285954](https://github.com/amoiba42/markdown/actions/runs/45051285954) | ADR-014 |
| Design step cap | 30 | 45 | #2: the Stage 2 redo hit the 30-step cap | [45060103657](https://github.com/amoiba42/markdown/actions/runs/45060103657) | ADR-023 |
| Token cap per stage / run | 1.5M / 6M | 3M / 15M | #3: the design agent hit the 1.5M stage cap after 41 steps | [45062762557](https://github.com/amoiba42/markdown/actions/runs/45062762557) | ADR-023 |
| Command output kept in the conversation | whole output | 10,000 characters (head and tail) | #4: Stage 3 hit the 3M cap in 28 steps, about 113k tokens per step | [45064426078](https://github.com/amoiba42/markdown/actions/runs/45064426078) | ADR-023 |
| Implementation step cap | 60 | 90 | #4: Stage 3 wrote its summary at step 59 of 60 | [45066458963](https://github.com/amoiba42/markdown/actions/runs/45066458963) | ADR-023 |
| Requirements step cap | 25 | 40 | D1 pilot: the requirements agent hit the 25-step cap without a spec in 8 runs | [45086893972](https://github.com/amoiba42/markdown/actions/runs/45086893972) (one of the 8) | ADR-023 |
| Retries and wait on 429 / 503 | 4 retries, up to 90 s, inside the wall-clock cap | 3 retries, up to 60 s, outside the wall-clock cap | #3: the round-2 review hit its wall-clock cap after 15 steps while reviewer models were throttled | [45075733053](https://github.com/amoiba42/markdown/actions/runs/45075733053) | ADR-014, ADR-018 |
| Model switch on a per-minute token limit | after retries | at once when the limit is below 100k tokens a minute | #2: gemma's 16k tokens a minute is smaller than one agent turn | [45081907868](https://github.com/amoiba42/markdown/actions/runs/45081907868) | ADR-020 |

### Rules

| Rule | Before | After | What a run showed | Run | ADR |
|---|---|---|---|---|---|
| G4 | baseline passes still pass | no test fails that did not fail at the base commit | #5: the implementer's own failing test reached PR #7 and failed CI | [45063751078](https://github.com/amoiba42/markdown/actions/runs/45063751078) | ADR-022 |
| CI | plain `pytest` | JUnit report; ignores the one known upstream collection error | Same run: CI exited 1 on every commit because of the `test_md_in_html.py` collection error | [45063751078](https://github.com/amoiba42/markdown/actions/runs/45063751078) | ADR-021 |
| Release | push the branch as it is | merge the base branch before the push | #5: after the merge, CI on PR #7 passed | [45065600627](https://github.com/amoiba42/markdown/actions/runs/45065600627) | ADR-021 |
| Provider health | billing text means a dead account | a rate limit never marks a provider dead | Gemini's 429 text says "billing details", which marked Gemini dead | commit [f40d76a](https://github.com/amoiba42/markdown/commit/f40d76a) | ADR-020 |

## Issue numbering

Hidden tests and issue texts in this folder are numbered 1 to 5. On the fork they are issues #2 to #6
(`issue-1` = fork #2, ..., `issue-5` = fork #6).
