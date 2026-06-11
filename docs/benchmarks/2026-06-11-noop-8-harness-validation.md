# Harness Validation — 8-Task No-Op Pass

Date: 2026-06-11
Target: `harnessworks/harness-starter-kit` @ `main` (`af55924`)
Runner: this repository (`harness-agent-benchmark-runner`)

## What this run is

This is a **harness validation** pass, not an agent score. It drives all eight
official `harness-starter-kit` benchmark task specs through the runner using the
bundled **no-op agent** (`examples/agents/noop_agent.py`), which makes no edits.
Its purpose is to prove the runner clones in isolation, executes each task's
deterministic verification oracle, and scores file boundaries correctly.

It acts as a negative-control run: every task should fail because the adapter
makes no edits. See "Reproducing a real agent run" below for the same runner
path with an authenticated agent adapter.

## Runner integrity

`python3 -m unittest discover -s tests` → **5 tests, OK**.

## No-op 8-task result

| Metric | Value |
| --- | ---: |
| Runs | 8 |
| Successes | 0 |
| Verification passed | 0 |
| Wrong-file edits | 0 |
| Forbidden-file edits | 0 |
| Agent timeouts | 0 |
| Runner errors | 0 |

All eight runs completed cleanly (agent exit `0`, no runner errors) and every
task's oracle **correctly rejected the empty change set**. Because the no-op
agent edits nothing, zero successes is the expected and desired outcome — it
confirms the oracles are not trivially passing.

| Task | Success | Verify | Failing oracle (expected) |
| --- | --- | --- | --- |
| command-workflow-refresh-benchmark-guidance | False | False | refresh workflow oracle |
| decision-memory-benchmark-ownership-adr | False | False | decision record oracle |
| docs-only-evaluation-benchmark-ownership | False | False | benchmark ownership text oracle |
| failure-memory-benchmark-noop-oracle-gap | False | False | failure note oracle |
| forbidden-file-structure-ignore-runner-output | False | False | structure rules oracle |
| installer-non-destructive-list-profiles | False | False | list profiles oracle |
| profile-boundary-go-race-check | False | False | go profile boundary oracle |
| small-bugfix-docs-drift-uv-command | False | False | uv command oracle |

Raw results: `results/noop-8-harness-validation/2026-06-11.jsonl`.

## Comparison: agent runs (same 8 tasks)

For reference, the existing agent runs against the same task set:

| Run | Agent | Runs | Successes | Wrong-file | Forbidden | Timeouts |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| codex-dry-run-8 | Codex CLI | 8 | 7 | 0 | 0 | 0 |
| codex-dry-run-8-oracle-fix | Codex CLI | 8 | 8 | 0 | 0 | 0 |
| claude-as-agent-8 | Claude Opus, patch replay | 8 | 8 | 0 | 0 | 0 |

In `codex-dry-run-8`, the single failure was
`command-workflow-refresh-benchmark-guidance`, where the oracle checked exact
phrases without normalizing line-wrapped text — a brittle oracle, not an agent
boundary violation. The `oracle-fix` run reached 8/8 after that oracle was
corrected.

Read together, the no-op pass (oracles correctly fail on no work) and the
Codex/Claude passes (oracles correctly pass on correct work) bracket the
harness: the eight oracles distinguish "no work" from "correct work" with no
false positives or false negatives observed.

## Reproducing a real agent run

On a machine with an authenticated agent CLI, run from the runner root:

```bash
for t in benchmarks/tasks/*.json; do   # or the 8 specs in the target repo
  python3 -m harness_agent_benchmark_runner run \
    --task "$t" \
    --agent-command "python3 $PWD/examples/agents/codex_exec_agent.py" \
    --max-agent-timeout 900 --max-cost-usd 2.5
done
python3 -m harness_agent_benchmark_runner summarize --results results
```

Swap `codex_exec_agent.py` for a Claude Code / Aider / custom adapter as needed
(adapter contract is in the README).

### Environment notes for this sandbox

- The runner's workspace and results dirs must live on the local filesystem
  (e.g. `/tmp`), not the mounted folder: git's clone hardlink/lock operations
  are blocked on the mount, which surfaces as `CalledProcessError` (git exit
  128). This run used `--workspace /tmp/... --results /tmp/...` and copied the
  JSONL back.
- The eight task specs were taken from the target repo
  (`benchmarks/tasks/*.json` in `harness-starter-kit`); this runner repo ships
  only `harness-starter-kit-smoke.json`.
