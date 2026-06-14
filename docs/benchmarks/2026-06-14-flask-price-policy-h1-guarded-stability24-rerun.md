# Flask Price-Policy H1 Guarded Stability 24 Rerun - 2026-06-14

This was the guarded four-arm 24-record H1 stability rerun after the prior
guarded 24-record expansion stopped on a `full-harness` no-edit watchdog. It
kept the same task and four-arm matrix, kept `CODEX_PROMPT_GUARD=1`, and used a
shorter no-edit watchdog so pre-edit stalls would fail faster.

The rerun completed all 24 planned records with zero stalls, zero timeouts,
zero wrong-file edits, and zero forbidden-file edits. The direct decision-memory
arms separated cleanly from controls: `decision-only` and `full-harness` were
both 6/6 strict and record-consistent, while `workflow-only` and `failure-only`
were both 0/6 record-consistent.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Task: `hidden-effect-catalog-price-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `workflow-only`, `decision-only`, `failure-only`, `full-harness`
- Repeats: 6
- Planned records: 24
- Completed records: 24
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Prior clean readiness:
  `results/hidden-flask-ab-pilot-20260614T033056Z`
- Minimum prior clean rounds: 3 per selected task/arm pair
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 240`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Codex model/config: `gpt-5.5`,
  `model_reasoning_effort=medium`, `service_tier=priority`
- Runner ref: `25afa65900c0f07f0872f7138efdf3c9a0eb5bd1`
- Started: `2026-06-14T04:37:26Z`
- Finished: `2026-06-14T05:18:52Z`

Target refs:

| Arm | Source | Ref |
| --- | --- | --- |
| `workflow-only` | `../flask-workflow-only` | `1a79d8cf9e0799789b3da8029dbbb5a572b3133e` |
| `decision-only` | `../flask-decision-only` | `95a843171d2183865c8698207b3b7d4075ba567b` |
| `failure-only` | `../flask-failure-only` | `18330ea23880b1ca7a647ea58b0d694e2c658fc8` |
| `full-harness` | `../flask-memory-harness` | `51700b72737a32fd9d96625a7547e28562865c57` |

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-price-policy \
  --arms workflow-only,decision-only,failure-only,full-harness \
  --repeats 6 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --require-clean-results results/hidden-flask-ab-pilot-20260614T033056Z \
  --min-clean-rounds 3 \
  --stop-on-abnormal \
  --execute
```

## Headline

| Arm | Completed | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | Duration range | First repo change range |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `workflow-only` | 6 | 0 | 6 | 6 | 6 | 6 | 0/6 | 0 | 0 | 0 | 0 | 52.0-62.2s | 28.1-46.0s |
| `decision-only` | 6 | 6 | 6 | 6 | 6 | 6 | 6/6 | 0 | 0 | 0 | 0 | 48.7-52.4s | 24.0-33.1s |
| `failure-only` | 6 | 0 | 5 | 6 | 6 | 6 | 0/6 | 0 | 0 | 0 | 0 | 49.4-83.1s | 26.1-50.1s |
| `full-harness` | 6 | 6 | 6 | 6 | 6 | 6 | 6/6 | 0 | 0 | 0 | 0 | 46.8-56.5s | 20.0-37.1s |

Overall:

- Completed records: 24/24
- Strict successes: 12/24
- Record consistency: 12/24
- Decision-bearing record consistency: 12/12
- Control-arm record consistency: 0/12
- Stalls/timeouts: 0
- Preflight failures: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- No-edit watchdog records: 0

## Watchdog Diagnostics

`scripts/summarize_hidden_ab.py` reported:

| Target | Watchdog records | No-edit watchdogs | No observed repo changes | p50 seconds to repo change | Max seconds without repo change | Max seconds since output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 6 | 0 | 0 | 27s | - | 0s |
| `failure-only` | 6 | 0 | 0 | 35s | - | 0s |
| `full-harness` | 6 | 0 | 0 | 33s | - | 0s |
| `workflow-only` | 6 | 0 | 0 | 41s | - | 0s |

`scripts/triage_no_edit_stalls.py` reported:

```text
## No-Edit Stall Triage

No-edit watchdog records: 0
```

The run therefore cleared the immediate operational blocker observed in the
previous guarded 24-record attempt.

## Control Notes

One `failure-only` control record failed the functional oracle while still
passing schema and workflow checks. The hidden functional oracle reported:

```text
glossary must document catalog price policy route and price bands; missing: price band
```

That control implementation also used a 30.00 premium floor. This is not a
decision-memory false positive: the target had no accepted decision record, and
the record-consistency oracle correctly failed it.

## Reading

What held:

- `decision-only` completed 6/6 strict and record-consistent.
- `full-harness` completed 6/6 strict and record-consistent.
- Both non-decision controls stayed 0/6 record-consistent.
- No run touched wrong or forbidden files.
- No run hit the idle or no-edit watchdog.

What changed relative to the previous guarded stability attempt:

- The previous guarded 24-record run stopped after 4 records on a
  `full-harness` no-edit watchdog.
- This rerun completed the full 24-record matrix.
- Successful records showed first observed repository changes within
  20.0-50.1s across all arms.

This makes the H1 price-policy result promotion-relevant, but still narrow. It
directly supports the claim that an accepted decision record can carry behavior
not present in workflow-only or failure-only guidance for this task. It does
not prove broad decision-memory value across other decision families.

## Decision

The immediate 24-record H1 stability gate is now clean.

A 100-record H1 promotion is now more defensible than it was after the abort,
but the expected value is limited because the current H1 suite still measures
one decision family. Before spending on a larger matrix, either add a second
decision-memory task family or explicitly scope the promotion claim to the
catalog price-policy decision only.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T043726Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T043726Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-price-policy-h1-guarded-stability24-rerun.md`
