# Hidden Flask Heldout Memory-Hide Aborted Pilot - 2026-06-12

## Summary

This is a diagnostic report for the fresh 10-record heldout pilot after the
final mitigation pass. It is not representative product evidence and should not
be used as a 100-run launch signal.

The pilot was stopped early under the stated mid-run abnormal-signal rule:

- A first fresh attempt exposed real hidden-content leakage through the runner's
  temporary `_agent_excluded` directory.
- After fixing that runner leak, a targeted canary showed the hidden path was no
  longer visible.
- The next fresh 10-record pilot was stopped during record 3 because the bare
  `hidden-effect-bundle-quote` run exceeded 5 minutes without producing an
  agent result or agent log.
- After adding adapter isolation for Codex plugins and execpolicy `.rules`, a
  narrow canary completed without a stall, but the fresh 10-record pilot was
  stopped during record 4 because the workflow-only agent attempted to enumerate
  hidden `benchmarks/oracles` and `benchmarks/tasks` paths.
- After updating the workflow target ref to remove hidden-path guidance, the
  workflow-only canary completed with zero hidden access. A fresh 10-record
  pilot then reached record 7 before stopping on a bare `catalog-metrics` stall.
- A narrow recheck of that exact bare `catalog-metrics` task completed without
  a stall, but the next fresh 10-record rerun stopped at record 2 on a
  workflow-only `availability-badge` stall.

Do not start the 100-record heldout run from this state.

## Leak Found Before Memory-Hide Fix

- Workspace: `runs/hidden-flask-heldout-10-finalmit-20260612T1222Z`
- Stop point: workflow-only `hidden-effect-bundle-quote`
- Stop reason: agent log read hidden benchmark files from
  `../_agent_excluded/benchmarks/...`

The runner had moved `agent_excluded_paths` under the run directory. That hid
`benchmarks/` from the target repository path, but it was still reachable by
parent-directory traversal. This was a real leakage path, not a scoring artifact.

The runner was updated so excluded files are snapshotted in memory and deleted
from the agent-visible repository. The original `.git` directory is now held in
a system temporary directory while the agent runs, and the agent sees only a
temporary baseline git history.

## Memory-Hide Canary

- Workspace: `runs/hidden-flask-bundle-workflow-memoryhide-canary-20260612T1232Z`
- Task: `hidden-effect-bundle-quote`
- Target arm: `workflow-only`
- Agent setup duration: 3.879 seconds
- Agent duration: 255.646 seconds
- Timeout: no
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Excluded-path conflicts: 0

The canary log had no `_agent_excluded`, `../_agent_excluded`, or direct hidden
benchmark path access. Remaining `benchmarks/tasks` and `benchmarks/oracles`
mentions were generic docs/check references, not access to hidden task content.

## Fresh Pilot After Memory-Hide

- Suite: `benchmarks/suites/flask-hidden-heldout-10.json`
- Planned shape: 5 tasks x 2 arms x 1 repeat = 10 records
- Completed records before stop: 2
- Interrupted record: record 3, `bare` `hidden-effect-bundle-quote`
- Workspace: `runs/hidden-flask-heldout-10-memoryhide-20260612T1237Z`
- Results: `results/hidden-flask-heldout-10-memoryhide-20260612T1237Z`
- Command: `python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/flask-hidden-heldout-10.json --task-limit 5 --repeats 1 --workspace runs/hidden-flask-heldout-10-memoryhide-20260612T1237Z --results results/hidden-flask-heldout-10-memoryhide-20260612T1237Z --execute`

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Timeouts | Wrong-file edits | Forbidden-file edits | Excluded-path conflicts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| `workflow-only` | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |

| Record | Target | Task | Agent duration | Result |
| --- | --- | --- | ---: | --- |
| `20260612T123451Z-hidden-effect-availability-badge-21961b8b` | `bare` | `hidden-effect-availability-badge` | 72.236s | Functional and schema hidden checks failed; workflow and boundary passed. |
| `20260612T123622Z-hidden-effect-availability-badge-0b35b6ea` | `workflow-only` | `hidden-effect-availability-badge` | 105.541s | Functional and schema hidden checks failed; workflow and boundary passed. |
| `20260612T123815Z-hidden-effect-bundle-quote-93c50214` | `bare` | `hidden-effect-bundle-quote` | stopped at about 5m30s wall time | No `result.json`; only agent setup completed. |

