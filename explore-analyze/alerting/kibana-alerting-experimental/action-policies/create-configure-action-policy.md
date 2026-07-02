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


Action policies are part of the {{alerting-v2-system}} in {{kib}}. This page covers how to configure policy type, match conditions, grouping, frequency, and workflow destinations. Where rules define what counts as a problem, action policies define what happens when one is detected: which alert episodes generate notifications, how they batch for dispatch, and where they're routed.

Because policies are separate from rules, you can update notification behavior across many rules at once without touching detection logic, and you can route the same alert episodes differently depending on severity or source. You create and manage policies from the **Action policies** page, not from the rule form.

## Select a policy type [policy-type]

Action policies only process alert episodes from rules running in Alert mode. Signals produced by rules running in Detect mode aren't eligible for action policy evaluation.

An action policy can be **global** (applies to any alert episode in the space) or **per-rule** (scoped to a single rule). For an explanation of how the two types differ and how they evaluate, refer to [About action policies](about-action-policies.md#policy-types).

You set the policy type at creation and can't change it later. If you need a different type, create a new policy.

## Add tags to categorize the policy [policy-tags]

Tags are optional labels you assign to a policy to categorize it or filter it in the Action policies list. Policy tags describe the policy itself, not the alert episodes it matches. You can add, edit, or remove tags at any time without affecting routing behavior.

## Filter which episodes the policy applies to [matcher]

Use an optional [KQL](../../../query-filter/languages/kql.md) expression to filter which alert episodes this policy applies to. Leaving it empty matches every episode in the policy's scope.

Match conditions are the only way to scope a policy beyond its base type. There are no separate rule type or rule ID selector fields. Some common patterns include scoping to a severity level (`severity: "critical"`), to a specific rule (`rule.id: "my-rule-id"`), or to rules with a shared tag (`rule.tags: "payment-service"`).

For all available fields, refer to [Match conditions fields](action-policy-reference.md#matcher-fields).

## Control how episodes batch and how often the policy notifies [reduce-noise-grouping]

**Notify per** controls how alert episodes batch into notifications. **Frequency** controls how often the policy can notify for each batch.

:::{table}
:widths: 4-4-4

| Notify per | What it does | Available Frequency options |
|---|---|---|
| Episode | One notification per alert episode. | - On status change <br> - On status change + repeat at interval <br> - Every evaluation |
| Group | Bundle alert episodes that share a field value. Specify a **Group by** field such as `data.service.name` or `data.host.name`. | - At most once every… <br> - Every evaluation |
| Digest | One notification for all matching alert episodes combined. | - At most once every… (default) <br> - Every evaluation |

:::

**Frequency** limits how often the policy fires for a given notification group. The interval resets from the last time the policy fired, so successive notifications stay at least `interval` apart. Set a duration such as `1h` or `30m`.

:::{note}
`On status change` only re-notifies when the alert episode's status changes, not when its severity changes. If an episode escalates from `low` to `critical` but the policy already matched it and the status hasn't changed, the throttle blocks re-notification.

To receive escalation notifications, either create separate policies scoped to specific severity levels, or use a time-based throttle such as `At most once every 1h` so the policy re-notifies after the interval regardless of severity or status changes. For examples, refer to [Re-notify for persistently active episodes](re-notification.md).
:::

For detailed descriptions, frequency options, and examples for each mode, refer to [Notify per options](action-policy-reference.md#notification-grouping).

## Select workflows to invoke [policy-destinations]

One or more [workflows](../../../workflows.md) to invoke when the policy matches. Use the search field to find and attach workflows.

## Related pages

- [Manage action policies in {{alerting-v2-system}}](manage-action-policies.md) to view, enable, disable, or snooze the policies you create.
- [Action policy reference in {{alerting-v2-system}}](action-policy-reference.md) to look up match condition fields, grouping modes, and frequency options.
- [About action policies](about-action-policies.md) to understand how action policies evaluate and gate alert episodes.
