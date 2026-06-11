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
- Set per-task timeout and global scheduler timeout.
- Store raw run directories as short-retention artifacts.
- Keep long-lived result summaries separate from raw logs.
- Never run benchmark agents against a dirty source checkout.

## Suggested Loop

```bash
for task in benchmarks/tasks/*.json; do
  python3 -m harness_agent_benchmark_runner run \
    --task "$task" \
    --agent-command "$AGENT_COMMAND"
done

python3 -m harness_agent_benchmark_runner summarize --results results
```
