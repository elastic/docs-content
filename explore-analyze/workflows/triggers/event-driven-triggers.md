---
navigation_title: Event-driven triggers
applies_to:
  stack: ga 9.5+, preview =9.4
  serverless: ga
description: Run a workflow in response to a platform event, such as a workflow failure, a case change, an entity store change, or an alert lifecycle event.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Event-driven triggers [workflows-event-driven-triggers]

Event-driven triggers let workflows react to events elsewhere in {{kib}}. The following trigger families are available:

- **`workflows.failed`** — Fires when another workflow's execution fails. {applies_to}`stack: ga 9.5+, preview =9.4` {applies_to}`serverless: ga`
- **Cases triggers** — Fire when cases change (created, updated, status changed, attachments added, comments added). {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview`
- **Entity store triggers** — Fire when an entity's asset criticality or risk score changes in the entity store. {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview`
- **Alert episode lifecycle triggers** — Fire on specific alert episode events in the {{alerting-v2-system}}, such as when it is activated, assigned, acknowledged, or snoozed. {applies_to}`stack: experimental 9.5+` {applies_to}`serverless: experimental`
- **{{alerting-v2-system-cap}} rule lifecycle triggers** — Fire when rules are created, updated, deleted, enabled, or disabled in the {{alerting-v2-system}}. {applies_to}`stack: experimental 9.5+` {applies_to}`serverless: experimental`

:::{note}
The event-driven trigger framework is generally available. Individual trigger families can have a different maturity: check the availability badge in each section. The schema and semantics of triggers still in technical preview can change in future releases.
:::

:::{include} ../_snippets/schema-location-legend.md
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

## Cases triggers

```{applies_to}
stack: preview 9.5+
serverless: preview
```

Cases triggers fire when cases change. Use them to react to case lifecycle events without polling the Cases API.

**Shared payload.** Every cases trigger event includes:

- `event.caseId` — The case ID, the alphanumeric identifier that is unique to each case.
- `event.owner` — The solution that owns the case. It can be `securitySolution` for {{elastic-sec}} cases, `observability` for {{observability}} cases, or `cases` for Stack cases.

Use `event.owner` in `on.condition` to filter by solution. For example, a workflow that only fires for {{elastic-sec}} cases:

```yaml
triggers:
  - type: cases.caseCreated
    on:
      condition: 'event.owner: "securitySolution"'
```

Individual trigger sections below document any additional payload fields specific to that event.

### `cases.caseCreated` [cases-casecreated-trigger]

Fires when a case is created.

#### Schema

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `type` | top level | string | Yes | Must be `cases.caseCreated`. |
| `condition` | `on` | KQL string | No | Optional KQL predicate evaluated against the `event` payload. |

#### Event payload

| Field | Contains |
|---|---|
| `event.caseId` | The new case's ID. |
| `event.owner` | The case owner (`securitySolution`, `observability`, or `cases`). |

#### Example

Fire only for {{elastic-sec}} cases:

```yaml
triggers:
  - type: cases.caseCreated
    on:
      condition: 'event.owner: "securitySolution"'
```

### `cases.caseUpdated` [cases-caseupdated-trigger]

Fires when a case is updated. The `event.updatedFields` array lists which fields changed.

This trigger also fires when a case's status changes; the dedicated [`cases.caseStatusUpdated`](#cases-casestatusupdated-trigger) trigger fires alongside it and carries the previous status for easier filtering. For bulk updates, `cases.caseUpdated` fires once per case.

#### Schema

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `type` | top level | string | Yes | Must be `cases.caseUpdated`. |
| `condition` | `on` | KQL string | No | Optional KQL predicate evaluated against the `event` payload. |

#### Event payload

| Field | Contains |
|---|---|
| `event.caseId` | The updated case's ID. |
| `event.owner` | The case owner (`securitySolution`, `observability`, or `cases`). |
| `event.updatedFields` | Array of field names that changed in this update. |

#### Example

Fire when a {{elastic-sec}} case's title changes:

```yaml
triggers:
  - type: cases.caseUpdated
    on:
      condition: 'event.owner: "securitySolution" and event.updatedFields: "title"'
```

### `cases.caseStatusUpdated` [cases-casestatusupdated-trigger]

Fires when a case's status changes.

#### Schema

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `type` | top level | string | Yes | Must be `cases.caseStatusUpdated`. |
| `condition` | `on` | KQL string | No | Optional KQL predicate evaluated against the `event` payload. |

#### Event payload

| Field | Contains |
|---|---|
| `event.caseId` | The case ID. |
| `event.owner` | The case owner (`securitySolution`, `observability`, or `cases`). |
| `event.previousStatus` | The previous status (`open`, `in-progress`, or `closed`). |
| `event.status` | The current status (`open`, `in-progress`, or `closed`). |

#### Example

Fire when a {{elastic-sec}} case is closed:

```yaml
triggers:
  - type: cases.caseStatusUpdated
    on:
      condition: 'event.owner: "securitySolution" and event.status: "closed"'
```

### `cases.attachmentsAdded` [cases-attachmentsadded-trigger]

Fires when attachments are added to a case. If attachments of multiple types are added in one operation (for example, three alerts and two comments), the trigger fires once per type, with one event for each type.

Adding a comment fires both this trigger (with `event.attachmentType: "comment"`) and the dedicated [`cases.commentsAdded`](#cases-commentsadded-trigger) trigger. Both exist because users don't always think of comments as attachments.

#### Schema

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `type` | top level | string | Yes | Must be `cases.attachmentsAdded`. |
| `condition` | `on` | KQL string | No | Optional KQL predicate evaluated against the `event` payload. |

#### Event payload

| Field | Contains |
|---|---|
| `event.caseId` | The case ID. |
| `event.owner` | The case owner (`securitySolution`, `observability`, or `cases`). |
| `event.attachmentIds` | Array of attachment IDs added in this operation, all of `event.attachmentType`. |
| `event.attachmentType` | The type of attachments added, for example `"comment"` or `"alert"`. |

#### Examples

Fire only for {{elastic-sec}} cases:

```yaml
triggers:
  - type: cases.attachmentsAdded
    on:
      condition: 'event.owner: "securitySolution"'
```

Fire only when a comment-type attachment is added:

```yaml
triggers:
  - type: cases.attachmentsAdded
    on:
      condition: 'event.attachmentType: "comment"'
```

### `cases.commentsAdded` [cases-commentsadded-trigger]

Fires when comments are added to a case.

#### Schema

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `type` | top level | string | Yes | Must be `cases.commentsAdded`. |
| `condition` | `on` | KQL string | No | Optional KQL predicate evaluated against the `event` payload. |

#### Event payload

| Field | Contains |
|---|---|
| `event.caseId` | The case ID. |
| `event.owner` | The case owner (`securitySolution`, `observability`, or `cases`). |
| `event.commentIds` | Array of comment IDs added in this operation. |

#### Example

Fire only for {{elastic-sec}} cases:

```yaml
triggers:
  - type: cases.commentsAdded
    on:
      condition: 'event.owner: "securitySolution"'
```

## Entity store triggers [entity-store-triggers-event-driven]

```{applies_to}
stack: preview 9.5+
serverless: preview
```

Entity store triggers fire when an entity in the [entity store](/solutions/security/advanced-entity-analytics/entity-store.md) changes. Use them to react to changes in an entity's asset criticality or risk score without polling.

**Shared payload.** Every entity store trigger event includes:

- `event.entityId` — The unique identifier (EUID) of the entity that changed.
- `event.entityType` — The type of entity: `host`, `user`, or `service`.

Individual trigger sections below document the additional payload fields specific to that event.

### `entityStore.entityAssetCriticalityUpdated` [entitystore-assetcriticalityupdated-trigger]

Fires when an entity's asset criticality level is assigned or cleared.

#### Schema

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `type` | top level | string | Yes | Must be `entityStore.entityAssetCriticalityUpdated`. |
| `condition` | `on` | KQL string | No | Optional KQL predicate evaluated against the `event` payload. |

#### Event payload

| Field | Contains |
|---|---|
| `event.entityId` | The unique identifier (EUID) of the entity whose asset criticality changed. |
| `event.entityType` | The entity type (`host`, `user`, or `service`). |
| `event.criticalityLevel` | The new asset criticality level (`low_impact`, `medium_impact`, `high_impact`, or `extreme_impact`), or `null` when criticality is cleared. |

#### Examples

Fire when an entity is assigned high or extreme impact:

```yaml
triggers:
  - type: entityStore.entityAssetCriticalityUpdated
    on:
      condition: 'event.criticalityLevel: "high_impact" OR event.criticalityLevel: "extreme_impact"'
```

Fire only when a host entity's criticality changes:

```yaml
triggers:
  - type: entityStore.entityAssetCriticalityUpdated
    on:
      condition: 'event.entityType: "host"'
```

Fire when criticality is removed from an entity:

```yaml
triggers:
  - type: entityStore.entityAssetCriticalityUpdated
    on:
      condition: 'NOT event.criticalityLevel: *'
```

### `entityStore.entityRiskScoreChanged` [entitystore-riskscorechanged-trigger]

Fires when an entity's risk score changes.

#### Schema

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `type` | top level | string | Yes | Must be `entityStore.entityRiskScoreChanged`. |
| `condition` | `on` | KQL string | No | Optional KQL predicate evaluated against the `event` payload. |

#### Event payload

| Field | Contains |
|---|---|
| `event.entityId` | The unique identifier (EUID) of the entity whose risk score changed. |
| `event.entityType` | The entity type (`host`, `user`, or `service`). |
| `event.score` | The risk score after the update (0–100). |
| `event.previousScore` | The risk score before the update, or `null` when this is the first score assignment. |
| `event.delta` | The absolute magnitude of the change in risk score. Use `event.direction` to distinguish an increase from a decrease. `null` when the previous score is unavailable. |
| `event.direction` | Whether the risk score increased or decreased (`increase` or `decrease`). `null` when the previous score is unavailable. |

#### Examples

Fire when a risk score increases by 25 or more:

```yaml
triggers:
  - type: entityStore.entityRiskScoreChanged
    on:
      condition: 'event.direction: "increase" AND event.delta >= 25'
```

Fire when a risk score decreases:

```yaml
triggers:
  - type: entityStore.entityRiskScoreChanged
    on:
      condition: 'event.direction: "decrease"'
```

Fire when a risk score crosses a high-risk threshold:

```yaml
triggers:
  - type: entityStore.entityRiskScoreChanged
    on:
      condition: 'event.score >= 70'
```

## {{alerting-v2-system-cap}} alert episode lifecycle triggers [alert-episode-lifecycle-triggers-event-driven]

```{applies_to}
stack: experimental 9.5+
serverless: experimental
```

:::{note}
These triggers are available only when the {{alerting-v2-system}} is enabled. If it isn't enabled, they don't appear in the trigger picker.
:::

Alert episode lifecycle triggers fire on specific alert episode events in the {{alerting-v2-system}}. Unlike `workflows.failed` and cases triggers, they are not configured through a `triggers` block in your workflow YAML. They are emitted by the alerting system and automatically invoke any workflow attached to the matching trigger type. Each trigger fires exactly once per event. There is no polling interval or frequency gate.

### Available triggers [alert-episode-lifecycle-triggers-available]

| Trigger ID | When it fires |
|---|---|
| `alerting.episodeActivated` | An alert episode transitions to the active state. |
| `alerting.episodeDeactivated` | An alert episode is manually deactivated or recovers. |
| `alerting.episodeSnoozed` | An alert episode is snoozed. |
| `alerting.episodeUnsnoozed` | An alert episode is unsnoozed. |
| `alerting.episodeAcked` | An alert episode is acknowledged. |
| `alerting.episodeUnacked` | An alert episode acknowledgment is removed. |
| `alerting.episodeAssigned` | An alert episode is assigned to a user. |
| `alerting.episodeUnassigned` | An alert episode assignment is removed. |
| `alerting.episodeTagged` | A tag is applied to an alert episode. |

### Event payload [alert-episode-lifecycle-triggers-event]

All lifecycle triggers include these common fields in the event payload.

| `event.*` field | Contains |
|---|---|
| `event.episodeId` | Unique identifier of the alert episode. |
| `event.ruleId` | ID of the rule that produced the alert episode. |
| `event.spaceId` | ID of the {{kib}} space where the event occurred. |

Reference these fields with Liquid templating in workflow steps:

```yaml
- name: log
  type: console
  with:
    message: |
      Episode {{ event.episodeId }} from rule {{ event.ruleId }} changed state.
```

Use these fields to write workflow conditions that scope the automation to specific rules or episodes. For example, use `event.ruleId: "my-rule-id"` to scope the workflow to alert episodes from a specific rule.

## {{alerting-v2-system-cap}} rule lifecycle triggers [alerting-rule-lifecycle-triggers-event-driven]

```{applies_to}
stack: experimental 9.5+
serverless: experimental
```

:::{note}
These triggers are available only when the {{alerting-v2-system}} is enabled. If it isn't enabled, they don't appear in the trigger picker.
:::

{{alerting-v2-system-cap}} rule lifecycle triggers fire when rules are created, updated, deleted, enabled, or disabled in the {{alerting-v2-system}}. Use them to automate responses to rule management actions, for example, auditing rule changes, syncing rule inventory with an external CMDB, or notifying a team channel when a new rule is added to a space.

Rule lifecycle triggers are part of the {{alerting-v2-system}} and fire independently of alert episodes.

### Available triggers [alerting-rule-lifecycle-triggers-available]

| Trigger ID | When it fires |
|---|---|
| `alerting.ruleCreated` | A rule is created. |
| `alerting.ruleUpdated` | A rule's configuration is changed using a `PATCH` or `PUT` update. Enabling or disabling a rule through the dedicated enable or disable action does not emit this trigger. It emits `alerting.ruleEnabled` or `alerting.ruleDisabled` instead. |
| `alerting.ruleDeleted` | A rule is deleted. |
| `alerting.ruleEnabled` | A rule is enabled. |
| `alerting.ruleDisabled` | A rule is disabled. |

For bulk operations (bulk enable, bulk disable, bulk delete), one trigger event is emitted for each affected rule.

### Schema [alerting-rule-lifecycle-triggers-schema]

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `type` | top level | string | Yes | One of: `alerting.ruleCreated`, `alerting.ruleUpdated`, `alerting.ruleDeleted`, `alerting.ruleEnabled`, `alerting.ruleDisabled`. |
| `condition` | `on` | KQL string | No | Optional KQL predicate evaluated against the `event` payload. The trigger fires only when the condition matches. |

```yaml
triggers:
  - type: alerting.ruleCreated
  - type: alerting.ruleUpdated
  - type: alerting.ruleDeleted
  - type: alerting.ruleEnabled
  - type: alerting.ruleDisabled
```

### Event payload [alerting-rule-lifecycle-triggers-event]

All rule lifecycle triggers share the same minimal payload.

| `event.*` field | Contains |
|---|---|
| `event.rule.ruleId` | Unique identifier of the rule that was created, updated, deleted, enabled, or disabled. |
| `event.rule.spaceId` | ID of the {{kib}} space where the operation occurred. |

Reference these fields with Liquid templating in workflow steps:

```yaml
- name: log_rule_event
  type: console
  with:
    message: |
      Rule {{ event.rule.ruleId }} changed in space {{ event.rule.spaceId }}.
```

Use `on.condition` to scope the trigger to a specific rule or space:

```yaml
triggers:
  - type: alerting.ruleCreated
    on:
      condition: 'event.rule.spaceId: "production"'
```

### Example: Audit rule changes [alerting-rule-lifecycle-triggers-example]

```yaml
name: audit-rule-changes
description: Log rule lifecycle events across all spaces.
enabled: true

triggers:
  - type: alerting.ruleCreated
  - type: alerting.ruleUpdated
  - type: alerting.ruleDeleted
  - type: alerting.ruleEnabled
  - type: alerting.ruleDisabled

steps:
  - name: log_change
    type: console
    with:
      message: |
        Rule {{ event.rule.ruleId }} in space {{ event.rule.spaceId }} — trigger: {{ trigger.type }}
```

## Control event chains and prevent loops

When a workflow's own steps cause an event that its trigger listens for, executions can chain together (workflow A emits an event, which runs workflow B, which emits an event that runs A again). Left unchecked, these chains can loop or generate load. Event-driven triggers give you controls to manage this, with safe defaults.

### Filter workflow-generated events [event-driven-triggers-workflow-events]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

Use `on.workflowEvents` on any event-driven trigger to control whether events that originated from a workflow run can fire this trigger:

| Value | Behavior |
|---|---|
| `avoid-loop` | Default, applied when `workflowEvents` is omitted or set to an unrecognized value. The trigger fires on workflow-generated events, but a cycle guard skips scheduling when this workflow is already part of the current event chain. This blocks same-workflow loops while still allowing linear chains. |
| `ignore` | The trigger does not fire on workflow-generated events. Events that originate from a user action or a domain change (not attributed to a workflow) still fire the trigger. Use this to react only to external signals. |
| `allow-all` | The trigger fires even when this workflow is already in the event chain, bypassing the cycle guard. Use this only when repeated same-workflow runs are intentional. The maximum chain depth still applies as a backstop. |

```yaml
triggers:
  - type: cases.caseUpdated
    on:
      # React only to case updates made by people, not updates made by workflows
      workflowEvents: ignore
```

Regardless of the value, the execution engine enforces a maximum event-chain depth as a final safety net against runaway chains.

### Prevent `workflows.failed` handler loops [event-driven-triggers-handler-loops]

If a `workflows.failed` handler fails, it can trigger itself. In addition to the controls above, every failure event includes `event.workflow.isErrorHandler`, which is `true` when the failed workflow was itself a handler. Filter on this field to skip handling your own failures:

```yaml
triggers:
  - type: workflows.failed
    on:
      condition: "event.workflow.isErrorHandler : false"
```

In practice, keep handler workflows simpler than the workflows they monitor. A handler that only logs, opens a case, and notifies is less likely to fail than the automation it's handling.

## Test a workflow with a real event [event-driven-triggers-test]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

You can test an event-driven workflow against a real event before enabling it. When you run a workflow from the editor, the **Run workflow** dialog shows a trigger tab for each way to supply input, including an **Event** tab for event-driven triggers.

On the **Event** tab, browse events that have already occurred for your trigger type. Use the KQL search bar and time range to narrow the list, select an event from the results, and run the workflow against that event's payload. The execution then runs exactly as it would have when the event first occurred, so you can confirm your conditions and steps behave as expected.

:::{tip}
To reuse the input from an earlier run instead of a fresh event, use the **Historical** tab, which lets you rerun a workflow with the input data from a previous execution.
:::

## Related

- [Triggers overview](/explore-analyze/workflows/triggers.md): All trigger types.
- [Workflow authorization](/explore-analyze/workflows/authorization.md): Whose privileges event-driven workflows run with.
- [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md): Per-step `on-failure` strategies complement event-driven handlers.
- [Monitor workflow execution](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md): See what triggered each run and inspect the event payload.
- [Cases steps](/explore-analyze/workflows/steps/cases.md): Open cases from your handler.
- [Connect workflows to the {{alerting-v2-system}}](../../alerting/experimental-alerting-system/workflows-alerting.md): Full reference for alert episode lifecycle triggers, including available trigger IDs, event payload fields, and when to use lifecycle triggers versus action policies.
