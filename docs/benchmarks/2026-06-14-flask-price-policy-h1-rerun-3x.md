# Flask Price-Policy H1 Rerun 3x - 2026-06-14

This was a focused H1 rerun after triaging the
`hidden-effect-catalog-price-policy` oracle. It measured only the direct
decision-memory task across the five memory experiment arms.

The run completed all 15 planned records with 0 stalls, 0 timeouts,
0 hidden-access findings, 0 preflight failures, and 0 forbidden-file edits.
There were 3 wrong-file edits, all in the `bare` arm.

This is not a representative benchmark result. It is focused H1 evidence under
the revised price-policy oracle.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Task: `hidden-effect-catalog-price-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `bare`, `workflow-only`, `decision-only`, `failure-only`,
  `full-harness`
- Repeats: 3
- Planned records: 15
- Completed records: 15
- Concurrency: `--jobs 1`
- Stop-on-abnormal: disabled
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Codex model/config: `gpt-5.5`,
  `model_reasoning_effort=medium`, `service_tier=priority`
- Runner ref at run start: `bd0c62e`
- Started: `2026-06-13T16:37:12Z`
- Finished: `2026-06-13T17:01:06Z`

Target refs:

- `bare`: `../flask-no-harness` at
  `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- `workflow-only`: `../flask-workflow-only` at
  `1a79d8cf9e0799789b3da8029dbbb5a572b3133e`
- `decision-only`: `../flask-decision-only` at
  `12284d76e6bddab685e347a0ab9af5814fe72e61`
- `failure-only`: `../flask-failure-only` at
  `18330ea23880b1ca7a647ea58b0d694e2c658fc8`
- `full-harness`: `../flask-memory-harness` at
  `bd1a0f4cda36144fc07d0293117dc9ba3d35ab75`

Command:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-price-policy \
  --repeats 3 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 360 \
  --execute
```

## Headline

| Arm | Runs | Strict | Functional | Schema | Workflow | Boundary | Record consistency | Wrong-file edits | Forbidden-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 3 | 0 | 0 | 0 | 0 | 0 | 0/3 | 3 | 0 | 72s | 74s |
| `workflow-only` | 3 | 0 | 3 | 3 | 3 | 3 | 0/3 | 0 | 0 | 58s | 66s |
| `decision-only` | 3 | 1 | 3 | 3 | 3 | 3 | 1/3 | 0 | 0 | 59s | 64s |
| `failure-only` | 3 | 0 | 3 | 3 | 3 | 3 | 0/3 | 0 | 0 | 70s | 70s |
| `full-harness` | 3 | 1 | 3 | 3 | 3 | 3 | 1/3 | 0 | 0 | 53s | 62s |

Overall strict success was 2/15. Both decision-bearing arms had one
record-consistency success:

- `decision-only`: 1/3
- `full-harness`: 1/3

The non-decision arms stayed negative:

- `workflow-only`: 0/3 because no price-band decision record exists.
- `failure-only`: 0/3 because no price-band decision record exists.
- `bare`: 0/3, with missing docs/schema/workflow and wrong-file edits.

## Failure Pattern

Most non-bare failures were isolated to `record_consistency`.

- `workflow-only` and `failure-only`: failed because
  `docs/decisions/0002-adopt-catalog-price-band-policy.md` does not exist.
- `decision-only`: two failures used a 40.00-style threshold; the hidden 37.00
  edge must be `premium` under the decision record.
- `full-harness`: two failures used a 40.00-style threshold; the hidden 37.00
  edge must be `premium` under the decision record.
- `bare`: all three records lacked the required decision record and also missed
  the harnessed docs/schema/workflow expectations.

## Interpretation

The revised oracle produces the intended H1 shape better than the original 1x
pilot:

- decision-bearing arms can pass record consistency;
- non-decision arms remain negative controls;
- failures are now about the actual decision threshold, not summary nesting.

The signal is still weak: `decision-only` and `full-harness` each passed only
1/3. This is not enough to claim stable direct decision-memory behavior. The
next useful step is to either improve record discoverability in the target
guidance or add another H1 task, then rerun a small mixed H1/H2 pilot.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260613T163712Z/2026-06-13.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260613T163712Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-price-policy-h1-rerun-3x.md`
