# Latest Benchmark Status

Updated: 2026-06-14

## At A Glance

| Question | Answer |
| --- | --- |
| Representative result | `2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md` |
| Main claim | Safety and failure measurement are strong; raw coding lift is not the main claim. |
| Cleanliness | 96/96 records completed with 0 stalls, 0 timeouts, 0 hidden-access findings, 0 wrong-file edits, and 0 forbidden-file edits. |
| Harness signal | Schema contract improved from 0/32 in `bare` to 24/32 in both harness arms. |
| Memory signal | Accuracy tied `workflow-only`; duration tail was better. |
| Latest execution | Scoped H1 promotion96 stopped after 11/96 on a `full-harness` price-policy no-edit watchdog. |

## Representative Result

Current representative report:
[`2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md`](2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md).

Supported kit-effect claim:

> In answer-free held-out Flask tasks, the kit made agent work safer and more
> measurable, and the harnessed repos preserved project API/schema conventions
> that the bare repo missed. The representative run completed 96/96 records
> with no operational abnormal events, and schema-contract success improved
> from 0/32 in `bare` to 24/32 in both harness arms.

This is the result currently promoted as the public benchmark headline. Its
claim is not "the harness always makes agents better at coding." Its claim is
more specific: the kit makes agent work safer to run and much easier to measure
when the task depends on repository-local conventions.

Why this run is representative:

- It completed the full 96-record sequential promotion with `--jobs 1`.
- It used three arms: `bare`, `workflow-only`, and `memory-harness`.
- It used answer-free `partial-realistic` prompts.
- It kept task-specific answers and hidden oracle logic out of target
  repositories.
- It separated strict, functional, schema, workflow, boundary, timeout, and
  duration-tail signals.
- It completed with 0 stalls, 0 timeouts, 0 hidden-access findings,
  0 wrong-file edits, and 0 forbidden-file edits.

| Arm | Runs | Strict | Functional | Schema contract | Workflow | Boundary clean | p95 duration | Max duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 32 | 0 | 0 | 0 | 32 | 32 | 134.6s | 639.3s |
| `workflow-only` | 32 | 8 | 8 | 24 | 32 | 32 | 124.1s | 544.7s |
| `memory-harness` | 32 | 8 | 8 | 24 | 32 | 32 | 86.2s | 87.6s |

## Interpretation

The current evidence is strongest for safety, repeatability, and failure
measurement:

- The runner distinguished 80 expected benchmark failures from runner
  abnormalities.
- The three-arm design made the `bare` baseline, workflow guidance, and memory
  layer separable.
- Hidden-access, timeout, wrong-file, and forbidden-file counts all remained
  clean in the representative promotion.
- Per-dimension scoring showed where the harness helped: schema contract
  success improved from 0/32 to 24/32 for both harness arms.
- Per-task scoring showed where the harness did not solve the task:
  `cart-validation` stayed 0/8 strict and 0/8 schema across all arms.

Correctness lift exists, but it is narrow. Both harness arms passed
`catalog-segments` 8/8 strict while `bare` passed 0/8. The same result does
not prove a general raw-coding lift, and `memory-harness` did not improve
accuracy over `workflow-only`. The memory arm's useful signal in this suite is
duration-tail repeatability.

## Latest Run

Latest executed focused H1 check:
[`2026-06-14-flask-h1-promotion96-aborted-noedit.md`](2026-06-14-flask-h1-promotion96-aborted-noedit.md).

The scoped 96-record H1 promotion used `CODEX_PROMPT_GUARD=1`, `--promotion-run`,
and the clean 16-record revised-oracle gate as readiness evidence. It stopped
after 11/96 planned records because a `full-harness`
`hidden-effect-catalog-price-policy` record hit the no-edit watchdog.

Before the stop, the partial H1 signal still separated decision-bearing arms
from controls: `decision-only` was 3/3 strict and record-consistent, completed
`full-harness` records were 2/2 strict and record-consistent, and controls were
0/5 record-consistent. The stopped record found the accepted price-band
decision record but made no repository changes for 240 seconds.

This means the H1 promotion is not achieved. The current blocker is
operational no-edit behavior in `full-harness` price-policy, not oracle
wording or control false positives.

## Controls And Prior Evidence

