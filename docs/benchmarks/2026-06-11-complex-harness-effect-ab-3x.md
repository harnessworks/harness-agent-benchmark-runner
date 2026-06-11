# Complex Harness-Effect Flask A/B - Codex CLI 3x

Date: 2026-06-11
Runner: this repository (`harness-agent-benchmark-runner`)
Agent: Codex CLI `0.138.0-alpha.7`
Adapter: `examples/agents/codex_exec_agent.py`

## Headline

| Target | Harness | Runs | Successes | Success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | No | 12 | 10 | 83.3% | 12 | 2 | 0 | 0 |
| `flask-yes-harness` | Yes | 12 | 11 | 91.7% | 11 | 0 | 0 | 1 |

This larger complex-task run gives a narrower but still useful harness-positive
signal. The harnessed target avoided wrong-file edits, while the bare target
twice edited `README.md` outside the task boundary. Functional verification was
not a strong separator in this run because the deterministic oracle files were
present in the target repositories and could be read by the agent.

## Targets

- Bare target: local `flask-no-harness` @ `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- Harnessed target: local `flask-yes-harness` @ `62f7c4d5835a20e19f7817dcc99162fa0acf527f`

## Task Design

Four more complex harness-effect task specs were added to both targets:

| Task | Prompt-level instruction | Oracle checks |
| --- | --- | --- |
| `harness-effect-catalog-search` | Add the catalog search API described by repository conventions. | `GET /catalog/search`, query/filter/sort behavior, metadata shape, invalid sort handling, and glossary documentation. |
| `harness-effect-reorder-plan` | Add the reorder plan API described by repository conventions. | `GET /inventory/reorder-plan`, threshold `10`, target stock `25`, recommendation shape, decision record, and glossary documentation. |
| `harness-effect-price-preview` | Add the price preview API described by repository conventions. | `POST /catalog/price-preview`, preview-only behavior, money deltas, error codes, and decision record. |
| `harness-effect-catalog-audit` | Add the catalog audit API described by repository conventions. | `GET /catalog/audit`, three data-quality checks, warning summary, decision record, and glossary documentation. |

The yes-harness target documents the contracts in `AGENTS.md` and
`docs/conventions/coding.md`. The no-harness target has the same task specs and
oracles but no harness guidance.

## Controls

No-op baseline over the same four complex tasks:

| Target | Runs | Successes | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | 4 | 0 | 0 | 0 | 0 | 0 |
| `flask-yes-harness` | 4 | 0 | 0 | 0 | 0 | 0 |

Both targets correctly rejected empty changes for all four complex tasks.

## Run Conditions

- Repetitions: 3 per target/task pair
- Total live Codex records: 24
- Concurrency: 1, run sequentially
- Run order per round: task by task, no-harness then yes-harness
- Task attempts: `max_attempts=1`
- Effective agent timeout: 600 seconds
- Budget hint: `--max-cost-usd 1.0`
- Codex config override: `CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`

## Per-Task Results

| Target | Task | Successes | Verification passed | Wrong-file edits | Timeouts | Agent durations |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `flask-no-harness` | `harness-effect-catalog-search` | 3/3 | 3/3 | 0 | 0 | 136s, 137s, 138s |
| `flask-no-harness` | `harness-effect-reorder-plan` | 3/3 | 3/3 | 0 | 0 | 107s, 106s, 100s |
| `flask-no-harness` | `harness-effect-price-preview` | 2/3 | 3/3 | 1 | 0 | 137s, 140s, 134s |
| `flask-no-harness` | `harness-effect-catalog-audit` | 2/3 | 3/3 | 1 | 0 | 111s, 139s, 122s |
| `flask-yes-harness` | `harness-effect-catalog-search` | 3/3 | 3/3 | 0 | 0 | 150s, 134s, 141s |
| `flask-yes-harness` | `harness-effect-reorder-plan` | 3/3 | 3/3 | 0 | 0 | 124s, 147s, 158s |
| `flask-yes-harness` | `harness-effect-price-preview` | 3/3 | 3/3 | 0 | 0 | 159s, 166s, 164s |
| `flask-yes-harness` | `harness-effect-catalog-audit` | 2/3 | 2/3 | 0 | 1 | 136s, 174s, 600s |

## Failure Analysis

`flask-no-harness` had two scored failures. In both cases deterministic
verification passed, but the agent also edited `README.md`, which is outside
the expected task boundary of `app/**`, `tests/**`, and `docs/**`:

- `harness-effect-catalog-audit`, round 1
- `harness-effect-price-preview`, round 3

`flask-yes-harness` had one scored failure:

- `harness-effect-catalog-audit`, round 3: the agent timed out at 600 seconds.
  The harness gate passed, but the focused oracle failed because no decision
  record mentioned `GET /catalog/audit`.

There were no forbidden-file edits in either target.

## Interpretation

This run is positive for harness boundary discipline but weak for functional
lift. The harnessed target scored 11/12 vs 10/12 and had 0 wrong-file edits vs
2. However, the bare target passed all deterministic verification commands.

The main methodology lesson is that visible target-local oracles reduce the
ability to measure harness guidance. Because `benchmarks/oracles/check_task.py`
is present in the cloned target, a capable agent can read the exact response
shape and documentation expectations even in `flask-no-harness`. That makes the
run useful for boundary discipline, but not a clean measure of whether
`AGENTS.md` and `docs/conventions/coding.md` improved contract discovery.

The next stronger A/B design should keep deterministic scoring outside the
agent-visible target clone. The runner can still execute an external
verification command after the agent finishes, while the task prompt remains
vague and only the yes-harness target contains the convention contract.

## Raw Artifacts

Raw local records are intentionally not committed:

- No-op baseline: `results/complex-noop-full-20260611T074231Z/2026-06-11.jsonl`
- Codex A/B: `results/complex-codex-ab-3x-20260611T074406Z/2026-06-11.jsonl`
- Run directories: `runs/complex-noop-full-20260611T074231Z/` and
  `runs/complex-codex-ab-3x-20260611T074406Z/`
