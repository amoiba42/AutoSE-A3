# Decision Index

ADRs are numbered in the order they were written; none is deleted. Each ADR names the decision areas it covers
(`Covers: Dx`) under its title. Statuses follow Nygard: Accepted, Deprecated, or Superseded by ADR-0xx.
"Amended by ADR-0xx" marks an accepted ADR that still holds but was changed in part by a later ADR; the ADR's own
Status section says what changed, and the later ADR names the ADRs it amends.

## All ADRs

| ADR | Title | Covers | Status |
|---|---|---|---|
| [ADR-001](ADR-001-agent-split.md) | Four-agent split | D1 | Accepted |
| [ADR-002](ADR-002-reviewer-independence.md) | Reviewer isolation | D8 | Accepted. Amended by ADR-018 and ADR-025. |
| [ADR-003](ADR-003-control-flow.md) | Orchestrator control flow | D2 | Accepted. Amended by ADR-021, ADR-022 and ADR-024. |
| [ADR-004](ADR-004-state.md) | Artifact-based state | D4 | Accepted. Amended by ADR-022 and ADR-024. |
| [ADR-005](ADR-005-triggers.md) | Label and comment triggers | D10 | Accepted. Amended by ADR-014 and ADR-024. |
| [ADR-006](ADR-006-safety-and-failures.md) | Least privilege and caps | D9 | Accepted. Amended by ADR-014, ADR-015, ADR-017, ADR-018 and ADR-023. |
| [ADR-007](ADR-007-checks.md) | Script-decided checks | D7 | Accepted. Amended by ADR-017, ADR-018, ADR-021 and ADR-022. |
| [ADR-008](ADR-008-linters-and-secret-checks.md) | Ruff and regex scan | D7, D9 | Accepted |
| [ADR-009](ADR-009-no-sonarqube.md) | No SonarQube | D7 | Accepted |
| [ADR-010](ADR-010-agent-tools.md) | Bash-only mini-swe-agent | D5 | Accepted. Amended by ADR-018 and ADR-023. |
| [ADR-011](ADR-011-models.md) | Models per role | D6 | Superseded by ADR-016 |
| [ADR-012](ADR-012-hand-offs.md) | Full-artifact hand-offs | D3 | Accepted. Amended by ADR-017, ADR-018 and ADR-024. |
| [ADR-013](ADR-013-skill-adaptation-and-vague-issues.md) | Adapted A1 skill | D1, D7 | Accepted |
| [ADR-014](ADR-014-model-error-waits-and-sequential-runs.md) | Waits and sequential runs | D6, D9, D10 | Accepted. Amended by ADR-018 and ADR-020. |
| [ADR-015](ADR-015-public-comment-hygiene.md) | Comment hygiene | D9 | Accepted. Amended by ADR-018 and ADR-027. |
| [ADR-016](ADR-016-claude-models-per-role.md) | Claude model tiers | D6 | Superseded by ADR-020 |
| [ADR-017](ADR-017-reasks-and-stage4-routing.md) | One re-ask | D2, D9 | Accepted. Amended by ADR-022. |
| [ADR-018](ADR-018-check-and-isolation-corrections.md) | Check and isolation fixes | D3, D5, D6, D7, D8, D9 | Accepted. Amended by ADR-025. |
| [ADR-019](ADR-019-claude-code-sandbox.md) | Claude Code sandbox | D5, D9 | Deprecated |
| [ADR-020](ADR-020-model-fallback-chains.md) | Model fallback chains | D6, D9 | Accepted |
| [ADR-021](ADR-021-release-merges-base.md) | Release merges base | D2, D7 | Accepted |
| [ADR-022](ADR-022-strict-g4-and-reruns.md) | Strict G4, re-runs | D2, D7 | Accepted |
| [ADR-023](ADR-023-agent-loop-budgets.md) | Agent loop budgets | D5, D9 | Accepted |
| [ADR-024](ADR-024-restart-from-stage.md) | Restart from stage | D2, D4, D10 | Accepted |
| [ADR-025](ADR-025-reviewer-sees-pr-only.md) | Reviewer sees PR only | D8, D9 | Accepted |
| [ADR-026](ADR-026-experiment-harness.md) | Experiment harness | D1, D6, D8 | Accepted |
| [ADR-027](ADR-027-encoded-secret-redaction.md) | Encoded secret redaction | D9 | Accepted |

## D1-D10

This table lists, for each of the brief's decision areas D1-D10, every ADR whose `Covers` line names that area,
including superseded and deprecated ones.

