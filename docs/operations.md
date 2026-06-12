# Operations

## 24-Hour Runner Shape

Use an external scheduler first:

- self-hosted GitHub Actions runner for hosted artifacts
- `launchd` on macOS
- `systemd` timer on Linux
- a managed VM cron job

Each scheduled invocation should run one task in one isolated clone and append a
JSONL result. A separate job can summarize results every hour or at the end of a
24-hour window.

## Minimum Production Safeguards

- Use a dedicated benchmark machine or self-hosted runner.
- Run with a dedicated API key and budget limit.
- Set per-task timeout, optional runner `--agent-timeout-override`, runner
  `--max-agent-timeout`, and global scheduler timeout.
- For pilots, set runner `--agent-stall-timeout` below the task timeout so
  stalled agent attempts are recorded as JSONL evidence instead of being
  terminated manually.
- For promotion-readiness pilots, prefer `--agent-idle-timeout` plus
  `--agent-no-edit-timeout` over a short wall-clock stall timeout. The idle
  watchdog catches no-output hangs; the no-edit watchdog catches active-output
  attempts that still make no repository changes.
- Keep task `max_attempts` at `1` for first-pass measurements; increase it only
  when intentionally measuring retry recovery.
- Store raw run directories as short-retention artifacts.
- Keep long-lived result summaries separate from raw logs.
- Never run benchmark agents against a dirty source checkout.

## Suggested Loop

```bash
for task in benchmarks/tasks/*.json; do
  python3 -m harness_agent_benchmark_runner run \
    --task "$task" \
    --agent-command "$AGENT_COMMAND" \
    --max-agent-timeout "${BENCHMARK_MAX_AGENT_TIMEOUT:-900}" \
    --max-cost-usd "${BENCHMARK_MAX_COST_USD:-2.5}"
done

python3 -m harness_agent_benchmark_runner summarize --results results
```

## Hidden Flask Harness Arm Runs

Use `scripts/run_hidden_flask_ab.py` for hidden-oracle Flask arm runs. It
supports legacy two-arm task pairs and the preferred three-arm shape:

- `bare`: no harness.
- `workflow-only`: `AGENTS`, local gate, docs placement, and boundary rules.
- `memory-harness`: workflow harness plus generalized project conventions and
  failure memory.

The script interleaves arms by round/task/group, pins Codex to one model
configuration, and defaults to a no-cost dry run. Live agent execution requires
`--execute`.

Dry-run the reduced heldout promotion pilot plan:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-heldout-stable-8.json \
  --mode pilot \
  --repeats 2 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal
```

`benchmarks/suites/flask-hidden-heldout-stable-8.json` deliberately excludes
`hidden-effect-bundle-quote` after repeated tail-latency stops. One repeat is
4 tasks x 2 arms, so a one-repeat smoke is 8 records rather than the older
10-record full-heldout shape. Use at least 2 repeats, or 16 records, as the
reduced promotion-readiness pilot. For a near-100 promotion over this reduced
suite, use 12 repeats for 96 balanced records or 13 repeats for 104 balanced
records; do not cut a schedule mid-repeat just to force exactly 100 records.

The no-edit watchdog is the mitigation for the previously observed no-edit idle
tail. Earlier reduced attempts stopped at workflow-only and bare
cart-validation records, while focused workflow-only cart-validation triage
completed 3/3 clean records. Treat those older stops as intermittent tail
behavior across arms, not as a single task/arm failure.

The A/B script now has an explicit promotion guard. Near-100 reduced runs
should use `--promotion-run` and point at a prior clean pilot with at least two
clean records for every selected task/arm pair. The promotion guard requires
both the idle-output watchdog and the no-edit watchdog:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-heldout-stable-8.json \
  --repeats 12 \
  --promotion-run \
  --require-clean-results results/<stable8-two-round-pilot> \
  --min-clean-rounds 2 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal \
  --execute
```

Using a one-repeat stable-8 pilot as promotion evidence fails this guard
because it covers each task/arm pair only once. A two-round pilot with any
watchdog stop, timeout, boundary issue, hidden-access finding, or preflight
failure also fails. This is intended: do not run near-100 promotion until the
prior pilot results are both sufficiently covered and clean.

When rerunning reduced heldout readiness from fresh workspaces, remember that
the stable-8 suite has eight task/arm pairs per repeat. The clean readiness
pilot is 16 records rather than an exact 10-record pilot:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-heldout-stable-8.json \
  --mode pilot \
  --repeats 2 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal \
  --execute
```

For focused triage, prefer a quarantine suite when one exists:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-heldout-bundlequote-quarantine.json \
  --repeats 3
```

