---
navigation_title: Connect workflows
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How workflows connect to the {{alerting-v2-system}} action policies and rule automation, and where to configure them."
---

# Connect workflows to the {{alerting-v2-system}} [connect-workflows-experimental-alerting-system]

Workflows are part of the {{alerting-v2-system}} in {{kib}}. Without a workflow attached, an action policy cannot act on an alert episode. [Workflows](../../workflows.md) are the delivery layer. They define what happens when an action policy decides to act, such as sending a message, calling a webhook, or triggering automation. Setting up a workflow is what connects the {{alerting-v2-system}} to the tools your team uses for incident response.

:::{important}
Before creating an action policy, make sure the workflows you want to use already exist in your space. For information on creating a workflow, refer to [Build your first workflow](../../workflows/get-started/build-your-first-workflow.md).
:::

## Runtime execution order [runtime-execution-order]

After a rule runs, processing follows this sequence:

```
Rule → Alert episode → [Dispatcher] → Action policy → Workflow → Notification
```

1. A rule evaluates data on a schedule and writes a rule event.
2. In Alert mode, the rule event opens or updates an alert episode.
3. The dispatcher runs on a short interval, independently of the rule schedule, and picks up active alert episodes.
4. For each active alert episode, the dispatcher evaluates all enabled action policies. Each policy runs the episode through a sequence of gates: suppression, match conditions, grouping, and frequency.
5. For policies where the episode clears all gates, the dispatcher invokes the configured workflows.
6. Workflows deliver the notification or run the automation.

## Next steps

- [Create and configure an action policy](action-policies/create-configure-action-policy.md) to start routing alert episodes to workflows.
- [Notifications and actions in {{alerting-v2-system}}](notifications-actions.md) to learn how action policies evaluate and gate alert episodes before invoking a workflow.

