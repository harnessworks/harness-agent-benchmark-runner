# Hidden Flask Workflow-Smoke Stable-4 Full-Contract Control - 2026-06-13

This control checks whether the hidden-oracle path and Codex adapter can pass
the same four stable tasks when the task-critical API contract is explicit in
the prompt. It is a control for the partial-realistic stable-8 heldout pilot,
not product-value evidence.

## Run Conditions

- Suite: `benchmarks/suites/flask-hidden-workflow-smoke.json`
- Split: `calibration`
- Prompt variant: `full-contract`
- Selected tasks: `availability-badge`, `cart-validation`, `catalog-metrics`,
  `catalog-segments`
- Arms: `bare`, `workflow-only`
- Repeats: 1
- Planned records: 8
- Completed records: 8
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

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-workflow-smoke.json \
  --task-id hidden-effect-availability-badge \
  --task-id hidden-effect-cart-validation \
  --task-id hidden-effect-catalog-metrics \
  --task-id hidden-effect-catalog-segments \
  --repeats 1 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal \
  --workspace runs/hidden-flask-workflow-smoke-stable4-control-20260612T204629Z \
  --results results/hidden-flask-workflow-smoke-stable4-control-20260612T204629Z \
  --execute
```

## Initial Control Result

| Target | Runs | Strict | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 4 | 3 | 3 | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 58s | 68s |
| `workflow-only` | 4 | 3 | 3 | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 90s | 140s |

Per task:

| Target | Task | Strict | Functional | Schema contract | Workflow | Boundary | Duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | `hidden-effect-availability-badge` | 1 | 1 | 1 | 1 | 1 | 68s |
| `workflow-only` | `hidden-effect-availability-badge` | 1 | 1 | 1 | 1 | 1 | 77s |
| `bare` | `hidden-effect-cart-validation` | 0 | 0 | 0 | 1 | 1 | 63s |
| `workflow-only` | `hidden-effect-cart-validation` | 0 | 0 | 0 | 1 | 1 | 140s |
| `bare` | `hidden-effect-catalog-metrics` | 1 | 1 | 1 | 1 | 1 | 55s |
| `workflow-only` | `hidden-effect-catalog-metrics` | 1 | 1 | 1 | 1 | 1 | 102s |
| `bare` | `hidden-effect-catalog-segments` | 1 | 1 | 1 | 1 | 1 | 58s |
| `workflow-only` | `hidden-effect-catalog-segments` | 1 | 1 | 1 | 1 | 1 | 90s |

The two failures were both `cart-validation`, and both failed with:

```text
hidden oracle failure: cart validation summary is wrong
```

Inspection showed both agents returned:

```json
{"summary":{"requested_quantity":7,"accepted_quantity":5,"rejected_quantity":2}}
```

The strict oracle expected:

```json
{"summary":{"requested":7,"accepted":5,"rejected":2}}
```

That is a full-contract prompt ambiguity, not an operational abnormal. The run
had 0 stalls, 0 timeouts, 0 hidden-access findings, and 0 file-boundary issues.

## Mitigation

The full-contract `cart-validation` prompts in both
`benchmarks/tasks/flask-hidden-workflow-smoke/` and
`benchmarks/tasks/flask-hidden-balanced/` now explicitly say:

```text
The summary object must use exactly these quantity keys: requested, accepted,
rejected.
```

The split functional oracle also now checks the `summary` object before
recursing into item rows, so item-level `requested_quantity` no longer masks the
aggregate summary value.

## Focused Verification

After the prompt/oracle fix, a focused two-record `cart-validation`
full-contract control passed both arms:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-workflow-smoke.json \
  --task-id hidden-effect-cart-validation \
  --repeats 1 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal \
  --workspace runs/hidden-flask-workflow-smoke-cartvalidation-promptfix-20260612T210126Z \
  --results results/hidden-flask-workflow-smoke-cartvalidation-promptfix-20260612T210126Z \
  --execute
```

| Target | Runs | Strict | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 166s |
| `workflow-only` | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 89s |

## Interpretation

The full-contract control shows the hidden oracle and adapter path are capable
of passing these stable tasks when the exact API contract is provided. The
partial-realistic stable-8 result should therefore be read as a prompt/convention
generalization failure, not as proof that the runner or hidden oracle path is
broken.

The next product-value step is still not a 96-record partial-realistic
promotion. The better next step is to build or run the intended three-arm
`bare` / `workflow-only` / `memory-harness` design, or to create a smaller
partial-realistic pilot whose conventions are clear enough to produce nonzero
schema-contract signal before scaling.
