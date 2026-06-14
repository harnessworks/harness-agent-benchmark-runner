# Flask Price-Policy H1 Decision Guard Diagnostic - 2026-06-14

This was a focused diagnostic after the H1 24-record stability expansion
stopped on a `decision-only` no-edit watchdog. It reran only the
`decision-only` arm with the generic Codex prompt guard enabled.

The purpose was not to add comparable H1 performance evidence. The purpose was
to test whether a generic benchmark-operation guard helps the agent move from
decision-record discovery into repository edits.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Task: `hidden-effect-catalog-price-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `decision-only`
- Repeats: 2
- Planned records: 2
- Completed records: 2
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 360`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Codex model/config: `gpt-5.5`,
  `model_reasoning_effort=medium`, `service_tier=priority`
- Runner ref at run start:
  `da027889c459ffea8f3e49780ca7c4aed6468b2e`
- Started: `2026-06-14T03:23:19Z`
- Finished: `2026-06-14T03:28:06Z`

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-price-policy \
  --arms decision-only \
  --repeats 2 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 360 \
  --stop-on-abnormal \
  --execute
```

## Headline

| Arm | Completed | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | p50 duration | Max duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 2 | 2 | 2 | 2 | 2 | 2 | 2/2 | 0 | 0 | 0 | 0 | 55.5s | 74.1s |

Overall:

- Completed records: 2/2
- Strict successes: 2/2
- Record consistency: 2/2
- Stalls/timeouts: 0
- Preflight failures: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0

## Watchdog Diagnostics

Both records included `agent.watchdog` diagnostics.

| Run | Duration | Seconds until repo change | No-edit watchdog | Observed repo changes |
| --- | ---: | ---: | --- | --- |
| `20260614T032319Z-hidden-effect-catalog-price-policy-6295c1b4` | 55.5s | 24.0s | no | yes |
| `20260614T032451Z-hidden-effect-catalog-price-policy-443a7cd5` | 74.1s | 43.1s | no | yes |

This contrasts with the immediately prior stability expansion, where the first
`decision-only` record read the decision record but made no visible repository
changes for 360.035 seconds.

## Reading

`CODEX_PROMPT_GUARD=1` is a promising operational mitigation for the
`decision-only` no-edit stall pattern, but this run is only a two-record
diagnostic and should not be merged into the main H1 score.

The useful interpretation:

- The generic prompt guard did not prevent the agent from using the adopted
  decision record correctly.
- It did coincide with quick visible repository edits in both records.
- It does not prove the stall pattern is solved; it suggests the next
  stability check should compare guarded versus unguarded H1 runs explicitly.

## Decision

Do not run a 100-record promotion yet.

Next useful work:

- Run a guarded clean gate for the same four non-bare H1 arms before any larger
  promotion attempt.
- Keep guarded and unguarded evidence separate in reports.
- If guarded H1 gates remain clean, consider making `CODEX_PROMPT_GUARD=1` the
  documented operational default for promotion-style runs.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T032319Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T032319Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-price-policy-h1-decision-guard-diagnostic.md`
