# Earlier runs

Every main-workflow run on the test fork that is not listed in [`runs.md`](runs.md): runs that stopped, were superseded by a later run, or were cancelled. They show how the workflow reached the version in `workflow/`. Each stop that led to a change names the ADR that records the change. Decision-experiment runs (D8, D1) are in [`experiments.csv`](experiments.csv).

Base URL for every run: `https://github.com/amoiba42/markdown/actions/runs/<id>`.

## All issues at once (2026-11-22)

| Run | Issue | Outcome | Led to |
|---|---|---|---|
| [45049141883](https://github.com/amoiba42/markdown/actions/runs/45049141883) to [45051285954](https://github.com/amoiba42/markdown/actions/runs/45051285954), including [45051275915](https://github.com/amoiba42/markdown/actions/runs/45051275915) | #2 to #6 | Every issue stopped in Stage 1 or 2 on Gemini free-tier quotas or 503s. None reached Release. | One issue at a time; waits on 429/503 (ADR-014) |

## #2 Closing hashes (bug, never completed)

| Run | Outcome | Led to |
|---|---|---|
| [45053283898](https://github.com/amoiba42/markdown/actions/runs/45053283898) | Stage 1 passed; Stage 2 stopped on the fallback model's daily quota | Model fallback chains (ADR-020) |
| [45053966082](https://github.com/amoiba42/markdown/actions/runs/45053966082) | G2 failed: the design targeted a class attribute (`HashHeaderProcessor.RE`) the symbol lookup could not resolve | G2 correction (ADR-018) |
| [45059313796](https://github.com/amoiba42/markdown/actions/runs/45059313796) | Stopped at once: Anthropic key has no credit | Claude skipped when it has no credit (ADR-020) |
| [45060103657](https://github.com/amoiba42/markdown/actions/runs/45060103657) | G4 failed 3 times: every fix broke 8 existing tests that pin closed headings. The Stage 2 redo hit its 30-step cap. Gates, retries and send-backs worked as designed | Prompts treat existing tests as the contract; design cap 30 → 45 (ADR-023) |
| [45081907868](https://github.com/amoiba42/markdown/actions/runs/45081907868) | Stage 3 fell back to gemma-4-26b, whose 16k tokens-per-minute limit is smaller than one agent turn | Switch model at once on small per-minute limits (ADR-020) |
| [45086146435](https://github.com/amoiba42/markdown/actions/runs/45086146435) | Cancelled by a GitHub runner shutdown | — |
| [45093961768](https://github.com/amoiba42/markdown/actions/runs/45093961768) | Full retry ladder again. Root cause: the issue still used a Stage 1 spec written before the "existing tests are the contract" prompt | `restart_from` input (ADR-024) |

The last attempt, [45096311557](https://github.com/amoiba42/markdown/actions/runs/45096311557), is in `runs.md`.

## #3 Blank wikilink (bug, completed as PR #9)

| Run | Outcome | Led to |
|---|---|---|
| [45062762557](https://github.com/amoiba42/markdown/actions/runs/45062762557) | Stage 1 passed; the design agent ran 41 steps and hit the 1.5M-token stage cap | Token caps 1.5M/6M → 3M/15M (ADR-023) |
| [45064355691](https://github.com/amoiba42/markdown/actions/runs/45064355691) | Full retry ladder ran (3→4 twice, Stage 2 redo, 3→4) and stopped: the implementation never met two criteria. Routing and caps worked as designed | — |
| [45067801276](https://github.com/amoiba42/markdown/actions/runs/45067801276) | Stopped on daily quotas | — |

## #4 Scheme autolinks (feature, completed as PR #8)

| Run | Outcome | Led to |
|---|---|---|
| [45064426078](https://github.com/amoiba42/markdown/actions/runs/45064426078) | Stage 3 hit the 3M-token cap in 28 steps, about 113k tokens per step, because whole-file outputs were resent every step | 10,000-character output cap (ADR-023) |
| [45065675437](https://github.com/amoiba42/markdown/actions/runs/45065675437) | Stage 3 hit the 60-step cap after about 40 steps re-checking one criterion | Prompt: check each criterion at most twice |
| [45066458963](https://github.com/amoiba42/markdown/actions/runs/45066458963) | Stage 3 wrote its summary at step 59 of 60, then hit the cap | Implementation cap 60 → 90 (ADR-023) |
| [45067139467](https://github.com/amoiba42/markdown/actions/runs/45067139467) | Stage 3 finished; Stage 4 stopped on OpenRouter's account-wide daily limit | Daily-limit detection covers OpenRouter's wording (ADR-020) |
| [45068613410](https://github.com/amoiba42/markdown/actions/runs/45068613410) | Stopped in Stage 4: every Gemini model with tool calls out of daily quota | More Gemini models in the chains (ADR-020) |
| [45072002404](https://github.com/amoiba42/markdown/actions/runs/45072002404) | Stages 1–4 passed, PR #8 opened, CI green. Review round 1 requested changes: new processor at priority 105, below automail (110). Route re-entered at Stage 3 | Review round 2 |
| [45074534442](https://github.com/amoiba42/markdown/actions/runs/45074534442) | Round-2 re-entry: G3 failed 3 times on unsorted imports in a new test | G3 message names `ruff check --fix`; review findings kept until their stage passes |
| [45074994586](https://github.com/amoiba42/markdown/actions/runs/45074994586) | The implementer edited an existing test; G4 caught it three times | G3 rejects edits to existing tests |
| [45076805093](https://github.com/amoiba42/markdown/actions/runs/45076805093) | Stage 4 stopped on the gemini-3.1-flash-lite daily quota | — |
| [45080036391](https://github.com/amoiba42/markdown/actions/runs/45080036391) | Stage 4 stopped again on the same quota | More writer models in the chains (ADR-020) |

## #5 Wikilink label (feature, completed as PR #7)

| Run | Outcome | Led to |
|---|---|---|
| [45062691403](https://github.com/amoiba42/markdown/actions/runs/45062691403) | First run to reach Release; the push failed | Release keeps only git's error output (ADR-027) |
| [45063751078](https://github.com/amoiba42/markdown/actions/runs/45063751078) | First PR (#7). G5 failed: the implementer's own test failed, and CI exited 1 on a known upstream collection error | Strict G4 (ADR-022); CI ignores that one error (ADR-021) |
| [45065600627](https://github.com/amoiba42/markdown/actions/runs/45065600627) | Restarted at Stage 4. The new G4 caught the failing test and sent it back to Stage 3, which fixed it; Release merged the base and CI passed. Review stopped: no reviewer model answered | Release merges base (ADR-021); longer reviewer chain (ADR-020) |
| [45067740812](https://github.com/amoiba42/markdown/actions/runs/45067740812) | Stopped on daily quotas | — |
| [45068585987](https://github.com/amoiba42/markdown/actions/runs/45068585987) | Stopped in Stage 4 within 3 minutes: Gemini quota spent | More Gemini models in the chains (ADR-020) |

## #6 TOC for non-English docs (vague, completed as PR #15)

| Run | Outcome | Led to |
|---|---|---|
| [45076688539](https://github.com/amoiba42/markdown/actions/runs/45076688539) | Stage 1 passed with recorded assumptions (two-tier vague handling, ADR-013); Stage 2 passed; Stage 3 stopped on the daily quota | — |
| [45086166354](https://github.com/amoiba42/markdown/actions/runs/45086166354) | Cancelled by a GitHub runner shutdown | — |
| [45093973179](https://github.com/amoiba42/markdown/actions/runs/45093973179) | Stages 1–4 passed, PR #15 opened, CI green. Review stopped on an OpenRouter 422 the chain could not switch past | OpenRouter 422 made switchable; review-only re-run |

## Clean reruns (frozen commit e51b70d)

| Run | Issue | Outcome |
|---|---|---|
| [45189596189](https://github.com/amoiba42/markdown/actions/runs/45189596189) | #18 (same text as issue-3) | Cancelled by the user when no quota or time was left |

The two clean reruns that ran to a stop (#16, #17) are in `runs.md`.
