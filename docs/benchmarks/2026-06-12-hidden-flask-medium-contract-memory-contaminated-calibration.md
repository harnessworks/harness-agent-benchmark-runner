# Hidden Flask Medium A/B - Contract-Memory Contaminated Calibration

Date: 2026-06-12
Runner: `harness-agent-benchmark-runner` @
`674879c180ee76a2f46e8e71ca6ded254ae2340e`
Agent: Codex CLI `0.138.0-alpha.7` through
`examples/agents/codex_exec_agent.py`
Run ID: `hidden-flask-ab-medium-20-jobs2-20260612T081231Z`

## Classification

This is a **medium prompt / contract-memory contaminated calibration** only.
It is not a completed 20-run pilot and must not be promoted to
`docs/benchmarks/latest.md` or the README as representative evidence.

The run was stopped by operator request after 11 completed JSONL records out of
20 planned records. Two additional run directories existed for in-flight
attempts when the process tree was terminated; those attempts did not append
completed JSONL records and are excluded from all scored counts below.

The result is also contaminated for the intended medium-prompt research
question: the harnessed target still contains repository-local convention
memory with exact hidden-task API contracts from prior calibration work. That
makes this run useful for operational calibration and failure inspection, but
not clean evidence that a medium-realistic prompt alone measured convention
discovery.

## Headline

| Target | Completed runs | Strict scored successes | Strict success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | 5 | 0 | 0.0% | 0 | 0 | 0 | 0 | 125s | 155s |
| `flask-yes-harness` | 6 | 5 | 83.3% | 5 | 0 | 0 | 1 | 108s | 600s |

## Stop Status

The live run used:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --mode large \
  --task-dir benchmarks/tasks/flask-hidden-medium \
  --repeats 1 \
  --jobs 2 \
  --workspace runs/hidden-flask-ab-medium-20-jobs2-20260612T081231Z \
  --results results/hidden-flask-ab-medium-20-jobs2-20260612T081231Z \
  --execute
```

It was canceled before completion. The active process tree was terminated, and
a follow-up process check found no remaining `run_hidden_flask_ab.py`,
`harness_agent_benchmark_runner run`, `codex_exec_agent.py`, or `codex ...
exec` process for this run.

Partial local artifacts were intentionally preserved:

- Completed result records: 11
- Partial run directories: 13
- Results JSONL: `results/hidden-flask-ab-medium-20-jobs2-20260612T081231Z/2026-06-12.jsonl`
- Run directories: `runs/hidden-flask-ab-medium-20-jobs2-20260612T081231Z/`

## Targets

- Bare target: local `flask-no-harness` @
  `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- Harnessed target: local `flask-yes-harness` @
  `c3eaf9a0105d7b99db414467b5df0edb833697ad`

Both target repositories were clean before the `jobs=2` run.

## Run Conditions

- Completed records: 11 of 20 planned records
- Task pairs: 10 hidden Flask medium A/B pairs
- Repetitions: 1 per target/task pair
- Pair order: `alternate`
- Concurrency: `--jobs 2`
- Task attempts: `max_attempts=1`
- Effective runner cap: `--max-agent-timeout 900`
- Task timeout in these records: 600 seconds
- Budget hint: `--max-cost-usd 1.0`
- Codex model: `gpt-5.5`
- Codex config override:
  `CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`

## Per-Task Results

| Target | Task | Runs | Strict scored successes | Strict success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | `hidden-effect-availability-badge` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 125s | 125s |
| `flask-no-harness` | `hidden-effect-bundle-quote` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 155s | 155s |
| `flask-no-harness` | `hidden-effect-cart-validation` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 137s | 137s |
| `flask-no-harness` | `hidden-effect-catalog-metrics` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 106s | 106s |
| `flask-no-harness` | `hidden-effect-catalog-segments` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 95s | 95s |
| `flask-yes-harness` | `hidden-effect-availability-badge` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 103s | 103s |
| `flask-yes-harness` | `hidden-effect-bundle-quote` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 155s | 155s |
| `flask-yes-harness` | `hidden-effect-cart-validation` | 1 | 0 | 0.0% | 0 | 0 | 0 | 1 | 600s | 600s |
| `flask-yes-harness` | `hidden-effect-catalog-metrics` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 122s | 122s |
| `flask-yes-harness` | `hidden-effect-catalog-segments` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 108s | 108s |
| `flask-yes-harness` | `hidden-effect-pick-list` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 100s | 100s |

## Failure Signals

Completed no-harness failures:

| Target | Task | Failure signal |
| --- | --- | --- |
| `flask-no-harness` | `hidden-effect-availability-badge` | Hidden oracle rejected the product summary shape. |
| `flask-no-harness` | `hidden-effect-bundle-quote` | Hidden oracle expected HTTP 200 but got `400 {"error":"invalid_items"}`. |
| `flask-no-harness` | `hidden-effect-cart-validation` | Hidden oracle did not find the expected `items` list. |
| `flask-no-harness` | `hidden-effect-catalog-metrics` | Hidden oracle found `average_price` missing or non-decimal-compatible. |
| `flask-no-harness` | `hidden-effect-catalog-segments` | Hidden oracle found the `catalog-segments-v1` rules marker missing or wrong. |

Completed yes-harness failure:

| Target | Task | Failure signal |
| --- | --- | --- |
| `flask-yes-harness` | `hidden-effect-cart-validation` | Agent timed out at 600 seconds and did not implement the endpoint; hidden oracle then got HTTP 404. |

## Boundary Check

No completed record had wrong-file edits or forbidden-file edits.

This means the partial signal is about functional contract-following and one
timeout, not file-boundary drift. Because the run is partial and contaminated,
these counts are calibration data only.

## Interpretation

This run should not be used to claim a medium-prompt harness win. The result is
consistent with strong harness-side contract memory, not necessarily with the
intended question of whether a realistic prompt helps agents discover
repository-local conventions.

The useful takeaways are narrower:

- The `flask-hidden-medium` task family executes under `--jobs 2` and appends
  valid result records before cancellation.
- No completed record showed wrong-file or forbidden-file edits.
- The bare target missed several hidden oracle conventions under medium prompts
  in the completed subset.
- The harnessed target still suffered a timeout on cart validation under
  `--jobs 2`, so timeout noise remains a separate concern.

For a clean medium-realistic pilot, remove or neutralize exact task-contract
memory from the harnessed target before rerunning, then execute the full
20-record schedule and report strict success, verification success, boundary
issues, and timeouts separately.

## Raw Artifacts

Raw local artifacts are intentionally not committed:

- Results JSONL: `results/hidden-flask-ab-medium-20-jobs2-20260612T081231Z/2026-06-12.jsonl`
- Run directories: `runs/hidden-flask-ab-medium-20-jobs2-20260612T081231Z/`
