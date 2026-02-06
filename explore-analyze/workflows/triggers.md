---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn about workflow triggers and how to create and configure them.
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

## Trigger context

Each trigger type provides different data to the workflow context through the `event` field:

* **Manual**: User information and any parameters passed
* **Scheduled**: Execution time and schedule information
* **Alert**: Complete alert data including fields, severity, and rule information

Access trigger data in your workflow using template variables:

```yaml
steps:
  - name: logTriggerInfo
    type: console
    with:
      message: "Workflow started at {{ execution.startedAt }}"
      details: "Event data: {{ event | json:2 }}"
```