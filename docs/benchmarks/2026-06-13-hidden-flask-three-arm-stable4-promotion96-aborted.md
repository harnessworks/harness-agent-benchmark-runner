# Hidden Flask Three-Arm Stable-4 Promotion-96 Aborted - 2026-06-13

This run attempted the balanced near-100 three-arm promotion after two clean
12-record readiness rounds. The promotion guard passed, but the live promotion
aborted at record 2 of 96 due to a `workflow-only` no-edit watchdog stop.

Do not treat this as clean product evidence. The larger run reconfirmed that
intermittent first-edit latency remains a promotion blocker.

## Readiness Inputs

Two clean 12-record rounds were available before promotion:

- `results/hidden-flask-three-arm-stable4-docslim-pilot-20260612T2202Z`
- `results/hidden-flask-three-arm-stable4-docslim-secondround-20260612T2220Z`

Combined readiness coverage:

- 12 task/arm pairs
- 2 clean rounds per pair
- 24 prior records
- 0 stalls
- 0 timeouts
- 0 hidden-access findings
- 0 wrong-file edits
- 0 forbidden-file edits

The dry-run promotion guard accepted the combined readiness results:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-three-arm-stable4.json \
  --repeats 8 \
  --promotion-run \
  --require-clean-results results/hidden-flask-three-arm-stable4-docslim-2round-combined-20260612T2240Z \
  --min-clean-rounds 2 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 360 \
  --stop-on-abnormal
```

It reported:

```text
Clean readiness coverage: 12 task/arm pair(s) x 2 clean round(s); 24 prior record(s)
Planned runs: 96
```

## Promotion Run Conditions

- Suite: `benchmarks/suites/flask-hidden-three-arm-stable4.json`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `bare`, `workflow-only`, `memory-harness`
- Tasks: `availability-badge`, `cart-validation`, `catalog-metrics`,
  `catalog-segments`
- Repeats: 8
- Planned records: 96
- Completed records: 2
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Promotion run: enabled
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Prompt guard: `CODEX_PROMPT_GUARD=1`

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-three-arm-stable4.json \
  --repeats 8 \
  --promotion-run \
  --require-clean-results results/hidden-flask-three-arm-stable4-docslim-2round-combined-20260612T2240Z \
  --min-clean-rounds 2 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 360 \
  --stop-on-abnormal \
  --workspace runs/hidden-flask-three-arm-stable4-docslim-promotion96-20260612T2240Z \
  --results results/hidden-flask-three-arm-stable4-docslim-promotion96-20260612T2240Z \
  --execute
```

## Result

| Target | Task | Runs | Strict | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | Duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | `hidden-effect-availability-badge` | 1 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 93s |
| `workflow-only` | `hidden-effect-availability-badge` | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 1 | 0 | 0 | 360s |

The abnormal record:

- Run id: `20260612T223806Z-hidden-effect-availability-badge-151f03b4`
- Target: `workflow-only`
- Task: `hidden-effect-availability-badge`
- Termination: `no_edit_watchdog`
- Changed files: none
- Agent duration: 360 seconds

The agent read the app, catalog, tests, conventions, README, and route-related
references. It then stated that it was ready to edit, but the no-edit watchdog
fired before any repository change became visible.

## Interpretation

The clean 2-round readiness pilot was not sufficient to protect the 96-record
promotion from first-edit latency. The blocker is now broader than the memory
arm: this abort happened in `workflow-only` on `availability-badge`.

The likely mitigation is to apply the same short benchmark-feature fast path to
the `workflow-only` target that helped the memory target. That keeps
`workflow-only` distinct from `memory-harness`: it receives workflow/gate/docs
guidance only, not generalized failure memory.

Do not restart the 96-record promotion until the `workflow-only`
`availability-badge` no-edit case is targeted and the full two-clean-round gate
is re-established for the updated workflow-only ref.

