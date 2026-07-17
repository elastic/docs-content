---
navigation_title: Connect workflows
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How workflows connect to the experimental alerting system through action policies and alert episode lifecycle triggers, and when to use each."
---

# Connect workflows to the {{alerting-v2-system}} [connect-workflows]

[Workflows](../../workflows.md) are part of the {{alerting-v2-system}} in {{kib}}. They are the delivery layer that defines what happens when the {{alerting-v2-system}} takes an action, such as sending a message, calling a webhook, or triggering an automation. Workflows are what allow your team's incident response tools to connect with the {{alerting-v2-system}}.

This page covers how action policies drive workflow invocations at runtime, the available alert episode lifecycle triggers, and when to use each pathway.

## How the alerting system connects to workflows [connection-pathways]

The {{alerting-v2-system}} connects to workflows through two pathways.

- **Action policies** - Action policies evaluate active alert episodes on a continuous schedule and invoke workflows based on match conditions and frequency settings.
- **Alert episode lifecycle triggers** - Workflows are invoked when a specific event occurs on an alert episode, such as when the alert episode is activated, assigned, or resolved.

### Action policies [action-policy-driven-workflows]

Action policies evaluate alert episodes on a continuous schedule and invoke workflows when an episode meets the configured conditions. After a rule runs, the system routes alert episodes to workflows through a suppression check, match conditions, grouping, and frequency gates. For the full step-by-step evaluation sequence, refer to [How action policies are evaluated](action-policies/about-action-policies.md#how-action-policies-evaluated).

### Alert episode lifecycle triggers [alert-episode-lifecycle-triggers]

Lifecycle triggers are a type of [event-driven trigger](../../workflows/triggers/event-driven-triggers.md) that start a workflow immediately when a specific event occurs on an alert episode, with no scheduling or gating.

When an episode is activated, assigned to a user, acknowledged, or snoozed, the {{alerting-v2-system}} emits a trigger event, and any workflow attached to that trigger type runs immediately. Assigning, acknowledging, and snoozing are triage actions. They each emit their own lifecycle trigger, but they don't move the episode between its lifecycle states (`inactive`, `pending`, `active`, `recovering`).
<!-- TODO: When PR #6527 (alerts) merges, link "lifecycle states" above to alerts.md#alert-episode-lifecycle and "triage actions" to alerts/triage-alert-episodes.md. -->

For a list of available triggers and event payload fields, refer to [Alert episode lifecycle triggers](../../workflows/triggers/event-driven-triggers.md). 

### When to use action policies or lifecycle triggers [when-to-use-action-policies-lifecycle-triggers]

If you're unsure whether to use lifecycle triggers or action policies, the following table compares when each option is a good fit. Both can run different workflows simultaneously and coexist without conflict.

| | Action policies | Lifecycle triggers |
|---|---|---|
| **How they run** | Evaluate alert episodes on a continuous schedule | React immediately to a specific event |
| **Frequency control** | Apply suppression, grouping, and frequency gates | Fire exactly once per event, no gates to configure |
| **Best for** | Recurring notifications and escalation logic that runs as long as a problem persists | One-shot automations, such as opening a ticket when an episode is assigned or posting a message when it resolves |

## Related pages

- [Create and configure an action policy](action-policies/create-configure-action-policy.md): Start routing alert episodes to workflows.
- [About action policies](action-policies/about-action-policies.md): Understand how action policies gate alert episodes before invoking a workflow.

