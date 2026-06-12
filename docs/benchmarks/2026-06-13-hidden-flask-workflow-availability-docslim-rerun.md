# Hidden Flask Workflow Availability Doc-Slim Rerun - 2026-06-13

This targeted rerun checks the specific blocker from the aborted 96-record
promotion: `workflow-only` `availability-badge` stopped after 360 seconds with
no repository changes.

Before rerunning, the `workflow-only` target guidance was trimmed into the same
short benchmark feature fast path used by the memory target. This did not add
generalized failure memory or task-specific hidden answers to `workflow-only`.

## Run Conditions

- Task: `hidden-effect-availability-badge`
- Arm: `workflow-only`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Planned records: 1
- Completed records: 1
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Prompt guard: `CODEX_PROMPT_GUARD=1`

Target ref:

- `workflow-only`: `../flask-yes-harness` at
  `3933a09a74cfefbd8455eb3aecd1ff225d7a7457`

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 -m harness_agent_benchmark_runner run \
  --task benchmarks/tasks/flask-hidden-three-arm-stable4/hidden-effect-availability-badge-workflow-only.json \
  --agent-command "python3 $PWD/examples/agents/codex_exec_agent.py" \
  --workspace runs/hidden-flask-workflow-availability-docslim-rerun-20260612T2248Z \
  --results results/hidden-flask-workflow-availability-docslim-rerun-20260612T2248Z \
  --max-agent-timeout 900 \
  --max-cost-usd 1.0 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 360
```

## Result

| Target | Task | Runs | Strict | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | Duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `workflow-only` | `hidden-effect-availability-badge` | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 88s |

Changed files in the isolated run:

- `app/__init__.py`
- `app/catalog.py`
- `docs/domain/glossary.md`
- `tests/test_app.py`

The remaining functional failure was:

```text
hidden oracle failure: missing SKU must return product_not_found
```

## Interpretation

The targeted no-edit reproduction cleared: the same task/arm that stopped at
360 seconds during promotion completed in 88 seconds with normal file changes.
This is an operational mitigation signal, not product-value evidence.

Because the `workflow-only` target ref changed, the previous two clean readiness
rounds no longer apply. The next readiness step is to rebuild the full
three-arm clean gate with the updated `workflow-only` ref before any new
promotion attempt.

