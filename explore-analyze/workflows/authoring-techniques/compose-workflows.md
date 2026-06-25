---
navigation_title: Compose workflows
applies_to:
  stack: preview 9.4+
  serverless: preview
description: Decompose long workflows into reusable child workflows. Design the input and output contract, test children in isolation, and fan out with asynchronous composition.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Compose workflows from reusable parts [workflows-compose-workflows]

Composition lets one workflow call another. Done well, it turns a sprawling multi-purpose workflow into a small, testable parent that delegates to focused children. This page covers the authoring decisions: when to extract a child workflow, how to design its input and output contract, how to test it in isolation, and how to fan out to background jobs.

:::{warning}
Composition steps (`workflow.execute`, `workflow.executeAsync`, `workflow.output`, `workflow.fail`) are in technical preview. Use them for prototypes and reusable utility workflows. Hold off on critical paths until composition reaches GA.
:::

For the step parameter reference, refer to [Composition steps](/explore-analyze/workflows/steps/composition.md).

## When to extract a child workflow [workflows-compose-when]

Reach for composition when you notice any of the following:

| Signal | What to extract |
|---|---|
| You're copying the same five to ten steps across several workflows. | A shared child that owns the repeated sequence. |
| A workflow has grown long enough that you can't test it end to end. | Split it along a natural boundary (enrichment, notification, remediation). |
| Different teams own different parts of a process. | Give each team their own child workflow with a documented contract. |
| You need to fan out to N background jobs. | An asynchronous child invoked with `workflow.executeAsync`. |
| A step sequence is easier to reason about in isolation. | Extract it so you can read, test, and change it on its own. |

If a workflow is short, used once, and clear end to end, don't extract. Composition introduces a contract you have to maintain.

## Design the input and output contract [workflows-compose-contract]

A child workflow is a unit of code with a public interface. Treat it like one.

### Declare inputs and outputs at the top

Use the `inputs` and `outputs` fields to spell out the contract. The engine validates inputs at invocation and outputs at `workflow.output` time, so callers can rely on shape without guarding against missing keys.

The location of `inputs` in the YAML depends on your version. On stack 9.4 and earlier, `inputs` sits at the top level of the workflow. On stack 9.5+ and on serverless, `inputs` sits inside the `manual` trigger. Refer to [Workflow anatomy](/explore-analyze/workflows/authoring-techniques/anatomy.md#workflows-anatomy-inputs) for the full reference.

::::{applies-switch}

:::{applies-item} stack: preview 9.3, ga 9.4
```yaml
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
:::

:::{applies-item} { stack: ga 9.5+, serverless: ga }
```yaml
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
:::

::::

### Keep the shape small

A child with a dozen inputs and a deeply nested output is hard to call. When you notice the contract growing, ask whether the child is doing too much. Most shared children work best with one or two inputs (an object bag if you have several related fields) and two or three outputs.

### Name children so they're discoverable

A common convention: platform teams name shared workflows with a `shared--<verb>-<noun>` prefix (for example, `shared--enrich-alerts`, `shared--open-case`, `shared--notify-team`). Product teams then compose from those shared children into their own domain workflows. The prefix makes the shared library easy to scan in the **Workflows** list.

## Test children in isolation [workflows-compose-test]

Give every child a `manual` trigger so you can test it on its own. This is one of the main operational wins of composition: you can exercise a single piece of your automation without running the parent.

1. Open the child workflow in the [YAML editor](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md).
2. Use the **Run** action and provide the inputs that a parent would normally pass.
3. Verify the outputs match the declared schema. Mismatches are caught by the engine, so a failing schema validation points directly at a broken child.

Parents invoke children through `workflow.execute`, but triggers and invocation live independently. A child workflow is still a normal workflow: anything that can call it (another workflow, the UI, an API client) works the same way.

## Choose synchronous or asynchronous composition [workflows-compose-sync-async]

| Use | When |
|---|---|
| [`workflow.execute`](/explore-analyze/workflows/steps/composition.md#workflow-execute) (synchronous) | The parent needs the child's result before it can continue. For example, enrich and then decide. |
| [`workflow.executeAsync`](/explore-analyze/workflows/steps/composition.md#workflow-executeasync) (asynchronous) | Fire and forget. Notifications, logging, and fan-out to background workers. |

Asynchronous composition is the primary fan-out primitive in workflows. Each call spawns an independent execution with its own execution log, retry policy, and observability. This is cleaner than any intra-execution concurrency construct and lets each background job fail or succeed without affecting its siblings.

### Fan out with `foreach` plus `workflow.executeAsync`

The canonical fan-out pattern is a `foreach` over a list of work items, each one invoking an asynchronous child:

```yaml
- name: fan_out_hosts
  type: foreach
  foreach: "${{ steps.find_hosts.output.hits.hits }}"
  steps:
    - name: spawn_handler
      type: workflow.executeAsync
      with:
        workflow-id: "shared--handle-host"
        inputs:
          host_id: "{{ foreach.item._source.host.id }}"
          correlation_id: "{{ execution.id }}"
```

The parent finishes quickly. The N child executions continue in the background. Pass `execution.id` (or a similar correlation token) as an input so you can link parent and child executions in your observability tooling.

## Guard against recursion [workflows-compose-recursion]

The execution engine enforces a maximum composition depth to prevent infinite recursion. A workflow cannot call itself directly, and a deep chain of parent-child-grandchild calls stops at the depth limit with a clear error.

If you need to guard against your own recursion (for example, a handler that could trigger itself again), read `execution.compositionDepth` inside the child and short-circuit when it exceeds what your design expects:

```yaml
- name: stop_if_nested
  type: if
  condition: "execution.compositionDepth > 2"
  steps:
    - name: abort
      type: workflow.fail
      with:
        message: "Nested too deep. Intended max depth is 2."
        reason: "max_depth_exceeded"
```

## Version and deprecate shared children [workflows-compose-versioning]

When a shared child changes shape (new required input, renamed output, breaking behavior), the safest path is to publish a new name rather than mutate the existing one.

- Keep `shared--enrich-alerts` stable for callers that depend on the current contract.
- Ship `shared--enrich-alerts-v2` with the new shape.
- Migrate callers one at a time and retire v1 when all are moved.

This discipline pays off quickly once more than one team depends on a shared workflow.

## Related pages [workflows-compose-related]

- [Composition steps reference](/explore-analyze/workflows/steps/composition.md): Parameter shapes for `workflow.execute`, `workflow.executeAsync`, `workflow.output`, and `workflow.fail`.
- [Anatomy of a workflow](/explore-analyze/workflows/authoring-techniques/anatomy.md#workflows-anatomy-outputs): Background on the `outputs` field required for child workflows.
- [Use the YAML editor](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md): How test runs work when you're iterating on a child workflow.
- [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md): `on-failure` interacts with `workflow.fail` in predictable ways.
- [Foreach step](/explore-analyze/workflows/steps/foreach.md): Pair with `workflow.executeAsync` for the fan-out pattern.
