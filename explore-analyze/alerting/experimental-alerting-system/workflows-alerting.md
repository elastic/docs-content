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

[Workflows](../../workflows.md) are the delivery layer that defines what happens when the {{alerting-v2-system}} takes an action, such as sending a message, calling a webhook, or triggering an automation. Workflows connect the alerting system to your incident-response tools.

This page covers how action policies drive workflow invocations at runtime, the available alert episode lifecycle and rule execution triggers, and when to use each pathway.

## How the alerting system connects to workflows [connection-pathways]

The {{alerting-v2-system}} connects to workflows through the following pathways.

- **Action Policies** - Action policies evaluate eligible alert episodes on a continuous schedule and invoke workflows based on match conditions and frequency settings. Requires an alert episode.
- **Alert episode lifecycle triggers** - Workflows are invoked when a specific event occurs on an alert episode, such as when the alert episode is activated, assigned, or deactivated. Requires an alert episode.
- **Rule execution triggers** - Workflows are invoked based on the outcome of a rule's own execution, whether it produced rule events or failed. No alert episode is needed, so this is the only pathway for a rule whose `kind` is `signal`. {applies_to}`stack: experimental 9.6+` {applies_to}`serverless: experimental`

### Action policies [action-policy-driven-workflows]

{{kib}} evaluates action policies against alert episodes on a continuous schedule and invokes a workflow when an alert episode meets a policy's conditions. After a rule runs, the system routes each alert episode through the eligibility, scope, and frequency gates before invoking a workflow. For the step-by-step evaluation sequence, refer to [How the dispatcher evaluates action policies](action-policies/about-action-policies.md#how-action-policies-evaluated).

### Alert episode lifecycle triggers [alert-episode-lifecycle-triggers]

Lifecycle triggers are a type of [event-driven trigger](../../workflows/triggers/event-driven-triggers.md) that start a workflow immediately when a specific event occurs on an alert episode, with no scheduling or gating.

When an alert episode is [activated](alerts.md#alert-episode-lifecycle), or [assigned, acknowledged, or snoozed](alerts/triage-alert-episodes.md), the {{alerting-v2-system}} emits a named trigger event (such as `alerting.episodeAssigned` or `alerting.episodeAcked`) and any workflow attached to it runs immediately.

### Rule execution triggers [rule-execution-triggers]

```{applies_to}
stack: experimental 9.6+
serverless: experimental
```

Rule execution triggers react to a rule's own evaluation instead of to an alert episode. `alerting.ruleEventsGenerated` fires when an execution writes at least one rule event, and `alerting.ruleExecutionFailed` fires when an execution throws an error. Use them to process the rule events a single execution produced, or to find out that a rule stopped working at all.

Because these triggers don't need an alert episode, they're also the only way to automate on a rule whose `kind` is `signal`. For the trigger IDs, event payloads, and examples, refer to [rule execution triggers](../../workflows/triggers/event-driven-triggers.md#alerting-rule-execution-triggers-event-driven).

### When to use action policies or lifecycle triggers [when-to-use-action-policies-lifecycle-triggers]

If you're unsure whether to use lifecycle triggers or action policies, the following table compares when each option is a good fit. Both can run different workflows simultaneously and coexist without conflict.

| | Action policies | Lifecycle triggers |
|---|---|---|
| **How they run** | Evaluate alert episodes on a continuous schedule | React immediately to a specific event |
| **Frequency control** | Apply eligibility, match condition, and frequency gates | Fire exactly once per event, no gates to configure |
| **Best for** | Recurring notifications and escalation logic that runs as long as a problem persists | One-shot automations, such as opening a ticket when an alert episode is assigned or posting a message when it's deactivated |

{applies_to}`stack: experimental 9.6+` {applies_to}`serverless: experimental` Rule execution triggers aren't an alternative to either option, because they react to a rule's execution rather than to an alert episode. A rule can use them alongside an action policy or a lifecycle trigger.

## Related pages

- [Create and configure an action policy](action-policies/create-configure-action-policy.md): Start routing alert episodes to workflows.
- [About action policies](action-policies/about-action-policies.md): Understand how action policies gate alert episodes before invoking a workflow.

