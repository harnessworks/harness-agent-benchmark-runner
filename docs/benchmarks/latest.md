# Latest Benchmark Status

Updated: 2026-06-11

## Current Summary

The latest public snapshot covers three compatible 8-task runs against the
first target repository, `harnessworks/harness-starter-kit`:

- a no-op baseline that should fail every task,
- a live Codex CLI dry run,
- and a Claude Opus solution-quality run replayed through the runner.

| Target | Agent | Mode | Runs | Successes | First-pass verify | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `harness-starter-kit` | No-op | Harness validation | 8 | 0 | 0 | 0 | 0 | 0 |
| `harness-starter-kit` | Codex CLI | Live adapter | 8 | 8 | 8 | 0 | 0 | 0 |
| `harness-starter-kit` | Claude Opus | Patch replay | 8 | 8 | 8 | 0 | 0 | 0 |

Detailed reports:

- [`2026-06-11-noop-8-harness-validation.md`](2026-06-11-noop-8-harness-validation.md)
- [`2026-06-11-codex-dry-run-8-oracle-fix.md`](2026-06-11-codex-dry-run-8-oracle-fix.md)
- [`2026-06-11-claude-as-agent-8.md`](2026-06-11-claude-as-agent-8.md)

## Interpretation

This is a benchmark infrastructure dry run, not yet a product-effectiveness
claim. The no-op baseline proves the task oracles do not pass empty work. The
Codex run proves the runner can execute a live agent subprocess in isolated
clones, collect deterministic evidence, and separate verification failures from
file-boundary violations. The Claude replay proves another agent's produced
solutions can be scored against the same task specs, but it does not measure
Claude latency or cost because the solve phase happened before replay.

The next evidence milestone is to run the expanded task set repeatedly, then
compare baseline versus harnessed target repositories.

## Raw Artifacts

Raw `runs/` and `results/` artifacts are intentionally ignored by git. Public
docs should summarize reproducible fields from those artifacts without
committing full logs, cloned repositories, credentials, or local run output.
