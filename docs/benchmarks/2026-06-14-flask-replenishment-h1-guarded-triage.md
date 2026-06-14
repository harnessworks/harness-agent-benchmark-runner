# Flask Replenishment H1 Guarded Triage - 2026-06-14

This was the focused follow-up to the two-family H1 pilot. It ran only the
new `hidden-effect-catalog-replenishment-policy` family across the two
decision-bearing arms to separate real decision-memory failures from oracle
wording brittleness.

The live run completed all 10 records with zero stalls, zero timeouts, zero
wrong-file edits, and zero forbidden-file edits. Live scoring was 8/10 strict:
both `decision-only` and `full-harness` were 4/5. The two failures had the
same cause: the glossary documented the API key `replenishment_status`, but
the oracle required the prose phrase `replenishment status`.

After triage, the oracle was narrowed to treat `replenishment_status` as
concept-equivalent documentation for the replenishment status term while still
requiring the route to be documented. Replaying all 10 saved worktrees with
the revised oracle produced 10/10 functional and record-consistency success.

## Run Conditions

- Suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`
- Task: `hidden-effect-catalog-replenishment-policy`
- Split: `heldout`
- Prompt variant: `partial-realistic`
- Arms: `decision-only`, `full-harness`
- Repeats: 5
- Planned records: 10
- Completed records: 10
- Concurrency: `--jobs 1`
- Stop-on-abnormal: enabled
- Prompt guard: `CODEX_PROMPT_GUARD=1`
- Agent timeout override: `--agent-timeout-override 900`
- Agent idle watchdog: `--agent-idle-timeout 300`
- Agent no-edit watchdog: `--agent-no-edit-timeout 240`
- Agent adapter: `examples/agents/codex_exec_agent.py`
- Live-run runner ref: `17af8a6`
- Started: `2026-06-14T05:50:18Z`
- Finished: `2026-06-14T06:09:31Z`

Target refs:

| Arm | Source | Ref |
| --- | --- | --- |
| `decision-only` | `../flask-decision-only` | `e9b0a3e919a7827497c7163912a1023c2346008f` |
| `full-harness` | `../flask-memory-harness` | `ba8b3963d071089429fa2c2c8ebc10049e80cca4` |

Command:

```bash
CODEX_PROMPT_GUARD=1 python3 scripts/run_hidden_flask_ab.py \
  --suite benchmarks/suites/flask-full-harness-memory-pilot.json \
  --task-id hidden-effect-catalog-replenishment-policy \
  --arms decision-only,full-harness \
  --repeats 5 \
  --agent-timeout-override 900 \
  --agent-idle-timeout 300 \
  --agent-no-edit-timeout 240 \
  --stop-on-abnormal \
  --execute
```

## Live Scoring

| Arm | Completed | Strict | Functional | Schema | Workflow | Boundary clean | Record consistency | Stalls | Timeouts | Wrong-file edits | Forbidden-file edits | Duration range | First repo change range |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 5 | 4 | 4 | 5 | 5 | 5 | 4/5 | 0 | 0 | 0 | 0 | 52.5-493.3s | 22.0-144.2s |
| `full-harness` | 5 | 4 | 4 | 5 | 5 | 5 | 4/5 | 0 | 0 | 0 | 0 | 52.3-65.3s | 25.0-37.0s |

Overall:

- Completed records: 10/10
- Live strict successes: 8/10
- Live record consistency: 8/10
- Stalls/timeouts: 0
- Preflight failures: 0
- Wrong-file edits: 0
- Forbidden-file edits: 0
- No-edit watchdog records: 0

## Failure Cause

The two live failures were:

| Run | Arm | Live failure |
| --- | --- | --- |
| `20260614T060112Z-hidden-effect-catalog-replenishment-policy-b00d441b` | `decision-only` | `glossary must document catalog replenishment policy route and statuses; missing: replenishment status` |
| `20260614T060821Z-hidden-effect-catalog-replenishment-policy-0031de87` | `full-harness` | `glossary must document catalog replenishment policy route and statuses; missing: replenishment status` |

Both failed worktrees implemented the adopted labels, thresholds, response key,
summary counts, and hidden edge behavior. Their glossaries documented
`replenishment_status` as the stable term, which is concept-equivalent for this
task because the task's API contract also requires the `replenishment_status`
response key.

The failure was therefore classified as oracle wording brittleness, not as
evidence that the agents missed the accepted replenishment decision.

## Oracle Revision

The oracle change was intentionally narrow:

- `GET /catalog/replenishment-policy` remains required in the glossary.
- The replenishment status concept may be documented as either
  `replenishment status` or `replenishment_status`.
- Summary counts still must include `reorder_now`, `monitor`, and `healthy`.
- Record consistency still checks the tracked decision record, forbids decision
  record edits, checks current catalog labels, and checks hidden stock 5 and
  stock 20 edge rows.

Validation added:

```text
python3 -m unittest tests.test_flask_hidden_oracle_docs
11 tests OK
```

Saved worktree replay under the revised oracle:

```text
revised_functional_record_pass 10 of 10
```

This replay used the saved isolated worktrees from
`runs/hidden-flask-ab-pilot-20260614T055018Z/` and did not mutate the raw
result records.

## Watchdog Diagnostics

`scripts/summarize_hidden_ab.py` reported:

| Target | Watchdog records | No-edit watchdogs | No observed repo changes | p50 seconds to repo change | Max seconds without repo change | Max seconds since output |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `decision-only` | 5 | 0 | 0 | 28s | - | 0s |
| `full-harness` | 5 | 0 | 0 | 35s | - | 0s |

`scripts/triage_no_edit_stalls.py` reported:

```text
## No-Edit Stall Triage

No-edit watchdog records: 0
```

One `decision-only` pass took 493.3s, with first repository changes observed
after 144.2s. This was not a stall or timeout, but it is still a duration-tail
warning for any promotion-sized H1 run.

## Reading

What this triage supports:

- The replenishment task's first live failures were caused by a brittle
  documentation wording check.
- With the corrected oracle semantics, saved decision-bearing worktrees are
  10/10 functional and record-consistent.
- The no-edit watchdog did not reproduce.

What this triage does not prove:

- It does not recheck `workflow-only` and `failure-only` controls under the
  revised oracle.
- It does not prove the full two-family H1 matrix is promotion-ready.
- It does not eliminate duration-tail risk.

## Decision

Do not run a 100-record H1 promotion immediately from the original live score.

The next useful gate is a revised-oracle two-family four-arm run:

- `hidden-effect-catalog-price-policy`
- `hidden-effect-catalog-replenishment-policy`
- arms: `workflow-only`, `decision-only`, `failure-only`, `full-harness`
- start with 1-2 repeats before any 60- or 100-record promotion

If that gate keeps controls negative, decision-bearing arms positive, and
watchdogs clean, a larger H1 promotion becomes much more valuable.

## Raw Artifacts

Raw local artifacts are intentionally not committed.

- Results JSONL:
  `results/hidden-flask-ab-pilot-20260614T055018Z/2026-06-14.jsonl`
- Run directories:
  `runs/hidden-flask-ab-pilot-20260614T055018Z/`
- Public-safe report:
  `docs/benchmarks/2026-06-14-flask-replenishment-h1-guarded-triage.md`
