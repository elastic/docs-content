---
navigation_title: Event-driven triggers
applies_to:
  stack: ga 9.5+, preview =9.4
  serverless: ga
description: Run a workflow in response to a platform event, such as a workflow failure, a case change, an entity store change, a security event, an alert lifecycle event, or an Agent Builder conversation change.
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

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+, preview =9.4` **`workflows.failed`**: Fires when another workflow's execution fails.
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.5+` **Cases triggers**: Fire when cases change (created, updated, status changed, attachments added, comments added).
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.5+` **Entity store triggers**: Fire when an entity's asset criticality or risk score changes in the entity store.
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.6+` **Security triggers**: Fire when detection alerts, attack discoveries, or document notes change.
- {applies_to}`observability: preview` {applies_to}`stack: preview 9.6+` **Alert lifecycle triggers in {{alerting-v2-system}}**: Fire when a user takes a triage action on an alert, such as resolving, assigning, acknowledging, or snoozing it.
- {applies_to}`observability: preview` {applies_to}`stack: preview 9.6+` **Rule lifecycle triggers in {{alerting-v2-system-short}}**: Fire when someone creates, updates, deletes, enables, or disables a rule.
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.6+` **{{agent-builder}} triggers**: Fire when a conversation attachment is added, updated, or deleted, or when conversation metadata changes. `ai.conversation.updated` also fires for other conversation changes, but only for conversation templates that have it turned on.


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
    type: pagerduty
    connector-id: "platform-pagerduty"
    with:
      eventAction: "trigger"
      dedupKey: "{{ event.workflow.id }}-{{ event.execution.id }}"
      summary: "Workflow {{ event.workflow.name }} failed"
      severity: "critical"
      customDetails:
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

## Security triggers [security-triggers-event-driven]

```{applies_to}
stack: preview 9.6+
serverless: preview
```

Security triggers fire when {{elastic-sec}} detection alerts, attack discoveries, or document notes change. Use them to react to triage activity without polling the {{elastic-sec}} APIs.

:::{note}
These triggers are separate from the alert lifecycle triggers for the {{alerting-v2-system}}. Refer to [](#alert-episode-lifecycle-triggers-event-driven) for those.
:::

**Shared schema.** Every security trigger takes a top-level `type`, set to the trigger ID, and an optional `condition` under `on`, which is a KQL predicate evaluated against the `event` payload. Like other event-driven triggers, they also accept [`on.workflowEvents`](#event-driven-triggers-workflow-events).

**Batched events.** The alert and attack discovery triggers fire once per bulk operation rather than once per affected item, so `event.alertIds` and `event.attackIds` are arrays. They list only the alerts or attack discoveries that actually changed, so an operation that changes nothing doesn't fire the trigger. Both arrays are capped at 10,000 entries, and `event.truncated` is `true` when the payload was capped. For the status triggers, that means more than 10,000 items were affected. For the tags and assignees triggers, it also means more than 100 tags or assignees were supplied in one operation, or that a tag value or assignee UID exceeded its length limit. Treat `event.truncated` as a signal to re-query the affected items rather than to trust the array. To act on each item in an untruncated payload, iterate the array with a `foreach` step.

**Related changes.** Changing the status, tags, or assignees of attack discoveries together with their related alerts fires both the attack discovery trigger and the matching alert trigger. A case status change that syncs to the case's attached alerts fires `security.alertStatusChanged` for detection alerts and `security.attackStatusChanged` for attack discoveries.

The note triggers carry a single `event.noteId` instead of an array, so they have no truncation field. Both fire only for notes attached to a document. Investigation guide notes and Timeline-level notes don't fire them.

### `security.alertStatusChanged` [security-alertstatuschanged-trigger]

Fires after the workflow status of a batch of detection alerts changes. The payload carries `event.alertIds`, `event.status` with the new status, `event.previousStatuses`, and `event.truncated`.

Statuses are `open`, `acknowledged`, and `closed`. A payload can also carry `in-progress`, an older status value that {{elastic-sec}} treats the same as `acknowledged`. Each entry in `event.previousStatuses` pairs an `id` with the `previousStatus` that alert held.

```yaml
triggers:
  - type: security.alertStatusChanged
    on:
      condition: 'event.status: "acknowledged"'
