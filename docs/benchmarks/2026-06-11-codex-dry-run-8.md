# 2026-06-11 Codex 8-Task Dry Run

## Scope

This run tested the benchmark runner with the real Codex CLI adapter against
the expanded deterministic benchmark task set in `harness-starter-kit`.

- Runner repository: `harnessworks/harness-agent-benchmark-runner`
- Target repository: `harnessworks/harness-starter-kit`
- Target ref: `497db091d591c710e973f43e148019a4d84e94fe`
- Adapter: `examples/agents/codex_exec_agent.py`
- Runs: 8
- Attempts per task: 1

## Aggregate Result

| Metric | Value |
| --- | ---: |
| Runs | 8 |
| Successes | 7 |
| Verification passed | 7 |
| Agent timeouts | 0 |
| Wrong-file edits | 0 |
| Forbidden-file edits | 0 |
| Runner errors | 0 |
| Total Codex tokens | 318,627 |
| Average Codex tokens per run | 39,828 |

## Task Results

| Task | Result | Changed files | Agent tokens | Notes |
| --- | --- | --- | ---: | --- |
| `command-workflow-refresh-benchmark-guidance` | Failed | `commands/harness-refresh.md`, `tests/test_repository_hygiene.py` | 80,015 | Boundary was clean, but verification failed because the oracle checked exact phrases without whitespace normalization. |
| `decision-memory-benchmark-ownership-adr` | Passed | `docs/decisions/0008-benchmark-task-ownership.md` | 22,928 | Verification and boundary checks passed. |
| `docs-only-evaluation-benchmark-ownership` | Passed | `docs/evaluation.md` | 19,779 | Verification and boundary checks passed after the concept-based oracle update. |
| `failure-memory-benchmark-noop-oracle-gap` | Passed | `docs/failures/0011-benchmark-noop-oracle-gap.md` | 24,467 | Verification and boundary checks passed. |
| `forbidden-file-structure-ignore-runner-output` | Passed | `.harness/structure-rules.json` | 35,527 | Verification and boundary checks passed. |
| `installer-non-destructive-list-profiles` | Passed | `scripts/apply_harness.py`, `tests/test_apply_harness.py` | 67,818 | Verification and boundary checks passed. |
| `profile-boundary-go-race-check` | Passed | `templates/profiles/go/README.md` | 19,428 | Verification and boundary checks passed. |
| `small-bugfix-docs-drift-uv-command` | Passed | `scripts/check_docs_drift.py`, `tests/test_check_docs_drift.py` | 48,665 | Verification and boundary checks passed. |

## Failure Detail

`command-workflow-refresh-benchmark-guidance` failed the deterministic refresh
workflow oracle. Codex edited only the expected files and added the requested
concepts, but `commands/harness-refresh.md` line-wrapped two expected phrases:

- `stale verification commands`
- `runner-output assumptions`

The task oracle checked those exact phrases in the raw Markdown text, while the
test file itself normalized whitespace before asserting the same concepts. This
is a brittle oracle failure, not a wrong-file or forbidden-file failure.

Recommended follow-up: normalize whitespace in the command workflow oracle, or
check the required concepts with focused regular expressions.

## Evidence Location

The local raw artifacts for this run were stored under ignored paths:

- `results/codex-dry-run-8/2026-06-11.jsonl`
- `runs/codex-dry-run-8/*/result.json`
- `runs/codex-dry-run-8/*/logs/agent.log`

Do not commit those raw artifacts. This report is the public summary.
