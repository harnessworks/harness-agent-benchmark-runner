# Hidden Flask Stable-8 Final-Mitigation Aborted 96 - 2026-06-13

## Summary

This is the latest reduced heldout diagnostic after quarantining
`hidden-effect-bundle-quote` into
`benchmarks/suites/flask-hidden-heldout-bundlequote-quarantine.json`.

The reduced suite, `benchmarks/suites/flask-hidden-heldout-stable-8.json`,
completed an 8-record final-mitigation pilot cleanly. The follow-up balanced
96-record promotion attempt then stopped at record 11 when workflow-only
`hidden-effect-cart-validation` hit the idle-output watchdog after 500.8
seconds.

This run should not be promoted to official product evidence. It is useful
diagnostic evidence:

- The `bundle-quote` quarantine reduced the original promotion blocker but did
  not eliminate workflow-only no-edit idle stalls.
- The stopped record had no hidden access, wrong-file edits, forbidden-file
  edits, or excluded-path conflicts.
- The stopped record made no file edits, passed the local harness gate because
  the repository remained unchanged, and failed hidden functional/schema checks
  because `/cart/validate` was absent.
- The 8-record pilot was not strong enough to predict 96-record stability.

The current blocker is therefore broader than `bundle-quote` tail latency:
workflow-only can still spend several minutes inspecting generic harness checks
and then idle out without making changes.

## Run Configuration

- Reduced suite: `benchmarks/suites/flask-hidden-heldout-stable-8.json`
- Quarantined suite:
  `benchmarks/suites/flask-hidden-heldout-bundlequote-quarantine.json`
- Prompt variant: `partial-realistic`
- Arms: legacy `no-harness` and `yes-harness`
  - `no-harness` maps to `bare`
  - clean `yes-harness` maps to `workflow-only`
- Agent: Codex CLI, `gpt-5.5`
- Codex args: `-c model_reasoning_effort=medium -c service_tier=priority`
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Adapter isolation: `--ignore-user-config --ignore-rules --disable plugins`
- Target workflow ref: `flask-yes-harness` @
  `0f478ddede915b2f0cf41662373c53d8c70f3f86`
- Bare target ref: `flask-no-harness` @
  `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- Scheduler: sequential, `jobs=1`
- Stop rule: `--stop-on-abnormal`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent timeout override: `--agent-timeout-override 900`
- Max agent timeout cap: `--max-agent-timeout 900`

## Stable-8 Pilot

- Workspace:
  `runs/hidden-flask-heldout-stable8-pilot-finalmitigation-20260612T1848Z`
- Results:
  `results/hidden-flask-heldout-stable8-pilot-finalmitigation-20260612T1848Z`
- Command: `CODEX_PROMPT_GUARD=1 CODEX_MODEL=gpt-5.5 CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority' python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/flask-hidden-heldout-stable-8.json --repeats 1 --agent-timeout-override 900 --agent-idle-timeout 300 --stop-on-abnormal --workspace runs/hidden-flask-heldout-stable8-pilot-finalmitigation-20260612T1848Z --results results/hidden-flask-heldout-stable8-pilot-finalmitigation-20260612T1848Z --execute`
- Completed records: 8/8
- Hidden access: 0
- Stalls/timeouts: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Excluded-path conflicts: 0

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 4 | 0 | 0 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 64s | 259s |
| `workflow-only` | 4 | 0 | 1 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 63s | 87s |

The pilot was clean enough to attempt a balanced 96-record promotion over the
same reduced suite. It was not product-success evidence because strict
successes remained 0 under the intentionally partial prompt.

## Stable-8 96 Attempt

- Workspace:
  `runs/hidden-flask-heldout-stable8-promotion96-finalmitigation-20260612T1902Z`
- Results:
  `results/hidden-flask-heldout-stable8-promotion96-finalmitigation-20260612T1902Z`
