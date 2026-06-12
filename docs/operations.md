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
- Set per-task timeout, runner `--max-agent-timeout`, and global scheduler timeout.
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

Dry-run the pilot plan:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-heldout-10.json \
  --mode pilot
```

Run the pilot only after approving live Codex usage:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-heldout-10.json \
  --mode pilot \
  --execute
```

The current committed answer-free heldout and workflow-smoke suite manifests
are still legacy two-arm calibrations. In the three-arm taxonomy,
`no-harness` maps to `bare`, and the clean `yes-harness` ref maps to
`workflow-only`. They do not measure `memory-harness` product value.

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

The Codex adapter also applies runtime hygiene by default:

- `CODEX_IGNORE_USER_CONFIG=1` unless `CODEX_PROFILE` is set, so local Codex
  plugins, MCP clients, and personal config do not affect evidence runs.
- `CODEX_PROMPT_GUARD=0`; representative evidence runs leave the task prompt
  unchanged. Turn this on only for deliberate adapter debugging, and report it.

Hidden held-out tasks can also set `agent_excluded_paths`, typically
`["benchmarks"]`, so benchmark specs and target-local oracle files are hidden
while the agent runs and restored before verification. This is the preferred way
to prevent answer-adjacent benchmark files from shaping agent behavior without
adding prompt guidance.

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
separately from functional, schema-contract, workflow, and boundary success.

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
