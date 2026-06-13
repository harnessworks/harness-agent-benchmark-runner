# Full Harness Decision And Failure Memory Experiment Plan

## Purpose

This experiment tests whether full-harness decision records and failure records
create measurable value for future coding-agent work.

The claim under test is intentionally narrow:

> Decision records and failure records are meaningful when they reduce repeated
> documented mistakes, improve record-consistent implementation choices, or make
> failures easier to classify beyond what workflow-only harness guidance already
> provides.

This is not a claim that the full harness generally improves raw coding ability
across arbitrary tasks. The current representative Flask benchmark already
shows that `memory-harness` did not beat `workflow-only` on correctness in the
stable-4 suite, so this experiment should isolate decision and failure memory
more directly instead of reusing that result as proof.

## Current Evidence Base

Existing evidence supports the need for a more targeted design:

- The stable-4 three-arm promotion showed strong safety and schema-contract
  measurement, but `memory-harness` tied `workflow-only` on correctness.
- The Flask `memory-harness` target contains generalized failure memory for
  response-key drift and metadata-envelope drift, but only one lightweight
  decision record. It is useful as a product-task probe, not a clean factorial
  test of decision memory versus failure memory.
- The `harness-starter-kit` target contains richer decision and failure-memory
  systems, including rules that failure records must cite detection or
  prevention checks.
- Older `harness-starter-kit` benchmark tasks already include
  `decision-memory-benchmark-ownership-adr` and
  `failure-memory-benchmark-noop-oracle-gap`, but those tasks mostly test
  whether agents can write new records. They do not prove that pre-existing
  records improve later work.

## Hypotheses

| ID | Hypothesis | Expected signal |
| --- | --- | --- |
| H0 | Decision and failure records add no measurable value beyond workflow guidance. | Full-harness, decision-only, and failure-only arms tie `workflow-only` within noise. |
| H1 | Decision records are meaningful. | Decision-bearing arms make more record-consistent structural choices than `workflow-only`. |
| H2 | Failure records are meaningful. | Failure-bearing arms repeat fewer documented mistakes than `workflow-only`. |
| H3 | Full harness has combined value. | Full-harness beats decision-only and failure-only on tasks requiring both a structural choice and prevention of a known mistake. |
| H4 | Full harness has operational cost. | Full-harness accuracy ties `workflow-only`, but duration tail or no-edit stalls increase because agents read more guidance. |

## Experiment Plan

### Arm Design

Use matched target repositories or pinned worktrees that differ only in the
presence of durable memory layers.

| Arm | Contents | Purpose |
| --- | --- | --- |
| `bare` | App code, tests, README-level basics only. | Negative baseline. |
| `workflow-only` | `AGENTS.md`, normal local gate, docs location rules, coding conventions. No decision or failure record content. | Controls for ordinary harness workflow. |
| `decision-only` | `workflow-only` plus `docs/decisions/**`; no `docs/failures/**` record content. | Isolates decision memory. |
| `failure-only` | `workflow-only` plus `docs/failures/**`; no project decision record content. | Isolates failure memory. |
| `full-harness` | `workflow-only` plus decision records and failure records. | Tests combined value and overhead. |

Keep the harness skeleton identical across memory arms. Directory READMEs,
templates, scripts, checks, and local gates should stay present unless their
absence is the explicit variable. For `decision-only` and `failure-only`, remove
or neutralize only the substantive record bodies that carry reusable memory.
This keeps the measured variable close to decision or failure memory instead of
accidentally measuring a broken docs layout or changed gate behavior.

If the five-arm setup is too expensive for the first pass, run the three-arm
pilot first:

| Pilot arm | Maps to |
| --- | --- |
| `workflow-only` | workflow guidance without durable memory |
| `failure-only` | workflow plus failure records |
| `full-harness` | workflow plus decision and failure records |

Do not collapse `failure-only` and `full-harness` unless the pilot question is
only "does any durable memory help?"

This three-arm pilot gives direct evidence for failure-memory value and combined
full-harness behavior. It gives only indirect evidence for decision-memory
value; direct H1 evidence requires the five-arm matrix with `decision-only`.

