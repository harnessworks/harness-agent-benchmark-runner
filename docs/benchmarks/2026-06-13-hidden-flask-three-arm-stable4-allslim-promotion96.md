# Hidden Flask Three-Arm Stable-4 All-Slim Promotion96 - 2026-06-13

This report records the fresh all-slim three-arm readiness run and the following
96-record promotion run for the stable-4 held-out Flask suite.

This run is promoted as the current representative result for the kit's
safety-and-measurement claim. It is representative because it used
answer-free partial-realistic prompts, kept task-specific answers out of target
repositories, ran a three-arm comparison, and separated failure dimensions
instead of reducing the outcome to one pass/fail number.

Supported kit-effect claim:

> In answer-free held-out Flask tasks, the kit made agent work safer and more
> measurable, and the harnessed repos preserved project API/schema conventions
> that the bare repo missed. The representative run completed 96/96 records
> with no operational abnormal events, and schema-contract success improved
> from 0/32 in `bare` to 24/32 in both harness arms.

The promotion completed all 96 planned records with no operational abnormal:
0 stalls, 0 timeouts, 0 hidden-access findings, 0 wrong-file edits, and
0 forbidden-file edits.

## Run Conditions

- Suite: `benchmarks/suites/flask-hidden-three-arm-stable4.json`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `bare`, `workflow-only`, `memory-harness`
- Tasks: `availability-badge`, `cart-validation`, `catalog-metrics`,
  `catalog-segments`
- Promotion repeats: 8
- Promotion planned records: 96
- Promotion completed records: 96
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Prompt guard: `CODEX_PROMPT_GUARD=1`

Target refs:

- `bare`: `../flask-no-harness` at
  `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- `workflow-only`: `../flask-yes-harness` at
  `3933a09a74cfefbd8455eb3aecd1ff225d7a7457`
- `memory-harness`: `../flask-memory-harness` at
  `87c12fb5e276e40272ceee86d497823e93def4e9`

Promotion command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-three-arm-stable4.json \
  --repeats 8 \
  --promotion-run \
  --require-clean-results results/hidden-flask-three-arm-stable4-allslim-2round-20260612T2252Z \
  --min-clean-rounds 2 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 360 \
  --stop-on-abnormal \
  --workspace runs/hidden-flask-three-arm-stable4-allslim-promotion96-20260612T2325Z \
  --results results/hidden-flask-three-arm-stable4-allslim-promotion96-20260612T2325Z \
  --execute
```

The promotion guard accepted the prior fresh readiness set at
`results/hidden-flask-three-arm-stable4-allslim-2round-20260612T2252Z`.
That readiness run completed 24/24 records with 0 abnormal events:

| Target | Runs | Strict | Functional | Schema contract | Workflow | Max duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 8 | 0 | 0 | 0 | 8 | 85.1s |
| `workflow-only` | 8 | 2 | 2 | 6 | 8 | 212.4s |
| `memory-harness` | 8 | 2 | 2 | 6 | 8 | 100.5s |

## Headline

| Target | Runs | Strict | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | p95 duration | Max duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 32 | 0 | 0 | 0 | 32 | 32 | 0 | 0 | 0 | 0 | 0 | 61.3s | 134.6s | 639.3s |
| `workflow-only` | 32 | 8 | 8 | 24 | 32 | 32 | 0 | 0 | 0 | 0 | 0 | 59.2s | 124.1s | 544.7s |
| `memory-harness` | 32 | 8 | 8 | 24 | 32 | 32 | 0 | 0 | 0 | 0 | 0 | 58.8s | 86.2s | 87.6s |

The runner printed `Completed schedule with 80 non-zero runner exits`. Those
80 exits are expected benchmark failures, not runner abnormalities. They are
the 96 records minus the 16 strict successes.

## Representative Reading

| Signal | Reading |
| --- | --- |
| Safety | 96/96 records completed with 0 stalls, 0 timeouts, 0 hidden-access findings, 0 wrong-file edits, and 0 forbidden-file edits. |
| Failure measurement | Strict, functional, schema, workflow, boundary, hidden-access, timeout, and duration-tail signals are separable. |
| Harness workflow value | Harness arms recovered schema-contract behavior in 24/32 records; `bare` recovered 0/32. |
| Correctness value | Strict lift was real but narrow: `catalog-segments` passed 8/8 for both harness arms and 0/8 for `bare`. |
| Memory value | `memory-harness` tied `workflow-only` on correctness, but had the lowest duration tail. |
| Known hard failure | `cart-validation` stayed 0/8 strict and 0/8 schema across all arms, so it should not be treated as a clean memory discriminator. |

## Per-Task Results

