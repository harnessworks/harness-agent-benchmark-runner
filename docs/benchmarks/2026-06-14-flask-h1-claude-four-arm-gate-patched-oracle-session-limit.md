# Flask H1 Claude Four-Arm Gate After Price-Policy Oracle Patch - 2026-06-14

This was a fresh Claude four-arm control gate after the price-policy glossary
oracle was patched to accept equivalent `price band`, `price-band`, and
`price_band` concept spellings.

This run is not representative H1 evidence. It confirms that the price-policy
wording patch removed the prior glossary false negative, but the replenishment
half was contaminated by the Claude CLI session limit.

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
- Runner ref: `f2941a87162e727627d10216baed914febfab3c0`
- Started: `2026-06-14T10:32:53Z`
- Finished: `2026-06-14T10:47:58Z`
- Results directory: `results/hidden-flask-ab-pilot-20260614T103253Z`

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

| Arm | Runs | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Session-limit exits | Stalls | Timeouts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `workflow-only` | 2 | 0 | 1 | 2 | 2 | 2 | 0/2 | 0 | 0 | 0 |
| `decision-only` | 2 | 1 | 1 | 1 | 1 | 2 | 1/2 | 1 | 0 | 0 |
| `failure-only` | 2 | 0 | 1 | 1 | 1 | 2 | 0/2 | 1 | 0 | 0 |
| `full-harness` | 2 | 1 | 1 | 1 | 1 | 2 | 1/2 | 1 | 0 | 0 |

Overall:

- Completed records: 8/8
- Strict successes: 2/8
- Verification passed: 2/8
- Price-policy strict successes: 2/4
- Price-policy decision-bearing strict successes: 2/2
- Price-policy control-arm strict successes: 0/2
- Replenishment strict successes: 0/4
- Claude session-limit exits: 3
- No-edit watchdogs: 0
- Startup/no-output watchdogs: 0
- Timeouts: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Hidden-access findings: 0

## Per-Task Results

| Arm | Task | Strict | Functional | Schema | Workflow | Record consistency | Agent exit | Repo change observed | Duration | Note |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `workflow-only` | `hidden-effect-catalog-price-policy` | 0 | 1 | 1 | 1 | 0/1 | 0 | true | 176.9s | Missing pre-existing price-band decision record. |
| `decision-only` | `hidden-effect-catalog-price-policy` | 1 | 1 | 1 | 1 | 1/1 | 0 | true | 140.4s | Passed after glossary token variant patch. |
| `failure-only` | `hidden-effect-catalog-price-policy` | 0 | 1 | 1 | 1 | 0/1 | 0 | true | 147.2s | Missing pre-existing price-band decision record. |
| `full-harness` | `hidden-effect-catalog-price-policy` | 1 | 1 | 1 | 1 | 1/1 | 0 | true | 121.3s | Passed after glossary token variant patch. |
| `workflow-only` | `hidden-effect-catalog-replenishment-policy` | 0 | 0 | 1 | 1 | 0/1 | 0 | true | 137.8s | Used `reorder`/`watch`/`ok` instead of accepted statuses. |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | 0 | 0 | 0 | 0 | 0/1 | 1 | true | 94.5s | Claude session limit after a partial `app/catalog.py` edit. |
| `failure-only` | `hidden-effect-catalog-replenishment-policy` | 0 | 0 | 0 | 0 | 0/1 | 1 | false | 1.8s | Claude session limit before repository changes. |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | 0 | 0 | 0 | 0 | 0/1 | 1 | false | 1.4s | Claude session limit before repository changes. |

The Claude CLI message for the contaminated records was:

```text
You've hit your session limit · resets 11:30pm (Asia/Seoul)
```

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
| `decision-only` | 2 | 0 | 0 | 0 | 90s | - | 0s |
| `failure-only` | 2 | 0 | 0 | 1 | 107s | 2s | 1s |
| `full-harness` | 2 | 0 | 0 | 1 | 82s | 1s | 1s |
| `workflow-only` | 2 | 0 | 0 | 0 | 97s | - | 0s |
```

The two no-observed-repo-change records were not no-edit stalls. The agent
exited almost immediately after the Claude session-limit message, before the
240-second no-edit watchdog could fire.

## Reading

What held:

- The price-policy glossary-token patch behaved as intended.
- Price-policy separated cleanly under the patched oracle: decision-bearing
  arms passed 2/2 strict and record-consistent checks, while controls stayed
  0/2 record-consistent.
- No record hit the no-edit or idle watchdog.
- No record edited wrong or forbidden files.

What did not hold:

- The run cannot be used as representative two-family H1 evidence because
  Claude session limits contaminated three replenishment records.
- The current stop-on-abnormal path did not treat the known Claude
  session-limit message as a scheduler-stopping abnormal signal. The records
  completed as non-zero agent exits with verification failures.
- Replenishment cannot be compared across arms from this run.

## Decision

Keep the price-policy oracle patch. It removed the wording false negative
without allowing the control arms to pass record-consistency.

Do not promote from this run. Repeat either the replenishment half or the full
four-arm gate after Claude quota reset, or teach the runner to classify known
agent quota/session-limit messages as abnormal before another live gate.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T103253Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T103253Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-h1-claude-four-arm-gate-patched-oracle-session-limit.md`
