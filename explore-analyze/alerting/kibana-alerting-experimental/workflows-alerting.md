---
navigation_title: Connect workflows
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How workflows connect to the experimental alerting system through action policies and alert episode lifecycle triggers, and when to use each."
---

# Connect workflows to the {{alerting-v2-system}} [connect-workflows-experimental-alerting-system]

Workflows are part of the {{alerting-v2-system}} in {{kib}}. [Workflows](../../workflows.md) are the delivery layer. They define what happens when the {{alerting-v2-system}} decides to act, such as sending a message, calling a webhook, or triggering an automation. Setting up a workflow is what connects the {{alerting-v2-system}} to the tools your team uses for incident response.

This page covers how action policies drive workflow invocations at runtime, the available alert episode lifecycle triggers, and when to use each pathway.

The {{alerting-v2-system}} connects to workflows through two pathways.

- **Action policies** - Action policies evaluate active alert episodes on a continuous schedule and invoke workflows based on match conditions and frequency settings.
- **Alert episode lifecycle triggers** - Workflows are invoked when a specific state change occurs on an alert episode, such as when the alert episode is activated, assigned, or resolved.

## How action policies invoke workflows [action-policy-driven-workflows]

:::{important}
Action policies need a workflow to act on alert episodes. Without one, the policy has nowhere to send notifications or run automations. If you haven't created a workflow yet, [build your first workflow](../../workflows/get-started/build-your-first-workflow.md) before continuing.
:::

After a rule runs, the system routes alert episodes to workflows through the following steps.

```
Rule → Alert episode → [Dispatcher] → Action policy → Workflow → Notification
```

1. A rule evaluates data on a schedule and writes a rule event.
2. In Alert mode, the rule event opens or updates an alert episode.
3. The dispatcher runs on a short interval, independently of the rule schedule, and picks up active alert episodes.
4. For each active alert episode, the dispatcher evaluates all enabled action policies. Each policy runs the episode through suppression, match conditions, grouping, and frequency gates.
5. For policies where the episode clears all gates, the dispatcher invokes the configured workflows.
6. Workflows deliver the notification or run the automation.

## Alert episode lifecycle triggers [alert-episode-lifecycle-triggers]

Alert episode lifecycle triggers are a type of [event-driven trigger](../../workflows/triggers/event-driven-triggers.md) that start a workflow automatically when a specific event occurs. 

The {{alerting-v2-system}} emits a trigger event each time an alert episode changes state (for example, when it's activated, assigned to a user, acknowledged, or snoozed) and any workflow attached to that trigger type runs immediately in response. 

For a list of available triggers and event payload fields, refer to [Alert episode lifecycle triggers](../../workflows/triggers/event-driven-triggers.md). 

## Choosing between lifecycle triggers and action policies [choosing-lifecycle-triggers-action-policies]

If you're unsure whether to use lifecycle triggers or action policies, the following table compares when each option is a good fit. Both can run different workflows simultaneously and coexist without conflict.

| | Action policies | Lifecycle triggers |
|---|---|---|
| **How they run** | Evaluate alert episodes on a continuous schedule | React immediately to a specific state change |
| **Frequency control** | Apply suppression, grouping, and frequency gates | Fire exactly once per state change, no gates to configure |
| **Best for** | Recurring notifications and escalation logic that runs as long as a problem persists | One-shot automations, such as opening a ticket when an episode is assigned or posting a message when it resolves |

## Next steps

- [Create and configure an action policy](action-policies/create-configure-action-policy.md) to start routing alert episodes to workflows.
- [Notifications and actions in {{alerting-v2-system}}](notifications-actions.md) to learn how action policies evaluate and gate alert episodes before invoking a workflow.

