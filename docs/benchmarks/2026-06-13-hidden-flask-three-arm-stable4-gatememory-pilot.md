# Hidden Flask Three-Arm Stable-4 Gate/Memory Pilot - 2026-06-13

This was the fresh three-arm stable-4 pilot after two generalized mitigations:

- `workflow-only` target: strengthened the generic API style gate so new public
  routes must be documented under `docs/domain/` and feature tests must assert
  response `meta.service`.
- `memory-harness` target: included the same gate plus generalized response-key
  and response-metadata failure memory. No held-out route names, hidden oracle
  payloads, task-specific versions, or exact task answer strings were added to
  target docs.

The run produced all 12 planned records, but the final record hit the
`no_edit_watchdog`. This blocks promotion to a 100-run product experiment.

## Run Conditions

- Suite: `benchmarks/suites/flask-hidden-three-arm-stable4.json`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `bare`, `workflow-only`, `memory-harness`
- Tasks: `availability-badge`, `cart-validation`, `catalog-metrics`,
  `catalog-segments`
- Repeats: 1
- Planned records: 12
- Completed records: 12
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Codex model/config: `gpt-5.5`,
  `CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`
- Prompt guard: `CODEX_PROMPT_GUARD=1`

Target refs:

- `bare`: `../flask-no-harness` at
  `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- `workflow-only`: `../flask-yes-harness` at
  `8227136359b6c2807c3fa6630f2ce840b59e7281`
- `memory-harness`: `../flask-memory-harness` at
  `a710c2c1f237aeb1cd3ebd772dd28fe25d28b740`

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-three-arm-stable4.json \
  --repeats 1 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 360 \
  --stop-on-abnormal \
  --workspace runs/hidden-flask-three-arm-stable4-gatememory-pilot-20260612T2134Z \
  --results results/hidden-flask-three-arm-stable4-gatememory-pilot-20260612T2134Z \
  --execute
```

## Headline

| Target | Runs | Strict | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 4 | 0 | 0 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 49s | 85s |
| `workflow-only` | 4 | 1 | 1 | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 53s | 75s |
| `memory-harness` | 4 | 0 | 0 | 2 | 3 | 4 | 0 | 1 | 1 | 0 | 0 | 57s | 360s |

## Per-Task Results

| Target | Task | Strict | Functional | Schema contract | Workflow | Boundary | Result |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `bare` | `hidden-effect-availability-badge` | 0 | 0 | 0 | 1 | 1 | Missing-SKU behavior and `meta` envelope missed. |
| `workflow-only` | `hidden-effect-availability-badge` | 0 | 0 | 1 | 1 | 1 | Schema fixed; missing SKU returned the wrong error contract. |
| `memory-harness` | `hidden-effect-availability-badge` | 0 | 0 | 1 | 1 | 1 | Same as workflow-only. |
| `bare` | `hidden-effect-cart-validation` | 0 | 0 | 0 | 1 | 1 | Summary keys and `meta` envelope missed. |
| `workflow-only` | `hidden-effect-cart-validation` | 0 | 0 | 0 | 1 | 1 | Included `meta`, but unknown SKU returned `200` instead of a client error. |
| `memory-harness` | `hidden-effect-cart-validation` | 0 | 0 | 0 | 1 | 1 | Response-key memory helped summary names, but unknown SKU still returned `200`. |
| `bare` | `hidden-effect-catalog-metrics` | 0 | 0 | 0 | 1 | 1 | Stock extrema field and `meta` envelope missed. |
| `workflow-only` | `hidden-effect-catalog-metrics` | 0 | 0 | 1 | 1 | 1 | Schema fixed; docs missed the average price concept. |
| `memory-harness` | `hidden-effect-catalog-metrics` | 0 | 0 | 1 | 1 | 1 | Schema fixed; stock extrema field missed. |
| `bare` | `hidden-effect-catalog-segments` | 0 | 0 | 0 | 1 | 1 | Domain docs and `meta` envelope missed. |
| `workflow-only` | `hidden-effect-catalog-segments` | 1 | 1 | 1 | 1 | 1 | Passed strict scoring. |
| `memory-harness` | `hidden-effect-catalog-segments` | 0 | 0 | 0 | 0 | 1 | Stopped by `no_edit_watchdog` after 360 seconds with no repository changes. |

## Interpretation

The mitigation improved the schema signal but did not produce product-value
evidence strong enough to scale:

- The previous `workflow-only` `cart-validation` no-edit abort did not
  reproduce. It completed in 75 seconds with no file-boundary issues.
- `workflow-only` improved from 0 schema successes in the prior aborted pilot to
  3/4 schema successes, and reached the only strict success in this run.
- `memory-harness` improved schema on 2/4 tasks but did not beat
  `workflow-only`; it had 0 strict successes and the only no-edit watchdog stop.
- `bare` stayed at 0/4 strict, 0/4 functional, and 0/4 schema, which confirms
  the partial-realistic prompts are still hard without repository-local
  guidance.
- Functional failures remain mostly about hidden behavior generalization:
  missing-SKU status handling, stock extrema fields, and required domain
  concepts. The generalized response metadata memory alone does not solve
  those behaviors.

The right conclusion is not "run 100." The pilot still contains a promotion
blocker: `memory-harness` had a 360-second no-edit tail on `catalog-segments`.
Even ignoring that tail, memory did not show lift over workflow-only in this
single-repeat matrix.

## Next Step

Do not start a 100-run experiment from this state.

The next useful work is to reduce memory-harness latency and improve only
generalized behavior guidance:

- Keep `jobs=1`; do not move to `jobs=2` while the memory arm still has a
  first-edit latency tail.
- Keep the three-arm stable-4 matrix, but rerun only after memory docs are
  shorter or better organized so agents do not spend 360 seconds reading without
  editing.
- Consider a targeted one-record rerun of `memory-harness`
  `catalog-segments` after that documentation reduction. If it still no-edits,
  treat the memory harness as operationally too heavy for this benchmark shape.
- Do not add held-out route names, task-specific version strings, exact oracle
  payloads, or exact hidden response keys to target docs.

