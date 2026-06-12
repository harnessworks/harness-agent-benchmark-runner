<img width="2172" height="724" alt="harness_runner" src="https://github.com/user-attachments/assets/edf405d3-33fc-483b-a5c1-1730f430812f" />

# Harness Agent Benchmark Runner

Benchmark infrastructure for measuring coding-agent behavior against
deterministic repository tasks. The runner isolates each attempt under `runs/`,
records append-only JSONL evidence under `results/`, and publishes only
credential-safe summaries in `docs/benchmarks/`.

This README is the short evidence front page. Operational details live in task
specs, runner code, and detailed benchmark reports.

## Benchmark Status

Current official evidence is still the balanced hidden-oracle Flask A/B 100-run
`jobs=2` evidence run, but it should now be read as a full-contract control.
Both targets received the task-critical API contract in the prompt, while only
the harnessed target retained repository-local workflow, documentation,
boundary, and local-gate guidance.

Detailed report:
[`docs/benchmarks/2026-06-12-hidden-flask-balanced-ab-100-jobs2.md`](docs/benchmarks/2026-06-12-hidden-flask-balanced-ab-100-jobs2.md).

Latest heldout mitigation diagnostic:
[`docs/benchmarks/2026-06-12-hidden-flask-heldout-promptguard-aborted-100.md`](docs/benchmarks/2026-06-12-hidden-flask-heldout-promptguard-aborted-100.md).
After hidden-path, adapter-isolation, target-clean, and `_band`/`_bands`
API-style fixes, a prompt-guarded fresh 10-record pilot completed with zero
stalls, timeouts, hidden access, or boundary issues. The follow-up 100-record
attempt still stopped at record 14 on bare `bundle-quote` when the 330-second
pilot watchdog fired. That stopped record had active edits, so the current
watchdog is too strict for 100-record promotion as a wall-clock cap. It is not
official product evidence.

This is representative for the explicitly measured `jobs=2` run shape. It is
not a pure sequential claim: the run produced timeout noise, so strict scored
success and verification passed should be read separately.

The next product-value experiment should use a fixed three-arm structure:
`bare`, `workflow-only`, and `memory-harness`. The main product experiment is
`partial-realistic` held-out work where task-specific answer strings are absent
from the target repositories. `full-contract` prompts remain useful controls;
small gaps there are expected because the prompt already supplies much of the
answer.

## Current Evidence

| Target | Harness | Runs | Strict successes | Verification passed | Non-timeout oracle failures | Timeouts | Boundary issues |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `flask-no-harness` | No | 50 | 46 | 46 | 3 | 1 | 0 |
| `flask-yes-harness` | Yes | 50 | 48 | 49 | 0 | 2 | 0 |

Boundary issues combine wrong-file edits and forbidden-file edits. Both were 0
on both sides in the 100-run jobs=2 evidence run.

Guardrail detail:

| Target | Wrong-file edits | Forbidden-file edits | Timeouts |
| --- | ---: | ---: | ---: |
| `flask-no-harness` | 0 | 0 | 1 |
| `flask-yes-harness` | 0 | 0 | 2 |

The no-harness target reached 46/50 strict successes after endpoint, method,
request shape, response keys, constants, status codes, and business rules were
moved into the prompt. The yes-harness target reached 48/50. Verification
passed was 46/50 vs 49/50, showing a small residual harness lift under equal
prompt-level contract disclosure. Timeout behavior moved against the harnessed
target under `jobs=2`, so timeout stability remains unresolved.

## What This Shows

The balanced pilot no longer measures whether the agent can guess a hidden API
contract from repository conventions. It measures whether repository harnessing
improves completion after the basic contract is shared:

| Dimension | Observed signal |
| --- | --- |
| Functional implementation | no-harness had 2 reservation-preview summary misses; yes-harness had no non-timeout functional oracle misses. |
| Companion documentation | no-harness had 1 catalog-metrics docs concept miss; yes-harness had none. |
| File-boundary discipline | both targets had 0 wrong-file edits and 0 forbidden-file edits. |
| Timeout stability | jobs=2 produced 1 no-harness timeout and 2 yes-harness timeouts, so this run does not show a harness timeout advantage. |
| Local workflow use | yes-harness also ran its local harness gate before the hidden oracle. |

