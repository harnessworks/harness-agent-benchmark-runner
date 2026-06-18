# Latest Benchmark Status

Updated: 2026-06-18

## At A Glance

| Question | Answer |
| --- | --- |
| Representative result | `2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md` |
| Main claim | Safety and failure measurement are strong; raw coding lift is not the main claim. |
| Cleanliness | 96/96 records completed with 0 stalls, 0 timeouts, 0 hidden-access findings, 0 wrong-file edits, and 0 forbidden-file edits. |
| Harness signal | Schema contract improved from 0/32 in `bare` to 24/32 in both harness arms. |
| Memory signal | Accuracy tied `workflow-only`; duration tail was better. |
| Latest execution | Claude v2 pilot completed 9/9 with 0 operational abnormal signals; harness arms passed 2/3 strict and 3/3 schema while `bare` stayed 0/3 strict and 0/3 schema. Local Hermes adapter v2 repeat completed 9/9 clean with both harness arms 3/3 strict, but a follow-up 18-record Hermes gate attempt aborted on the first record due to an idle/no-observed-clone-edit watchdog signal. Comparable Codex v2 pilot completed 9/9 clean with both harness arms 3/3 strict. |

## Representative Result

Current representative report:
[`2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md`](2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md).

Supported kit-effect claim:

> In answer-free held-out Flask tasks, the kit made agent work safer and more
> measurable, and the harnessed repos preserved project API/schema conventions
> that the bare repo missed. The representative run completed 96/96 records
> with no operational abnormal events, and schema-contract success improved
> from 0/32 in `bare` to 24/32 in both harness arms.

This is the result currently promoted as the public benchmark headline. Its
claim is not "the harness always makes agents better at coding." Its claim is
more specific: the kit makes agent work safer to run and much easier to measure
when the task depends on repository-local conventions.

Why this run is representative:

- It completed the full 96-record sequential promotion with `--jobs 1`.
- It used three arms: `bare`, `workflow-only`, and `memory-harness`.
- It used answer-free `partial-realistic` prompts.
- It kept task-specific answers and hidden oracle logic out of target
  repositories.
- It separated strict, functional, schema, workflow, boundary, timeout, and
  duration-tail signals.
- It completed with 0 stalls, 0 timeouts, 0 hidden-access findings,
  0 wrong-file edits, and 0 forbidden-file edits.

| Arm | Runs | Strict | Functional | Schema contract | Workflow | Boundary clean | p95 duration | Max duration |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 32 | 0 | 0 | 0 | 32 | 32 | 134.6s | 639.3s |
| `workflow-only` | 32 | 8 | 8 | 24 | 32 | 32 | 124.1s | 544.7s |
| `memory-harness` | 32 | 8 | 8 | 24 | 32 | 32 | 86.2s | 87.6s |

## Interpretation

The current evidence is strongest for safety, repeatability, and failure
measurement:

- The runner distinguished 80 expected benchmark failures from runner
  abnormalities.
- The three-arm design made the `bare` baseline, workflow guidance, and memory
  layer separable.
- Hidden-access, timeout, wrong-file, and forbidden-file counts all remained
  clean in the representative promotion.
- Per-dimension scoring showed where the harness helped: schema contract
  success improved from 0/32 to 24/32 for both harness arms.
- Per-task scoring showed where the harness did not solve the task:
  `cart-validation` stayed 0/8 strict and 0/8 schema across all arms.

Correctness lift exists, but it is narrow. Both harness arms passed
`catalog-segments` 8/8 strict while `bare` passed 0/8. The same result does
not prove a general raw-coding lift, and `memory-harness` did not improve
accuracy over `workflow-only`. The memory arm's useful signal in this suite is
duration-tail repeatability.

## Latest Run

Latest completed Claude v2 pilot:
[`2026-06-18-hidden-flask-three-arm-v2-claude-pilot.md`](2026-06-18-hidden-flask-three-arm-v2-claude-pilot.md).

The Claude adapter pilot completed 9/9 records with 0 stalls, 0 timeouts,
0 hidden-access findings, 0 wrong-file edits, and 0 forbidden-file edits.
`bare` stayed 0/3 strict and 0/3 schema. Both harness arms passed 3/3 schema
and 2/3 strict, failing only the replenishment functional oracle with the same
`desk-lamp stock is wrong` message.

