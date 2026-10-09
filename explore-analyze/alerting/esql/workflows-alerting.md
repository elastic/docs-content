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

In {{alerting-v2-system}}, [workflows](../../workflows.md) are the delivery layer that defines what happens in response to an alert, such as sending a message, calling a webhook, or triggering an automation. Workflows connect the alerting system to your incident-response tools.

This page covers how action policies drive workflow invocations at runtime, the available alert lifecycle triggers, and when to use each pathway.

## How the alerting system connects to workflows [connection-pathways]

{{alerting-v2-system-cap}} connects to workflows through two pathways. Both require an alert.

- **Action Policies** - Action policies evaluate eligible alerts on a continuous schedule and invoke workflows based on match conditions and frequency settings.
- **Alert lifecycle triggers** - Lifecycle triggers invoke workflows when a user takes a triage action on an alert, such as resolving, assigning, or acknowledging it.

### Action policies [action-policy-driven-workflows]

{{kib}} evaluates action policies against alerts on a continuous schedule and invokes a workflow when an alert meets a policy's conditions. After a rule runs, the system routes each alert through the eligibility, scope, and frequency gates before invoking a workflow. For the step-by-step evaluation sequence, refer to [How the dispatcher evaluates action policies](action-policies/about-action-policies.md#how-action-policies-evaluated).

### Alert lifecycle triggers [alert-episode-lifecycle-triggers]

Lifecycle triggers are a type of [event-driven trigger](../../workflows/triggers/event-driven-triggers.md) that start a workflow immediately when a specific event occurs on an alert, with no scheduling or gating.

When a user [resolves, assigns, acknowledges, or snoozes](alerts/triage-alert-episodes.md) an alert, {{alerting-v2-system}} emits a named trigger event (such as `alerting.actions.alertAssigned` or `alerting.actions.alertAcked`) and any workflow attached to it runs immediately. Lifecycle triggers don't fire on [automatic status changes](alerts.md#alert-episode-lifecycle), such as when an alert becomes active or recovers based on rule evaluations. To respond to those changes, use an action policy. For the full list of trigger IDs, including the earlier IDs used in {{stack}} 9.5, refer to [Alert lifecycle triggers](../../workflows/triggers/event-driven-triggers.md#alert-episode-lifecycle-triggers-available).

### When to use action policies or lifecycle triggers [when-to-use-action-policies-lifecycle-triggers]

If you're unsure whether to use lifecycle triggers or action policies, the following table compares when each option is a good fit. Both can run different workflows simultaneously and coexist without conflict.

| | Action policies | Lifecycle triggers |
|---|---|---|
| **How they run** | Evaluate alerts on a continuous schedule | React immediately to a specific event |
| **Frequency control** | Apply eligibility, match condition, and frequency gates | Fire exactly once per event, no gates to configure |
| **Best for** | Recurring notifications and escalation logic that runs as long as a problem persists | One-shot automations, such as opening a ticket when a user assigns an alert or posting a message when a user resolves it |

## Related pages

- [Create and configure an action policy](action-policies/create-configure-action-policy.md): Start routing alerts to workflows.
- [About action policies](action-policies/about-action-policies.md): Understand how action policies gate alerts before invoking a workflow.

