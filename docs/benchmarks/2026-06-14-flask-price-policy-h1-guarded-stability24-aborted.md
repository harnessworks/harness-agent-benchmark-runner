# Flask Price-Policy H1 Guarded Stability 24 Aborted - 2026-06-14

This was the guarded 24-record H1 stability expansion after the guarded
four-arm clean gate completed 12/12. It kept `CODEX_PROMPT_GUARD=1`, required
the prior guarded clean gate as readiness evidence, and increased repeats from
3 to 6.

The run did not clear promotion readiness. It stopped after 4 of 24 planned
records because the first `full-harness` record hit the no-edit watchdog.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Task: `hidden-effect-catalog-price-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `workflow-only`, `decision-only`, `failure-only`, `full-harness`
- Repeats: 6
- Planned records: 24
- Completed records before stop: 4
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Prior clean readiness:
  `results/hidden-flask-ab-pilot-20260614T033056Z`
- Minimum prior clean rounds: 3 per selected task/arm pair
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Codex model/config: `gpt-5.5`,
  `model_reasoning_effort=medium`, `service_tier=priority`
- Runner ref at run start:
  `8e715327f8494cb117c2e1a64ab1018f75c00f3a`
- Started: `2026-06-14T03:58:36Z`
- Finished: `2026-06-14T04:10:54Z`

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-price-policy \
  --arms workflow-only,decision-only,failure-only,full-harness \
  --repeats 6 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 360 \
  --require-clean-results results/hidden-flask-ab-pilot-20260614T033056Z \
  --min-clean-rounds 3 \
  --stop-on-abnormal \
  --execute
```

## Headline

| Arm | Completed | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | Max duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `workflow-only` | 1 | 0 | 1 | 1 | 1 | 1 | 0/1 | 0 | 0 | 0 | 0 | 58.5s |
| `decision-only` | 1 | 1 | 1 | 1 | 1 | 1 | 1/1 | 0 | 0 | 0 | 0 | 47.3s |
| `failure-only` | 1 | 0 | 1 | 1 | 1 | 1 | 0/1 | 0 | 0 | 0 | 0 | 57.2s |
| `full-harness` | 1 | 0 | 0 | 0 | 0 | 1 | 0/1 | 1 | 1 | 0 | 0 | 360.0s |

Overall before stop:

- Completed records: 4/24
- Strict successes: 1/4
- Record consistency: 1/4
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
  `20260614T040347Z-hidden-effect-catalog-price-policy-cd00326d`
- Arm: `full-harness`
- Duration: 360.040s
- `agent_stalled=true`
- `agent_timed_out=true`
- `termination_reason=no_edit_watchdog`
- `wrong_file_edits=0`
- `forbidden_file_edits=0`
- Changed files: none

The watchdog diagnostics show the same shape as the earlier unguarded
decision-arm stall:

```json
{
  "idle_timeout_seconds": 300,
  "last_no_edit_check_seconds": 360.002,
  "no_edit_checks": 361,
  "no_edit_timeout_seconds": 360,
  "observed_repo_changes": false,
  "seconds_since_last_output": 83.269,
  "seconds_without_observed_repo_changes": 360.04
}
```

The agent read the app, tests, domain docs, coding guidance, and the accepted
catalog price-band decision record. It then announced it would add a reusable
catalog helper, route, envelope, and tests, but made no visible repository
changes before the no-edit watchdog fired.

No-edit triage command:

```bash
python3 scripts/triage_no_edit_stalls.py \
  --results results/hidden-flask-ab-pilot-20260614T035836Z
```

Triage output classified the stopped record as `post-planning`: the last Codex
message was an implementation plan, the no-edit duration was 360.0s, and the
last-output gap was 83.3s. This supports treating the stop as a pre-edit
execution stall rather than a task-understanding failure.

## Reading

The prompt guard is useful but not sufficient promotion evidence.

What held:

- `decision-only` completed 1/1 strict and record-consistent before the stop.
- `workflow-only` and `failure-only` remained record-consistency controls.
- No wrong-file or forbidden-file edits occurred.

What failed:

- The guarded 24-record expansion reproduced the no-edit stall pattern in
  `full-harness` after only 4 records.
- The failure happened after the agent had already found the relevant decision
  record and stated the correct implementation direction.

This means the blocker is no longer isolated to the `decision-only` arm or to
unguarded prompts. It is an intermittent Codex execution stall after planning
and before the first repository edit.

## Decision

Do not run a 100-record H1 promotion.

Do not treat `CODEX_PROMPT_GUARD=1` as a complete fix. It made a two-record
`decision-only` diagnostic and a 12-record guarded clean gate look better, but
the guarded 24-record expansion still failed operationally.

Next useful work:

- Diagnose the post-planning, pre-edit stall pattern directly.
- Consider adapter-level progress controls that force a first edit or fail
  faster, without hiding true no-edit stalls.
- Keep no-edit watchdog counts separate from H1 correctness rates.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T035836Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T035836Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-price-policy-h1-guarded-stability24-aborted.md`
