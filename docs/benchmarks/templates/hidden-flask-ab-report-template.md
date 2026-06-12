# Hidden-Oracle Flask Harness Arm Benchmark - Report Template

Date: YYYY-MM-DD
Runner: `harness-agent-benchmark-runner` @ `<runner-ref>`
Agent: Codex CLI `<version>`
Adapter: `examples/agents/codex_exec_agent.py`
Suite: `benchmarks/suites/<suite>.json`

## Headline

| Target arm | Target repo/ref | Prompt level | Runs | Functional success | Schema contract success | Workflow success | Strict success | Preflight failures | Wrong-file edits | Forbidden-file edits | Hidden access | Stalls | Timeouts | p50 duration | p95 duration |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | `<repo>@<ref>` | `<partial-realistic|full-contract>` |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `workflow-only` | `<repo>@<ref>` | `<partial-realistic|full-contract>` |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `memory-harness` | `<repo>@<ref>` | `<partial-realistic|full-contract>` |  |  |  |  |  |  |  |  |  |  |  |  |  |

One-sentence headline:
Under `<prompt-level>`, `<arm>` reached `<x>/<n>` functional successes and
`<y>/<n>` strict successes versus `<baseline>` at `<a>/<n>` and `<b>/<n>`.

## Scope

- Benchmark type: hidden-oracle harness arm comparison.
- Product comparison arms:
  - `bare`: no harness.
  - `workflow-only`: `AGENTS`, local gate, docs placement, and boundary rules only.
  - `memory-harness`: workflow harness plus generalized project conventions and failure memory.
- Prompt levels:
  - `partial-realistic`: product main experiment. The prompt gives intent and general constraints, not the full scoring contract.
  - `full-contract`: control experiment. The prompt may state exact route, request shape, response shape, and core rules; small arm gaps are expected.
- Not measured: cross-framework harness effectiveness, retry recovery, or generic model quality unless separately run.

## Leakage Audit

Before live execution, every task should include `leakage_audit` and the runner
should record `preflight.passed=true`.

| Check | Status | Notes |
| --- | --- | --- |
| Target source checkout clean before isolated clone |  |  |
| Isolated clone clean before agent execution |  |  |
| No hidden oracle files in target repo |  |  |
| No held-out endpoint names or exact version constants in target docs/memory |  |  |
| No raw `runs/` or `results/` artifacts committed |  |  |

The target repository may contain generalized conventions, glossary terms, and
failure memory. It must not contain task-specific answer strings such as exact
held-out route names, response key sets, hidden oracle payloads, or oracle file
names.

## Scoring

| Metric | Meaning |
| --- | --- |
| `functional_success` | Hidden oracle behavior passed for commands tagged `functional`. |
| `schema_contract_success` | Response envelope/key/meta contract passed for commands tagged `schema`. |
| `workflow_success` | Agent exit, diff check, file boundaries, and commands tagged `workflow` passed. |
| `boundary_success` | No wrong-file or forbidden-file edits. |
| `execution_success` | Agent exited successfully without timeout. |
| `strict_success` | Final score: preflight, execution, diff check, all verification commands, and boundaries passed. |
| `agent_stalled` | A stall, idle-output, or no-edit watchdog stopped the agent before clean completion. |
| `hidden_access` | Agent log contained a direct attempt to inspect hidden benchmark/oracle paths. |

Legacy untagged verification commands are treated as combined verification for
backward compatibility. New task specs should tag verification commands with
`dimensions`.

## Run Conditions

- Run command: `python3 scripts/run_hidden_flask_ab.py --suite benchmarks/suites/<suite>.json ...`
- Repetitions: `<repeats>` per task/arm
- Task groups: `<count>`
- Total records: `<count * repeats * arms>`
- Arm order: `rotate` unless an ordering effect is intentionally measured
- Concurrency: `1`, unless explicitly documented otherwise
- Task attempts: `max_attempts=1`
- Effective agent timeout: `<seconds>`
- Agent stall watchdog: `<seconds|none>`
- Agent idle watchdog: `<seconds|none>`
- Agent no-edit watchdog: `<seconds|none>`
- Budget hint: `<amount>`
- Codex model: `gpt-5.5`
- Codex config override:
  `CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`
- Codex adapter hygiene: `CODEX_IGNORE_USER_CONFIG=1`,
  `CODEX_IGNORE_RULES=1`, `CODEX_DISABLE_PLUGINS=1`, and
  `CODEX_PROMPT_GUARD=0`, unless explicitly documented otherwise.

## Task Design

| Task | Split | Prompt level | Held-out convention being generalized | Hidden oracle dimensions |
| --- | --- | --- | --- | --- |
| `<task-id>` | `<train|heldout|control>` | `<partial-realistic|full-contract>` |  | `functional`, `schema` |

Design notes:

- Task prompts are identical across arms.
- Held-out tasks should apply known conventions to a new endpoint or workflow,
  not repeat an API contract already written in target docs.
- Full-contract controls are allowed, but they are not the product-value claim.
- If a task fails because an oracle is brittle rather than because the agent
  violated task intent or file boundaries, record that distinction.

## Per-Task Results

| Target arm | Task | Runs | Functional | Schema contract | Workflow | Strict | Preflight failures | Wrong-file edits | Forbidden-file edits | Stalls | Timeouts | p50 duration | p95 duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | `<task-id>` |  |  |  |  |  |  |  |  |  |  |  |  |
| `workflow-only` | `<task-id>` |  |  |  |  |  |  |  |  |  |  |  |  |
| `memory-harness` | `<task-id>` |  |  |  |  |  |  |  |  |  |  |  |  |

## Failure Taxonomy

| Cause | `bare` | `workflow-only` | `memory-harness` | Notes |
| --- | ---: | ---: | ---: | --- |
| Functional behavior mismatch |  |  |  |  |
| Schema or response-envelope mismatch |  |  |  |  |
| Generic API style gate miss |  |  |  |  |
| Missing required docs |  |  |  |  |
| Wrong-file edit |  |  |  |  |
| Forbidden-file edit |  |  |  |  |
| Leakage preflight failure |  |  |  |  |
| Stall watchdog |  |  |  |  |
| Idle watchdog |  |  |  |  |
| No-edit watchdog |  |  |  |  |
| Timeout |  |  |  |  |
| Brittle oracle |  |  |  | Mark separately from genuine task failure. |

## Interpretation

State only claims supported by this measured scope. A `full-contract` arm gap
near zero is normal: the prompt has already supplied much of the answer. The
product-value claim requires `partial-realistic` held-out tasks where
`memory-harness` generalizes from conventions without task-specific leakage.

## Raw Artifacts

Raw local records are intentionally not committed.

- Results JSONL: `results/<run-id>/<date>.jsonl`
- Run directories: `runs/<run-id>/`
- Public-safe report: `docs/benchmarks/<date>-hidden-flask-<shape>.md`
