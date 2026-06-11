# Live Agent Run — Claude Code CLI, 8 Tasks × 5 Repetitions

Date: 2026-06-11
Target: `harnessworks/harness-starter-kit` @ `main` (`af559249abd3`)
Agent: Claude Code CLI (`claude -p`, `bypassPermissions` mode)
Runner: this repository (`harness-agent-benchmark-runner`)

## Headline

| Target | Agent | Mode | Repetitions | Total runs | Successes | Success rate | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `harness-starter-kit` | Claude Code CLI | Live adapter | 5 | 40 | 37 | 92.5% | 0 | 0 | 0 |

First multi-repetition live run for Claude Code CLI. Each repetition uses a
fresh isolated clone per task. All 40 runs completed within timeout; no
file-boundary violations across any run.

## Per-task result

| Task | Rate | Runs (O=pass X=fail) | Avg duration | Min | Max |
| --- | ---: | --- | ---: | ---: | ---: |
| command-workflow-refresh-benchmark-guidance | 5/5 | OOOOO | 62s | 51s | 73s |
| decision-memory-benchmark-ownership-adr | 3/5 | XOOXO | 54s | 46s | 65s |
| docs-only-evaluation-benchmark-ownership | 5/5 | OOOOO | 22s | 21s | 24s |
| failure-memory-benchmark-noop-oracle-gap | 5/5 | OOOOO | 36s | 32s | 44s |
| forbidden-file-structure-ignore-runner-output | 5/5 | OOOOO | 13s | 11s | 18s |
| installer-non-destructive-list-profiles | 5/5 | OOOOO | 68s | 59s | 82s |
| profile-boundary-go-race-check | 4/5 | OOOXO | 20s | 16s | 25s |
| small-bugfix-docs-drift-uv-command | 5/5 | OOOOO | 41s | 35s | 48s |

Overall average duration per task: **39s**. All tasks completed well within
their configured timeouts (180–360s).

## Failure analysis

### decision-memory-benchmark-ownership-adr (3/5)

Oracle requires the exact string `project-specific oracles` in the produced ADR.
In the two failing runs Claude wrote semantically equivalent content
(`project-specific oracle logic`, `oracle logic`) without using that exact
phrasing. The file structure, intent, and all other required strings were
correct. This is a string-matching sensitivity issue in the oracle, not a
reasoning failure in the agent.

Failing runs: rep1, rep4. Passing runs: rep2, rep3, rep5.

### profile-boundary-go-race-check (4/5)

Oracle requires the exact phrase `race-sensitive concurrent code, default
harness gate` in the Go profile guidance. In the one failing run (rep4) Claude
wrote the correct guidance but split the concept across two sentences
(`race-sensitive concurrent code` and `default harness gate` appeared
separately), causing the substring match to fail. All other oracle checks
passed.

## Performance

Tasks span a wide complexity range. Simpler read-and-edit tasks (forbidden-file,
docs-only, profile-boundary) complete in under 25s. Tasks requiring multi-file
reasoning and new file creation (installer, command-workflow-refresh) take
60–80s. No run approached the task timeout ceiling, indicating the current
timeout budget is comfortably sized for Claude Code.

| Bucket | Tasks | Avg duration |
| --- | --- | ---: |
| Fast (< 25s) | forbidden-file, docs-only, profile-boundary | 18s |
| Medium (25–50s) | failure-memory, small-bugfix | 39s |
| Slow (> 50s) | command-workflow-refresh, decision-memory, installer | 61s |

## Comparison

| Run | Agent | Mode | Successes | Rate |
| --- | --- | --- | ---: | ---: |
| noop-8-harness-validation | No-op | Harness validation | 0 / 8 | 0% |
| codex-dry-run-8-oracle-fix | Codex CLI | Live adapter (1×) | 8 / 8 | 100% |
| claude-as-agent-8 | Claude Opus | Patch replay (1×) | 8 / 8 | 100% |
| **claude-code-5runs (this run)** | **Claude Code CLI** | **Live adapter (5×)** | **37 / 40** | **92.5%** |

The two previous 100% runs were single-shot measurements (patch replay or single
live pass); this is the first run measuring variance across repetitions. The
two failures trace to oracle string-matching strictness rather than agent
capability gaps, which is worth addressing in the task specs.

## Reproducing

Artifacts: `results/claude-code-5runs/` (JSONL, per-run JSON).

Requires an authenticated Claude Code CLI (`claude`) on the host.

```bash
RUNNER="python3 -m harness_agent_benchmark_runner"
TASKS="/path/to/harness-starter-kit/benchmarks/tasks"
AGENT="python3 $PWD/examples/agents/claude_code_agent.py"

for rep in 1 2 3 4 5; do
  for task in "$TASKS"/*.json; do
    $RUNNER run \
      --task "$task" \
      --agent-command "$AGENT" \
      --results results/claude-code-5runs \
      --max-agent-timeout 900 \
      --max-cost-usd 2.5 &
  done
  wait
done

$RUNNER summarize --results results/claude-code-5runs
```
