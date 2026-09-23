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

This page covers how to link an action policy to rules, and how to configure grouping, frequency, and workflow destinations.

## Alert episode requirement [policy-alert-mode]

Action policies evaluate only alert episodes. Rule events that aren't part of an alert episode (`type: signal`) stay in `.rule-events` and aren't evaluated by action policies.

## Add tags to categorize the action policy [policy-tags]
```{applies_to}
stack: removed 9.6+, experimental =9.5
serverless: unavailable
```

Tags are optional labels you assign to an action policy to categorize it or filter it in the **Action Policies** list. Action policy tags describe the action policy itself, not the alert episodes it matches. You can add, edit, or remove tags at any time without affecting routing behavior.

## Link the action policy to rules [matcher]

**Policy scope** links the action policy to rules and can filter which alert episodes it applies to. Leaving it empty matches every eligible alert episode in the space. The eligibility check runs first, so alert episodes that are acknowledged, snoozed, or covered by a maintenance window are excluded before the scope is evaluated.

Multiple action policies can match the same alert episode, and each runs independently. There's no precedence or merging between them. If no action policy matches an alert episode, no workflow is invoked and no notification is sent. If you delete a rule, any action policies scoped to it aren't deleted automatically. Delete them after you delete the rule.

### Link with rule tags [link-with-rule-tags]
```{applies_to}
stack: ga 9.6+
serverless: ga
```

Use **Rule tags** to link the action policy to rules. This is the preferred way to create that relationship. The policy matches alert episodes from any rule that carries at least one of the tags you select, so adding tags includes more rules. To link the policy to one rule, give that rule a tag no other rule uses and select it. A rule with no tags never matches an action policy that specifies tags.

Add a filter when the alert episode also has to meet a condition. Open **Advanced matching** and enter a **Match conditions** [KQL](../../../query-filter/languages/kql.md) expression. When you set both tags and a filter, the episode has to satisfy both. The expression can reference the alert episode's own fields. For the available fields, refer to [Action policy reference](action-policy-reference.md#action-policy-matcher-fields).

| To match | How to configure it |
|---|---|
| All alert episodes that pass the eligibility check, regardless of rule or severity | Leave the scope empty |
| Alert episodes at a specific severity level | Enter `severity: "critical"` in **Match conditions** |
| Alert episodes from rules sharing a tag | Select the tag, for example `checkout`, in **Rule tags** |
| Alert episodes from one specific rule | Give the rule a tag that no other rule uses, then select that tag in **Rule tags** |

:::{dropdown} How the scope fields work
You can select up to 50 tags, each up to 256 characters. The field placeholder is **Search or add tags**. The **Recommended** group lists up to 20 of the most-used tags already on rules in the space. Enter text to search for more. You can also enter a tag that no rule has yet. Selected tags that aren't suggested appear under **Other**. When the space has no tagged rules, the field prompts you to add a tag.

**Advanced matching** stays collapsed until you open it, and it opens when you edit a policy that already has an expression. A summary in the section updates as you edit and states whether the policy applies to the selected tags, the expression, both, or every eligible alert episode in the space.
:::

### Match with a KQL expression [match-with-kql]
```{applies_to}
stack: removed 9.6+, experimental =9.5
serverless: unavailable
```

A single **Match conditions** [KQL](../../../query-filter/languages/kql.md) expression defines the scope, and it's the only scoping mechanism. There's no separate rule type or rule ID selector. Scope a group of rules with `rule.tags: "checkout"`. Scope one rule with `rule.id: "<rule-id>"`. Enter `severity: "critical"` to match alert episodes at a specific severity. Leave the expression empty to match every alert episode that passes the eligibility check.

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

Attach one or more [workflows](../../../workflows.md) to define what happens when the action policy matches. You can add or remove these workflows later by editing the action policy. For more complex routing or multi-step automations, build a dedicated workflow first and then attach it.

### Create a notification from the rule form [notification-from-rule-form]
```{applies_to}
stack: removed 9.6+, experimental =9.5
serverless: unavailable
```

If you don't have a workflow ready, you can set up an email or Slack notification while creating a rule. The system creates and links the workflow when you save, and the new action policy matches that rule with `rule.id: "<rule-id>"`.

### See which policies match a rule [policies-that-match-a-rule]
```{applies_to}
stack: ga 9.6+
serverless: ga
```

For a rule that opens alert episodes, the **Actions** step lists policies that already match the rule by catch-all or by tag under **Action policies**. A **Catch-all** badge means the policy applies to every rule. A tag icon means the policy matches one or more of the rule's tags, and its tooltip lists those tags under **Matching rule tags**. An **Expression** badge means the policy also has a KQL query. The dispatcher evaluates that query against alert data when the policy runs. This list omits policies that match only by a KQL expression, because they depend on alert data, and those policies can still match later.

## Related pages

- [Manage action policies](manage-action-policies.md): Enable, disable, snooze, and rotate API keys after setup.
- [Action policy reference](action-policy-reference.md): Look up match condition fields, grouping modes, and frequency options.
- [About action policies](about-action-policies.md): Understand the eligibility, match, and frequency gates that determine when workflows are invoked.
