# Latest Benchmark Status

Updated: 2026-06-13

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
| `flask-no-harness` | Codex CLI | Balanced hidden-oracle A/B pilot (20-run, run-time oracle) | 10 | 6 | 60% | 0 | 0 | 0 |
| `flask-yes-harness` | Codex CLI | Balanced hidden-oracle A/B pilot (20-run, run-time oracle) | 10 | 10 | 100% | 0 | 0 | 0 |
| `flask-no-harness` | Codex CLI | Balanced hidden-oracle A/B pilot (post-hoc concept-docs rescore) | 10 | 9 | 90% | 0 | 0 | 0 |
| `flask-yes-harness` | Codex CLI | Balanced hidden-oracle A/B pilot (post-hoc concept-docs rescore) | 10 | 10 | 100% | 0 | 0 | 0 |
| `flask-no-harness` | Codex CLI | Balanced hidden-oracle A/B `jobs=2` calibration | 10 | 9 | 90% | 0 | 0 | 0 |
| `flask-yes-harness` | Codex CLI | Balanced hidden-oracle A/B `jobs=2` calibration | 10 | 10 | 100% | 0 | 0 | 0 |
| `flask-no-harness` | Codex CLI | Balanced hidden-oracle A/B 100-run `jobs=2` | 50 | 46 | 92% | 0 | 0 | 1 |
| `flask-yes-harness` | Codex CLI | Balanced hidden-oracle A/B 100-run `jobs=2` | 50 | 48 | 96% | 0 | 0 | 2 |

Latest run:
[`2026-06-12-hidden-flask-balanced-ab-100-jobs2.md`](2026-06-12-hidden-flask-balanced-ab-100-jobs2.md) —
Codex CLI completed the balanced hidden-oracle Flask A/B suite with all ten
task pairs, `repeats=5`, and `--jobs 2`. `flask-no-harness` reached 46/50
strict scored successes and 46/50 verification passes. `flask-yes-harness`
reached 48/50 strict scored successes and 49/50 verification passes. Both
targets had 0 wrong-file edits and 0 forbidden-file edits. Timeout behavior was
not cleanly in favor of the harnessed target: no-harness had 1 timeout, while
yes-harness had 2 timeouts. This is representative for the measured `jobs=2`
condition, not a pure sequential claim. Codex was run with
`CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`.

Latest heldout diagnostic:
[`2026-06-13-hidden-flask-heldout-stable8-noedit-2round-pilot.md`](2026-06-13-hidden-flask-heldout-stable8-noedit-2round-pilot.md) —
after adding `--agent-no-edit-timeout`, `CODEX_PROMPT_GUARD=1` completed a
fresh 2-round stable-8 readiness pilot. All 16 records completed with 0
stalls, 0 timeouts, 0 wrong-file edits, 0 forbidden-file edits, and 0 hidden
access findings. A dry-run 96-record promotion plan passed the clean-readiness
gate against these results. This clears the immediate operational no-edit-tail
blocker for the reduced suite, but it is still not product evidence: strict
success was 0/16 and schema-contract success was 0/16.

Recent throughput calibration:
[`2026-06-12-hidden-flask-balanced-ab-20-jobs2-calibration.md`](2026-06-12-hidden-flask-balanced-ab-20-jobs2-calibration.md) —
Codex CLI repeated the balanced 20-run task set under the revised concept-docs
oracle with `--jobs 2`. It completed 20/20 records in about 22 minutes with 0
wrong-file edits, 0 forbidden-file edits, 0 timeouts, and 0 runner errors.
`flask-no-harness` scored 9/10; `flask-yes-harness` scored 10/10. This is a
parallel throughput calibration, not a replacement for representative
sequential evidence.

Detailed reports:

