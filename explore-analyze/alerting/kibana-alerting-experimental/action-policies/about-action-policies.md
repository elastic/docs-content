---
navigation_title: About action policies
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How action policies gate alert episodes through suppression, match conditions, and frequency before invoking workflows in the experimental alerting system."
---

# About action policies [about-action-policies]

Action policies are part of the {{alerting-v2-system}} in {{kib}}. An action policy is the gating layer between an alert episode and a workflow. It decides whether and when to invoke a workflow by running the alert episode through a sequence of gates. A workflow runs only if the alert episode clears each gate in sequence.

## Why action policies are separate from rules [policies-separate-from-rules]

Action policies are independent of rules. A single action policy can cover alert episodes from many rules, so an action policy matching `severity: "critical"` applies regardless of which rule produced the alert episode. You can also update notification routing without touching any rule, and you can create rules without any action policy, which is useful for testing detection logic before wiring up notifications.

When you need routing specific to one rule, scope an action policy to that rule using a matcher expression such as `rule.id: "my-rule-id"`.

## How action policies gate alert episodes [action-policy-gates]

The three gates are suppression, match conditions, and frequency:

* **Suppression** - Determines whether to silence the alert episode. Episodes that are acknowledged, snoozed, or inside a maintenance window are stopped here and no workflow is invoked. For details on each mechanism and its scope, refer to [Reduce notification noise](reduce-notification-noise.md).
* **Match conditions** - Filters which alert episodes the action policy applies to. You define them using a [KQL](../../../query-filter/languages/kql.md) expression. An empty match condition applies to all active, unsuppressed episodes in the space.
* **Frequency** - Controls how often the action policy can invoke its workflows for the same group of episodes, and how episodes batch before a workflow is invoked. Options are one notification per alert episode, one per notification group, or one digest for all matching episodes. If a workflow was already invoked within the cooldown period, the episode waits.

If any gate stops the episode, the workflow is not invoked for that action policy. Because each action policy evaluates alert episodes independently, an episode blocked by one action policy can still trigger a workflow through a second action policy with different conditions.

### Scoping with the KQL matcher [policy-types]

Every action policy you create has the potential to match alert episodes from any rule in the space. Which episodes actually get matched is expressed entirely through the KQL matcher. Leave the matcher empty to match all episodes in your space.

:::{note}
An empty matcher does not match every episode without exception. The suppression gate runs before the matcher, so episodes that are acknowledged, snoozed, or covered by a maintenance window are filtered out before the matcher evaluates. An empty matcher applies to all active, unsuppressed episodes in the space.
:::

The following table shows how different [KQL](../../../query-filter/languages/kql.md) expressions control the matching scope of an action policy:

| I want to match… | KQL expression | Example |
|---|---|---|
| All episodes that pass the suppression gate, regardless of rule or severity | No expression | No example |
| Episodes from one specific rule | `rule.id: "<rule-id>"` | `rule.id: "9fc6b280-5b9e-11ef-a6ec-119f369f542a"` |
| Episodes from rules sharing a tag | `rule.tags: "<tag>"` | `rule.tags: "checkout"` |
| Episodes at a specific severity level | `severity: "<severity>"` | `severity: "critical"` |

Multiple action policies can match the same alert episode, and each runs independently. There is no precedence or merging between them. If no action policy matches an alert episode, no workflow is invoked and no notification is sent. If you delete a rule, any action policies scoped to it are not deleted automatically. You must delete them manually after deleting the rule.

## How action policies are evaluated [how-action-policies-evaluated]

{{kib}} runs a background process called the dispatcher that checks for eligible alert episodes on a short interval (around 5 seconds) and evaluates action policies against them. The dispatcher runs on its own cycle, separate from the rule schedule.

For each enabled action policy that is not snoozed, the dispatcher works through the following steps:

| Step | Action |
|------|--------|
| 1 | Check whether the alert episode is acknowledged, snoozed, or marked inactive. If so, stop processing it. |
| 2 | Check whether the alert episode matches the action policy's KQL. If not, stop evaluating this action policy and move to the next one. The episode continues to be evaluated by other enabled action policies. |
| 3 | Determine how matching alert episodes batch into notification groups. |
| 4 | Check whether a workflow has already been invoked for this notification group recently. If so, wait. |
| 5 | Invoke the configured workflows. Workflow invocations happen after the dispatcher's next polling cycle, which runs roughly every 5 seconds after a rule evaluates. |

:::{tip}
A severity change can cause an action policy to match an episode for the first time and fire a notification, but it does not re-trigger an action policy that already matched the episode. For details and examples, refer to [Manage severity escalation notifications](severity-escalation.md).
:::

## Next steps

- [Create and configure an action policy](create-configure-action-policy.md) to set up match conditions, grouping, frequency, and workflow destinations.
- [Manage action policies](manage-action-policies.md) to enable, disable, snooze, edit, or delete the action policies in your space.
- [Action policy reference](action-policy-reference.md) to look up available match condition fields, grouping modes, and frequency options.
