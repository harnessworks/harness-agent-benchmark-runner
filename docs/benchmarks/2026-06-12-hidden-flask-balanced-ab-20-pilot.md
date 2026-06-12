# Balanced Hidden-Oracle Flask A/B - 20-Run Pilot

Date: 2026-06-12
Runner: `harness-agent-benchmark-runner` working tree on branch
`codex/balanced-hidden-flask-ab`
Agent: Codex CLI through `examples/agents/codex_exec_agent.py`
Run ID: `hidden-flask-ab-balanced-20-20260612T034429Z`

## Headline

| Target | Completed runs | Strict scored successes | Strict success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | 10 | 6 | 60.0% | 6 | 0 | 0 | 0 | 85s | 188s |
| `flask-yes-harness` | 10 | 10 | 100.0% | 10 | 0 | 0 | 0 | 129s | 203s |

This is a balanced hidden-oracle A/B 20-run pilot. It is not the earlier
hidden-contract calibration: both sides received the task-critical API contract
in the prompt, including endpoint, method, request shape, response keys,
business rules, constants or maps, status codes, and docs-boundary guidance.

## Task Shape

Task specs were added under:

```text
benchmarks/tasks/flask-hidden-balanced/
```

The run used 10 task pairs, one no-harness run plus one yes-harness run for
each task, with `repeats=1`.

Dry-run plan:

```text
Task pairs: 10
Repeats: 1
Planned runs: 20
Pair order: alternate
```

The prompt is byte-for-byte identical within each no/yes task pair. The
harnessed target still has repository-local workflow guidance, docs location
guidance, local gate guidance, and boundary guidance. The balanced prompt is
intended to be the source of truth for the task-specific API contract, reducing
the previous information asymmetry.

## Targets

