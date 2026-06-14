# Flask H1 Prompt-Guard Mitigation Diagnostic - 2026-06-14

This was the first live diagnostic after adding a generic prompt-guard
mitigation to the Codex adapter. The guardrail tells the agent to start a small
scoped repository edit after it identifies the relevant implementation
direction, before extended additional analysis.

The mitigation is answer-free: it does not name any H1 route, label, threshold,
or oracle expectation. It only changes the benchmark execution behavior under
`CODEX_PROMPT_GUARD=1`.

The diagnostic did not clear the no-edit blocker. It completed 7/8 strict and
record-consistent records, but one `decision-only`
`hidden-effect-catalog-replenishment-policy` record hit the no-edit watchdog
after finding the accepted replenishment policy and announcing the intended
implementation direction. No files changed before the watchdog stopped it.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Tasks:
  - `hidden-effect-catalog-price-policy`
  - `hidden-effect-catalog-replenishment-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `decision-only`, `full-harness`
- Repeats: 2
- Planned records: 8
- Completed records: 8
- Concurrency: `--jobs 1`
- Stop-on-abnormal: disabled
- Promotion mode: disabled
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Prompt mitigation: adapter default guard includes "start a small scoped
  repository edit before extended additional analysis"
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 240`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Runner ref: `b60a34c5b9c457e60554bb12882e9050efc66b82`
- Started: `2026-06-14T07:56:48Z`
- Finished: `2026-06-14T08:10:59Z`

Target refs:

| Arm | Source | Ref |
| --- | --- | --- |
| `decision-only` | `../flask-decision-only` | `e9b0a3e919a7827497c7163912a1023c2346008f` |
| `full-harness` | `../flask-memory-harness` | `ba8b3963d071089429fa2c2c8ebc10049e80cca4` |

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-price-policy \
  --task-id hidden-effect-catalog-replenishment-policy \
  --arms decision-only,full-harness \
  --repeats 2 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --execute
```

## Headline

| Arm | Runs | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 4 | 3 | 3 | 3 | 3 | 4 | 3/4 | 1 | 1 | 0 | 0 | 59s | 240s |
| `full-harness` | 4 | 4 | 4 | 4 | 4 | 4 | 4/4 | 0 | 0 | 0 | 0 | 50s | 68s |

Per task:

| Arm | Task | Runs | Strict | Record consistency | Stalls | p50 duration | p95 duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | `hidden-effect-catalog-price-policy` | 2 | 2 | 2/2 | 0 | 51s | 70s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | 2 | 1 | 1/2 | 1 | 59s | 240s |
| `full-harness` | `hidden-effect-catalog-price-policy` | 2 | 2 | 2/2 | 0 | 47s | 50s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | 2 | 2 | 2/2 | 0 | 53s | 68s |

## Watchdog Diagnostics

`scripts/summarize_hidden_ab.py` reported:

| Target | Watchdog records | No-edit watchdogs | No observed repo changes | p50 seconds to repo change | Max seconds without repo change | Max seconds since output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 4 | 1 | 1 | 33s | 240s | 103s |
| `full-harness` | 4 | 0 | 0 | 28s | - | 0s |

`scripts/triage_no_edit_stalls.py` reported one no-edit watchdog:

| Run ID | Arm | Task | Duration | Seconds without repo change | Last phase |
| --- | --- | --- | ---: | ---: | --- |
| `20260614T075914Z-hidden-effect-catalog-replenishment-policy-e254f735` | `decision-only` | `hidden-effect-catalog-replenishment-policy` | 240.0s | 240.0s | `post-planning` |

The last agent message said it had found the accepted replenishment policy:
`reorder_now` below stock 5, `monitor` for 5 through 19, and `healthy` for 20
or more. It then said it would add a catalog helper and route. No repository
changes were observed for 240 seconds after the run started.

The stopped worktree had no file changes. The harness gate passed against the
unchanged repository, and the hidden functional, schema, and record-consistency
checks failed with 404 because `/catalog/replenishment-policy` was still absent.

Per-record timing:

| Arm | Task | Run ID | Strict | Stall | Duration | First repo change |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `decision-only` | `hidden-effect-catalog-price-policy` | `20260614T075648Z-hidden-effect-catalog-price-policy-5d4619c9` | 1 | 0 | 51.3s | 33.1s |
| `full-harness` | `hidden-effect-catalog-price-policy` | `20260614T075816Z-hidden-effect-catalog-price-policy-71c785fe` | 1 | 0 | 47.4s | 34.1s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | `20260614T075914Z-hidden-effect-catalog-replenishment-policy-e254f735` | 0 | 1 | 240.0s | - |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | `20260614T080359Z-hidden-effect-catalog-replenishment-policy-3cd35816` | 1 | 0 | 67.8s | 28.1s |
| `full-harness` | `hidden-effect-catalog-price-policy` | `20260614T080517Z-hidden-effect-catalog-price-policy-72f7eeab` | 1 | 0 | 50.4s | 25.1s |
| `decision-only` | `hidden-effect-catalog-price-policy` | `20260614T080632Z-hidden-effect-catalog-price-policy-147d2ca6` | 1 | 0 | 69.9s | 37.1s |
| `full-harness` | `hidden-effect-catalog-replenishment-policy` | `20260614T080816Z-hidden-effect-catalog-replenishment-policy-e4f84eb6` | 1 | 0 | 53.0s | 37.1s |
| `decision-only` | `hidden-effect-catalog-replenishment-policy` | `20260614T080918Z-hidden-effect-catalog-replenishment-policy-aacb4798` | 1 | 0 | 59.3s | 25.1s |

## Reading

What this diagnostic shows:

- The generic prompt-guard mitigation is not sufficient.
- The no-edit failure can occur after the agent has already found the relevant
  accepted decision policy and described a correct implementation direction.
- The failure remained isolated to `decision-only`
  `hidden-effect-catalog-replenishment-policy` in this 8-record batch.
- `full-harness` stayed 4/4 strict and record-consistent.

What it does not show:

- It does not prove the mitigation made behavior worse. A prior 8-record
  diagnostic was clean, but the no-edit pattern has already been intermittent.
- It does not justify another blind 96/100-record H1 promotion.
- It does not identify whether the root cause is prompt planning, Codex CLI
  behavior, target-specific guidance shape, or the no-edit watchdog threshold.

## Decision

Keep the generic guardrail because it is answer-free and aligned with the
benchmark operating goal, but do not treat it as a solved mitigation.

The next useful work is stronger and more specific operational mitigation:

- reduce the `decision-only` replenishment path's planning surface in target
  guidance without adding task-specific answers;
- or add an adapter-level progress constraint that is still answer-free but
  more explicit about editing before narrating an implementation plan;
- then rerun a small diagnostic before any larger H1 promotion attempt.

Another blind 96/100-record H1 promotion remains low-value.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T075647Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T075647Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-h1-prompt-guard-mitigation-diagnostic.md`
