# Flask H1 Claude Adapter Control Two-Family Gate - 2026-06-14

This was a small Claude adapter-control gate for the two direct H1 catalog
decision-memory task families.

It used the same runner, same hidden task specs, same target refs, and the same
idle/no-edit watchdogs that exposed repeated Codex no-edit stalls. The only
substantive change was the benchmarked agent adapter:
`examples/agents/claude_code_agent.py`.

This was not a promotion-scale run. It was a bounded adapter-control check
before deciding whether H1 should continue under Claude while Codex remains
blocked by post-output no-edit behavior.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Tasks:
  - `hidden-effect-catalog-price-policy`
  - `hidden-effect-catalog-replenishment-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `decision-only`, `full-harness`
- Repeats: 1
- Planned records: 4
- Completed records: 4
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 240`
- Agent adapter: `examples/agents/claude_code_agent.py`
- Claude binary: `/opt/homebrew/bin/claude`
- Runner ref: `8f279027f45225ef6339f4580349cfcf675228be`
- Started: `2026-06-14T09:46:55Z`
- Finished: `2026-06-14T09:57:33Z`
- Results directory: `results/hidden-flask-ab-pilot-20260614T094655Z`

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
  --task-id hidden-effect-catalog-replenishment-policy \
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

| Arm | Runs | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | p50 duration | First repo change range |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `decision-only` | 2 | 2 | 2 | 2 | 2 | 2 | 2/2 | 0 | 0 | 126s | 81.1-91.1s |
| `full-harness` | 2 | 1 | 1 | 2 | 2 | 2 | 1/2 | 0 | 0 | 116s | 79.1-94.1s |

Overall:

- Completed records: 4/4
- Strict successes: 3/4
- Verification passed: 3/4
- No-edit watchdogs: 0
- Startup/no-output watchdogs: 0
- Timeouts: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Hidden-access findings: 0

## Per-Task Results

| Arm | Task | Strict | Functional | Schema | Workflow | Record consistency | First repo change | Duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | `hidden-effect-catalog-price-policy` | 1 | 1 | 1 | 1 | 1/1 | 91.1s | 138.6s |
| `full-harness` | `hidden-effect-catalog-price-policy` | 0 | 0 | 1 | 1 | 0/1 | 79.1s | 115.8s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | 1 | 1 | 1 | 1 | 1/1 | 81.1s | 126.3s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | 1 | 1 | 1 | 1 | 1/1 | 94.1s | 132.0s |

The one failed record, `full-harness` price-policy, was not an operational
failure. It edited real files and passed schema/workflow checks. Hidden
functional and record-consistency checks failed because the glossary omitted
the hidden oracle's `price band` concept wording.

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
| `decision-only` | 2 | 0 | 0 | 0 | 81s | - | 0s |
| `full-harness` | 2 | 0 | 0 | 0 | 79s | - | 0s |
```

## Reading

What held:

- Claude completed the two-family decision-bearing H1 gate without no-edit
  watchdogs, timeouts, file-boundary issues, or hidden-access findings.
- All four records made repository changes before the 240-second no-edit
  watchdog, with first changes observed between 79.1 and 94.1 seconds.
- `decision-only` was 2/2 strict and record-consistent.
- `full-harness` was 1/2 strict and record-consistent, with the miss caused by
  hidden glossary concept wording rather than failure to start editing.

What this supports:

- The repeated Codex no-edit blocker is not required by the runner, watchdog,
  task specs, or target refs.
- H1 remains worth studying under Claude because the same task family can
  complete without the Codex pre-edit stall.

What this does not prove:

- It does not prove promotion-scale H1 behavior.
- It does not prove `full-harness` is better than `decision-only`; this gate
  only included decision-bearing arms.
- It does not remove the need for controls (`workflow-only`, `failure-only`)
  before making a decision-memory claim.

## Decision

Do not run another blind Codex H1 promotion. Codex remains blocked by
post-output no-edit behavior.

The next useful H1 step is a Claude four-arm gate over both direct H1 task
families:

- arms: `workflow-only`, `decision-only`, `failure-only`, `full-harness`;
- repeats: 2 if budget allows, otherwise 1;
- keep `--jobs 1`, idle/no-edit watchdogs, and public-safe reporting;
- promote only if controls remain record-inconsistent and no operational
  abnormalities appear.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T094655Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T094655Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-h1-claude-adapter-control-two-family.md`
