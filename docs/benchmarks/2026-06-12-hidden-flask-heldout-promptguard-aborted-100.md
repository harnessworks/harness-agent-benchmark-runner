# Hidden Flask Heldout Prompt-Guard Aborted 100 - 2026-06-12

## Summary

This is the latest heldout diagnostic after the hidden-path, adapter-isolation,
target-clean, and `_band`/`_bands` API-style mitigations.

It should not be promoted to official product evidence. A prompt-guarded fresh
10-record pilot completed with zero promotion-abnormal signals, but the
follow-up 100-record run stopped at record 14 when the 330-second pilot
watchdog fired on bare `hidden-effect-bundle-quote`.

The aborted 100-run is useful infrastructure evidence:

- `CODEX_PROMPT_GUARD=1` cleared the repeated workflow-only availability stall
  in the fresh 10-record pilot.
- The `_band`/`_bands` gate fix cleared the `catalog-segments` wrong-file
  pressure.
- The 330-second watchdog is too strict for a 100-record promotion gate when it
  is implemented as a wall-clock cap rather than an idle-output watchdog.

Do not start or report a full 100-record heldout evidence run from this state
until the 100-run timeout policy is changed.

## Run Configuration

- Suite: `benchmarks/suites/flask-hidden-heldout-10.json`
- Planned heldout shape: 5 tasks x 2 arms
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
- Pilot watchdog: `--agent-stall-timeout 330`

## Availability Paired Triage

- Workspace: `runs/hidden-flask-availability-paired-stall-triage-20260612T144833Z`
- Results: `results/hidden-flask-availability-paired-stall-triage-20260612T144833Z`
- Shape: `availability-badge` only, both arms, `repeats=3`
- Completed records: 6/6
- Hidden access: 0
- Stalls/timeouts: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0

| Target | Runs | Functional | Schema contract | Workflow | Boundary | Stalls | Timeouts | Wrong-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 3 | 0 | 0 | 3 | 3 | 0 | 0 | 0 | 57s | 83s |
| `workflow-only` | 3 | 0 | 1 | 3 | 3 | 0 | 0 | 0 | 68s | 74s |

This weakened the hypothesis that `workflow-only availability-badge` always
stalls after a bare record. The stall is intermittent.

## Prompt-Guard Fresh 10

- Workspace: `runs/hidden-flask-heldout-10-promptguard-20260612T145720Z`
- Results: `results/hidden-flask-heldout-10-promptguard-20260612T145720Z`
- Command: `CODEX_PROMPT_GUARD=1 CODEX_MODEL=gpt-5.5 CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority' python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/flask-hidden-heldout-10.json --task-limit 5 --repeats 1 --agent-stall-timeout 330 --stop-on-abnormal --workspace runs/hidden-flask-heldout-10-promptguard-20260612T145720Z --results results/hidden-flask-heldout-10-promptguard-20260612T145720Z --execute`
- Completed records: 10/10
- Hidden access: 0
- Stalls/timeouts: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Excluded-path conflicts: 0

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 5 | 0 | 0 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 71s | 90s |
| `workflow-only` | 5 | 0 | 1 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 81s | 149s |

This was clean enough to attempt a 100-record promotion run under the same
mitigation, but it is still only a pilot. Strict successes remain 0 because the
heldout prompts are partial-realistic and the hidden functional/schema contract
is intentionally not fully supplied.

## Prompt-Guard 100 Attempt

- Workspace: `runs/hidden-flask-heldout-100-promptguard-20260612T151246Z`
- Results: `results/hidden-flask-heldout-100-promptguard-20260612T151246Z`
- Command: `CODEX_PROMPT_GUARD=1 CODEX_MODEL=gpt-5.5 CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority' python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/flask-hidden-heldout-10.json --task-limit 5 --repeats 10 --agent-stall-timeout 330 --stop-on-abnormal --workspace runs/hidden-flask-heldout-100-promptguard-20260612T151246Z --results results/hidden-flask-heldout-100-promptguard-20260612T151246Z --execute`
- Planned records: 100
- Completed records before stop: 14
- Stop reason: record 14, `bare` `hidden-effect-bundle-quote`, stopped by the
  330-second pilot watchdog.

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 7 | 0 | 0 | 0 | 6 | 7 | 0 | 1 | 1 | 0 | 65s | 330s |
| `workflow-only` | 7 | 0 | 1 | 1 | 7 | 7 | 0 | 0 | 0 | 0 | 77s | 91s |

The stopped record had no hidden benchmark access, wrong-file edits,
forbidden-file edits, or excluded-path conflicts. Unlike the earlier
workflow-only availability stalls, this record had already edited
`app/__init__.py`, `app/catalog.py`, `tests/test_app.py`, and `docs/`.

Manual post-stop verification on that partial work showed local pytest passed,
but hidden functional/schema checks failed:

- Functional: missing expected field matching one of `item_count`.
- Schema: `bundle_quote.discount` was an object, not a decimal-compatible
  money value.

The stop is therefore not product success evidence, but it also should not be
treated as the same kind of no-edit deadlock seen earlier. It shows the current
330-second pilot watchdog is a wall-clock cutoff, not an idle-progress detector.

## Recommendation

Do not promote this aborted 100-run.

For the next heldout promotion attempt:

- Keep `CODEX_PROMPT_GUARD=1`; it is a generic benchmark-operation guard and
  was applied equally to both arms.
- Keep target ref `0f478ddede915b2f0cf41662373c53d8c70f3f86`.
- Keep hidden access scanning and stop-on-abnormal.
- Do not use `--agent-stall-timeout 330` as the 100-record promotion cutoff.
  Either omit the pilot watchdog for the 100-run and rely on the task timeout
  of 600 seconds, or use `--agent-idle-timeout` so no-output hangs are stopped
  without cutting off long-but-active runs.
- Continue reporting strict success, functional success, schema-contract
  success, workflow success, boundary success, stalls, and timeouts separately.
