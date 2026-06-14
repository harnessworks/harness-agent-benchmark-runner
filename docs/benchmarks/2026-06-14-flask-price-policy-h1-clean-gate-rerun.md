# Flask Price-Policy H1 Clean Gate Rerun - 2026-06-14

This was the diagnostic rerun of the focused pre-100-run H1 price-policy clean
gate after adding first-class watchdog diagnostics to the runner. It excluded
the `bare` arm and used `--stop-on-abnormal`, matching the prior aborted gate.

The gate completed all 12 planned records with no operational abnormal events.

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
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Codex model/config: `gpt-5.5`,
  `model_reasoning_effort=medium`, `service_tier=priority`
- Runner ref at run start:
  `3e94074cf08406d71d4c4d27fd2566fbb927a35f`
- Started: `2026-06-14T02:38:36Z`
- Finished: `2026-06-14T03:05:25Z`

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

| Arm | Completed | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | Max duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `workflow-only` | 3 | 0 | 3 | 3 | 3 | 3 | 0/3 | 0 | 0 | 0 | 0 | 59.0s | 66.6s |
| `decision-only` | 3 | 3 | 3 | 3 | 3 | 3 | 3/3 | 0 | 0 | 0 | 0 | 227.4s | 360.9s |
| `failure-only` | 3 | 0 | 3 | 3 | 3 | 3 | 0/3 | 0 | 0 | 0 | 0 | 56.5s | 58.1s |
| `full-harness` | 3 | 3 | 3 | 3 | 3 | 3 | 3/3 | 0 | 0 | 0 | 0 | 50.4s | 61.2s |

Overall:

- Completed records: 12/12
- Strict successes: 6/12
- Record consistency: 6/12
- Functional/schema/workflow successes: 12/12 for each dimension
- Stalls/timeouts: 0
- Hidden-access audit: not separately configured for this focused gate;
  forbidden benchmark and decision paths stayed clean
- Preflight failures: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Expected non-zero runner exits: 6, from benchmark failures in the two
  non-decision arms

## Watchdog Diagnostics

All 12 records include the new `agent.watchdog` diagnostics because idle and
no-edit watchdogs were enabled.

- `observed_repo_changes=true`: 12/12
- `observed_repo_changes=false`: 0/12
- `agent_stalled=true`: 0/12
| Arm | Median seconds until repo change | Max seconds until repo change |
| --- | ---: | ---: |
| `workflow-only` | 34.1s | 42.1s |
| `decision-only` | 39.1s | 159.3s |
| `failure-only` | 40.1s | 43.1s |
| `full-harness` | 27.1s | 35.1s |

This distinguishes the rerun from the prior aborted gate. The earlier
abnormal record announced edits but did not create visible repository changes
within 360 seconds. In this rerun, every record produced visible repository
changes before the no-edit cutoff.

## H1 Reading

The narrow H1 signal reproduced cleanly:

- `decision-only`: 3/3 strict and record-consistent.
- `full-harness`: 3/3 strict and record-consistent.
- `workflow-only`: 0/3 record consistency because no price-band decision
  record exists.
- `failure-only`: 0/3 record consistency because no price-band decision record
  exists.

This is stronger than the prior aborted gate because the schedule completed
and the same separation held across all three repeats. It is still scoped to a
single H1 task, so it should not be read as broad cross-task harness proof.

## Decision

Do not jump directly to a 100-record promotion yet.

The clean gate now clears operationally for this focused H1 task, and the H1
effect is consistent. However, the evidence is still one task and one clean
rerun after a prior abnormal stop. The decision-only arm also retained a long
duration tail, with one record taking 360.9 seconds. The next higher-value
step is a second small stability check or a broadened pilot before spending
100 records.

Recommended next step:

- Run a broader, still-small H1 stability pilot before promotion. A practical
  next shape is 24 records: the same four arms, three repeats, across two H1
  tasks or two target refs if a second H1 task is not ready.
- Keep `--jobs 1`, `--stop-on-abnormal`, `--agent-idle-timeout 300`, and
  `--agent-no-edit-timeout 360`.
- Promote only if stalls/timeouts, hidden access, wrong-file edits, and
  forbidden-file edits stay at zero and the H1 separation remains clear.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T023836Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T023836Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-price-policy-h1-clean-gate-rerun.md`
