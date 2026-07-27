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

[Workflows](../../workflows.md) are the delivery layer that defines what happens when the {{alerting-v2-system}} takes an action, such as sending a message, calling a webhook, or triggering an automation. Workflows are what allow your team's incident response tools to connect with the {{alerting-v2-system}}.

This page covers how action policies drive workflow invocations at runtime, the available alert episode lifecycle triggers, and when to use each pathway.

## How the alerting system connects to workflows [connection-pathways]

The {{alerting-v2-system}} connects to workflows through two pathways.

- **Action Policies** - Action policies evaluate active alert episodes on a continuous schedule and invoke workflows based on match conditions and frequency settings.
- **Alert episode lifecycle triggers** - Workflows are invoked when a specific event occurs on an alert episode, such as when the alert episode is activated, assigned, or deactivated.

### Action policies [action-policy-driven-workflows]

Action policies evaluate alert episodes on a continuous schedule and invoke workflows when an episode meets the configured conditions. After a rule runs, the system routes each alert episode through episode eligibility, match conditions, and frequency gates before invoking a workflow. For the step-by-step evaluation sequence, refer to [How action policies are evaluated](action-policies/about-action-policies.md#how-action-policies-evaluated).

### Alert episode lifecycle triggers [alert-episode-lifecycle-triggers]

Lifecycle triggers are a type of [event-driven trigger](../../workflows/triggers/event-driven-triggers.md) that start a workflow immediately when a specific event occurs on an alert episode, with no scheduling or gating.

When an episode is [activated](alerts.md#alert-episode-lifecycle), or [assigned, acknowledged, or snoozed](alerts/triage-alert-episodes.md), the {{alerting-v2-system}} emits a named trigger event (such as `alerting.episodeAssigned` or `alerting.episodeAcked`) and any workflow attached to it runs immediately.

### When to use action policies or lifecycle triggers [when-to-use-action-policies-lifecycle-triggers]

If you're unsure whether to use lifecycle triggers or action policies, the following table compares when each option is a good fit. Both can run different workflows simultaneously and coexist without conflict.

| | Action policies | Lifecycle triggers |
|---|---|---|
| **How they run** | Evaluate alert episodes on a continuous schedule | React immediately to a specific event |
| **Frequency control** | Apply eligibility, match condition, and frequency gates | Fire exactly once per event, no gates to configure |
| **Best for** | Recurring notifications and escalation logic that runs as long as a problem persists | One-shot automations, such as opening a ticket when an episode is assigned or posting a message when it's deactivated |

## Related pages

- [Create and configure an action policy](action-policies/create-configure-action-policy.md): Start routing alert episodes to workflows.
- [About action policies](action-policies/about-action-policies.md): Understand how action policies gate alert episodes before invoking a workflow.