```

### `security.alertTagsChanged` [security-alerttagschanged-trigger]

Fires after tags are added to or removed from a batch of detection alerts. The payload carries `event.alertIds`, `event.tagsAdded`, `event.tagsRemoved`, and `event.truncated`.

```yaml
triggers:
  - type: security.alertTagsChanged
    on:
      condition: 'event.tagsAdded: "escalated"'
```

### `security.alertAssigneesChanged` [security-alertassigneeschanged-trigger]

Fires after assignees are added to or removed from a batch of detection alerts. The payload carries `event.alertIds`, `event.assigneesAdded`, `event.assigneesRemoved`, and `event.truncated`.

### `security.attackStatusChanged` [security-attackstatuschanged-trigger]

Fires after the workflow status of a batch of attack discoveries changes. The payload carries `event.attackIds`, `event.status`, `event.previousStatuses`, and `event.truncated`. It has the same shape as [`security.alertStatusChanged`](#security-alertstatuschanged-trigger), with attack discovery IDs in place of alert IDs.

### `security.attackTagsChanged` [security-attacktagschanged-trigger]

Fires after tags are added to or removed from a batch of attack discoveries. The payload carries `event.attackIds`, `event.tagsAdded`, `event.tagsRemoved`, and `event.truncated`.

### `security.attackAssigneesChanged` [security-attackassigneeschanged-trigger]

Fires after assignees are added to or removed from a batch of attack discoveries. The payload carries `event.attackIds`, `event.assigneesAdded`, `event.assigneesRemoved`, and `event.truncated`.

### `security.noteCreated` [security-notecreated-trigger]

Fires after a note is created on a document. The payload carries `event.noteId`, `event.createdBy` with the display name of the note's author (their full name if set, otherwise their username), and `event.documentId` with the ID of the document the note is attached to.

```yaml
triggers:
  - type: security.noteCreated
```

### `security.noteUpdated` [security-noteupdated-trigger]

Fires after an existing note on a document is updated. The payload carries `event.noteId`, `event.updatedBy` with the display name of the user who updated the note, and `event.documentId`.

## Alert lifecycle triggers in {{alerting-v2-system-short}} [alert-episode-lifecycle-triggers-event-driven]

```{applies_to}
serverless:
  observability: preview
stack: preview 9.6+
```

:::{note}
These triggers are available only when [{{alerting-v2-system-short}} is enabled](/explore-analyze/alerting/esql/setup.md).
:::

Alert lifecycle triggers run a workflow when a user acts on an alert in {{alerting-v2-system-short}}, either in the UI or through the API. They don't fire when an alert becomes active or recovers based on rule evaluations. To run a workflow when an alert's status changes automatically, use an action policy instead. For a comparison, refer to [When to use action policies or lifecycle triggers](../../alerting/esql/workflows-alerting.md#when-to-use-action-policies-lifecycle-triggers).

Each trigger fires exactly once per event. To subscribe a workflow, add the trigger ID to its `triggers` block, as with other event-driven triggers.

### Available triggers [alert-episode-lifecycle-triggers-available]

| Trigger ID | When it fires |
|---|---|
| `alerting.actions.alertActivated` | A user unresolves an alert. |
| `alerting.actions.alertDeactivated` | A user resolves an alert. |
| `alerting.actions.alertSnoozed` | An alert is snoozed. |
| `alerting.actions.alertUnsnoozed` | An alert is unsnoozed. |
| `alerting.actions.alertAcked` | An alert is acknowledged. |
| `alerting.actions.alertUnacked` | An alert acknowledgment is removed. |
| `alerting.actions.alertAssigned` | An alert is assigned to a user. |
| `alerting.actions.alertUnassigned` | An alert assignment is removed. |
| `alerting.actions.alertTagged` | A tag is applied to an alert. |

### Event payload [alert-episode-lifecycle-triggers-event]

All lifecycle triggers include these common fields in the event payload.

| `event.*` field | Contains |
|---|---|
| `event.alertId` | Unique identifier of the alert. |
| `event.ruleId` | ID of the rule that produced the alert. |
| `event.spaceId` | ID of the {{kib}} space where the event occurred. |

Reference these fields with Liquid templating in workflow steps:

```yaml
- name: log
  type: console
  with:
    message: |
      Alert {{ event.alertId }} from rule {{ event.ruleId }} changed state.