| Scope | Mode | Runs | Strict successes | Verification passed | Timeouts | Boundary issues | Reading |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Three-arm stable-4 | promotion96 `bare` | 32 | 0 | 0 | 0 | 0 | Representative negative baseline. |
| Three-arm stable-4 | promotion96 `workflow-only` | 32 | 8 | 8 | 0 | 0 | Workflow and docs conventions recover schema behavior. |
| Three-arm stable-4 | promotion96 `memory-harness` | 32 | 8 | 8 | 0 | 0 | Same correctness as workflow-only, lower duration tail. |
| Two-family H1 | promotion96 aborted | 11/96 | 5 | 5 | 1 | 0 | Stopped on `full-harness` price-policy no-edit after decision lookup. |
| Two-family H1 | revised-oracle four-arm gate | 16 | 8 | 8 | 0 | 0 | Decision-bearing arms 8/8 record-consistent; controls 0/8. |
| Replenishment H1 | guarded decision-bearing triage | 10 | 8 live / 10 revised | 8 live / 10 revised | 0 | 0 | Oracle wording brittleness fixed; controls still need revised-oracle rerun. |
| Two-family H1 | guarded pilot | 8 | 3 | 3 | 0 | 0 | Operationally clean, but replenishment passed only in `full-harness`; not promotion-ready. |
| Price-policy H1 | guarded stability24 rerun | 24 | 12 | 12 | 0 | 0 | Completed four-arm stability gate; decision-bearing arms 12/12 record-consistent, controls 0/12. |
| Price-policy H1 | guarded decision-arms no-edit triage | 8 | 8 | 8 | 0 | 0 | Decision-bearing arms completed cleanly; no-edit stall did not immediately reproduce. |
| Price-policy H1 | guarded stability24 expansion | 4/24 | 1 | 1 | 1 | 0 | Aborted on `full-harness` no-edit watchdog after decision-record discovery. |
| Price-policy H1 | guarded clean gate | 12 | 6 | 6 | 0 | 0 | Guarded four-arm H1 gate completed; decision memory arms separated cleanly from controls. |
| Price-policy H1 | guarded decision-only diagnostic | 2 | 2 | 2 | 0 | 0 | Prompt guard coincided with quick repo edits; mitigation signal only. |
| Price-policy H1 | stability24 expansion | 2/24 | 0 | 0 | 1 | 0 | Aborted on `decision-only` no-edit watchdog despite prior clean readiness. |
| Price-policy H1 | non-bare clean gate rerun | 12 | 6 | 6 | 0 | 0 | Completed focused H1 gate; decision memory arms separated cleanly from controls. |
| Price-policy H1 | non-bare clean gate | 8/12 | 4 | 4 | 1 | 0 | H1 signal held, but gate aborted on no-edit watchdog. |
| Three-arm v2 | replenishment smoke | 3 | 2 | 2 | 0 | 0 | Scaffold check only. |
| Balanced Flask A/B | 100-run `jobs=2` full-contract control | 100 | 94 | 95 | 3 | 0 | Useful control, but parallel timeout stability remains unresolved. |
| Hidden-oracle Flask A/B | 3x convention-dependent tasks | 24 | 11 | 11 | 3 | 11 | Historical strong signal, but older and less balanced than the representative three-arm run. |

The balanced 100-run `jobs=2` report remains useful as a full-contract control:
both arms received task-critical API contracts in the prompt. It is not the
main product claim because the prompt disclosed much more of the answer and the
parallel execution introduced timeout noise.

Older `harness-starter-kit` runs remain adapter validation evidence. The Flask
hidden-oracle rows are the relevant harness-effect evidence.

## Next Step

Do not rerun the same stable-4 96-record promotion unless the harness or runner
semantics change. For H1, do not immediately rerun the 96-record promotion.
The next useful step is targeted no-edit mitigation:

- task: `hidden-effect-catalog-price-policy`
- arm: `full-harness`
- repeat enough times to reproduce or bound the no-edit rate
- inspect whether stalls happen after decision-record lookup
- test any prompt/adapter mitigation on a small gate before promotion

Only rerun promotion after that blocker is understood.

The next useful v2 experiment remains a fresh 9-record pilot using the current
three-task suite:

