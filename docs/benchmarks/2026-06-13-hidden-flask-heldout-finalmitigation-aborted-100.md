# Hidden Flask Heldout Final-Mitigation Aborted 100 - 2026-06-13

## Summary

This is the latest heldout diagnostic after adding both promotion mitigations:

- `--agent-idle-timeout 300`
- `--agent-timeout-override 900`

A fresh 10-record pilot completed cleanly. The follow-up 100-record sequential
attempt then stopped at record 4 when workflow-only
`hidden-effect-bundle-quote` hit the idle-output watchdog after 719.3 seconds.

This run should not be promoted to official product evidence. It is useful
diagnostic evidence:

- The timeout override was applied and recorded in result limits.
- The stopped record did not hit the 600-second task timeout; it ran past that
  limit because the effective process timeout was 900 seconds.
- The stopped record had no hidden access, wrong-file edits, forbidden-file
  edits, or excluded-path conflicts.
- The stopped record made no file edits, passed the local harness gate because
  the repository remained unchanged, and failed hidden functional/schema checks
  because `/catalog/bundle-quote` was absent.

The failure mode is therefore different from the previous 600-second task
timeout. It is an intermittent workflow-only no-edit idle stall on a held-out
task, not a timeout-cap artifact and not a boundary/leakage issue.

A follow-up focused bundle-quote triage then stopped on the first `bare`
bundle-quote record with a 900-second task timeout after active edits. That
means the current promotion blocker is not workflow-only-specific. Bundle-quote
itself has severe tail-latency risk under the partial-realistic prompt.

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
- Agent timeout override: `--agent-timeout-override 900`
- Max agent timeout cap: `--max-agent-timeout 900`

## Final-Mitigation Fresh 10

- Workspace: `runs/hidden-flask-heldout-10-finalmitigation-20260612T174632Z`
- Results: `results/hidden-flask-heldout-10-finalmitigation-20260612T174632Z`
- Command: `CODEX_PROMPT_GUARD=1 CODEX_MODEL=gpt-5.5 CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority' python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/flask-hidden-heldout-10.json --task-limit 5 --repeats 1 --agent-timeout-override 900 --agent-idle-timeout 300 --stop-on-abnormal --workspace runs/hidden-flask-heldout-10-finalmitigation-20260612T174632Z --results results/hidden-flask-heldout-10-finalmitigation-20260612T174632Z --execute`
- Completed records: 10/10
- Hidden access: 0
- Stalls/timeouts: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Excluded-path conflicts: 0

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 5 | 0 | 0 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 58s | 82s |
| `workflow-only` | 5 | 0 | 1 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 63s | 80s |

This was clean enough to attempt the 100-record promotion run under the same
mitigation. It was not product-success evidence because strict successes
remained 0 under the intentionally partial prompt.

## Final-Mitigation 100 Attempt

- Workspace: `runs/hidden-flask-heldout-100-finalmitigation-20260612T180104Z`
- Results: `results/hidden-flask-heldout-100-finalmitigation-20260612T180104Z`
- Command: `CODEX_PROMPT_GUARD=1 CODEX_MODEL=gpt-5.5 CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority' python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/flask-hidden-heldout-10.json --task-limit 5 --repeats 10 --agent-timeout-override 900 --agent-idle-timeout 300 --stop-on-abnormal --workspace runs/hidden-flask-heldout-100-finalmitigation-20260612T180104Z --results results/hidden-flask-heldout-100-finalmitigation-20260612T180104Z --execute`
- Planned records: 100
- Completed records before stop: 4
- Stop reason: record 4, `workflow-only` `hidden-effect-bundle-quote`,
  `termination_reason=idle_watchdog`, duration 719.3 seconds
- Hidden access: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Excluded-path conflicts: 0

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 2 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 58s | 72s |
| `workflow-only` | 2 | 0 | 0 | 0 | 1 | 2 | 0 | 1 | 1 | 0 | 69s | 719s |

The first three records completed without abnormal signals:

- `bare` `hidden-effect-availability-badge`: 58.3s
- `workflow-only` `hidden-effect-availability-badge`: 68.5s
- `bare` `hidden-effect-bundle-quote`: 72.0s

The fourth record was an idle-watchdog stop, not a 900-second timeout.

## Stopped Record

