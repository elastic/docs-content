---
navigation_title: Create an action policy
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Create action policies in the experimental alerting system, configure match conditions, Notify per, Frequency, and workflow destinations."
---

# Create an action policy for the {{alerting-v2-system}} [create-manage-action-policies]


Action policies are part of the {{alerting-v2-system}} in {{kib}}. This page covers how to configure match conditions, grouping, frequency, and workflow destinations. Where rules define what counts as a problem, action policies define what happens when one is detected: which alert episodes generate notifications, how they batch for dispatch, and where they're routed.

Because action policies are separate from rules, you can update notification behavior across many rules at once without touching detection logic, and you can route the same alert episodes differently depending on severity or source. You create and manage action policies from the **Action policies** page, not from the rule form.

## Alert mode requirement [policy-alert-mode]

Action policies only apply to alert episodes from rules running in Alert mode. Rules running in Signal mode produce signals rather than alert episodes, so they aren't evaluated by action policies.

## Add tags to categorize the action policy [policy-tags]

Tags are optional labels you assign to an action policy to categorize it or filter it in the **Action policies** list. Action policy tags describe the action policy itself, not the alert episodes it matches. You can add, edit, or remove tags at any time without affecting routing behavior.

## Filter which episodes the action policy applies to [matcher]

Use a [KQL](../../../query-filter/languages/kql.md) expression to filter which alert episodes this action policy applies to. Leaving it empty matches every alert episode in the space. The matcher is the only scoping mechanism, there are no separate rule type or rule ID selector fields. Common patterns include scoping to a severity level (`severity: "critical"`), to a specific rule (`rule.id: "my-rule-id"`), or to rules with a shared tag (`rule.tags: "payment-service"`).

For all available fields, refer to [Match conditions fields](action-policy-reference.md#matcher-fields).

## Control how episodes batch and how often the action policy notifies [reduce-noise-grouping]

**Notify per** controls how alert episodes batch into notifications. **Frequency** controls how often the action policy can notify for each batch.

:::{table}
:widths: 4-4-4

| Notify per | What it does | Available Frequency options |
|---|---|---|
| Episode | One notification for each alert episode. | - On status change <br> - On status change + repeat at interval <br> - Every evaluation |
| Group | Bundle alert episodes that share a field value. Specify a **Group by** field such as `data.service.name` or `data.host.name`. | - At most once every… <br> - Every evaluation |
| Digest | One notification for all matching alert episodes combined. | - At most once every… (default) <br> - Every evaluation |

:::

**Frequency** limits how often the action policy fires for a given notification group. The interval resets from the last time the action policy fired, so successive notifications stay at least `interval` apart. Set a duration such as `1h` or `30m`.

:::{note}
`On status change` only re-notifies when the alert episode's status changes, not when its severity changes. If an episode escalates from `low` to `critical` but the action policy already matched it and the status hasn't changed, the throttle blocks re-notification.

To receive escalation notifications, either create separate action policies scoped to specific severity levels, or use a time-based throttle such as `At most once every 1h` so the action policy re-notifies after the interval regardless of severity or status changes. For examples, refer to [Re-notify for persistently active episodes](re-notification.md).
:::

For detailed descriptions, frequency options, and examples for each mode, refer to [Notify per options](action-policy-reference.md#notification-grouping).

## Select workflows to invoke [policy-destinations]

Attach one or more [workflows](../../../workflows.md) to define what happens when the action policy matches. If you don't have a workflow ready, you can set up a simple email or Slack notification while creating a rule instead. The system creates and links the workflow for you when you save. You can add or remove these notifications later by editing the policy. For more complex routing or multi-step automations, build a dedicated workflow first and then attach it.

## Related pages

- [Manage action policies in {{alerting-v2-system}}](manage-action-policies.md) - View, enable, disable, or snooze the action policies you create.
- [Action policy reference in {{alerting-v2-system}}](action-policy-reference.md) - Look up match condition fields, grouping modes, and frequency options.
- [About action policies](about-action-policies.md) - Understand how action policies evaluate and gate alert episodes.
