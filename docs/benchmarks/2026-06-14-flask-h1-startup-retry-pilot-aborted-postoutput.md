# Flask H1 Startup-Retry Pilot Aborted On Post-Output No-Edit - 2026-06-14

This was a small H1 operational pilot after adding
`--retry-startup-no-output-once` to the Flask A/B wrapper.

The pilot was intentionally not a 96/100-record promotion. It checked whether
the runner could absorb only startup/no-output no-edit events while still
treating post-planning or post-output no-edit as real abnormal results.

The run stopped after 1/8 planned records. The stopped record was not eligible
for startup retry: the agent found the accepted price-band decision, announced
that it was making the first scoped edit, and then made no repository changes
before the no-edit watchdog fired.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Tasks:
  - `hidden-effect-catalog-price-policy`
  - `hidden-effect-catalog-replenishment-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `decision-only`, `full-harness`
- Repeats: 2
- Planned records: 8
- Completed records before stop: 1
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Startup retry: `--retry-startup-no-output-once`
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 240`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Runner ref: `7dd11282c5d0c499c3c1b2f3eed46bf7340cca47`
- Started: `2026-06-14T09:21:14Z`
- Finished: `2026-06-14T09:25:32Z`

Target refs:

| Arm | Source | Ref |
| --- | --- | --- |
| `decision-only` | `../flask-decision-only` | `e9b0a3e919a7827497c7163912a1023c2346008f` |
| `full-harness` | `../flask-memory-harness` | `ba8b3963d071089429fa2c2c8ebc10049e80cca4` |

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --mode pilot \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-price-policy \
  --task-id hidden-effect-catalog-replenishment-policy \
  --arms decision-only,full-harness \
  --repeats 2 \
  --arm-order rotate \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal \
  --retry-startup-no-output-once \
  --execute
```

## Result Before Stop

| Arm | Completed | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | Duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 1 | 0 | 0 | 0 | 0 | 1 | 0/1 | 1 | 1 | 0 | 0 | 240.0s |

Overall:

- Completed records: 1/8
- Strict successes: 0/1
- Verification passed: 0/1
- Startup retries used: 0
- Stalls/timeouts: 1
- Wrong-file edits: 0
- Forbidden-file edits: 0
- Hidden-access findings: 0

## Stop Reason

Stopped run:

| Run ID | Arm | Task | No-edit class | Duration | Seconds without repo change | Seconds since last output | Last phase |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| `20260614T092114Z-hidden-effect-catalog-price-policy-ff7220f4` | `decision-only` | `hidden-effect-catalog-price-policy` | `after-agent-output` | 240.0s | 240.0s | 27.4s | `after-agent-output` |

`scripts/triage_no_edit_stalls.py` reported:

```text
## No-Edit Stall Triage

No-edit watchdog records: 1

| Run ID | Target | Task | No-edit class | Duration | Seconds without repo change | Seconds since last output | Last Codex phase | Last Codex message |
| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |
| `20260614T092114Z-hidden-effect-catalog-price-policy-ff7220f4` | `decision-only` | `hidden-effect-catalog-price-policy` | after-agent-output | 240.0s | 240.0s | 27.4s | after-agent-output | I’m making the first scoped edit now: a catalog helper that returns deterministic price-policy rows plus summary counts, the new route, and focused assertions for shape, ordering,… |
```

The agent log showed that the agent:

- searched the decision records;
- found the accepted catalog price-band policy;
- restated the correct thresholds;
- announced an immediate scoped edit;
- produced no repository changes before the no-edit watchdog stopped it.

The stopped worktree had no changed files. Hidden functional, schema, workflow,
and record-consistency checks failed because the endpoint was never
implemented.

## Reading

What held:

- The new startup retry gate stayed narrow. It did not retry a post-output
  no-edit failure.
- The no-edit triage separated this from the prior startup/no-output event.
- File-boundary and hidden-access signals stayed clean.

What failed:

- The H1 operational bottleneck is not limited to startup/no-output.
- The strengthened prompt guard still allows a post-output, pre-edit stall.
- A blind 96/100-record H1 promotion remains low-value.

## Decision

Stop H1 promotion reruns for now.

The next useful work is not another 100-run. It is a smaller adapter or agent
diagnostic focused on why Codex can announce an immediate edit and then fail to
issue any repository-changing command. Startup-only retry remains useful for
infrastructure startup silence, but it does not address this post-output
no-edit path and should not be broadened to hide it.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T092114Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T092114Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-h1-startup-retry-pilot-aborted-postoutput.md`
