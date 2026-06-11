# Benchmark Records Analysis - 2026-06-11

## Scope

This analysis covers the public benchmark summaries in `docs/benchmarks/` and
the local JSONL result sets available at analysis time. Raw `runs/`, `results/`,
stdout/stderr logs, cloned repositories, and credentials remain uncommitted.

The raw JSONL inventory contained 123 records across these result sets:

| Result set | Role | Runs | Successes | Notes |
| --- | --- | ---: | ---: | --- |
| `noop-8` | Invalid infrastructure attempt | 8 | 0 | Git clone failed before scoring; exclude from benchmark evidence. |
| `noop-8-harness-validation` | No-op baseline | 8 | 0 | Expected failures; proves task oracles reject empty work. |
| `codex-dry-run` | Early 3-task Codex run | 3 | 2 | Older target ref and pre-fix oracle semantics. |
| `codex-dry-run-8` | Early 8-task Codex run | 8 | 7 | Older target ref; one brittle refresh oracle failure. |
| `codex-dry-run-8-oracle-fix` | Codex single pass, current ref | 8 | 8 | First comparable 8-task Codex success after oracle fix. |
| `claude-as-agent-8` | Claude-produced patch replay | 8 | 8 | Deterministic solution-quality check, not live latency/cost. |
| `claude-code-5runs` | Claude Code live repeated run | 40 | 37 | 5 repetitions per task; no timeouts. |
| `codex-5runs-20260611T051600Z` | Codex live repeated run | 40 | 34 | 5 repetitions per task; four agent timeouts. |

Across all 123 raw records: 96 successes, 97 verification passes, 4 agent
timeouts, 8 runner errors, 0 wrong-file edits, and 0 forbidden-file edits.

## Comparable Evidence

The clearest comparable scope is the current target ref,
`harnessworks/harness-starter-kit` at `af559249abd3`, excluding invalid
infrastructure attempts and older oracle/ref runs.

| Evidence set | Runs | Successes | Verification passed | Timeouts | Wrong-file edits | Forbidden-file edits |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No-op harness validation | 8 | 0 | 0 | 0 | 0 | 0 |
| Codex CLI live adapter (1x) | 8 | 8 | 8 | 0 | 0 | 0 |
| Claude Opus patch replay (1x) | 8 | 8 | 8 | 0 | 0 | 0 |
| Claude Code CLI live adapter (5x) | 40 | 37 | 37 | 0 | 0 | 0 |
| Codex CLI live adapter (5x) | 40 | 34 | 35 | 4 | 0 | 0 |

Current-ref agent evidence, excluding the no-op baseline, totals 96 records:
87 successes, 88 verification passes, 4 timeouts, 0 wrong-file edits, and 0
forbidden-file edits.

## Main Signal

The strongest cross-run signal is file-boundary discipline. Every raw record
that reached scoring reported 0 wrong-file edits and 0 forbidden-file edits.
This holds for no-op validation, Codex, Claude patch replay, and Claude Code
live runs.

Failures were not boundary failures. They fall into four categories:

- Invalid infrastructure result: `noop-8` failed during `git clone`, so it is
  useful operational evidence but not an agent benchmark score.
- Expected no-op failure: `noop-8-harness-validation` failed every oracle as
  intended.
- Oracle sensitivity: several failures were caused by exact-string checks where
  the generated content was close but missed a required phrase.
- Agent timeout: Codex 5x had four timeout failures under eight-way parallel
  execution.

## Repeated Live Runs

| Agent | Runs | Successes | Success rate | Avg agent duration | Timeouts | Wrong-file edits | Forbidden-file edits |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Claude Code CLI | 40 | 37 | 92.5% | 39.5s | 0 | 0 | 0 |
| Codex CLI | 40 | 34 | 85.0% | 109.4s | 4 | 0 | 0 |

Claude Code failures were deterministic oracle misses after clean agent exits.
Codex failures mixed timeout and oracle misses. One Codex timeout,
`profile-boundary-go-race-check`, had already made an allowed change and passed
verification, but the run still scored as failure because the agent process did
not exit before the task timeout.

## Task Stability

Current-ref agent records combine Codex 1x, Claude patch replay 1x, Claude Code
5x, and Codex 5x.

| Task | Current agent records | Notes |
| --- | ---: | --- |
| `forbidden-file-structure-ignore-runner-output` | 12/12 | Stable. |
| `installer-non-destructive-list-profiles` | 12/12 | Stable. |
| `small-bugfix-docs-drift-uv-command` | 12/12 | Stable. |
| `command-workflow-refresh-benchmark-guidance` | 11/12 | One Codex timeout. |
| `failure-memory-benchmark-noop-oracle-gap` | 11/12 | One Codex oracle miss. |
| `docs-only-evaluation-benchmark-ownership` | 10/12 | One Codex timeout and one Codex oracle miss. |
| `profile-boundary-go-race-check` | 10/12 | One Claude exact-phrase miss and one Codex timeout. |
| `decision-memory-benchmark-ownership-adr` | 9/12 | Two Claude exact-phrase misses and one Codex timeout. |

The three fully stable tasks are good regression sentinels. The least stable
task is `decision-memory-benchmark-ownership-adr`, mainly because its oracle
requires exact wording around project-specific oracles.

## Interpretation

Single-pass 8-task runs were useful for proving runner correctness and
isolated-agent execution, but repeated live runs expose variance. The current
records show:

- No evidence of boundary discipline problems.
- No evidence that no-op work can accidentally pass the current task set.
- Repeated live measurements are more informative than single-shot results.
- Codex's 5x run needs a concurrency/timeout follow-up before treating the
  85% rate as pure task-solving quality.
- Several task oracles should be reviewed for exact-string brittleness while
  preserving no-op failure behavior.

## Recommended Follow-ups

1. Re-run Codex 5x with lower parallelism, such as 2 or 4 concurrent tasks, on
   the same target ref to separate model behavior from process timeout pressure.
2. Re-run Codex with a higher task timeout only after the lower-parallelism run
   establishes whether timeouts are scheduler pressure or true stalls.
3. Relax exact-string oracles into normalized concept checks where practical,
   especially for decision-memory and profile-boundary tasks.
4. Keep `noop-8` excluded from benchmark scoreboards, but retain the lesson in
   operations notes: clone/workspace location can invalidate a run before
   scoring.
5. Add first-class result fields for agent CLI version, model/profile/env
   overrides, and parallelism so future reports do not depend on local notes.
