# Flask H1 Strengthened Prompt-Guard Diagnostic - 2026-06-14

This was the first live diagnostic after strengthening the Codex prompt guard
from a generic "start a scoped edit" instruction to a more explicit
answer-free progress constraint:

> After you identify the relevant implementation direction, do not stop after
> narrating a plan; make the first small scoped app/test/docs edit immediately,
> then continue.

The prior prompt-guard mitigation diagnostic still reproduced a no-edit
watchdog on `decision-only` replenishment after the agent found the accepted
policy and described the intended implementation. This diagnostic reran the
same small decision-bearing matrix against the strengthened guardrail.

All 8 records completed strict/pass and record-consistent. No no-edit
watchdogs, timeouts, wrong-file edits, or forbidden-file edits occurred. First
repository changes were observed within 29.1-39.1 seconds.

This is a positive mitigation signal. It is not enough by itself to justify a
blind 96/100-record H1 promotion, because the no-edit path has been
intermittent across earlier small diagnostics.

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
- Prompt mitigation: adapter default guard says not to stop after narrating a
  plan, and to make the first small scoped app/test/docs edit immediately
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 240`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Runner ref: `29d3c12d1dd2f71dd2f295bb21439ecc762e66e0`
- Started: `2026-06-14T08:16:02Z`
- Finished: `2026-06-14T08:25:30Z`

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
| `decision-only` | 4 | 4 | 4 | 4 | 4 | 4 | 4/4 | 0 | 0 | 0 | 0 | 50s | 54s |
| `full-harness` | 4 | 4 | 4 | 4 | 4 | 4 | 4/4 | 0 | 0 | 0 | 0 | 50s | 57s |

Per task:

| Arm | Task | Runs | Strict | Record consistency | Stalls | p50 duration | p95 duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | `hidden-effect-catalog-price-policy` | 2 | 2 | 2/2 | 0 | 42s | 50s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | 2 | 2 | 2/2 | 0 | 52s | 54s |
| `full-harness` | `hidden-effect-catalog-price-policy` | 2 | 2 | 2/2 | 0 | 50s | 54s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | 2 | 2 | 2/2 | 0 | 50s | 57s |

## Watchdog Diagnostics

`scripts/summarize_hidden_ab.py` reported:

| Target | Watchdog records | No-edit watchdogs | No observed repo changes | p50 seconds to repo change | Max seconds without repo change | Max seconds since output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 4 | 0 | 0 | 35s | - | 0s |
| `full-harness` | 4 | 0 | 0 | 36s | - | 0s |

`scripts/triage_no_edit_stalls.py` reported:

```text
## No-Edit Stall Triage

No-edit watchdog records: 0
```

Per-record timing:

| Arm | Task | Run ID | Strict | Stall | Duration | First repo change |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `decision-only` | `hidden-effect-catalog-price-policy` | `20260614T081602Z-hidden-effect-catalog-price-policy-f20ffa6e` | 1 | 0 | 42.5s | 29.1s |
| `full-harness` | `hidden-effect-catalog-price-policy` | `20260614T081654Z-hidden-effect-catalog-price-policy-1ac7d78e` | 1 | 0 | 49.6s | 36.1s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | `20260614T081753Z-hidden-effect-catalog-replenishment-policy-1aa6fcba` | 1 | 0 | 51.9s | 35.1s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | `20260614T081853Z-hidden-effect-catalog-replenishment-policy-424c97d0` | 1 | 0 | 56.9s | 31.1s |
| `full-harness` | `hidden-effect-catalog-price-policy` | `20260614T082030Z-hidden-effect-catalog-price-policy-ab8234b9` | 1 | 0 | 54.4s | 39.1s |
| `decision-only` | `hidden-effect-catalog-price-policy` | `20260614T082134Z-hidden-effect-catalog-price-policy-53bd8279` | 1 | 0 | 50.4s | 35.1s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | `20260614T082308Z-hidden-effect-catalog-replenishment-policy-8f45013f` | 1 | 0 | 49.7s | 36.1s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | `20260614T082407Z-hidden-effect-catalog-replenishment-policy-54bda324` | 1 | 0 | 54.1s | 35.1s |

## Reading

What this diagnostic shows:

- The strengthened answer-free prompt guard is a plausible no-edit mitigation.
- It cleared the exact small matrix that the prior generic guard failed.
- The previously recurring `decision-only`
  `hidden-effect-catalog-replenishment-policy` path completed 2/2 strict and
  record-consistent.
- First observed repository changes stayed within 29.1-39.1 seconds.

What it does not show:

- It does not prove the no-edit path is solved at promotion scale.
- It does not prove the improvement is causal; no-edit has been intermittent in
  small diagnostics.
- It does not justify disabling no-edit watchdogs or running a blind 96/100
  promotion immediately.

## Decision

Keep the strengthened prompt guard.

The next useful H1 step is a larger but still bounded operational gate, not a
blind promotion:

- rerun a 16-record or 24-record decision-bearing gate under the strengthened
  guard;
- keep sequential execution and no-edit watchdog reporting;
- only consider a scoped 96-record H1 promotion after that gate is clean.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T081602Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T081602Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-h1-strengthened-prompt-guard-diagnostic.md`