This is a narrower and more defensible claim than the earlier hidden-contract
calibration: the harness appears to produce a small residual verification-rate
lift under the measured Flask API task shape. It is not a generic claim about
all coding tasks or all repositories.

It is also not a clean `memory-harness` product claim. A valid product claim
needs the three arms separated so `workflow-only` cannot be confused with
generalized memory, and so task-specific hidden answers cannot leak into target
docs or failure memory.

## Why Use The Harness

The harness is useful when agent success depends on more than writing code that
passes obvious local tests. It gives the repository a durable way to teach and
enforce local expectations without putting every convention into every prompt.

| Harness advantage | Practical effect | Evidence in latest run |
| --- | --- | --- |
| Repository-local guidance | Agents can find project conventions, docs locations, and completion gates inside the target repository. | yes-harness completed 48/50 strict successes and 49/50 verification passes; no-harness completed 46/50 on both measures. |
| Better companion docs discipline | Agents are steered toward the documented docs location and expected terminology. | no-harness had 1 catalog-metrics docs concept miss in the 100-run jobs=2 evidence run; yes-harness had none. |
| Local gate before hidden scoring | The harnessed target can run repository-specific checks before the external hidden oracle. | yes-harness ran `scripts/check_harness.py` before hidden oracle checks. |
| Boundary reinforcement | The target can state what files are in scope and what files are off-limits. | Both targets had 0 wrong-file edits in the latest 100-run jobs=2 evidence run; earlier hidden-oracle runs showed boundary drift when prompt wording was weaker. |
| Less prompt burden over time | Stable conventions live in the repo instead of being repeated in every benchmark prompt. | The balanced prompt exposed the API contract; harness guidance still carried workflow, docs, and gate behavior. |

The current evidence does not prove that a harness always improves raw coding
ability. It shows a more specific and useful thing: under convention-heavy
repository tasks, the harness can reduce missed local expectations and make
successful agent work more repeatable.

## Evidence Trail

| Scope | Agent | Mode | Runs | Strict successes | Verification passed | Timeouts | Boundary issues |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `flask-yes-harness` balanced hidden-oracle A/B | Codex CLI | 100-run jobs=2 | 50 | 48 | 49 | 2 | 0 |
| `flask-no-harness` balanced hidden-oracle A/B | Codex CLI | 100-run jobs=2 | 50 | 46 | 46 | 1 | 0 |
| `flask-yes-harness` balanced hidden-oracle A/B | Codex CLI | 20-run pilot, run-time oracle | 10 | 10 | 10 | 0 | 0 |
| `flask-no-harness` balanced hidden-oracle A/B | Codex CLI | 20-run pilot, run-time oracle | 10 | 6 | 6 | 0 | 0 |

Older `harness-starter-kit` runs remain useful agent-adapter evidence, but the
Flask A/B rows are the relevant harness-effect evidence.

```mermaid
xychart-beta
    title "Flask A/B Strict Success Rates"
    x-axis ["100 jobs2 no", "100 jobs2 yes", "20 pilot no runtime", "20 pilot no rescore", "20 pilot yes"]
    y-axis "Success %" 0 --> 100
    bar [92, 96, 60, 90, 100]
```

## Metric Definitions

- `Functional success`: hidden-oracle behavior for commands tagged
  `functional`.
- `Schema contract success`: response envelope, key, metadata, and API-style
  checks for commands tagged `schema`.
- `Workflow success`: agent exit, diff check, local workflow/gate commands
  tagged `workflow`, and file-boundary checks.
- `Strict scored success`: final scored success after preflight, agent exit,
  diff check, verification, and file-boundary checks. A passing test suite alone is not
  counted as full success if file boundaries are violated.
- `Verification passed`: deterministic pytest plus hidden-oracle success before
  any file-boundary penalty.
- `Functional oracle failures`: hidden-oracle failures in endpoint behavior,
  response shape, calculations, status codes, mutation behavior, or edge cases.
- `Docs oracle failures`: hidden-oracle failures in required companion
  documentation content or placement.
