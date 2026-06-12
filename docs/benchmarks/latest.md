# Latest Benchmark Status

Updated: 2026-06-12

## Current Summary

| Target | Agent | Mode | Runs | Strict scored successes | Strict success rate | Wrong-file edits | Forbidden-file edits | Timeouts |
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
| `flask-no-harness` | No-op | Hidden-oracle validation | 4 | 0 | 0% | 0 | 0 | 0 |
| `flask-yes-harness` | No-op | Hidden-oracle validation | 4 | 0 | 0% | 0 | 0 | 0 |
| `flask-no-harness` | Codex CLI | Hidden-oracle A/B (3×) | 12 | 0 | 0% | 11 | 0 | 3 |
| `flask-yes-harness` | Codex CLI | Hidden-oracle A/B (3×) | 12 | 11 | 91.7% | 0 | 0 | 0 |
| `flask-no-harness` | Codex CLI | Hidden-oracle calibration (1×, 10 tasks) | 10 | 0 | 0% | 0 | 0 | 0 |
| `flask-yes-harness` | Codex CLI | Hidden-oracle calibration (1×, 10 tasks) | 10 | 10 | 100% | 0 | 0 | 0 |

Latest run:
[`2026-06-12-hidden-flask-ab-calibration-1x.md`](2026-06-12-hidden-flask-ab-calibration-1x.md) —
Codex CLI calibration on all ten hidden-oracle Flask A/B task pairs after the
prompt wording was tightened. The harnessed target reached 10/10 strict scored
successes and 10/10 verification passes. The bare target reached 0/10
verification passes and 0/10 strict scored successes. Both targets had 0
wrong-file edits, 0 forbidden-file edits, and 0 timeouts; root `README.md` was
not changed in any record. This is calibration evidence for the next 200-run
large A/B, not the representative large evidence run itself. Codex was run with
`CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`.
The latest repeated hidden-oracle evidence remains
[`2026-06-11-hidden-oracle-harness-effect-ab-3x.md`](2026-06-11-hidden-oracle-harness-effect-ab-3x.md),
and the latest broader repeated snapshot remains
[`2026-06-11-codex-cli-5runs.md`](2026-06-11-codex-cli-5runs.md).

Detailed reports:

- [`2026-06-12-hidden-flask-ab-calibration-1x.md`](2026-06-12-hidden-flask-ab-calibration-1x.md) ← latest calibration
- [`2026-06-11-hidden-oracle-harness-effect-ab-3x.md`](2026-06-11-hidden-oracle-harness-effect-ab-3x.md)
- [`2026-06-11-complex-harness-effect-ab-3x.md`](2026-06-11-complex-harness-effect-ab-3x.md)
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
harness conventions. That motivated the hidden-oracle follow-up below.

The hidden-oracle follow-up removes that leakage by keeping task specs and the
deterministic oracle in this runner repository. Under the same four-task shape
and 3x repetition, `flask-no-harness` fell to 0/12 while `flask-yes-harness`
reached 11/12. This is the clearest current evidence that the harness is
meaningful for convention-dependent work: it improved contract discovery,
strict task-boundary adherence, and timeout behavior. Verification passed is
the functional signal; wrong-file edits are the strict boundary signal.

The 2026-06-12 calibration then expanded the hidden-oracle shape to all ten
task pairs with one repetition per side. It confirmed that the tightened prompt
removed the root `README.md` ambiguity: both targets had 0 wrong-file edits,
while the functional split remained large (`flask-no-harness` 0/10 verification
passes, `flask-yes-harness` 10/10). This supports proceeding to the planned
200-run large A/B.

Full records analysis:
[`2026-06-11-benchmark-records-analysis.md`](2026-06-11-benchmark-records-analysis.md).

## Raw Artifacts

Raw `runs/` and `results/` artifacts are intentionally ignored by git. Public
docs should summarize reproducible fields from those artifacts without
committing full logs, cloned repositories, credentials, or local run output.
