---
navigation_title: Create an action policy
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Create action policies in the experimental alerting system, configure match conditions, Notify per, Frequency, and workflow destinations."
---

# Create an action policy for the {{alerting-v2-system}} [create-action-policy]

In the {{alerting-v2-system}}, an action policy determines which alert episodes invoke a workflow, how they batch, and which workflow runs. To create an action policy, go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Action Policies**.

This page covers how to configure an action policy's match conditions, grouping, frequency, and workflow destinations. For a quicker setup, you can also create a basic action policy directly while creating a rule, as described in [Select workflows to invoke](#policy-destinations).

## Alert episode requirement [policy-alert-mode]

Action policies evaluate only alert episodes. Rule events that aren't part of an alert episode (`type: signal`) stay in `.rule-events` and aren't evaluated by action policies.

## Add tags to categorize the action policy [policy-tags]
```{applies_to}
stack: removed 9.6+, experimental =9.5
serverless: unavailable
```

Tags are optional labels you assign to an action policy to categorize it or filter it in the **Action Policies** list. Action policy tags describe the action policy itself, not the alert episodes it matches. You can add, edit, or remove tags at any time without affecting routing behavior.

## Filter which alert episodes the action policy applies to [matcher]

**Policy scope** controls which alert episodes this action policy applies to. Leaving it empty matches every eligible alert episode in the space.

:::{note}
An empty scope applies to all eligible alert episodes in the space, not literally every alert episode. The eligibility check runs first, so alert episodes that are acknowledged, snoozed, or covered by a maintenance window are excluded before the scope is ever evaluated.
:::

{applies_to}`stack: experimental 9.6+` {applies_to}`serverless: experimental` Two optional controls define the scope. When you set both, an alert episode has to satisfy both:

* **Rule tags** selects the rules the action policy covers. It matches alert episodes from any rule carrying at least one of the tags you select, so adding tags broadens the scope rather than narrowing it. You can select up to 50 tags of up to 256 characters each. A rule with no tags never matches an action policy that specifies tags.
* **Match conditions**, under **Advanced matching**, is a [KQL](../../../query-filter/languages/kql.md) expression evaluated against each alert episode. It can reference the alert episode's own fields, but not the rule that produced it. For the available fields, refer to [Action policy reference](action-policy-reference.md#action-policy-matcher-fields).

{applies_to}`stack: removed 9.6+, experimental =9.5` {applies_to}`serverless: unavailable` A single **Match conditions** [KQL](../../../query-filter/languages/kql.md) expression defines the scope, and it is the only scoping mechanism: there are no separate rule type or rule ID selector fields. Scope to one rule with `rule.id: "<rule-id>"`, or to a group of rules with `rule.tags: "<tag>"`.

The following table shows how to configure some common scopes:

| I want to match… | How to configure it |
|---|---|
| All alert episodes that pass the eligibility check, regardless of rule or severity | Leave the scope empty |
| Alert episodes at a specific severity level | Enter `severity: "critical"` in **Match conditions** |
| Alert episodes from rules sharing a tag | {applies_to}`stack: experimental 9.6+` Select the tag, for example `checkout`, in **Rule tags** |
| Alert episodes from one specific rule | {applies_to}`stack: experimental 9.6+` Give the rule a tag that no other rule uses, then select that tag in **Rule tags** |

Multiple action policies can match the same alert episode, and each runs independently. There is no precedence or merging between them. If no action policy matches an alert episode, no workflow is invoked and no notification is sent. If you delete a rule, any action policies scoped to it are not deleted automatically. You must delete them manually after deleting the rule.

## Control how alert episodes batch and how often a workflow is invoked [reduce-noise-grouping]

**Notify per** controls how alert episodes batch before a workflow is invoked. **Frequency** controls how often the action policy can invoke a workflow for each batch.

:::{table}
:widths: 4-4-4

| Notify per | What it does | Available Frequency options |
|---|---|---|
| Episode | One workflow invocation for each alert episode. | - On status change <br> - On status change + repeat at interval <br> - At most once every… <br> - Every evaluation |
| Group | Bundle alert episodes that share a field value. Specify a **Group by** field such as `data.service.name` or `data.host.name`. | - At most once every… <br> - Every evaluation |
| Digest | One workflow invocation for all matching alert episodes combined. | - At most once every… (default) <br> - Every evaluation |

:::

**Frequency** limits how often the action policy can invoke a workflow for a given alert episode or notification group, depending on the **Notify per** setting. The interval resets from the last time a workflow was invoked, so successive notifications stay at least `interval` apart. Set a duration such as `1h` or `30m`.

:::{note}
`On status change` only re-notifies when the alert episode's status changes, not when its severity changes. If the action policy already matched an alert episode and its status stays the same, the throttle blocks re-notification, even if severity later escalates from `low` to `critical`.

To receive escalation notifications, either create separate action policies scoped to specific severity levels, or use a time-based throttle such as `At most once every 1h` so the action policy invokes a workflow again after the interval regardless of severity or status changes. For examples, refer to [Re-notify for persistently active alert episodes](re-notification.md).
:::

## Select workflows to invoke [policy-destinations]

Attach one or more [workflows](../../../workflows.md) to define what happens when the action policy matches. If you don't have a workflow ready, you can set up a simple email or Slack notification while creating a rule instead. The system creates and links the workflow for you when you save. You can add or remove these workflows later by editing the action policy. For more complex routing or multi-step automations, build a dedicated workflow first and then attach it.

## Related pages

- [Manage action policies](manage-action-policies.md): Enable, disable, snooze, and rotate API keys after setup.
- [Action policy reference](action-policy-reference.md): Look up match condition fields, grouping modes, and frequency options.
- [About action policies](about-action-policies.md): Understand the eligibility, match, and frequency gates that determine when workflows are invoked.
