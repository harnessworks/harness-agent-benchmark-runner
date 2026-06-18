# Benchmark Report Index

This directory keeps public-safe benchmark summaries. Raw `runs/` and
`results/` artifacts are intentionally ignored by git and may be archived
outside the repository after their reproducible fields are summarized here.

## Start Here

- [`latest.md`](latest.md): current benchmark status, representative result,
  latest execution, and next steps.
- [`2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md`](2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md):
  current representative 96-record Flask result.

## Current H1 Decision-Memory Line

- [`2026-06-15-flask-h1-claude-four-arm-interim-gate.md`](2026-06-15-flask-h1-claude-four-arm-interim-gate.md):
  current H1 interim representative gate; decision-bearing arms passed 4/4
  strict and record-consistent checks, while controls stayed 0/4
  record-consistent.
- [`2026-06-14-flask-h1-claude-four-arm-gate-patched-oracle-session-limit.md`](2026-06-14-flask-h1-claude-four-arm-gate-patched-oracle-session-limit.md):
  patched price-policy oracle gate; price-policy separated cleanly, but the
  replenishment half was contaminated by a Claude session limit.
- [`2026-06-14-flask-h1-claude-four-arm-gate.md`](2026-06-14-flask-h1-claude-four-arm-gate.md):
  prior Claude four-arm gate; operationally clean, with price-policy glossary
  wording noise before the oracle patch.
- [`2026-06-14-flask-h1-claude-adapter-control-two-family.md`](2026-06-14-flask-h1-claude-adapter-control-two-family.md):
  Claude two-family adapter control.
- [`2026-06-14-flask-h1-startup-retry-pilot-aborted-postoutput.md`](2026-06-14-flask-h1-startup-retry-pilot-aborted-postoutput.md):
  Codex startup-retry diagnostic that stopped on post-output no-edit.
- [`2026-06-14-flask-h1-strengthened-prompt-guard-decision-gate16.md`](2026-06-14-flask-h1-strengthened-prompt-guard-decision-gate16.md):
  clean decision-bearing gate under strengthened prompt guard.

## Current V2 Held-Out Line

- [`2026-06-18-hidden-flask-three-arm-v2-claude-pilot.md`](2026-06-18-hidden-flask-three-arm-v2-claude-pilot.md):
  clean operational 9-record Claude pilot; harness arms passed 2/3 strict and
  3/3 schema while `bare` stayed 0/3 strict and 0/3 schema. Both harness arms
  missed replenishment functional stock.
- [`2026-06-18-hidden-flask-three-arm-v2-hermes-gate18-aborted.md`](2026-06-18-hidden-flask-three-arm-v2-hermes-gate18-aborted.md):
  attempted 18-record Hermes adapter gate; stopped on the first record after an
  idle/no-observed-clone-edit watchdog signal. Do not promote the Hermes line
  beyond the 9-record repeat until the adapter is hardened.
- [`2026-06-18-hidden-flask-three-arm-v2-hermes-repeat.md`](2026-06-18-hidden-flask-three-arm-v2-hermes-repeat.md):
  clean 9-record Hermes adapter repeat; both harness arms passed 3/3 strict
  while `bare` stayed 0/3. Treat as adapter-diversity evidence, not as a direct
  Codex repeat.
- [`2026-06-18-hidden-flask-three-arm-v2-pilot.md`](2026-06-18-hidden-flask-three-arm-v2-pilot.md):
  clean 9-record Codex v2 pilot; both harness arms passed 3/3 strict while
  `bare` stayed 0/3.
- [`2026-06-13-hidden-flask-three-arm-v2-smoke.md`](2026-06-13-hidden-flask-three-arm-v2-smoke.md):
  earlier single-task v2 smoke.

## Stable-4 Harness Effect Line

- [`2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md`](2026-06-13-hidden-flask-three-arm-stable4-allslim-promotion96.md):
  representative three-arm promotion.
- [`2026-06-13-hidden-flask-three-arm-stable4-promotion96-aborted.md`](2026-06-13-hidden-flask-three-arm-stable4-promotion96-aborted.md):
  earlier promotion attempt stopped by no-edit watchdog.
- [`2026-06-13-hidden-flask-three-arm-stable4-pilot-aborted.md`](2026-06-13-hidden-flask-three-arm-stable4-pilot-aborted.md):
  pilot abort that informed later watchdog policy.

## Controls And Historical Context

- [`2026-06-12-hidden-flask-balanced-ab-100-jobs2.md`](2026-06-12-hidden-flask-balanced-ab-100-jobs2.md):
  100-run full-contract control with parallel timeout noise.
- [`2026-06-11-hidden-oracle-harness-effect-ab-3x.md`](2026-06-11-hidden-oracle-harness-effect-ab-3x.md):
  historical hidden-oracle A/B.
- [`2026-06-11-benchmark-records-analysis.md`](2026-06-11-benchmark-records-analysis.md):
  early record analysis.

## Local Artifact Policy

Keep raw artifacts out of git. For local cleanup, preserve a small working set
under `runs/` and `results/`, then move older run/result directories to a local
archive outside this repository with manifests for recovery.
