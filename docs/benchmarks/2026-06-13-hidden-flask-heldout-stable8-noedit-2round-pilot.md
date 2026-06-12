# Hidden Flask Heldout Stable-8 No-Edit 2-Round Pilot - 2026-06-13

This is the first fresh stable-8 readiness pilot after adding the runner
`--agent-no-edit-timeout` watchdog.

The pilot completed all 16 planned records. `--stop-on-abnormal` did not stop
the run. All records failed strict hidden-oracle scoring, but the operational
signals were clean: 0 stalls, 0 timeouts, 0 wrong-file edits, 0 forbidden-file
edits, 0 hidden-access findings, and 0 runner errors.

## Run Conditions

- Suite: `benchmarks/suites/flask-hidden-heldout-stable-8.json`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `bare`, `workflow-only`
- Tasks: `availability-badge`, `cart-validation`, `catalog-metrics`,
  `catalog-segments`
- Repeats: 2
- Planned records: 16
- Completed records: 16
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
  --suite benchmarks/suites/flask-hidden-heldout-stable-8.json \
  --mode pilot \
  --repeats 2 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal \
  --workspace runs/hidden-flask-heldout-stable8-noedit-2round-pilot-20260612T202028Z \
  --results results/hidden-flask-heldout-stable8-noedit-2round-pilot-20260612T202028Z \
  --execute
```

## Headline

| Target | Runs | Strict | Functional | Schema contract | Workflow | Boundary | Verification passed | Hidden access | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 8 | 0 | 0 | 0 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 51s | 83s |
| `workflow-only` | 8 | 0 | 2 | 0 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 62s | 127s |

## Per-Task Results

| Target | Task | Runs | Strict | Functional | Schema contract | Workflow | Boundary | Stalls | Timeouts | p50 duration | p95 duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | `hidden-effect-availability-badge` | 2 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 51s | 74s |
| `bare` | `hidden-effect-cart-validation` | 2 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 70s | 83s |
| `bare` | `hidden-effect-catalog-metrics` | 2 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 39s | 43s |
| `bare` | `hidden-effect-catalog-segments` | 2 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 46s | 53s |
| `workflow-only` | `hidden-effect-availability-badge` | 2 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 58s | 71s |
| `workflow-only` | `hidden-effect-cart-validation` | 2 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 70s | 72s |
| `workflow-only` | `hidden-effect-catalog-metrics` | 2 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 61s | 127s |
| `workflow-only` | `hidden-effect-catalog-segments` | 2 | 0 | 2 | 0 | 2 | 2 | 0 | 0 | 56s | 62s |

## Promotion Guard Check

A dry-run 96-record promotion plan using these results as
`--require-clean-results` passed the clean-readiness gate:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-heldout-stable-8.json \
  --repeats 12 \
  --promotion-run \
  --require-clean-results results/hidden-flask-heldout-stable8-noedit-2round-pilot-20260612T202028Z \
  --min-clean-rounds 2 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal
```

The guard reported 8 task/arm pairs x 2 clean rounds from 16 prior records.

## Interpretation

The no-edit mitigation cleared the immediate operational blocker for this
stable-8 pilot: the run did not reproduce the previous no-edit idle tail on
`cart-validation`, and the guard now accepts the pilot as clean.

This is not product-value evidence. Strict success was 0/16 and schema-contract
success was 0/16. A 96-record promotion would now be operationally allowed by
the clean-readiness guard, but it would mainly measure repeated partial-realistic
oracle failures unless the product question is specifically timeout/tail
stability.

Next step: do not treat this as a reason to claim harness effectiveness. Either
run a small full-contract control to verify the hidden oracles and agent path
still pass when the contract is explicit, or build the intended three-arm
`bare` / `workflow-only` / `memory-harness` suite before spending on another
near-100 product-value run.
