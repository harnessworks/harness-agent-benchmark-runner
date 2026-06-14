# Flask Price-Policy H1 Clean Gate Aborted - 2026-06-14

This was a focused pre-100-run clean gate for the H1 price-policy task. It
excluded the `bare` arm so expected negative-control boundary behavior would
not stop the gate, and it used `--stop-on-abnormal` so the first operational
abnormal would halt the schedule.

The gate did not pass. It stopped after 8 of 12 planned records because the
`workflow-only` second-round record hit the no-edit watchdog.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Task: `hidden-effect-catalog-price-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `workflow-only`, `decision-only`, `failure-only`, `full-harness`
- Repeats: 3
- Planned records: 12
- Completed records before stop: 8
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Codex model/config: `gpt-5.5`,
  `model_reasoning_effort=medium`, `service_tier=priority`
- Runner ref at run start:
  `e98c8299ee6e2e85eced61fe2cc3a3d5fc8fb6dd`
- Started: `2026-06-14T02:13:27Z`
- Finished: `2026-06-14T02:30:28Z`

Command:

```bash
python3 scripts/run_hidden_flask_ab.py \
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

| Arm | Completed | Strict | Functional | Schema | Workflow | Boundary | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | Max duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `workflow-only` | 2 | 0 | 1 | 1 | 1 | 2 | 0/2 | 1 | 1 | 0 | 0 | 208s | 360s |
| `decision-only` | 2 | 2 | 2 | 2 | 2 | 2 | 2/2 | 0 | 0 | 0 | 0 | 60s | 67s |
| `failure-only` | 2 | 0 | 2 | 2 | 2 | 2 | 0/2 | 0 | 0 | 0 | 0 | 65s | 69s |
| `full-harness` | 2 | 2 | 2 | 2 | 2 | 2 | 2/2 | 0 | 0 | 0 | 0 | 56s | 58s |

Overall before stop:

- Completed records: 8/12
- Strict successes: 4/8
- Record consistency: 4/8
- Stalls/timeouts: 1
- Hidden-access findings: 0
- Preflight failures: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0

## Stop Reason

The scheduler stopped after:

```text
Stopping schedule after abnormal signal:
- agent no-edit watchdog fired
```

The stopped record was:

- Run ID:
  `20260614T022415Z-hidden-effect-catalog-price-policy-88dc806a`
- Arm: `workflow-only`
- Duration: 360.044s
- `agent_stalled=true`
- `agent_timed_out=true`
- `wrong_file_edits=0`
- `forbidden_file_edits=0`

The agent log tail showed that the agent announced it was editing
`app/catalog.py`, `app/__init__.py`, `tests/test_app.py`, and
`docs/domain/glossary.md`, but the no-edit watchdog fired after 360 seconds
without repository changes.

## H1 Reading

The H1 behavior itself remained strong in the records completed before the
abnormal stop:

- `decision-only`: 2/2 strict and record-consistent.
- `full-harness`: 2/2 strict and record-consistent.
- `workflow-only`: 0/2 record consistency because no price-band decision
  record exists.
- `failure-only`: 0/2 record consistency because no price-band decision record
  exists.

This preserves the narrow H1 discoverability signal, but it does not clear the
operational gate required before a 100-run evidence push.

## Decision

Do not run the 100-record promotion yet.

This gate was designed to answer whether a smaller non-bare H1 run can proceed
without operational abnormal events. It did not. A 100-run now would likely
measure timeout/no-edit noise alongside the memory effect.

Next useful work:

- Investigate why the Codex run can announce edits but make no repository
  changes for 360 seconds.
- Consider a shorter no-edit watchdog or adapter-level heartbeat only if it
  improves diagnosis without hiding real stalls.
- Rerun this same 12-record clean gate before moving to any larger run.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T021326Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T021326Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-price-policy-h1-clean-gate-aborted.md`
