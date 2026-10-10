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

To notify people or run automation for an alert in {{alerting-v2-system}}, build a workflow and create an action policy that invokes it. Action policies act only on alerts, so the rule's [mode](rules/configure-rule-mode.md) must be **Detect and respond** or **Alert** (depending on your {{stack}} version).

Before you start, check the [notification requirements](setup.md#alerting-setup-requirements) and make sure your role has [access to workflows](manage/configure-access.md#alerting-workflows-access).

## Send notifications or trigger an action

To send a notification or trigger an action from a rule in {{alerting-v2-system}}:

1. [Build a workflow](../../workflows/get-started/build-your-first-workflow.md) that defines what to do, for example, send a message, call a webhook, open a case, or run any other automation.

2. [Create an action policy](action-policies/create-configure-action-policy.md) that routes alerts to that workflow. The action policy controls which alerts qualify, how they batch, and how often it invokes the workflow.

   {applies_to}`serverless: ga` {applies_to}`stack: experimental 9.6+` To apply the policy to specific rules, give the policy and those rules the same [routing tag](action-policies/create-configure-action-policy.md#routing-tags).

   To run a workflow when a user acts on an alert, such as opening a ticket when someone assigns it, use an [alert lifecycle trigger](../../workflows/triggers/event-driven-triggers.md#alert-episode-lifecycle-triggers-event-driven) instead. For a comparison, refer to [Connect workflows](workflows-alerting.md#when-to-use-action-policies-lifecycle-triggers).

## What to do next with action policies [notifications-actions-next-steps]

- [About action policies](action-policies/about-action-policies.md): Understand how action policies evaluate and gate alerts.
- [Create an action policy](action-policies/create-configure-action-policy.md): Configure scope, grouping, frequency, and destinations.
- [Examples and common scenarios](action-policies/common-action-policy-scenarios.md): Route by severity, manage escalation, and re-notify for persistently active alerts.
