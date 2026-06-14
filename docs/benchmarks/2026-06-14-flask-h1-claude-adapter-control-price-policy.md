# Flask H1 Claude Adapter Control Price Policy - 2026-06-14

This was a minimal live adapter-control pilot for the H1 price-policy task
after Codex repeatedly hit no-edit watchdogs.

It used the same runner, same hidden task family, same target refs, and the
same idle/no-edit watchdogs, but swapped the benchmarked agent from the Codex
adapter to `examples/agents/claude_code_agent.py`.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Task: `hidden-effect-catalog-price-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `decision-only`, `full-harness`
- Repeats: 1
- Planned records: 2
- Completed records: 2
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 240`
- Agent adapter: `examples/agents/claude_code_agent.py`
- Claude binary: `/opt/homebrew/bin/claude`
- Runner ref: `2b95293608b7aeaa4b5577d727b42e2dfce336e7`
- Results directory: `results/hidden-flask-ab-pilot-20260614T093634Z`

Target refs:

| Arm | Source | Ref |
| --- | --- | --- |
| `decision-only` | `../flask-decision-only` | `e9b0a3e919a7827497c7163912a1023c2346008f` |
| `full-harness` | `../flask-memory-harness` | `ba8b3963d071089429fa2c2c8ebc10049e80cca4` |

Command:

```bash
CLAUDE_BIN=/opt/homebrew/bin/claude python3 scripts/run_hidden_flask_ab.py \
  --mode pilot \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-price-policy \
  --arms decision-only,full-harness \
  --repeats 1 \
  --arm-order listed \
  --agent-command "python3 /Users/wb/Desktop/harness-agent-benchmark-runner/examples/agents/claude_code_agent.py" \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal \
  --execute
```

## Headline

| Arm | Runs | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | First repo change | Duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 1 | 0 | 0 | 1 | 1 | 1 | 0/1 | 0 | 0 | 85.1s | 121.7s |
| `full-harness` | 1 | 1 | 1 | 1 | 1 | 1 | 1/1 | 0 | 0 | 92.1s | 130.3s |

Overall:

- Completed records: 2/2
- Strict successes: 1/2
- Verification passed: 1/2
- No-edit watchdogs: 0
- Startup/no-output watchdogs: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Hidden-access findings: 0

## Per-Run Reading

`decision-only`:

- Edited `app/__init__.py`, `app/catalog.py`, `docs/domain/glossary.md`, and
  `tests/test_catalog_price_policy.py`.
- First repository change was observed after 85.1 seconds.
- The local harness gate passed.
- Hidden schema passed.
- Hidden functional and record-consistency checks failed because the glossary
  did not include the exact concept wording required by the hidden oracle:
  `price band`.

`full-harness`:

- Edited `app/__init__.py`, `app/catalog.py`, `docs/domain/glossary.md`, and
  `tests/test_app.py`.
- First repository change was observed after 92.1 seconds.
- Local harness, hidden functional, hidden schema, and hidden
  record-consistency checks all passed.

## Watchdog Diagnostics

`scripts/triage_no_edit_stalls.py` reported:

```text
## No-Edit Stall Triage

No-edit watchdog records: 0
```

`scripts/summarize_hidden_ab.py` reported:

```text
| Target | Watchdog records | No-edit watchdogs | No-output no-edit | No observed repo changes | p50 seconds to repo change | Max seconds without repo change | Max seconds since output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 1 | 0 | 0 | 0 | 85s | - | 0s |
| `full-harness` | 1 | 0 | 0 | 0 | 92s | - | 0s |
```

## Interpretation

This run does not prove H1 at promotion scale. It is only a two-record
adapter-control pilot.

It does show that the repeated Codex no-edit path is not required by the
runner, task, target refs, or no-edit watchdog itself. Under the Claude adapter,
both records reached real repository edits and neither hit a no-edit watchdog.

The `full-harness` pass is directionally positive for the H1 task, while the
`decision-only` failure is a task/oracle wording miss after a real
implementation, not an operational stall. The next useful comparison is a
small multi-task Claude adapter-control gate, not another Codex 96/100-record
promotion.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T093634Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T093634Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-h1-claude-adapter-control-price-policy.md`
