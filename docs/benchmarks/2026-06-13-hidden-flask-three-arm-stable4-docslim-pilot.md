# Hidden Flask Three-Arm Stable-4 Doc-Slim Pilot - 2026-06-13

This fresh full three-arm stable-4 pilot used the trimmed `memory-harness`
guidance from `87c12fb5e276e40272ceee86d497823e93def4e9`.

The pilot completed all 12 planned records with no operational abnormal. It is
the first clean three-arm partial-realistic stable-4 matrix after separating
`bare`, `workflow-only`, and `memory-harness`.

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
  `87c12fb5e276e40272ceee86d497823e93def4e9`

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-three-arm-stable4.json \
  --repeats 1 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 360 \
  --stop-on-abnormal \
  --workspace runs/hidden-flask-three-arm-stable4-docslim-pilot-20260612T2202Z \
  --results results/hidden-flask-three-arm-stable4-docslim-pilot-20260612T2202Z \
  --execute
```

## Headline

| Target | Runs | Strict | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 4 | 0 | 0 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 46s | 60s |
| `workflow-only` | 4 | 0 | 0 | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 59s | 79s |
| `memory-harness` | 4 | 1 | 1 | 3 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 61s | 69s |

## Per-Task Results

| Target | Task | Strict | Functional | Schema contract | Workflow | Boundary | Duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | `hidden-effect-availability-badge` | 0 | 0 | 0 | 1 | 1 | 53s |
| `workflow-only` | `hidden-effect-availability-badge` | 0 | 0 | 1 | 1 | 1 | 63s |
| `memory-harness` | `hidden-effect-availability-badge` | 0 | 0 | 1 | 1 | 1 | 61s |
| `bare` | `hidden-effect-cart-validation` | 0 | 0 | 0 | 1 | 1 | 60s |
| `workflow-only` | `hidden-effect-cart-validation` | 0 | 0 | 0 | 1 | 1 | 79s |
| `memory-harness` | `hidden-effect-cart-validation` | 0 | 0 | 0 | 1 | 1 | 69s |
| `bare` | `hidden-effect-catalog-metrics` | 0 | 0 | 0 | 1 | 1 | 42s |
| `workflow-only` | `hidden-effect-catalog-metrics` | 0 | 0 | 1 | 1 | 1 | 56s |
| `memory-harness` | `hidden-effect-catalog-metrics` | 0 | 0 | 1 | 1 | 1 | 64s |
| `bare` | `hidden-effect-catalog-segments` | 0 | 0 | 0 | 1 | 1 | 46s |
| `workflow-only` | `hidden-effect-catalog-segments` | 0 | 0 | 1 | 1 | 1 | 59s |
| `memory-harness` | `hidden-effect-catalog-segments` | 1 | 1 | 1 | 1 | 1 | 44s |

## Interpretation

This pilot clears the immediate operational blocker for the trimmed memory
target: 12/12 records completed, with 0 stalls, 0 timeouts, 0 hidden-access
findings, 0 wrong-file edits, and 0 forbidden-file edits.

The product signal is still small:

- `bare` remains a negative baseline under partial-realistic prompts: 0/4
  strict and 0/4 schema.
- `workflow-only` and `memory-harness` both improved schema to 3/4.
- `memory-harness` produced the only strict success, on `catalog-segments`.
- `cart-validation` remains unsolved across all arms.

This is enough to justify collecting the second clean round required by the
promotion guard if the goal is to estimate whether the small memory lift is
real. It is not enough to claim product value yet, and it is not enough to
execute the 96-record promotion run because the guard requires at least two
clean rounds. The balanced promotion shape should be 96 records (`repeats=8`)
rather than exactly 100, because the suite has 12 records per round.

The next step is one more clean 12-record round, or an equivalent fresh
2-round pilot. Promotion should still use `--jobs 1`, `--stop-on-abnormal`, and
the 360-second no-edit watchdog. Any no-edit watchdog, timeout, hidden-access
finding, wrong-file edit, or forbidden-file edit should stop interpretation as
clean product evidence.
