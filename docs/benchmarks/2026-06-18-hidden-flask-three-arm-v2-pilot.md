# Hidden Flask Three-Arm V2 Pilot - 2026-06-18

This pilot closes the first full v2 held-out three-arm check after the earlier
single-task v2 smoke. It ran three partial-realistic tasks across `bare`,
`workflow-only`, and `memory-harness`.

The final scoring run completed all 9 planned records with no operational
abnormal signals: 0 stalls, 0 timeouts, 0 hidden-access findings, 0 wrong-file
edits, and 0 forbidden-file edits.

## Run Conditions

- Suite: `benchmarks/suites/flask-hidden-three-arm-v2.json`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Tasks:
  - `hidden-effect-replenishment-signals`
  - `hidden-effect-catalog-price-ladder`
  - `hidden-effect-catalog-value-snapshot`
- Arms: `bare`, `workflow-only`, `memory-harness`
- Repeats: 1
- Planned records: 9
- Completed records: 9
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 180`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Model: `gpt-5.5`
- Service tier: `priority`
- Started: `2026-06-18T06:11:27Z`
- Finished: `2026-06-18T06:20:58Z`

Target refs:

| Arm | Source | Ref |
| --- | --- | --- |
| `bare` | `../flask-no-harness` | `b5351eae78ed9f17d46a43eee05354e9e13f6b94` |
| `workflow-only` | `../flask-yes-harness` | `3b3b5c5a295b0b025ea3519debaddfbed09c2ecd` |
| `memory-harness` | `../flask-memory-harness` | `00e3d5170bde7e5451f525f5ac011f16b6df2edb` |

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-three-arm-v2.json \
  --mode pilot \
  --task-limit 3 \
  --repeats 1 \
  --stop-on-abnormal \
  --agent-timeout-override 900 \
  --agent-no-edit-timeout 360 \
  --agent-idle-timeout 180 \
  --execute
```

## Headline

| Target | Runs | Strict | Functional | Schema contract | Workflow | Boundary | Verification passed | Wrong-file edits | Forbidden-file edits | Stalls | Timeouts | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 3 | 0 | 0 | 0 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 52s | 53s |
| `workflow-only` | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 53s | 54s |
| `memory-harness` | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 59s | 75s |

The runner printed `Completed schedule with 3 non-zero runner exits`. Those
three non-zero exits are the expected `bare` benchmark failures, not runner
abnormal events.

## Per-Task Results

| Target | Task | Strict | Functional | Schema contract | Workflow | Boundary | Duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | `hidden-effect-replenishment-signals` | 0 | 0 | 0 | 1 | 1 | 52s |
| `workflow-only` | `hidden-effect-replenishment-signals` | 1 | 1 | 1 | 1 | 1 | 48s |
| `memory-harness` | `hidden-effect-replenishment-signals` | 1 | 1 | 1 | 1 | 1 | 56s |
| `bare` | `hidden-effect-catalog-price-ladder` | 0 | 0 | 0 | 1 | 1 | 53s |
| `workflow-only` | `hidden-effect-catalog-price-ladder` | 1 | 1 | 1 | 1 | 1 | 53s |
| `memory-harness` | `hidden-effect-catalog-price-ladder` | 1 | 1 | 1 | 1 | 1 | 75s |
| `bare` | `hidden-effect-catalog-value-snapshot` | 0 | 0 | 0 | 1 | 1 | 47s |
| `workflow-only` | `hidden-effect-catalog-value-snapshot` | 1 | 1 | 1 | 1 | 1 | 54s |
| `memory-harness` | `hidden-effect-catalog-value-snapshot` | 1 | 1 | 1 | 1 | 1 | 59s |

## Failure Cluster

All `bare` records failed functional and schema checks while keeping workflow and
boundary signals clean:

- `hidden-effect-replenishment-signals`: no domain glossary, and response schema
  lacked the expected metadata envelope.
- `hidden-effect-catalog-price-ladder`: no domain glossary, and response shape
  did not follow the schema conventions expected by the hidden oracle.
- `hidden-effect-catalog-value-snapshot`: no domain glossary, and response
  schema lacked the expected metadata envelope.

This is the intended v2 negative-control pattern: the prompts provide endpoint
and business-rule requirements, while the harnessed repos carry API-envelope,
docs-location, metadata, and local-gate conventions.

## Calibration Notes

Two earlier same-day calibration attempts stopped before the final scoring run:

- `results/hidden-flask-ab-pilot-20260618T053947Z` stopped after 5/9 records
  when `workflow-only` price-ladder edited `scripts/check_api_style.py`. That
  exposed a target-gate mismatch: `price_tier` labels were treated as money-like
  values.
- `results/hidden-flask-ab-pilot-20260618T054858Z` stopped after 8/9 records
  when `workflow-only` value-snapshot edited `scripts/check_api_style.py`. That
  exposed the same class of mismatch for SKU identifier fields containing
  `value`, plus an overly narrow hidden-oracle glossary spelling check.
- `results/hidden-flask-ab-pilot-20260618T060050Z` completed 9/9 operationally
  clean, but value-snapshot was scored before the functional glossary oracle was
  fully updated. It is superseded by the final scoring run.

The target repos were patched with generic API-style allowances for tier labels
and SKU identifier fields, and the hidden oracle was patched to accept
`inventory_value` and `highest_value_sku` as documented concept spellings. The
final scoring run above is the authoritative result.

## Interpretation

This v2 pilot is a clean held-out convention-transfer signal:

- `bare` remained 0/3 strict and 0/3 schema.
- `workflow-only` passed 3/3 strict.
- `memory-harness` passed 3/3 strict.
- All 9 final records were clean for preflight, hidden access, stalls, timeouts,
  wrong-file edits, and forbidden-file edits.

The result supports the current product claim that harness guidance makes agent
work safer and more measurable, and helps preserve repo-local API/schema/docs
conventions. It does not show an accuracy advantage for `memory-harness` over
`workflow-only`; both harness arms passed all three tasks. In this pilot,
`workflow-only` also had the shorter duration tail.

## Decision

The v2 pilot is complete and clean enough to publish as latest execution
evidence, but it is still only a 9-record pilot. Do not promote it above the
96-record stable-4 run as the main representative result. The next useful step
is to either add more v2 held-out task families or repeat this v2 matrix before
spending on a larger v2 promotion.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Final results JSONL:
  `results/hidden-flask-ab-pilot-20260618T061126Z/2026-06-18.jsonl`
- Final run directories:
  `runs/hidden-flask-ab-pilot-20260618T061126Z/`
- Calibration results:
  `results/hidden-flask-ab-pilot-20260618T053947Z/`,
  `results/hidden-flask-ab-pilot-20260618T054858Z/`,
  `results/hidden-flask-ab-pilot-20260618T060050Z/`
