---
navigation_title: Notifications and actions
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "How to set up notifications and actions for rules. Action policies invoke workflows, which send the notification."
---

# Notifications and actions [notifications-actions]

Use this page to set up notifications and actions for alerts in {{alerting-v2-system}}. Build a workflow that sends a notification or runs automation, then create an action policy that invokes it. Rule events that aren't part of an alert (`type: signal`) stay in `.rule-events`. Both action policies and lifecycle triggers require an alert. For how those connections work at runtime, refer to [Connect workflows](workflows-alerting.md).

:::{note}
To use workflows, your role must have the appropriate privileges and your subscription must include workflows. Refer to the subscription page for [{{ecloud}}]({{subscriptions}}/cloud) and [{{stack}}/self-managed]({{subscriptions}}) for a breakdown of available features by tier.
:::

## Send notifications or trigger an action

To send a notification or trigger an action from a rule in {{alerting-v2-system}}:

1. [Build a workflow](../../workflows/get-started/build-your-first-workflow.md) that defines what to do, for example, send a message, call a webhook, open a case, or run any other automation.

2. [Create an action policy](action-policies/create-configure-action-policy.md) that routes alerts to that workflow. The action policy controls which alerts qualify, how they batch, and how often it invokes the workflow.

   {applies_to}`serverless: ga` {applies_to}`stack: experimental 9.6+` To apply the policy to specific rules, give the policy and those rules the same [routing tag](action-policies/create-configure-action-policy.md#routing-tags).

   For actions that fire exactly once in response to a specific alert event (such as opening a ticket when an alert is assigned) use an [alert lifecycle trigger](../../workflows/triggers/event-driven-triggers.md#alert-episode-lifecycle-triggers-event-driven) instead of an action policy. Refer to [Connect workflows](workflows-alerting.md) for a comparison of action policies and lifecycle triggers.

## What to do next with action policies [notifications-actions-next-steps]

From here, you can learn how action policies work and start creating your own.

- [About action policies](action-policies/about-action-policies.md): Understand how action policies evaluate and gate alerts.
- [Create an action policy](action-policies/create-configure-action-policy.md): Configure scope, grouping, frequency, and destinations.
- [Examples and common scenarios](action-policies/common-action-policy-scenarios.md): Route by severity, manage escalation, and re-notify for persistently active alerts.
