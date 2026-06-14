# Flask H1 Claude Four-Arm Gate - 2026-06-14

This was a Claude four-arm control gate for the two direct H1 catalog
decision-memory task families.

It used the same runner, hidden task specs, target refs, and idle/no-edit
watchdogs that exposed repeated Codex no-edit stalls. The benchmarked agent was
`examples/agents/claude_code_agent.py`.

This was not a promotion-scale run. It was an 8-record gate to add controls
(`workflow-only`, `failure-only`) around the prior decision-bearing Claude
adapter-control runs.

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
- Runner ref: `08fbf83fe0c4126632548f2d36fb3496f9b3d003`
- Started: `2026-06-14T10:02:15Z`
- Finished: `2026-06-14T10:22:28Z`
- Results directory: `results/hidden-flask-ab-pilot-20260614T100214Z`

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

| Arm | Runs | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | p50 duration | First repo change |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `workflow-only` | 2 | 0 | 1 | 2 | 2 | 2 | 0/2 | 0 | 0 | 108s | 71.1-83.1s |
| `decision-only` | 2 | 1 | 1 | 2 | 2 | 2 | 1/2 | 0 | 0 | 131s | 93.1-93.1s |
| `failure-only` | 2 | 0 | 0 | 2 | 2 | 2 | 0/2 | 0 | 0 | 115s | 67.1-97.1s |
| `full-harness` | 2 | 1 | 1 | 2 | 2 | 2 | 1/2 | 0 | 0 | 143s | 98.1-144.2s |

Overall:

- Completed records: 8/8
- Strict successes: 2/8
- Verification passed: 2/8
- Decision-bearing strict successes: 2/4
- Control-arm strict successes: 0/4
- Decision-bearing record consistency: 2/4
- Control-arm record consistency: 0/4
- No-edit watchdogs: 0
- Startup/no-output watchdogs: 0
- Timeouts: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Hidden-access findings: 0

## Per-Task Results

| Arm | Task | Strict | Functional | Schema | Workflow | Record consistency | First repo change | Duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `workflow-only` | `hidden-effect-catalog-price-policy` | 0 | 1 | 1 | 1 | 0/1 | 83.1s | 124.3s |
| `decision-only` | `hidden-effect-catalog-price-policy` | 0 | 0 | 1 | 1 | 0/1 | 93.1s | 131.4s |
| `failure-only` | `hidden-effect-catalog-price-policy` | 0 | 0 | 1 | 1 | 0/1 | 97.1s | 138.6s |
| `full-harness` | `hidden-effect-catalog-price-policy` | 0 | 0 | 1 | 1 | 0/1 | 144.2s | 178.0s |
| `workflow-only` | `hidden-effect-catalog-replenishment-policy` | 0 | 0 | 1 | 1 | 0/1 | 71.1s | 108.4s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | 1 | 1 | 1 | 1 | 1/1 | 93.1s | 134.9s |
| `failure-only` | `hidden-effect-catalog-replenishment-policy` | 0 | 0 | 1 | 1 | 0/1 | 67.1s | 114.7s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | 1 | 1 | 1 | 1 | 1/1 | 98.1s | 142.9s |

The replenishment family produced a clean H1 separation: both decision-bearing
arms passed strict and record-consistent checks, while both controls stayed
record-inconsistent.

The price-policy family did not produce a clean decision-bearing pass in this
gate. All arms edited real files and passed schema/workflow. The failure causes
were hidden functional or record-consistency details:

- `workflow-only`: functional passed, but record-consistency failed because no
  price-band decision record exists in the target.
- `decision-only`: glossary missed the hidden oracle's `price band` concept
  wording.
- `failure-only`: summary did not count `budget`, `standard`, and `premium`,
  and no price-band decision record exists in the target.
- `full-harness`: glossary missed the hidden oracle's `price band` concept
  wording.

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
| `decision-only` | 2 | 0 | 0 | 0 | 93s | - | 0s |
| `failure-only` | 2 | 0 | 0 | 0 | 67s | - | 0s |
| `full-harness` | 2 | 0 | 0 | 0 | 98s | - | 0s |
| `workflow-only` | 2 | 0 | 0 | 0 | 71s | - | 0s |
```

## Reading

What held:

- Claude completed the four-arm gate without no-edit watchdogs, timeouts,
  hidden-access findings, wrong-file edits, or forbidden-file edits.
- Every record made repository changes before the 240-second no-edit watchdog.
- Controls stayed 0/4 record-consistent.
- Replenishment separated cleanly: decision-bearing arms 2/2, controls 0/2.

What did not hold:

- Price-policy decision-bearing arms did not pass in this particular gate.
- The dominant price-policy miss was glossary concept wording rather than
  failure to discover or apply the price-band thresholds.

## Decision

This gate strengthens the adapter conclusion: the Codex no-edit blocker is not
required by the runner, watchdog, target refs, or task specs. Claude can run
the same four-arm matrix without operational abnormal events.

This gate does not yet justify a broad H1 promotion. It supports continuing H1
under Claude, but price-policy remains noisy because the hidden oracle is
sensitive to glossary concept wording. The next useful step is a repeated
Claude four-arm gate or a price-policy oracle/wording triage before any
promotion-scale run.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T100214Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T100214Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-h1-claude-four-arm-gate.md`