The completed two records had no preflight failures, no wrong-file edits, no
forbidden-file edits, no excluded-path conflicts, and no hidden path access in
agent logs. The interrupted third record had no `agent.log`; the only retained
log was `agent-setup-1.log`, which completed successfully in 3.810 seconds.

After termination, no matching `run_hidden_flask_ab.py`,
`harness_agent_benchmark_runner run`, `codex_exec_agent.py`, or `codex exec`
processes remained.

## Interpretation

The memory-hide runner fix closed the concrete parent-directory leakage found
in the first fresh attempt. However, the heldout pilot still did not satisfy the
promotion criteria because record 3 stalled before producing an agent result.

The two completed `availability-badge` records are behaviorally informative:
both targets implemented plausible nearby solutions, both passed their local
workflow/boundary checks, and both missed hidden functional/schema expectations.
That is consistent with the heldout suite being a partial-realistic product
experiment rather than a full-contract control.

The interrupted `bundle-quote` record should be treated as an execution
stability signal, not as a product-value score. Because it stopped before
result collection, it cannot be counted as a strict timeout or oracle failure in
the JSONL summary, but it is enough to block a 100-record run.

## Watchdog Implementation And Follow-Up

The runner and A/B script now record stalls instead of relying on manual
process termination:

- `harness_agent_benchmark_runner run` accepts `--agent-stall-timeout`.
- Result records include `limits.agent_stall_timeout_seconds`,
  `limits.agent_process_timeout_seconds`, `agent.termination_reason`, and
  `scoring.agent_stalled`.
- `scripts/run_hidden_flask_ab.py` accepts `--stop-on-abnormal`, which stops a
  sequential schedule after preflight failures, agent stalls, agent timeouts,
  wrong/forbidden edits, excluded-path conflicts, runner errors, or hidden
  benchmark access patterns in agent logs.

A narrow diagnostic was run after this implementation:

- Workspace: `runs/hidden-flask-bundle-bare-stallwatch-20260612T1252Z`
- Results: `results/hidden-flask-bundle-bare-stallwatch-20260612T1252Z`
- Task: `hidden-effect-bundle-quote`
- Target arm: `bare`
- Agent stall watchdog: 330 seconds
- Agent duration: 92.998 seconds
- Stall/timeout: no
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Excluded-path conflicts: 0
- Hidden benchmark access patterns: 0

The narrow diagnostic failed only hidden functional/schema checks:

- Functional: missing expected field matching one of `item_count`.
- Schema: `bundle_quote.metadata.discount_applied` was not decimal-compatible.

This confirms the earlier bare bundle stall was not reliably reproducible once
measured with the watchdog.

## Fresh Pilot With Stall Watchdog

- Suite: `benchmarks/suites/flask-hidden-heldout-10.json`
- Planned shape: 5 tasks x 2 arms x 1 repeat = 10 records
- Completed records before stop: 4
- Workspace: `runs/hidden-flask-heldout-10-stallwatch-20260612T1256Z`
- Results: `results/hidden-flask-heldout-10-stallwatch-20260612T1256Z`
- Command: `python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/flask-hidden-heldout-10.json --task-limit 5 --repeats 1 --agent-stall-timeout 330 --stop-on-abnormal --workspace runs/hidden-flask-heldout-10-stallwatch-20260612T1256Z --results results/hidden-flask-heldout-10-stallwatch-20260612T1256Z --execute`
- Stop reason: record 4, `workflow-only` `hidden-effect-bundle-quote`, stopped
  by the stall watchdog at 330.004 seconds.

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | Excluded-path conflicts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 2 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| `workflow-only` | 2 | 0 | 0 | 0 | 1 | 2 | 1 | 1 | 0 | 0 | 0 |

