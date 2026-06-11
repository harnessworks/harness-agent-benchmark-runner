# Harness Agent Benchmark Runner

Continuous benchmark runner for measuring coding-agent performance against
repository-specific harness tasks.

This repository owns the runner infrastructure. The repositories being measured
own their task definitions, success oracles, and project-specific checks.

## Goal

Run agent tasks repeatedly in isolated clones, collect deterministic evidence,
and produce comparable metrics:

- task success rate
- first-pass verification rate
- wrong-file edit rate
- forbidden-file edit rate
- verification failure rate
- runtime per task
- changed-file boundary violations

The runner should not decide product quality by itself. It records deterministic
signals first, then leaves judgment-heavy fields to a reviewer or a separate
read-only evaluation agent.

## Repository Layout

```text
benchmarks/tasks/      Example task specs.
examples/agents/       Tiny local agent adapters for smoke tests.
src/                   Runner package.
tests/                 Unit tests for task loading, scoring, and summaries.
results/               Local JSONL result output, ignored by git.
runs/                  Per-run cloned workspaces and logs, ignored by git.
```

## Quick Start

Run the local test suite:

```bash
python3 -m unittest discover -s tests
```

Run one benchmark task against a sibling `harness-starter-kit` checkout:

```bash
python3 -m harness_agent_benchmark_runner run \
  --task benchmarks/tasks/harness-starter-kit-smoke.json \
  --agent-command "python3 $PWD/examples/agents/noop_agent.py"
```

Summarize local results:

```bash
python3 -m harness_agent_benchmark_runner summarize --results results
```

## Task Spec

Task specs are JSON in the initial version so the runner works with the Python
standard library only.

```json
{
  "schema_version": 1,
  "id": "example-task",
  "description": "Short human-readable scenario.",
  "repo": {
    "source": "../target-repo",
    "ref": "main"
  },
  "prompt": "Do the task the agent should attempt.",
  "timeout_seconds": 900,
  "expected_files": ["docs/**", "scripts/**"],
  "forbidden_files": [".env", "**/.env", "node_modules/**"],
  "verification": {
    "commands": [
      {
        "name": "unit tests",
        "command": ["python3", "-m", "unittest", "discover", "-s", "tests"],
        "timeout_seconds": 300
      }
    ]
  }
}
```

`repo.source` can be a local path or a Git URL. Relative local paths are resolved
from the current working directory first, then from the task file directory.

## Agent Adapter Contract

The runner executes `--agent-command` inside the isolated clone. It sets these
environment variables:

- `BENCHMARK_REPO`: absolute path to the isolated repository clone
- `BENCHMARK_PROMPT_FILE`: path to the task prompt text file
- `BENCHMARK_PROMPT`: prompt text
- `BENCHMARK_TASK_ID`: task id
- `BENCHMARK_RUN_ID`: unique run id

Any agent command that can read those values and edit the isolated clone can be
used. For example, a wrapper script can call Codex CLI, Claude Code, Aider, or a
custom OpenAI API agent.

Because the command runs from the isolated target repository clone, reference
local adapter scripts with an absolute path such as
`python3 $PWD/examples/agents/noop_agent.py` when invoking the runner from this
repository root.

## Scoring

A run is marked successful only when:

- the agent command exits with code `0`
- `git diff --check` exits with code `0`
- all verification commands exit with code `0`
- no changed file falls outside `expected_files`, when expected files are set
- no changed file matches `forbidden_files`

The raw result is always preserved under `runs/<run-id>/result.json` and appended
to `results/YYYY-MM-DD.jsonl`.

## 24-Hour Operation

The intended production setup is a self-hosted runner, launchd job, systemd
timer, or small scheduler that repeatedly calls:

```bash
python3 -m harness_agent_benchmark_runner run \
  --task <task-spec> \
  --agent-command <agent-wrapper>
```

Use an external scheduler for now. Keeping scheduling outside the runner makes
timeouts, API keys, cost limits, and machine isolation easier to audit.
