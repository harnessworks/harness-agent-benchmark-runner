# Flask Full-Harness Memory Pilot 1x - 2026-06-14

This was a one-repeat operational pilot for the five-arm full-harness memory
suite. It is evidence that the suite runs end to end and that the new scoring
dimensions are recorded, not a representative benchmark result.

The run completed all 25 planned records with 0 stalls, 0 timeouts,
0 hidden-access findings, 0 preflight failures, and 0 forbidden-file edits.
There was 1 wrong-file edit in the `bare` arm.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `bare`, `workflow-only`, `decision-only`, `failure-only`,
  `full-harness`
- Task groups: 5
- Repeats: 1
- Planned records: 25
- Completed records: 25
- Concurrency: `--jobs 1`
- Stop-on-abnormal: disabled
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Codex model/config: `gpt-5.5`,
  `model_reasoning_effort=medium`, `service_tier=priority`
- Runner ref: `9002bd4b876be9a2b8be59f74219ea81568bc72d`
- Started: `2026-06-13T15:09:04Z`
- Finished: `2026-06-13T15:54:01Z`

Target refs:

- `bare`: `../flask-no-harness` at
  `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- `workflow-only`: `../flask-workflow-only` at
  `1a79d8cf9e0799789b3da8029dbbb5a572b3133e`
- `decision-only`: `../flask-decision-only` at
  `12284d76e6bddab685e347a0ab9af5814fe72e61`
- `failure-only`: `../flask-failure-only` at
  `18330ea23880b1ca7a647ea58b0d694e2c658fc8`
- `full-harness`: `../flask-memory-harness` at
  `bd1a0f4cda36144fc07d0293117dc9ba3d35ab75`

Command:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --repeats 1 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 360 \
  --execute
```

## Headline

| Arm | Runs | Strict | Functional | Schema | Workflow | Boundary | Record consistency | Mistake prevention | Repeated documented mistakes | Wrong-file edits | Forbidden-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 5 | 0 | 0 | 0 | 4 | 4 | 0/1 | 0/4 | 4 | 1 | 0 | 68s | 88s |
| `workflow-only` | 5 | 2 | 2 | 5 | 5 | 5 | 0/1 | 4/4 | 0 | 0 | 0 | 55s | 60s |
| `decision-only` | 5 | 2 | 2 | 5 | 5 | 5 | 0/1 | 4/4 | 0 | 0 | 0 | 64s | 77s |
| `failure-only` | 5 | 2 | 2 | 5 | 5 | 5 | 0/1 | 4/4 | 0 | 0 | 0 | 56s | 363s |
| `full-harness` | 5 | 2 | 2 | 5 | 5 | 5 | 0/1 | 4/4 | 0 | 0 | 0 | 62s | 550s |

Overall strict success was 8/25. All non-bare arms tied at 2/5 strict
successes. The `bare` arm was 0/5 strict and 0/5 schema.

## Per-Task Strict Results

Each cell is one record.

| Task | `bare` | `workflow-only` | `decision-only` | `failure-only` | `full-harness` | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `hidden-effect-availability-badge` | 0 | 0 | 0 | 0 | 0 | All arms missed hidden missing-SKU behavior. |
| `hidden-effect-catalog-price-policy` | 0 | 0 | 0 | 0 | 0 | H1 record-consistency task produced no positive signal. |
| `hidden-effect-catalog-metrics` | 0 | 0 | 0 | 0 | 0 | All arms missed part of the hidden metrics contract. |
| `hidden-effect-catalog-segments` | 0 | 1 | 1 | 1 | 1 | All harnessed arms passed; `bare` missed docs/meta conventions. |
| `hidden-effect-replenishment-signals` | 0 | 1 | 1 | 1 | 1 | All harnessed arms passed; `bare` missed docs/meta conventions. |

## H1: Direct Decision-Memory Claim

