---
navigation_title: Create an action policy
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Create action policies in the experimental alerting system to route alert episodes to workflows. Set the policy scope with rule tags or KQL, then batching and notification frequency."
---

# Create an action policy for the {{alerting-v2-system}} [create-action-policy]

In the {{alerting-v2-system}}, an action policy connects alert episodes to the [workflows](../../../workflows.md) that respond to them. To create one, you set which alert episodes the policy applies to, how those episodes batch into notifications, how often a workflow can run, and which workflows to invoke.

To start, go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Action Policies**.

## Specify the action policy scope [matcher]

The policy's scope decides which alert episodes it applies to, and [frequency](#reduce-noise-grouping) decides how often the policy invokes a workflow for an alert episode in scope. Leave the scope empty and the policy applies to every alert episode in the space that [passes the eligibility check](about-action-policies.md#action-policy-gates). Rule events that aren't part of an alert episode (`type: signal`) stay in `.rule-events`, so the action policy scope doesn't include them.

To narrow the scope of an action policy, filter by [rule tags](#filter-by-rule-tags), with a [KQL expression](#filter-with-kql-expression), or both. If you use both, the episode's rule has to carry one of the tags and the episode has to match the expression.

### Filter by rule tags [filter-by-rule-tags]
```{applies_to}
serverless: experimental
stack: experimental 9.6+
```

Select tags in **Rule tags** to apply the policy to alert episodes from the rules that carry them. An alert episode is in scope when its rule carries at least one of the selected tags. You can select up to 50 tags, each up to 256 characters, including a tag that no rule uses yet.

| To apply the policy to | How to configure it |
|---|---|
| All alert episodes that pass the eligibility check, regardless of rule or severity | Leave **Rule tags** and **Match conditions** empty |
| Alert episodes at a specific severity level | Enter `severity: "critical"` in **Match conditions** |
| Alert episodes from rules sharing a tag | Select the tag, for example `checkout`, in **Rule tags** |
| Alert episodes from one specific rule | Give the rule a [tag](../rules/configure-rule-artifacts.md#add-tags-runbooks) that no other rule uses, then select that tag in **Rule tags** |

To narrow the scope further, add a [match conditions expression](#filter-with-kql-expression).

### Filter with a KQL expression [filter-with-kql-expression]

Add a **Match conditions** [KQL](../../../query-filter/languages/kql.md) expression to narrow the policy to the alert episodes whose fields match it. For example, `severity: "critical"` applies the policy to critical alert episodes only. For the fields you can use, refer to [Match conditions fields](action-policy-reference.md#action-policy-matcher-fields).

{applies_to}`serverless: experimental` {applies_to}`stack: experimental 9.6+` On a new action policy, **Match conditions** is hidden until you expand **Advanced matching**.

## Add tags to categorize the action policy [policy-tags]
```{applies_to}
stack: removed 9.6+, experimental =9.5
serverless: unavailable
```

Tags are optional labels you assign to an action policy to categorize it or filter it in the **Action Policies** list. Action policy tags describe the action policy itself, not the alert episodes it applies to. You can add, edit, or remove tags at any time without affecting routing behavior.

## Set batching and frequency [reduce-noise-grouping]

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

### Re-notify when severity escalates [re-notify-on-severity]

`On status change` re-notifies only when the alert episode's status changes, not when its severity changes. Once the action policy has invoked a workflow and the status stays the same, the throttle blocks re-notification, even if severity later escalates from `low` to `critical`.

To get a notification for the escalation, do either of the following:

* Create separate action policies scoped to specific severity levels. For examples, refer to [Manage severity escalation notifications](severity-escalation.md).
* Set a time-based frequency such as `At most once every 1h`, so the action policy invokes a workflow again after the interval regardless of severity or status changes. For examples, refer to [Re-notify for persistently active alert episodes](re-notification.md).

## Select workflows to invoke [policy-destinations]

An action policy needs at least one destination. In **Destination**, attach the [workflows](../../../workflows.md) that run when the action policy notifies. You can attach workflows you built earlier, create an email or Slack workflow without leaving the action policy, or do both. You can add or remove destinations later by editing the action policy.

### Attach an existing workflow [attach-existing-workflow]

In **Workflows**, search for a workflow by name and select it. Select as many as you need. Use an existing workflow for anything beyond a single message, such as opening a ticket, calling a webhook, or running several steps in order.

If the workflow doesn't exist yet, select **Create a workflow** to build it in the **Workflows** app in a new tab, then return to the action policy and select it.

### Create an email or Slack workflow [inline-email-slack-workflow]
```{applies_to}
serverless: experimental
stack: experimental 9.6+
```

If all the action policy needs to do is send an email or post a Slack message, build that workflow in the action policy itself:

1. Select **Create Email workflow** or **Create Slack workflow**.
2. Select a **Connector**, or select **+ Create new connector** to add one. For Slack, also select the **Channel**.
3. In **Parameters**, write the message in YAML. An email takes `to`, `subject`, and `message`. A Slack message takes `text`.

To put alert episode details in the message, reference the dispatcher payload with `{{inputs.payload.<field>}}`, for example `{{inputs.payload.policyId}}`, `{{inputs.payload.groupKey}}`, or `{{inputs.payload.episodes}}`.

{{kib}} creates a single-step workflow for each one when you save the action policy and attaches it as a destination. These are ordinary workflows, so you can open them in **Workflows** afterwards to edit them or attach them to another action policy. If the action policy fails to save, {{kib}} deletes the workflows it created for it.

### Create a notification from the rule form [notification-from-rule-form]
```{applies_to}
stack: removed 9.6+, experimental =9.5
serverless: unavailable
```

If you don't have a workflow ready, set up an email or Slack notification while you create a rule. When you save, {{kib}} creates the workflow and an action policy that matches that rule's alert episodes by `rule.id`.

## Check which policies apply to a rule [policies-that-match-a-rule]

When you create or edit a rule that opens alert episodes, the **Actions** step lists the policies that apply to those episodes under **Action policies**. Select a policy's name to open it for editing in a new tab.

The list also indicates why each policy applies.

::::{applies-switch}

:::{applies-item} { serverless: experimental, stack: experimental 9.6+ }
Each entry shows the connector types its workflows use, along with a badge or icon:

* A **Catch-all** badge means the policy has an empty scope, so it applies to alert episodes from every rule.
* A tag icon means the rule carries tags the policy selects. The tooltip lists them under **Matching rule tags**.
* An **Expression** badge means the policy also has a KQL expression. {{kib}} evaluates that expression against alert data when the policy runs, so the list can't confirm it in advance. A policy scoped by an expression alone doesn't appear in the list at all, but it can still apply once the rule opens an alert episode.
:::

:::{applies-item} stack: experimental =9.5
The list covers policies whose **Match conditions** expression matches the rule's ID, name, or tags. Policies that match every rule appear under **Global policies**, and policies that match this rule in particular appear under **Matching global policies**.
:::

::::

## Related pages

- [Manage action policies](manage-action-policies.md): Enable, disable, snooze, and rotate API keys after setup.
- [Action policy reference](action-policy-reference.md): Look up match condition fields, grouping modes, and frequency options.
- [About action policies](about-action-policies.md): Understand the eligibility, scope, and frequency gates that determine when workflows are invoked.
