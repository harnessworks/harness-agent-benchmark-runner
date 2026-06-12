# Hidden Flask A/B Partial Calibration - Codex CLI 35 Records

Date: 2026-06-12
Runner: this repository (`harness-agent-benchmark-runner`) @ `9a6ab662a3c9c72253170bfcb10d83ca7e8c9a66`
Agent: Codex CLI through `examples/agents/codex_exec_agent.py`
Run ID: `hidden-flask-ab-large-20260612T020437Z`

## Headline

| Target | Completed records | Strict scored successes | Strict success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | 17 | 0 | 0.0% | 0 | 0 | 0 | 0 | 154s | 216s |
| `flask-yes-harness` | 18 | 18 | 100.0% | 18 | 0 | 0 | 0 | 134s | 192s |

This was an intentionally stopped partial run. It is partial hidden-contract
calibration and upper-bound evidence, not representative large A/B evidence.
It should not be promoted to `docs/benchmarks/latest.md` or the README as the
latest representative benchmark.

## Stop Status

The planned command was:

```bash
python3 scripts/run_hidden_flask_ab.py --mode large --repeats 5 --execute
```

The run was interrupted with Ctrl-C after 35 completed JSONL records. The
in-flight 36th record was `hidden-effect-stock-risk` against
`flask-no-harness`; it was interrupted before a result record was appended and
is excluded from all counts in this report.

After interruption, no matching `run_hidden_flask_ab.py`,
`harness_agent_benchmark_runner run`, or `codex ... exec` process remained.

## Targets

- Bare target: local `flask-no-harness` @ `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- Harnessed target: local `flask-yes-harness` @ `c3eaf9a0105d7b99db414467b5df0edb833697ad`

Both target repositories were clean when checked after the stop.

## Run Conditions

- Command: `python3 scripts/run_hidden_flask_ab.py --mode large --repeats 5 --execute`
- Completed records: 35 of 100 planned records
- Task pairs: 10 hidden Flask A/B pairs
- Pair order: `alternate`
- Task attempts: `max_attempts=1`
- Effective runner cap: `--max-agent-timeout 900`
- Budget hint: `--max-cost-usd 1.0`
- Codex model: `gpt-5.5`
- Codex config override: `CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`

## Per-Task Results

| Target | Task | Runs | Strict scored successes | Strict success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | `hidden-effect-availability-badge` | 2 | 0 | 0.0% | 0 | 0 | 0 | 0 | 115s | 170s |
| `flask-no-harness` | `hidden-effect-bundle-quote` | 2 | 0 | 0.0% | 0 | 0 | 0 | 0 | 154s | 187s |
| `flask-no-harness` | `hidden-effect-cart-validation` | 2 | 0 | 0.0% | 0 | 0 | 0 | 0 | 121s | 216s |
| `flask-no-harness` | `hidden-effect-catalog-metrics` | 2 | 0 | 0.0% | 0 | 0 | 0 | 0 | 120s | 149s |
| `flask-no-harness` | `hidden-effect-catalog-segments` | 2 | 0 | 0.0% | 0 | 0 | 0 | 0 | 154s | 171s |
| `flask-no-harness` | `hidden-effect-pick-list` | 2 | 0 | 0.0% | 0 | 0 | 0 | 0 | 180s | 195s |
| `flask-no-harness` | `hidden-effect-reservation-preview` | 2 | 0 | 0.0% | 0 | 0 | 0 | 0 | 140s | 160s |
| `flask-no-harness` | `hidden-effect-stock-risk` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 180s | 180s |
| `flask-no-harness` | `hidden-effect-supplier-readiness` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 149s | 149s |
| `flask-no-harness` | `hidden-effect-tax-preview` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 134s | 134s |
| `flask-yes-harness` | `hidden-effect-availability-badge` | 2 | 2 | 100.0% | 2 | 0 | 0 | 0 | 133s | 152s |
| `flask-yes-harness` | `hidden-effect-bundle-quote` | 2 | 2 | 100.0% | 2 | 0 | 0 | 0 | 135s | 192s |
| `flask-yes-harness` | `hidden-effect-cart-validation` | 2 | 2 | 100.0% | 2 | 0 | 0 | 0 | 124s | 154s |
| `flask-yes-harness` | `hidden-effect-catalog-metrics` | 2 | 2 | 100.0% | 2 | 0 | 0 | 0 | 105s | 134s |
| `flask-yes-harness` | `hidden-effect-catalog-segments` | 2 | 2 | 100.0% | 2 | 0 | 0 | 0 | 116s | 116s |
| `flask-yes-harness` | `hidden-effect-pick-list` | 2 | 2 | 100.0% | 2 | 0 | 0 | 0 | 148s | 158s |
| `flask-yes-harness` | `hidden-effect-reservation-preview` | 2 | 2 | 100.0% | 2 | 0 | 0 | 0 | 124s | 170s |
| `flask-yes-harness` | `hidden-effect-stock-risk` | 2 | 2 | 100.0% | 2 | 0 | 0 | 0 | 100s | 106s |
| `flask-yes-harness` | `hidden-effect-supplier-readiness` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 134s | 134s |
| `flask-yes-harness` | `hidden-effect-tax-preview` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 135s | 135s |

## Boundary Check

No completed record had a wrong-file edit, forbidden-file edit, or timeout.
The observed split was functional hidden-contract discovery, not task-boundary
drift.

- `flask-no-harness`: 17 completed, 0 strict scored successes, 0 verification
  passes, 0 wrong-file edits, 0 forbidden-file edits, 0 timeouts
- `flask-yes-harness`: 18 completed, 18 strict scored successes, 18
  verification passes, 0 wrong-file edits, 0 forbidden-file edits, 0 timeouts

## Interpretation

This partial run gives useful calibration evidence but should be interpreted
narrowly. It shows that the current hidden Flask harnessed target can produce
repeatable hidden-contract passes while the bare target misses those contracts
under the current task shape.

It should not be read as a general comparison of agent coding ability. The
current design has strong information asymmetry: the `flask-yes-harness`
repository has hidden task by task API contracts in repository-local guidance,
while `flask-no-harness` does not. That makes this run closer to an upper-bound
test of contract-guidance value than a fair benchmark of how well the same
agent can infer an underspecified API from code alone.

Strict scored success and verification passed remain separate signals.
Verification passed measures functional hidden-oracle correctness. Strict
scored success also requires clean agent exit and file-boundary compliance.
Wrong-file edits measure task-boundary misses relative to `expected_files`,
not functional failure by themselves.

## Next Experiment

The next A/B should reduce the information asymmetry while preserving a real
harness signal.

- Give both sides the endpoint, HTTP method, and top-level response shape in
  the task prompt.
- Keep detailed business conventions, companion docs expectations, and local
  gate guidance only in the harnessed repository.
- Keep the deterministic hidden oracle in this runner repository.
- Keep `expected_files` and root `README.md` exclusion unchanged.
- Treat success, verification passed, wrong-file edits, forbidden-file edits,
  and timeouts as separate reported columns.

That middle-difficulty shape would measure whether repository-local harness
guidance improves convention-following after the basic API skeleton is no
longer hidden from the bare target.

## Raw Artifacts

Raw local artifacts are intentionally not committed:

- Results JSONL: `results/hidden-flask-ab-large-20260612T020437Z/2026-06-12.jsonl`
- Run directories: `runs/hidden-flask-ab-large-20260612T020437Z/`
