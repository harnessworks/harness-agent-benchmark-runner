# Hidden Flask Three-Arm V2 Smoke - 2026-06-13

This smoke run validates the first v2 held-out three-arm task,
`hidden-effect-replenishment-signals`.

The run completed all 3 planned records with no operational abnormal:
0 stalls, 0 timeouts, 0 hidden-access findings, 0 wrong-file edits, and
0 forbidden-file edits.

## Run Conditions

- Suite: `benchmarks/suites/flask-hidden-three-arm-v2.json`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `bare`, `workflow-only`, `memory-harness`
- Task: `hidden-effect-replenishment-signals`
- Repeats: 1
- Planned records: 3
- Completed records: 3
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

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-three-arm-v2.json \
  --repeats 1 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 360 \
  --stop-on-abnormal \
  --workspace runs/hidden-flask-three-arm-v2-smoke-20260613T0206Z \
  --results results/hidden-flask-three-arm-v2-smoke-20260613T0206Z \
  --execute
```

## Headline

| Target | Runs | Strict | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | Duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 44.0s |
| `workflow-only` | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 493.9s |
| `memory-harness` | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 47.8s |

The runner printed `Completed schedule with 1 non-zero runner exits`. That
non-zero exit is the expected `bare` benchmark failure, not a runner abnormal.

## Failure Cluster

`bare` failed both split oracles:

- Functional: `domain glossary must exist`
- Schema: `catalog replenishment signals must include meta object`

This is the intended negative-control pattern for the v2 task: the prompt
provides the new route and business rules, while repository-local conventions
carry docs location and metadata-envelope expectations.

## Interpretation

This is not enough to replace the 96-record stable-4 promotion as the main
product diagnostic. It is enough to validate that the v2 task is runnable,
leakage-free at preflight, and capable of producing a clear three-arm signal.

The initial signal matches the stable-4 promotion pattern:

- `bare` misses schema/docs conventions.
- `workflow-only` can pass strict scoring on a new convention-transfer task.
- `memory-harness` also passes strict scoring.
- `memory-harness` has a much shorter duration than `workflow-only` on this
  record: 47.8s versus 493.9s.

Treat the duration result as an early smoke signal only. The next step should be
to add more v2 tasks before spending on a larger v2 promotion, so the suite can
separate one-off task luck from repeatable memory/workflow behavior.

