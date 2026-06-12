# Hidden Flask Three-Arm Stable-4 Pilot Aborted - 2026-06-13

This was the first fresh three-arm partial-realistic product pilot after adding
the separate `memory-harness` target. It did not complete. The run stopped at
record 5 of 12 because `--stop-on-abnormal` saw a `no_edit_watchdog` termination
on `workflow-only` `cart-validation`.

Do not promote from this pilot to a 100-run experiment. It produced an abnormal
operational signal before enough `memory-harness` records existed to evaluate
product lift.

## Run Conditions

- Suite: `benchmarks/suites/flask-hidden-three-arm-stable4.json`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `bare`, `workflow-only`, `memory-harness`
- Tasks: `availability-badge`, `cart-validation`, `catalog-metrics`,
  `catalog-segments`
- Repeats: 1
- Planned records: 12
- Completed records: 5
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 240`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Codex model/config: `gpt-5.5`,
  `CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`
- Prompt guard: `CODEX_PROMPT_GUARD=1`

Target refs:

- `bare`: `../flask-no-harness` at
  `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- `workflow-only`: `../flask-yes-harness` at
  `0f478ddede915b2f0cf41662373c53d8c70f3f86`
- `memory-harness`: `../flask-memory-harness` at
  `bc097c48d592e7ddcd26beb7bb2c185d7a33fa59`

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-three-arm-stable4.json \
  --repeats 1 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal \
  --workspace runs/hidden-flask-three-arm-stable4-pilot-20260612T211212Z \
  --results results/hidden-flask-three-arm-stable4-pilot-20260612T211212Z \
  --execute
```

## Headline

| Target | Runs | Strict | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 2 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 61s | 75s |
| `workflow-only` | 2 | 0 | 0 | 0 | 1 | 2 | 0 | 1 | 1 | 0 | 0 | 220s | 240s |
| `memory-harness` | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 62s | 62s |

## Completed Records

| Target | Task | Strict | Functional | Schema contract | Workflow | Boundary | Result |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `bare` | `hidden-effect-availability-badge` | 0 | 0 | 0 | 1 | 1 | Implemented but missed restock behavior and `meta` envelope. |
| `workflow-only` | `hidden-effect-availability-badge` | 0 | 0 | 0 | 1 | 1 | Implemented but missed unknown-SKU behavior and `meta` envelope. |
| `memory-harness` | `hidden-effect-availability-badge` | 0 | 0 | 0 | 1 | 1 | Implemented but missed restock behavior and `meta` envelope. |
| `bare` | `hidden-effect-cart-validation` | 0 | 0 | 0 | 1 | 1 | Implemented but returned 200 for unknown SKU and missed `meta` envelope. |
| `workflow-only` | `hidden-effect-cart-validation` | 0 | 0 | 0 | 0 | 1 | Stopped by `no_edit_watchdog` after 240 seconds with no repository changes. |

## Interpretation

The pilot answered the immediate promotion question: do not run the larger
experiment from this state. The abnormal stop happened before the run reached
the `memory-harness` `cart-validation` record or either `catalog-*` task, so
there is no valid three-arm product comparison.

The abnormal record was not a hidden-oracle or boundary failure. The agent read
the prompt, app, tests, and harness docs, but made no visible repository change
before the 240-second no-edit watchdog terminated it. Verification then ran
against an unchanged repository, so the hidden oracle returned 404 for
`POST /cart/validate`.

The first four completed implementation records also show that the
partial-realistic prompt still lacks enough generalizable convention signal to
produce schema-contract success: all four missed the generic `meta` envelope.
The `memory-harness` arm had only one completed record and did not show lift on
`availability-badge`.

## Next Step

Keep the 100-run promotion blocked. The next run should be another fresh
small pilot, not a scaled evidence run:

- Keep the three-arm structure, but use a balanced 9- or 12-record pilot rather
  than forcing an arbitrary 10-record count that would imbalance arms.
- Keep `--jobs 1` until the no-edit tail is stable; do not add `jobs=2` while
  the operational blocker is first-edit latency.
- Keep `--stop-on-abnormal` and the no-edit watchdog, but consider raising the
  no-edit threshold from 240s to 360s only if the product question accepts
  slower harness-guided exploration as a cost. A small Flask task with no edit
  after 240s should still count as operational risk.
- Before rerunning, improve only generalized, non-task-specific guidance around
  API response envelopes and error status conventions. Do not add held-out
  route names, oracle payloads, exact response keys, or task-specific examples
  to target docs.

