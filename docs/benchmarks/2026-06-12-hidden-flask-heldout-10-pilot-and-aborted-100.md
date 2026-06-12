# Hidden Flask Heldout 10-Run Pilot And Aborted 100-Run - 2026-06-12

## Summary

After splitting heldout scoring into `functional` and `schema` dimensions, a
10-record pilot completed cleanly. Based on that pilot, a 100-record sequential
run was started. It was stopped after 14 complete records because two early
bare-arm agent timeouts made the run unsuitable as product-value evidence.

This report is diagnostic. Do not promote it to `latest.md` or README headline
evidence.

## 10-Run Pilot

- Suite: `benchmarks/suites/flask-hidden-heldout-10.json`
- Shape: 5 tasks x 2 arms x 1 repeat = 10 records
- Workspace: `runs/hidden-flask-heldout-10-20260612T1001Z`
- Results: `results/hidden-flask-heldout-10-20260612T1001Z`
- Concurrency: `jobs=1`
- Timeout cap: task timeout, 600 seconds

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Timeouts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 5 | 1 | 2 | 4 | 5 | 5 | 0 |
| `workflow-only` | 5 | 2 | 3 | 4 | 5 | 5 | 0 |

The pilot had no preflight failures, wrong-file edits, forbidden-file edits, or
timeouts. The scoring split worked as intended: several records passed schema
and workflow while failing functional behavior, and `catalog-segments` exposed
functional/schema separation in the other direction.

## Aborted 100-Run

- Suite: `benchmarks/suites/flask-hidden-heldout-10.json`
- Planned shape: 5 tasks x 2 arms x 10 repeats = 100 records
- Completed records before stop: 14
- Workspace: `runs/hidden-flask-heldout-100-20260612T1025Z`
- Results: `results/hidden-flask-heldout-100-20260612T1025Z`
- Stop reason: two early bare-arm agent timeouts in 14 records

| Target | Runs | Strict successes | Functional | Schema contract | Workflow | Boundary | Timeouts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bare` | 7 | 0 | 0 | 4 | 5 | 7 | 2 |
| `workflow-only` | 7 | 4 | 5 | 5 | 7 | 7 | 0 |

The stopped run still showed a workflow-only advantage in the completed records,
but the timeout pattern appeared too early to treat the partial 100-record run
as representative product evidence.

## Interpretation

The 10-run pilot was clean enough to justify starting the 100-run. The 100-run
itself was not clean enough to finish unchanged. Two bare-arm timeouts in the
first 14 completed records indicate either model/service tail latency or task
prompt/agent behavior that can consume the full 600-second task timeout.

The next run should either:

- keep `jobs=1` and raise the task timeout cap deliberately, reporting timeout
  stability as a measured condition; or
- keep the 600-second cap and reduce task ambiguity or agent looping before
  another 100-record attempt.

Do not compare this partial 100-run against prior representative runs as if it
were complete.
