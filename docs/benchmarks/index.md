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
