---
navigation_title: Event-driven triggers
applies_to:
  stack: preview 9.4+
  serverless: preview
description: Run a workflow in response to a platform event. In 9.4, the workflows.failed trigger fires when another workflow execution fails.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Event-driven triggers [workflows-event-driven-triggers]

Event-driven triggers let workflows react to events elsewhere in {{kib}}. In 9.4, the only event-driven trigger is `workflows.failed`, which fires when another workflow's execution fails. More event-driven triggers are planned for subsequent releases.

:::{warning}
The event-driven trigger system, including the `workflows.failed` trigger, is in technical preview. The schema and semantics can change in future releases.
:::

## `workflows.failed`

Fires when any workflow execution reaches the `failed` terminal state. Use this trigger to build handler workflows that react to failures in your production workflows, for example by paging on-call, opening a case, or logging to a dedicated index for observability.

### Schema

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `type` | top level | string | Yes | Must be `workflows.failed`. |
| `condition` | `on` | KQL string | No | Optional KQL predicate evaluated against the `event` payload. The trigger fires only when the condition matches. |

```yaml
triggers:
  - type: workflows.failed
```

### Filter the events that fire the trigger

Use `on.condition` to narrow which failed executions trigger the handler. The value is a KQL predicate evaluated against the `event` payload.

Fire only on failures from a specific workflow:

```yaml
triggers:
  - type: workflows.failed
    on:
      condition: "event.workflow.name : 'ops--rollback-deployment'"
```

Ignore failures that came from another error handler:

```yaml
triggers:
  - type: workflows.failed
    on:
      condition: "event.workflow.isErrorHandler : false"
```

Combine conditions with KQL's `and` to filter on multiple fields:

```yaml
triggers:
  - type: workflows.failed
    on:
      condition: "event.workflow.isErrorHandler : false and event.workflow.spaceId : 'production'"
```

### Event payload

When a failed workflow triggers your handler, the handler runs with an `event` context that describes the failure. The payload has four groups: `workflow`, `execution`, `error`, and the top-level `timestamp` and `spaceId`.

| Field | Contains |
|---|---|
| `event.spaceId` | The {{kib}} space where the failure occurred. |
| `event.timestamp` | ISO timestamp of when the event fired. |
| `event.workflow.id` | The failed workflow's ID. |
| `event.workflow.name` | The failed workflow's name. |
| `event.workflow.spaceId` | The {{kib}} space where the failed workflow ran. |
| `event.workflow.isErrorHandler` | `true` if the failed workflow was itself an error handler. Use this to prevent cascading handler loops. |
| `event.execution.id` | The failed execution's ID. |
| `event.execution.startedAt` | ISO timestamp of when the execution started. |
| `event.execution.failedAt` | ISO timestamp of when the execution failed. |
| `event.error.message` | The error message. |
| `event.error.stepId` | Identifier of the step where the failure occurred, when available. |
| `event.error.stepName` | Name of the step where the failure occurred, when available. |
| `event.error.stepExecutionId` | ID of the step execution where the failure occurred, when available. |

Reference these fields with Liquid templating inside the handler:

```yaml
- name: log_failure
  type: console
  with:
    message: |
      Workflow {{ event.workflow.name }} (id: {{ event.workflow.id }}) failed
      at step {{ event.error.stepName }}: {{ event.error.message }}
```

## Example: Page on-call when a critical workflow fails

```yaml
name: handle-critical-workflow-failures
description: Page on-call and open a case whenever a critical workflow fails.
enabled: true

triggers:
  - type: workflows.failed

steps:
  - name: skip_if_handler
    type: if
    condition: "event.workflow.isErrorHandler : true"
    steps:
      - name: no_op
        type: console
        with:
          message: "Skipping: the failure came from another error handler."

  - name: page_oncall
    if: "not event.workflow.isErrorHandler"
    type: pagerduty.triggerIncident
    connector-id: "platform-pagerduty"
    with:
      dedup_key: "{{ event.workflow.id }}-{{ event.execution.id }}"
      summary: "Workflow {{ event.workflow.name }} failed"
      severity: "critical"
      details:
        failed_step: "{{ event.error.stepName }}"
        error: "{{ event.error.message }}"
        workflow_id: "{{ event.workflow.id }}"
        execution_id: "{{ event.execution.id }}"

  - name: open_case
    if: "not event.workflow.isErrorHandler"
    type: cases.createCase
    with:
      title: "[Auto] Workflow failure: {{ event.workflow.name }}"
      description: |
        Step `{{ event.error.stepName }}` failed.

        Error: `{{ event.error.message }}`
      severity: "high"
      tags: ["workflow-failure", "auto-triage"]
```

## Prevent cascading handler loops

If a handler workflow itself fails, it can re-trigger itself. Two safeguards help you avoid infinite loops:

- Every event includes `event.workflow.isErrorHandler`, which is `true` when the failing workflow is itself a handler. Filter on this in your handler's logic to skip handling your own failures.
- The execution engine enforces a chain-depth limit on cascading event-driven triggers as a safety net.

In practice, keep handler workflows simpler than the workflows they monitor. A handler that only logs, opens a case, and notifies is less likely to fail than the automation it's handling.

## Related

- [Triggers overview](/explore-analyze/workflows/triggers.md): Every 9.4 trigger type.
- [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md): Per-step `on-failure` strategies complement event-driven handlers.
- [Cases steps](/explore-analyze/workflows/steps/cases.md): Open cases from your handler.
