# Harness-Effect Flask A/B - Codex CLI 3x

Date: 2026-06-11
Runner: this repository (`harness-agent-benchmark-runner`)
Agent: Codex CLI `0.138.0-alpha.7`
Adapter: `examples/agents/codex_exec_agent.py`

## Headline

| Target | Harness | Runs | Successes | Success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | No | 6 | 4 | 66.7% | 5 | 1 | 0 | 1 |
| `flask-yes-harness` | Yes | 6 | 6 | 100% | 6 | 0 | 0 | 0 |

This run intentionally measures tasks where harness guidance should matter:
the prompt names a repository-specific API but does not restate the detailed
response contract or companion-document requirements. The harnessed target
documents those details in `AGENTS.md` and `docs/conventions/coding.md`; the
bare target does not.

## Targets

- Bare target: local `flask-no-harness` @ `d7589538c35a601e61621ed3dba9151ec63b0b51`
- Harnessed target: local `flask-yes-harness` @ `f5856f3a63a00c36888be807ec203ebd63654a1b`

## Task design

Two task specs were added to both targets:

| Task | Prompt-level instruction | Oracle checks |
| --- | --- | --- |
| `harness-effect-product-detail` | Add the product detail API described by repository conventions. | `GET /products/<sku>` response shape, 404 `product_not_found`, tests, and a decision record mentioning `GET /products/<sku>`, `API response shape`, `product_not_found`, and `catalog lookup endpoint`. |
| `harness-effect-inventory-summary` | Add the inventory summary API described by repository conventions. | `GET /inventory/summary` response shape, low-stock threshold `5`, tests, and glossary documentation for the inventory summary endpoint and threshold. |

The same functional oracle is used in both targets. The difference is that
`flask-yes-harness` has explicit repository guidance for these contracts, while
`flask-no-harness` only has the vague task prompt and the existing app.

## Controls

No-op baseline:

| Target | Runs | Successes | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | 2 | 0 | 0 | 0 | 0 | 0 |
| `flask-yes-harness` | 2 | 0 | 0 | 0 | 0 | 0 |

Both targets correctly rejected empty changes for both harness-effect tasks.

## Run conditions

- Repetitions: 3 per target/task pair
- Total live Codex records: 12
- Concurrency: 1, run sequentially to reduce concurrency timeout pressure
- Run order per round: no-harness product detail, no-harness inventory summary,
  yes-harness product detail, yes-harness inventory summary
- Task attempts: `max_attempts=1`
- Effective agent timeout: 600 seconds, from task spec `timeout_seconds`
- Budget hint: `--max-cost-usd 1.0`
- Codex defaults: no `CODEX_MODEL`, `CODEX_PROFILE`, or `CODEX_EXEC_ARGS`
  override was set

## Per-task results

| Target | Task | Successes | Verification passed | Wrong-file edits | Timeouts | Agent durations |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `flask-no-harness` | `harness-effect-product-detail` | 2/3 | 3/3 | 1 | 0 | 258s, 175s, 167s |
| `flask-no-harness` | `harness-effect-inventory-summary` | 2/3 | 2/3 | 0 | 1 | 137s, 142s, 600s |
| `flask-yes-harness` | `harness-effect-product-detail` | 3/3 | 3/3 | 0 | 0 | 159s, 159s, 191s |
| `flask-yes-harness` | `harness-effect-inventory-summary` | 3/3 | 3/3 | 0 | 0 | 160s, 160s, 182s |

## Failure analysis

`flask-no-harness` had two failures:

- `harness-effect-product-detail`, round 1: deterministic oracle passed, but
  the agent also edited `README.md`, which is outside the task's expected file
  boundary of `app/**`, `tests/**`, and `docs/**`.
- `harness-effect-inventory-summary`, round 3: agent timed out at 600 seconds
  with no changed files. Verification then failed because
  `GET /inventory/summary` still returned Flask's default 404.

`flask-yes-harness` had no failures, no wrong-file edits, no forbidden-file
edits, and no timeouts. Its product-detail runs consistently wrote decision
records under `docs/decisions/`, and its inventory-summary runs updated
`docs/domain/glossary.md`, matching the harness guidance.

## Interpretation

This is the first local A/B evidence showing a measurable harness effect in
this Flask setup. The effect appears in exactly the intended dimensions:

- better success rate: 100% vs 66.7%
- fewer boundary misses: 0 vs 1 wrong-file edit
- fewer timeouts: 0 vs 1
- same deterministic task oracles, with yes-harness giving agents discoverable
  repository guidance instead of restating the full contract in the prompt

Scope matters: this does not prove harness improves all Flask coding tasks. It
shows harness helps when the benchmark requires repository-specific convention
discovery, companion documentation, and file-boundary discipline.

## Raw artifacts

Raw local records are intentionally not committed:

- No-op baseline: `results/harness-effect-noop-20260611T063257Z/2026-06-11.jsonl`
- Codex A/B: `results/harness-effect-codex-ab-1x-20260611T063332Z/2026-06-11.jsonl`
  contains all 12 records. The directory name came from the initial 1x pilot
  and was reused when the run was extended to 3x.
- Run directories: `runs/harness-effect-noop-20260611T063257Z/` and
  `runs/harness-effect-codex-ab-1x-20260611T063332Z/`
