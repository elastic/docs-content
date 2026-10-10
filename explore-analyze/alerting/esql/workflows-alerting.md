---
navigation_title: Connect workflows
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "How action policies and alert lifecycle triggers invoke workflows, and when to use each."
---

# Connect workflows [connect-workflows]

In {{alerting-v2-system}}, [workflows](../../workflows.md) define what happens in response to an alert, such as sending a message, calling a webhook, or opening a ticket.

## How the alerting system connects to workflows [connection-pathways]

{{alerting-v2-system-cap}} starts workflows in two ways: through action policies and through alert lifecycle triggers. Both require an alert.

### Action policies [action-policy-driven-workflows]

{{kib}} evaluates action policies against alerts on a continuous schedule. When an alert passes a policy's eligibility, scope, and frequency gates, {{kib}} invokes the policy's workflow. For the step-by-step evaluation sequence, refer to [How the dispatcher evaluates action policies](action-policies/about-action-policies.md#how-action-policies-evaluated).

### Alert lifecycle triggers [alert-episode-lifecycle-triggers]

```{applies_to}
serverless: preview
stack: experimental 9.5+
```

Lifecycle triggers are [event-driven triggers](../../workflows/triggers/event-driven-triggers.md) that start a workflow immediately when a user [resolves, assigns, acknowledges, or snoozes](alerts/triage-alert-episodes.md) an alert, with no scheduling or gating. Each action emits a named trigger event, such as `alerting.actions.alertAssigned` (`alerting.episodeAssigned` in earlier versions).

Lifecycle triggers don't fire on [automatic status changes](alerts.md#alert-episode-lifecycle), such as when an alert becomes active or recovers based on rule evaluations. To respond to those changes, use an action policy. For the full list of trigger IDs, refer to [Alert lifecycle triggers](../../workflows/triggers/event-driven-triggers.md#alert-episode-lifecycle-triggers-available).

### When to use action policies or lifecycle triggers [when-to-use-action-policies-lifecycle-triggers]

You can use both at the same time. Each runs its own workflows without conflict.

| | Action policies | Lifecycle triggers |
|---|---|---|
| **How they run** | Evaluate alerts on a continuous schedule | React immediately to a specific event |
| **Frequency control** | Apply eligibility, scope, and frequency gates | Fire exactly once per event, no gates to configure |
| **Best for** | Recurring notifications and escalation logic that runs as long as a problem persists | One-shot automations, such as opening a ticket when a user assigns an alert or posting a message when a user resolves it |

## Related pages

- [Create and configure an action policy](action-policies/create-configure-action-policy.md): Start routing alerts to workflows.
- [About action policies](action-policies/about-action-policies.md): Understand how action policies gate alerts before invoking a workflow.

