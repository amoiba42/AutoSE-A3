# AutoSE

A GitHub Actions workflow in which agents turn an issue into a tested, independently reviewed pull request. A human merges; the workflow never does.

## Fork URL and commit

| | |
|---|---|
| Fork (test space) | https://github.com/amoiba42/markdown |
| Target repo and pinned commit | Python-Markdown [`3f2c551`](https://github.com/amoiba42/markdown/commit/3f2c551) |
| Workflow added on top of the pin | [`99b30ed`](https://github.com/amoiba42/markdown/commit/99b30ede952d99785dd9d56d12e82f50363a052e) (AutoSE workflow and `ARCHITECTURE.md` on `3f2c551`) |
| Frozen workflow used for the final runs | [`e51b70d`](https://github.com/amoiba42/markdown/commit/e51b70debf4613eafc87201287b4e764b59ab2db), copied in [`workflow/`](workflow/) |
| Commit used for every D8 experiment run | tag `d8-experiment` ([`846d3f2`](https://github.com/amoiba42/markdown/commit/846d3f2)) |

## Models

Every role walks an ordered chain: Claude first, then free Gemini models, then free OpenRouter models. A call moves to the next model after its retries, or at once on a daily limit ([ADR-020](architecture/decisions/ADR-020-model-fallback-chains.md)). The chains are defined in [`config.py`](workflow/.github/autose/config.py).

| Role | Chain, in order |
|---|---|
| Requirements | `claude-sonnet-5-5` → `gemini-3.5-flash-lite` → `gemini-3.1-flash-lite` → OpenRouter `nemotron-3-ultra-550b-a55b` → `gemini-3.6-flash` |
| Design + implementation | `claude-sonnet-5-5` → `gemini-3.5-flash` → `gemini-3.8-flash` → `gemini-3-flash-preview` → OpenRouter `nemotron-3-ultra-550b-a55b` → `gemini-3.6-flash` → `gemini-3.1-flash-lite` → `gemini-3.7-flash` → `gemma-4-26b-a4b-it` |
| Testing | `claude-sonnet-5-5` → `gemini-3-flash-preview` → `gemini-3.6-flash` → `gemini-3.5-flash` → OpenRouter `nemotron-3-ultra-550b-a55b` → `gemini-3.8-flash` → `gemini-3.1-flash-lite` → `gemini-3.7-flash` → `gemma-4-26b-a4b-it` |
| Testability judge | `claude-haiku-5-5` → `gemini-3.8-flash` → `gemini-3.6-flash` → `gemini-3.1-flash-lite` → `gemini-3.5-flash-lite` (skips the model the requirements agent ran on) |
| Reviewer | `claude-opus-5-5` → `gemini-4-hydrogen` → `gemma-4-31b-it` → OpenRouter `gemma-4-31b-it` → OpenRouter `nemotron-3.5-super-vl` → OpenRouter `ling-3.2-flash` → `gemini-3.5-flash-lite` (no model shared with design, implementation or testing) |

The Anthropic key had no credit, so no role ran on Claude; every run used Gemini and OpenRouter models. The model each stage actually used is recorded per issue in [`results/runs.md`](results/runs.md). Experiment runs pin one model per role ([`experiment/variants.md`](experiment/variants.md)).

## How to trigger the workflow

One-time setup of the fork (labels, secrets, branch protection) is in [`workflow/README.md`](workflow/README.md).

| Trigger | Who | How |
|---|---|---|
| Label | users with triage or write access | add the label `autose` to an issue |
| Comment | owner, members and collaborators | comment `/autose` on an issue (not a pull request) |
| Manual | users with write access | `gh workflow run autose -R amoiba42/markdown -f issue=<n>`; add `-f restart_from=<1-4>` to redo the issue from that stage |

Follow a run through the issue's "AutoSE status" comment, the run's artifact `autose-issue-<n>`, the pull request, and the review comment and label on it.

## Repo structure

| Path | Contents |
|---|---|
| [`README.md`](README.md) | Fork URL and commit, models, and how to trigger the workflow |
| [`report.pdf`](report.pdf) | Project report |
| `demo.mp4` | Demo video, or a link in this README (to add) |
| [`architecture/views/`](architecture/views/) | [Component view](architecture/views/component_view.mmd), [sequence view](architecture/views/sequence_view.mmd), [stage map](architecture/views/stage_map.md), [agent contracts](architecture/views/contracts.md) |
| [`img/`](img/) | Rendered [component view](img/component_view.png) and [sequence view](img/sequence_view.png) |
| [`architecture/decisions/`](architecture/decisions/) | One ADR per decision, superseded ones kept; [index](architecture/decisions/README.md) |
| [`workflow/`](workflow/) | Copy of [`.github/workflows/`](workflow/.github/workflows/), all [agent code](workflow/.github/autose/) and [prompts](workflow/.github/autose/prompts/) |
| [`experiment/issues/`](experiment/issues/) | The 5 issue texts |
| [`experiment/hidden_tests/`](experiment/hidden_tests/) | Hidden tests |
| [`experiment/seeded_prs/`](experiment/seeded_prs/) | The 5 reviewer-check PRs: diffs and [labels](experiment/seeded_prs/README.md) |
| [`experiment/variants.md`](experiment/variants.md) | What each decision-experiment variant changes |
| [`results/results.csv`](results/results.csv) | Results per issue |
| [`results/experiments.csv`](results/experiments.csv) | Results per experiment run |
| [`results/runs.md`](results/runs.md) | The runs, PRs and reviews behind each result |
| [`results/old_runs.md`](results/old_runs.md) | Every other run (stopped, superseded or cancelled), with what it showed and the change it led to |
| [`results/README.md`](results/README.md) | Column meanings and the counts behind the report |
| [`updated_files/ARCHITECTURE.md`](updated_files/ARCHITECTURE.md) | Architecture file from A2 |
| [`updated_files/skills.md`](updated_files/skills.md) | A1 requirements skill, adapted for the workflow |

## AI assistance

All the architecture and design decisions are mine. Claude Code (Anthropic) was used as a coding assistant: for the [workflow and agent code](workflow/), the adapted [A1 skill](updated_files/skills.md), the [seeded PRs and their notes](experiment/seeded_prs/). I reviewed all of it.
