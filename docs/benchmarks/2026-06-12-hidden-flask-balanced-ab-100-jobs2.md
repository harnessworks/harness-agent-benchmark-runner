# Balanced Hidden-Oracle Flask A/B - 100-Run Jobs=2 Evidence

Date: 2026-06-12
Runner: `harness-agent-benchmark-runner` @
`ae0a1111053f365183ed4efaa475599ed09e6189`
Agent: Codex CLI `0.138.0-alpha.7` through
`examples/agents/codex_exec_agent.py`
Run ID: `hidden-flask-ab-balanced-100-jobs2-20260612T053525Z`

## Headline

| Target | Completed runs | Strict scored successes | Strict success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | 50 | 46 | 92.0% | 46 | 0 | 0 | 1 | 104s | 188s |
| `flask-yes-harness` | 50 | 48 | 96.0% | 49 | 0 | 0 | 2 | 137s | 353s |

This is the first 100-record balanced hidden-oracle Flask A/B run after the
docs oracle was relaxed from exact English phrases to concept-based route and
domain-term checks. It used `--jobs 2`, so timeout behavior is part of the
measured condition and must be interpreted separately from task quality.

## Scope

Both targets received the task-critical API contract in the prompt. The
yes-harness target still had repository-local harness guidance,
documentation-location guidance, local gate guidance, and boundary guidance.

This run measures residual harness effect under equal prompt-level API
contract disclosure, not hidden contract discovery. It also measures the
practical effect of low parallelism because the schedule used `--jobs 2`.

## Targets

- Bare target: local `flask-no-harness` @ `b5351eae78ed9f17d46a43eee05354e9e13f6b94`
- Harnessed target: local `flask-yes-harness` @ `c3eaf9a0105d7b99db414467b5df0edb833697ad`

Both target repositories were clean before execution.

## Run Conditions

- Command: `python3 scripts/run_hidden_flask_ab.py --mode large --task-dir benchmarks/tasks/flask-hidden-balanced --repeats 5 --jobs 2 --workspace runs/hidden-flask-ab-balanced-100-jobs2-20260612T053525Z --results results/hidden-flask-ab-balanced-100-jobs2-20260612T053525Z --execute`
- Started: `2026-06-12T05:35:25+00:00`
- Finished: `2026-06-12T07:41:32+00:00`
- Completed records: 100 of 100 planned records
- Task pairs: 10 hidden Flask A/B pairs
- Repetitions: 5 per target/task pair
- Pair order: `alternate`
- Concurrency: `--jobs 2`
- Task attempts: `max_attempts=1`
- Effective runner cap: `--max-agent-timeout 900`
- Budget hint: `--max-cost-usd 1.0`
- Codex model: `gpt-5.5`
- Codex config override: `CODEX_EXEC_ARGS='-c model_reasoning_effort=medium -c service_tier=priority'`

## Per-Task Results

| Target | Task | Runs | Strict scored successes | Strict success rate | Verification passed | Wrong-file edits | Forbidden-file edits | Timeouts | p50 duration | p95 duration |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | `hidden-effect-availability-badge` | 5 | 5 | 100.0% | 5 | 0 | 0 | 0 | 85s | 141s |
| `flask-no-harness` | `hidden-effect-bundle-quote` | 5 | 5 | 100.0% | 5 | 0 | 0 | 0 | 127s | 160s |
| `flask-no-harness` | `hidden-effect-cart-validation` | 5 | 5 | 100.0% | 5 | 0 | 0 | 0 | 144s | 173s |
| `flask-no-harness` | `hidden-effect-catalog-metrics` | 5 | 4 | 80.0% | 4 | 0 | 0 | 0 | 91s | 148s |
| `flask-no-harness` | `hidden-effect-catalog-segments` | 5 | 5 | 100.0% | 5 | 0 | 0 | 0 | 86s | 95s |
| `flask-no-harness` | `hidden-effect-pick-list` | 5 | 5 | 100.0% | 5 | 0 | 0 | 0 | 87s | 97s |
| `flask-no-harness` | `hidden-effect-reservation-preview` | 5 | 3 | 60.0% | 3 | 0 | 0 | 0 | 146s | 214s |
| `flask-no-harness` | `hidden-effect-stock-risk` | 5 | 4 | 80.0% | 4 | 0 | 0 | 1 | 105s | 600s |
| `flask-no-harness` | `hidden-effect-supplier-readiness` | 5 | 5 | 100.0% | 5 | 0 | 0 | 0 | 87s | 118s |
| `flask-no-harness` | `hidden-effect-tax-preview` | 5 | 5 | 100.0% | 5 | 0 | 0 | 0 | 151s | 188s |
| `flask-yes-harness` | `hidden-effect-availability-badge` | 5 | 5 | 100.0% | 5 | 0 | 0 | 0 | 122s | 246s |
| `flask-yes-harness` | `hidden-effect-bundle-quote` | 5 | 5 | 100.0% | 5 | 0 | 0 | 0 | 157s | 159s |
| `flask-yes-harness` | `hidden-effect-cart-validation` | 5 | 5 | 100.0% | 5 | 0 | 0 | 0 | 156s | 181s |
| `flask-yes-harness` | `hidden-effect-catalog-metrics` | 5 | 5 | 100.0% | 5 | 0 | 0 | 0 | 121s | 137s |
| `flask-yes-harness` | `hidden-effect-catalog-segments` | 5 | 5 | 100.0% | 5 | 0 | 0 | 0 | 121s | 137s |
| `flask-yes-harness` | `hidden-effect-pick-list` | 5 | 4 | 80.0% | 5 | 0 | 0 | 1 | 142s | 600s |
| `flask-yes-harness` | `hidden-effect-reservation-preview` | 5 | 5 | 100.0% | 5 | 0 | 0 | 0 | 169s | 307s |
| `flask-yes-harness` | `hidden-effect-stock-risk` | 5 | 5 | 100.0% | 5 | 0 | 0 | 0 | 117s | 353s |
| `flask-yes-harness` | `hidden-effect-supplier-readiness` | 5 | 4 | 80.0% | 4 | 0 | 0 | 1 | 116s | 600s |
| `flask-yes-harness` | `hidden-effect-tax-preview` | 5 | 5 | 100.0% | 5 | 0 | 0 | 0 | 179s | 224s |