Latest attempted Hermes expansion:
[`2026-06-18-hidden-flask-three-arm-v2-hermes-gate18-aborted.md`](2026-06-18-hidden-flask-three-arm-v2-hermes-gate18-aborted.md).
An attempted 18-record Hermes adapter gate stopped on the first record after the
idle watchdog fired with no observed repository changes in the isolated clone.
Do not promote the Hermes adapter line beyond the clean 9-record repeat until
adapter isolation and output/watchdog behavior are hardened.

Latest completed local Hermes v2 adapter-diversity repeat:
[`2026-06-18-hidden-flask-three-arm-v2-hermes-repeat.md`](2026-06-18-hidden-flask-three-arm-v2-hermes-repeat.md).

The Hermes adapter repeat completed 9/9 records with 0 stalls, 0 timeouts,
0 hidden-access findings, 0 wrong-file edits, and 0 forbidden-file edits.
`bare` stayed 0/3 strict, while both `workflow-only` and `memory-harness`
passed 3/3 strict across replenishment signals, price ladder, and value
snapshot tasks. This is useful adapter-diversity evidence, not a direct Codex
repeat, because the local Codex CLI was unavailable and the run used a temporary
Hermes CLI adapter.

Comparable Codex v2 pilot:
[`2026-06-18-hidden-flask-three-arm-v2-pilot.md`](2026-06-18-hidden-flask-three-arm-v2-pilot.md).
The Codex v2 held-out pilot also completed 9/9 records with 0 operational
abnormal signals and the same strict pattern: `bare` 0/3, both harness arms 3/3.

Treat both v2 runs as latest clean execution evidence and useful v2 pilots, not
as replacements for the 96-record stable-4 representative benchmark.

## Controls And Prior Evidence

