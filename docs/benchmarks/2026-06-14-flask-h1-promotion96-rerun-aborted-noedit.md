# Flask H1 Promotion96 Rerun Aborted On No-Edit - 2026-06-14

This was the second scoped 96-record H1 promotion attempt after the
revised-oracle two-family gate completed cleanly and a focused
`full-harness` price-policy diagnostic did not reproduce the prior no-edit
watchdog.

The rerun stopped after 13/96 planned records because a `decision-only`
`hidden-effect-catalog-replenishment-policy` record hit the no-edit watchdog.
The stopped agent announced that it would stay scoped to the app, tests, and
domain/convention docs, then look for the adopted replenishment policy before
editing. It made no repository changes for 240 seconds.

This is the second aborted H1 promotion at this scale. The no-edit stop
occurred on a different arm and task than the prior promotion stop, so blind
promotion reruns are no longer a good use of budget until the operational
no-edit path is mitigated or explicitly studied.

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
- Completed records before stop: 13
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
- Runner ref: `e80e1fcd5f4c6f7c50d67dff8dce7c756288c4d1`
- Started: `2026-06-14T07:17:42Z`
- Finished: `2026-06-14T07:38:25Z`

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
| `workflow-only` | 3 | 0 | 2 | 3 | 3 | 3 | 0/3 | 0 | 0 | 0 | 0 | 60s | 62s |
| `decision-only` | 4 | 3 | 3 | 3 | 3 | 4 | 3/4 | 1 | 1 | 0 | 0 | 53s | 240s |
| `failure-only` | 3 | 0 | 2 | 3 | 3 | 3 | 0/3 | 0 | 0 | 0 | 0 | 59s | 85s |
| `full-harness` | 3 | 3 | 3 | 3 | 3 | 3 | 3/3 | 0 | 0 | 0 | 0 | 53s | 56s |

Overall:

- Completed records: 13/96
- Strict successes: 6/13
- Decision-bearing strict successes: 6/7
- Control-arm strict successes: 0/6
- Record consistency: 6/13
- Decision-bearing record consistency: 6/7
- Control-arm record consistency: 0/6
- Stalls/timeouts: 1
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Hidden-access findings: 0

## Stop Reason

Stopped run:

| Run ID | Arm | Task | Duration | Seconds without repo change | Last phase |
| --- | --- | --- | ---: | ---: | --- |
| `20260614T073348Z-hidden-effect-catalog-replenishment-policy-e29d0c4b` | `decision-only` | `hidden-effect-catalog-replenishment-policy` | 240.0s | 240.0s | `post-planning` |

`scripts/triage_no_edit_stalls.py` reported:

```text
## No-Edit Stall Triage

No-edit watchdog records: 1

Run ID: 20260614T073348Z-hidden-effect-catalog-replenishment-policy-e29d0c4b
Target: decision-only
Task: hidden-effect-catalog-replenishment-policy
Duration: 240.0s
Seconds without repo change: 240.0s
Seconds since last output: 36.1s
Last Codex phase: post-planning
Last Codex message: I'll keep this scoped to the app, tests, and the domain/convention docs the repo guidance calls out, then look for the adopted replenishment policy before editing.
```

The agent log showed the stopped agent read `docs/domain/glossary.md`,
`tests/test_app.py`, and `docs/conventions/coding.md`. It did not make a
visible repository edit before the watchdog stopped it.

The stopped worktree still lacked `/catalog/replenishment-policy`. The harness
gate passed, but the hidden functional, schema, and record-consistency checks
failed with 404.

## Partial Signal

Before the stop, the scoring pattern still matched H1:

- `decision-only` was 3/4 strict and record-consistent, with the only miss
  being the stopped no-edit record.
- `full-harness` was 3/3 strict and record-consistent.
- `workflow-only` and `failure-only` were 0/6 record-consistent across control
  records.
- No completed or stopped record touched wrong or forbidden files.

This partial signal is not enough for promotion because the run stopped on an
operational abnormal event.

## Reading

What held:

- The clean-readiness gate worked: all selected task/arm pairs had prior clean
  evidence before the promotion attempt.
- The early completed records continued to separate decision-bearing arms from
  controls.
- The no-edit watchdog preserved a concrete stop reason instead of letting the
  run hang silently.

What failed:

- H1 promotion-scale execution is not operationally stable yet.
- The second no-edit stop appeared on a different task/arm pair than the first
  promotion stop, so the failure mode is broader than one unlucky
  `full-harness` price-policy record.
- A focused diagnostic that does not reproduce one stopped pair is not enough
  evidence to keep rerunning blind 96-record promotions.

## Decision

Do not run another blind 96-record or 100-record H1 promotion now.

The next useful work is one of:

- add an operational mitigation that causes agents to start a minimal scoped
  implementation edit shortly after relevant record discovery, without exposing
  task answers;
- run a small no-edit-focused diagnostic matrix that intentionally measures
  time-to-first-edit across the decision-bearing arms and both H1 tasks;
- broaden task coverage only after no-edit behavior is either mitigated or
  accepted as the explicit variable under study.

Until then, a 100-run matrix would mostly measure promotion-scale no-edit
instability rather than the direct decision-memory H1 claim.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-large-20260614T071742Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-large-20260614T071742Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-h1-promotion96-rerun-aborted-noedit.md`
