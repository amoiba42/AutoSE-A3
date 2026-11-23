# AutoSE workflow

This folder is a copy of the workflow as it lives in the fork of Python-Markdown (`amoiba42/markdown`, commit
`e51b70d`). Everything under `.github/` is identical to that commit. Copy it into the fork's root so the paths match:

```
.github/workflows/autose.yml             # the four jobs: orchestrator, release, review, route
.github/workflows/autose-experiment.yml  # decision experiments (manual, read-only, posts nothing)
.github/workflows/ci.yml                 # CI that Gate 5 checks
.github/autose/                          # orchestrator and job scripts, prompts, requirements.txt
scripts/run_issues.sh                    # helper: dispatch issues one at a time (not part of the fork)
```

The tooling lives under `.github/`, so the Stage 3 scope guard protects it from agent edits.

## One-time setup in the fork

1. Fork `Python-Markdown/markdown`; reset `master` to `3f2c551`; commit `ARCHITECTURE.md` (A2) and this folder.
2. Protect `master` (no direct pushes).
3. Labels: create `autose`, `autose-approved`, `autose-changes-requested`.
4. Secrets (Settings → Secrets → Actions):
   - `GEMINI_API_KEY`, and optionally `GEMINI_API_KEY_2` to `GEMINI_API_KEY_5` and `GEMINI_API_KEY_7`: AI Studio keys,
     free tier. Keys from one Google project share one quota; `_7` is meant for a second project.
   - `OPENROUTER_API_KEY`: free OpenRouter models at the end of every role's model chain.
   - `ANTHROPIC_API_KEY`: optional. Probed once per job; skipped when it cannot serve requests.
   - `AUTOSE_PAT`: fine-grained PAT for the fork only: Contents read/write, Pull requests read/write.
5. Allowing GitHub Actions to create pull requests is not needed (the PAT opens them).

## Trigger

- Add the label `autose` to an issue, or
- comment `/autose` on an issue (owner, members and collaborators only), or
- start `autose` by hand (`workflow_dispatch`) with `issue`, and optionally `restart_from` (1–4) to redo the issue
  from that stage.

## Where things are

| Thing | Where |
|---|---|
| State and stage artifacts | Actions run → artifact `autose-issue-<n>` |
| Status | the issue's "AutoSE status" comment (edited in place) |
| Review | PR comment + label |
| Why a run stopped | the issue's stop comment + `explanation.md` in the run's artifacts |

## Known leftovers in the frozen code

The code under `.github/` is kept exactly as it ran, so these are left in place:

- `config.py` and `autose.yml` still read `AUTOSE_VARIANT` and `AUTOSE_RETRIES` for two experiments that were
  dropped (second-family reviewer; retry caps). With the defaults (`A`, `2`) they change nothing.
- `config.py` and `claude_agent.py` cite ADR-011 and ADR-016, which are superseded (ADR-020 is current).
- `claude_agent.py`, `proxy.py` and the Claude Code parts of `sandbox.py` are the deprecated Claude Code harness
  (ADR-019). They never ran: without Anthropic credit every role uses mini-swe-agent.
- `requirements.txt` does not pin exact versions, and `config.py` marks starting values as `TUNE`.
- `autose.yml` falls back to an older secret name, `AUTOSAT_PAT`, if `AUTOSE_PAT` is missing.