| Target | Task | Runs | Strict | Functional | Schema contract | Workflow | p95 duration | Max duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | `hidden-effect-availability-badge` | 8 | 0 | 0 | 0 | 8 | 134.6s | 134.6s |
| `workflow-only` | `hidden-effect-availability-badge` | 8 | 0 | 0 | 8 | 8 | 70.3s | 70.3s |
| `memory-harness` | `hidden-effect-availability-badge` | 8 | 0 | 0 | 8 | 8 | 81.2s | 81.2s |
| `bare` | `hidden-effect-cart-validation` | 8 | 0 | 0 | 0 | 8 | 109.0s | 109.0s |
| `workflow-only` | `hidden-effect-cart-validation` | 8 | 0 | 0 | 0 | 8 | 124.1s | 124.1s |
| `memory-harness` | `hidden-effect-cart-validation` | 8 | 0 | 0 | 0 | 8 | 87.6s | 87.6s |
| `bare` | `hidden-effect-catalog-metrics` | 8 | 0 | 0 | 0 | 8 | 63.6s | 63.6s |
| `workflow-only` | `hidden-effect-catalog-metrics` | 8 | 0 | 0 | 8 | 8 | 544.7s | 544.7s |
| `memory-harness` | `hidden-effect-catalog-metrics` | 8 | 0 | 0 | 8 | 8 | 77.5s | 77.5s |
| `bare` | `hidden-effect-catalog-segments` | 8 | 0 | 0 | 0 | 8 | 639.3s | 639.3s |
| `workflow-only` | `hidden-effect-catalog-segments` | 8 | 8 | 8 | 8 | 8 | 62.1s | 62.1s |
| `memory-harness` | `hidden-effect-catalog-segments` | 8 | 8 | 8 | 8 | 8 | 60.8s | 60.8s |

## Failure Clusters

- `availability-badge`: both harness arms recovered schema contract in 8/8
  runs, but no arm passed functional scoring. Most failures were missing-SKU
  error contract misses.
- `cart-validation`: all arms scored 0/8 strict and 0/8 schema. Harness arms
  preserved workflow and metadata, but repeatedly missed unknown-SKU client
  error behavior or response shape.
- `catalog-metrics`: both harness arms recovered schema contract in 8/8 runs,
  but no arm passed functional scoring. Failures concentrated on average-price
  glossary coverage or highest-stock field naming.
- `catalog-segments`: both harness arms passed 8/8 strict. Bare scored 0/8,
  mostly because it lacked the required domain glossary and metadata envelope.

## Interpretation

This is the first clean 96-record three-arm representative result for the
answer-free stable-4 suite. The strongest claim is not raw coding uplift. The
strongest claim is that the kit makes agent work safe to run and precise to
diagnose.

The run shows that the benchmark can tell apart:

- expected benchmark failures versus runner abnormalities;
- functional endpoint failures versus schema-contract failures;
- workflow/local-gate success versus hidden-oracle success;
- file-boundary discipline versus task correctness;
- timeout/no-edit problems versus semantic implementation problems.

That separation is the main product value. It converts "the agent failed" into
actionable failure classes:

- `bare` is a strong negative baseline under partial-realistic prompts:
  0/32 strict and 0/32 schema.
- `workflow-only` and `memory-harness` both improved schema contract to 24/32
  and strict success to 8/32.
- The strict lift came entirely from `catalog-segments`.
- The schema lift came from `availability-badge`, `catalog-metrics`, and
  `catalog-segments`.
- `cart-validation` remains unsolved across all arms and should be redesigned
  or split before being used as a memory-specific discriminator.

The `memory-harness` did not beat `workflow-only` on strict, functional, or
schema accuracy in this suite. Its useful signal is operational: it had a much
lower duration tail (`p95` 86.2s, max 87.6s) than `workflow-only` (`p95` 124.1s,
max 544.7s) and `bare` (max 639.3s). Treat that as latency/repeatability
evidence, not as proof of better correctness.

## Recommended Next Step

Do not spend the next run on another identical 96-record promotion. The current
suite has answered its main question for this scope: the kit is strong at
safety and failure measurement, harness workflow guidance helps contract shape
and one convention-transfer task, and memory-specific guidance does not yet add
accuracy beyond workflow-only.

The next product experiment should be a v2 held-out suite:

- Keep the same three arms: `bare`, `workflow-only`, `memory-harness`.
- Keep `partial-realistic` as the main product prompt and `full-contract` as a
  control.
- Add more held-out tasks that require applying general project conventions to
  new routes.
- Split or redesign `cart-validation`; it is currently a hard semantic task,
  not a clean harness-memory discriminator.
- Keep task-specific answers out of target docs and failure memory.
- Continue reporting functional, schema-contract, workflow, boundary, strict,
  timeout, and duration-tail metrics separately.