```

Use these fields to write workflow conditions that scope the automation to specific rules or alerts. For example, use `event.ruleId: "my-rule-id"` to scope the workflow to alerts from a specific rule.

## Rule lifecycle triggers in {{alerting-v2-system-short}} [alerting-rule-lifecycle-triggers-event-driven]

```{applies_to}
serverless:
  observability: preview
stack: preview 9.6+
```

:::{note}
These triggers are available only when [{{alerting-v2-system-short}} is enabled](/explore-analyze/alerting/esql/setup.md).
:::

Rule lifecycle triggers run a workflow when someone creates, updates, deletes, enables, or disables a rule. Use them to automate responses to rule management actions, for example, auditing rule changes, syncing rule inventory with an external CMDB, or notifying a team channel when a new rule is added to a space.

Rule lifecycle triggers fire independently of alerts.

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
| `event.rule.tags` | Tags assigned to the rule. |

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

## {{agent-builder}} triggers [agent-builder-triggers]

```{applies_to}
stack: preview 9.6+
serverless: preview
```

{{agent-builder}} triggers run a workflow when a conversation changes. Use them to react to attachment changes, metadata updates, and, for supported conversation templates, new messages and other conversation changes without polling the {{agent-builder}} APIs.

The attachment and metadata triggers are available wherever {{agent-builder}} is available. They aren't available in [Observability Logs Essentials](/solutions/observability/observability-serverless-feature-tiers.md) projects or in [Security Analytics Essentials](/solutions/security/security-serverless-feature-tiers.md) projects, where {{agent-builder}} is turned off.

[`ai.conversation.updated`](#ai-conversation-updated-trigger) has an additional requirement: it fires only for conversation templates that a {{kib}} feature has turned it on for. Refer to the trigger's section for details.

| Trigger | Fires when | Fires for |
|---|---|---|
| [`ai.attachmentAdded`](#ai-attachment-added-trigger) | An attachment is added. | Any conversation. |
| [`ai.attachmentUpdated`](#ai-attachment-updated-trigger) | An attachment's content changes. | Any conversation. |
| [`ai.attachmentDeleted`](#ai-attachment-deleted-trigger) | An attachment is deleted. | Any conversation. |
| [`ai.conversation.metadataUpdated`](#ai-conversation-metadata-updated-trigger) | A metadata update changes at least one field. | Conversations that use a template. |
| [`ai.conversation.updated`](#ai-conversation-updated-trigger) | A conversation write changes the conversation. | Conversation templates that have it turned on. |

### Attachment triggers [agent-builder-attachment-triggers]

Attachment triggers fire after the change is saved to the conversation.

An attachment trigger doesn't fire in these cases:

- **Hidden attachments**: Hidden attachments are internal conversation data, so adding, updating, or deleting one doesn't fire a trigger.
- **Changes other than content**: Edits to the description, the hidden setting, or the read-only setting don't fire `ai.attachmentUpdated`. Renaming an attachment or changing its origin doesn't fire a trigger.
- **Identical content**: The new content is identical to the current version.
- **Restores**: Restoring a soft-deleted attachment doesn't fire a trigger.
- **Permanently deleting a soft-deleted attachment**: The soft delete already fired `ai.attachmentDeleted`.

Every attachment trigger event includes these fields:

| Field | Contains |
|---|---|
| `event.conversationId` | The conversation the attachment belongs to. |
| `event.attachmentId` | The attachment ID. |
| `event.attachmentType` | The attachment type, for example `text`, `esql`, or `platform.dashboard.dashboard_state`. |
| `event.source` | What made the change. |

`event.source` is one of these values:

| Value | Set when |
|---|---|
| `workflow` | An attachment workflow step made the change (`ai.attachment.add`, `ai.attachment.update`, or `ai.attachment.delete`). |
| `http_api` | The attachment HTTP API made the change. |
| `server_api` | Another {{kib}} feature made the change through the {{agent-builder}} server API. |
| `chat_input` | The attachment was sent with a user message. |
| `execution` | The agent created or changed the attachment during a run, for example when a tool generates a dashboard. |

To skip attachment changes caused by workflows, pick the control that matches your goal:

| Goal | Use |
|---|---|
| Stop a workflow from triggering itself | Nothing. By default, [`on.workflowEvents`](#event-driven-triggers-workflow-events) skips a run when the workflow is already part of the current event chain. |
| Ignore attachment changes made by the attachment steps of any workflow | `event.source` in `on.condition`, as in the following example. `event.source` is narrower than `on.workflowEvents`: it identifies only what made this attachment change. Attachments that you pass to an `ai.agent` step report `chat_input`, so this condition doesn't skip them. |
| Ignore every event that originated from a workflow run, including attachments that an agent adds during an `ai.agent` step | `on.workflowEvents: ignore`. |

```yaml
triggers:
  - type: ai.attachmentAdded
    on:
      condition: 'not event.source: "workflow"'
