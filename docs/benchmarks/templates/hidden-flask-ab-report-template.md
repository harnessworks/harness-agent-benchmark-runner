# Hidden-Oracle Flask Harness A/B - Report Template

Date: YYYY-MM-DD
Runner: `harness-agent-benchmark-runner` @ `<runner-ref>`
Agent: Codex CLI `<version>`
Adapter: `examples/agents/codex_exec_agent.py`

## Headline

| Target | Harness | Runs | Successes | Success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | No |  |  |  |  |  |  |  |  |  |
| `flask-yes-harness` | Yes |  |  |  |  |  |  |  |  |  |

One-sentence headline:
`flask-yes-harness` reached `<x>/<n>` successes versus `<y>/<n>` for
`flask-no-harness` under the same hidden-oracle tasks and Codex settings.

## Scope

- Benchmark type: hidden-oracle harness A/B
- Measured scope: Flask API tasks where success depends on repository-local
  conventions and durable project guidance
- Not measured: cross-framework harness effectiveness, generic Flask coding
  ability, retry recovery, or multi-model performance

## Targets

- A, no harness: `flask-no-harness` @ `<commit>`
- B, yes harness: `flask-yes-harness` @ `<commit>`
- Target repository cleanliness: `<clean/dirty with reason>`

## Run Conditions

- Run command: `python3 scripts/run_hidden_flask_ab.py --mode <pilot|large> ...`
- Repetitions: `<repeats>` per target/task pair
- Task pairs: `<count>`
- Total records: `<count * repeats * 2>`
- Pair order: `<ab|ba|alternate>`
- Concurrency: `1`, unless explicitly documented otherwise
- Task attempts: `max_attempts=1`
- Effective agent timeout: `<seconds>`
- Budget hint: `<amount>`
- Codex model: `gpt-5.5`
- Codex config override:
  `CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`

## Task Design

| Task | Prompt-level instruction | Hidden oracle checks | Difficulty |
| --- | --- | --- | --- |
| `hidden-effect-availability-badge` |  |  |  |
| `hidden-effect-cart-validation` |  |  |  |
| `hidden-effect-catalog-metrics` |  |  |  |
| `hidden-effect-catalog-segments` |  |  |  |
| `hidden-effect-stock-risk` |  |  |  |
| `hidden-effect-supplier-readiness` |  |  |  |
| `hidden-effect-bundle-quote` |  |  |  |
| `hidden-effect-pick-list` |  |  |  |
| `hidden-effect-reservation-preview` |  |  |  |
| `hidden-effect-tax-preview` |  |  |  |

Design notes:

- A/B prompts are identical.
- The exact scoring contract is outside the target clone.
- The yes-harness target may expose repository conventions through harness
  guidance; the no-harness target must infer them from the bare codebase.
- The task is invalid if the prompt states the full hidden oracle contract.

## No-Op Control

| Target | Runs | Successes | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` |  |  |  |  |  |  |
| `flask-yes-harness` |  |  |  |  |  |  |

Expected result: both targets reject empty work for every hidden task.

## Per-Task Results

| Target | Task | Runs | Successes | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | `hidden-effect-availability-badge` |  |  |  |  |  |  |  |  |
| `flask-no-harness` | `hidden-effect-cart-validation` |  |  |  |  |  |  |  |  |
| `flask-no-harness` | `hidden-effect-catalog-metrics` |  |  |  |  |  |  |  |  |
| `flask-no-harness` | `hidden-effect-catalog-segments` |  |  |  |  |  |  |  |  |
| `flask-no-harness` | `hidden-effect-stock-risk` |  |  |  |  |  |  |  |  |
| `flask-no-harness` | `hidden-effect-supplier-readiness` |  |  |  |  |  |  |  |  |
| `flask-no-harness` | `hidden-effect-bundle-quote` |  |  |  |  |  |  |  |  |
| `flask-no-harness` | `hidden-effect-pick-list` |  |  |  |  |  |  |  |  |
| `flask-no-harness` | `hidden-effect-reservation-preview` |  |  |  |  |  |  |  |  |
| `flask-no-harness` | `hidden-effect-tax-preview` |  |  |  |  |  |  |  |  |
| `flask-yes-harness` | `hidden-effect-availability-badge` |  |  |  |  |  |  |  |  |
| `flask-yes-harness` | `hidden-effect-cart-validation` |  |  |  |  |  |  |  |  |
| `flask-yes-harness` | `hidden-effect-catalog-metrics` |  |  |  |  |  |  |  |  |
| `flask-yes-harness` | `hidden-effect-catalog-segments` |  |  |  |  |  |  |  |  |
| `flask-yes-harness` | `hidden-effect-stock-risk` |  |  |  |  |  |  |  |  |
| `flask-yes-harness` | `hidden-effect-supplier-readiness` |  |  |  |  |  |  |  |  |
| `flask-yes-harness` | `hidden-effect-bundle-quote` |  |  |  |  |  |  |  |  |
| `flask-yes-harness` | `hidden-effect-pick-list` |  |  |  |  |  |  |  |  |
| `flask-yes-harness` | `hidden-effect-reservation-preview` |  |  |  |  |  |  |  |  |
| `flask-yes-harness` | `hidden-effect-tax-preview` |  |  |  |  |  |  |  |  |

## Failure Taxonomy

| Cause | `flask-no-harness` | `flask-yes-harness` | Notes |
| --- | ---: | ---: | --- |
| Route mismatch |  |  |  |
| Response shape mismatch |  |  |  |
| Business rule mismatch |  |  |  |
| Missing required docs |  |  |  |
| Wrong-file edit |  |  |  |
| Forbidden-file edit |  |  |  |
| Timeout |  |  |  |
| Brittle oracle |  |  | Mark separately from genuine task failure. |

## Interpretation

State only claims supported by this measured scope. Do not generalize beyond
Flask hidden-oracle API tasks unless another target repository has also been
measured with the same discipline.

## Raw Artifacts

Raw local records are intentionally not committed.

- Results JSONL: `results/<run-id>/<date>.jsonl`
- Run directories: `runs/<run-id>/`
- Public-safe report: `docs/benchmarks/<date>-hidden-flask-ab-<shape>.md`
