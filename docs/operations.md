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

## Hidden Flask Harness A/B

Use `scripts/run_hidden_flask_ab.py` for the next hidden-oracle Flask A/B run.
It interleaves A (`flask-no-harness`) and B (`flask-yes-harness`) by
round/task/group, pins Codex to one model configuration, and defaults to a
no-cost dry run. Live agent execution requires `--execute`.

Dry-run the pilot plan:

```bash
python3 scripts/run_hidden_flask_ab.py --mode pilot
```

Run the pilot only after approving live Codex usage:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --mode pilot \
  --execute
```

The current committed hidden Flask set has ten task pairs. A representative
large run uses all hidden task pairs and 10 repeats:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --mode large \
  --execute
```

The script sets:

- `CODEX_MODEL=gpt-5.5`
- `CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`

Keep `max_attempts=1` for A/B measurements. A failed task is benchmark data, so
the A/B script continues after non-zero runner exits and writes every result it
can collect.

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
