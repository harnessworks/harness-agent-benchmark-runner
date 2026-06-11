# 2026-06-11 Codex Dry Run

## Scope

This run tested the benchmark runner with the real Codex CLI adapter against
the first three deterministic benchmark tasks in `harness-starter-kit`.

- Runner repository: `harnessworks/harness-agent-benchmark-runner`
- Target repository: `harnessworks/harness-starter-kit`
- Target ref: `fbcb14e1bfc0b2156a3e1e52efa24fc72cccc9b0`
- Adapter: `examples/agents/codex_exec_agent.py`
- Runs: 3
- Attempts per task: 1

## Aggregate Result

| Metric | Value |
| --- | ---: |
| Runs | 3 |
| Successes | 2 |
| Verification passed | 2 |
| Agent timeouts | 0 |
| Wrong-file edits | 0 |
| Forbidden-file edits | 0 |
| Runner errors | 0 |

## Task Results

| Task | Result | Changed files | Agent tokens | Notes |
| --- | --- | --- | ---: | --- |
| `docs-only-evaluation-benchmark-ownership` | Failed | `docs/evaluation.md` | 20,475 | Boundary was clean, but verification failed because the oracle required exact substrings. |
| `forbidden-file-structure-ignore-runner-output` | Passed | `.harness/structure-rules.json` | 46,664 | Verification and boundary checks passed. |
| `small-bugfix-docs-drift-uv-command` | Passed | `scripts/check_docs_drift.py`, `tests/test_check_docs_drift.py` | 39,802 | Verification and boundary checks passed. |

## Failure Detail

`docs-only-evaluation-benchmark-ownership` failed the deterministic text oracle.
Codex added the expected section and changed only `docs/evaluation.md`, but the
oracle required exact substrings that did not tolerate casing, line wrapping, or
near-equivalent phrasing.

The missing oracle substrings were:

- ``benchmark task definitions live under `benchmarks/tasks/` ``
- ``project-specific benchmark oracles belong to this repository``
- ``boundary adherence separately from verification success``

Recommended follow-up: keep the task deterministic, but normalize whitespace and
case or check required concepts with focused regular expressions.

## Evidence Location

The local raw artifacts for this run were stored under ignored paths:

- `results/codex-dry-run/2026-06-11.jsonl`
- `runs/codex-dry-run/*/result.json`
- `runs/codex-dry-run/*/logs/agent.log`

Do not commit those raw artifacts. This report is the public summary.
