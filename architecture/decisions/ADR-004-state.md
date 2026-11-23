# 4. Artifact-based state

Covers: D4

Date: 2026-11-22

## Status

Accepted. Amended by ADR-022 (where a re-run resumes after a Release or Review stop) and ADR-024 (a restart resets the stages it repeats).

## Context

ADR-003 sends work back by starting a new run through `workflow_dispatch` at Stage 1, 2, 3 or 4. The new run needs the earlier stages' outputs, the review round and the branch. A run can also be restarted after a failure.

Workflow artifacts belong to one run; a later run can find them by name through the REST API and download them with `actions: read`. The issue exists for the whole run, while PR comments exist only after Stage 5. Files on the PR branch are visible to the reviewer (ADR-002). The Actions cache can evict entries.

Restarting from Stage 1 repeats stages that already passed. A stage that is rerun with no record of its earlier attempt can repeat the same mistake. A failure often traces back to a point where the work drifted from the spec, the design or `ARCHITECTURE.md`. A check failure produces exact output, such as a failing command or test. The reviewer cannot see the spec or the design (ADR-002), while the agent that receives the work can. The orchestrator is a script and cannot summarize work; the agent that did the work can. The issue author can edit the issue after a maintainer starts a run, and a run can be triggered again after the work has finished.

## Decision

We will store state as workflow artifacts, and the artifacts are the source of truth. `state.json` holds the current stage, the last stage that passed, the target stage, the review round, the branch, the run IDs and a `done` flag. Each stage's output is stored next to it.

We will name the artifacts per issue (`autose-issue-<n>`). A new run, whether a re-entry or a restart, downloads the latest artifact with that name. Before starting a re-entry run, Route records the target stage in `state.json`, so the new run reads its starting stage from state and not from a workflow input.

We will mirror `state.json` in one comment on the issue, updated in place, for humans to follow. The workflow does not read the mirror.

We will use one branch per issue, `autose/issue-<n>`, and reuse an existing branch or pull request.

We will store a snapshot of the issue title and body, with a hash of both, in `state.json` on the first run. Every later run uses the snapshot. If the hash no longer matches, a run started by a comment or a dispatch stops, and a run started by a maintainer re-adding the `autose` label restarts from Stage 1 with a new snapshot. While the hash matches, re-adding the label resumes as below. The issue's `updated_at` is not used, because every comment changes it.

A new run starts from the target stage if `state.json` holds one; otherwise it resumes from the last stage that passed. Earlier stage outputs are downloaded, not regenerated.

When the work ends with an approval or after the second review round, `state.json` is marked `done`. A later trigger only posts a comment that the work has finished.

When work goes back to a stage, we will give that stage the outputs of the stages before it, plus a send-back note. The note records what the previous attempt did, why it failed or was sent back, and a reference to the likely point of drift: the relevant part of the spec, the design or `ARCHITECTURE.md`.

Each agent will end its stage by writing a short attempt summary of what it did and why, stored as an artifact.

The orchestrator will assemble the send-back note without writing prose. It copies in the attempt summary of the stage being redone, plus the failed check's output or the reviewer's findings and classification from the review artifact. The reviewer's drift reference points at the issue, the code or `ARCHITECTURE.md`. The agent that receives the note links it to its own spec and design.

## Consequences

**Positive.** Resuming from the last stage that passed saves tokens and time.

**Neutral.** Artifacts expire after 90 days by default, which does not matter for this study. The send-back note is only as good as the agent's own attempt summary, so a weak model writes a weak note.
