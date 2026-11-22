# 10. mini-swe-agent with bash as the only agent tool

Covers: D5

Date: 2026-11-22

## Status

Proposed

## Context

Agents can get tools through an MCP server, the `gh` CLI, the REST API or tool definitions in an agent SDK. Allowed frameworks include the Claude Agent SDK, the OpenAI Agents SDK, LangGraph and mini-swe-agent.

mini-swe-agent's only tool is bash. Its history is one linear list of messages, saved as a trajectory file. It calls models through LiteLLM, so any provider works. It has a step limit, a wall-clock limit and a cost limit in dollars, which stays at zero on free models. It can run commands locally or in a container.

ADR-002 lets the reviewer read and run code but not push. ADR-003 keeps write tokens away from agents. ADR-006 caps tool calls and tokens per stage. The model API key must be present in the process that calls the model, and a bash tool can read environment variables, including the parent process's through `/proc`. Bash cannot be limited to certain files, so a testing agent could edit source code to make its own tests pass, which ADR-001 separates it to avoid.

## Decision

We will build all four agents on mini-swe-agent.

Each agent's only tool is bash, in a checkout of the fork. No agent gets an MCP server, or a `gh` CLI or REST API with a token. Jobs that run agents check out the repository with `persist-credentials: false`, so no token is left in `.git/config`.

Script steps outside the agents do all GitHub actions with the `gh` CLI: pushing, opening the pull request, posting comments and labels, and starting runs.

We will enforce ADR-006's tool-call and wall-clock caps through mini-swe-agent's step limit and wall-clock limit. The orchestrator will enforce the token caps by counting tokens from the `usage` field of each model response.

We will run the testing agent in a scratch copy of the repository. Its only output is test files and its test report. A script copies only test files back into the workspace; any other change is discarded and logged. The testing agent cannot write source code.

We will save each agent's trajectory as a workflow artifact.

We will strip the model API key from the environment of every bash command the agent runs. We will not rely on prompt rules to protect the key.

We will run every agent's bash commands, and every check that runs repository code, in a sandbox container with no secrets, as the runner's own user. Stripping variables alone is not enough: a process on the runner can read its parent's environment through `/proc`.

## Consequences

**Positive.** The tester's discarded changes are logged, which helps us audit whether it tried to edit source code.

**Neutral.** Agents cannot call GitHub, so the scripts carry more logic; this keeps the agents under control. Bash-only agents read and edit files through shell commands, which may work better or may take more time and tokens; this is not known yet.
