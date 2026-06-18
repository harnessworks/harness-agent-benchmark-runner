# Hidden Flask Three-Arm V2 Claude Pilot - 2026-06-18

This run repeated the v2 held-out three-arm matrix with the in-repo Claude Code
adapter after local Claude authentication was refreshed. It ran the three v2
partial-realistic tasks across `bare`, `workflow-only`, and `memory-harness`.

The run completed all 9 planned records with no operational abnormal signals:
0 stalls, 0 timeouts, 0 hidden-access findings, 0 wrong-file edits, and 0
forbidden-file edits.

## Run Conditions

- Suite: `benchmarks/suites/flask-hidden-three-arm-v2.json`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Tasks:
  - `hidden-effect-replenishment-signals`
  - `hidden-effect-catalog-price-ladder`
  - `hidden-effect-catalog-value-snapshot`
- Arms: `bare`, `workflow-only`, `memory-harness`
- Repeats: 1
- Planned records: 9
- Completed records: 9
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 180`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: `examples/agents/claude_code_agent.py`
- Claude Code: `2.1.172`
- Started: `2026-06-18T07:36:59Z`
- Finished: `2026-06-18T07:54:45Z`

Target refs:

| Arm | Source | Ref |
| --- | --- | --- |
| `bare` | `../flask-no-harness` | `b5351eae78ed9f17d46a43eee05354e9e13f6b94` |
| `workflow-only` | `../flask-yes-harness` | `3b3b5c5a295b0b025ea3519debaddfbed09c2ecd` |
| `memory-harness` | `../flask-memory-harness` | `00e3d5170bde7e5451f525f5ac011f16b6df2edb` |

Command:

```bash
python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-three-arm-v2.json \
  --mode pilot \
  --task-limit 3 \
  --repeats 1 \
  --stop-on-abnormal \
  --agent-timeout-override 900 \
  --agent-no-edit-timeout 360 \
  --agent-idle-timeout 180 \
  --agent-command "python3 $PWD/examples/agents/claude_code_agent.py" \
  --execute
```

## Headline

| Target | Runs | Strict | Functional | Schema contract | Workflow | Boundary | Verification passed | Wrong-file edits | Forbidden-file edits | Stalls | Timeouts | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 3 | 0 | 0 | 0 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 118s | 141s |
| `workflow-only` | 3 | 2 | 2 | 3 | 3 | 3 | 2 | 0 | 0 | 0 | 0 | 105s | 113s |
| `memory-harness` | 3 | 2 | 2 | 3 | 3 | 3 | 2 | 0 | 0 | 0 | 0 | 113s | 129s |

The runner printed `Completed schedule with 5 non-zero runner exits`. Three of
those were the expected `bare` benchmark failures. The other two were the
harness-arm replenishment functional failures described below.

## Per-Task Results

| Target | Task | Strict | Functional | Schema contract | Workflow | Boundary | Duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | `hidden-effect-replenishment-signals` | 0 | 0 | 0 | 1 | 1 | 141s |
| `workflow-only` | `hidden-effect-replenishment-signals` | 0 | 0 | 1 | 1 | 1 | 113s |
| `memory-harness` | `hidden-effect-replenishment-signals` | 0 | 0 | 1 | 1 | 1 | 113s |
| `bare` | `hidden-effect-catalog-price-ladder` | 0 | 0 | 0 | 1 | 1 | 118s |
| `workflow-only` | `hidden-effect-catalog-price-ladder` | 1 | 1 | 1 | 1 | 1 | 78s |
| `memory-harness` | `hidden-effect-catalog-price-ladder` | 1 | 1 | 1 | 1 | 1 | 129s |
| `bare` | `hidden-effect-catalog-value-snapshot` | 0 | 0 | 0 | 1 | 1 | 110s |
| `workflow-only` | `hidden-effect-catalog-value-snapshot` | 1 | 1 | 1 | 1 | 1 | 105s |
| `memory-harness` | `hidden-effect-catalog-value-snapshot` | 1 | 1 | 1 | 1 | 1 | 92s |

## Failure Cluster

All `bare` records failed functional and schema checks while keeping workflow and
boundary signals clean. That matches the intended negative-control pattern.

Both harness arms passed schema for `hidden-effect-replenishment-signals` but
failed the functional oracle with the same message:

```text
hidden oracle failure: desk-lamp stock is wrong
```

This means Claude followed the harnessed response envelope and workflow/docs
conventions, but did not preserve the hidden oracle's expected current catalog
stock value for that task. The failure should be treated as a task/agent
functional miss, not as a runner abnormal event: preflight, local harness gate,
schema, workflow, and boundary checks were clean for both harness arms.

## Interpretation

This Claude run is operationally clean and supports a narrower v2 reading than
the earlier clean 9-record Codex and Hermes runs:

- The harness arms still separated from `bare` on schema contract: 3/3 schema in
  both harness arms versus 0/3 in `bare`.
- The harness arms passed 2/3 strict and 2/3 functional, failing only the
  replenishment functional oracle.
- `bare` stayed 0/3 strict, 0/3 functional, and 0/3 schema.
- There were no stalls, timeouts, hidden-access findings, wrong-file edits, or
  forbidden-file edits.

The product claim remains narrow: harness guidance improves measurement and
helps preserve repo-local API/schema/docs conventions. This run does not support
an accuracy advantage for `memory-harness` over `workflow-only`; both harness
arms tied on all reported dimensions.

## Decision

Publish this as a clean Claude v2 pilot with a replenishment functional miss in
both harness arms. Do not promote it above the 96-record stable-4 representative
result. Use it as agent-diversity evidence and as a prompt/oracle review input
for the replenishment task family.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260618T073659Z/2026-06-18.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260618T073659Z/`
