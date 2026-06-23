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

- **Action policies** evaluate active alert episodes on a continuous schedule and invoke workflows based on match conditions and frequency settings.
- **Alert episode lifecycle triggers** fire a workflow once when a specific state change occurs on an alert episode, such as when it is activated, assigned, or resolved.

## Action policy-driven workflows [action-policy-driven-workflows]

:::{important}
Before creating an action policy, make sure the workflows you want to use already exist in your space. For information on creating a workflow, refer to [Build your first workflow](../../workflows/get-started/build-your-first-workflow.md).
:::

Without a workflow attached, an action policy cannot act on an alert episode. After a rule runs, processing follows these steps.

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

:::{note}
Alert episode lifecycle triggers are available in Stack deployments only, from 9.5.0.
:::

The {{alerting-v2-system}} emits a workflow trigger event each time a significant state change occurs on an alert episode. You can attach a workflow to any of these triggers to run automations in response to specific transitions without routing through an action policy.

### Available triggers

<!-- [CONTENT NEEDED: Issue #6873 (Jun 8) documents a trigger with the ID `alertingV2.episodeAssigned`, while issue #7006 (Jun 19) lists the same trigger as `alerting.episodeAssigned`. Confirm the correct trigger ID prefix before publishing. The table below uses `alerting.*` per the more recent issue.] -->

| Trigger ID | When it fires |
|---|---|
| `alerting.episodeActivated` | An alert episode transitions to the active state. |
| `alerting.episodeDeactivated` | An alert episode is manually deactivated or recovers. |
| `alerting.episodeSnoozed` | An alert episode is snoozed. |
| `alerting.episodeUnsnoozed` | An alert episode is unsnoozed. |
| `alerting.episodeAcked` | An alert episode is acknowledged. |
| `alerting.episodeAssigned` | An alert episode is assigned to a user. |
| `alerting.episodeUnassigned` | An alert episode assignment is removed. |
| `alerting.episodeTagged` | A tag is applied to an alert episode. |

### Event payload

All lifecycle triggers include these common fields in the event payload.

| Field | Description |
|---|---|
| `episodeId` | Unique identifier of the alert episode. |
| `ruleId` | ID of the rule that produced the alert episode. |
| `spaceId` | ID of the Kibana space where the event occurred. |

Use these fields to write workflow conditions that scope the automation to specific rules or episodes. For example, use `event.ruleId: "my-rule-id"` to scope the workflow to alert episodes from a specific rule.

### When to use lifecycle triggers vs action policies

Action policies and lifecycle triggers serve different purposes.

- **Use action policies** when you need recurring notifications or escalation logic that runs as long as a problem persists. Action policies evaluate continuously and apply frequency controls, grouping, and suppression.
- **Use lifecycle triggers** when you need a one-shot response to a specific state change, such as opening a ticket when an alert episode is first assigned, or posting a summary when it resolves.

Both can run different workflows simultaneously and coexist without conflict.

## Next steps

- [Create and configure an action policy](action-policies/create-configure-action-policy.md) to start routing alert episodes to workflows.
- [Notifications and actions in {{alerting-v2-system}}](notifications-actions.md) to learn how action policies evaluate and gate alert episodes before invoking a workflow.

