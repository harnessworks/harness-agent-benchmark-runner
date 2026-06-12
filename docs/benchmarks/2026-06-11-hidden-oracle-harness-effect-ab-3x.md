# Hidden-Oracle Harness-Effect Flask A/B - Codex CLI 3x

Date: 2026-06-11
Runner: this repository (`harness-agent-benchmark-runner`)
Agent: Codex CLI `0.138.0-alpha.7`
Adapter: `examples/agents/codex_exec_agent.py`

## Headline

| Target | Harness | Runs | Strict scored successes | Strict success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | No | 12 | 0 | 0% | 0 | 11 | 0 | 3 |
| `flask-yes-harness` | Yes | 12 | 11 | 91.7% | 11 | 0 | 0 | 0 |

This is the strongest Flask A/B evidence so far. The harnessed target improved
hidden contract discovery and strict boundary adherence. Verification passed
measures functional correctness; wrong-file edits measure whether changes stayed
inside the task boundary. Unlike the previous complex run, the task specs and
deterministic oracle live in this runner repository, not in the target clone.
The agent-visible target clone no longer contains the exact scoring contract.

## Targets

- Bare target: local `flask-no-harness` @ `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- Harnessed target: local `flask-yes-harness` @ `2aa110a37f1ed213470be41155c82b59ad06f549`

## Task Design

Four hidden-oracle task specs were added under
`benchmarks/tasks/flask-hidden/` in this runner. Their prompts are intentionally
vague and refer to repository conventions; the exact scoring oracle is
`benchmarks/oracles/flask_hidden_oracle.py`.

The historical 2026-06-11 run used prompt wording that asked for "related
project docs." That wording can reasonably be read as inviting root `README.md`
edits, so the README signal below is interpreted only as strict task-boundary
adherence. Current task specs tighten this before the large rerun by asking for
companion documentation in the repository's documented docs location and by
explicitly excluding root `README.md` unless a task asks for README changes.

| Task | Prompt-level instruction | Hidden oracle checks |
| --- | --- | --- |
| `hidden-effect-stock-risk` | Add the stock risk report API described by repository conventions. | `GET /inventory/risk-report`, stock risk bands, action labels, summary, metadata, and glossary terms. |
| `hidden-effect-supplier-readiness` | Add the supplier readiness API described by repository conventions. | `GET /suppliers/readiness`, supplier map, lead-time rules, summary, metadata, and decision record. |
| `hidden-effect-bundle-quote` | Add the bundle quote API described by repository conventions. | `POST /catalog/bundle-quote`, quantity validation, discount rate, money totals, metadata, and decision record. |
| `hidden-effect-reservation-preview` | Add the reservation preview API described by repository conventions. | `POST /inventory/reservations/preview`, safety stock, partial reservations, no mutation, metadata, and glossary terms. |

The yes-harness target documents these contracts in `AGENTS.md` and
`docs/conventions/coding.md`. The no-harness target does not.

## Controls

No-op baseline over the same four hidden tasks:

| Target | Runs | Strict scored successes | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | 4 | 0 | 0 | 0 | 0 | 0 |
| `flask-yes-harness` | 4 | 0 | 0 | 0 | 0 | 0 |

Both targets correctly rejected empty changes for all four hidden tasks.

## Run Conditions

- Repetitions: 3 per target/task pair
- Total live Codex records: 24
- Concurrency: 1, run sequentially
- Run order per round: task by task, no-harness then yes-harness
- Task attempts: `max_attempts=1`
- Effective agent timeout: 600 seconds
- Budget hint: `--max-cost-usd 1.0`
- Codex config override: `CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`
  (`medium` reasoning, `priority` service tier)

## Per-Task Results

| Target | Task | Strict scored successes | Verification passed | Wrong-file edits | Timeouts | Agent durations |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `flask-no-harness` | `hidden-effect-stock-risk` | 0/3 | 0/3 | 3 | 1 | 183s, 600s, 197s |
| `flask-no-harness` | `hidden-effect-supplier-readiness` | 0/3 | 0/3 | 2 | 1 | 112s, 140s, 600s |
| `flask-no-harness` | `hidden-effect-bundle-quote` | 0/3 | 0/3 | 3 | 0 | 162s, 166s, 198s |
| `flask-no-harness` | `hidden-effect-reservation-preview` | 0/3 | 0/3 | 3 | 1 | 192s, 166s, 600s |
| `flask-yes-harness` | `hidden-effect-stock-risk` | 3/3 | 3/3 | 0 | 0 | 102s, 91s, 94s |
| `flask-yes-harness` | `hidden-effect-supplier-readiness` | 3/3 | 3/3 | 0 | 0 | 103s, 103s, 96s |
| `flask-yes-harness` | `hidden-effect-bundle-quote` | 2/3 | 2/3 | 0 | 0 | 189s, 141s, 162s |
| `flask-yes-harness` | `hidden-effect-reservation-preview` | 3/3 | 3/3 | 0 | 0 | 136s, 164s, 159s |

## Failure Analysis

`flask-no-harness` failed every hidden task. Common causes:

- The agent guessed route names or response shapes that did not match the
  hidden contract, often producing Flask 404s for the oracle endpoint.
- The agent edited root `README.md` in 11/12 runs, outside this task suite's
  expected boundary of `app/**`, `tests/**`, and `docs/**`. This is a strict
  task-boundary miss, not a functional failure by itself and not a general
  judgment that README edits are bad. The prompt's "related project docs"
  wording may reasonably invite documentation work; the scored distinction is
  that this benchmark only allowed companion project docs under `docs/**`.
- Three no-harness runs timed out at 600 seconds.

`flask-yes-harness` had one failure:

- `hidden-effect-bundle-quote`, round 3: the agent implemented the feature in
  the expected files, but wrote an incorrect local pytest expectation for a
  money total (`52.87` instead of the implementation's rounded `52.88`). The
  harness gate failed before the hidden oracle could complete. There were no
  wrong-file edits, forbidden-file edits, or timeouts.

## Interpretation

This run directly addresses the oracle-leakage issue from the previous complex
A/B. With the exact scoring contract hidden outside the target clone, the
bare target fell to 0/12 while the harnessed target reached 11/12.

The measured harness effect is strongest in three dimensions:

- contract discovery: yes-harness found repository-specific route names,
  thresholds, supplier maps, discount rules, and safety-stock semantics
- strict task-boundary adherence: yes-harness had 0 wrong-file edits vs 11 in
  no-harness, where the no-harness misses were root `README.md` edits outside
  this task suite's allowed `docs/**` companion-document path
- timeout behavior: yes-harness had 0 timeouts vs 3 in no-harness

Scope still matters. This proves a meaningful effect for tasks where success
depends on repository-local conventions and durable project knowledge. It does
not claim the harness improves generic Flask coding tasks where the prompt
fully specifies the desired behavior.

## Raw Artifacts

Raw local records are intentionally not committed:

- No-op baseline: `results/hidden-noop-v2-20260611T090611Z/2026-06-11.jsonl`
- Codex A/B: `results/hidden-codex-ab-3x-v3-20260611T092514Z/2026-06-11.jsonl`
- Run directories: `runs/hidden-noop-v2-20260611T090611Z/` and
  `runs/hidden-codex-ab-3x-v3-20260611T092514Z/`
