# Latest Benchmark Status

Updated: 2026-06-13

## At A Glance

| Question | Answer |
| --- | --- |
| Representative result | `2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md` |
| Main claim | Safety and failure measurement are strong; raw coding lift is not the main claim. |
| Cleanliness | 96/96 records completed with 0 stalls, 0 timeouts, 0 hidden-access findings, 0 wrong-file edits, and 0 forbidden-file edits. |
| Harness signal | Schema contract improved from 0/32 in `bare` to 24/32 in both harness arms. |
| Memory signal | Accuracy tied `workflow-only`; duration tail was better. |
| Latest execution | v2 replenishment smoke, useful as scaffold validation only. |

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

Latest executed scaffold check:
[`2026-06-13-hidden-flask-three-arm-v2-smoke.md`](2026-06-13-hidden-flask-three-arm-v2-smoke.md).

The v2 smoke completed 3/3 records cleanly for
`hidden-effect-replenishment-signals`. `bare` failed functional/schema scoring,
while `workflow-only` and `memory-harness` both passed strict scoring. This
validates the v2 task scaffold and gives an early convention-transfer signal;
it is not a replacement for the 96-record representative result.

## Controls And Prior Evidence

| Scope | Mode | Runs | Strict successes | Verification passed | Timeouts | Boundary issues | Reading |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Three-arm stable-4 | promotion96 `bare` | 32 | 0 | 0 | 0 | 0 | Representative negative baseline. |
| Three-arm stable-4 | promotion96 `workflow-only` | 32 | 8 | 8 | 0 | 0 | Workflow and docs conventions recover schema behavior. |
| Three-arm stable-4 | promotion96 `memory-harness` | 32 | 8 | 8 | 0 | 0 | Same correctness as workflow-only, lower duration tail. |
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
semantics change. The next useful experiment is a fresh 9-record v2 pilot using
the current three-task suite:

- `hidden-effect-replenishment-signals`
- `hidden-effect-catalog-price-ladder`
- `hidden-effect-catalog-value-snapshot`

Keep the same three arms and continue to report functional, schema-contract,
workflow, boundary, strict, timeout, and duration-tail metrics separately.

## Detailed Reports

- [`2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md`](2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md) (representative result)
- [`2026-06-13-hidden-flask-three-arm-v2-smoke.md`](2026-06-13-hidden-flask-three-arm-v2-smoke.md) (latest v2 scaffold check)
- [`2026-06-13-hidden-flask-workflow-smoke-stable4-fullcontract-control.md`](2026-06-13-hidden-flask-workflow-smoke-stable4-fullcontract-control.md) (full-contract control)
- [`2026-06-12-hidden-flask-balanced-ab-100-jobs2.md`](2026-06-12-hidden-flask-balanced-ab-100-jobs2.md) (100-run full-contract control)
- [`2026-06-11-hidden-oracle-harness-effect-ab-3x.md`](2026-06-11-hidden-oracle-harness-effect-ab-3x.md) (historical hidden-oracle A/B)
- [`2026-06-11-benchmark-records-analysis.md`](2026-06-11-benchmark-records-analysis.md) (records analysis)

## Raw Artifacts

Raw `runs/` and `results/` artifacts are intentionally ignored by git. Public
docs should summarize reproducible fields from those artifacts without
committing full logs, cloned repositories, credentials, or local run output.
