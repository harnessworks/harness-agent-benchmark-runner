# Hidden Flask Stable-8 2-Round Pilot Aborted - 2026-06-13

## Summary

This is the latest stable-8 promotion-readiness diagnostic after adding the
runner promotion guard:

- `--promotion-run`
- `--require-clean-results`
- `--min-clean-rounds`

The stronger 2-round reduced pilot stopped at record 12 of 16 when `bare`
`hidden-effect-cart-validation` hit the idle-output watchdog after 314.5
seconds. Because the pilot had an abnormal signal, the guarded 96-record
promotion was not run. A dry-run readiness check with the failed pilot results
correctly failed before execution.

This run should not be promoted to official product evidence. It shows that
the no-edit idle tail is not isolated to `workflow-only`; it can also appear on
the bare target under the partial-realistic heldout prompt. The runner guard is
working as intended: it prevents using an abnormal pilot as near-100 promotion
evidence.

## Run Configuration

- Suite: `benchmarks/suites/flask-hidden-heldout-stable-8.json`
- Quarantined suite:
  `benchmarks/suites/flask-hidden-heldout-bundlequote-quarantine.json`
- Planned pilot shape: 4 tasks x 2 arms x 2 repeats = 16 records
- Prompt variant: `partial-realistic`
- Agent: Codex CLI, `gpt-5.5`
- Codex args: `-c model_reasoning_effort=medium -c service_tier=priority`
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Scheduler: sequential, `jobs=1`
- Stop rule: `--stop-on-abnormal`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent timeout override: `--agent-timeout-override 900`
- Max agent timeout cap: `--max-agent-timeout 900`

## Stable-8 2-Round Pilot

- Workspace:
  `runs/hidden-flask-heldout-stable8-2round-pilot-finalmitigation-20260612T1941Z`
- Results:
  `results/hidden-flask-heldout-stable8-2round-pilot-finalmitigation-20260612T1941Z`
- Command: `CODEX_PROMPT_GUARD=1 CODEX_MODEL=gpt-5.5 CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority' python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/flask-hidden-heldout-stable-8.json --mode pilot --repeats 2 --agent-timeout-override 900 --agent-idle-timeout 300 --stop-on-abnormal --workspace runs/hidden-flask-heldout-stable8-2round-pilot-finalmitigation-20260612T1941Z --results results/hidden-flask-heldout-stable8-2round-pilot-finalmitigation-20260612T1941Z --execute`
- Planned records: 16
- Completed records before stop: 12
- Stop reason: record 12, `bare` `hidden-effect-cart-validation`,
  `termination_reason=idle_watchdog`, duration 314.5 seconds
- Hidden access: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Excluded-path conflicts: 0

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 6 | 0 | 0 | 0 | 5 | 6 | 0 | 1 | 1 | 0 | 64s | 314s |
| `workflow-only` | 6 | 0 | 1 | 0 | 6 | 6 | 0 | 0 | 0 | 0 | 69s | 652s |

The first 11 records completed without abnormal signals. Record 6 was a long
but clean `workflow-only` `hidden-effect-catalog-metrics` record at 651.6
seconds. Record 12 stopped on the idle watchdog.

## Stopped Record

- Run directory:
  `runs/hidden-flask-heldout-stable8-2round-pilot-finalmitigation-20260612T1941Z/20260612T200514Z-hidden-effect-cart-validation-21f1db43`
- Arm: `bare`
- Task: `hidden-effect-cart-validation`
- Effective limits:
  - `agent_timeout_override_seconds`: 900
  - `agent_timeout_seconds`: 900
  - `agent_process_timeout_seconds`: 900
  - `agent_idle_timeout_seconds`: 300
  - `max_agent_timeout_seconds`: 900
- Agent exit: 124
- Termination reason: `idle_watchdog`
- Agent duration: 314.5 seconds
- Changed files: none
- Boundary success: true
- Workflow success: false
- Functional success: false
- Schema contract success: false

The hidden checks failed because the endpoint was absent:

- Functional oracle: expected `POST /cart/validate` status 200, got 404
- Schema oracle: expected `POST /cart/validate` status 200, got 404

The agent log tail showed the agent reading `app/__init__.py`,
`app/catalog.py`, `tests/test_app.py`, and `README.md`, then the runner stopped
it after 300 seconds without output. Hidden access scanning found no matches.

## Promotion Guard Check

The near-100 command was checked with the new promotion guard:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-heldout-stable-8.json \
  --repeats 12 \
  --promotion-run \
  --require-clean-results results/hidden-flask-heldout-stable8-2round-pilot-finalmitigation-20260612T1941Z \
  --min-clean-rounds 2 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --stop-on-abnormal
```

It failed before execution because the prior pilot contained an abnormal
signal:

```text
clean readiness results contain abnormal signals:
20260612T200514Z-hidden-effect-cart-validation-21f1db43: agent idle watchdog fired
```

This is the desired behavior. The guard prevented a 96-record promotion from
starting with insufficient readiness evidence.

## Interpretation

The previous stable-8 96 attempt showed a workflow-only no-edit idle stall. The
focused workflow-only cart-validation triage did not reproduce that stall. This
2-round pilot now shows a bare no-edit idle stall on the same task, while also
showing a long-but-clean workflow-only catalog-metrics tail.

The defensible reading is:

- `bundle-quote` should remain quarantined.
- `cart-validation` should not be quarantined solely as a workflow-only task
  problem.
- The current partial-realistic stable-8 suite still has intermittent no-edit
  idle tails across arms.
- A one-repeat or two-repeat pilot is not sufficient promotion evidence when
  the objective is near-100 stability.

## Recommendation

Do not run the 96-record stable-8 promotion yet.

Before another near-100 attempt:

- Keep the new `--promotion-run` guard mandatory.
- Reduce no-edit idle tails before promotion, especially around cart-validation
  exploration and generic harness/style inspection.
- Consider a pre-promotion stability shape that is longer than two rounds but
  cheaper than 96 records.
- Keep `bundle-quote` quarantined.
- Keep reporting strict success separately from functional, schema, workflow,
  boundary, timeout, and stall dimensions.
- Add the `memory-harness` arm before making a product-value claim.
