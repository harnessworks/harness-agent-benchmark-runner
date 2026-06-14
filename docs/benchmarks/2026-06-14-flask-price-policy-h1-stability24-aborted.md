# Flask Price-Policy H1 Stability 24 Aborted - 2026-06-14

This was the next H1 stability expansion after the 12-record clean gate rerun.
It kept the same four non-bare arms and increased repeats from 3 to 6, for 24
planned records. The run required the prior clean 12-record result as a
readiness gate before execution.

The run did not clear promotion readiness. It stopped after 2 of 24 planned
records because the first `decision-only` record hit the no-edit watchdog.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Task: `hidden-effect-catalog-price-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `workflow-only`, `decision-only`, `failure-only`, `full-harness`
- Repeats: 6
- Planned records: 24
- Completed records before stop: 2
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Prior clean readiness:
  `results/hidden-flask-ab-pilot-20260614T023836Z`
- Minimum prior clean rounds: 3 per selected task/arm pair
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Codex model/config: `gpt-5.5`,
  `model_reasoning_effort=medium`, `service_tier=priority`
- Runner ref at run start:
  `b13363523197a1411dcf7ebd0219a9388bfe295c`
- Started: `2026-06-14T03:10:03Z`
- Finished: `2026-06-14T03:17:32Z`

Command:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-price-policy \
  --arms workflow-only,decision-only,failure-only,full-harness \
  --repeats 6 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 360 \
  --require-clean-results results/hidden-flask-ab-pilot-20260614T023836Z \
  --min-clean-rounds 3 \
  --stop-on-abnormal \
  --execute
```

## Headline

| Arm | Completed | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | Max duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `workflow-only` | 1 | 0 | 1 | 1 | 1 | 1 | 0/1 | 0 | 0 | 0 | 0 | 65.6s |
| `decision-only` | 1 | 0 | 0 | 0 | 0 | 1 | 0/1 | 1 | 1 | 0 | 0 | 360.0s |
| `failure-only` | 0 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | n/a |
| `full-harness` | 0 | 0 | 0 | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | n/a |

Overall before stop:

- Completed records: 2/24
- Strict successes: 0/2
- Record consistency: 0/2
- Stalls/timeouts: 1
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
  `20260614T031122Z-hidden-effect-catalog-price-policy-1d803759`
- Arm: `decision-only`
- Duration: 360.035s
- `agent_stalled=true`
- `agent_timed_out=true`
- `termination_reason=no_edit_watchdog`
- `wrong_file_edits=0`
- `forbidden_file_edits=0`
- Changed files: none

The new watchdog diagnostics make the failure mode explicit:

```json
{
  "idle_timeout_seconds": 300,
  "last_no_edit_check_seconds": 360.0,
  "no_edit_checks": 361,
  "no_edit_timeout_seconds": 360,
  "observed_repo_changes": false,
  "seconds_since_last_output": 110.863,
  "seconds_without_observed_repo_changes": 360.035
}
```

The agent inspected the app, tests, catalog helper, domain glossary, coding
conventions, and the accepted catalog price-band decision record. It then made
no visible repository changes before the no-edit watchdog fired.

## Reading

This run invalidates a direct jump to 100 records. The prior 12-record clean
gate showed that the H1 task can complete cleanly and separate decision-bearing
arms from controls, but the first expanded stability check immediately
reproduced the operational risk in a decision-bearing arm.

The H1 correctness signal is still plausible, but promotion readiness is not:

- The 12-record clean gate had `decision-only` and `full-harness` at 3/3
  strict and record-consistent.
- This 24-record expansion stopped before testing the full matrix.
- The stopped `decision-only` record read the relevant decision record but did
  not edit the repository.

## Decision

Do not run a 100-record promotion yet.

Next useful work:

- Diagnose the Codex no-edit stall pattern in decision-bearing arms before
  spending more live benchmark budget.
- Keep the `agent.watchdog` fields in all future reports; they now distinguish
  no-change stalls from ordinary benchmark failures.
- Consider a narrow adapter or prompt-handoff investigation before another
  multi-record H1 expansion.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T031002Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T031002Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-price-policy-h1-stability24-aborted.md`
