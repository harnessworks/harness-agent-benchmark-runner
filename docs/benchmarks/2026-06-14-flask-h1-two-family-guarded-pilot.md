# Flask H1 Two-Family Guarded Pilot - 2026-06-14

This was a guarded small H1 pilot over two direct decision-memory task
families after adding the second catalog replenishment-policy decision task.
It intentionally ran a small matrix before any 100-run promotion decision.

The run was operationally clean: all 8 planned records completed with zero
stalls, zero timeouts, zero wrong-file edits, and zero forbidden-file edits.
The scoring result was mixed. `hidden-effect-catalog-price-policy` reproduced
the expected H1 separation, but `hidden-effect-catalog-replenishment-policy`
passed only in `full-harness`; `decision-only` failed the functional and
record-consistency dimensions.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Tasks:
  - `hidden-effect-catalog-price-policy`
  - `hidden-effect-catalog-replenishment-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `workflow-only`, `decision-only`, `failure-only`, `full-harness`
- Repeats: 1
- Planned records: 8
- Completed records: 8
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 240`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Runner ref: `2bf16d6aa4bb02705aaf5f1234e519f3c46869a6`
- Started: `2026-06-14T05:28:20Z`
- Finished: `2026-06-14T05:43:07Z`

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
  --repeats 1 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal \
  --execute
```

## Headline

| Arm | Completed | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | Duration range | First repo change range |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `workflow-only` | 2 | 0 | 1 | 2 | 2 | 2 | 0/2 | 0 | 0 | 0 | 0 | 50.6-64.9s | 31.1-37.1s |
| `decision-only` | 2 | 1 | 1 | 2 | 2 | 2 | 1/2 | 0 | 0 | 0 | 0 | 48.2-49.4s | 22.0-33.1s |
| `failure-only` | 2 | 0 | 1 | 2 | 2 | 2 | 0/2 | 0 | 0 | 0 | 0 | 54.9-79.1s | 37.0-40.1s |
| `full-harness` | 2 | 2 | 2 | 2 | 2 | 2 | 2/2 | 0 | 0 | 0 | 0 | 50.9-58.2s | 33.0-39.1s |

Overall:

- Completed records: 8/8
- Strict successes: 3/8
- Record consistency: 3/8
- Decision-bearing record consistency: 3/4
- Control-arm record consistency: 0/4
- Stalls/timeouts: 0
- Preflight failures: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- No-edit watchdog records: 0

## Per-Task Results

| Arm | Task | Strict | Functional | Schema | Workflow | Record consistency | First failure |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `workflow-only` | `hidden-effect-catalog-price-policy` | 0 | 1 | 1 | 1 | 0 | Missing pre-existing decision record. |
| `decision-only` | `hidden-effect-catalog-price-policy` | 1 | 1 | 1 | 1 | 1 | - |
| `failure-only` | `hidden-effect-catalog-price-policy` | 0 | 1 | 1 | 1 | 0 | Missing pre-existing decision record. |
| `full-harness` | `hidden-effect-catalog-price-policy` | 1 | 1 | 1 | 1 | 1 | - |
| `workflow-only` | `hidden-effect-catalog-replenishment-policy` | 0 | 0 | 1 | 1 | 0 | Summary did not count `reorder_now`, `monitor`, and `healthy`. |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | 0 | 0 | 1 | 1 | 0 | Glossary missed the normalized phrase `replenishment status`. |
| `failure-only` | `hidden-effect-catalog-replenishment-policy` | 0 | 0 | 1 | 1 | 0 | Summary did not count `reorder_now`, `monitor`, and `healthy`. |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | 1 | 1 | 1 | 1 | 1 | - |

## Watchdog Diagnostics

`scripts/summarize_hidden_ab.py` reported:

| Target | Watchdog records | No-edit watchdogs | No observed repo changes | p50 seconds to repo change | Max seconds without repo change | Max seconds since output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 2 | 0 | 0 | 22s | - | 0s |
| `failure-only` | 2 | 0 | 0 | 37s | - | 0s |
| `full-harness` | 2 | 0 | 0 | 33s | - | 0s |
| `workflow-only` | 2 | 0 | 0 | 31s | - | 0s |

`scripts/triage_no_edit_stalls.py` reported:

```text
## No-Edit Stall Triage

No-edit watchdog records: 0
```

This keeps the previous H1 no-edit blocker cleared for this small matrix.

## Replenishment Failure Triage

The `decision-only` replenishment record was not a total decision-memory miss.
It implemented the adopted response key and current catalog labels:
`reorder_now`, `monitor`, and `healthy`. The first oracle failure was the
functional documentation check:

```text
glossary must document catalog replenishment policy route and statuses;
missing: replenishment status
```

The generated glossary used the code-style token `replenishment_status` as the
term heading instead of the normalized prose phrase `replenishment status`.
That is a useful signal, but it also means the replenishment oracle is more
sensitive to documentation wording than the price-policy task.

The same `decision-only` code used `stock < 5` for `reorder_now` and
`stock < 20` for `monitor`. The adopted decision says `reorder_now` is stock
below 5, `monitor` is stock from 5 up to but not including 20, and `healthy` is
stock 20 or higher, so the code's boundary behavior appears consistent. The
record-consistency failure in this saved run did not reach the hidden edge
check because the functional glossary requirement failed first.

The `full-harness` replenishment record passed strict, functional, schema,
workflow, and record-consistency checks. Its glossary used the expected prose
term and its implementation used the adopted labels and thresholds.

## Reading

What held:

- The run was operationally clean: 8/8 completed, no stalls, no timeouts, no
  boundary misses, and no hidden-access findings.
- The price-policy H1 signal reproduced: decision-bearing arms passed and
  control arms failed record consistency.
- `full-harness` passed both direct H1 decision-memory task families.

What did not hold:

- `decision-only` did not pass the new replenishment family on the first live
  run.
- The new task family is not yet a stable direct H1 discriminator because its
  first failure is a documentation wording mismatch, not a clear absence of the
  accepted decision behavior.
- The current two-family evidence is therefore not strong enough to justify a
  broad 100-run H1 promotion.

## Decision

Do not run a 100-record H1 promotion yet.

The useful next spend is a small triage rerun, not a broad promotion:

- run `hidden-effect-catalog-replenishment-policy` across `decision-only` and
  `full-harness` for 3-5 repeats;
- keep `workflow-only` and `failure-only` as 1-repeat controls or include them
  only after the decision-bearing triage is clean;
- decide whether the functional glossary check should accept the exact API key
  `replenishment_status` as concept-equivalent to the prose phrase
  `replenishment status`, or keep the stricter prose-documentation expectation;
- only promote to a larger H1 run after both direct decision-memory families
  are clean across decision-bearing arms.

A 100-run promotion would be valuable after that gate because it would measure
stability across more than one decision family. Running it now would mostly
amplify an unresolved task/oracle/discoverability ambiguity.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T052820Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T052820Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-h1-two-family-guarded-pilot.md`
