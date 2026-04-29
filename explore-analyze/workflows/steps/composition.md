---
navigation_title: Composition
applies_to:
  stack: preview 9.4+
  serverless: preview
description: Invoke child workflows with typed inputs and outputs. Use composition to build reusable workflow building blocks and fan out to background jobs.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Composition steps [workflows-composition-steps]

Composition steps let one workflow invoke another. Use them to build reusable workflow building blocks, break long workflows into testable pieces, and fan out to background jobs.

:::{warning}
Composition steps (`workflow.execute`, `workflow.executeAsync`, `workflow.output`, `workflow.fail`) are in technical preview in 9.4. The parameter shapes can change in future releases. Use for prototypes and reusable utility workflows; hold off on critical paths until composition reaches GA.
:::

## When to use composition

| Problem | Why composition helps |
|---|---|
| You're copying the same steps across many workflows. | Extract them into a shared child workflow and call it. |
| A long workflow is hard to test end to end. | Break it into smaller pieces and test each one in isolation. |
| You need to fan out to N background jobs. | Use `workflow.executeAsync` to fire and forget. |
| Different teams own different parts of a process. | Each team maintains their own child workflow. |

## Shape of a composed workflow

A parent calls a child with [`workflow.execute`](#workflow-execute) (synchronous) or [`workflow.executeAsync`](#workflow-executeasync) (fire-and-forget). The child is a normal workflow with two additions:

1. It **declares its outputs** in the top-level `outputs` field so callers know what to expect.
2. It **emits outputs** with [`workflow.output`](#workflow-output), or terminates with [`workflow.fail`](#workflow-fail) on error.

The engine validates child outputs against the declared schema before returning them to the caller, so the parent can reference `{{ steps.<child>.output.<field> }}` without guarding against missing keys.

## Synchronous or asynchronous composition

| Use | When |
|---|---|
| [`workflow.execute`](#workflow-execute) (synchronous) | The parent needs the child's result to continue. |
| [`workflow.executeAsync`](#workflow-executeasync) (asynchronous) | Fire and forget. Notifications, logging, fan-out to background workers. |

## Composition depth limit

The execution engine enforces a maximum composition depth to prevent infinite recursion. If a child tries to invoke a grandchild that would exceed the limit, the step fails at the depth check. A workflow also cannot call itself directly.

---

## `workflow.execute` [workflow-execute]

Run a child workflow synchronously. The parent waits for the child to finish and receives its validated outputs.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `workflow-id` | `with` | string | Yes | Name of the child workflow to run. Use the child's `name` field, not an internal saved-object ID. |
| `inputs` | `with` | object | No | Typed inputs passed to the child. Must match the child's `inputs` declaration. |

```yaml
- name: enrich_alerts
  type: workflow.execute
  with:
    workflow-id: "shared--enrich-alerts"
    inputs:
      alerts: "${{ event.alerts }}"

- name: use_enrichment
  type: cases.createCase
  with:
    title: "Threat: {{ steps.enrich_alerts.output.enrichment_stats.top_indicator }}"
```

:::{important}
Both `workflow-id` and `inputs` live **inside the `with` block**. `workflow-id` is the only kebab-case parameter in workflows that sits inside `with` rather than at the step top level.
:::

## `workflow.executeAsync` [workflow-executeasync]

Start a child workflow without blocking. Fire and forget. Use for fan-out patterns where the parent doesn't need the child's result.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `workflow-id` | `with` | string | Yes | Name of the child workflow to run. |
| `inputs` | `with` | object | No | Typed inputs passed to the child. |

```yaml
- name: notify_async
  type: workflow.executeAsync
  with:
    workflow-id: "shared--post-to-slack"
    inputs:
      message: "Processing started"
      channel: "#soc-oncall"
```

The parent continues immediately. The child runs on its own, and its success or failure is independent of the parent.

## `workflow.output` [workflow-output]

Emit the final outputs of a workflow. Outputs are validated against the workflow's declared `outputs` schema. An optional top-level `status` field controls the execution's terminal state.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `status` | top level | string | No | `completed` (default), `cancelled`, or `failed`. |
| output values | `with` | object | Yes | Output values that match the declared output schema. |

```yaml
outputs:
  - name: enriched_documents
    type: object
  - name: enrichment_stats
    type: object

steps:
  # ...enrichment logic...

  - name: return_result
    type: workflow.output
    with:
      enriched_documents: "${{ steps.enrich.output }}"
      enrichment_stats: "${{ steps.stats.output }}"
```

`workflow.output` is terminal. Once it runs, the workflow reports its outputs to the caller and exits.

## `workflow.fail` [workflow-fail]

Stop the workflow with a `failed` terminal state. Useful for short-circuiting when input validation fails or a required condition is not met.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `message` | `with` | string | No | Human-readable failure message. |
| `reason` | `with` | string | No | Machine-readable failure code. |

```yaml
- name: abort
  type: workflow.fail
  if: "not steps.validate.output.ok"
  with:
    message: "Required input missing"
    reason: "missing_input"
```

If the workflow was invoked by a parent through `workflow.execute`, the parent receives the error on `steps.<child>.error`.

## Shared a workflow library across teams

A common pattern: a platform team maintains a set of `shared--<verb>-<noun>` workflows, each with a clean manual trigger and a documented input and output schema. Product teams then compose those shared workflows into their own domain-specific automation.

```yaml
# Platform team's shared workflow
name: shared--enrich-alerts
description: Enrich alerts with threat intel and geo data.
triggers:
  - type: manual

inputs:
  - name: alerts
    type: object
    required: true

outputs:
  - name: enriched_alerts
    type: object
  - name: enrichment_stats
    type: object

steps:
  # ...enrichment logic...

  - name: return_result
    type: workflow.output
    with:
      enriched_alerts: "${{ steps.enrich.output }}"
      enrichment_stats: "${{ steps.stats.output }}"
```

```yaml
# Security team's workflow that composes it
name: security--triage-with-enrichment
triggers:
  - type: alert

steps:
  - name: enrich
    type: workflow.execute
    with:
      workflow-id: "shared--enrich-alerts"
      inputs:
        alerts: "${{ event.alerts }}"

  - name: open_case
    type: cases.createCase
    with:
      title: "Threat: {{ steps.enrich.output.enrichment_stats.top_indicator }}"
```

## Related

- [Workflow authoring techniques](/explore-analyze/workflows/authoring-techniques.md): How to structure a workflow for composition.
- [Triggers overview](/explore-analyze/workflows/triggers.md): Composed workflows typically use `manual` triggers so they can be tested in isolation.
- [Flow control steps](/explore-analyze/workflows/steps/flow-control-steps.md): For fan-out across independent executions, combine `foreach` with `workflow.executeAsync`.
