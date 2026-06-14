# Flask Price-Policy Full-Harness No-Edit Diagnostic - 2026-06-14

This was a focused diagnostic after the scoped H1 promotion stopped on a
`full-harness` `hidden-effect-catalog-price-policy` no-edit watchdog.

The diagnostic reran only that task/arm pair for five repeats without
`--stop-on-abnormal`, so any no-edit recurrence would be recorded without
censoring the rest of the small diagnostic batch.

All five records completed strict/pass. No no-edit watchdogs, timeouts,
wrong-file edits, or forbidden-file edits occurred. This means the promotion
stop is intermittent, not deterministic for this task/arm pair.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Task: `hidden-effect-catalog-price-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arm: `full-harness`
- Repeats: 5
- Planned records: 5
- Completed records: 5
- Concurrency: `--jobs 1`
- Stop-on-abnormal: disabled
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 240`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Started: `2026-06-14T07:08:43Z`
- Finished: `2026-06-14T07:14:41Z`

Target ref:

| Arm | Source | Ref |
| --- | --- | --- |
| `full-harness` | `../flask-memory-harness` | `ba8b3963d071089429fa2c2c8ebc10049e80cca4` |

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-price-policy \
  --arms full-harness \
  --repeats 5 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --execute
```

## Headline

| Arm | Task | Runs | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | p95 duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `full-harness` | `hidden-effect-catalog-price-policy` | 5 | 5 | 5 | 5 | 5 | 5 | 5/5 | 0 | 0 | 0 | 0 | 55s | 57s |

Per-record timing:

| Run | Strict | Duration | First repo change |
| --- | ---: | ---: | ---: |
| `20260614T070843Z-hidden-effect-catalog-price-policy-70379828` | 1 | 44.5s | 31.0s |
| `20260614T070947Z-hidden-effect-catalog-price-policy-a16397b0` | 1 | 55.0s | 36.0s |
| `20260614T071054Z-hidden-effect-catalog-price-policy-3a5d21cd` | 1 | 52.9s | 27.0s |
| `20260614T071220Z-hidden-effect-catalog-price-policy-6ecf172b` | 1 | 55.7s | 36.0s |
| `20260614T071331Z-hidden-effect-catalog-price-policy-21dd3158` | 1 | 57.1s | 23.0s |

## Watchdog Diagnostics

`scripts/summarize_hidden_ab.py` reported:

| Target | Watchdog records | No-edit watchdogs | No observed repo changes | p50 seconds to repo change | Max seconds without repo change | Max seconds since output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `full-harness` | 5 | 0 | 0 | 31s | - | 0s |

`scripts/triage_no_edit_stalls.py` reported:

```text
## No-Edit Stall Triage

No-edit watchdog records: 0
```

## Reading

What this diagnostic shows:

- The `full-harness` price-policy no-edit failure is intermittent.
- The same task/arm pair can complete quickly and consistently under the same
  prompt guard and watchdog settings.
- The previous promotion stop remains real; this run does not erase it.

What this diagnostic does not show:

- It does not prove a 96-record promotion will complete.
- It does not identify the root cause of the stopped agent after decision
  lookup.
- It does not justify disabling the no-edit watchdog.

## Decision

Another promotion attempt is reasonable because the focused diagnostic did not
reproduce the no-edit failure. Keep the same safeguards:

- sequential execution;
- `CODEX_PROMPT_GUARD=1`;
- `--promotion-run`;
- clean-readiness results;
- `--stop-on-abnormal`;
- no-edit and duration-tail reporting.

If the next promotion stops on the same no-edit pattern, treat it as repeated
operational instability rather than as random noise.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T070842Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T070842Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-price-policy-full-harness-noedit-diagnostic.md`
