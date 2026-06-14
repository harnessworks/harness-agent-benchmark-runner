# Flask H1 Promotion96 Aborted On No-Edit - 2026-06-14

This was the scoped 96-record H1 promotion attempt after the revised-oracle
two-family gate completed cleanly. It used the two direct decision-memory task
families, four non-bare arms, and twelve repeats.

The run stopped after 11/96 planned records because a `full-harness`
`hidden-effect-catalog-price-policy` record hit the no-edit watchdog. The
stopped agent read the coding conventions and found the accepted price-band
decision record, but made no repository changes for 240 seconds. This is an
operational promotion blocker, not a scoring ambiguity.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Tasks:
  - `hidden-effect-catalog-price-policy`
  - `hidden-effect-catalog-replenishment-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `workflow-only`, `decision-only`, `failure-only`, `full-harness`
- Repeats: 12
- Planned records: 96
- Completed records before stop: 11
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Promotion mode: `--promotion-run`
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Clean readiness:
  `results/hidden-flask-ab-pilot-20260614T061356Z`
- Minimum prior clean rounds: 2 per selected task/arm pair
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 240`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Runner ref: `66564d0874d7305a5fe3c76b438781e217d7af28`
- Started: `2026-06-14T06:46:42Z`
- Finished: `2026-06-14T07:05:18Z`

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
  --mode large \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-price-policy \
  --task-id hidden-effect-catalog-replenishment-policy \
  --arms workflow-only,decision-only,failure-only,full-harness \
  --repeats 12 \
  --allow-small-large \
  --promotion-run \
  --require-clean-results results/hidden-flask-ab-pilot-20260614T061356Z \
  --min-clean-rounds 2 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal \
  --execute
```

## Headline Before Stop

| Arm | Completed | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `workflow-only` | 2 | 0 | 2 | 2 | 2 | 2 | 0/2 | 0 | 0 | 0 | 0 | 53s | 64s |
| `decision-only` | 3 | 3 | 3 | 3 | 3 | 3 | 3/3 | 0 | 0 | 0 | 0 | 58s | 75s |
| `failure-only` | 3 | 0 | 2 | 3 | 3 | 3 | 0/3 | 0 | 0 | 0 | 0 | 50s | 64s |
| `full-harness` | 3 | 2 | 2 | 2 | 2 | 3 | 2/3 | 1 | 1 | 0 | 0 | 69s | 240s |

Overall:

- Completed records: 11/96
- Strict successes: 5/11
- Decision-bearing strict successes: 5/6
- Control-arm strict successes: 0/5
- Record consistency: 5/11
- Decision-bearing record consistency: 5/6
- Control-arm record consistency: 0/5
- Stalls/timeouts: 1
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Hidden-access findings: 0

## Stop Reason

Stopped run:

| Run ID | Arm | Task | Duration | Seconds without repo change | Last phase |
| --- | --- | --- | ---: | ---: | --- |
| `20260614T070107Z-hidden-effect-catalog-price-policy-38f21a0e` | `full-harness` | `hidden-effect-catalog-price-policy` | 240.0s | 240.0s | `after-agent-output` |

`scripts/triage_no_edit_stalls.py` reported:

```text
## No-Edit Stall Triage

No-edit watchdog records: 1

Run ID: 20260614T070107Z-hidden-effect-catalog-price-policy-38f21a0e
Target: full-harness
Task: hidden-effect-catalog-price-policy
Duration: 240.0s
Seconds without repo change: 240.0s
Seconds since last output: 27.5s
Last Codex phase: after-agent-output
```

The agent log showed the agent read `docs/conventions/coding.md`, then said it
was checking accepted decision records for the exact price-band labels and
thresholds. It then ran:

```text
rg -n "price|band|catalog" docs/decisions
```

The command found `docs/decisions/0002-adopt-catalog-price-band-policy.md`,
including the accepted labels and thresholds:

- `budget`: price below 10.00
- `standard`: price from 10.00 up to but not including 35.00
- `premium`: price 35.00 or higher
- response key `price_band`

No files changed before the watchdog stopped the agent. The stopped worktree's
route table still lacked `/catalog/price-policy`, so functional, schema, and
record-consistency checks all failed with 404.

## Partial Signal

Before the stop, the scoring pattern still matched H1:

- `decision-only` was 3/3 strict and record-consistent.
- Completed `full-harness` records before the stopped one were 2/2 strict and
  record-consistent.
- `workflow-only` and `failure-only` were 0/5 record-consistent across completed
  control records.
- No completed record touched wrong or forbidden files.

This partial signal is not enough for promotion because the run stopped on an
operational abnormal event.

## Reading

What held:

- The clean-readiness gate worked: 8 selected task/arm pairs had two prior
  clean records before the promotion attempt.
- The early completed records continued to separate decision-bearing arms from
  controls.
- The stop captured a concrete no-edit failure instead of allowing a silent
  hang.

What failed:

- `full-harness` price-policy still has intermittent no-edit behavior even
  after a clean 16-record gate.
- The no-edit happened after the agent found the relevant decision record, so
  this is not a discoverability failure alone.
- The 96-record promotion was not achieved.

## Decision

Do not claim the H1 promotion as complete.

The next useful work is targeted operational mitigation before another
promotion attempt:

- run a focused `full-harness` price-policy no-edit diagnostic with several
  repeats;
- compare whether the stall occurs after decision-record lookup or before any
  useful output;
- consider a prompt/adapter mitigation that forces an early minimal file edit
  plan after decision lookup, without exposing task answers;
- rerun a smaller gate after mitigation before attempting another 96-record
  promotion.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-large-20260614T064642Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-large-20260614T064642Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-h1-promotion96-aborted-noedit.md`
