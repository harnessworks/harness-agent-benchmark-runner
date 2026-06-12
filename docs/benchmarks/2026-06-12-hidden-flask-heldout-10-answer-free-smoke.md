# Hidden Flask Held-Out 10-Run Answer-Free Harness Smoke

Date: 2026-06-12
Runner: `harness-agent-benchmark-runner` @
`674879c180ee76a2f46e8e71ca6ded254ae2340e` with local uncommitted task/report
work
Agent: Codex CLI `0.138.0-alpha.7` through
`examples/agents/codex_exec_agent.py`
Run ID: `hidden-flask-ab-heldout-10-20260612T085000Z`

## Headline

| Target | Runs | Strict scored successes | Verification passed | Harness gate passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | Max duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | 5 | 0 | 0 | n/a | 0 | 0 | 1 | 148s | 600s |
| `flask-yes-harness` | 5 | 0 | 0 | 5 | 0 | 0 | 0 | 128s | 187s |

## Scope

This was a quick diagnostic 10-run smoke for the answer-memory-free harness
question, not a new representative evidence run.

The task set used five medium-realistic partial prompts:

- `hidden-effect-availability-badge`
- `hidden-effect-bundle-quote`
- `hidden-effect-cart-validation`
- `hidden-effect-catalog-metrics`
- `hidden-effect-catalog-segments`

Targets:

- Bare target: local `flask-no-harness` @
  `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- Answer-memory-free harness target: local `flask-yes-harness` @
  `91da156916e4cf924ded1fdc4d4db80338b19284`
  (`Remove hidden API contract memory`)

The yes-harness target kept the generic harness workflow, local gate, docs
placement rules, and boundary guidance, but removed the hidden task-specific
API convention memory used by earlier full-harness calibration runs.

## Results

| Target | Task | Strict success | Failure signal |
| --- | --- | ---: | --- |
| `flask-no-harness` | `hidden-effect-availability-badge` | 0 | Hidden oracle rejected response content: availability product summary was wrong. |
| `flask-no-harness` | `hidden-effect-bundle-quote` | 0 | Hidden oracle rejected request handling: expected 200, got `invalid_items`. |
| `flask-no-harness` | `hidden-effect-cart-validation` | 0 | Hidden oracle rejected response content: cart validation summary was wrong. |
| `flask-no-harness` | `hidden-effect-catalog-metrics` | 0 | Agent timed out; hidden oracle then saw missing `/catalog/metrics`. |
| `flask-no-harness` | `hidden-effect-catalog-segments` | 0 | Hidden oracle rejected metadata: catalog segments rules marker was wrong. |
| `flask-yes-harness` | `hidden-effect-availability-badge` | 0 | Hidden oracle rejected response content: availability product summary was wrong. |
| `flask-yes-harness` | `hidden-effect-bundle-quote` | 0 | Hidden oracle rejected request handling: expected 200, got `invalid_items`. |
| `flask-yes-harness` | `hidden-effect-cart-validation` | 0 | Hidden oracle rejected response shape: cart validation did not return top-level `items`. |
| `flask-yes-harness` | `hidden-effect-catalog-metrics` | 0 | Hidden oracle rejected response content: catalog metrics `total_skus` was wrong. |
| `flask-yes-harness` | `hidden-effect-catalog-segments` | 0 | Hidden oracle rejected metadata: catalog segments rules marker was wrong. |

All completed records had 0 wrong-file edits and 0 forbidden-file edits.

## Interpretation

This smoke does not support a claim that generic harness workflow alone fixes
hidden schema inference under partial prompts. Once task-specific API convention
memory was removed from `flask-yes-harness`, both targets missed the hidden
oracle contract on all five tasks.

The useful positive harness signal is narrower: `flask-yes-harness` ran and
passed its local `scripts/check_harness.py` gate in all five records and had no
timeouts, while `flask-no-harness` had one timeout. However, the local gate did
not catch the hidden schema mismatches.

The practical product implication is that the earlier large full-harness lift
was mostly a repository-memory effect, not an isolated workflow-gate effect.
For product evidence, future held-out tasks should use naturally accumulated
project conventions that are not benchmark-answer records, then measure whether
that memory generalizes to new partial prompts.

## Raw Artifacts

Raw `runs/` and `results/` artifacts remain local and intentionally untracked.
This report summarizes only public-safe fields: target refs, task ids, counts,
durations, boundary counts, timeout counts, and hidden-oracle failure signals.