- [`2026-06-13-hidden-flask-heldout-stable8-noedit-2round-pilot.md`](2026-06-13-hidden-flask-heldout-stable8-noedit-2round-pilot.md) ← latest heldout diagnostic
- [`2026-06-13-hidden-flask-heldout-stable8-2round-pilot-aborted.md`](2026-06-13-hidden-flask-heldout-stable8-2round-pilot-aborted.md)
- [`2026-06-13-hidden-flask-heldout-stable8-finalmitigation-aborted-96.md`](2026-06-13-hidden-flask-heldout-stable8-finalmitigation-aborted-96.md)
- [`2026-06-13-hidden-flask-heldout-finalmitigation-aborted-100.md`](2026-06-13-hidden-flask-heldout-finalmitigation-aborted-100.md)
- [`2026-06-13-hidden-flask-heldout-idlewatch-aborted-100.md`](2026-06-13-hidden-flask-heldout-idlewatch-aborted-100.md)
- [`2026-06-12-hidden-flask-heldout-promptguard-aborted-100.md`](2026-06-12-hidden-flask-heldout-promptguard-aborted-100.md)
- [`2026-06-12-hidden-flask-heldout-memoryhide-aborted-pilot.md`](2026-06-12-hidden-flask-heldout-memoryhide-aborted-pilot.md)
- [`2026-06-12-hidden-flask-balanced-ab-100-jobs2.md`](2026-06-12-hidden-flask-balanced-ab-100-jobs2.md) ← latest 100-run evidence
- [`2026-06-12-hidden-flask-balanced-ab-20-jobs2-calibration.md`](2026-06-12-hidden-flask-balanced-ab-20-jobs2-calibration.md) ← latest throughput calibration
- [`2026-06-12-hidden-flask-balanced-ab-20-pilot.md`](2026-06-12-hidden-flask-balanced-ab-20-pilot.md) ← latest pilot
- [`2026-06-12-hidden-flask-ab-calibration-1x.md`](2026-06-12-hidden-flask-ab-calibration-1x.md)
- [`2026-06-12-hidden-flask-ab-partial-calibration-35.md`](2026-06-12-hidden-flask-ab-partial-calibration-35.md)
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
passes, `flask-yes-harness` 10/10). That run is best treated as upper-bound
hidden-contract calibration because the harnessed target had much more
task-specific contract guidance.

The balanced 20-run pilot moved the task-critical API contract into both
prompts. Under that fairer shape, `flask-no-harness` improved to 6/10 at run
time while `flask-yes-harness` remained 10/10, with 0 wrong-file edits, 0
forbidden-file edits, and 0 timeouts on both sides. Three of the four
no-harness failures were docs phrase misses under the original pilot oracle, so
the docs oracle has now been revised to check route and domain-term coverage
rather than exact English phrases. The saved run directories rescore to 9/10 vs
10/10 under that revised oracle; the remaining no-harness miss is functional.

The `jobs=2` calibration then reran the balanced 20-run task set with the
revised concept-docs oracle and low parallelism. It completed cleanly with 0
timeouts and 0 boundary violations, scoring 9/10 for `flask-no-harness` and
10/10 for `flask-yes-harness`. This supports `jobs=2` as a candidate
wall-clock-saving shape, but any 100-run report that uses it must state the
parallelism explicitly and keep timeout behavior separate from task quality.

The follow-up 100-run `jobs=2` evidence run completed all 100 planned records.
It narrowed the strict success gap to 46/50 for `flask-no-harness` vs 48/50 for
`flask-yes-harness`, while verification passed was 46/50 vs 49/50. The harness
signal is therefore small and mostly visible in deterministic oracle misses,
not file-boundary discipline. `jobs=2` introduced timeout noise: 1 no-harness
timeout and 2 yes-harness timeouts. A sequential follow-up or a jobs=2 run with
a higher timeout cap is needed before making a timeout-stability claim.

The latest 2026-06-13 stable-8 2-round pilot diagnostic is the current
promotion-readiness evidence for answer-free partial-realistic prompts. It
stopped at record 12 on a bare cart-validation idle-watchdog stop. The run had
0 hidden access, 0 wrong-file edits, 0 forbidden-file edits, and 0
excluded-path conflicts. The runner's new promotion guard then blocked the
96-record command before execution because the pilot results contained that
abnormal signal. `bundle-quote` should stay quarantined, but the remaining
blocker is now intermittent no-edit idle tail across arms under partial
prompts, not just bundle-quote task latency or workflow-only behavior.

Full records analysis:
[`2026-06-11-benchmark-records-analysis.md`](2026-06-11-benchmark-records-analysis.md).

## Raw Artifacts

Raw `runs/` and `results/` artifacts are intentionally ignored by git. Public
docs should summarize reproducible fields from those artifacts without
committing full logs, cloned repositories, credentials, or local run output.