- Bare target: local `flask-no-harness` @ `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- Harnessed target: local `flask-yes-harness` @ `c3eaf9a0105d7b99db414467b5df0edb833697ad`

Both target repositories were clean before execution.

## Run Conditions

- Command: `python3 scripts/run_hidden_flask_ab.py --mode large --task-dir benchmarks/tasks/flask-hidden-balanced --repeats 1 --workspace runs/hidden-flask-ab-balanced-20-20260612T034429Z --results results/hidden-flask-ab-balanced-20-20260612T034429Z --execute`
- Completed records: 20 of 20 planned records
- Task pairs: 10 hidden Flask A/B pairs
- Pair order: `alternate`
- Task attempts: `max_attempts=1`
- Effective runner cap: `--max-agent-timeout 900`
- Budget hint: `--max-cost-usd 1.0`
- Codex model: `gpt-5.5`
- Codex config override: `CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`

## Per-Task Results

| Target | Task | Runs | Strict scored successes | Strict success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | `hidden-effect-availability-badge` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 77s | 77s |
| `flask-no-harness` | `hidden-effect-bundle-quote` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 106s | 106s |
| `flask-no-harness` | `hidden-effect-cart-validation` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 85s | 85s |
| `flask-no-harness` | `hidden-effect-catalog-metrics` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 83s | 83s |
| `flask-no-harness` | `hidden-effect-catalog-segments` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 78s | 78s |
| `flask-no-harness` | `hidden-effect-pick-list` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 125s | 125s |
| `flask-no-harness` | `hidden-effect-reservation-preview` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 188s | 188s |
| `flask-no-harness` | `hidden-effect-stock-risk` | 1 | 0 | 0.0% | 0 | 0 | 0 | 0 | 67s | 67s |
| `flask-no-harness` | `hidden-effect-supplier-readiness` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 86s | 86s |
| `flask-no-harness` | `hidden-effect-tax-preview` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 136s | 136s |
| `flask-yes-harness` | `hidden-effect-availability-badge` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 129s | 129s |
| `flask-yes-harness` | `hidden-effect-bundle-quote` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 203s | 203s |
| `flask-yes-harness` | `hidden-effect-cart-validation` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 174s | 174s |
| `flask-yes-harness` | `hidden-effect-catalog-metrics` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 103s | 103s |
| `flask-yes-harness` | `hidden-effect-catalog-segments` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 139s | 139s |
| `flask-yes-harness` | `hidden-effect-pick-list` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 118s | 118s |
| `flask-yes-harness` | `hidden-effect-reservation-preview` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 146s | 146s |
| `flask-yes-harness` | `hidden-effect-stock-risk` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 92s | 92s |
| `flask-yes-harness` | `hidden-effect-supplier-readiness` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 102s | 102s |
| `flask-yes-harness` | `hidden-effect-tax-preview` | 1 | 1 | 100.0% | 1 | 0 | 0 | 0 | 161s | 161s |

## Failure Signals

All failures were in `flask-no-harness`. The agent exited cleanly in each failed
record, and pytest passed before the hidden oracle assertion failed.

| Target | Task | Failure signal |
| --- | --- | --- |
| `flask-no-harness` | `hidden-effect-availability-badge` | Hidden oracle rejected docs wording: glossary did not include the expected `availability badge endpoint` phrase. |
| `flask-no-harness` | `hidden-effect-cart-validation` | Hidden oracle rejected functional output: cart validation summary was wrong. |
| `flask-no-harness` | `hidden-effect-catalog-segments` | Hidden oracle rejected docs wording: glossary did not include the expected `catalog segments endpoint` phrase. |
| `flask-no-harness` | `hidden-effect-stock-risk` | Hidden oracle rejected docs wording: glossary did not include the expected `stock risk report endpoint` phrase. |

No completed record had a wrong-file edit, forbidden-file edit, or timeout.

Post-pilot oracle update: after reviewing these failures, the docs checks were
relaxed from exact phrase substrings to concept-based checks. The revised
oracle expects the relevant route and domain terms in companion docs, rather
than the literal phrases listed above. The 20 records in this report were scored
before that change, so future balanced runs should not be compared as strict
apples-to-apples evidence without noting the oracle revision.

Post-hoc rescore with the revised docs oracle:

| Target | Saved runs | Run-time strict successes | Current concept-docs rescore | Remaining failure |
| --- | ---: | ---: | ---: | --- |
| `flask-no-harness` | 10 | 6 | 9 | `hidden-effect-cart-validation` summary mismatch |
| `flask-yes-harness` | 10 | 10 | 10 | none |

## Interpretation

The balanced prompt removed the strongest contract-discovery asymmetry from the
earlier calibration. Under this fairer shape, the no-harness target improved
from 0/10 in the previous 1x hidden-contract calibration to 6/10 here, while
the yes-harness target remained 10/10.

The run-time gap should be interpreted as a mix of implementation correctness
and docs-oracle exactness. Three of the four no-harness misses were
docs-content exactness misses, not endpoint behavior misses. That finding led
to the post-pilot oracle update above. Under the revised oracle, the saved
outputs narrow to a 9/10 vs 10/10 split, with the remaining no-harness miss
being functional.

Strict scored success and verification passed stayed aligned in this pilot.
Wrong-file edits, forbidden-file edits, and timeouts were all zero, so this run
does not show a file-boundary or timeout difference between targets.

## 100-Run Recommendation

Do not scale the original phrase-based task shape directly to 100 runs. Rerun a
balanced pilot with the concept-based docs oracle first. If that still completes
cleanly, a 100-run expansion with `repeats=5` is justified: the first 20-run
pilot completed cleanly, produced no boundary noise, and showed a large but less
artificial gap than the earlier hidden-contract calibration.

## Raw Artifacts

Raw local artifacts are intentionally not committed:

- Results JSONL: `results/hidden-flask-ab-balanced-20-20260612T034429Z/2026-06-12.jsonl`
- Run directories: `runs/hidden-flask-ab-balanced-20-20260612T034429Z/`
