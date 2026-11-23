# Results

| File | Contents |
|---|---|
| [`results.csv`](results.csv) | One row per completed issue (#3 to #6): stages passed, hidden tests, tokens, final run link. Issue #2 never completed and has no row. `tokens` excludes review jobs; `wall_seconds` is blank because quota waits made wall-clock time meaningless. |
| [`experiments.csv`](experiments.csv) | One row per decision-experiment run: D8 (reviewer independence), D1 (requirements prompt), and the D1 pilot. |
| [`runs.md`](runs.md) | The runs, pull requests and reviews behind each result. |
| [`old_runs.md`](old_runs.md) | Every other main-workflow run: stopped, superseded or cancelled, with what each showed and the change it led to. |

## `experiments.csv` columns

| Column | Meaning |
|---|---|
| `experiment` | `D8`, `D1`, or `D1-pilot`. **`D1-pilot` rows are not valid for comparison.** They are the earlier OpenRouter-pinned attempt that hit step caps and rate limits. Use only `D1` and `D8` rows for conclusions (see [`experiment/variants.md`](../experiment/variants.md)) |
| `subject` | Seeded PR `s1` to `s5`, real AutoSE PR `pr7` to `pr9`, or fork issue `issueN` |
| `variant` | D8: `blind` or `notes`. D1: `skill` or `bare` |
| `rep` | Repetition number |
| `expected` | Seeded PRs only: `approve` for clean seeds, `changes_requested` for defective ones |
| `verdict` | Reviewer verdict (D8) |
| `outcome` | Run state: `reviewed`, `stopped: ...`, `error: ...`, or `cancelled` |
| `n_findings`, `findings` | Count and `category/severity` of findings |
| `g6` | Result of the G6 evidence check on the review |
| `model` | Pinned model for the role under test (requirements agent for D1; reviewer for D8) |
| `judge_model` | Testability judge model for D1 rows (`gemini/gemini-3.8-flash`; pilot: `openrouter/ling-3.2-flash`, per `variants.md`). Blank for D8, and for the D1 row that stopped before the judge ran |
| `tokens` | Tokens used by the run. Blank when the run was cancelled before reporting |
| `run_url` | Actions run |

## Counts behind the report

These were recomputed from `experiments.csv` and match the figures in the report.

| Experiment | Runs | Tokens |
|---|---|---|
| D8 (blind and notes) | 26 | 534,196 |
| D1 (skill and bare, final) | 9 | 2,277,234 |
| D1-pilot | 10 | 2,311,845 |

D8 per variant, over the 2 repetitions of the 3 defective seeds (`s2`, `s3`, `s5`) and 2 clean seeds (`s1`, `s4`):

| Variant | Defective reviews caught | False alarms on clean seeds | Real PRs `pr7` / `pr8` / `pr9` |
|---|---|---|---|
| blind | 3 of 6 | 0 of 4 | approve / approve / changes requested |
| notes | 1 of 6 | 0 of 4 | approve / approve / approve |

The seeded defect `s5` was missed in every review. Samples are small (2 reps per seed), so treat the 3-of-6 versus 1-of-6 gap as a direction, not a measured effect.
