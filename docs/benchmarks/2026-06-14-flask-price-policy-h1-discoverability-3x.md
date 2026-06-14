# Flask Price-Policy H1 Discoverability Rerun 3x - 2026-06-14

This was a focused H1 rerun after adding narrow decision-record discovery
guidance to the two decision-bearing target variants.

The run completed all 15 planned records, but it was not operationally clean:
2 records stalled/timed out. Treat this as targeted H1 triage evidence, not as
a representative benchmark result.

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
- Runner ref at run start:
  `0819a4d1ea72ef94125bf3f681f743d05b53c5aa`
- Started: `2026-06-13T17:06:00Z`
- Finished: `2026-06-14T02:08:54Z`

Target refs:

- `bare`: `../flask-no-harness` at
  `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- `workflow-only`: `../flask-workflow-only` at
  `1a79d8cf9e0799789b3da8029dbbb5a572b3133e`
- `decision-only`: `../flask-decision-only` at
  `95a843171d2183865c8698207b3b7d4075ba567b`
- `failure-only`: `../flask-failure-only` at
  `18330ea23880b1ca7a647ea58b0d694e2c658fc8`
- `full-harness`: `../flask-memory-harness` at
  `51700b72737a32fd9d96625a7547e28562865c57`

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

| Arm | Runs | Strict | Functional | Schema | Workflow | Boundary | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 3 | 0 | 0 | 0 | 0 | 1 | 0/3 | 1 | 1 | 2 | 0 | 310s | 360s |
| `workflow-only` | 3 | 0 | 3 | 3 | 3 | 3 | 0/3 | 0 | 0 | 0 | 0 | 62s | 270s |
| `decision-only` | 3 | 3 | 3 | 3 | 3 | 3 | 3/3 | 0 | 0 | 0 | 0 | 57s | 64s |
| `failure-only` | 3 | 0 | 3 | 3 | 3 | 3 | 0/3 | 0 | 0 | 0 | 0 | 59s | 385s |
| `full-harness` | 3 | 2 | 2 | 2 | 2 | 3 | 2/3 | 1 | 1 | 0 | 0 | 52s | 358s |

Overall strict success was 5/15. Record-consistency successes were:

- `decision-only`: 3/3
- `full-harness`: 2/3
- `workflow-only`: 0/3
- `failure-only`: 0/3
- `bare`: 0/3

## H1 Reading

The guidance change improved the direct decision-memory signal:

- `decision-only` moved from 1/3 in the prior H1 rerun to 3/3 here.
- `full-harness` moved from 1/3 to 2/3 overall, and 2/2 among non-stalled
  records.
- Non-decision controls stayed negative at 0/3 record consistency.

This supports a narrow claim: when the target tells agents to search accepted
decision records for adopted repository policies, agents more reliably apply
the price-band decision. It does not prove a broad decision-memory effect
outside this task family.

## Operational Notes

This run is not promotable as a clean result:

- 2 records had `agent_stalled=true` and `agent_timed_out=true`.
- The stalled records were `bare` round 1 and `full-harness` round 3.
- The `full-harness` stalled record never implemented the route, so its H1
  failure is operational rather than a threshold mismatch.
- `bare` had 2 wrong-file edits and remained an expected negative control.
- There were 0 hidden-access findings, 0 preflight failures, and
  0 forbidden-file edits.

The long local wall-clock span should not be read as agent CPU time. Use the
recorded per-agent durations for benchmark comparison.

## Next Step

Keep the target guidance change. For the next evidence run, use either:

- a smaller H1-only rerun with `--stop-on-abnormal` to validate operational
  cleanliness after the first abnormal signal; or
- a mixed H1/H2 pilot only after the stall pattern is understood.

Do not promote this result to the representative benchmark headline.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260613T170559Z/2026-06-13.jsonl`
  and
  `results/hidden-flask-ab-pilot-20260613T170559Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260613T170559Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-price-policy-h1-discoverability-3x.md`