```

### `ai.attachmentAdded` [ai-attachment-added-trigger]

Fires when an attachment is added to a conversation. `event.currentVersion` is `1`.

#### Schema

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `type` | top level | string | Yes | Must be `ai.attachmentAdded`. |
| `condition` | `on` | KQL string | No | Optional KQL predicate evaluated against the `event` payload. |

#### Event payload

In addition to the [shared attachment fields](#agent-builder-attachment-triggers):

| Field | Contains |
|---|---|
| `event.currentVersion` | The attachment version after this change. Always `1` for a new attachment. |

#### Example

Fire when an agent run attaches a dashboard:

```yaml
triggers:
  - type: ai.attachmentAdded
    on:
      condition: 'event.attachmentType: "platform.dashboard.dashboard_state" and event.source: "execution"'
```

### `ai.attachmentUpdated` [ai-attachment-updated-trigger]

Fires when a new content version of an attachment is stored. `event.currentVersion` is greater than `event.previousVersion`. Edits that don't change attachment content don't fire this trigger.

#### Schema

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `type` | top level | string | Yes | Must be `ai.attachmentUpdated`. |
| `condition` | `on` | KQL string | No | Optional KQL predicate evaluated against the `event` payload. |

#### Event payload

In addition to the [shared attachment fields](#agent-builder-attachment-triggers):

| Field | Contains |
|---|---|
| `event.previousVersion` | The attachment version before this change. |
| `event.currentVersion` | The attachment version after this change. |

#### Example

Fire when a user edits attachment content through chat or the attachment HTTP API:

```yaml
triggers:
  - type: ai.attachmentUpdated
    on:
      condition: 'event.source: "http_api" or event.source: "chat_input"'
```

### `ai.attachmentDeleted` [ai-attachment-deleted-trigger]

Fires when an attachment is soft-deleted or permanently deleted while it's still active. A soft-deleted attachment can be restored.

| Deletion | Result |
|---|---|
| Soft delete | Fires with `event.hardDelete` set to `false`. Restoring the attachment later doesn't fire another trigger. |
| Permanent deletion of an active attachment | Fires once, with `event.hardDelete` set to `true`. |
| Permanent deletion of an attachment that's already soft-deleted | Doesn't fire. The soft delete already fired this trigger. |

#### Schema

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `type` | top level | string | Yes | Must be `ai.attachmentDeleted`. |
| `condition` | `on` | KQL string | No | Optional KQL predicate evaluated against the `event` payload. |

#### Event payload

In addition to the [shared attachment fields](#agent-builder-attachment-triggers):

| Field | Contains |
|---|---|
| `event.hardDelete` | `true` when the attachment was permanently deleted. `false` when it was soft-deleted and can be restored. |

#### Example

Fire only when an attachment is permanently deleted:

```yaml
triggers:
  - type: ai.attachmentDeleted
    on:
      condition: 'event.hardDelete: true'