H1 was represented by `hidden-effect-catalog-price-policy`, whose oracle tagged
`record_consistency`.

Result: 0/5 record-consistency successes.

- `bare`: 0/1, expected negative control.
- `workflow-only`: 0/1, expected no direct decision record.
- `decision-only`: 0/1.
- `failure-only`: 0/1, expected no direct decision record.
- `full-harness`: 0/1.

This pilot does not support the direct decision-memory claim. The decision
arms did not convert the existing price-band decision record into a hidden
oracle pass on this task. Before scaling H1, triage the task and oracle around
the price-policy summary expectation and the record-consistency command
tagging.

Post-run triage found one brittle oracle condition in this H1 result: the
original functional check rejected `summary.price_bands`, even though the
prompt only required a compact summary with counts by price band and existing
catalog segment conventions use nested band-count objects. The oracle was
updated after this run to accept `summary.price_bands` and to add a hidden
37.00 price edge case for the adopted 35.00 decision threshold.

Replaying the revised oracle against the saved H1 worktrees gives this
classification:

- `bare`: functional still fails because no domain glossary exists;
  record-consistency still fails because no decision record exists.
- `workflow-only`: functional passes; record-consistency fails because no
  decision record exists.
- `decision-only`: functional passes; record-consistency passes.
- `failure-only`: functional passes; record-consistency fails because no
  decision record exists.
- `full-harness`: functional passes; record-consistency fails because the
  implementation used a 40.00 threshold, and the hidden 37.00 edge must be
  `premium` under the decision record.

Do not compare the original H1 row from this report directly with future H1
runs unless this oracle revision is called out.

## H2: Mistake-Prevention Signal

H2 was represented by schema oracles tagged `mistake_prevention` on the four
non-H1 convention-transfer tasks.

Result:

- `bare`: 0/4 mistake-prevention successes and 4 repeated documented mistakes.
- Every non-bare arm: 4/4 mistake-prevention successes and 0 repeated
  documented mistakes.

This supports a narrow H2 reading: repository workflow/memory scaffolding
prevented repeated schema/documentation mistakes relative to `bare`. It does
not separate `workflow-only`, `decision-only`, `failure-only`, and
`full-harness`, because all non-bare arms tied.

## Failure Notes

- `availability-badge`: all arms failed hidden behavior for missing SKU
  handling; `bare` also missed the metadata envelope.
- `catalog-metrics`: all arms failed a hidden metrics detail or documentation
  expectation; non-bare arms still preserved schema/workflow dimensions.
- `catalog-price-policy`: all arms failed; this is the main H1 triage target.
- `catalog-segments` and `replenishment-signals`: all non-bare arms passed
  strict scoring while `bare` failed docs/meta conventions.
- Wrong-file edit: the only boundary issue was `docs/` in the `bare`
  `catalog-price-policy` record.

## Duration

Agent duration summary across all 25 records:

- Min: 44.463s
- Mean: 93.3s
- Median: 61.7s
- p95: 363.175s using nearest-rank calculation across all records
- Max: 550.207s
- Sum: 2331.9s

The two long-tail records were both `catalog-segments`:

- `full-harness`: 550.207s
- `failure-only`: 363.175s

Neither record timed out or stalled, but the full-harness duration tail should
be watched before promotion.

## Interpretation

Use this as a pilot-readiness result:

- The five-arm suite completed cleanly from an operations perspective.
- The new `record_consistency` and `mistake_prevention` dimensions were
  recorded and can be summarized.
- The original H1 score was not supported by a clean oracle; post-run triage
  fixed a brittle summary-shape check and added a hidden threshold edge.
- H2 has a clear `bare` versus non-bare signal, but not a memory-layer
  separation inside the non-bare arms.
- The next useful step is a small multi-repeat rerun under the revised H1
  oracle, not a direct promotion from this 1x result.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260613T150904Z/2026-06-13.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260613T150904Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-full-harness-memory-pilot-1x.md`
