---
navigation_title: Triggers
applies_to:
  stack: preview 9.3+
  serverless: preview
products:
  - id: kibana
  - id: elasticsearch
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Workflow triggers

Triggers determine when your workflows start executing. Every workflow must have at least one trigger defined.

A trigger is an event or condition that initiates a workflow. Without a trigger, a workflow remains dormant. Triggers connect workflows to real-world signals, schedules, or user actions.

Triggers also provide initial context to the workflow. For example, a workflow triggered by an alert carries the alert's metadata, entities, and source events. This context shapes how the workflow executes.

## Trigger types

The following trigger types are available:

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

### Scheduled triggers

Scheduled triggers run workflows automatically at specific times or intervals. You can configure schedules using:

* Intervals: Run every _x_ minutes, hours, or days
* Cron expressions: Run at specific times (for example, daily at 2 AM)

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
      interval: 5m
```

### Alert triggers

Alert triggers run workflows in response to {{kib}} alerts. When a detection or alerting rule generates an alert, the workflow receives the alert context, including all alert fields and values.

Use alert triggers for:

* Alert enrichment and triage
* Automated incident response
* Case creation and assignment
* Notification routing based on alert severity

Scheduled trigger example:

```yaml
triggers:
  - type: alert
```

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
      details: "Event data: {{ event | json(2) }}"
```