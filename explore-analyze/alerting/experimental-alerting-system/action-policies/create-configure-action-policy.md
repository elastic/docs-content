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

In the {{alerting-v2-system}}, an action policy determines which alert episodes generate notifications, how they batch for dispatch, and where they're routed. To create an action policy, go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Action Policies**.

This page covers how to configure an action policy's match conditions, grouping, frequency, and workflow destinations. For a quicker setup, you can also create a basic action policy directly while creating a rule, as described in [Select workflows to invoke](#policy-destinations).

## Alert mode requirement [policy-alert-mode]

Action policies only apply to alert episodes from rules running in Alert mode. Rules running in Signal mode produce signals rather than alert episodes, so they aren't evaluated by action policies.

## Add tags to categorize the action policy [policy-tags]

Tags are optional labels you assign to an action policy to categorize it or filter it in the **Action Policies** list. Action policy tags describe the action policy itself, not the alert episodes it matches. You can add, edit, or remove tags at any time without affecting routing behavior.

## Filter which episodes the action policy applies to [matcher]

Use a [KQL](../../../query-filter/languages/kql.md) expression to filter which alert episodes this action policy applies to. Leaving it empty matches every eligible alert episode in the space. The matcher is the only scoping mechanism, there are no separate rule type or rule ID selector fields.

:::{note}
An empty matcher applies to all eligible episodes in the space, not literally every episode. The eligibility check runs first, so episodes that are acknowledged, snoozed, or covered by a maintenance window are excluded before the matcher ever evaluates them.
:::

The following table shows how different KQL expressions control the matching scope of an action policy:

| I want to match… | KQL expression | Example |
|---|---|---|
| All episodes that pass the eligibility check, regardless of rule or severity | No expression | No example |
| Episodes from one specific rule | `rule.id: "<rule-id>"` | `rule.id: "9fc6b280-5b9e-11ef-a6ec-119f369f542a"` |
| Episodes from rules sharing a tag | `rule.tags: "<tag>"` | `rule.tags: "checkout"` |
| Episodes at a specific severity level | `severity: "<severity>"` | `severity: "critical"` |

Multiple action policies can match the same alert episode, and each runs independently. There is no precedence or merging between them. If no action policy matches an alert episode, no workflow is invoked and no notification is sent. If you delete a rule, any action policies scoped to it are not deleted automatically. You must delete them manually after deleting the rule.

## Control how episodes batch and how often the action policy notifies [reduce-noise-grouping]

**Notify per** controls how alert episodes batch into notifications. **Frequency** controls how often the action policy can notify for each batch.

:::{table}
:widths: 4-4-4

| Notify per | What it does | Available Frequency options |
|---|---|---|
| Episode | One notification for each alert episode. | - On status change <br> - On status change + repeat at interval <br> - At most once every… <br> - Every evaluation |
| Group | Bundle alert episodes that share a field value. Specify a **Group by** field such as `data.service.name` or `data.host.name`. | - At most once every… <br> - Every evaluation |
| Digest | One notification for all matching alert episodes combined. | - At most once every… (default) <br> - Every evaluation |

:::

**Frequency** limits how often the action policy fires for a given alert episode or notification group, depending on the **Notify per** setting. The interval resets from the last time the action policy fired, so successive notifications stay at least `interval` apart. Set a duration such as `1h` or `30m`.

:::{note}
`On status change` only re-notifies when the alert episode's status changes, not when its severity changes. If the action policy already matched an episode and its status stays the same, the throttle blocks re-notification, even if severity later escalates from `low` to `critical`.

To receive escalation notifications, either create separate action policies scoped to specific severity levels, or use a time-based throttle such as `At most once every 1h` so the action policy re-notifies after the interval regardless of severity or status changes. For examples, refer to [Re-notify for persistently active episodes](re-notification.md).
:::

<!-- For detailed descriptions, frequency options, and examples for each mode, refer to [Notify per options](action-policy-reference.md#action-policy-notification-grouping). -->

## Select workflows to invoke [policy-destinations]

Attach one or more [workflows](../../../workflows.md) to define what happens when the action policy matches. If you don't have a workflow ready, you can set up a simple email or Slack notification while creating a rule instead. The system creates and links the workflow for you when you save. You can add or remove these notifications later by editing the action policy. For more complex routing or multi-step automations, build a dedicated workflow first and then attach it.

## Related pages

- [Manage action policies](manage-action-policies.md): Enable, disable, snooze, and rotate API keys after setup.
- [Action policy reference](action-policy-reference.md): Look up match condition fields, grouping modes, and frequency options.
- [About action policies](about-action-policies.md): Understand the eligibility, match, and frequency gates that determine when workflows are invoked.