- `hidden-effect-replenishment-signals`
- `hidden-effect-catalog-price-ladder`
- `hidden-effect-catalog-value-snapshot`

Keep the same three arms and continue to report functional, schema-contract,
workflow, boundary, strict, timeout, and duration-tail metrics separately.

## Detailed Reports

- [`2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md`](2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md) (representative result)
- [`2026-06-14-flask-h1-promotion96-aborted-noedit.md`](2026-06-14-flask-h1-promotion96-aborted-noedit.md) (scoped H1 promotion, aborted on no-edit)
- [`2026-06-14-flask-h1-revised-oracle-two-family-gate.md`](2026-06-14-flask-h1-revised-oracle-two-family-gate.md) (latest revised-oracle two-family H1 gate)
- [`2026-06-14-flask-replenishment-h1-guarded-triage.md`](2026-06-14-flask-replenishment-h1-guarded-triage.md) (latest guarded replenishment H1 triage)
- [`2026-06-14-flask-h1-two-family-guarded-pilot.md`](2026-06-14-flask-h1-two-family-guarded-pilot.md) (prior guarded two-family H1 pilot)
- [`2026-06-14-flask-price-policy-h1-guarded-stability24-rerun.md`](2026-06-14-flask-price-policy-h1-guarded-stability24-rerun.md) (guarded H1 stability rerun)
- [`2026-06-14-flask-price-policy-h1-decision-arms-noedit-triage.md`](2026-06-14-flask-price-policy-h1-decision-arms-noedit-triage.md) (guarded H1 decision-bearing no-edit triage)
- [`2026-06-14-flask-price-policy-h1-guarded-stability24-aborted.md`](2026-06-14-flask-price-policy-h1-guarded-stability24-aborted.md) (guarded H1 stability expansion, aborted)
- [`2026-06-14-flask-price-policy-h1-guarded-clean-gate.md`](2026-06-14-flask-price-policy-h1-guarded-clean-gate.md) (guarded H1 clean gate)
- [`2026-06-14-flask-price-policy-h1-decision-guard-diagnostic.md`](2026-06-14-flask-price-policy-h1-decision-guard-diagnostic.md) (guarded H1 decision-only diagnostic)
- [`2026-06-14-flask-price-policy-h1-stability24-aborted.md`](2026-06-14-flask-price-policy-h1-stability24-aborted.md) (focused H1 stability expansion, aborted)
- [`2026-06-14-flask-price-policy-h1-clean-gate-rerun.md`](2026-06-14-flask-price-policy-h1-clean-gate-rerun.md) (focused H1 clean gate rerun)
- [`2026-06-14-flask-price-policy-h1-clean-gate-aborted.md`](2026-06-14-flask-price-policy-h1-clean-gate-aborted.md) (focused H1 clean gate, aborted)
- [`2026-06-14-flask-price-policy-h1-discoverability-3x.md`](2026-06-14-flask-price-policy-h1-discoverability-3x.md) (focused H1 discoverability triage)
- [`2026-06-14-flask-price-policy-h1-rerun-3x.md`](2026-06-14-flask-price-policy-h1-rerun-3x.md) (focused H1 triage)
- [`2026-06-13-hidden-flask-three-arm-v2-smoke.md`](2026-06-13-hidden-flask-three-arm-v2-smoke.md) (latest v2 scaffold check)
- [`2026-06-13-hidden-flask-workflow-smoke-stable4-fullcontract-control.md`](2026-06-13-hidden-flask-workflow-smoke-stable4-fullcontract-control.md) (full-contract control)
- [`2026-06-12-hidden-flask-balanced-ab-100-jobs2.md`](2026-06-12-hidden-flask-balanced-ab-100-jobs2.md) (100-run full-contract control)
- [`2026-06-11-hidden-oracle-harness-effect-ab-3x.md`](2026-06-11-hidden-oracle-harness-effect-ab-3x.md) (historical hidden-oracle A/B)
- [`2026-06-11-benchmark-records-analysis.md`](2026-06-11-benchmark-records-analysis.md) (records analysis)

## Raw Artifacts

Raw `runs/` and `results/` artifacts are intentionally ignored by git. Public
docs should summarize reproducible fields from those artifacts without
committing full logs, cloned repositories, credentials, or local run output.
