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
| `flask-no-harness` | No-op | Target validation | 4 | 0 | 0% | 0 | 0 | 0 |
| `flask-no-harness` | Codex CLI | Live adapter pilot (1×) | 4 | 3 | 75% | 0 | 0 | 1 |
| `flask-yes-harness` | No-op | Target validation | 4 | 0 | 0% | 0 | 0 | 0 |
| `flask-yes-harness` | Codex CLI | Live adapter pilot (1×) | 4 | 3 | 75% | 0 | 0 | 1 |
| `flask-no-harness` | Codex CLI | Harness-effect A/B (3×) | 6 | 4 | 66.7% | 1 | 0 | 1 |
| `flask-yes-harness` | Codex CLI | Harness-effect A/B (3×) | 6 | 6 | 100% | 0 | 0 | 0 |
| `flask-no-harness` | No-op | Complex harness-effect validation | 4 | 0 | 0% | 0 | 0 | 0 |
| `flask-yes-harness` | No-op | Complex harness-effect validation | 4 | 0 | 0% | 0 | 0 | 0 |
| `flask-no-harness` | Codex CLI | Complex harness-effect A/B (3×) | 12 | 10 | 83.3% | 2 | 0 | 0 |
| `flask-yes-harness` | Codex CLI | Complex harness-effect A/B (3×) | 12 | 11 | 91.7% | 0 | 0 | 1 |

Latest run:
[`2026-06-11-complex-harness-effect-ab-3x.md`](2026-06-11-complex-harness-effect-ab-3x.md) —
Codex CLI A/B on four more complex Flask harness-effect tasks. The harnessed
target reached 11/12 successes with 0 wrong-file edits, while the bare target
reached 10/12 with 2 wrong-file edits. The latest broader repeated snapshot
remains
[`2026-06-11-codex-cli-5runs.md`](2026-06-11-codex-cli-5runs.md).

Detailed reports:

- [`2026-06-11-complex-harness-effect-ab-3x.md`](2026-06-11-complex-harness-effect-ab-3x.md) ← latest
- [`2026-06-11-harness-effect-ab-3x.md`](2026-06-11-harness-effect-ab-3x.md)
- [`2026-06-11-flask-yes-harness-codex-pilot.md`](2026-06-11-flask-yes-harness-codex-pilot.md)
- [`2026-06-11-flask-yes-harness-noop-baseline.md`](2026-06-11-flask-yes-harness-noop-baseline.md)
- [`2026-06-11-flask-no-harness-codex-pilot.md`](2026-06-11-flask-no-harness-codex-pilot.md)
- [`2026-06-11-codex-cli-5runs.md`](2026-06-11-codex-cli-5runs.md)
- [`2026-06-11-flask-no-harness-noop-baseline.md`](2026-06-11-flask-no-harness-noop-baseline.md)
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

The `flask-no-harness` row is a negative-control baseline for a newly created
plain Flask target. It validates that the four Flask-specific oracles reject an
empty change set before any live agent score is collected.

The Flask Codex pilot then shows 4/4 deterministic verification passes and 0
boundary violations, but only 3/4 scored successes because `flask-order-quote`
hit the 600-second agent timeout after producing a verifying solution.

The `flask-yes-harness` pilot has the same aggregate score: 3/4 scored
successes, 4/4 verification passes, and 0 boundary violations. Its timeout moved
from `flask-order-quote` to `flask-health-version`, so the current A/B evidence
does not show a success-rate lift from the harness. It mainly shows timeout
variance under one parallel run.

The later harness-effect A/B suite changes the benchmark shape: detailed API
contracts and companion-document rules live in the harnessed repository rather
than the prompt. Under sequential 3x Codex runs, `flask-yes-harness` scored 6/6
while `flask-no-harness` scored 4/6.

The complex harness-effect follow-up expanded the A/B to four harder tasks and
24 live Codex records. It still showed better boundary discipline for
`flask-yes-harness` (0 wrong-file edits vs 2), but not a large functional lift:
`flask-no-harness` passed all deterministic verification commands. The likely
reason is methodology leakage: the target-local oracle code is visible in both
clones, so a capable agent can read the exact expected contract even without
harness conventions. The next stronger experiment should keep the deterministic
oracle outside the agent-visible target clone.

Full records analysis:
[`2026-06-11-benchmark-records-analysis.md`](2026-06-11-benchmark-records-analysis.md).

## Raw Artifacts

Raw `runs/` and `results/` artifacts are intentionally ignored by git. Public
docs should summarize reproducible fields from those artifacts without
committing full logs, cloned repositories, credentials, or local run output.
