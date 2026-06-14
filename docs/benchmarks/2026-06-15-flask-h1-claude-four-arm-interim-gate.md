# Flask H1 Claude Four-Arm Interim Gate - 2026-06-15

This was a fresh patched-oracle Claude four-arm gate for the two direct H1
catalog decision-memory task families.

This run is the current interim representative evidence for the H1
decision-memory line. It is still not the broad public representative result
for the whole benchmark runner; that remains the stable-4 96-record promotion.

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
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 240`
- Agent adapter: `examples/agents/claude_code_agent.py`
- Claude binary: `/opt/homebrew/bin/claude`
- Runner ref: `bc81ce035174075c65d9f8d6f1c8b9bd5d6230c5`
- Started: `2026-06-14T15:01:56Z`
- Finished: `2026-06-14T15:21:34Z`
- Results directory: `results/hidden-flask-ab-pilot-20260614T150156Z`

Target refs:

| Arm | Source | Ref |
| --- | --- | --- |
| `workflow-only` | `../flask-workflow-only` | `1a79d8cf9e0799789b3da8029dbbb5a572b3133e` |
| `decision-only` | `../flask-decision-only` | `e9b0a3e919a7827497c7163912a1023c2346008f` |
| `failure-only` | `../flask-failure-only` | `18330ea23880b1ca7a647ea58b0d694e2c658fc8` |
| `full-harness` | `../flask-memory-harness` | `ba8b3963d071089429fa2c2c8ebc10049e80cca4` |

Command:

```bash
CLAUDE_BIN=/opt/homebrew/bin/claude python3 scripts/run_hidden_flask_ab.py \
  --mode pilot \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-price-policy \
  --task-id hidden-effect-catalog-replenishment-policy \
  --arms workflow-only,decision-only,failure-only,full-harness \
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

| Arm | Runs | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Quota exits | p50 duration | First repo change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `workflow-only` | 2 | 0 | 1 | 2 | 2 | 2 | 0/2 | 0 | 0 | 0 | 130s | 86.1-89.1s |
| `decision-only` | 2 | 2 | 2 | 2 | 2 | 2 | 2/2 | 0 | 0 | 0 | 131s | 95.1-101.3s |
| `failure-only` | 2 | 0 | 1 | 2 | 2 | 2 | 0/2 | 0 | 0 | 0 | 120s | 79.5-95.1s |
| `full-harness` | 2 | 2 | 2 | 2 | 2 | 2 | 2/2 | 0 | 0 | 0 | 115s | 79.2-103.1s |

Overall:

- Completed records: 8/8
- Strict successes: 4/8
- Verification passed: 4/8
- Decision-bearing strict successes: 4/4
- Control-arm strict successes: 0/4
- Decision-bearing record consistency: 4/4
- Control-arm record consistency: 0/4
- No-edit watchdogs: 0
- Startup/no-output watchdogs: 0
- Agent quota/session-limit exits: 0
- Timeouts: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Hidden-access findings: 0

## Per-Task Results

| Arm | Task | Strict | Functional | Schema | Workflow | Record consistency | First repo change | Duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `workflow-only` | `hidden-effect-catalog-price-policy` | 0 | 1 | 1 | 1 | 0/1 | 86.1s | 130.4s |
| `decision-only` | `hidden-effect-catalog-price-policy` | 1 | 1 | 1 | 1 | 1/1 | 95.1s | 131.3s |
| `failure-only` | `hidden-effect-catalog-price-policy` | 0 | 1 | 1 | 1 | 0/1 | 95.1s | 130.4s |
| `full-harness` | `hidden-effect-catalog-price-policy` | 1 | 1 | 1 | 1 | 1/1 | 103.1s | 144.4s |
| `workflow-only` | `hidden-effect-catalog-replenishment-policy` | 0 | 0 | 1 | 1 | 0/1 | 89.1s | 136.8s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | 1 | 1 | 1 | 1 | 1/1 | 101.3s | 140.6s |
| `failure-only` | `hidden-effect-catalog-replenishment-policy` | 0 | 0 | 1 | 1 | 0/1 | 79.5s | 119.5s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | 1 | 1 | 1 | 1 | 1/1 | 79.2s | 115.0s |

Failure causes were expected control-arm misses:

- `workflow-only` price-policy: functional/schema/workflow passed, but no
  pre-existing price-band decision record existed.
- `failure-only` price-policy: functional/schema/workflow passed, but no
  pre-existing price-band decision record existed.
- `workflow-only` replenishment: schema/workflow passed, but summary/status
  terms did not match the accepted decision and no decision record existed.
- `failure-only` replenishment: schema/workflow passed, but summary/status
  terms did not match the accepted decision and no decision record existed.

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
| `decision-only` | 2 | 0 | 0 | 0 | 95s | - | 0s |
| `failure-only` | 2 | 0 | 0 | 0 | 80s | - | 0s |
| `full-harness` | 2 | 0 | 0 | 0 | 79s | - | 0s |
| `workflow-only` | 2 | 0 | 0 | 0 | 86s | - | 0s |
```

## Reading

This run cleanly separates direct decision-memory arms from controls on both
catalog decision families:

- `decision-only` and `full-harness` passed every strict and
  record-consistency check.
- `workflow-only` and `failure-only` stayed record-inconsistent, as expected.
- The previous price-policy glossary-token false negative did not recur.
- The previous Claude session-limit contamination did not recur.
- Every record made repository changes before the no-edit watchdog.

This is strong interim H1 evidence for the measured Flask scope. It is not yet
a promotion-scale claim and does not justify a blind 96/100-record Codex H1
promotion, because the Codex no-edit path remains unresolved.

## Decision

Use this report as the current H1 interim representative evidence. The next
useful step is a repeated 16-record or 24-record Claude gate before any larger
claim, while keeping Codex promotion blocked until the post-output no-edit path
is mitigated or explicitly becomes the diagnostic target.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T150156Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T150156Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-15-flask-h1-claude-four-arm-interim-gate.md`