- `Wrong-file edits`: changed files outside the task's expected file boundary.
  In these Flask runs, root `README.md` is outside the allowed companion-docs
  path (`docs/**`) unless the task explicitly asks for README changes. A
  README edit here is not a functional failure by itself and is not a general
  claim that README edits are bad; it is a strict boundary miss.
- `Forbidden-file edits`: changed files matching explicitly forbidden patterns.
- `Timeouts`: agent process failed to exit before the effective task timeout.
- `Stalls`: agent process was stopped by either the shorter pilot watchdog
  (`--agent-stall-timeout`) or the idle-output watchdog
  (`--agent-idle-timeout`). Count this separately from product-quality oracle
  failures.
- `Preflight failures`: leakage audit failures before agent execution. These
  should fail the run without spending model budget.

## What Comes Next

The next useful follow-up is not another identical `jobs=2` run. Build a
three-arm held-out suite with `bare`, `workflow-only`, and `memory-harness`,
then run `partial-realistic` prompts as the main product experiment and
`full-contract` prompts as controls. Keep functional, schema-contract,
workflow, boundary, strict success, and timeout counts separate in the report.
For held-out pilots, use `--agent-stall-timeout` so stalled records are written
to JSONL instead of requiring manual process termination. For 100-record
promotion, prefer `--agent-idle-timeout` or the task timeout so long-but-active
runs are not stopped by a short wall-clock pilot cap.
Keep adapter hygiene enabled during promotion checks:
`CODEX_IGNORE_USER_CONFIG=1`, `CODEX_IGNORE_RULES=1`, and
`CODEX_DISABLE_PLUGINS=1`.

To separate task quality from scheduler pressure, either rerun representative
shapes sequentially or rerun `jobs=2` with an explicitly higher timeout cap.
Timeout stability remains unresolved until a sequential follow-up rules out
parallel scheduler pressure.

## Reports

- [`docs/benchmarks/2026-06-12-hidden-flask-heldout-promptguard-aborted-100.md`](docs/benchmarks/2026-06-12-hidden-flask-heldout-promptguard-aborted-100.md)
- [`docs/benchmarks/2026-06-12-hidden-flask-heldout-memoryhide-aborted-pilot.md`](docs/benchmarks/2026-06-12-hidden-flask-heldout-memoryhide-aborted-pilot.md)
- [`docs/benchmarks/2026-06-12-hidden-flask-balanced-ab-100-jobs2.md`](docs/benchmarks/2026-06-12-hidden-flask-balanced-ab-100-jobs2.md)
- [`docs/benchmarks/2026-06-12-hidden-flask-balanced-ab-20-jobs2-calibration.md`](docs/benchmarks/2026-06-12-hidden-flask-balanced-ab-20-jobs2-calibration.md)
- [`docs/benchmarks/2026-06-12-hidden-flask-balanced-ab-20-pilot.md`](docs/benchmarks/2026-06-12-hidden-flask-balanced-ab-20-pilot.md)
- [`docs/benchmarks/2026-06-12-hidden-flask-ab-calibration-1x.md`](docs/benchmarks/2026-06-12-hidden-flask-ab-calibration-1x.md)
- [`docs/benchmarks/2026-06-12-hidden-flask-ab-partial-calibration-35.md`](docs/benchmarks/2026-06-12-hidden-flask-ab-partial-calibration-35.md)
- [`docs/benchmarks/2026-06-11-hidden-oracle-harness-effect-ab-3x.md`](docs/benchmarks/2026-06-11-hidden-oracle-harness-effect-ab-3x.md)
- [`docs/benchmarks/2026-06-11-complex-harness-effect-ab-3x.md`](docs/benchmarks/2026-06-11-complex-harness-effect-ab-3x.md)
- [`docs/benchmarks/2026-06-11-harness-effect-ab-3x.md`](docs/benchmarks/2026-06-11-harness-effect-ab-3x.md)
- [`docs/benchmarks/latest.md`](docs/benchmarks/latest.md)

Raw `runs/`, `results/`, local logs, cloned repositories, and credentials are
intentionally not committed. Public reports summarize reproducible,
credential-safe fields from local records.
