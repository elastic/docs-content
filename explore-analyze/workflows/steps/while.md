---
navigation_title: While
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Reference for the while step, which loops while a KQL condition evaluates to true.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# While [workflows-while-step]

The `while` step runs its nested steps repeatedly as long as a {{kib}} Query Language (KQL) condition evaluates to true. The condition is re-evaluated at the end of every iteration.

Use `while` for polling patterns: checking a status until it reaches `ready`, retrying an operation until it succeeds, or waiting for an external job to complete. For iterating over a known collection, use [`foreach`](/explore-analyze/workflows/steps/foreach.md) instead.

:::{include} ../_snippets/schema-location-legend.md
:::

## Parameters

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `name` | top level | string | Yes | Unique step identifier. |
| `type` | top level | string | Yes | Must be `while`. |
| `condition` | top level | string | Yes | KQL expression evaluated each iteration. The loop continues while it is true. |
| `steps` | top level | array | Yes | Loop body. |
| `if` | top level | string | No | KQL expression that skips the entire loop when it evaluates to false. |
| `max-iterations` | top level | number or object | No | Limit for number of iterations. Default is **2000**. Bare number is treated as `{ limit: N, on-limit: continue }`. Use the object form to opt into `on-limit: fail`. |
| `timeout` | top level | duration | No | Timeout for the entire loop. |
| `on-failure` | top level | object | No | Loop-level error-handling policy. Supports the same `continue`, `retry`, and `fallback` options as other steps. |
| `iteration-timeout` | top level | duration | No | Per-iteration timeout. |
| `iteration-on-failure` | top level | object | No | Per-iteration error-handling policy. Supports `continue`, `retry`, and `fallback` without failing the whole loop. |

:::{warning}
`while` defaults to `max-iterations: 2000` with `on-limit: continue`, which means the step **succeeds quietly when the cap is reached**. If your loop needs to fail the workflow on hitting the cap, set `on-limit: fail` explicitly. Always think about the cap on loops that depend on external state to avoid runaway executions or silently truncated work.
:::

## Guardrails

Use loop-level guardrails to control the `while` step as a whole:

* `max-iterations` caps the number of iterations to prevent runaway loops.
* `timeout` limits the total time spent in the loop, across all iterations.
* `on-failure` defines loop-level failure handling with the same `continue`, `retry`, and `fallback` options used by other steps.
* `if` skips the entire loop when the condition evaluates to false.

Use iteration-level guardrails to control each pass through the loop:

* `iteration-timeout` limits how long one iteration can run.
* `iteration-on-failure` handles failures for one iteration with `continue`, `retry`, or `fallback` without failing the whole loop.

### `max-iterations` shape

```yaml
# Bare number: default `on-limit` is `continue` (the step succeeds when the limit is reached)
max-iterations: 60

# Object form: opt into `on-limit: fail` to fail the workflow when the limit is reached
max-iterations:
  limit: 60
  on-limit: fail
```

## Loop-local context

Inside the `steps` block of a `while`, the following variables are available:

| Variable | Contains |
|---|---|
| `while.iteration` | Zero-based iteration counter. |

## Example: Poll until a job finishes

```yaml
- name: poll_job
  type: while
  if: "inputs.poll : true"
  condition: "steps.check.output.status : pending"
  max-iterations:
    limit: 60
    on-limit: fail
  timeout: "10m"
  iteration-timeout: "30s"
  iteration-on-failure:
    retry:
      max-attempts: 2
      delay: "1s"
  steps:
    - name: check
      type: elasticsearch.search
      with:
        index: "jobs"
        query:
          term:
            id: "{{ inputs.job_id }}"
        size: 1

    - name: log_progress
      type: console
      with:
        message: "Attempt {{ while.iteration }}: status {{ steps.check.output.hits.hits[0]._source.status }}"

    - name: wait
      type: wait
      with:
        duration: "5s"
```

If the job hasn't left `pending` after 60 iterations (five minutes), the loop exits with failure.

## Related

- [Flow control steps](/explore-analyze/workflows/steps/flow-control-steps.md): Overview of all flow-control types.
- [Foreach step](/explore-analyze/workflows/steps/foreach.md): For iterating over a known array.
- [Loop break](/explore-analyze/workflows/steps/loop-break.md) and [Loop continue](/explore-analyze/workflows/steps/loop-continue.md): Control loop flow from inside the body.
