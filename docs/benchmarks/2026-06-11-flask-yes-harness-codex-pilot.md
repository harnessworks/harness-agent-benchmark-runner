# Live Agent Pilot - Codex CLI on Flask Yes-Harness

Date: 2026-06-11
Target: local `flask-yes-harness` @ `512d105a345454363f36b40b0ba2b1c87987053b`
Agent: Codex CLI `0.138.0-alpha.7`
Adapter: `examples/agents/codex_exec_agent.py`
Runner: this repository (`harness-agent-benchmark-runner`)

## Headline

| Target | Agent | Mode | Runs | Successes | Success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-yes-harness` | Codex CLI | Live adapter pilot | 4 | 3 | 75% | 4 | 0 | 0 | 1 |

This was the first live-agent pass against the harnessed Flask target. The four
tasks ran in parallel once, matching the shape of the earlier
`flask-no-harness` pilot.

## Conditions

- Task source: local `/Users/wb/Desktop/flask-yes-harness/benchmarks/tasks/`
- Target ref: `512d105a345454363f36b40b0ba2b1c87987053b`
- Agent command: `python3 examples/agents/codex_exec_agent.py`
- Codex command defaults: no `CODEX_MODEL`, `CODEX_PROFILE`, or
  `CODEX_EXEC_ARGS` override was set
- Runner cap: `--max-agent-timeout 600`
- Budget hint: `--max-cost-usd 1.0`
- Task attempts: `max_attempts=1`
- Execution shape: four tasks run in parallel for one completed round
- Verification per task: harness gate plus focused oracle

## Per-task result

| Task | Success | Verification | Agent duration | Changed files | Notes |
| --- | --- | --- | ---: | --- | --- |
| `flask-json-errors` | True | True | 105s | `app/__init__.py`, `tests/test_app.py` | Clean pass. |
| `flask-products-min-stock` | True | True | 130s | `app/__init__.py`, `tests/test_app.py` | Clean pass. |
| `flask-order-quote` | True | True | 194s | `app/__init__.py`, `tests/test_app.py` | Clean pass. |
| `flask-health-version` | False | True | 600s | `app/__init__.py`, `tests/test_app.py` | Agent timed out after producing a verifying solution. |

## A/B comparison with no-harness pilot

| Target | Runs | Successes | Verification passed | Wrong-file edits | Forbidden-file edits | Timeout task |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `flask-no-harness` | 4 | 3 | 4 | 0 | 0 | `flask-order-quote` |
| `flask-yes-harness` | 4 | 3 | 4 | 0 | 0 | `flask-health-version` |

Both targets produced verifying solutions for all four tasks and stayed inside
file boundaries. The harnessed target did not improve the 1× scored success
rate, but it changed the timeout pattern: the complex quote task completed in
194 seconds under the harnessed prompt, while the simple health task produced a
verifying solution but did not exit before the 600-second cap.

## Interpretation

This single pilot is not enough to claim a harness effect. It does show that
the harnessed target is operational under the runner and that file-boundary
discipline remains clean. The current signal is mostly completion-time
variance, not correctness: both pilots have 4/4 verification passes and one
agent timeout.

The next useful measurement is a repeated 5x A/B run with controlled
parallelism. Use either one task at a time to isolate model behavior or two
concurrent tasks to reduce wall-clock time without reproducing the earlier
high-concurrency timeout pressure.

## Raw artifacts

Raw local records are intentionally not committed:

- `results/flask-yes-harness-codex-1run-20260611T061549Z/2026-06-11.jsonl`
- `runs/flask-yes-harness-codex-1run-20260611T061549Z/*/result.json`
- `runs/flask-yes-harness-codex-1run-20260611T061549Z/*/logs/`
