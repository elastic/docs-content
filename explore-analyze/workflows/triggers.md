---
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Learn about workflow triggers and how to create and configure them.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Triggers

Triggers determine when your workflows start executing. Every workflow must have at least one trigger defined.

A trigger is an event or condition that initiates a workflow. Without a trigger, a workflow remains dormant. Triggers connect workflows to real-world signals, schedules, or user actions.

Triggers also provide initial context to the workflow. For example, a workflow triggered by an alert carries the alert's metadata, entities, and source events. This context shapes how the workflow executes.

## Trigger types

The following types of triggers are available:
* [Manual triggers](#manual-triggers)
* [Scheduled triggers](#scheduled-triggers)
* [Alert triggers](#alert-triggers)
* [Event-driven triggers](#event-driven-triggers)

### Manual triggers

Manual triggers run workflows on-demand through the UI or API. They require explicit user action to start the workflow.

Use manual triggers for:

* Testing and development
* One-off data processing tasks
* Administrative actions
* Workflows that require a human decision to start

Manual trigger example:

```yaml
triggers:
  - type: manual
```

Refer to [](/explore-analyze/workflows/triggers/manual-triggers.md) for more information.

### Scheduled triggers

Scheduled triggers run workflows automatically at specific times or intervals. You can configure schedules using:

* Intervals: Run every _x_ minutes, hours, or days
* RRule expressions: Run at specific times (for example, daily at 2 AM)

Use scheduled triggers for:

* Daily reports
* Regular data cleanup
* Periodic health checks
* Scheduled data synchronization

Scheduled trigger example:

```yaml
triggers:
  - type: scheduled
    with:
      every: 5m
```

Refer to [](/explore-analyze/workflows/triggers/scheduled-triggers.md) for more information.

### Alert triggers

Alert triggers run workflows automatically when a detection or alerting rule generates an alert. The workflow receives the full alert context, including all fields and values.

Use alert triggers for:

* Alert enrichment and triage
* Automated incident response
* Case creation and assignment
* Notification routing based on alert severity

Alert trigger example:

```yaml
triggers:
  - type: alert
```

Refer to [](/explore-analyze/workflows/triggers/alert-triggers.md) for more information.

### Event-driven triggers

```{applies_to}
stack: ga 9.5+, preview =9.4
serverless: ga
```

Event-driven triggers run workflows when a platform event occurs:

* **`workflows.failed`** fires when another workflow's execution fails {applies_to}`stack: ga 9.5+, preview =9.4` {applies_to}`serverless: ga`.
* **Cases triggers** fire when cases change {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview`. The family includes `cases.caseCreated`, `cases.caseUpdated`, `cases.caseStatusUpdated`, `cases.attachmentsAdded`, and `cases.commentsAdded`.
* **Entity store triggers** fire when an entity's asset criticality or risk score changes in the entity store {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview`. The family includes `entityStore.entityAssetCriticalityUpdated` and `entityStore.entityRiskScoreChanged`.
* **Alert episode lifecycle triggers** fire on specific alert episode events in the {{alerting-v2-system}}, such as when it is activated, assigned, acknowledged, or snoozed. {applies_to}`stack: experimental 9.5+` {applies_to}`serverless: experimental`
* **{{alerting-v2-system-cap}} rule lifecycle triggers** fire when rules in the {{alerting-v2-system}} are created, updated, deleted, or have their status changed. The family includes `alerting.ruleCreated`, `alerting.ruleUpdated`, `alerting.ruleDeleted`, `alerting.ruleEnabled`, and `alerting.ruleDisabled`. {applies_to}`stack: experimental 9.5+` {applies_to}`serverless: experimental`

Use event-driven triggers for:

* Central error-handler workflows that react to failures across your automation
* Reacting to case lifecycle changes (case opened, status changed, attachments or comments added)
* Paging on-call, opening cases, or logging when a production workflow fails
* Auditing rule management actions, syncing rule inventory with external systems, or notifying a channel when rules change in the {{alerting-v2-system}} {applies_to}`stack: experimental 9.5+` {applies_to}`serverless: experimental`

Event-driven trigger example:

```yaml
triggers:
  - type: workflows.failed
```

Refer to [](/explore-analyze/workflows/triggers/event-driven-triggers.md) for more information.

## Trigger context

Each trigger type provides different data to the workflow context through the `event` field:

* **Manual**: User information and any parameters passed.
* **Scheduled**: Execution time and schedule information.
* **Alert**: Complete alert data including fields, severity, and rule information.
* **Event-driven**:
  * `workflows.failed` provides metadata about the failed workflow, its execution, and the step that failed.
  * Cases triggers provide `event.caseId`, `event.owner`, and event-specific fields (status changes carry `previousStatus` and `status`; attachment events carry IDs and type; comment events carry IDs).
  * Entity store triggers provide `event.entityId`, `event.entityType`, and event-specific fields (asset criticality changes carry `criticalityLevel`; risk score changes carry `score`, `previousScore`, `delta`, and `direction`). {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview`
  * Alert episode lifecycle triggers provide `event.episodeId`, `event.ruleId`, and `event.spaceId`. {applies_to}`stack: experimental 9.5+` {applies_to}`serverless: experimental`
  * {{alerting-v2-system-cap}} rule lifecycle triggers provide `event.rule.ruleId` and `event.rule.spaceId`. {applies_to}`stack: experimental 9.5+` {applies_to}`serverless: experimental`

  Refer to [Event-driven triggers](/explore-analyze/workflows/triggers/event-driven-triggers.md) for the full payload shapes.

Access trigger data in your workflow using template variables:

```yaml
steps:
  - name: logTriggerInfo
    type: console
    with:
      message: "Workflow started at {{ execution.startedAt }}"
      details: "Event data: {{ event | json:2 }}"
```