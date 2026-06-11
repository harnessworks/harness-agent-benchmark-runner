# Real Agent Run — Claude, 8 Tasks

Date: 2026-06-11
Target: `harnessworks/harness-starter-kit` @ `main` (`af55924`)
Agent: Claude (Opus, via Cowork) acting as the benchmarked coding agent
Runner: this repository (`harness-agent-benchmark-runner`)

## Headline

| Target | Agent | Runs | Successes | First-pass verify | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `harness-starter-kit` | Claude | 8 | 8 | 8 | 0 | 0 | 0 |

All eight deterministic tasks passed on the first attempt with no file-boundary
violations. Each run was an isolated clone, scored by the repository's own
verification oracles plus `expected_files`/`forbidden_files` boundary checks.

## Per-task result

| Task | Success | Changed files |
| --- | --- | --- |
| command-workflow-refresh-benchmark-guidance | ✅ | `commands/harness-refresh.md`, `tests/test_repository_hygiene.py` |
| decision-memory-benchmark-ownership-adr | ✅ | `docs/decisions/0008-benchmark-task-ownership.md` |
| docs-only-evaluation-benchmark-ownership | ✅ | `docs/evaluation.md` |
| failure-memory-benchmark-noop-oracle-gap | ✅ | `docs/failures/0012-benchmark-noop-oracle-gap.md` |
| forbidden-file-structure-ignore-runner-output | ✅ | `.harness/structure-rules.json` |
| installer-non-destructive-list-profiles | ✅ | `scripts/apply_harness.py`, `tests/test_apply_harness.py` |
| profile-boundary-go-race-check | ✅ | `templates/profiles/go/README.md` |
| small-bugfix-docs-drift-uv-command | ✅ | `scripts/check_docs_drift.py`, `tests/test_check_docs_drift.py` |

Every task changed exactly the files its spec allowed, and each task's oracle
ran the repository's real checks (unit tests, docs-drift, encoding hygiene,
failure-memory, structure, profile-consistency, and task-specific assertions).

## Method and honest caveats

The sandbox has no externally authenticated coding-agent CLI (`codex` not
installed; the `claude` CLI reports "Not logged in" with no API key), so the
agent could not be wired in as a live subprocess. Instead:

1. Claude solved each task directly in an isolated checkout and verified the
   edits against that task's real oracle.
2. Each solution was captured as a per-task git patch.
3. The runner executed each task normally against a fresh clone, using a thin
   patch-replay adapter (`results/claude-as-agent-8/claude_patch_agent.py`) as
   the `--agent-command`. The runner then ran `git diff --check`, the real
   verification oracles, and boundary scoring.

What this proves: the edits Claude produced satisfy every deterministic oracle
and stay within file boundaries — a real, reproducible measurement of solution
quality for these eight tasks.

What it does not capture: the recorded `agent.duration_seconds` reflects only
patch application (≈0.3s total), not Claude's solve/reasoning time, because the
reasoning happened before the replay. Latency and cost are therefore **not**
measured here. For live latency/cost, run the same tasks with an authenticated
agent CLI as `--agent-command` (see the runner README's adapter contract).

## Comparison

| Run | Agent | Successes |
| --- | --- | ---: |
| no-op harness validation | none (no edits) | 0 / 8 |
| codex-dry-run-8 | Codex CLI | 7 / 8 |
| codex-dry-run-8-oracle-fix | Codex CLI | 8 / 8 |
| claude-as-agent-8 (this run) | Claude | 8 / 8 |

The no-op run (0/8, oracles correctly reject empty work) and this run (8/8,
oracles accept correct work) bracket the harness: the eight oracles reliably
separate "no work" from "correct, in-boundary work."

## Reproducing

Artifacts: `results/claude-as-agent-8/` (JSONL, per-task patches, adapter).

```bash
export BENCHMARK_PATCH_DIR=/path/to/results/claude-as-agent-8/patches
for t in <harness-starter-kit>/benchmarks/tasks/*.json; do
  python3 -m harness_agent_benchmark_runner run \
    --task "$t" \
    --agent-command "python3 results/claude-as-agent-8/claude_patch_agent.py" \
    --workspace /tmp/runs --results /tmp/results --max-agent-timeout 120
done
python3 -m harness_agent_benchmark_runner summarize --results /tmp/results
```

Note: keep `--workspace`/`--results` on a local filesystem (not the mounted
folder); git clone's hardlink/lock operations are blocked on the mount.
