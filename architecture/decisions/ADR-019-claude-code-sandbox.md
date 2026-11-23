# 19. Claude Code sandbox

Covers: D5, D9

Date: 2026-11-23

## Status

Deprecated. The Anthropic key had no credit, so no role ever ran on Claude and every agent ran on mini-swe-agent (ADR-010).

## Context

ADR-010 builds every agent on mini-swe-agent with bash as the only tool. ADR-016 moves the primary models to Claude. Claude Code can run headless (`claude -p`) with file read, edit and search tools, a dollar cap per call (`--max-budget-usd`), resumable sessions (`--resume`) and a stream of every tool call (`stream-json`). Claude Code runs its tools in the process where it runs, so on the runner its bash would sit next to the GitHub tokens, which ADR-006 and ADR-010 forbid. Inside the sandbox it needs an API key, and an issue can carry instructions that ask an agent to print one. Docker can attach a container to an internal network with no route to the internet. This decision amends ADR-010 for roles that run on Claude models.

## Decision

We will run every agent whose role starts on a Claude model as headless Claude Code inside the sandbox container, with the tools Bash, Read, Write, Edit, Glob and Grep, and no web tools.

We will give the sandbox a placeholder API key only. A separate proxy container holds the real key, accepts only `/v1/` paths and adds the key to each request to api.anthropic.com.

We will move the sandbox onto an internal Docker network after setup and the first git fetch, so its only reachable host is the proxy, and check that the internet is unreachable before any agent runs.

We will cap each Claude Code call in dollars and wall-clock time, keep the token cap per run, resume the same session for re-asks and the tester's second phase, and save the tool-call stream as the trajectory.

We will keep mini-swe-agent for any role whose model is not Claude, and use it for every role when the Anthropic key cannot serve requests.

## Consequences

**Positive.** The sandbox never holds the API key and has no internet, so a prompt-injected issue cannot exfiltrate the key or reach outside services. Claude Code brings file editing, search and a dollar cap per call, which mini-swe-agent lacks.

**Negative.** Sandbox setup takes about two minutes longer, because Node and Claude Code are installed in every job. Builds in the offline sandbox cannot fetch build dependencies, so they run with `--no-build-isolation`. Two harnesses exist side by side, which complicates comparing runs.

**Neutral.** Roles on non-Claude models keep mini-swe-agent, and every role falls back to it when the Anthropic key cannot serve requests.