| D-number | Decision area | ADR(s) | Status |
|---|---|---|---|
| D1 | Splitting the work | [ADR-001](ADR-001-agent-split.md), [ADR-013](ADR-013-skill-adaptation-and-vague-issues.md), [ADR-026](ADR-026-experiment-harness.md) | Accepted |
| D2 | Control flow | [ADR-003](ADR-003-control-flow.md), [ADR-017](ADR-017-reasks-and-stage4-routing.md), [ADR-021](ADR-021-release-merges-base.md), [ADR-022](ADR-022-strict-g4-and-reruns.md), [ADR-024](ADR-024-restart-from-stage.md) | Accepted (ADR-003 amended by ADR-021, ADR-022, ADR-024; ADR-017 amended by ADR-022) |
| D3 | Hand-offs | [ADR-012](ADR-012-hand-offs.md), [ADR-018](ADR-018-check-and-isolation-corrections.md) | Accepted (ADR-012 amended by ADR-017, ADR-018, ADR-024; ADR-018 amended by ADR-025) |
| D4 | State | [ADR-004](ADR-004-state.md), [ADR-024](ADR-024-restart-from-stage.md) | Accepted (ADR-004 amended by ADR-022, ADR-024) |
| D5 | Tools | [ADR-010](ADR-010-agent-tools.md), [ADR-018](ADR-018-check-and-isolation-corrections.md), [ADR-019](ADR-019-claude-code-sandbox.md), [ADR-023](ADR-023-agent-loop-budgets.md) | Accepted (ADR-010 amended by ADR-018, ADR-023; ADR-018 amended by ADR-025; ADR-019 deprecated) |
| D6 | Models | [ADR-011](ADR-011-models.md), [ADR-014](ADR-014-model-error-waits-and-sequential-runs.md), [ADR-016](ADR-016-claude-models-per-role.md), [ADR-018](ADR-018-check-and-isolation-corrections.md), [ADR-020](ADR-020-model-fallback-chains.md), [ADR-026](ADR-026-experiment-harness.md) | Accepted (ADR-011 superseded by ADR-016; ADR-014 amended by ADR-018, ADR-020; ADR-016 superseded by ADR-020; ADR-018 amended by ADR-025) |
| D7 | Checks | [ADR-007](ADR-007-checks.md), [ADR-008](ADR-008-linters-and-secret-checks.md), [ADR-009](ADR-009-no-sonarqube.md), [ADR-013](ADR-013-skill-adaptation-and-vague-issues.md), [ADR-018](ADR-018-check-and-isolation-corrections.md), [ADR-021](ADR-021-release-merges-base.md), [ADR-022](ADR-022-strict-g4-and-reruns.md) | Accepted (ADR-007 amended by ADR-017, ADR-018, ADR-021, ADR-022; ADR-018 amended by ADR-025) |
| D8 | Reviewer independence | [ADR-002](ADR-002-reviewer-independence.md), [ADR-018](ADR-018-check-and-isolation-corrections.md), [ADR-025](ADR-025-reviewer-sees-pr-only.md), [ADR-026](ADR-026-experiment-harness.md) | Accepted (ADR-002 amended by ADR-018, ADR-025; ADR-018 amended by ADR-025) |
| D9 | Safety and failures | [ADR-006](ADR-006-safety-and-failures.md), [ADR-008](ADR-008-linters-and-secret-checks.md), [ADR-014](ADR-014-model-error-waits-and-sequential-runs.md), [ADR-015](ADR-015-public-comment-hygiene.md), [ADR-017](ADR-017-reasks-and-stage4-routing.md), [ADR-018](ADR-018-check-and-isolation-corrections.md), [ADR-019](ADR-019-claude-code-sandbox.md), [ADR-020](ADR-020-model-fallback-chains.md), [ADR-023](ADR-023-agent-loop-budgets.md), [ADR-025](ADR-025-reviewer-sees-pr-only.md), [ADR-027](ADR-027-encoded-secret-redaction.md) | Accepted (ADR-006 amended by ADR-014, ADR-015, ADR-017, ADR-018, ADR-023; ADR-014 amended by ADR-018, ADR-020; ADR-015 amended by ADR-018, ADR-027; ADR-017 amended by ADR-022; ADR-018 amended by ADR-025; ADR-019 deprecated) |
| D10 | Triggers | [ADR-005](ADR-005-triggers.md), [ADR-014](ADR-014-model-error-waits-and-sequential-runs.md), [ADR-024](ADR-024-restart-from-stage.md) | Accepted (ADR-005 amended by ADR-014, ADR-024; ADR-014 amended by ADR-018, ADR-020) |