```

### `ai.conversation.metadataUpdated` [ai-conversation-metadata-updated-trigger]

Fires after a successful metadata update changes at least one stored field. Only conversations that use a template have metadata, so this trigger fires only for those conversations. The available templates are `investigation` and `escalation`.

This trigger doesn't fire when:

- The update changes nothing.
- Creating a conversation or applying a template sets metadata.

The payload has no `event.source` field. To skip changes made by workflows, use [`on.workflowEvents`](#event-driven-triggers-workflow-events).

#### Schema

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `type` | top level | string | Yes | Must be `ai.conversation.metadataUpdated`. |
| `condition` | `on` | KQL string | No | Optional KQL predicate evaluated against the `event` payload. |

#### Event payload

| Field | Contains |
|---|---|
| `event.conversationId` | The conversation whose metadata changed. |
| `event.templateId` | The template that defines the metadata schema, when the conversation has one. |
| `event.parentId` | The parent conversation, when this conversation is a child, such as a sub-agent. |
| `event.changedFields` | Names of the metadata fields that changed. Values aren't included. |

#### Example

Fire when a decision is recorded:

```yaml
triggers:
  - type: ai.conversation.metadataUpdated
    on:
      condition: 'event.changedFields: "decision"'
```

### `ai.conversation.updated` [ai-conversation-updated-trigger]

Fires after a successful conversation write that changes the conversation: new events, attachments, metadata, the title, the template, or access.

:::{important}
This trigger appears with the other {{agent-builder}} triggers, but a write fires it only for conversation templates that a {{kib}} feature has turned it on for. You can't turn it on for other templates. Writes to other conversations don't fire this trigger.

[{{alertzero}}](/solutions/security/alertzero/set-up-alertzero.md) is the only feature that turns it on, for [investigations](/solutions/security/alertzero/glossary.md#alertzero-glossary-investigation) (`event.templateId: "investigation"`) and [escalations](/solutions/security/alertzero/glossary.md#alertzero-glossary-escalation) (`event.templateId: "escalation"`). This applies when {{alertzero}} is available on your deployment and turned on in the space with the `securitySolution:enableAlertZero` advanced setting. On {{stack}}, that space must also use the Security solution view.
:::

This trigger doesn't fire for:

- A write that changes nothing.
- Changes that only affect hidden attachments.
- Deleting a conversation, marking it as read, pinning it, or saving feedback on an agent response.

#### Schema

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `type` | top level | string | Yes | Must be `ai.conversation.updated`. |
| `condition` | `on` | KQL string | No | Optional KQL predicate evaluated against the `event` payload. |

#### Event payload

The payload describes the write and doesn't include field values. Read the conversation when you need the values.

| Field | Contains |
|---|---|
| `event.conversationId` | The conversation that was written. |
| `event.templateId` | The conversation template, when it has one. |
| `event.parentId` | The parent conversation, when this conversation is a child, such as a sub-agent. |
| `event.source` | What performed the write: `execution` (an agent run, including the user message stored when it arrives and a generated title), `http_api` ({{agent-builder}} HTTP APIs), `workflow` ({{agent-builder}} workflow steps that write directly, such as `ai.conversation.add_event`), or `server_api` (another {{kib}} feature using the {{agent-builder}} server API). |
| `event.changeKinds` | What this write changed. One or more of `created`, `events`, `attachments`, `metadata`, `title`, `template`, and `access`. Never empty. `created` means the write created the conversation. |
| `event.eventTypes` | Types of the events this write added, with duplicates removed. Examples include `user_message`, `execution_terminated`, `attachment_added`, activity events such as `title_updated`, and custom event types. Empty when no event was added. |
| `event.actorTypes` | Actor types of the events this write added, with duplicates removed: `user`, `agent`, `external`, or `system`. |
| `event.executionId` | The agent run this write saved, whether it finished, failed, or was stopped. Absent when the write saved no run. |
| `event.attachmentTypes` | Types of the attachments this write added, updated, deleted, restored, or edited, with duplicates removed. |
| `event.attachmentIds` | IDs of the attachments this write changed. |
| `event.changedFields` | Names of the metadata fields whose stored value changed. Values aren't included. |

#### Filter events [ai-conversation-updated-filter]

Keep these behaviors in mind when you write an `on.condition`:

- **Array fields**: An array field matches when any element matches. For example, `event.eventTypes: "user_message"` matches a write that added a user message among other events.
- **Missing fields**: A wildcard on a missing field doesn't match, so `event.executionId: *` matches only writes that saved an agent run.
- **New conversations**: A write that creates a conversation reports `created` plus everything set at creation, including template defaults. Add `not event.changeKinds: "created"` when a condition should match only later changes.
- **Activity events**: Creating a conversation, applying a template, and changing the title, metadata, or access also add activity events to the conversation: `conversation_created`, `title_updated`, `metadata_updated`, `visibility_updated`, `participants_added`, or `participants_removed`. These writes report `events` in `event.changeKinds` too. To react only to new messages, filter on `event.eventTypes` instead of `event.changeKinds: "events"`.
- **Hidden attachments**: Events for hidden attachments are left out of `event.eventTypes`. Attachments that are hidden both before and after the write are left out of `event.attachmentTypes` and `event.attachmentIds`. A write that hides a visible attachment or reveals a hidden one is still reported in those fields.

#### Handle bursts of writes [ai-conversation-updated-bursts]

A single conversation can produce a burst of writes, for example while an agent runs. To coalesce them into one run at a time per conversation, set a [concurrency key](/explore-analyze/workflows/authoring-techniques/settings.md#workflows-settings-concurrency) that includes the workflow ID and `event.conversationId`, and queue at most one waiting run:

```yaml
settings:
  concurrency:
    key: "{{ workflow.id }}-{{ event.conversationId }}"
    strategy: queue
    max: 1
    queue-size: 1
