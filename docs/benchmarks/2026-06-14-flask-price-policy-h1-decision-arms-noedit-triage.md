# Flask Price-Policy H1 Decision-Arms No-Edit Triage - 2026-06-14

This was a focused guarded no-edit triage after the guarded four-arm
24-record H1 stability expansion stopped on a `full-harness` no-edit watchdog.
It reran only the decision-bearing arms, `decision-only` and `full-harness`,
with a shorter no-edit watchdog to check whether the post-planning pre-edit
stall reproduced immediately.

This run completed cleanly. It does not promote H1 to 100-run readiness,
because it omitted the control arms and used 8 records rather than a
promotion-sized matrix. It does show that the no-edit stall is intermittent,
not a deterministic failure of every guarded decision-bearing attempt.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Task: `hidden-effect-catalog-price-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `decision-only`, `full-harness`
- Repeats: 4
- Planned records: 8
- Completed records: 8
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
- Runner ref: `5927e9643dddd7312d79362c40f1d2100d5a572f`
- Runner worktree note: uncommitted reporting-tool/docs changes were present;
  benchmark runner execution code was unchanged from the runner ref.
- Started: `2026-06-14T04:17:45Z`
- Finished: `2026-06-14T04:34:12Z`

Target refs:

| Arm | Source | Ref |
| --- | --- | --- |
| `decision-only` | `../flask-decision-only` | `95a843171d2183865c8698207b3b7d4075ba567b` |
| `full-harness` | `../flask-memory-harness` | `51700b72737a32fd9d96625a7547e28562865c57` |

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-price-policy \
  --arms decision-only,full-harness \
  --repeats 4 \
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
| `decision-only` | 4 | 4 | 4 | 4 | 4 | 4 | 4/4 | 0 | 0 | 0 | 0 | 50.8-59.6s | 33.1-39.1s |
| `full-harness` | 4 | 4 | 4 | 4 | 4 | 4 | 4/4 | 0 | 0 | 0 | 0 | 56.3-65.7s | 27.0-39.1s |

Overall:

- Completed records: 8/8
- Strict successes: 8/8
- Record consistency: 8/8
- Stalls/timeouts: 0
- Preflight failures: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- No-edit watchdog records: 0

## Watchdog Diagnostics

`scripts/summarize_hidden_ab.py` reported:

| Target | Watchdog records | No-edit watchdogs | No observed repo changes | p50 seconds to repo change | Max seconds without repo change | Max seconds since output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 4 | 0 | 0 | 36s | - | 0s |
| `full-harness` | 4 | 0 | 0 | 27s | - | 0s |

`scripts/triage_no_edit_stalls.py` reported:

```text
## No-Edit Stall Triage

No-edit watchdog records: 0
```

Per-record first repository change observations:

| Arm | Run ID | Duration | First repo change |
| --- | --- | ---: | ---: |
| `decision-only` | `20260614T041745Z-hidden-effect-catalog-price-policy-dae9de69` | 59.6s | 33.1s |
| `full-harness` | `20260614T041958Z-hidden-effect-catalog-price-policy-f6ee5e48` | 60.8s | 39.1s |
| `full-harness` | `20260614T042225Z-hidden-effect-catalog-price-policy-fa19dc83` | 65.7s | 32.1s |
| `decision-only` | `20260614T042458Z-hidden-effect-catalog-price-policy-0dcc70b4` | 59.3s | 37.1s |
| `decision-only` | `20260614T042609Z-hidden-effect-catalog-price-policy-45c22921` | 57.9s | 39.1s |
| `full-harness` | `20260614T042824Z-hidden-effect-catalog-price-policy-6876e299` | 56.3s | 27.1s |
| `full-harness` | `20260614T043046Z-hidden-effect-catalog-price-policy-d87a524a` | 58.2s | 27.0s |
| `decision-only` | `20260614T043312Z-hidden-effect-catalog-price-policy-2fb94ee4` | 50.8s | 36.1s |

## Reading

What this adds:

- Guarded `decision-only` and `full-harness` can both complete the price-policy
  task repeatedly with strict and record-consistent success.
- The previous no-edit watchdog is not deterministically triggered by simply
  combining the prompt guard with decision-bearing memory.
- Successful records touched the repository quickly: first observed changes
  appeared within 27.0-39.1s.

What this does not prove:

- It does not clear the four-arm H1 stability gate, because `workflow-only` and
  `failure-only` controls were omitted.
- It does not erase the prior guarded 24-record abort; the no-edit stall remains
  an intermittent promotion blocker.
- It does not justify a 100-record H1 promotion yet.

## Decision

Do not run a 100-record H1 promotion from this result alone.

The next useful promotion-readiness step is a guarded four-arm 24-record rerun
with no-edit triage enabled after any abnormal stop. If that completes 24/24
with clean boundaries and no stalls/timeouts, then a larger H1 matrix becomes
worth considering.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T041745Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T041745Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-price-policy-h1-decision-arms-noedit-triage.md`
