# Balanced Hidden-Oracle Flask A/B - 20-Run Jobs=2 Calibration

Date: 2026-06-12
Runner: `harness-agent-benchmark-runner` @
`39a4d943fa2ed2cbff6ee334fa1d8aac77f05638` plus local `--jobs`
and JSONL-lock changes
Agent: Codex CLI `0.138.0-alpha.7` through
`examples/agents/codex_exec_agent.py`
Run ID: `hidden-flask-ab-balanced-20-jobs2-20260612T050040Z`

## Headline

| Target | Completed runs | Strict scored successes | Strict success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | 10 | 9 | 90.0% | 9 | 0 | 0 | 0 | 102s | 216s |
| `flask-yes-harness` | 10 | 10 | 100.0% | 10 | 0 | 0 | 0 | 118s | 195s |

This run calibrates `--jobs 2` throughput for the balanced hidden-oracle Flask
A/B task set. It is not a representative large-run result. Its primary
question is whether low parallelism introduces timeout, runner, or
file-boundary noise before considering a costlier 100-run schedule.

## Scope

This run used the revised concept-based docs oracle. Companion docs are scored
for the relevant route and domain terms, not one exact English phrase.

The task-critical API contract was shared in both prompts. The yes-harness
target still had repository-local harness guidance, documentation-location
guidance, local gate guidance, and boundary guidance.

## Targets

- Bare target: local `flask-no-harness` @ `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- Harnessed target: local `flask-yes-harness` @ `c3eaf9a0105d7b99db414467b5df0edb833697ad`

Both target repositories were clean before execution.

## Run Conditions

- Command: `python3 scripts/run_hidden_flask_ab.py --mode large --task-dir benchmarks/tasks/flask-hidden-balanced --repeats 1 --jobs 2 --workspace runs/hidden-flask-ab-balanced-20-jobs2-20260612T050040Z --results results/hidden-flask-ab-balanced-20-jobs2-20260612T050040Z --execute`
- Started: `2026-06-12T05:00:40+00:00`
- Finished: `2026-06-12T05:22:35+00:00`
- Completed records: 20 of 20 planned records
- Task pairs: 10 hidden Flask A/B pairs
- Repetitions: 1 per target/task pair
- Pair order: `alternate`
- Concurrency: `--jobs 2`
- Task attempts: `max_attempts=1`
- Effective runner cap: `--max-agent-timeout 900`
- Budget hint: `--max-cost-usd 1.0`
- Codex model: `gpt-5.5`
- Codex config override: `CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`

## Per-Task Results

| Target | Task | Runs | Strict scored successes | Strict success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | `hidden-effect-availability-badge` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 95s | 95s |
| `flask-no-harness` | `hidden-effect-bundle-quote` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 151s | 151s |
| `flask-no-harness` | `hidden-effect-cart-validation` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 126s | 126s |
| `flask-no-harness` | `hidden-effect-catalog-metrics` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 102s | 102s |
| `flask-no-harness` | `hidden-effect-catalog-segments` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 66s | 66s |
| `flask-no-harness` | `hidden-effect-pick-list` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 114s | 114s |
| `flask-no-harness` | `hidden-effect-reservation-preview` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 128s | 128s |
| `flask-no-harness` | `hidden-effect-stock-risk` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 81s | 81s |
| `flask-no-harness` | `hidden-effect-supplier-readiness` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 90s | 90s |
| `flask-no-harness` | `hidden-effect-tax-preview` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 216s | 216s |
| `flask-yes-harness` | `hidden-effect-availability-badge` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 125s | 125s |
| `flask-yes-harness` | `hidden-effect-bundle-quote` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 175s | 175s |
| `flask-yes-harness` | `hidden-effect-cart-validation` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 118s | 118s |
| `flask-yes-harness` | `hidden-effect-catalog-metrics` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 97s | 97s |
| `flask-yes-harness` | `hidden-effect-catalog-segments` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 88s | 88s |
| `flask-yes-harness` | `hidden-effect-pick-list` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 195s | 195s |
| `flask-yes-harness` | `hidden-effect-reservation-preview` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 186s | 186s |
| `flask-yes-harness` | `hidden-effect-stock-risk` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 118s | 118s |
| `flask-yes-harness` | `hidden-effect-supplier-readiness` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 109s | 109s |
| `flask-yes-harness` | `hidden-effect-tax-preview` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 146s | 146s |

## Failure Signal

The single failure was in `flask-no-harness`:

| Target | Task | Failure signal |
| --- | --- | --- |
| `flask-no-harness` | `hidden-effect-catalog-metrics` | Hidden oracle rejected companion docs: glossary documented the route but missed the `inventory value` and `average price` concepts required by the current concept-docs oracle. |

The agent exited cleanly. Pytest passed before the hidden oracle assertion
failed. There were no wrong-file edits, forbidden-file edits, runner errors, or
agent timeouts.

## Interpretation

As a throughput calibration, this is a clean `jobs=2` result: 20/20 records
completed, JSONL output remained valid under concurrent appends, and no timeout
or boundary noise appeared. This supports using `--jobs 2` as a candidate run
shape when wall-clock time matters.

As harness-effect evidence, the result is narrower. It shows 9/10 vs 10/10
under the balanced prompt and revised docs oracle, but the run intentionally
changed the scheduler condition from sequential to `jobs=2`. A representative
100-run result should either remain sequential for the cleanest claim or state
`jobs=2` as part of the measured condition and keep timeout behavior as a
separate reported column.

## Raw Artifacts

Raw local artifacts are intentionally not committed:

- Results JSONL: `results/hidden-flask-ab-balanced-20-jobs2-20260612T050040Z/2026-06-12.jsonl`
- Run directories: `runs/hidden-flask-ab-balanced-20-jobs2-20260612T050040Z/`
