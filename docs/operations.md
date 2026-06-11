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