For ad-hoc triage inside a larger suite, select exact task groups with
`--task-id`. The option may be repeated and is applied after any suite
`task_ids` filter and before `--task-limit`.

Run the pilot only after approving live Codex usage:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-heldout-stable-8.json \
  --mode pilot \
  --repeats 2 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal \
  --execute
```

The original answer-free heldout, reduced heldout, quarantine, and
workflow-smoke suite manifests are legacy two-arm calibrations. In the
three-arm taxonomy, `no-harness` maps to `bare`, and the clean `yes-harness`
ref maps to `workflow-only`. They do not measure `memory-harness` product
value.

`benchmarks/suites/flask-hidden-three-arm-stable4.json` is the first scaffolded
three-arm partial-realistic pilot suite. It uses the same stable four heldout
task groups as the reduced suite, adds a `memory-harness` arm, and plans
4 tasks x 3 arms = 12 records per repeat. The memory arm points at the sibling
target repository `../flask-memory-harness` pinned to
`bc097c48d592e7ddcd26beb7bb2c185d7a33fa59`, which adds generalized
response-key failure memory without adding heldout route names or exact oracle
answers.

Dry-run the three-arm pilot plan:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-three-arm-stable4.json \
  --repeats 1 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal
```

A true product-value run should use a suite with:

- all three arms fixed to `bare`, `workflow-only`, and `memory-harness`
- `partial-realistic` prompts as the main experiment
- `full-contract` prompts only as controls
- held-out tasks that apply existing conventions to new API surfaces
- `leakage_audit` entries that block exact held-out route names, response
  constants, oracle filenames, raw `runs/`, and raw `results/` before the agent
  runs

For a 100-record legacy A/B control over the balanced hidden Flask set, use all
ten task pairs and `repeats=5`:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --mode large \
  --task-dir benchmarks/tasks/flask-hidden-balanced \
  --repeats 5 \
  --execute
```

The 2026-06-12 100-record `jobs=2` evidence run produced 46/50 strict scored
successes for `flask-no-harness` and 48/50 for `flask-yes-harness`.
Verification passed was 46/50 vs 49/50. Both targets had 0 wrong-file edits and
0 forbidden-file edits, but `jobs=2` introduced timeout noise: 1 no-harness
timeout and 2 yes-harness timeouts. Treat that result as representative for the
explicit `jobs=2` condition, not as a pure sequential claim.

For the cleanest timeout-stability follow-up, rerun the same 100-record shape
sequentially:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --mode large \
  --task-dir benchmarks/tasks/flask-hidden-balanced \
  --repeats 5 \
  --execute
```

The script sets:

- `CODEX_MODEL=gpt-5.5`
- `CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`
- `--jobs 1` by default, so representative runs are sequential unless
  parallelism is explicitly part of the measured condition

The optional `--agent-stall-timeout` is a pilot watchdog. It is intentionally
separate from the effective task timeout: if it fires, the runner records
`scoring.agent_stalled=true`, keeps `agent_timed_out=true` for timeout
accounting, and writes the result before moving to the next scheduled record.
Use it to diagnose promotion readiness; do not hide stall counts inside
functional or schema success rates.

Do not use a short pilot watchdog as the automatic cutoff for promotion runs.
In the current reduced heldout suite, a balanced promotion is 96 or 104
records, not exactly 100, because `bundle-quote` is quarantined. Require at
least a two-round reduced pilot or another stronger stability check before
promoting this shape again. In the
2026-06-12 prompt-guard heldout attempt, a 330-second wall-clock watchdog
stopped a record that had active edits. For promotion, either rely on the task
timeout or use `--agent-idle-timeout` plus `--agent-no-edit-timeout`. The idle
watchdog stops the agent only after no stdout/stderr output has been observed
for the configured interval. The no-edit watchdog stops active-output attempts
only if no visible repository changes have appeared by the configured interval.
All three watchdogs record `scoring.agent_stalled=true`; use
`agent.termination_reason` to distinguish `stall_watchdog`, `idle_watchdog`,
and `no_edit_watchdog`.

Use `--agent-timeout-override` when a promotion run intentionally needs a
different effective task timeout than the task JSON. The runner applies that
override before `--max-agent-timeout`, so `--max-agent-timeout` remains a cap.
For example, a 900-second heldout promotion should pass both
`--agent-timeout-override 900` and a `--max-agent-timeout` of at least `900`.
Without the override, a task with `timeout_seconds: 600` still times out at
600 seconds even if `--max-agent-timeout 900` is present.