### Task Families

Use tasks where the prompt is realistic and omits the durable-memory rule being
tested. The hidden oracle should evaluate the behavior, not whether the agent
quotes a record.

| Family | Memory under test | Example task shape | Oracle dimensions |
| --- | --- | --- | --- |
| Decision-consistent boundary choice | Decision records | Add or update benchmark ownership behavior without putting target-specific oracle logic into the generic runner. | `functional`, `workflow`, `record_consistency` |
| Decision-consistent evidence choice | Decision records | Make a substantial harness-maintenance change and decide whether task-outcome evidence is required or should be explicitly skipped. | `workflow`, `record_consistency` |
| Failure-prevention check linkage | Failure records | Add a failure note or fix a repeated failure path; the solution must name or add a concrete detection/prevention check. | `functional`, `schema`, `mistake_prevention` |
| Oracle brittleness prevention | Failure records | Update a Markdown-oriented benchmark oracle so concept-equivalent wrapped prose passes and missing concepts fail. | `functional`, `mistake_prevention` |
| API response memory transfer | Failure records | Add a new public API endpoint where agents often drift on prompt-named JSON keys or `meta.service`. | `functional`, `schema`, `mistake_prevention` |
| Combined memory task | Decisions plus failures | Add a benchmark task update that must respect ownership boundaries and avoid the no-op-oracle gap. | `functional`, `workflow`, `record_consistency`, `mistake_prevention` |

Good task candidates from existing records:

- `docs/decisions/0004-link-failure-memory-to-regression-checks.md`
- `docs/decisions/0006-trigger-task-outcome-evidence-for-substantial-harness-work.md`
- `docs/failures/0005-failure-memory-was-not-linked-to-regression-checks.md`
- `docs/failures/0010-docs-only-benchmark-oracle-exact-string-drift.md`
- `docs/failures/0011-refresh-benchmark-oracle-line-wrap-drift.md`
- Flask memory records for response-key drift and metadata-envelope drift.

### Scoring

Every record should preserve the runner's existing dimensions:

- strict success
- functional success
- schema or structure success
- workflow success
- boundary success
- preflight and hidden-access results
- timeout and stall results
- agent duration distribution

Use two experiment-specific verification dimensions in task specs:

| Metric | Meaning |
| --- | --- |
| `record_consistency` | Verification command dimension for checking that the final change follows the relevant decision or failure-memory rule. The runner records this as `record_consistent_success`. |
| `mistake_prevention` | Verification command dimension for checking that the final change avoided a documented recurring mistake. The runner records this as `mistake_prevention_success`; a failed evaluated check is reported as `repeated_documented_mistake=true`. |

These dimensions are first-class runner/reporting fields. Public reports should
show both evaluated counts and successes, for example `record_consistency 3/4`
and `mistake_prevention 2/4`, plus the count of repeated documented mistakes.

Do not score "agent read the record" unless logs explicitly prove it. The
primary outcome is behavior.

### Run Shape

Prepared measurement pilot:

- 5 task families.
- 5 arms: `bare`, `workflow-only`, `decision-only`, `failure-only`,
  `full-harness`.
- 2 repeats.
- 50 planned records.
- `--jobs 1`.
- `--agent-timeout-override 900`.
- `--agent-idle-timeout 300`.
- `--agent-no-edit-timeout 360`.
- Do not use `--stop-on-abnormal` for the measurement pilot. Collect every
  planned record, then classify wrong-file edits, stalls, timeouts,
  hidden-access findings, and preflight failures. Any hidden-access or preflight
  leakage finding makes the pilot non-promotable, but it should not censor the
  rest of the exploratory matrix.

Recommended promotion if the pilot is clean:

- 6 task families.
- 5 arms.
- 4 repeats.
- 120 planned records.
- Sequential execution unless concurrency pressure is the explicit variable.
- `--stop-on-abnormal`, after a clean pilot covers every selected task/arm pair.