## Failure Signals

| Target | Task | Count | Failure signal |
| --- | --- | ---: | --- |
| `flask-no-harness` | `hidden-effect-reservation-preview` | 2 | Hidden oracle rejected response content: reservation preview summary was wrong. |
| `flask-no-harness` | `hidden-effect-catalog-metrics` | 1 | Hidden oracle rejected companion docs: glossary missed `inventory value` and `average price`. |
| `flask-no-harness` | `hidden-effect-stock-risk` | 1 | Agent timed out at the 600-second task cap; hidden oracle also failed after timeout. |
| `flask-yes-harness` | `hidden-effect-pick-list` | 1 | Agent timed out at the 600-second task cap after verification had passed, so strict scoring failed. |
| `flask-yes-harness` | `hidden-effect-supplier-readiness` | 1 | Agent timed out at the 600-second task cap; hidden oracle also failed after timeout. |

No completed record had a wrong-file edit, forbidden-file edit, or runner
error.

## Checkpoints

| Checkpoint | `flask-no-harness` strict | `flask-yes-harness` strict | Timeout note |
| --- | ---: | ---: | --- |
| 20 records | 9 / 10 | 10 / 10 | 0 timeouts |
| 40 records | 18 / 20 | 20 / 20 | 0 timeouts |
| 60 records | 28 / 30 | 29 / 30 | 1 yes-harness timeout |
| 100 records | 46 / 50 | 48 / 50 | 1 no-harness timeout, 2 yes-harness timeouts |

## Interpretation

The strict scored-success gap is small: `flask-yes-harness` leads by 2 records
out of 50 per side, 96% vs 92%. The verification signal is slightly stronger:
`flask-yes-harness` reached 49/50 verification passes vs 46/50 for
`flask-no-harness`.

The run does not show a clean timeout-stability advantage for the harness.
Under `jobs=2`, the harnessed target had 2 agent timeouts and the bare target
had 1. One harnessed timeout had already passed verification, which means
strict scoring correctly penalized process non-completion even though the
repository state was functionally acceptable.

The cleanest positive harness signal is not boundary discipline here: both
targets had 0 wrong-file edits and 0 forbidden-file edits. The useful signal is
that the harnessed target had fewer deterministic oracle misses under equal
prompt-level contract disclosure. The no-harness misses clustered in
reservation-preview response content and catalog-metrics docs concepts.

This result supports a limited claim: under the measured balanced Flask task
shape, the harnessed repository produced a small residual success-rate and
verification-rate lift, but `jobs=2` introduced timeout noise. A sequential
follow-up, or a jobs=2 follow-up with a larger timeout cap, would be needed
before making a clean claim about timeout stability.

## Raw Artifacts

Raw local artifacts are intentionally not committed:

- Results JSONL: `results/hidden-flask-ab-balanced-100-jobs2-20260612T053525Z/2026-06-12.jsonl`
- Run directories: `runs/hidden-flask-ab-balanced-100-jobs2-20260612T053525Z/`
