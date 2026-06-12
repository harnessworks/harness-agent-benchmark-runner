# Hidden Flask Heldout 10-Run Pilot And Aborted 100-Run - 2026-06-12

## Summary

After splitting heldout scoring into `functional` and `schema` dimensions, a
10-record pilot completed cleanly. Based on that pilot, a 100-record sequential
run was started. It was stopped after 14 complete records because two early
bare-arm agent timeouts made the run unsuitable as product-value evidence.

This report is diagnostic. Do not promote it to `latest.md` or README headline
evidence.

## 10-Run Pilot

- Suite: `benchmarks/suites/flask-hidden-heldout-10.json`
- Shape: 5 tasks x 2 arms x 1 repeat = 10 records
- Workspace: `runs/hidden-flask-heldout-10-20260612T1001Z`
- Results: `results/hidden-flask-heldout-10-20260612T1001Z`
- Concurrency: `jobs=1`
- Timeout cap: task timeout, 600 seconds

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Timeouts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 5 | 1 | 2 | 4 | 5 | 5 | 0 |
| `workflow-only` | 5 | 2 | 3 | 4 | 5 | 5 | 0 |

The pilot had no preflight failures, wrong-file edits, forbidden-file edits, or
timeouts. The scoring split worked as intended: several records passed schema
and workflow while failing functional behavior, and `catalog-segments` exposed
functional/schema separation in the other direction.

## Aborted 100-Run

- Suite: `benchmarks/suites/flask-hidden-heldout-10.json`
- Planned shape: 5 tasks x 2 arms x 10 repeats = 100 records
- Completed records before stop: 14
- Workspace: `runs/hidden-flask-heldout-100-20260612T1025Z`
- Results: `results/hidden-flask-heldout-100-20260612T1025Z`
- Stop reason: two early bare-arm agent timeouts in 14 records

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Timeouts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 7 | 0 | 0 | 4 | 5 | 7 | 2 |
| `workflow-only` | 7 | 4 | 5 | 5 | 7 | 7 | 0 |

The stopped run still showed a workflow-only advantage in the completed records,
but the timeout pattern appeared too early to treat the partial 100-record run
as representative product evidence.

## Interpretation

The 10-run pilot was clean enough to justify starting the 100-run. The 100-run
itself was not clean enough to finish unchanged. Two bare-arm timeouts in the
first 14 completed records indicate either model/service tail latency or task
prompt/agent behavior that can consume the full 600-second task timeout.

Both timeout records failed before hidden verification became the bottleneck:

- `20260612T104903Z-hidden-effect-availability-badge-e436af4e` ran for
  600.005 seconds, timed out inside `codex_exec_agent.py`, and changed only
  `app/catalog.py`. The agent log shows broad `rg` output from `benchmarks/`
  and direct reads from `benchmarks/oracles/check_task.py` before it added only
  a small `get_product` helper.
- `20260612T110253Z-hidden-effect-bundle-quote-613c8aec` ran for 600.003
  seconds, timed out inside `codex_exec_agent.py`, and changed no files. The
  agent log shows broad `rg` output from `benchmarks/`, then extra docs and git
  history exploration (`git log`, `git ls-tree`, `git show`) after it had
  already decided the intended implementation.

The likely failure mode is not a hidden-oracle mismatch. It is a combination of
underspecified bare-repository exploration, answer-adjacent benchmark/oracle
files being visible to the agent, git-history exploration, and local Codex
configuration/plugin loading noise. The successful bare runs in the same
partial 100-run often inspected benchmark/oracle files too, which also weakens
the product-value interpretation even when they complete.

## Follow-Up Mitigation

The runner and Codex adapter now apply generic benchmark hygiene before another
large held-out run:

- It passes `--ignore-user-config` to `codex exec` by default unless
  `CODEX_PROFILE` is set, reducing local plugin/MCP/config effects in evidence
  runs.
- Held-out task specs set `agent_excluded_paths: ["benchmarks"]`, so target
  benchmark specs and target-local oracle files are hidden while the agent runs
  and restored before verification. The runner now uses a temporary
  agent-visible git baseline for these runs so the hidden files are not still
  readable through `git show`.
- Held-out task specs set `agent_setup.commands` to create `.venv` and install
  `requirements.txt` before the agent starts, and the runner prepends
  `.venv/bin` to PATH. This matches hidden-oracle dependency setup and avoids
  measuring recovery from a missing local pytest executable.
- The optional Codex prompt guard remains disabled by default
  (`CODEX_PROMPT_GUARD=0`) because changing the prompt would weaken
  comparability between arms and with prior runs.
- Runtime controls remain env-configurable for deliberate compatibility checks:
  `CODEX_IGNORE_USER_CONFIG=0` or `CODEX_PROMPT_GUARD=1`.

## Post-Mitigation Checks

Two follow-up checks were run before starting another 100-record attempt:

- `runs/hidden-flask-heldout-10-isolatedgit-20260612T1158Z` was stopped after
  three records because `hidden-effect-bundle-quote` on `bare` still hit the
  600-second agent timeout. This time the agent log had no `./benchmarks`,
  `benchmarks/oracles`, `benchmarks/tasks`, `git show`, `git log`, or
  `git ls-tree` hits, confirming the benchmark-file leakage path was closed.
  The timeout happened after the agent had implemented files and passed a
  manual bundle quote client check.
- After adding `agent_setup.commands`, the targeted canary
  `runs/hidden-flask-bundle-bare-setup-canary-20260612T1213Z` completed the
  same `bare` bundle-quote task without timeout: agent setup took 4.328
  seconds, agent execution took 160.203 seconds, there were no excluded-path
  conflicts, and the log had no benchmark/git-history leakage hits. Strict
  success still failed on hidden functional/schema expectations, which is a
  task-behavior result rather than a loop/timeout failure.

Based on these checks, do not start the 100-record held-out run yet. First run a
fresh 10-record pilot with both `agent_excluded_paths` and `agent_setup.commands`
enabled. Promote to 100 records only if that pilot has zero agent timeouts, zero
excluded-path conflicts, zero preflight failures, and no benchmark/git-history
leakage hits in agent logs.

Keep the 600-second cap for the next product-value pilot. Raise the timeout only
for a separate timeout-pressure diagnostic, not for the representative
held-out product run.

Do not compare this partial 100-run against prior representative runs as if it
were complete.
