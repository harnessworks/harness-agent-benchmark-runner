# Flask Price-Policy H1 Guarded Clean Gate - 2026-06-14

This was the guarded four-arm H1 clean gate after a two-record
`decision-only` diagnostic suggested `CODEX_PROMPT_GUARD=1` could mitigate
the no-edit stall pattern. It used the same non-bare H1 arms as the prior
clean gates and kept `--stop-on-abnormal` enabled.

The guarded gate completed all 12 planned records with no operational
abnormal events.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Task: `hidden-effect-catalog-price-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `workflow-only`, `decision-only`, `failure-only`, `full-harness`
- Repeats: 3
- Planned records: 12
- Completed records: 12
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Codex model/config: `gpt-5.5`,
  `model_reasoning_effort=medium`, `service_tier=priority`
- Runner ref at run start:
  `470b5117e03d7576f58d0027a4a1845e323adca9`
- Started: `2026-06-14T03:30:56Z`
- Finished: `2026-06-14T03:55:13Z`

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-price-policy \
  --arms workflow-only,decision-only,failure-only,full-harness \
  --repeats 3 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 360 \
  --stop-on-abnormal \
  --execute
```

## Headline

| Arm | Completed | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | Max duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `workflow-only` | 3 | 0 | 3 | 3 | 3 | 3 | 0/3 | 0 | 0 | 0 | 0 | 62.1s | 352.9s |
| `decision-only` | 3 | 3 | 3 | 3 | 3 | 3 | 3/3 | 0 | 0 | 0 | 0 | 57.1s | 60.1s |
| `failure-only` | 3 | 0 | 3 | 3 | 3 | 3 | 0/3 | 0 | 0 | 0 | 0 | 59.8s | 61.8s |
| `full-harness` | 3 | 3 | 3 | 3 | 3 | 3 | 3/3 | 0 | 0 | 0 | 0 | 48.0s | 59.0s |

Overall:

- Completed records: 12/12
- Strict successes: 6/12
- Record consistency: 6/12
- Functional/schema/workflow successes: 12/12 for each dimension
- Stalls/timeouts: 0
- Preflight failures: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Expected non-zero runner exits: 6, from benchmark failures in the two
  non-decision arms

## Watchdog Diagnostics

All 12 records included `agent.watchdog` diagnostics.

| Arm | No-edit watchdogs | No observed repo changes | Median seconds until repo change | Max seconds until repo change |
| --- | ---: | ---: | ---: | ---: |
| `workflow-only` | 0 | 0 | 39.1s | 43.1s |
| `decision-only` | 0 | 0 | 39.1s | 39.1s |
| `failure-only` | 0 | 0 | 39.1s | 45.1s |
| `full-harness` | 0 | 0 | 26.0s | 33.1s |

The guarded gate avoided the no-edit failure mode that stopped the prior
24-record stability expansion. It did not eliminate all duration tail risk:
one `workflow-only` control record took 352.9 seconds despite producing
visible repository changes.

## H1 Reading

The guarded run preserved the intended H1 separation:

- `decision-only`: 3/3 strict and record-consistent.
- `full-harness`: 3/3 strict and record-consistent.
- `workflow-only`: 0/3 record consistency because no price-band decision
  record exists.
- `failure-only`: 0/3 record consistency because no price-band decision record
  exists.

This is stronger operational evidence for guarded H1 runs than the previous
two-record diagnostic. It remains scoped to one H1 task and should not be used
as broad decision-memory proof.

## Decision

Do not jump directly to a 100-record promotion yet.

The guarded four-arm gate passed, so `CODEX_PROMPT_GUARD=1` is a credible
promotion-style operating condition for the next H1 experiment. However, the
single 352.9-second `workflow-only` tail means the next step should still be a
small guarded stability expansion, not a 100-record run.

Recommended next step:

- Run a guarded 24-record H1 stability expansion with the same four arms and
  six repeats.
- Keep `--jobs 1`, `--stop-on-abnormal`, `--agent-idle-timeout 300`, and
  `--agent-no-edit-timeout 360`.
- Promote only if stalls/timeouts, wrong-file edits, and forbidden-file edits
  remain at zero and the H1 separation remains clear.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T033056Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T033056Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-price-policy-h1-guarded-clean-gate.md`
