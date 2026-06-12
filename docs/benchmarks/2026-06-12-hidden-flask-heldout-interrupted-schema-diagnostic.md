# Hidden Flask Heldout Interrupted Schema Diagnostic - 2026-06-12

## Summary

An attempted `partial-realistic` heldout pilot was interrupted after 3 complete
records and one in-progress record. The run is diagnostic only and is not
representative evidence.

The useful finding is methodological: the previous heldout task specs used the
strict exact hidden oracle for product-style partial prompts. That made hidden
task-specific response keys and request envelope choices part of the success
criterion even when those details were not in the prompt and were not
generalized by harness memory.

## Run Shape

- Suite: `benchmarks/suites/flask-hidden-heldout-10.json`
- Command shape: `task_limit=5`, `repeats=2`, sequential
- Completed records: 3
- Interrupted record: `hidden-effect-bundle-quote` on the harnessed target
- Raw local paths: `runs/hidden-flask-heldout-20-20260612T0945Z/` and
  `results/hidden-flask-heldout-20-20260612T0945Z/`

## Completed Records

| Target arm | Task | Strict success | Functional success | Schema success | Workflow success | Boundary issues | Failure symptom |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `bare` | `hidden-effect-availability-badge` | 0 | 0 | 0 | 1 | 0 | Strict oracle required an exact `product` object and `availability.badge`; the implementation used a nearby but different shape and lacked the documented domain glossary. |
| `workflow-only` | `hidden-effect-availability-badge` | 0 | 0 | 0 | 1 | 0 | Local harness gate passed; strict oracle rejected exact field naming and product summary shape. |
| `bare` | `hidden-effect-bundle-quote` | 0 | 0 | 0 | 1 | 0 | Strict oracle sent request key `bundle`; implementation accepted `items`, which is a plausible item-list envelope under the partial prompt. |

The in-progress harnessed `hidden-effect-bundle-quote` run was inspected before
discarding it as a benchmark record. Its implementation passed the revised
functional and generic schema oracles, confirming that the earlier strict
failure was primarily an exact-schema mismatch.

## Root Cause

The product-style heldout suite was still using an exact hidden oracle as the
only success oracle. That contradicts the intended experiment design:

- `partial-realistic` prompts should measure whether generalized conventions
  transfer to new work.
- Exact task-specific response keys, request envelope names, and hidden marker
  constants should not be required unless the prompt or generalized memory
  makes them available.
- `full-contract` controls may keep exact strict checks because the prompt
  gives the contract.

## Fix Applied

- `benchmarks/oracles/flask_hidden_oracle.py` now supports three modes:
  `strict`, `functional`, and `schema`.
- `strict` remains the default for full-contract/control suites.
- `functional` checks behavior and business rules without requiring arbitrary
  exact hidden response shape.
- `schema` checks generic JSON/API style: object envelopes, snake_case keys,
  decimal-compatible money-like fields, client-error shape, and `meta.service`
  where appropriate.
- `benchmarks/tasks/flask-hidden-heldout-10/*.json` now calls functional and
  schema checks as separate verification commands.
- Harnessed heldout tasks keep the local `harness gate` command tagged as
  `workflow`.

## Interpretation

Do not run a 100-record product experiment on the old strict heldout scoring.
The corrected design should first be re-piloted at 20 records. If functional,
schema, workflow, preflight, and timeout signals look stable, then a 100-record
run is meaningful.
