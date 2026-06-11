# AGENTS.md

## Purpose

This repository is the benchmark runner infrastructure for continuously
measuring coding-agent behavior against deterministic repository harness tasks.

Keep target-specific benchmark tasks and scoring rules in the target repository
when practical. Keep scheduler, adapter, isolation, result collection, and
summary logic here.

## Core Rules

- Do not run agent benchmarks against a dirty source repository unless the task
  explicitly documents why that is required.
- Run each benchmark in an isolated clone or worktree under `runs/`.
- Do not commit `runs/`, `results/`, API keys, local logs, virtual
  environments, or agent credentials.
- Keep scoring deterministic where practical. LLM or subagent review may add
  annotations, but it should not be the only success oracle.
- Keep agent adapters thin. The runner should pass environment variables and
  collect evidence; product-specific behavior belongs in task specs or target
  repository oracles.
- Prefer standard-library Python unless a dependency removes clear operational
  complexity.
- When changing scoring semantics, update README task spec docs and tests in
  the same change.

## Validation

Run:

```bash
python3 -m unittest discover -s tests
```

For a smoke run against a sibling `harness-starter-kit` checkout:

```bash
python3 -m harness_agent_benchmark_runner run \
  --task benchmarks/tasks/harness-starter-kit-smoke.json \
  --agent-command "python3 $PWD/examples/agents/noop_agent.py"
```

## Design Constraints

- The measured repository is the source of truth for task boundaries and
  verification commands.
- A passing test suite alone is not a full success signal when file-boundary or
  forbidden-file rules are violated.
- Result records should be append-only and easy to archive as CI artifacts.
- Long-running orchestration should live in external schedulers first; add an
  in-process daemon only after repeated manual scheduling pain is visible.