If cost or latency is a concern, prefer one repeat across the prepared task
families before shrinking the arm matrix. Do not promote a one-task result,
because it cannot distinguish record value from task-specific luck.

## Validity Assessment

### What The Experiment Can Prove

The experiment can support a narrow claim:

- decision records helped agents make a documented structural or workflow
  choice in this target and task family;
- failure records reduced recurrence of specific known mistakes in this target
  and task family;
- full-harness memory improved or worsened duration-tail behavior relative to
  workflow-only guidance.

### What It Cannot Prove

The experiment cannot prove:

- full harness improves arbitrary coding tasks;
- decision records are always worth writing;
- failure records replace regression tests;
- an agent used the record internally unless log evidence shows that;
- a target with more documentation is always better than a smaller harness.

### Main Threats To Validity

| Threat | Risk | Mitigation |
| --- | --- | --- |
| Guidance confounding | Full-harness arms may differ in more than decision/failure records. | Build target variants from one pinned ref and remove only the intended memory layer. |
| Answer leakage | Records might contain exact held-out route names or oracle payloads. | Preflight `leakage_audit` must block task-specific answers and hidden oracle strings. |
| Visible oracle contamination | Agents may read benchmark oracle code and bypass memory guidance. | Keep deterministic hidden oracles in this runner and hide target `benchmarks/` during agent execution when needed. |
| Documentation volume overhead | Full harness may slow agents because there is more to read. | Track duration p50, p95, max, no-edit stalls, and idle stalls separately from correctness. |
| Record-writing bias | Tasks that ask agents to create records overstate memory value. | Prefer tasks that require using existing records to avoid a known mistake. |
| Exact-string brittleness | Record-consistency oracles may punish acceptable wording. | Use normalized concept checks and negative fixtures, following existing failure-memory lessons. |
| Small sample variance | One or two tasks can produce misleading arm gaps. | Use at least four task families for a pilot and at least six for a promotion. |

## Feasibility Assessment

### What Exists Now

The current runner already supports most required mechanics:

- isolated clones under `runs/`;
- pinned `repo.ref` values;
- external hidden oracles;
- expected and forbidden file boundaries;
- verification dimensions;
- agent-excluded paths;
- idle and no-edit watchdogs;
- JSONL result collection;
- public-safe benchmark reports.

The target material also exists:

- `../flask-memory-harness` has generalized response-key and metadata-envelope
  failure records.
- `../harness-starter-kit` has a richer decision/failure memory system and
  benchmark tasks related to record creation.

### Pre-Execution Ready State

The first executable five-arm Flask pilot scaffold is prepared:

| Arm | Target | Ref |
| --- | --- | --- |
| `bare` | `../flask-no-harness` | `b5351eae78ed9f17d46a43eee05354e9e13f6b94` |
| `workflow-only` | `../flask-workflow-only` | `1a79d8cf9e0799789b3da8029dbbb5a572b3133e` |
| `decision-only` | `../flask-decision-only` | `95a843171d2183865c8698207b3b7d4075ba567b` |
| `failure-only` | `../flask-failure-only` | `18330ea23880b1ca7a647ea58b0d694e2c658fc8` |
| `full-harness` | `../flask-memory-harness` | `51700b72737a32fd9d96625a7547e28562865c57` |

Prepared runner artifacts:

- suite: `benchmarks/suites/flask-full-harness-memory-pilot.json`;
- task specs: `benchmarks/tasks/flask-full-harness-memory-pilot/*.json`;
- task matrix: five held-out Flask endpoint tasks across five arms;
- planned measurement run: two repeats, 50 records, `--jobs 1`, without
  `--stop-on-abnormal`;
- first-class result fields: `record_consistent_success`,
  `mistake_prevention_success`, and `repeated_documented_mistake`;
- direct H1 task: `hidden-effect-catalog-price-policy`, whose prompt omits the
  price-band labels and thresholds while decision-bearing arms carry the
  tracked catalog price-band decision record;
- hidden schema oracles tagged with `mistake_prevention` because the visible
  failure records target prompt-named response-key drift and `meta.service`
  envelope drift.

Post-run H1 oracle triage:

