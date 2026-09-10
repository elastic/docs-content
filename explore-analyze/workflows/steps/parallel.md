---
navigation_title: Parallel
applies_to:
  stack: preview 9.5+
  serverless: preview
description: Reference for the parallel step, which runs branches concurrently and collects a per-branch result. Covers dynamic fan-out over a list and a fixed set of named branches.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Parallel [workflows-parallel-step]

The `parallel` step runs several branches at the same time and continues when every branch reaches a terminal state. Use it for independent work that would otherwise run one item at a time: enriching an indicator from three services at once, or calling the same API for each item in a list.

The step always produces a per-branch result plus aggregate counts, so a later step can inspect what succeeded and what failed.

The step has two modes, and each step must use exactly one of them.

| Mode | Use it when | Configure |
|---|---|---|
| Dynamic fan-out | The work is the same for every item, and you only know the number of items at runtime. | `foreach` and `steps` |
| Static branches | The work differs per branch and you know the set of branches when you author the workflow. | `branches` |

:::{include} ../_snippets/schema-location-legend.md
:::

## Parameters [workflows-parallel-parameters]

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `name` | top level | string | Yes | Unique step identifier. |
| `type` | top level | string | Yes | Must be `parallel`. |
| `foreach` | top level | string or array | Yes, for dynamic fan-out | Liquid expression that evaluates to an array, or a literal array. The `steps` body runs once per item. Mutually exclusive with `branches`. |
| `steps` | top level | array | Yes, for dynamic fan-out | Branch body that runs once per item. Use only with `foreach`. |
| `branches` | top level | array | Yes, for static branches | Fixed set of named branches, each with its own `name` and `steps`. Requires at least two branches. Mutually exclusive with `foreach` and `steps`. |
| `concurrency` | top level | number or object | No | How many branches run at once. Bare number is shorthand for `{ max: N }`. Defaults to `{ max: 5, count-waiting: true }`. `max` can't exceed `20`. |
| `mode` | top level | string | No | Failure policy: `fail-fast` (default) or `settled`. Refer to [Handle branch failures](#workflows-parallel-failures). |
| `branch-timeout` | top level | duration | No | Maximum time a single branch may run. No default. |
| `timeout` | top level | duration | No | Maximum time the whole step may run, across all branches. No default. |

Each entry in `branches` takes the following fields:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Branch identifier, up to 256 characters. Used as the branch's `key` in the step output, so it must be unique within the step. |
| `steps` | array | Yes | Branch body. Refer to [Branch body limitations](#workflows-parallel-branch-limits). |

## Dynamic fan-out [workflows-parallel-dynamic]

Set `foreach` to the list and put the shared work in `steps`. The engine creates one branch per item and runs up to `concurrency.max` of them at a time.

```yaml
- name: enrich_indicators
  type: parallel
  foreach: "${{ steps.get_indicators.output.hits.hits }}"
  concurrency:
    max: 5
  branch-timeout: "30s"
  steps:
    - name: lookup_reputation
      type: http
      with:
        url: "https://api.example.com/reputation/{{ foreach.item._source.indicator }}"
```

Inside a branch, the current item is available as `foreach.item`, its zero-based position as `foreach.index`, the item count as `foreach.total`, and the full list as `foreach.items`, exactly as in a [`foreach`](/explore-analyze/workflows/steps/foreach.md) loop.

A dynamic step can fan out over at most 100 items. A longer list fails the step when it starts. If `foreach` resolves to an empty array, the step completes immediately with `total: 0` and an empty `results` array, and the workflow continues.

:::{tip}
The YAML editor warns when a dynamic `parallel` step has no `concurrency` setting, because a large runtime list can spike resource usage. Set an explicit `max` rather than relying on the default.
:::

`foreach` must resolve to the same array throughout the step's execution. Reading it from `consts` or from a step output that no longer changes keeps the branch-to-item correlation stable.

## Static branches [workflows-parallel-static]

List each branch under `branches` with its own `name` and `steps`. Every branch runs a different body, and the set is fixed when you save the workflow.

```yaml
- name: enrich_file
  type: parallel
  mode: settled
  branch-timeout: "45s"
  branches:
    - name: reputation
      steps:
        - name: check_reputation
          type: http
          with:
            url: "https://api.example.com/hash/{{ inputs.file_hash }}"
    - name: geoip
      steps:
        - name: geo_lookup
          type: http
          with:
            url: "https://api.example.com/ip/{{ inputs.source_ip }}"
    - name: internal_sightings
      steps:
        - name: search_sightings
          type: elasticsearch.search
          with:
            index: "logs-*"
            query:
              term:
                file.hash.sha256: "{{ inputs.file_hash }}"
```

Static branches don't get a `foreach` context. Each branch reads the shared workflow context directly, so `inputs.*`, `consts.*`, `event.*`, and the outputs of steps that ran before the `parallel` step all resolve as usual.

Steps inside a branch keep their normal identifiers, so a later step can read one branch's output directly, for example `{{ steps.geo_lookup.output.body.country }}`.

Branch names must be unique within the step, because each name is used as that branch's key in the output. A static step needs at least two branches: for a single branch, use a plain step sequence instead.

`concurrency` still applies to static branches. With five branches and `concurrency: 2`, the step runs two at a time.

## Read the results [workflows-parallel-output]

The step's output holds one entry per branch in `results`, index-aligned with the branches, plus aggregate counts:

```json
{
  "results": [
    {
      "index": 0,
      "key": "reputation",
      "status": "completed",
      "startedAt": 1718900000000,
      "finishedAt": 1718900001432,
      "durationMs": 1432,
      "output": {}
    }
  ],
  "total": 3,
  "succeeded": 2,
  "failed": 1,
  "status": "failed"
}
```

| Field | Description |
|---|---|
| `results[].index` | Zero-based branch position. Always present. |
| `results[].key` | For static branches, the branch `name`. For dynamic fan-out, the full item value captured when the step started (can be a string or an object). |
| `results[].status` | `completed`, `failed`, `timed_out`, or `skipped`. |
| `results[].output` | Output of the last step the branch ran. Present for completed branches. |
| `results[].error` | Error details for failed and timed-out branches. |
| `results[].startedAt`, `results[].finishedAt`, `results[].durationMs` | Branch timing. `startedAt` is present once the branch starts; `durationMs` is present once it finishes. |
| `total`, `succeeded`, `failed` | Branch counts. Timed-out branches count as failed. |
| `status` | `failed` if any branch failed or timed out, otherwise `completed`. |
| `branches` | Static branches only. Results keyed by branch name, each with `status`, `output`, and `error`. |

For static branches, read a result by name instead of by position:

```yaml
- name: summarize
  type: console
  with:
    message: "Reputation: {{ steps.enrich_file.output.branches.reputation.status }}, geo: {{ steps.enrich_file.output.branches.geoip.status }}"
```

A branch that never started, because `fail-fast` short-circuited it, has `status: skipped` and carries no output or error.

## Handle branch failures [workflows-parallel-failures]

The `mode` parameter decides what a failed branch does to the step:

* `fail-fast` (default): the engine stops starting new branches, lets branches already in flight finish, marks the branches that never started as `skipped`, and then **fails the step**. The aggregate output is still written, so the failed step's `results` remain readable.
* `settled`: every branch runs to a terminal state and the **step completes**, even when some branches failed. Check `output.failed` or the individual `results[].status` values downstream to decide what to do.

Use `settled` for best-effort enrichment where partial results are useful, and `fail-fast` when any failure should stop the workflow.

:::{note}
`fail-fast` doesn't cancel branches that are already running. It only stops the step from starting more branches.
:::

The `parallel` step doesn't accept `on-failure` or `if` as top-level parameters. To keep the workflow running when a branch fails, set `mode: settled` and branch on the results in a following step:

```yaml
- name: handle_partial_failure
  type: if
  condition: "steps.enrich_file.output.failed > 0"
  steps:
    - name: log_gaps
      type: console
      with:
        message: "{{ steps.enrich_file.output.failed }} of {{ steps.enrich_file.output.total }} branches failed."
```

## Timeouts [workflows-parallel-timeouts]

* `branch-timeout` bounds each branch independently. A branch that exceeds it is marked `timed_out` and counted as failed.
* `timeout` bounds the whole step. When it elapses, branches still in flight are marked `timed_out` and the step finishes with whatever results exist.
* When you set both, each branch stops at whichever deadline comes first.

Cancellation is best effort. The engine signals the running step to stop, but a step that ignores that signal can keep working in the background after its branch is marked `timed_out`.

## Concurrency and waiting branches [workflows-parallel-concurrency]

A branch occupies a slot from the moment it starts until it reaches a terminal state. `concurrency.count-waiting` controls whether a branch that's parked in a `wait` step keeps its slot:

* `true` (default): a waiting branch keeps its slot, so the total number of branches in flight never exceeds `max`.
* `false`: a branch parked in a wait frees its slot so another branch can start. Branches doing active work still count against `max`.

Set `count-waiting: false` when branches spend most of their time waiting, so sleeping branches don't hold up the rest.

```yaml
- name: poll_jobs
  type: parallel
  foreach: "${{ consts.job_ids }}"
  concurrency:
    max: 4
    count-waiting: false
  steps:
    - name: check_job
      type: http
      with:
        url: "https://api.example.com/jobs/{{ foreach.item }}"
    - name: settle
      type: wait
      with:
        duration: "5s"
```

## Branch body limitations [workflows-parallel-branch-limits]

A branch body must be a straight-line sequence of steps. The following are rejected when you save the workflow, with an error on the offending step:

| Not supported in a branch | Use instead |
|---|---|
| Nested flow control: `if`, `switch`, `foreach`, `while` | Put the branching logic in a step before or after the `parallel` step, or move the branch body into a child workflow and call it with [`workflow.execute`](/explore-analyze/workflows/steps/composition.md#workflow-execute). |
| Human-in-the-loop waits: `waitForInput`, `waitForApproval` | Pause before or after the `parallel` step. |
| Step-level `on-failure` inside a branch | `mode: settled` to collect every branch's outcome, then handle failures in a step after the `parallel` step. |
| Step-level `timeout` inside a branch | `branch-timeout` on the `parallel` step. |

Timer-based `wait` steps are supported inside a branch.

## Example: Fan out enrichment, then act on the results [workflows-parallel-example]

This example enriches an alert from three sources at once, keeps going when one source fails, and comments on a case with what came back.

```yaml
- name: enrich_alert
  type: parallel
  mode: settled
  branch-timeout: "30s"
  timeout: "2m"
  branches:
    - name: reputation
      steps:
        - name: check_reputation
          type: http
          with:
            url: "https://api.example.com/hash/{{ event.alerts[0].file.hash.sha256 }}"
    - name: sightings
      steps:
        - name: search_sightings
          type: elasticsearch.search
          with:
            index: "logs-*"
            size: 5
            query:
              term:
                file.hash.sha256: "{{ event.alerts[0].file.hash.sha256 }}"
    - name: asset_context
      steps:
        - name: get_host
          type: elasticsearch.search
          with:
            index: "metrics-*"
            size: 1
            query:
              term:
                host.name: "{{ event.alerts[0].host.name }}"

- name: record_enrichment
  type: cases.addComment
  with:
    case_id: "{{ steps.create_case.output.case.id }}"
    comment: "Enrichment finished: {{ steps.enrich_alert.output.succeeded }} of {{ steps.enrich_alert.output.total }} sources returned data. Reputation: {{ steps.enrich_alert.output.branches.reputation.status }}."
```

## Related [workflows-parallel-related]

- [Flow control steps](/explore-analyze/workflows/steps/flow-control-steps.md): Overview of every flow-control step type.
- [Foreach step](/explore-analyze/workflows/steps/foreach.md): Iterate over an array one item at a time.
- [Composition steps](/explore-analyze/workflows/steps/composition.md): Run child workflows, including fan-out to independent executions.
- [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md): `on-failure` strategies and data flow between steps.
