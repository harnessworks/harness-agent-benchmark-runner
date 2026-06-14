# Flask H1 Strengthened Promotion96 Aborted On No-Output No-Edit - 2026-06-14

This was the scoped 96-record H1 promotion attempt after the strengthened
prompt guard completed a clean 16-record decision-bearing gate.

The promotion stopped after 8/96 planned records because a `full-harness`
`hidden-effect-catalog-replenishment-policy` record hit the no-edit watchdog.
Unlike earlier H1 no-edit stops, this stopped record produced no assistant
message and made no repository changes. The agent log only showed Codex CLI
startup text, the full user prompt, and repeated rollout state warnings before
the no-edit watchdog stopped the process.

This is best classified as a startup/no-output no-edit event, not a
decision-record discovery or implementation-planning failure.

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
- Completed records before stop: 8
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Promotion mode: `--promotion-run`
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Prompt mitigation: strengthened adapter default guard says not to stop after
  narrating a plan, and to make the first small scoped app/test/docs edit
  immediately
- Clean readiness:
  `results/hidden-flask-ab-pilot-20260614T061356Z`
- Minimum prior clean rounds: 2 per selected task/arm pair
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 240`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Runner ref: `658e634bc304828190eb3190ac77a47c80811a9a`
- Started: `2026-06-14T08:53:48Z`
- Finished: `2026-06-14T09:05:49Z`

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
| `workflow-only` | 2 | 0 | 1 | 2 | 2 | 2 | 0/2 | 0 | 0 | 0 | 0 | 53s | 60s |
| `decision-only` | 2 | 2 | 2 | 2 | 2 | 2 | 2/2 | 0 | 0 | 0 | 0 | 53s | 60s |
| `failure-only` | 2 | 0 | 2 | 2 | 2 | 2 | 0/2 | 0 | 0 | 0 | 0 | 55s | 66s |
| `full-harness` | 2 | 1 | 1 | 1 | 1 | 2 | 1/2 | 1 | 1 | 0 | 0 | 43s | 240s |

Overall:

- Completed records: 8/96
- Strict successes: 3/8
- Decision-bearing strict successes: 3/4
- Control-arm strict successes: 0/4
- Record consistency: 3/8
- Decision-bearing record consistency: 3/4
- Control-arm record consistency: 0/4
- Stalls/timeouts: 1
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Hidden-access findings: 0

## Stop Reason

Stopped run:

| Run ID | Arm | Task | Duration | Seconds without repo change | Last phase |
| --- | --- | --- | ---: | ---: | --- |
| `20260614T090139Z-hidden-effect-catalog-replenishment-policy-6e5b0aef` | `full-harness` | `hidden-effect-catalog-replenishment-policy` | 240.1s | 240.1s | `unknown` |

`scripts/triage_no_edit_stalls.py` reported:

```text
## No-Edit Stall Triage

No-edit watchdog records: 1

| Run ID | Target | Task | No-edit class | Duration | Seconds without repo change | Seconds since last output | Last Codex phase | Last Codex message |
| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `20260614T090139Z-hidden-effect-catalog-replenishment-policy-6e5b0aef` | `full-harness` | `hidden-effect-catalog-replenishment-policy` | startup/no-output | 240.1s | 240.1s | 239.7s | unknown | - |
```

The agent log contained:

- Codex CLI startup metadata.
- The full benchmark prompt, including the strengthened prompt guard.
- Repeated `state db discrepancy ... falling_back` warnings.
- No assistant message.
- No tool command output from the model.
- `Stopped by no-edit watchdog after 240 seconds without repository changes.`

The stopped worktree had no file changes. The local harness gate passed against
the unchanged repository, and the hidden functional, schema, and
record-consistency checks failed with 404 because
`/catalog/replenishment-policy` was still absent.

## Reading

What held:

- The clean-readiness gate was enforced.
- The first seven records behaved as expected: decision-bearing arms passed,
  controls stayed record-inconsistent, and no boundary issues occurred.
- The no-edit watchdog stopped a non-progressing agent before the full timeout.

What failed:

- The strengthened prompt guard did not prevent a startup/no-output no-edit
  event at promotion scale.
- The stopped run did not get far enough for decision-record lookup, planning,
  or implementation behavior to matter.
- The 96-record H1 promotion is still not achieved.

## Decision

Do not keep rerunning blind H1 promotions.

This stop has a different shape from the prior planning-stage no-edit stops.
The next useful work is adapter or runner handling for startup/no-output
no-edit events, for example:

- keep no-output no-edit classified separately from post-planning no-edit;
- consider a bounded retry only for no-output/no-change startup failures;
- keep post-planning no-edit as a real abnormal result;
- rerun a small diagnostic before another scoped promotion.

The H1 effect signal remains promising in partial data, but promotion-scale
operational stability is still unresolved.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-large-20260614T085347Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-large-20260614T085347Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-h1-strengthened-promotion96-aborted-nooutput.md`