| Record | Target | Task | Agent duration | Stall | Hidden access | Result |
| --- | --- | --- | ---: | --- | --- | --- |
| `20260612T125617Z-hidden-effect-availability-badge-95097bd6` | `bare` | `hidden-effect-availability-badge` | 63.894s | no | no | Functional/schema failed; workflow and boundary passed. |
| `20260612T125759Z-hidden-effect-availability-badge-1c48ffc6` | `workflow-only` | `hidden-effect-availability-badge` | 102.828s | no | no | Functional/schema failed; workflow and boundary passed. |
| `20260612T125950Z-hidden-effect-bundle-quote-463a9588` | `bare` | `hidden-effect-bundle-quote` | 114.637s | no | no | Functional/schema failed; workflow and boundary passed. |
| `20260612T130151Z-hidden-effect-bundle-quote-d3c2d55a` | `workflow-only` | `hidden-effect-bundle-quote` | 330.004s | yes | no | No files changed; workflow failed because the agent was stopped by the watchdog. |

The stopped `workflow-only` record had no wrong-file edits, no forbidden-file
edits, no excluded-path conflicts, no git-history exploration, and no hidden
benchmark access pattern. The agent attempted broad local discovery, saw
`benchmarks` was absent, read app/tests/docs/harness files, and then stalled
before making edits. Codex startup logs still contained local plugin manifest
warnings despite the adapter's default `--ignore-user-config`.

Follow-up adapter mitigation: the Codex exec adapter now also defaults to
`CODEX_IGNORE_RULES=1` and `CODEX_DISABLE_PLUGINS=1`, which add
`--ignore-rules --disable plugins` to evidence-run commands. `--ignore-rules`
disables execpolicy `.rules` files, not repository `AGENTS.md`, so workflow-arm
guidance remains part of the measured target repository.

## Adapter-Isolation Canary

- Workspace: `runs/hidden-flask-bundle-workflow-adapteriso-canary-20260612T1315Z`
- Results: `results/hidden-flask-bundle-workflow-adapteriso-canary-20260612T1315Z`
- Task: `hidden-effect-bundle-quote`
- Target arm: `workflow-only`
- Agent stall watchdog: 330 seconds
- Agent duration: 141.895 seconds
- Stall/timeout: no
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Excluded-path conflicts: 0
- Hidden benchmark access patterns: 0
- Codex plugin manifest warnings: 0

The canary failed hidden functional/schema checks, which is expected evidence
under a partial-realistic heldout prompt rather than an infrastructure abnormal:

- Functional: missing expected field matching one of `item_count`.
- Schema: `$.bundle_quote.discount_applied` was not decimal-compatible.

## Fresh Pilot With Adapter Isolation

- Suite: `benchmarks/suites/flask-hidden-heldout-10.json`
- Planned shape: 5 tasks x 2 arms x 1 repeat = 10 records
- Completed records before stop: 4
- Workspace: `runs/hidden-flask-heldout-10-adapteriso-20260612T1319Z`
- Results: `results/hidden-flask-heldout-10-adapteriso-20260612T1319Z`
- Command: `python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/flask-hidden-heldout-10.json --task-limit 5 --repeats 1 --agent-stall-timeout 330 --stop-on-abnormal --workspace runs/hidden-flask-heldout-10-adapteriso-20260612T1319Z --results results/hidden-flask-heldout-10-adapteriso-20260612T1319Z --execute`
- Stop reason: record 4, `workflow-only` `hidden-effect-bundle-quote`, because
  the agent log contained a direct hidden benchmark access pattern.

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 2 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| `workflow-only` | 2 | 0 | 0 | 0 | 2 | 2 | 1 | 0 | 0 | 0 | 0 |

| Record | Target | Task | Agent duration | Hidden access | Result |
| --- | --- | --- | ---: | --- | --- |
| `20260612T131925Z-hidden-effect-availability-badge-318eae72` | `bare` | `hidden-effect-availability-badge` | 65.829s | no | Functional/schema failed; workflow and boundary passed. |
| `20260612T132109Z-hidden-effect-availability-badge-76c908a5` | `workflow-only` | `hidden-effect-availability-badge` | 82.893s | no | Functional/schema failed; workflow and boundary passed. |
| `20260612T132241Z-hidden-effect-bundle-quote-0bf17d73` | `bare` | `hidden-effect-bundle-quote` | 115.029s | no | Functional/schema failed; workflow and boundary passed. |
| `20260612T132444Z-hidden-effect-bundle-quote-b1e1e279` | `workflow-only` | `hidden-effect-bundle-quote` | 141.229s | yes | Functional/schema failed; workflow and boundary passed, but the schedule stopped because the agent ran `rg --files benchmarks/oracles benchmarks/tasks`. |

