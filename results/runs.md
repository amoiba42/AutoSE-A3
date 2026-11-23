# Runs

Test fork: https://github.com/amoiba42/markdown. Every link below is a real GitHub Actions run or pull request.
This file lists the runs behind each result. Every other run (stopped, superseded or cancelled) is in [`old_runs.md`](old_runs.md), with what it showed and the change it led to.

## Issues completed end to end

An issue is complete when all six stages ran, the independent review approved the pull request (or two review rounds were used), and the route job posted the hand-off comment. The workflow never merges.

| Issue | Pull request | Review rounds | Final run | Verdict | Other runs in the story |
|---|---|---|---|---|---|
| #5 Wikilinks custom label | [PR #7](https://github.com/amoiba42/markdown/pull/7) | 1 | [45069192202](https://github.com/amoiba42/markdown/actions/runs/45069192202) | approve | none |
| #3 Blank `[[ ]]` disappears | [PR #9](https://github.com/amoiba42/markdown/pull/9) | 2 | [45079974897](https://github.com/amoiba42/markdown/actions/runs/45079974897) | round 1 changes requested (design), round 2 approve | round 1 [45073862168](https://github.com/amoiba42/markdown/actions/runs/45073862168); re-entry at Stage 2 [45075733053](https://github.com/amoiba42/markdown/actions/runs/45075733053) |
| #6 Vague: TOC for non-English docs | [PR #15](https://github.com/amoiba42/markdown/pull/15) | 1 | [45101838429](https://github.com/amoiba42/markdown/actions/runs/45101838429) | approve | review-only re-run |
| #4 Scheme autolinks (`<tel:...>`) | [PR #8](https://github.com/amoiba42/markdown/pull/8) | 2 | [45081398796](https://github.com/amoiba42/markdown/actions/runs/45081398796) | round 1 changes requested (code), round 2 approve | none |

## Earlier stops and their fixes

Each stop below led to a change in the workflow (ADR in brackets). The full list of limits and rules, with the run that showed each one, is in `architecture/decisions/` and `experiment/variants.md`.

| Stop | Fix |
|---|---|
| Five issues started at once on one key; all stopped in Stages 1–2 on quota or overload errors | One issue at a time; waits and key rotation [ADR-014] |
| Stage caps reached (design 30 steps, implementation 60, requirements 25; output about 113k tokens per step) | Higher step caps and a 10,000-character output limit [ADR-023] |
| G4 let an implementer's failing test reach a PR (#5, PR #7) | G4 fails on any new test failure [ADR-022] |
| CI failed on one known upstream collection error | CI ignores that error only [ADR-021] |
| A rate-limit message was read as a dead provider | Rate limits no longer mark a provider dead [ADR-020] |

Issue #2 (closing hashes) never completed. Its implementation failed G4 on every attempt because the change conflicts with 8 existing tests. The retry ladder ran out ([45096311557](https://github.com/amoiba42/markdown/actions/runs/45096311557)).

## Models used

Each role has an ordered chain of models (`workflow/.github/autose/config.py`; see [ADR-020](../architecture/decisions/ADR-020-model-fallback-chains.md)). A call uses the first model in the chain that still has quota, so the model behind a role depends on which free-tier quotas were left when the run started. Claude models were first in every chain but were never used: the Anthropic key had no credit, which the workflow detects at the start of each job.

Models in the final, successful run of each issue (from `state.json` `models_used` in the `autose-issue-N` artifact, and the `reviewer:` line of the review job log):

| Role | #5 (PR #7) | #3 (PR #9) | #4 (PR #8) | #6 (PR #15) |
|---|---|---|---|---|
| Requirements (Stage 1) | gemini-3.5-flash-lite | gemini-3.5-flash-lite | gemini-3.5-flash-lite | gemini-3.5-flash-lite |
| Testability judge (G1) | gemini-3.8-flash | gemini-3.6-flash | gemini-3.6-flash | gemini-3.8-flash |
| Design (Stage 2) | OpenRouter nemotron-3-ultra-550b (free) | gemini-3.1-flash-lite | gemini-3.1-flash-lite | gemini-3.1-flash-lite |
| Implementation (Stage 3) | OpenRouter nemotron-3-ultra-550b (free) | gemini-3.1-flash-lite | gemini-3.1-flash-lite | OpenRouter nemotron-3-ultra-550b (free) |
| Tester (Stage 4) | gemini-3.1-flash-lite | gemini-3.1-flash-lite | gemma-4-26b-a4b-it (last phase) | OpenRouter nemotron-3-ultra-550b (free) |
| Independent reviewer (Stage 6) | gemini-3.5-flash-lite | gemini-3.5-flash-lite | gemini-3.5-flash-lite | gemini-3.5-flash-lite |

Notes:

- `models_used` keeps only the last model per stage. Earlier attempts on the same issue used other models; for example, the earlier rounds of #3 and #4 ran Stages 2 and 3 on OpenRouter nemotron-3-ultra. Each run's orchestrator log has one `stageN: {... 'model': ...}` line per agent call.
- In every run the reviewer's chain shares no model with the design, implementation and tester chains, and the judge skips the model the requirements agent ran on.
- Models differ between issues, so compare results across issues with that in mind.

## Hidden tests

Run locally on 2026-11-22 against the head of each AutoSE branch (the final pull request commit). The hidden tests are numbered by issue file: fork #3 = `test_issue2_wikilink_blank.py`, #4 = `test_issue3_autolink.py`, #5 = `test_issue4_wikilink_label.py`, #6 = `test_issue5_vague_toc.py`.

| Issue | PR | Commit | Hidden tests | Full suite |
|---|---|---|---|---|
| #5 | #7 | 3516c1f | 4 / 4 | passes (only the known upstream collection error) |
| #4 | #8 | 8dbf509 | 4 / 4 | passes (only the known upstream collection error) |
| #3 | #9 | c0666e5 | 4 / 4 | passes (only the known upstream collection error) |
| #6 (vague) | #15 | b932103 | 4 / 4 | passes (only the known upstream collection error) |

`results.csv` notes: `tokens` is the orchestrator's cumulative `run_total` from `state.json` over all runs of the issue. Review jobs are not included. `wall_seconds` is blank because the runs were spread over many hours of quota waits.

## Clean reruns (fork commit e51b70d)

Fresh copies of the first issues, run one at a time with no tooling changes. Their results are in the report's Results section.

| Issue | Same text as | Final run | Outcome |
|---|---|---|---|
| #16 | issue-1 (closing hashes) | [45178313377](https://github.com/amoiba42/markdown/actions/runs/45178313377) | stopped at Stage 2: design agent TimeExceeded (Gemini 503 "high demand" on every key) |
| #17 | issue-2 (blank wikilink) | [45183576640](https://github.com/amoiba42/markdown/actions/runs/45183576640) | stopped at Stage 2: design agent used all 45 steps (Gemini writers out of quota, fell back to OpenRouter) |
| #18 | issue-3 (scheme autolinks) | see [`old_runs.md`](old_runs.md) | cancelled by the user at 14:05 UTC, when no quota or time was left |

The clean reruns stopped after #18: Gemini's free quota on the GitHub keys was used up, and OpenRouter's free model could not finish the design stage within its cap. Fork #19 was not started. Fork #20 was used only for the D1 requirements-prompt experiment (see `experiments.csv`).