- Command: `CODEX_PROMPT_GUARD=1 CODEX_MODEL=gpt-5.5 CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority' python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/flask-hidden-heldout-stable-8.json --repeats 12 --agent-timeout-override 900 --agent-idle-timeout 300 --stop-on-abnormal --workspace runs/hidden-flask-heldout-stable8-promotion96-finalmitigation-20260612T1902Z --results results/hidden-flask-heldout-stable8-promotion96-finalmitigation-20260612T1902Z --execute`
- Planned records: 96
- Completed records before stop: 11
- Stop reason: record 11, `workflow-only` `hidden-effect-cart-validation`,
  `termination_reason=idle_watchdog`, duration 500.8 seconds
- Hidden access: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Excluded-path conflicts: 0

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 5 | 0 | 0 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 59s | 84s |
| `workflow-only` | 6 | 0 | 0 | 0 | 5 | 6 | 0 | 1 | 1 | 0 | 60s | 501s |

The first 10 records completed without abnormal signals. Record 11 was a
workflow-only idle-watchdog stop.

## Stopped Record

- Run directory:
  `runs/hidden-flask-heldout-stable8-promotion96-finalmitigation-20260612T1902Z/20260612T191844Z-hidden-effect-cart-validation-cceac3a4`
- Arm: `workflow-only`
- Task: `hidden-effect-cart-validation`
- Effective limits:
  - `agent_timeout_override_seconds`: 900
  - `agent_timeout_seconds`: 900
  - `agent_process_timeout_seconds`: 900
  - `agent_idle_timeout_seconds`: 300
  - `max_agent_timeout_seconds`: 900
- Agent exit: 124
- Termination reason: `idle_watchdog`
- Agent duration: 500.8 seconds
- Changed files: none
- Boundary success: true
- Workflow success: false
- Functional success: false
- Schema contract success: false

The local harness gate passed because the agent made no changes:

- `scripts/check_harness.py`: exit 0
- Local pytest inside the harness gate: 7 passed
- Flask route table, API style, docs drift, structure drift, failure memory,
  and benchmark task contract checks passed

The hidden checks failed because the endpoint was absent:

- Functional oracle: expected `POST /cart/validate` status 200, got 404
- Schema oracle: expected `POST /cart/validate` status 200, got 404

The agent log tail showed generic harness/test inspection, including
`scripts/check_api_style.py` and `tests/test_api_style_gate.py`, then the runner
stopped it after 300 seconds without output. Hidden access scanning found no
matches.

## Interpretation

The reduced suite answered the immediate `bundle-quote` question:

- `bundle-quote` is tail-heavy and should stay quarantined.
- Removing it is not sufficient for a promotion run.
- Workflow-only still has no-edit idle stalls on partial-realistic heldout
  work.

This means another identical 96-record reduced promotion is not the next best
step. A larger pilot is unlikely to be enough by itself because the 8-record
pilot was clean and the promotion still stalled by record 11.

This remains consistent with the product-test conclusion: `workflow-only` gives
local gate and boundary discipline but does not provide the generalized
implementation memory needed to solve hidden functional/schema contracts under
partial prompts. The product-value experiment still needs the fixed three-arm
shape: `bare`, `workflow-only`, and `memory-harness`.

## Recommendation

Do not promote this aborted 96-run and do not immediately repeat the same
reduced promotion shape.

Before the next full heldout promotion attempt:

- Keep `bundle-quote` in the quarantine suite.
- Add a focused workflow-only cart-validation idle-stall triage run, or reduce
  the workflow-only search burden before rerunning promotion.
- Treat a clean one-repeat pilot as insufficient promotion evidence; require at
  least a two-round reduced pilot or another stronger stability check before a
  near-100 run.
- Keep `CODEX_PROMPT_GUARD=1`, target-clean checks, hidden access scanning, and
  `--stop-on-abnormal`.
- Keep `--agent-idle-timeout 300` and `--agent-timeout-override 900`.
- Keep reporting idle-watchdog stops separately from task timeouts.
- Add the `memory-harness` arm before making a product-value claim.
