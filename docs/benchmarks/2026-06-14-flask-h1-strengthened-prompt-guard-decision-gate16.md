# Flask H1 Strengthened Prompt-Guard Decision Gate16 - 2026-06-14

This was a bounded operational gate after strengthening the Codex prompt guard
to prevent agents from stopping after narrating a plan. It expanded the clean
8-record strengthened-guard diagnostic to 16 decision-bearing records.

The gate used only the two decision-bearing arms and the two direct H1 task
families. It intentionally did not re-run controls; the question was whether
the strengthened guard reduced no-edit risk on the arms that must succeed
before another H1 promotion attempt.

All 16 records completed strict/pass and record-consistent. No no-edit
watchdogs, timeouts, hidden-access findings, wrong-file edits, or forbidden-file
edits occurred. First repository changes were observed within 21.0-54.1
seconds.

This is the strongest mitigation evidence so far. It still is not a 96/100-run
promotion result.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Tasks:
  - `hidden-effect-catalog-price-policy`
  - `hidden-effect-catalog-replenishment-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `decision-only`, `full-harness`
- Repeats: 4
- Planned records: 16
- Completed records: 16
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
- Runner ref: `6cdbd1f315910775ef736f16034ebadc5d1fae7a`
- Started: `2026-06-14T08:27:55Z`
- Finished: `2026-06-14T08:50:58Z`

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
  --repeats 4 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --execute
```

## Headline

| Arm | Runs | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 8 | 8 | 8 | 8 | 8 | 8 | 8/8 | 0 | 0 | 0 | 0 | 54s | 87s |
| `full-harness` | 8 | 8 | 8 | 8 | 8 | 8 | 8/8 | 0 | 0 | 0 | 0 | 55s | 85s |

Per task:

| Arm | Task | Runs | Strict | Record consistency | Stalls | p50 duration | p95 duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | `hidden-effect-catalog-price-policy` | 4 | 4 | 4/4 | 0 | 54s | 87s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | 4 | 4 | 4/4 | 0 | 51s | 65s |
| `full-harness` | `hidden-effect-catalog-price-policy` | 4 | 4 | 4/4 | 0 | 50s | 66s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | 4 | 4 | 4/4 | 0 | 55s | 85s |

## Watchdog Diagnostics

`scripts/summarize_hidden_ab.py` reported:

| Target | Watchdog records | No-edit watchdogs | No observed repo changes | p50 seconds to repo change | Max seconds without repo change | Max seconds since output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 8 | 0 | 0 | 27s | - | 0s |
| `full-harness` | 8 | 0 | 0 | 32s | - | 0s |

`scripts/triage_no_edit_stalls.py` reported:

```text
## No-Edit Stall Triage

No-edit watchdog records: 0
```

Per-record timing:

| Arm | Task | Run ID | Strict | Stall | Duration | First repo change |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `decision-only` | `hidden-effect-catalog-price-policy` | `20260614T082755Z-hidden-effect-catalog-price-policy-8175de7b` | 1 | 0 | 87.4s | 54.1s |
| `full-harness` | `hidden-effect-catalog-price-policy` | `20260614T082931Z-hidden-effect-catalog-price-policy-e6e09ee6` | 1 | 0 | 44.7s | 31.1s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | `20260614T083027Z-hidden-effect-catalog-replenishment-policy-ae48b93d` | 1 | 0 | 65.3s | 27.1s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | `20260614T083209Z-hidden-effect-catalog-replenishment-policy-c22e803d` | 1 | 0 | 55.4s | 33.1s |
| `full-harness` | `hidden-effect-catalog-price-policy` | `20260614T083348Z-hidden-effect-catalog-price-policy-b24363d7` | 1 | 0 | 58.0s | 27.0s |
| `decision-only` | `hidden-effect-catalog-price-policy` | `20260614T083455Z-hidden-effect-catalog-price-policy-2e6ab046` | 1 | 0 | 51.1s | 36.1s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | `20260614T083631Z-hidden-effect-catalog-replenishment-policy-2ad4cac1` | 1 | 0 | 47.5s | 32.1s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | `20260614T083808Z-hidden-effect-catalog-replenishment-policy-3dbc15f5` | 1 | 0 | 50.0s | 33.1s |
| `decision-only` | `hidden-effect-catalog-price-policy` | `20260614T083907Z-hidden-effect-catalog-price-policy-ea3dac96` | 1 | 0 | 54.1s | 25.0s |
| `full-harness` | `hidden-effect-catalog-price-policy` | `20260614T084028Z-hidden-effect-catalog-price-policy-a63923d7` | 1 | 0 | 50.3s | 33.1s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | `20260614T084128Z-hidden-effect-catalog-replenishment-policy-f407870e` | 1 | 0 | 56.7s | 23.0s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | `20260614T084314Z-hidden-effect-catalog-replenishment-policy-78e1f4ad` | 1 | 0 | 54.5s | 36.1s |
| `full-harness` | `hidden-effect-catalog-price-policy` | `20260614T084456Z-hidden-effect-catalog-price-policy-a4b1216d` | 1 | 0 | 65.5s | 26.1s |
| `decision-only` | `hidden-effect-catalog-price-policy` | `20260614T084713Z-hidden-effect-catalog-price-policy-dbfef10a` | 1 | 0 | 56.1s | 29.1s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | `20260614T084819Z-hidden-effect-catalog-replenishment-policy-e0c627aa` | 1 | 0 | 84.7s | 40.1s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | `20260614T084956Z-hidden-effect-catalog-replenishment-policy-9124136d` | 1 | 0 | 51.4s | 21.0s |

## Reading

What this gate shows:

- The strengthened prompt guard held across a larger bounded decision-bearing
  gate.
- The previously recurring `decision-only`
  `hidden-effect-catalog-replenishment-policy` path completed 4/4 strict and
  record-consistent.
- Both decision-bearing arms completed 8/8 strict and record-consistent.
- No run touched wrong or forbidden files.

What it does not show:

- It does not measure control arms in this run.
- It does not prove promotion-scale stability across 96 records.
- It does not prove the no-edit risk is eliminated; prior stops were
  intermittent.

## Decision

The strengthened prompt guard is now strong enough to justify a scoped H1
promotion attempt if the next objective is promotion-scale evidence.

Do not call this a 100-run result. The next promotion attempt should stay
scoped and guarded:

- keep the two direct H1 task families;
- keep all four non-bare arms if measuring H1 effect size again;
- keep `CODEX_PROMPT_GUARD=1`, sequential execution, clean-readiness results,
  no-edit watchdogs, and `--stop-on-abnormal`;
- report any stop as operational instability, not as a scoring ambiguity.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T082755Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T082755Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-h1-strengthened-prompt-guard-decision-gate16.md`
