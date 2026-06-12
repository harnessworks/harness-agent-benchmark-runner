# Hidden Flask A/B Calibration - Codex CLI 1x

Date: 2026-06-12
Runner: this repository (`harness-agent-benchmark-runner`) @ `49825c7612f17ed9440c4b978dfb697a83acb899`
Agent: Codex CLI through `examples/agents/codex_exec_agent.py`
Run ID: `hidden-flask-ab-large-20260612T005420Z`

## Headline

| Target | Runs | Strict scored successes | Strict success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | 10 | 0 | 0.0% | 0 | 0 | 0 | 0 | 169s | 256s |
| `flask-yes-harness` | 10 | 10 | 100.0% | 10 | 0 | 0 | 0 | 118s | 184s |

This 20-record run was a pre-large calibration after tightening the hidden Flask
task prompts. It is not the representative 200-run evidence run. It verifies
that the prompt ambiguity around root `README.md` edits was removed before the
larger run.

## Targets

- Bare target: local `flask-no-harness` @ `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- Harnessed target: local `flask-yes-harness` @ `c3eaf9a0105d7b99db414467b5df0edb833697ad`

Both target repositories were clean before the run.

## Run Conditions

- Command: `python3 scripts/run_hidden_flask_ab.py --mode large --repeats 1 --execute`
- Task pairs: 10 hidden Flask A/B pairs
- Repetitions: 1 per target/task pair
- Total live Codex records: 20
- Pair order: `alternate`
- Task attempts: `max_attempts=1`
- Effective runner cap: `--max-agent-timeout 900`
- Budget hint: `--max-cost-usd 1.0`
- Codex config override: `CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`

## Per-Task Results

| Target | Task | Runs | Strict scored successes | Strict success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | `hidden-effect-availability-badge` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 156s | 156s |
| `flask-no-harness` | `hidden-effect-bundle-quote` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 175s | 175s |
| `flask-no-harness` | `hidden-effect-cart-validation` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 159s | 159s |
| `flask-no-harness` | `hidden-effect-catalog-metrics` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 192s | 192s |
| `flask-no-harness` | `hidden-effect-catalog-segments` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 134s | 134s |
| `flask-no-harness` | `hidden-effect-pick-list` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 190s | 190s |
| `flask-no-harness` | `hidden-effect-reservation-preview` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 169s | 169s |
| `flask-no-harness` | `hidden-effect-stock-risk` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 145s | 145s |
| `flask-no-harness` | `hidden-effect-supplier-readiness` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 203s | 203s |
| `flask-no-harness` | `hidden-effect-tax-preview` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 256s | 256s |
| `flask-yes-harness` | `hidden-effect-availability-badge` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 123s | 123s |
| `flask-yes-harness` | `hidden-effect-bundle-quote` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 150s | 150s |
| `flask-yes-harness` | `hidden-effect-cart-validation` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 184s | 184s |
| `flask-yes-harness` | `hidden-effect-catalog-metrics` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 118s | 118s |
| `flask-yes-harness` | `hidden-effect-catalog-segments` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 77s | 77s |
| `flask-yes-harness` | `hidden-effect-pick-list` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 118s | 118s |
| `flask-yes-harness` | `hidden-effect-reservation-preview` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 117s | 117s |
| `flask-yes-harness` | `hidden-effect-stock-risk` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 90s | 90s |
| `flask-yes-harness` | `hidden-effect-supplier-readiness` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 134s | 134s |
| `flask-yes-harness` | `hidden-effect-tax-preview` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 122s | 122s |

## Boundary Check

The calibration directly tested the prompt change that now says companion
documentation belongs in the repository's documented docs location and that
root `README.md` should not be changed unless requested.

- Root `README.md` changed: 0 records
- Wrong-file edits: 0 records
- Forbidden-file edits: 0 records
- Timeouts: 0 records

The no-harness failures were functional hidden-contract misses, not strict
boundary misses.

## Failure Analysis

`flask-no-harness` failed all ten tasks. The observed failure modes were route
mismatches, response-shape mismatches, and business-rule mismatches:

| Task | Failure signal |
| --- | --- |
| `hidden-effect-availability-badge` | Hidden oracle reached Flask 404 for the expected endpoint. |
| `hidden-effect-bundle-quote` | Hidden oracle expected HTTP 200 but received `invalid_items`. |
| `hidden-effect-cart-validation` | Cart validation rows were wrong. |
| `hidden-effect-catalog-metrics` | `highest_stock_sku` was wrong. |
| `hidden-effect-catalog-segments` | Catalog segment rows were wrong. |
| `hidden-effect-pick-list` | Response did not return the required picks list. |
| `hidden-effect-reservation-preview` | Hidden oracle reached Flask 404 for the expected endpoint. |
| `hidden-effect-stock-risk` | Hidden oracle reached Flask 404 for the expected endpoint. |
| `hidden-effect-supplier-readiness` | Supplier readiness rows were wrong. |
| `hidden-effect-tax-preview` | Hidden oracle reached Flask 404 for the expected endpoint. |

`flask-yes-harness` passed all ten hidden contracts and stayed inside the task
boundary.

## Interpretation

The calibration supports proceeding to the representative 200-run large A/B.
It confirms three preconditions:

- the ten-task hidden Flask suite executes end to end
- prompt ambiguity around root `README.md` edits no longer creates boundary
  noise
- strict scored success and verification passed remain clearly separated

This should still be treated as calibration evidence only. The next publishable
large evidence run should use `--mode large --execute` with the default 10
repeats.

## Raw Artifacts

Raw local records are intentionally not committed:

- Results JSONL: `results/hidden-flask-ab-large-20260612T005420Z/2026-06-12.jsonl`
- Run directories: `runs/hidden-flask-ab-large-20260612T005420Z/`
