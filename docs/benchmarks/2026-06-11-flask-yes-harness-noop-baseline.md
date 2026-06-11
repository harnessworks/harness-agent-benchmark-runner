# Flask Yes-Harness No-Op Baseline

Date: 2026-06-11
Target: local `flask-yes-harness` @ `512d105a345454363f36b40b0ba2b1c87987053b`
Runner: this repository (`harness-agent-benchmark-runner`)
Agent: bundled no-op adapter (`examples/agents/noop_agent.py`)

## What this run is

This is the negative-control baseline for the harnessed Flask target. The
target starts from the same app and functional benchmark suite as
`flask-no-harness`, then adds project-specific harness instructions, local
drift checks, source tracking, decision/failure memory, and a normal harness
gate.

The no-op adapter makes no edits. Expected result: every focused task oracle
fails, while the harness gate itself passes in the isolated clone.

## Harness target setup

- Harness target path: `/Users/wb/Desktop/flask-yes-harness`
- Harness adoption commit: `a0193fc`
- Corrected benchmark ref: `512d105`
- Correction after adoption: `scripts/check_harness.py` now creates `.venv` and
  installs `requirements.txt` when needed, so runner-owned isolated clones do
  not depend on host-level pytest installation.

Each task spec now points at `../flask-yes-harness` and verifies both:

- `python3 scripts/check_harness.py`
- `bash benchmarks/oracles/run_checks.sh <task-id>`

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

In every task, the harness gate passed first, then the focused oracle rejected
the empty change set.

| Task | Harness gate | Focused oracle | Expected oracle failure |
| --- | --- | --- | --- |
| `flask-health-version` | Passed | Failed | `health must include service name` |
| `flask-products-min-stock` | Passed | Failed | `min_stock filter is wrong` |
| `flask-order-quote` | Passed | Failed | `expected status 200, got 404` |
| `flask-json-errors` | Passed | Failed | `expected JSON content type, got 'text/html; charset=utf-8'` |

## Interpretation

This proves the harnessed target's normal gate is usable from isolated clones
and that the focused task oracles are still non-trivial. It is not a live agent
score; pair it with the Codex pilot from the same target ref.

## Raw artifacts

Raw local records are intentionally not committed:

- `results/flask-yes-harness-noop-20260611T061507Z/2026-06-11.jsonl`
- `runs/flask-yes-harness-noop-20260611T061507Z/*/result.json`
