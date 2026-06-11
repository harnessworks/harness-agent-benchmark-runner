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

## Benchmark Reporting

After any real agent dry run, pilot, or evidence run that should be visible to
future maintainers:

- Do not commit raw `runs/`, `results/`, local logs, cloned repositories, or
  credentials.
- Summarize public-safe results in `docs/benchmarks/`.
- Keep `docs/benchmarks/latest.md` pointed at the most recent representative
  report.
- Keep README's `Benchmark Status` section short: current infrastructure state,
  latest run headline, and a link to the detailed report.
- Include enough detail for reproducibility: target repository, target ref,
  agent adapter, run count, success count, wrong-file edits, forbidden-file
  edits, timeouts, and notable failure causes.
- Treat benchmark results as evidence only for the measured scope. A
  target-repository dry run proves runner/task/adapter behavior for that target;
  it does not prove cross-repository harness effectiveness.
- When a task fails because an oracle is brittle rather than because the agent
  violated task intent or file boundaries, record that distinction.

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