- The first 1x pilot exposed a brittle `catalog-price-policy` summary check:
  `summary.price_bands` was rejected even though the prompt only required a
  compact summary with counts by price band.
- The oracle now accepts direct or nested price-band count objects and keeps
  the stricter requirement that all three adopted band labels are counted.
- The `record_consistency` check now adds a hidden 37.00 price edge case, so
  the adopted 35.00 premium threshold is measured directly rather than inferred
  from the current catalog rows.
- Replaying saved H1 worktrees under the revised oracle classifies
  `decision-only` as record-consistent, keeps `workflow-only` and
  `failure-only` negative because they lack the decision record, and keeps
  `full-harness` negative because it used a 40.00 threshold.
- The decision-bearing target refs now also surface a narrow discoverability
  rule: when a prompt refers to an adopted or repository policy that is not
  fully specified, agents should search `docs/decisions/` by prompt domain
  terms and apply the accepted decision without editing decision records.

Pre-execution checks completed:

- each non-bare target variant passes `python3 scripts/check_harness.py`;
- the pilot suite dry-runs to 50 planned runs;
- the task matrix has 25 specs, with five specs per arm and five arm variants
  per task family;
- `python3 -m unittest discover -s tests` passes in the runner.

Scope of this ready pilot: it directly measures failure-memory transfer through
`mistake_prevention` and direct decision-memory behavior through
`record_consistency`. The H1 signal is intentionally narrow: whether agents use
the pre-existing catalog price-band decision without modifying decision
records.

### Remaining Gaps Before Promotion

| Gap | Impact | Practical fix |
| --- | --- | --- |
| H1 coverage is narrow. | The current pilot directly tests one catalog policy decision, not every structural decision-memory family. | Add at least one harness-structure `record_consistency` task before making a broad decision-memory claim. |
| Public summary script is still Flask-shaped. | Reports can group custom arms and memory metrics, but table naming remains Flask benchmark oriented. | Use it for the pilot, then add a neutral memory-experiment summary wrapper before promotion if the result becomes representative. |
| Live Codex runs cost time and budget. | Promotion run may be expensive. | Start with the prepared 50-record pilot and promote only if operationally clean. |

Feasibility verdict: the first five-arm pilot is ready to execute with both
`mistake_prevention` and `record_consistency` metrics. A clean factorial
promotion still needs broader H1 task coverage before making a broad
decision-memory claim.

## Direction Review

Recommended direction:

1. Execute the prepared five-arm pilot before spending effort on a promotion
   matrix.
2. Prefer failure-memory tasks first. They have clearer behavioral oracles:
   "did the known mistake recur?"
3. Add decision-memory tasks second. Their oracles need careful concept checks
   so they measure structural choice rather than preferred prose.
4. Promote only after the pilot has no abnormal signals: no hidden-access
   findings, no wrong-file edits, no forbidden-file edits, no stalls, and no
   unexplained timeouts.

If the pilot produces a positive result, the first meaningful product claim
should be phrased conservatively:

> In record-sensitive held-out Flask API tasks, failure memory reduced specific
> repeated response-contract mistakes relative to workflow-only harness
> guidance, while preserving the runner's safety and boundary guarantees.

If the pilot ties `workflow-only`, the result is still useful. It would mean
the current records are not yet carrying measurable extra behavior, and the
next step should be to improve record quality, task selection, or the agent's
record-discovery path instead of promoting full-harness memory as a proven
accuracy lift.

## Minimum Next Implementation Steps

1. Rerun a small multi-repeat H1/H2 pilot under the revised price-policy
   oracle before promoting the 50-record plan.
2. Classify every abnormal result after the run: hidden access, wrong-file
   edits, forbidden-file edits, preflight failures, stalls, and timeouts.
3. Summarize public-safe pilot evidence under `docs/benchmarks/`.
4. Add another harness-structure `record_consistency` task before claiming
   broad decision-memory value or promoting to the 120-record factorial run.
5. Keep `docs/benchmarks/latest.md` unchanged unless the pilot becomes the most
   recent representative report.
