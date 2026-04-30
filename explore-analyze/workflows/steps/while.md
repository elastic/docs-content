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

## Parameters

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `name` | top level | string | Yes | Unique step identifier. |
| `type` | top level | string | Yes | Must be `while`. |
| `condition` | top level | string | Yes | KQL expression evaluated each iteration. The loop continues while it is true. |
| `steps` | top level | array | Yes | Loop body. |
| `max-iterations` | top level | number or object | No | Limit for number of iterations. Bare number is treated as `{ limit: N, on-limit: continue }`. Use the object form to opt into `on-limit: fail`. |
| `iteration-timeout` | top level | duration | No | Per-iteration timeout. |
| `iteration-on-failure` | top level | object | No | Per-iteration error-handling policy. Same shape as `on-failure`. |

:::{warning}
`while` has no default `max-iterations`. Without an explicit cap, a `while` loop runs as long as its condition holds. Always set `max-iterations` on loops that depend on external state to avoid runaway executions.
:::

### `max-iterations` shape

```yaml
# Bare number: default `on-limit` is `continue` (the step succeeds when the cap is hit)
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
  condition: "steps.check.output.status : pending"
  max-iterations:
    limit: 60
    on-limit: fail
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
