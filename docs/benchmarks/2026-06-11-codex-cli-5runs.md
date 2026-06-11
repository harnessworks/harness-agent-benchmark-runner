# Live Agent Run - Codex CLI, 8 Tasks x 5 Repetitions

Date: 2026-06-11
Target: `harnessworks/harness-starter-kit` @ `main` (`af559249abd3`)
Agent: Codex CLI `0.138.0-alpha.7`
Adapter: `examples/agents/codex_exec_agent.py`
Runner: this repository (`harness-agent-benchmark-runner`)

## Headline

| Target | Agent | Mode | Repetitions | Total runs | Successes | Success rate | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `harness-starter-kit` | Codex CLI | Live adapter | 5 | 40 | 34 | 85% | 0 | 0 | 4 |

This run measured all eight deterministic target-repository benchmark tasks
five times each. Each run used a fresh isolated clone. No run edited a wrong or
forbidden file. Six runs failed: four due to agent timeout and two due to
verification oracle misses after the agent exited successfully.

## Conditions

- Task source: `https://github.com/harnessworks/harness-starter-kit`
- Target ref: `main` at `af559249abd3`
- Agent command: `python3 examples/agents/codex_exec_agent.py`
- Codex command defaults: no `CODEX_MODEL`, `CODEX_PROFILE`, or
  `CODEX_EXEC_ARGS` override was set
- Runner cap: `--max-agent-timeout 900`
- Budget hint: `--max-cost-usd 2.5`
- Task attempts: `max_attempts=1`
- Execution shape: five rounds; eight tasks were run in parallel per round
- Combined local artifact: `results/codex-5runs-20260611T051600Z/combined.jsonl`

## Per-task Result

| Task | Rate | Runs (O=pass X=fail) | Avg agent duration | Min | Max |
| --- | ---: | --- | ---: | ---: | ---: |
| command-workflow-refresh-benchmark-guidance | 4/5 | OXOOO | 177s | 108s | 360s |
| decision-memory-benchmark-ownership-adr | 4/5 | OOOOX | 112s | 51s | 240s |
| docs-only-evaluation-benchmark-ownership | 3/5 | OOXXO | 86s | 25s | 240s |
| failure-memory-benchmark-noop-oracle-gap | 4/5 | OOOXO | 75s | 55s | 90s |
| forbidden-file-structure-ignore-runner-output | 5/5 | OOOOO | 80s | 41s | 117s |
| installer-non-destructive-list-profiles | 5/5 | OOOOO | 121s | 108s | 161s |
| profile-boundary-go-race-check | 4/5 | OOXOO | 65s | 31s | 180s |
| small-bugfix-docs-drift-uv-command | 5/5 | OOOOO | 158s | 109s | 227s |

## Failure Analysis

### Timeouts

Four runs hit the task-level agent timeout:

| Task | Run id | Timeout | Changed files | Verification |
| --- | --- | ---: | --- | --- |
| command-workflow-refresh-benchmark-guidance | `20260611T051924Z-command-workflow-refresh-benchmark-guidance-7c00fdd0` | 360s | none | failed |
| docs-only-evaluation-benchmark-ownership | `20260611T052528Z-docs-only-evaluation-benchmark-ownership-f191abac` | 240s | none | failed |
| profile-boundary-go-race-check | `20260611T052529Z-profile-boundary-go-race-check-1767f3a0` | 180s | `templates/profiles/go/README.md` | passed |
| decision-memory-benchmark-ownership-adr | `20260611T053219Z-decision-memory-benchmark-ownership-adr-c28a87ee` | 240s | none | failed |

The profile-boundary timeout is notable because the agent had already made an
allowed change and both verification commands passed. The run still scored as a
failure because the runner requires the agent process itself to exit with code
0 before timeout.

### Verification failures after clean agent exit

Two runs exited normally but failed deterministic oracles:

- `docs-only-evaluation-benchmark-ownership`: edited `docs/evaluation.md`, but
  missed the required ownership concept `project-specific oracle ownership`.
- `failure-memory-benchmark-noop-oracle-gap`: edited
  `docs/failures/0012-benchmark-noop-oracle-gap.md`, but missed the required
  reference to `tests/test_benchmark_tasks.py`.

Both failures stayed inside the expected file boundaries.

## Summary

This evidence run shows strong file-boundary discipline: 0 wrong-file edits and
0 forbidden-file edits across 40 live Codex runs. The dominant instability is
completion within task timeout, especially when the task timeout is 180-360
seconds and eight Codex processes run concurrently. The two non-timeout failures
are task-oracle misses rather than boundary violations.