```

Writes that arrive while a run is waiting are skipped, and the skipped runs appear in the workflow's execution history.

#### Avoid repeated runs [ai-conversation-updated-loops]

A workflow's own writes to the conversation don't trigger it again. By default, [`on.workflowEvents`](#event-driven-triggers-workflow-events) skips a run when the workflow is already part of the current event chain. This also covers user messages and agent runs that the workflow started. If you set `on.workflowEvents: allow-all`, add a condition that stops repeated runs.

Not every write a workflow causes has `event.source` set to `workflow`:

| Write caused by | `event.source` |
|---|---|
| Steps such as [`ai.conversation.add_event`](/explore-analyze/workflows/steps/ai-steps.md#ai-conversation-add-event) and [`ai.conversation.create`](/explore-analyze/workflows/steps/ai-steps.md#ai-conversation-create) | `workflow` |
| [`ai.conversation.add_user_message`](/explore-analyze/workflows/steps/ai-steps.md#ai-conversation-add-user-message) and agent runs started by [`ai.agent`](/explore-analyze/workflows/steps/ai-steps.md#ai-agent) | `execution` |
| Steps from other {{kib}} features, such as {{alertzero}} steps | `server_api` |

To ignore every write that originated from a workflow run, set `on.workflowEvents: ignore`.

#### Example

Fire when an {{alertzero}} investigation receives a user message:

```yaml
triggers:
  - type: ai.conversation.updated
    on:
      condition: 'event.templateId: "investigation" and event.eventTypes: "user_message"'
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

You can test an event-driven workflow against a real event before enabling it. When you run a workflow from the editor, the **Test workflow** dialog shows a tab for each way to supply data, including an **Event** tab for event-driven triggers.

On the **Event** tab, browse events that have already occurred for your trigger type. Use the KQL search bar and time range to narrow the list, select an event from the results, and run the workflow against that event's payload. The execution then runs exactly as it would have when the event first occurred, so you can confirm your conditions and steps behave as expected.

:::{tip}
To reuse the data from an earlier run instead of a fresh event, select **Historical** in the **Test workflow** dialog. Refer to [Provide data for a test run](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md#workflows-supply-test-input) for more information.
:::

## Related

- [Triggers overview](/explore-analyze/workflows/triggers.md): All trigger types.
- [Workflow authorization](/explore-analyze/workflows/authorization.md): Whose privileges event-driven workflows run with.
- [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md): Per-step `on-failure` strategies complement event-driven handlers.
- [Monitor workflow execution](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md): See what triggered each run and inspect the event payload.
- [Cases steps](/explore-analyze/workflows/steps/cases.md): Open cases from your handler.
- [Connect workflows to {{alerting-v2-system}}](../../alerting/esql/workflows-alerting.md): Learn how action policies invoke workflows for alerts, and when to use lifecycle triggers instead.
- [Connect {{agent-builder}} agents and Elastic Workflows](/explore-analyze/ai-features/agent-builder/agents-and-workflows.md): Other ways to use agents and workflows together.