- Run directory:
  `runs/hidden-flask-heldout-100-finalmitigation-20260612T180104Z/20260612T180444Z-hidden-effect-bundle-quote-c50b962a`
- Arm: `workflow-only`
- Task: `hidden-effect-bundle-quote`
- Effective limits:
  - `agent_timeout_override_seconds`: 900
  - `agent_timeout_seconds`: 900
  - `agent_process_timeout_seconds`: 900
  - `agent_idle_timeout_seconds`: 300
  - `max_agent_timeout_seconds`: 900
- Agent exit: 124
- Termination reason: `idle_watchdog`
- Changed files: none
- Boundary success: true
- Workflow success: false
- Functional success: false
- Schema contract success: false

The repository-local harness gate passed because the agent made no changes:

- `scripts/check_harness.py`: exit 0
- Local pytest inside the harness gate: 7 passed
- API style, docs drift, structure drift, failure memory, and benchmark task
  contract checks passed

The hidden checks failed because the endpoint was absent:

- Functional oracle: expected `POST /catalog/bundle-quote` status 200, got 404
- Schema oracle: expected `POST /catalog/bundle-quote` status 200, got 404

The agent log tail showed it was reading generic local harness files such as
`scripts/check_api_style.py` and `docs/domain/glossary.md`, then the runner
stopped it after 300 seconds without output. Hidden access scanning found no
matches.

## Bundle-Quote Focused Triage

- Workspace:
  `runs/hidden-flask-bundlequote-finalmitigation-triage-20260612T182328Z`
- Results:
  `results/hidden-flask-bundlequote-finalmitigation-triage-20260612T182328Z`
- Command: `CODEX_PROMPT_GUARD=1 CODEX_MODEL=gpt-5.5 CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority' python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/flask-hidden-heldout-10.json --task-id hidden-effect-bundle-quote --repeats 3 --agent-timeout-override 900 --agent-idle-timeout 300 --stop-on-abnormal --workspace runs/hidden-flask-bundlequote-finalmitigation-triage-20260612T182328Z --results results/hidden-flask-bundlequote-finalmitigation-triage-20260612T182328Z --execute`
- Planned records: 6
- Completed records before stop: 1
- Stop reason: record 1, `bare` `hidden-effect-bundle-quote`,
  `termination_reason=timeout`, duration 900.0 seconds
- Hidden access: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Excluded-path conflicts: 0

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 900s | 900s |

The stopped bare record edited `app/__init__.py`, `app/catalog.py`,
`tests/test_app.py`, and `docs/`, and local pytest passed before the timeout.
It still timed out before a clean agent exit. This focused triage weakens the
hypothesis that the final-mitigation 100-run stop was only a workflow-only
problem. The more defensible reading is that `hidden-effect-bundle-quote` is a
tail-heavy held-out task under partial-realistic prompts.

## Interpretation

The final mitigation split the prior timeout question correctly:

- A 900-second override prevented the previous 600-second task timeout from
  being the promotion cutoff.
- The idle watchdog still caught a no-output stall before the 900-second
  timeout.

That is operationally better than the prior wall-clock and task-timeout
attempts, but it also means another identical 100-record run is not the next
best step. After the focused bundle-quote triage, the promotion blocker should
be treated as bundle-quote tail latency across arms, with at least one
workflow-only idle stall and one bare 900-second task timeout observed.

This remains consistent with the product-test conclusion: `workflow-only` is
not enough to solve hidden functional/schema contracts under partial-realistic
prompts, and it may still spend excessive time exploring generic harness
conventions. The product-value experiment still needs the fixed three-arm
shape: `bare`, `workflow-only`, and `memory-harness`.

## Recommendation

Do not promote this aborted 100-run and do not immediately repeat the same
100-record shape.

Before the next full heldout promotion attempt:

- Keep `CODEX_PROMPT_GUARD=1`, target-clean checks, hidden access scanning, and
  `--stop-on-abnormal`.
- Keep `--agent-idle-timeout 300` and `--agent-timeout-override 900`.
- Do not run another 100-record promotion until bundle-quote tail behavior is
  either reduced or explicitly separated from product-value scoring.
- Keep reporting idle-watchdog stops separately from task timeouts.
- Add the `memory-harness` arm before making a product-value claim.