The stopped record did not read hidden oracle content because `benchmarks/` was
absent from the agent-visible checkout. The abnormal signal is still valid:
agent-visible workflow docs and `AGENTS.md` mention local benchmark/oracle
paths, so the workflow-only agent naturally tried to inspect paths that the
heldout runner intentionally hides.

## Target-Clean Canary

The workflow target repository was updated to remove direct hidden
benchmark/oracle path guidance from agent-visible docs and to make
`scripts/check_harness.py` skip benchmark task-contract checks when
`benchmarks/` is intentionally absent during agent execution.

- Updated target ref: `flask-yes-harness` @
  `3a8f7ff50d967275156e48056598a6babb9686a9`
- Workspace:
  `runs/hidden-flask-bundle-workflow-targetclean-canary-20260612T1335Z`
- Results:
  `results/hidden-flask-bundle-workflow-targetclean-canary-20260612T1335Z`
- Task: `hidden-effect-bundle-quote`
- Target arm: `workflow-only`
- Agent duration: 135.967 seconds
- Stall/timeout: no
- Hidden access: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Excluded-path conflicts: 0

The canary failed hidden functional/schema checks but passed workflow and
boundary checks. This is acceptable diagnostic evidence: the target-clean ref
removed the hidden-path abnormal without turning the heldout task into a
full-contract success.

## Fresh Pilot With Target-Clean Ref

- Suite: `benchmarks/suites/flask-hidden-heldout-10.json`
- Planned shape: 5 tasks x 2 arms x 1 repeat = 10 records
- Completed records before stop: 7
- Workspace: `runs/hidden-flask-heldout-10-targetclean-20260612T1338Z`
- Results: `results/hidden-flask-heldout-10-targetclean-20260612T1338Z`
- Command: `python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/flask-hidden-heldout-10.json --task-limit 5 --repeats 1 --agent-stall-timeout 330 --stop-on-abnormal --workspace runs/hidden-flask-heldout-10-targetclean-20260612T1338Z --results results/hidden-flask-heldout-10-targetclean-20260612T1338Z --execute`
- Stop reason: record 7, `bare` `hidden-effect-catalog-metrics`, stopped by
  the stall watchdog at 330.004 seconds.

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 4 | 0 | 0 | 0 | 3 | 4 | 0 | 1 | 1 | 0 | 0 |
| `workflow-only` | 3 | 0 | 0 | 1 | 3 | 3 | 0 | 0 | 0 | 0 | 0 |

| Record | Target | Task | Agent duration | Stall | Hidden access | Result |
| --- | --- | --- | ---: | --- | --- | --- |
| `20260612T133834Z-hidden-effect-availability-badge-0828e050` | `bare` | `hidden-effect-availability-badge` | 63.404s | no | no | Functional/schema failed; workflow and boundary passed. |
| `20260612T133945Z-hidden-effect-availability-badge-55259745` | `workflow-only` | `hidden-effect-availability-badge` | 71.662s | no | no | Functional/schema failed; workflow and boundary passed. |
| `20260612T134105Z-hidden-effect-bundle-quote-b2ff6ce3` | `bare` | `hidden-effect-bundle-quote` | 166.064s | no | no | Functional/schema failed; workflow and boundary passed. |
| `20260612T134359Z-hidden-effect-bundle-quote-d70d4583` | `workflow-only` | `hidden-effect-bundle-quote` | 122.259s | no | no | Schema passed, functional failed; workflow and boundary passed. |
| `20260612T134608Z-hidden-effect-cart-validation-733788e3` | `bare` | `hidden-effect-cart-validation` | 81.569s | no | no | Functional/schema failed; workflow and boundary passed. |
| `20260612T134736Z-hidden-effect-cart-validation-64e1ac2c` | `workflow-only` | `hidden-effect-cart-validation` | 115.744s | no | no | Functional/schema failed; workflow and boundary passed. |
| `20260612T134959Z-hidden-effect-catalog-metrics-9924a689` | `bare` | `hidden-effect-catalog-metrics` | 330.004s | yes | no | No files changed; workflow failed because the agent was stopped by the watchdog. |