| Scope | Mode | Runs | Strict successes | Verification passed | Timeouts | Boundary issues | Reading |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Three-arm v2 | Claude pilot | 9 | 4 | 4 | 0 | 0 | Clean operational run; harness arms 2/3 strict each and 3/3 schema each, `bare` 0/3. Harness arms missed replenishment functional stock. |
| Three-arm v2 | Hermes adapter gate18 aborted | 1/18 | 0 | 0 | 1 | 0 | Stopped on first `bare` replenishment record after idle/no-observed-clone-edit watchdog; do not promote Hermes line beyond 9-record repeat yet. |
| Three-arm v2 | Hermes adapter repeat | 9 | 6 | 6 | 0 | 0 | Latest completed local adapter-diversity evidence; both harness arms 3/3 strict, `bare` 0/3. Not a direct Codex repeat. |
| Three-arm v2 | held-out pilot | 9 | 6 | 6 | 0 | 0 | Comparable Codex v2 pilot; both harness arms 3/3 strict, `bare` 0/3. |
| Three-arm stable-4 | promotion96 `bare` | 32 | 0 | 0 | 0 | 0 | Representative negative baseline. |
| Three-arm stable-4 | promotion96 `workflow-only` | 32 | 8 | 8 | 0 | 0 | Workflow and docs conventions recover schema behavior. |
| Three-arm stable-4 | promotion96 `memory-harness` | 32 | 8 | 8 | 0 | 0 | Same correctness as workflow-only, lower duration tail. |
| Two-family H1 | Claude interim gate | 8 | 4 | 4 | 0 | 0 | Current H1 interim representative; decision-bearing arms 4/4, controls 0/4 record-consistent. |
| Two-family H1 | Claude patched-oracle gate | 8 | 2 | 2 | 0 | 0 | Price-policy separated cleanly; replenishment half contaminated by Claude CLI session limit. |
| Two-family H1 | Claude four-arm gate | 8 | 2 | 2 | 0 | 0 | No operational abnormal events; replenishment separated cleanly, price-policy wording remained noisy. |
| Two-family H1 | Claude adapter-control | 4 | 3 | 3 | 0 | 0 | Decision-bearing arms completed with no no-edit stalls; one `full-harness` glossary wording miss. |
| Price-policy H1 | Claude adapter-control | 2 | 1 | 1 | 0 | 0 | Completed with no no-edit stalls; `full-harness` strict, `decision-only` glossary wording miss. |
| Two-family H1 | startup-retry pilot aborted | 1/8 | 0 | 0 | 1 | 0 | Startup retry correctly did not apply; stopped on post-output no-edit after decision discovery. |
| Two-family H1 | strengthened promotion96 aborted | 8/96 | 3 | 3 | 1 | 0 | Stopped on `full-harness` replenishment startup/no-output no-edit. |
| Two-family H1 | strengthened prompt-guard decision gate16 | 16 | 16 | 16 | 0 | 0 | Decision-bearing arms 16/16 strict and record-consistent; no no-edit recurrence. |
| Two-family H1 | strengthened prompt-guard diagnostic | 8 | 8 | 8 | 0 | 0 | Stronger edit-before-plan guard cleared the small decision-bearing matrix. |
| Two-family H1 | prompt-guard mitigation diagnostic | 8 | 7 | 7 | 1 | 0 | Generic edit-start guard did not prevent `decision-only` replenishment no-edit. |
| Two-family H1 | decision-arms time-to-first-edit diagnostic | 8 | 8 | 8 | 0 | 0 | Decision-bearing arms started edits within 22.0-38.1s; no no-edit reproduction in small batch. |
| Two-family H1 | promotion96 rerun aborted | 13/96 | 6 | 6 | 1 | 0 | Second promotion-scale no-edit stop, this time on `decision-only` replenishment. |
| Price-policy H1 | full-harness no-edit diagnostic | 5 | 5 | 5 | 0 | 0 | Did not reproduce the promotion no-edit failure. |
| Two-family H1 | promotion96 aborted | 11/96 | 5 | 5 | 1 | 0 | Stopped on `full-harness` price-policy no-edit after decision lookup. |
| Two-family H1 | revised-oracle four-arm gate | 16 | 8 | 8 | 0 | 0 | Decision-bearing arms 8/8 record-consistent; controls 0/8. |
| Replenishment H1 | guarded decision-bearing triage | 10 | 8 live / 10 revised | 8 live / 10 revised | 0 | 0 | Oracle wording brittleness fixed; controls still need revised-oracle rerun. |
| Two-family H1 | guarded pilot | 8 | 3 | 3 | 0 | 0 | Operationally clean, but replenishment passed only in `full-harness`; not promotion-ready. |
| Price-policy H1 | guarded stability24 rerun | 24 | 12 | 12 | 0 | 0 | Completed four-arm stability gate; decision-bearing arms 12/12 record-consistent, controls 0/12. |
| Price-policy H1 | guarded decision-arms no-edit triage | 8 | 8 | 8 | 0 | 0 | Decision-bearing arms completed cleanly; no-edit stall did not immediately reproduce. |
| Price-policy H1 | guarded stability24 expansion | 4/24 | 1 | 1 | 1 | 0 | Aborted on `full-harness` no-edit watchdog after decision-record discovery. |
| Price-policy H1 | guarded clean gate | 12 | 6 | 6 | 0 | 0 | Guarded four-arm H1 gate completed; decision memory arms separated cleanly from controls. |
| Price-policy H1 | guarded decision-only diagnostic | 2 | 2 | 2 | 0 | 0 | Prompt guard coincided with quick repo edits; mitigation signal only. |
| Price-policy H1 | stability24 expansion | 2/24 | 0 | 0 | 1 | 0 | Aborted on `decision-only` no-edit watchdog despite prior clean readiness. |
| Price-policy H1 | non-bare clean gate rerun | 12 | 6 | 6 | 0 | 0 | Completed focused H1 gate; decision memory arms separated cleanly from controls. |
| Price-policy H1 | non-bare clean gate | 8/12 | 4 | 4 | 1 | 0 | H1 signal held, but gate aborted on no-edit watchdog. |
| Three-arm v2 | replenishment smoke | 3 | 2 | 2 | 0 | 0 | Scaffold check only. |
| Balanced Flask A/B | 100-run `jobs=2` full-contract control | 100 | 94 | 95 | 3 | 0 | Useful control, but parallel timeout stability remains unresolved. |
| Hidden-oracle Flask A/B | 3x convention-dependent tasks | 24 | 11 | 11 | 3 | 11 | Historical strong signal, but older and less balanced than the representative three-arm run. |

The balanced 100-run `jobs=2` report remains useful as a full-contract control:
both arms received task-critical API contracts in the prompt. It is not the
main product claim because the prompt disclosed much more of the answer and the
parallel execution introduced timeout noise.

Older `harness-starter-kit` runs remain adapter validation evidence. The Flask
hidden-oracle rows are the relevant harness-effect evidence.

## Next Step

Do not rerun the same stable-4 96-record promotion unless the harness or runner
semantics change. For H1, do not run another blind 96/100-record promotion
now. Two promotion-scale attempts have stopped on no-edit watchdogs across
different task/arm pairs.

