---
navigation_title: Notifications and actions
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How to set up notifications and actions for rules in the experimental alerting system using workflows and action policies."
---

# Notifications and actions for the {{alerting-v2-system}} [notifications-actions]

{{rules-ui}} in the {{alerting-v2-system}} don't send notifications directly. Instead, they produce alert episodes, and you use workflows and action policies to decide what happens next. For an explanation of how these two connect at runtime, refer to [Connect workflows](workflows-alerting.md).

:::{note}
To use workflows, your role must have the appropriate privileges and your subscription must include workflows. Refer to the subscription page for [{{ecloud}}]({{subscriptions}}/cloud) and [{{stack}}/self-managed]({{subscriptions}}) for a breakdown of available features by tier.
:::

## Send notifications or trigger an action

To send a notification or trigger an action from a rule in the {{alerting-v2-system}}:

1. [Build a workflow](../../workflows/get-started/build-your-first-workflow.md) that defines what to do, for example, send a message, call a webhook, open a case, or run any other automation.

2. [Create an action policy](action-policies/create-configure-action-policy.md) that routes alert episodes to that workflow. The action policy controls which alert episodes qualify, how they batch, and how often it invokes the workflow.

   For actions that fire exactly once in response to a specific alert episode event (such as opening a ticket when an episode is assigned) use an [alert episode lifecycle trigger](../../workflows/triggers/event-driven-triggers.md#alert-episode-lifecycle-triggers-event-driven) instead of an action policy. Refer to [Connect workflows](workflows-alerting.md) for a comparison of action policies and lifecycle triggers.

## What to do next with action policies [notifications-actions-next-steps]

From here, you can learn how action policies work and start creating your own.

- [About action policies](action-policies/about-action-policies.md): Understand how action policies evaluate and gate alert episodes.
- [Create an action policy](action-policies/create-configure-action-policy.md): Configure match conditions, grouping, frequency, and destinations.
- [Examples and common scenarios](action-policies/common-action-policy-scenarios.md): Route by severity, manage escalation, and re-notify for persistently active episodes.

:::{important} - How to use the {{alerting-v2-system}} docs
The docs about the {{alerting-v2-system}} don't always name a specific button or menu. When that's the case, look for the closest matching label in the {{kib}} UI.
:::
