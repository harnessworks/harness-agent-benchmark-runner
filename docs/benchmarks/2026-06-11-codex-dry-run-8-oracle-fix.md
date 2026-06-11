# 2026-06-11 Codex 8-Task Dry Run After Oracle Fix

## Scope

This run retested the expanded deterministic benchmark task set in
`harness-starter-kit` after the target repository fixed the brittle
command-workflow oracle that failed the previous 8-task dry run.

- Runner repository: `harnessworks/harness-agent-benchmark-runner`
- Target repository: `harnessworks/harness-starter-kit`
- Target ref: `af559249abd3d24e713bf1d045345e0d53480a5e`
- Target tag: `v0.1.11`
- Adapter: `examples/agents/codex_exec_agent.py`
- Runs: 8
- Attempts per task: 1

## Aggregate Result

| Metric | Value |
| --- | ---: |
| Runs | 8 |
| Successes | 8 |
| Verification passed | 8 |
| Agent timeouts | 0 |
| Wrong-file edits | 0 |
| Forbidden-file edits | 0 |
| Runner errors | 0 |
| Total Codex tokens | 307,467 |
| Average Codex tokens per run | 38,433 |

## Task Results

| Task | Result | Changed files | Agent tokens | Notes |
| --- | --- | --- | ---: | --- |
| `command-workflow-refresh-benchmark-guidance` | Passed | `commands/harness-refresh.md`, `tests/test_repository_hygiene.py` | 45,638 | Previously brittle oracle now passes with line-wrapped Markdown. |
| `decision-memory-benchmark-ownership-adr` | Passed | `docs/decisions/0008-benchmark-task-ownership.md` | 26,418 | Verification and boundary checks passed. |
| `docs-only-evaluation-benchmark-ownership` | Passed | `docs/evaluation.md` | 32,084 | Verification and boundary checks passed. |
| `failure-memory-benchmark-noop-oracle-gap` | Passed | `docs/failures/0012-benchmark-noop-oracle-gap.md` | 29,502 | Verification and boundary checks passed. |
| `forbidden-file-structure-ignore-runner-output` | Passed | `.harness/structure-rules.json` | 30,880 | Verification and boundary checks passed. |
| `installer-non-destructive-list-profiles` | Passed | `scripts/apply_harness.py`, `tests/test_apply_harness.py` | 61,153 | Verification and boundary checks passed. |
| `profile-boundary-go-race-check` | Passed | `templates/profiles/go/README.md` | 23,721 | Verification and boundary checks passed. |
| `small-bugfix-docs-drift-uv-command` | Passed | `scripts/check_docs_drift.py`, `tests/test_check_docs_drift.py` | 58,071 | Verification and boundary checks passed. |

## Interpretation

This run is the first fully green Codex dry run across the expanded
`harness-starter-kit` benchmark set.

The result demonstrates that the runner, Codex adapter, target task definitions,
deterministic verification commands, and file-boundary scoring all work
end-to-end for this target at the pinned ref above. It is still a dry run, not a
cross-repository harness-effectiveness claim.

The next milestone is a repeated pilot, such as 8 tasks times 3 repeats, before
using the results in a broader baseline-versus-harnessed comparison.

## Evidence Location

The local raw artifacts for this run were stored under ignored paths:

- `results/codex-dry-run-8-oracle-fix/2026-06-11.jsonl`
- `runs/codex-dry-run-8-oracle-fix/*/result.json`
- `runs/codex-dry-run-8-oracle-fix/*/logs/agent.log`

Do not commit those raw artifacts. This report is the public summary.
