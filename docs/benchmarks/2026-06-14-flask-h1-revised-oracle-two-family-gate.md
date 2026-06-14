# Flask H1 Revised-Oracle Two-Family Gate - 2026-06-14

This was the revised-oracle H1 gate after fixing the replenishment glossary
oracle brittleness. It reran both direct decision-memory families across the
four non-bare arms for two repeats.

The gate completed all 16 records with zero stalls, zero timeouts, zero
wrong-file edits, and zero forbidden-file edits. Decision-bearing arms were
8/8 strict and record-consistent. Control arms were 0/8 strict and
0/8 record-consistent.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Tasks:
  - `hidden-effect-catalog-price-policy`
  - `hidden-effect-catalog-replenishment-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `workflow-only`, `decision-only`, `failure-only`, `full-harness`
- Repeats: 2
- Planned records: 16
- Completed records: 16
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 240`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Runner ref: `5d52476`
- Started: `2026-06-14T06:13:56Z`
- Finished: `2026-06-14T06:43:29Z`

Target refs:

| Arm | Source | Ref |
| --- | --- | --- |
| `workflow-only` | `../flask-workflow-only` | `1a79d8cf9e0799789b3da8029dbbb5a572b3133e` |
| `decision-only` | `../flask-decision-only` | `e9b0a3e919a7827497c7163912a1023c2346008f` |
| `failure-only` | `../flask-failure-only` | `18330ea23880b1ca7a647ea58b0d694e2c658fc8` |
| `full-harness` | `../flask-memory-harness` | `ba8b3963d071089429fa2c2c8ebc10049e80cca4` |

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-price-policy \
  --task-id hidden-effect-catalog-replenishment-policy \
  --arms workflow-only,decision-only,failure-only,full-harness \
  --repeats 2 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal \
  --execute
```

## Headline

| Arm | Completed | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `workflow-only` | 4 | 0 | 2 | 4 | 4 | 4 | 0/4 | 0 | 0 | 0 | 0 | 66s | 76s |
| `decision-only` | 4 | 4 | 4 | 4 | 4 | 4 | 4/4 | 0 | 0 | 0 | 0 | 55s | 69s |
| `failure-only` | 4 | 0 | 2 | 4 | 4 | 4 | 0/4 | 0 | 0 | 0 | 0 | 62s | 68s |
| `full-harness` | 4 | 4 | 4 | 4 | 4 | 4 | 4/4 | 0 | 0 | 0 | 0 | 58s | 406s |

Overall:

- Completed records: 16/16
- Strict successes: 8/16
- Decision-bearing strict successes: 8/8
- Control-arm strict successes: 0/8
- Record consistency: 8/16
- Decision-bearing record consistency: 8/8
- Control-arm record consistency: 0/8
- Stalls/timeouts: 0
- Preflight failures: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- No-edit watchdog records: 0

## Per-Task Results

| Arm | Task | Runs | Strict | Functional | Schema | Workflow | Record consistency |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `workflow-only` | `hidden-effect-catalog-price-policy` | 2 | 0 | 2 | 2 | 2 | 0/2 |
| `decision-only` | `hidden-effect-catalog-price-policy` | 2 | 2 | 2 | 2 | 2 | 2/2 |
| `failure-only` | `hidden-effect-catalog-price-policy` | 2 | 0 | 2 | 2 | 2 | 0/2 |
| `full-harness` | `hidden-effect-catalog-price-policy` | 2 | 2 | 2 | 2 | 2 | 2/2 |
| `workflow-only` | `hidden-effect-catalog-replenishment-policy` | 2 | 0 | 0 | 2 | 2 | 0/2 |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | 2 | 2 | 2 | 2 | 2 | 2/2 |
| `failure-only` | `hidden-effect-catalog-replenishment-policy` | 2 | 0 | 0 | 2 | 2 | 0/2 |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | 2 | 2 | 2 | 2 | 2 | 2/2 |

Control failures were expected and useful:

- Price-policy controls implemented functional/schema behavior but failed
  record consistency because the accepted price-band decision record was not
  present.
- Replenishment controls failed functional and record-consistency checks; their
  summaries did not count the adopted `reorder_now`, `monitor`, and `healthy`
  statuses, and the accepted replenishment decision record was not present.

## Watchdog Diagnostics

`scripts/summarize_hidden_ab.py` reported:

| Target | Watchdog records | No-edit watchdogs | No observed repo changes | p50 seconds to repo change | Max seconds without repo change | Max seconds since output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 4 | 0 | 0 | 36s | - | 0s |
| `failure-only` | 4 | 0 | 0 | 35s | - | 0s |
| `full-harness` | 4 | 0 | 0 | 30s | - | 0s |
| `workflow-only` | 4 | 0 | 0 | 37s | - | 0s |

`scripts/triage_no_edit_stalls.py` reported:

```text
## No-Edit Stall Triage

No-edit watchdog records: 0
```

The run had one notable duration tail:

- `20260614T062431Z-hidden-effect-catalog-replenishment-policy-2246a111`
  (`full-harness`) completed strict/pass but took 405.9s. First repository
  change was observed after 30.0s, so this was a return-time tail rather than a
  no-edit stall.

## Reading

What held:

- Both H1 task families separated decision-bearing arms from controls.
- `decision-only` and `full-harness` were both 4/4 strict and
  record-consistent.
- `workflow-only` and `failure-only` were both 0/4 record-consistent.
- The revised replenishment oracle did not create control false positives.
- There were no stalls, timeouts, hidden-access findings, wrong-file edits, or
  forbidden-file edits.

What remains:

- This is still a 16-record gate, not a promotion-sized stability run.
- A `full-harness` replenishment pass had a 405.9s duration tail.
- The direct H1 evidence now covers two catalog decision families, not all
  possible decision-memory uses.

## Decision

The H1 direct decision-memory claim is now much more defensible than it was
after the first two-family pilot.

A promotion-sized H1 run is now valuable if the claim is scoped narrowly:

> In this Flask catalog benchmark, accepted decision records help agents recover
> decision-consistent behavior that workflow-only and failure-only guidance do
> not recover.

Use a 96-record guarded promotion rather than an arbitrary 100-record run:

- Tasks: the two direct H1 families.
- Arms: `workflow-only`, `decision-only`, `failure-only`, `full-harness`.
- Repeats: 12.
- Planned records: 96.
- Keep `CODEX_PROMPT_GUARD=1`.
- Keep sequential execution and `--stop-on-abnormal`.
- Preserve timeout and no-edit watchdog reporting because duration-tail risk
  has not disappeared.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T061356Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T061356Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-h1-revised-oracle-two-family-gate.md`
