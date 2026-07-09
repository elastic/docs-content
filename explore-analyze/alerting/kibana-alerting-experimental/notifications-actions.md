---
navigation_title: Notifications and actions
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How to set up notifications and actions for rules in the experimental alerting system using workflows and action policies."
---

# Notifications and actions for the {{alerting-v2-system}} [experimental-alerting-system-notifications-actions]

{{rules-ui}} in the {{alerting-v2-system}} don't send notifications directly. Instead, they produce alert episodes, and you use workflows and action policies to decide what happens next. For an explanation of how these two connect at runtime, refer to [Connect workflows](workflows-alerting.md).

:::{note}
:applies_to: {"stack": "ga 9.4+", "serverless": "ga"}
To use workflows, your role must have the appropriate privileges and your subscription must include workflows. Refer to the subscription page for [{{ecloud}}]({{subscriptions}}/cloud) and [{{stack}}/self-managed]({{subscriptions}}) for a breakdown of available features by tier.
:::

## Send notifications or trigger an action

To send a notification or trigger an action from a rule in the {{alerting-v2-system}}:

1. [Build a workflow](../../workflows/get-started/build-your-first-workflow.md) that defines what to do, for example, send a message, call a webhook, open a case, or run any other automation.

2. [Create an action policy](action-policies/create-configure-action-policy.md) that routes alert episodes to that workflow. The action policy controls which alert episodes qualify, how they batch, and how often it invokes the workflow.

   For actions that fire exactly once in response to a specific alert episode state change (such as opening a ticket when an episode is assigned) use an [alert episode lifecycle trigger](../../workflows/triggers/event-driven-triggers.md#alert-episode-lifecycle-triggers-event-driven) instead of an action policy. Refer to [Connect workflows](workflows-alerting.md) for a comparison of action policies and lifecycle triggers.

## Related pages

- [Connect workflows](workflows-alerting.md): Understand how action policies and lifecycle triggers invoke workflows at runtime.
- [About action policies](action-policies/about-action-policies.md): Understand how action policies evaluate and gate alert episodes.
- [Create an action policy](action-policies/create-configure-action-policy.md): Configure match conditions, grouping, frequency, and destinations.
- [Action policy reference](action-policies/action-policy-reference.md): Look up match condition fields, grouping modes, and frequency options.
- [Manage action policies](action-policies/manage-action-policies.md): Enable, disable, snooze, edit, or delete action policies.
- [Reduce notification noise](action-policies/reduce-notification-noise.md): Silence alert episodes using acknowledgment, snooze, and maintenance windows.