The latest clean Claude four-arm gate suggests the repeated no-edit blocker is
specific to the Codex execution path rather than the runner, target refs, or
watchdog mechanics. Do not keep rerunning blind Codex H1 promotions. The next
useful H1 step is a repeated 16-record or 24-record Claude gate before making
a larger H1 claim.

The next useful v2 work is adapter hardening before another larger Hermes gate,
or a comparable Codex repeat after the Codex CLI is restored locally. For the
Hermes adapter line, do not rerun blind 16/18/24-record gates until the adapter
has a clone-isolation smoke check and emits a startup/progress line that avoids
ambiguous no-output watchdog stops. Once hardened, use the same three-task suite:

- `hidden-effect-replenishment-signals`
- `hidden-effect-catalog-price-ladder`
- `hidden-effect-catalog-value-snapshot`

Keep the same three arms and continue to report functional, schema-contract,
workflow, boundary, strict, timeout, and duration-tail metrics separately. Do
not merge Hermes adapter results into the Codex line without labeling the agent
adapter difference.

## Detailed Reports

- [`index.md`](index.md) (curated report index)
- [`2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md`](2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md) (representative result)
- [`2026-06-18-hidden-flask-three-arm-v2-claude-pilot.md`](2026-06-18-hidden-flask-three-arm-v2-claude-pilot.md) (latest completed Claude v2 pilot)
- [`2026-06-18-hidden-flask-three-arm-v2-hermes-gate18-aborted.md`](2026-06-18-hidden-flask-three-arm-v2-hermes-gate18-aborted.md) (attempted Hermes v2 expansion, aborted on idle/no-observed-clone-edit)
- [`2026-06-18-hidden-flask-three-arm-v2-hermes-repeat.md`](2026-06-18-hidden-flask-three-arm-v2-hermes-repeat.md) (latest completed local v2 adapter-diversity repeat)
- [`2026-06-18-hidden-flask-three-arm-v2-pilot.md`](2026-06-18-hidden-flask-three-arm-v2-pilot.md) (comparable Codex v2 pilot)
- [`2026-06-15-flask-h1-claude-four-arm-interim-gate.md`](2026-06-15-flask-h1-claude-four-arm-interim-gate.md) (current H1 interim representative gate)
- [`2026-06-14-flask-h1-claude-four-arm-gate-patched-oracle-session-limit.md`](2026-06-14-flask-h1-claude-four-arm-gate-patched-oracle-session-limit.md) (patched-oracle H1 Claude gate, contaminated by Claude session limit)
- [`2026-06-14-flask-h1-claude-four-arm-gate.md`](2026-06-14-flask-h1-claude-four-arm-gate.md) (prior H1 four-arm Claude gate)
- [`2026-06-14-flask-h1-claude-adapter-control-two-family.md`](2026-06-14-flask-h1-claude-adapter-control-two-family.md) (latest H1 adapter-control, Claude two-family gate)
- [`2026-06-14-flask-h1-claude-adapter-control-price-policy.md`](2026-06-14-flask-h1-claude-adapter-control-price-policy.md) (latest H1 adapter-control, Claude completed with 0 no-edit stalls)
- [`2026-06-14-flask-h1-startup-retry-pilot-aborted-postoutput.md`](2026-06-14-flask-h1-startup-retry-pilot-aborted-postoutput.md) (latest H1 startup-retry diagnostic, aborted on post-output no-edit)
- [`2026-06-14-flask-h1-strengthened-promotion96-aborted-nooutput.md`](2026-06-14-flask-h1-strengthened-promotion96-aborted-nooutput.md) (latest scoped H1 promotion, aborted on startup/no-output no-edit)
- [`2026-06-14-flask-h1-strengthened-prompt-guard-decision-gate16.md`](2026-06-14-flask-h1-strengthened-prompt-guard-decision-gate16.md) (latest H1 strengthened prompt-guard decision-bearing gate)
- [`2026-06-14-flask-h1-strengthened-prompt-guard-diagnostic.md`](2026-06-14-flask-h1-strengthened-prompt-guard-diagnostic.md) (prior H1 prompt-guard mitigation diagnostic)
- [`2026-06-14-flask-h1-prompt-guard-mitigation-diagnostic.md`](2026-06-14-flask-h1-prompt-guard-mitigation-diagnostic.md) (prior H1 prompt-guard mitigation diagnostic)
- [`2026-06-14-flask-h1-decision-arms-time-to-first-edit-diagnostic.md`](2026-06-14-flask-h1-decision-arms-time-to-first-edit-diagnostic.md) (prior H1 decision-bearing no-edit diagnostic)
- [`2026-06-14-flask-h1-promotion96-rerun-aborted-noedit.md`](2026-06-14-flask-h1-promotion96-rerun-aborted-noedit.md) (latest scoped H1 promotion rerun, aborted on no-edit)
- [`2026-06-14-flask-price-policy-full-harness-noedit-diagnostic.md`](2026-06-14-flask-price-policy-full-harness-noedit-diagnostic.md) (focused no-edit diagnostic)
- [`2026-06-14-flask-h1-promotion96-aborted-noedit.md`](2026-06-14-flask-h1-promotion96-aborted-noedit.md) (scoped H1 promotion, aborted on no-edit)
- [`2026-06-14-flask-h1-revised-oracle-two-family-gate.md`](2026-06-14-flask-h1-revised-oracle-two-family-gate.md) (latest revised-oracle two-family H1 gate)
- [`2026-06-14-flask-replenishment-h1-guarded-triage.md`](2026-06-14-flask-replenishment-h1-guarded-triage.md) (latest guarded replenishment H1 triage)
- [`2026-06-14-flask-h1-two-family-guarded-pilot.md`](2026-06-14-flask-h1-two-family-guarded-pilot.md) (prior guarded two-family H1 pilot)
- [`2026-06-14-flask-price-policy-h1-guarded-stability24-rerun.md`](2026-06-14-flask-price-policy-h1-guarded-stability24-rerun.md) (guarded H1 stability rerun)
- [`2026-06-14-flask-price-policy-h1-decision-arms-noedit-triage.md`](2026-06-14-flask-price-policy-h1-decision-arms-noedit-triage.md) (guarded H1 decision-bearing no-edit triage)
- [`2026-06-14-flask-price-policy-h1-guarded-stability24-aborted.md`](2026-06-14-flask-price-policy-h1-guarded-stability24-aborted.md) (guarded H1 stability expansion, aborted)
- [`2026-06-14-flask-price-policy-h1-guarded-clean-gate.md`](2026-06-14-flask-price-policy-h1-guarded-clean-gate.md) (guarded H1 clean gate)
- [`2026-06-14-flask-price-policy-h1-decision-guard-diagnostic.md`](2026-06-14-flask-price-policy-h1-decision-guard-diagnostic.md) (guarded H1 decision-only diagnostic)
- [`2026-06-14-flask-price-policy-h1-stability24-aborted.md`](2026-06-14-flask-price-policy-h1-stability24-aborted.md) (focused H1 stability expansion, aborted)
- [`2026-06-14-flask-price-policy-h1-clean-gate-rerun.md`](2026-06-14-flask-price-policy-h1-clean-gate-rerun.md) (focused H1 clean gate rerun)
- [`2026-06-14-flask-price-policy-h1-clean-gate-aborted.md`](2026-06-14-flask-price-policy-h1-clean-gate-aborted.md) (focused H1 clean gate, aborted)
- [`2026-06-14-flask-price-policy-h1-discoverability-3x.md`](2026-06-14-flask-price-policy-h1-discoverability-3x.md) (focused H1 discoverability triage)
- [`2026-06-14-flask-price-policy-h1-rerun-3x.md`](2026-06-14-flask-price-policy-h1-rerun-3x.md) (focused H1 triage)
- [`2026-06-13-hidden-flask-three-arm-v2-smoke.md`](2026-06-13-hidden-flask-three-arm-v2-smoke.md) (latest v2 scaffold check)
- [`2026-06-13-hidden-flask-workflow-smoke-stable4-fullcontract-control.md`](2026-06-13-hidden-flask-workflow-smoke-stable4-fullcontract-control.md) (full-contract control)
- [`2026-06-12-hidden-flask-balanced-ab-100-jobs2.md`](2026-06-12-hidden-flask-balanced-ab-100-jobs2.md) (100-run full-contract control)
- [`2026-06-11-hidden-oracle-harness-effect-ab-3x.md`](2026-06-11-hidden-oracle-harness-effect-ab-3x.md) (historical hidden-oracle A/B)
- [`2026-06-11-benchmark-records-analysis.md`](2026-06-11-benchmark-records-analysis.md) (records analysis)

## Raw Artifacts

Raw `runs/` and `results/` artifacts are intentionally ignored by git. Public
docs should summarize reproducible fields from those artifacts without
committing full logs, cloned repositories, credentials, or local run output.
