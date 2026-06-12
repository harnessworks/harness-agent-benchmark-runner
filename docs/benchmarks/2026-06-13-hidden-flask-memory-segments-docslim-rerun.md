# Hidden Flask Memory Segments Doc-Slim Rerun - 2026-06-13

This targeted rerun checks the specific operational blocker from the previous
three-arm gate/memory pilot: `memory-harness` `catalog-segments` stopped after
360 seconds with no repository changes.

Before rerunning, the memory target guidance was trimmed and made more
action-oriented:

- `AGENTS.md` now starts with a benchmark feature fast path.
- `docs/conventions/coding.md` was shortened into a public API checklist.
- Generalized memory remains, but agents are told not to read full failure
  records unless the task or a gate failure points there.
- No held-out route names, hidden oracle payloads, task-specific versions, or
  exact hidden answer strings were added to target docs.

## Run Conditions

- Task: `hidden-effect-catalog-segments`
- Arm: `memory-harness`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Repeats: 1
- Planned records: 1
- Completed records: 1
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Prompt guard: `CODEX_PROMPT_GUARD=1`

Target ref:

- `memory-harness`: `../flask-memory-harness` at
  `87c12fb5e276e40272ceee86d497823e93def4e9`

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 -m harness_agent_benchmark_runner run \
  --task benchmarks/tasks/flask-hidden-three-arm-stable4/hidden-effect-catalog-segments-memory-harness.json \
  --agent-command "python3 $PWD/examples/agents/codex_exec_agent.py" \
  --workspace runs/hidden-flask-memory-segments-docslim-rerun-20260612T2159Z \
  --results results/hidden-flask-memory-segments-docslim-rerun-20260612T2159Z \
  --max-agent-timeout 900 \
  --max-cost-usd 1.0 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 360
```

## Result

| Target | Task | Runs | Strict | Functional | Schema contract | Workflow | Boundary | Hidden access | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | Duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `memory-harness` | `hidden-effect-catalog-segments` | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 76s |

Changed files in the isolated run:

- `app/__init__.py`
- `app/catalog.py`
- `docs/domain/glossary.md`
- `tests/test_app.py`

## Interpretation

This targeted rerun clears the immediate `memory-harness`
`catalog-segments` no-edit reproduction: the same task/arm that previously
stopped at 360 seconds completed in 76 seconds and passed strict scoring.

This is not enough to promote to a 100-run experiment. It is one targeted
record after a documentation-shape change. The next evidence step should be a
fresh full 12-record three-arm stable-4 pilot using the trimmed memory target.
Promotion should remain blocked unless that full pilot has 0 no-edit watchdog
stops and a product signal worth scaling.

