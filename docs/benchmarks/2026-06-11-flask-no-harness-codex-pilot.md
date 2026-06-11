# Live Agent Pilot - Codex CLI on Flask No-Harness

Date: 2026-06-11
Target: local `flask-no-harness` @ `878f5c2a0c625d713df4714097601dff50849139`
Agent: Codex CLI `0.138.0-alpha.7`
Adapter: `examples/agents/codex_exec_agent.py`
Runner: this repository (`harness-agent-benchmark-runner`)

## Headline

| Target | Agent | Mode | Runs | Successes | Success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | Codex CLI | Live adapter pilot | 4 | 3 | 75% | 4 | 0 | 0 | 1 |

This was the first live-agent pass against the plain Flask target. It started
as a planned 5× run, but the first round exposed a 600-second timeout on
`flask-order-quote`, so the remaining rounds were stopped before they wrote
records. The completed records are therefore treated as a 1× pilot.

## Conditions

- Task source: local `/Users/wb/Desktop/flask-no-harness/benchmarks/tasks/`
- Target ref: `878f5c2a0c625d713df4714097601dff50849139`
- Agent command: `python3 examples/agents/codex_exec_agent.py`
- Codex command defaults: no `CODEX_MODEL`, `CODEX_PROFILE`, or
  `CODEX_EXEC_ARGS` override was set
- Runner cap: `--max-agent-timeout 600`
- Budget hint: `--max-cost-usd 1.0`
- Task attempts: `max_attempts=1`
- Execution shape: four tasks run in parallel for one completed round

## Per-task result

| Task | Success | Verification | Agent duration | Changed files | Notes |
| --- | --- | --- | ---: | --- | --- |
| `flask-health-version` | True | True | 123s | `app/__init__.py`, `tests/test_app.py` | Clean pass. |
| `flask-products-min-stock` | True | True | 107s | `app/__init__.py`, `tests/test_app.py` | Clean pass. |
| `flask-json-errors` | True | True | 166s | `app/__init__.py`, `tests/test_app.py` | Clean pass. |
| `flask-order-quote` | False | True | 600s | `app/__init__.py`, `tests/test_app.py` | Agent timed out after producing a verifying solution. |

## Failure analysis

`flask-order-quote` is the only failed record. The changed files were inside
the expected boundary and the task oracle passed:

- pytest plus oracle: 10 tests passed, `flask-order-quote: oracle passed`
- `git diff --check`: passed
- wrong-file edits: 0
- forbidden-file edits: 0

The run still scored as failure because the runner requires the agent process
to exit with code `0` before timeout. The Codex process hit the 600-second cap
and returned exit `124`.

## Interpretation

This pilot shows the plain Flask task suite is solvable by Codex CLI under the
runner: all four completed records passed deterministic verification, and there
were no file-boundary violations. The only score failure is completion-time
behavior on the most complex task.

The next representative measurement should rerun the same four tasks for 5×
with a deliberately chosen cap and concurrency. A lower cap, such as 300
seconds, would make timeout behavior cheaper to measure; lower parallelism
would isolate whether the long tail is task complexity or concurrent Codex
pressure.

## Raw artifacts

Raw local records are intentionally not committed:

- `results/flask-no-harness-codex-5runs-20260611T055613Z/2026-06-11.jsonl`
- `runs/flask-no-harness-codex-5runs-20260611T055613Z/*/result.json`
- `runs/flask-no-harness-codex-5runs-20260611T055613Z/*/logs/`
