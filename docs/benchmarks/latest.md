# Latest Benchmark Status

Updated: 2026-06-11

## Current Summary

| Target | Agent | Mode | Runs | Successes | Rate | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `harness-starter-kit` | No-op | Harness validation | 8 | 0 | 0% | 0 | 0 | 0 |
| `harness-starter-kit` | Codex CLI | Live adapter (1×) | 8 | 8 | 100% | 0 | 0 | 0 |
| `harness-starter-kit` | Codex CLI | Live adapter (5×) | 40 | 34 | 85% | 0 | 0 | 4 |
| `harness-starter-kit` | Claude Opus | Patch replay (1×) | 8 | 8 | 100% | 0 | 0 | 0 |
| `harness-starter-kit` | Claude Code CLI | Live adapter (5×) | 40 | 37 | 92.5% | 0 | 0 | 0 |

Latest run: [`2026-06-11-codex-cli-5runs.md`](2026-06-11-codex-cli-5runs.md) —
Codex CLI live adapter, 34/40 successes across 8 tasks × 5 runs, with 0
wrong-file edits and 0 forbidden-file edits.

Detailed reports:

- [`2026-06-11-codex-cli-5runs.md`](2026-06-11-codex-cli-5runs.md) ← latest
- [`2026-06-11-benchmark-records-analysis.md`](2026-06-11-benchmark-records-analysis.md)
- [`2026-06-11-claude-code-5runs.md`](2026-06-11-claude-code-5runs.md)
- [`2026-06-11-claude-as-agent-8.md`](2026-06-11-claude-as-agent-8.md)
- [`2026-06-11-codex-dry-run-8-oracle-fix.md`](2026-06-11-codex-dry-run-8-oracle-fix.md)
- [`2026-06-11-noop-8-harness-validation.md`](2026-06-11-noop-8-harness-validation.md)

## Interpretation

The multi-repetition Codex run shows 0 file-boundary violations across 40 live
runs. Six runs failed: four agent timeouts and two deterministic oracle misses
after a clean agent exit. The profile-boundary timeout had passing verification,
but still scored as failure because the agent process timed out.

The Claude Code multi-repetition run remains useful comparison evidence: 37/40
successes, 0 timeouts, and 0 file-boundary violations. Next milestone: separate
agent quality failures from timeout/concurrency pressure by re-running Codex
with lower parallelism or higher task timeouts.

Full records analysis:
[`2026-06-11-benchmark-records-analysis.md`](2026-06-11-benchmark-records-analysis.md).

## Raw Artifacts

Raw `runs/` and `results/` artifacts are intentionally ignored by git. Public
docs should summarize reproducible fields from those artifacts without
committing full logs, cloned repositories, credentials, or local run output.