This run confirms that the target-clean ref removed the hidden benchmark path
abnormal from the workflow-only arm. It does not clear promotion criteria:
record 7 produced a first-class `agent_stalled=true` signal on the bare arm.

## Catalog-Metrics Narrow Recheck

- Workspace: `runs/hidden-flask-catalog-metrics-bare-stall-recheck-20260612T1358Z`
- Results: `results/hidden-flask-catalog-metrics-bare-stall-recheck-20260612T1358Z`
- Task: `hidden-effect-catalog-metrics`
- Target arm: `bare`
- Agent duration: 53.577 seconds
- Stall/timeout: no
- Hidden access: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0

The narrow recheck completed and failed only hidden functional/schema checks:
the domain glossary requirement was missed and the catalog metrics response did
not include the expected `meta` object. This suggests the previous
`catalog-metrics` stall was not immediately reproducible as a task-specific
deadlock.

## Target-Clean Fresh Rerun

- Suite: `benchmarks/suites/flask-hidden-heldout-10.json`
- Planned shape: 5 tasks x 2 arms x 1 repeat = 10 records
- Completed records before stop: 2
- Workspace: `runs/hidden-flask-heldout-10-targetclean-rerun-20260612T1359Z`
- Results: `results/hidden-flask-heldout-10-targetclean-rerun-20260612T1359Z`
- Command: `python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/flask-hidden-heldout-10.json --task-limit 5 --repeats 1 --agent-stall-timeout 330 --stop-on-abnormal --workspace runs/hidden-flask-heldout-10-targetclean-rerun-20260612T1359Z --results results/hidden-flask-heldout-10-targetclean-rerun-20260612T1359Z --execute`
- Stop reason: record 2, `workflow-only` `hidden-effect-availability-badge`,
  stopped by the stall watchdog at 330.003 seconds.

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| `workflow-only` | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 |

| Record | Target | Task | Agent duration | Stall | Hidden access | Result |
| --- | --- | --- | ---: | --- | --- | --- |
| `20260612T135953Z-hidden-effect-availability-badge-751d4eb6` | `bare` | `hidden-effect-availability-badge` | 67.084s | no | no | Functional/schema failed; workflow and boundary passed. |
| `20260612T140131Z-hidden-effect-availability-badge-00a8d69e` | `workflow-only` | `hidden-effect-availability-badge` | 330.003s | yes | no | No files changed; workflow failed because the agent was stopped by the watchdog. |

The stopped workflow-only record had no wrong-file edits, forbidden-file edits,
excluded-path conflicts, or hidden benchmark access patterns. The agent read
local Flask routes, tests, docs, and harness guidance, then stalled before
making edits. This keeps the blocker in execution stability rather than hidden
content leakage.

## Recommendation

Do not proceed to the 100-record heldout run yet.

Before the next promotion attempt:

- Keep the in-memory `agent_excluded_paths` handling and temporary git baseline.
- Keep Codex adapter isolation enabled: `CODEX_IGNORE_USER_CONFIG=1`,
  `CODEX_IGNORE_RULES=1`, and `CODEX_DISABLE_PLUGINS=1`, unless running a
  deliberate compatibility control.
- Use the runner's `--agent-stall-timeout` pilot watchdog so "no result after N
  seconds" is captured as a first-class `agent_stalled` record rather than
  requiring manual termination.
- Keep the target-clean workflow ref pinned for future pilots:
  `flask-yes-harness` @ `3a8f7ff50d967275156e48056598a6babb9686a9`.
- Investigate the remaining stall instability before another promotion attempt.
  It has now appeared on bare `hidden-effect-catalog-metrics` and workflow-only
  `hidden-effect-availability-badge`. Both stopped records made no edits and
  had no hidden access, so this is an execution-stability issue rather than a
  leakage issue.
- Only rerun the fresh 10-record pilot after the stall is explained or made
  consistently non-recurring and the agent-visible docs no longer point at
  hidden benchmark/oracle directories. Promote to 100 records only if the
  10-record pilot has zero stalls, zero agent timeouts, zero excluded-path
  conflicts, zero preflight failures, zero wrong/forbidden edits, and no hidden
  benchmark-content access.