The Codex adapter also applies runtime hygiene by default:

- `CODEX_IGNORE_USER_CONFIG=1` unless `CODEX_PROFILE` is set, reducing local
  Codex profile/config effects in evidence runs.
- `CODEX_IGNORE_RULES=1`, disabling user/project execpolicy `.rules` files.
  This does not disable repository `AGENTS.md` guidance used by workflow arms.
- `CODEX_DISABLE_PLUGINS=1`, disabling Codex plugin loading so local plugin
  manifests and plugin-contributed skills do not shape benchmark behavior.
  Setting `CODEX_PROFILE` does not re-enable `.rules` files or plugins; use
  `CODEX_IGNORE_RULES=0` or `CODEX_DISABLE_PLUGINS=0` only for an explicit
  compatibility control.
- `CODEX_PROMPT_GUARD=0`; representative evidence runs leave the task prompt
  unchanged. Turn this on only for deliberate adapter debugging, and report it.

Hidden held-out tasks can also set `agent_excluded_paths`, typically
`["benchmarks"]`, so benchmark specs and target-local oracle files are hidden
while the agent runs and restored before verification. This is the preferred way
to prevent answer-adjacent benchmark files from shaping agent behavior without
adding prompt guidance.

When `agent_excluded_paths` hides `benchmarks/`, the agent-visible target docs
and `AGENTS.md` should not instruct agents to inspect `benchmarks/tasks`,
`benchmarks/oracles`, or parent-directory benchmark paths. Keep answer-free
local gates visible through `scripts/check_harness.py` or similar generic
commands instead. The A/B script's `--stop-on-abnormal` mode treats direct
agent attempts to enumerate hidden benchmark/oracle paths as a promotion
blocker even if the hidden files are not actually readable.

Hidden Flask held-out tasks also use `agent_setup.commands` to create `.venv`
and install `requirements.txt` before the agent starts. The runner prepends
`.venv/bin` to the agent PATH when present. This matches the hidden oracle's
dependency setup and avoids measuring whether the agent can recover from a
missing local pytest executable.

These controls are answer-free operational controls. Disable or change them
only for a deliberate adapter compatibility check, and record that in the
benchmark report.

Keep `max_attempts=1` for A/B measurements. A failed task is benchmark data, so
the A/B script continues after non-zero runner exits and writes every result it
can collect.

Use `--arm-order rotate` for multi-arm runs unless ordering effects are the
thing being measured. The legacy `--pair-order alternate` maps to the same
rotation behavior for two arms.

Use `--jobs 2` only as a throughput calibration before promoting it to a
representative run shape. Record the job count in the report, and treat any
timeout under parallel execution as possibly caused by scheduler or service
pressure until a sequential follow-up rules that out. Avoid higher concurrency
for Codex evidence runs unless the experiment is explicitly measuring
concurrency pressure.

Treat interrupted large runs as diagnostic only. Do not promote partial JSONL
records to `docs/benchmarks/latest.md` or README evidence tables. When reporting
wrong-file edits, describe them as task-boundary misses relative to
`expected_files`; for this Flask suite, root `README.md` edits are outside the
allowed companion-document path (`docs/**`), not inherently bad documentation
changes.

Before a representative hidden Flask run, verify that every task prompt is
identical across arms and says to update companion documentation in the
repository's documented docs location. If `expected_files` includes `docs/**`
but not `README.md`, the prompt must explicitly exclude root `README.md` unless
the task asks for README changes. Keep reporting strict scored success
separately from functional, schema-contract, workflow, boundary success,
timeouts, and stalls.

Use
`docs/benchmarks/templates/hidden-flask-ab-report-template.md` for the public
summary. To generate the headline and per-task Markdown tables from local JSONL
records, run:

```bash
python3 scripts/summarize_hidden_ab.py --results results/<run-id>
```

Do not commit raw `runs/`, `results/`, logs, cloned repositories, or
credentials.

## launchd Shape

On macOS, prefer a thin `launchd` job that calls a shell script in this
repository. Keep API keys in the user environment or keychain-backed shell setup,
not in the plist.

The script should:

- update or reset the runner checkout only when the source repository is clean
- export one `AGENT_COMMAND`
- run the suggested loop above
- archive `results/*.jsonl` and selected `runs/*/logs` as job artifacts

## GitHub Actions Shape

A self-hosted GitHub Actions runner gives artifact retention and scheduling
without adding a daemon here. The job should check out this repository, check out
or mount target repositories separately, then run one task per step or matrix
entry. Store `results/*.jsonl` as the primary artifact and raw run logs with
shorter retention.
