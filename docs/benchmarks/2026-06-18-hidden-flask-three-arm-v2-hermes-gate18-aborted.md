# Hidden Flask Three-Arm V2 Hermes Gate18 Aborted - 2026-06-18

This attempted to expand the local Hermes adapter v2 line from the clean
9-record repeat to a two-repeat, 18-record gate across the same three v2 tasks
and three arms.

The gate did not complete. It stopped on the first planned record because the
Hermes adapter produced no stdout and no observed repository changes in the
isolated clone before the idle watchdog fired.

## Run Conditions

- Suite: `benchmarks/suites/flask-hidden-three-arm-v2.json`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Tasks:
  - `hidden-effect-replenishment-signals`
  - `hidden-effect-catalog-price-ladder`
  - `hidden-effect-catalog-value-snapshot`
- Arms: `bare`, `workflow-only`, `memory-harness`
- Repeats requested: 2
- Planned records: 18
- Completed records: 1
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Prompt guard: `CODEX_PROMPT_GUARD=1` with equivalent guard text in the Hermes
  adapter
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 180`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: temporary `/tmp/hermes_benchmark_agent.py`
- Started: `2026-06-18T07:17:48Z`
- Stopped: `2026-06-18T07:20:55Z`

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-hidden-three-arm-v2.json \
  --mode pilot \
  --task-limit 3 \
  --repeats 2 \
  --stop-on-abnormal \
  --agent-timeout-override 900 \
  --agent-no-edit-timeout 360 \
  --agent-idle-timeout 180 \
  --agent-command '/tmp/hermes_benchmark_agent.py' \
  --execute
```

## Observed Result

| Planned record | Target | Task | Strict | Functional | Schema contract | Workflow | Boundary | Stall/timeout |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | `bare` | `hidden-effect-replenishment-signals` | 0 | 0 | 0 | 0 | 1 | idle watchdog at 180s |

The runner stopped the schedule after the abnormal signal:

```text
Stopping schedule after abnormal signal:
- agent idle watchdog fired
```

The agent log for the first record ended with:

```text
exit_code: 124
duration_seconds: 180.025
Stopped by idle watchdog after 180 seconds without output.
```

The verification logs show the isolated clone did not receive the endpoint
implementation before scoring:

```text
hidden oracle failure: expected status 200, got 404
```

## Follow-Up Attempt

A follow-up attempt added `--retry-startup-no-output-once` and raised the idle
watchdog to 300 seconds, but planning stopped before live execution because the
local `../flask-no-harness` target source was dirty:

```text
benchmark plan error: dirty target repositories are not allowed:
/Users/wb/Desktop/flask-no-harness (M app/__init__.py)
```

The dirty local target files matched generated benchmark feature edits and were
cleaned so future runs are not blocked by this local side effect. The benchmark
runner repository itself was not dirty beyond the public-safe report/document
changes.

## Interpretation

This aborted gate does not invalidate the clean 9-record Hermes adapter repeat,
but it means the Hermes adapter line is not ready to be promoted as a larger
stable gate. The immediate blocker is operational: the temporary Hermes adapter
can enter a no-output/no-observed-clone-edit state and, in this local attempt,
left the source target dirty enough to block a retry.

Do not make a 16/18/24-record Hermes adapter claim from this attempt. Keep the
published successful Hermes evidence at the 9-record adapter-diversity repeat
until the adapter isolation and output/watchdog behavior are hardened.

## Decision

Do not rerun blind larger Hermes gates yet. Next useful work is to harden the
Hermes benchmark adapter before another gate attempt:

- make the adapter an in-repo example rather than a `/tmp` script;
- add a preflight smoke that verifies Hermes edits the isolated clone, not the
  source target repository;
- make the adapter emit a short startup line so the runner can distinguish
  true no-output stalls from a silent-but-active Hermes invocation;
- keep source-target cleanliness checks enabled.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260618T071748Z/2026-06-18.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260618T071748Z/`
- Retry planning attempt:
  `results/hidden-flask-ab-pilot-20260618T072158Z/`
