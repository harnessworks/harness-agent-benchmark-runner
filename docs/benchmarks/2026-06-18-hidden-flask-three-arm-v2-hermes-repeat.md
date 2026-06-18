# Hidden Flask Three-Arm V2 Hermes Repeat - 2026-06-18

This repeat ran the same v2 held-out three-arm matrix as the earlier v2 pilot,
but used a temporary Hermes CLI adapter because the local Codex CLI binary was
not installed and the local Claude Code CLI returned an authentication error.
Treat this as useful adapter-diversity evidence, not a direct replacement for
the Codex v2 pilot and not a replacement for the 96-record stable-4
representative result.

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
- Prompt guard: `CODEX_PROMPT_GUARD=1` with equivalent guard text in the Hermes
  adapter
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 180`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: temporary `/tmp/hermes_benchmark_agent.py`
- Hermes CLI: available locally through `hermes -z`
- Started: `2026-06-18T06:56:15Z`
- Finished: `2026-06-18T07:10:28Z`

Target refs:

| Arm | Source | Ref |
| --- | --- | --- |
| `bare` | `../flask-no-harness` | `b5351eae78ed9f17d46a43eee05354e9e13f6b94` |
| `workflow-only` | `../flask-yes-harness` | `3b3b5c5a295b0b025ea3519debaddfbed09c2ecd` |
| `memory-harness` | `../flask-memory-harness` | `00e3d5170bde7e5451f525f5ac011f16b6df2edb` |

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-three-arm-v2.json \
  --mode pilot \
  --task-limit 3 \
  --repeats 1 \
  --stop-on-abnormal \
  --agent-timeout-override 900 \
  --agent-no-edit-timeout 360 \
  --agent-idle-timeout 180 \
  --agent-command '/tmp/hermes_benchmark_agent.py' \
  --execute
```

## Headline

| Target | Runs | Strict | Functional | Schema contract | Workflow | Boundary | Verification passed | Wrong-file edits | Forbidden-file edits | Stalls | Timeouts | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 3 | 0 | 0 | 0 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 60s | 86s |
| `workflow-only` | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 102s | 119s |
| `memory-harness` | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 90s | 103s |

The runner printed `Completed schedule with 3 non-zero runner exits`. Those
three non-zero exits are the expected `bare` benchmark failures, not runner
abnormal events.

## Per-Task Results

| Target | Task | Strict | Functional | Schema contract | Workflow | Boundary | Duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | `hidden-effect-replenishment-signals` | 0 | 0 | 0 | 1 | 1 | 60s |
| `workflow-only` | `hidden-effect-replenishment-signals` | 1 | 1 | 1 | 1 | 1 | 102s |
| `memory-harness` | `hidden-effect-replenishment-signals` | 1 | 1 | 1 | 1 | 1 | 75s |
| `bare` | `hidden-effect-catalog-price-ladder` | 0 | 0 | 0 | 1 | 1 | 48s |
| `workflow-only` | `hidden-effect-catalog-price-ladder` | 1 | 1 | 1 | 1 | 1 | 119s |
| `memory-harness` | `hidden-effect-catalog-price-ladder` | 1 | 1 | 1 | 1 | 1 | 90s |
| `bare` | `hidden-effect-catalog-value-snapshot` | 0 | 0 | 0 | 1 | 1 | 86s |
| `workflow-only` | `hidden-effect-catalog-value-snapshot` | 1 | 1 | 1 | 1 | 1 | 99s |
| `memory-harness` | `hidden-effect-catalog-value-snapshot` | 1 | 1 | 1 | 1 | 1 | 103s |

## Interpretation

This repeat reproduced the same high-level v2 separation pattern with a Hermes
adapter:

- `bare` stayed 0/3 strict, 0/3 functional, and 0/3 schema-contract.
- `workflow-only` passed 3/3 strict.
- `memory-harness` passed 3/3 strict.
- All 9 records were clean for preflight, stalls, timeouts, wrong-file edits,
  forbidden-file edits, and boundary checks.

The useful reading is narrow: the v2 task family again separated harnessed repos
from the bare repo on repo-local API/schema/docs conventions. It still does not
show an accuracy advantage for `memory-harness` over `workflow-only`, because
both harness arms passed all three tasks.

Because this run used a Hermes adapter rather than the Codex adapter from the
previous v2 pilot, it should be reported as adapter-diversity evidence. It
should not be merged into the Codex pilot as a direct repeat and should not
replace the 96-record stable-4 representative result.

## Local Adapter Notes

The intended Codex repeat could not run in this local environment because the
adapter failed immediately with:

```text
FileNotFoundError: [Errno 2] No such file or directory: 'codex'
```

A Claude Code fallback was also unavailable because `claude -p` returned:

```text
Failed to authenticate. API Error: 401 Invalid authentication credentials
```

A temporary Hermes CLI adapter was therefore used for this local evidence run.
The adapter read `BENCHMARK_PROMPT_FILE`, prepended the same generic benchmark
prompt guard when `CODEX_PROMPT_GUARD=1`, and invoked `hermes -z` inside the
isolated clone with `terminal,file` toolsets.

## Decision

Publish this as the latest local v2 adapter-diversity repeat, while keeping the
2026-06-18 Codex v2 pilot as the comparable v2 Codex line and the 2026-06-13
stable-4 promotion96 as the representative result.

The next useful v2 step is still a comparable Codex repeat after installing or
restoring the Codex CLI, or a deliberately labeled 16/24-record Hermes adapter
gate if the product question shifts to Hermes as the evaluated agent.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260618T065615Z/2026-06-18.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260618T065615Z/`
- Failed Codex environment-check run:
  `results/hidden-flask-ab-pilot-20260618T065244Z/`
