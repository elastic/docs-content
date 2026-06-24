---
navigation_title: Notifications and actions
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How to set up notifications and actions for rules in the experimental alerting system using workflows and action policies."
---

# Notifications and actions for the {{alerting-v2-system}}

Rules in the {{alerting-v2-system}} don't send notifications directly. Instead, they produce alert episodes, and you use workflows and action policies to decide what happens next.

- **Workflows** are the delivery layer. They define what happens when the system decides to act, such as sending a message, calling a webhook, or triggering an automation.
- **Action policies** are the gating layer. They evaluate active alert episodes on a continuous schedule and invoke workflows based on match conditions, grouping, and frequency settings.

## Get started

To send notifications or run actions from an alerting v2 rule:

1. [Build a workflow](../../workflows/get-started/build-your-first-workflow.md) that defines the action to take.
2. [Create an action policy](action-policies/create-configure-action-policy.md) that routes alert episodes to that workflow.

:::{tip}
If you need an action to fire exactly once in response to a specific alert episode state change (such as opening a ticket when an episode is assigned) use an alert episode lifecycle trigger instead of an action policy. Refer to [Connect workflows](workflows-alerting.md) for a comparison of both approaches.
:::

## In this section

- [Connect workflows](workflows-alerting.md) - How action policies and lifecycle triggers invoke workflows at runtime.
- [About action policies](action-policies/about-action-policies.md) - How action policies evaluate and gate alert episodes.
- [Create an action policy](action-policies/create-configure-action-policy.md) - Configure policy type, match conditions, grouping, frequency, and destinations.
- [Action policy reference](action-policies/action-policy-reference.md) - Available match condition fields, grouping modes, and frequency options.
- [Manage action policies](action-policies/manage-action-policies.md) - Enable, disable, snooze, edit, or delete policies.
- [Reduce notification noise](action-policies/reduce-notification-noise.md) - Suppress alerts using acknowledgment, snooze, and maintenance windows.
