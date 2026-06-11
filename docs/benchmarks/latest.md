# Latest Benchmark Status

Updated: 2026-06-11

## Current Summary

The runner has completed an end-to-end Codex adapter dry run against the first
eight deterministic benchmark tasks in the first target repository,
`harnessworks/harness-starter-kit`.

| Target | Agent | Runs | Successes | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `harness-starter-kit` | Codex CLI | 8 | 7 | 0 | 0 | 0 |

Latest detailed report:
[`2026-06-11-codex-dry-run-8.md`](2026-06-11-codex-dry-run-8.md).

## Interpretation

This is a benchmark infrastructure dry run, not yet a product-effectiveness
claim. It proves that the runner can execute real Codex tasks in isolated
clones, collect deterministic evidence, and separate verification failures from
file-boundary violations.

The next evidence milestone is to run the expanded task set repeatedly and then
compare baseline versus harnessed target repositories.

## Raw Artifacts

Raw `runs/` and `results/` artifacts are intentionally ignored by git. Public
docs should summarize reproducible fields from those artifacts without
committing full logs, cloned repositories, credentials, or local run output.
