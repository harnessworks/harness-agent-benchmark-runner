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

## Recommendation

Do not proceed to the 100-record heldout run yet.

Before the next promotion attempt:

- Keep the in-memory `agent_excluded_paths` handling and temporary git baseline.
- Add a short pilot watchdog to the orchestrator so "no result after N seconds"
  is captured as a first-class interrupted/stalled record rather than requiring
  manual termination.
- Re-run a narrow `bare` `hidden-effect-bundle-quote` diagnostic with log
  streaming enabled or a lower pilot cap to determine whether the stall is
  Codex execution latency, task-specific exploration, or adapter buffering.
- Only rerun the fresh 10-record pilot after the stall is explained or made
  measurable. Promote to 100 records only if the 10-record pilot has zero
  stalls, zero agent timeouts, zero excluded-path conflicts, zero preflight
  failures, zero wrong/forbidden edits, and no hidden benchmark-content access.

