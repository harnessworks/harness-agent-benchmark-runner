# Flask No-Harness No-Op Baseline

Date: 2026-06-11
Target: local `flask-no-harness` @ `878f5c2a0c625d713df4714097601dff50849139`
Runner: this repository (`harness-agent-benchmark-runner`)
Agent: bundled no-op adapter (`examples/agents/noop_agent.py`)

## What this run is

This is a negative-control run for a plain Flask app target. The target is not
`harness-starter-kit` and does not include harness-specific command files. Its
target-specific benchmark specs and deterministic oracles live under the target
repo's `benchmarks/` directory.

The no-op adapter makes no edits. Expected result: every task fails its oracle,
while runner isolation, dependency setup, pytest execution, and file-boundary
scoring all complete cleanly.

## Target suite

The initial Flask suite contains four independent tasks:

| Task | Intended app change | Expected files |
| --- | --- | --- |
| `flask-health-version` | Add service and env-driven version metadata to `GET /health`. | `app/**`, `tests/**` |
| `flask-products-min-stock` | Add `min_stock` filtering and invalid-query JSON errors to `GET /products`. | `app/**`, `tests/**` |
| `flask-order-quote` | Add `POST /orders/quote` using the in-memory product catalog. | `app/**`, `tests/**` |
| `flask-json-errors` | Return JSON bodies for 404 and 405 routing errors. | `app/**`, `tests/**` |

All task specs forbid edits to `benchmarks/**`, requirements, local env files,
`runs/**`, and `results/**`, so an agent cannot score by weakening the oracle or
changing dependency declarations.

## No-op result

| Metric | Value |
| --- | ---: |
| Runs | 4 |
| Successes | 0 |
| Verification passed | 0 |
| Wrong-file edits | 0 |
| Forbidden-file edits | 0 |
| Agent timeouts | 0 |
| Runner errors | 0 |

Each verification command installed the target dependencies into an ignored
`.venv`, ran the baseline pytest suite, then ran the task-specific oracle. The
pytest suite passed in every run, and each oracle rejected the empty change set.

| Task | Success | Verify | Expected oracle failure |
| --- | --- | --- | --- |
| `flask-health-version` | False | False | `health must include service name` |
| `flask-products-min-stock` | False | False | `min_stock filter is wrong` |
| `flask-order-quote` | False | False | `expected status 200, got 404` |
| `flask-json-errors` | False | False | `expected JSON content type, got 'text/html; charset=utf-8'` |

## Reproduction

The target repo was created as a sibling checkout:
`/Users/wb/Desktop/flask-no-harness`.

From the runner root:

```bash
python3 -m harness_agent_benchmark_runner run \
  --task /Users/wb/Desktop/flask-no-harness/benchmarks/tasks/flask-health-version.json \
  --agent-command "python3 /Users/wb/Desktop/harness-agent-benchmark-runner/examples/agents/noop_agent.py" \
  --repo-ref 878f5c2a0c625d713df4714097601dff50849139 \
  --workspace runs/flask-no-harness-noop-20260611T055420Z \
  --results results/flask-no-harness-noop-20260611T055420Z \
  --max-agent-timeout 60 \
  --command-timeout 240
```

Repeat for the other three task specs in
`/Users/wb/Desktop/flask-no-harness/benchmarks/tasks/`.

Raw local artifact:
`results/flask-no-harness-noop-20260611T055420Z/2026-06-11.jsonl`.
Raw `runs/` and `results/` artifacts are intentionally not committed.

## Interpretation

This proves the new bare Flask target suite has non-trivial deterministic
oracles and clean runner boundaries. It is not a live coding-agent score. Pair
this baseline with the Codex pilot from the same date to distinguish oracle
validity from live-agent completion behavior.
