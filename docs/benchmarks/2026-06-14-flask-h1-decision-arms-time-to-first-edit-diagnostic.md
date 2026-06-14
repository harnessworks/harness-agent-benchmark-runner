# Flask H1 Decision-Arms Time-To-First-Edit Diagnostic - 2026-06-14

This was a small no-edit-focused diagnostic after two scoped H1 promotion
attempts stopped on no-edit watchdogs at promotion scale.

The diagnostic used only the two decision-bearing arms and the two direct H1
task families. It ran without `--stop-on-abnormal` so any no-edit recurrence
would be recorded without censoring the rest of the small matrix.

All 8 records completed strict/pass and record-consistent. No no-edit
watchdogs, timeouts, wrong-file edits, or forbidden-file edits occurred. First
repository changes were observed within 22.0-38.1 seconds.

This does not make another blind 96/100-record promotion valuable. It shows the
no-edit failure is intermittent and promotion-scale, not deterministic for the
selected task/arm pairs in a small diagnostic batch.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Tasks:
  - `hidden-effect-catalog-price-policy`
  - `hidden-effect-catalog-replenishment-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `decision-only`, `full-harness`
- Repeats: 2
- Planned records: 8
- Completed records: 8
- Concurrency: `--jobs 1`
- Stop-on-abnormal: disabled
- Promotion mode: disabled
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 240`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Runner ref: `1de1e81ebf506afdd692e6067d241189e833655d`
- Started: `2026-06-14T07:43:49Z`
- Finished: `2026-06-14T07:52:37Z`

Target refs:

| Arm | Source | Ref |
| --- | --- | --- |
| `decision-only` | `../flask-decision-only` | `e9b0a3e919a7827497c7163912a1023c2346008f` |
| `full-harness` | `../flask-memory-harness` | `ba8b3963d071089429fa2c2c8ebc10049e80cca4` |

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-price-policy \
  --task-id hidden-effect-catalog-replenishment-policy \
  --arms decision-only,full-harness \
  --repeats 2 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --execute
```

## Headline

| Arm | Runs | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 4 | 4 | 4 | 4 | 4 | 4 | 4/4 | 0 | 0 | 0 | 0 | 50s | 61s |
| `full-harness` | 4 | 4 | 4 | 4 | 4 | 4 | 4/4 | 0 | 0 | 0 | 0 | 48s | 58s |

Per task:

| Arm | Task | Runs | Strict | Record consistency | Stalls | p50 duration | p95 duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | `hidden-effect-catalog-price-policy` | 2 | 2 | 2/2 | 0 | 42s | 50s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | 2 | 2 | 2/2 | 0 | 58s | 61s |
| `full-harness` | `hidden-effect-catalog-price-policy` | 2 | 2 | 2/2 | 0 | 48s | 58s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | 2 | 2 | 2/2 | 0 | 47s | 53s |

## Watchdog Diagnostics

`scripts/summarize_hidden_ab.py` reported:

| Target | Watchdog records | No-edit watchdogs | No observed repo changes | p50 seconds to repo change | Max seconds without repo change | Max seconds since output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 4 | 0 | 0 | 33s | - | 0s |
| `full-harness` | 4 | 0 | 0 | 32s | - | 0s |

`scripts/triage_no_edit_stalls.py` reported:

```text
## No-Edit Stall Triage

No-edit watchdog records: 0
```

Per-record timing:

| Arm | Task | Run ID | Duration | First repo change |
| --- | --- | --- | ---: | ---: |
| `decision-only` | `hidden-effect-catalog-price-policy` | `20260614T074349Z-hidden-effect-catalog-price-policy-8a4ebc67` | 50.4s | 38.1s |
| `full-harness` | `hidden-effect-catalog-price-policy` | `20260614T074448Z-hidden-effect-catalog-price-policy-054258b8` | 57.8s | 22.0s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | `20260614T074555Z-hidden-effect-catalog-replenishment-policy-381f670d` | 60.9s | 25.0s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | `20260614T074705Z-hidden-effect-catalog-replenishment-policy-6c069ddc` | 52.5s | 37.1s |
| `full-harness` | `hidden-effect-catalog-price-policy` | `20260614T074811Z-hidden-effect-catalog-price-policy-64698c08` | 47.9s | 32.1s |
| `decision-only` | `hidden-effect-catalog-price-policy` | `20260614T074908Z-hidden-effect-catalog-price-policy-8375de55` | 42.3s | 33.1s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | `20260614T074959Z-hidden-effect-catalog-replenishment-policy-ccbfed1b` | 47.4s | 34.1s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | `20260614T075127Z-hidden-effect-catalog-replenishment-policy-1138ea2c` | 58.5s | 38.1s |

## Reading

What this diagnostic shows:

- The two stopped promotion records are not deterministic failures for these
  task/arm pairs.
- In a small decision-bearing matrix, agents started editing quickly:
  22.0-38.1 seconds to first observed repository change.
- Both decision-bearing arms remained 4/4 strict and record-consistent across
  the two direct H1 task families.

What it does not show:

- It does not prove a 96/100-record promotion will complete.
- It does not identify why no-edit appears at promotion scale.
- It does not justify disabling the no-edit watchdog.
- It does not measure control arms, because this diagnostic was scoped to
  time-to-first-edit behavior in the decision-bearing arms.

## Decision

Do not claim H1 promotion readiness from this diagnostic.

The next useful work is still operational:

- either add a prompt/adapter mitigation that nudges agents to begin a minimal
  scoped implementation edit after finding relevant records;
- or run another small diagnostic whose explicit purpose is time-to-first-edit
  behavior, not broad H1 scoring.

Another blind 96/100-record promotion remains low-value until this intermittent
no-edit path is better controlled or accepted as the explicit variable under
study.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T074349Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T074349Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-h1-decision-arms-time-to-first-edit-diagnostic.md`
