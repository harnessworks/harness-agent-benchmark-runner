# Hidden Flask Heldout Idle-Watch Aborted 100 - 2026-06-13

## Summary

This is the latest heldout diagnostic after adding the agent idle-output
watchdog. It supersedes the earlier prompt-guard 100 attempt as the current
promotion-readiness evidence for the partial-realistic heldout suite.

A fresh 10-record pilot completed cleanly with `--agent-idle-timeout 300`. The
follow-up sequential 100-record attempt progressed past the previous record-14
wall-clock watchdog stop, then stopped at record 62 when workflow-only
`hidden-effect-availability-badge` hit the task timeout of 600 seconds.

This run should not be promoted to official product evidence. It is useful
diagnostic evidence:

- The idle watchdog avoided the earlier 330-second wall-clock false cutoff.
- The run reached 62/100 records with 0 hidden access, 0 wrong-file edits,
  0 forbidden-file edits, and 0 excluded-path conflicts.
- The stop was a real task timeout, not hidden leakage or a boundary failure.
- `--max-agent-timeout 900` did not raise the effective timeout because the task
  specs set `timeout_seconds` to 600; the runner caps task timeout, it does not
  extend it.

Strict successes remain 0 because these are partial-realistic prompts and the
hidden functional/schema contract is intentionally not fully supplied. The
main signal here is operational stability and boundary discipline, not product
lift.

## Run Configuration

- Suite: `benchmarks/suites/flask-hidden-heldout-10.json`
- Planned heldout shape: 5 tasks x 2 arms x 10 repeats
- Prompt variant: `partial-realistic`
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
- Task timeout: 600 seconds from the task specs

## Idle-Watch Fresh 10

- Workspace: `runs/hidden-flask-heldout-10-idlewatch-20260612T154619Z`
- Results: `results/hidden-flask-heldout-10-idlewatch-20260612T154619Z`
- Command: `CODEX_PROMPT_GUARD=1 CODEX_MODEL=gpt-5.5 CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority' python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/flask-hidden-heldout-10.json --task-limit 5 --repeats 1 --agent-idle-timeout 300 --stop-on-abnormal --workspace runs/hidden-flask-heldout-10-idlewatch-20260612T154619Z --results results/hidden-flask-heldout-10-idlewatch-20260612T154619Z --execute`
- Completed records: 10/10
- Hidden access: 0
- Stalls/timeouts: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Excluded-path conflicts: 0

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 5 | 0 | 0 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 59s | 94s |
| `workflow-only` | 5 | 0 | 1 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 64s | 72s |

This was clean enough to attempt the 100-record promotion run. It was not
clean enough to make a product-success claim because the strict/functional
contract remained intentionally hidden.

## Idle-Watch 100 Attempt

- Workspace: `runs/hidden-flask-heldout-100-idlewatch-20260612T160005Z`
- Results: `results/hidden-flask-heldout-100-idlewatch-20260612T160005Z`
- Command: `CODEX_PROMPT_GUARD=1 CODEX_MODEL=gpt-5.5 CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority' python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/flask-hidden-heldout-10.json --task-limit 5 --repeats 10 --agent-idle-timeout 300 --stop-on-abnormal --workspace runs/hidden-flask-heldout-100-idlewatch-20260612T160005Z --results results/hidden-flask-heldout-100-idlewatch-20260612T160005Z --execute`
- Planned records: 100
- Completed records before stop: 62
- Stop reason: record 62, `workflow-only` `hidden-effect-availability-badge`,
  `agent_timed_out=True`, `termination_reason=timeout`, duration 600 seconds
- Hidden access: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Excluded-path conflicts: 0

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 31 | 0 | 0 | 0 | 31 | 31 | 0 | 0 | 0 | 0 | 59s | 141s |
| `workflow-only` | 31 | 0 | 6 | 2 | 30 | 31 | 0 | 0 | 1 | 0 | 68s | 105s |

The run crossed the previous record-14 failure point. Long-but-active records
completed at 140.5 seconds and 173.2 seconds without being stopped by the idle
watchdog, which is the desired behavior for promotion runs.

## Stopped Record

- Run directory:
  `runs/hidden-flask-heldout-100-idlewatch-20260612T160005Z/20260612T172611Z-hidden-effect-availability-badge-f4c6e7f1`
- Arm: `workflow-only`
- Task: `hidden-effect-availability-badge`
- Effective limits:
  - `agent_idle_timeout_seconds`: 300
  - `agent_timeout_seconds`: 600
  - `agent_process_timeout_seconds`: 600
  - `max_agent_timeout_seconds`: 900
- Agent exit: 124
- Termination reason: `timeout`
- Boundary success: true
- Workflow success: false
- Functional success: false
- Schema contract success: false

The agent made active edits and the repository-local harness gate passed:

- `scripts/check_harness.py`: exit 0
- Local pytest inside the harness gate: 10 passed
- API style, docs drift, structure drift, failure memory, and benchmark task
  contract checks passed

The hidden checks failed after the timeout:

- Functional oracle: missing SKU needed `product_not_found`
- Schema oracle: availability badge response needed the generic `meta` object

The agent log also showed local command success before the final timeout. This
was not a no-edit deadlock and not a hidden-access event. It is best classified
as an agent process tail timeout after partial local completion.

## Interpretation

The mitigation worked for the specific problem it targeted: the earlier
330-second wall-clock cutoff was too strict, while the idle-output watchdog let
long active records continue. The new stop is a different failure mode: the
task's 600-second timeout still catches rare long-tail Codex executions.

This does not justify another immediate identical 100-run. The next run should
first decide which timeout policy is being measured:

- Keep 600 seconds when timeout stability is part of the product signal.
- Raise the heldout task `timeout_seconds` or create a promotion variant if the
  goal is to separate implementation quality from agent process tail latency.
- Keep `--agent-idle-timeout 300` in either case so no-output hangs are still
  caught without cutting off active records.

This diagnostic also reinforces the test-design conclusion: `workflow-only`
does not supply enough generalized memory to solve hidden functional/schema
contracts under partial-realistic prompts. The product-value experiment still
needs the fixed three-arm shape: `bare`, `workflow-only`, and `memory-harness`.

## Recommendation

Do not promote this aborted 100-run.

Before the next full heldout promotion attempt:

- Keep `CODEX_PROMPT_GUARD=1`, target-clean checks, hidden access scanning, and
  `--stop-on-abnormal`.
- Keep `--agent-idle-timeout 300`.
- Decide whether the 100-record promotion timeout should remain 600 seconds or
  whether task specs should explicitly move to 900 or 1200 seconds.
- Add the `memory-harness` arm before making a product-value claim.
- Continue reporting strict success, functional success, schema-contract
  success, workflow success, boundary success, stalls, and timeouts separately.
