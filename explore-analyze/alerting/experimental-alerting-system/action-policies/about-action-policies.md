---
navigation_title: About action policies
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Action policies decide whether and when an alert episode invokes a workflow in the experimental alerting system. Eligibility, policy scope, and frequency gates control each dispatcher decision."
---

# About action policies [about-action-policies]

An action policy is the gating layer between an alert episode and a workflow in the {{alerting-v2-system}}. It decides whether and when to invoke a workflow by running the alert episode through a sequence of gates, and a workflow runs only once the alert episode clears every gate.

This page explains why action policies are separate from rules, the gates an alert episode must pass, and how the dispatcher evaluates them.

## Why action policies are separate from rules [policies-separate-from-rules]

Action policies are independent of rules. A single action policy can apply to alert episodes from many rules. An action policy scoped to `severity: "critical"` runs regardless of which rule produced the alert episode. You can create a rule without any action policy, which is useful for testing detection logic before wiring up notifications. You can also update notification routing later without touching the rule.

## How action policies gate alert episodes [action-policy-gates]

A workflow runs only when the alert episode passes every gate. The action policy checks the gates in this order:

* **Episode eligibility** - Skips alert episodes that are acknowledged, snoozed, or in a maintenance window. For details, refer to [Reduce notification noise](reduce-notification-noise.md).
* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` **Policy scope** - Limits the action policy to alert episodes from rules that carry at least one of the selected tags. You can also narrow it to the alert episodes that match a [KQL](../../../query-filter/languages/kql.md) expression. When you set tags and an expression, the alert episode has to satisfy both. An empty scope applies to every eligible alert episode in the space.
* {applies_to}`stack: removed 9.6+, experimental =9.5` {applies_to}`serverless: unavailable` **Match conditions** - Filters which alert episodes the action policy applies to. You define them using a [KQL](../../../query-filter/languages/kql.md) expression. An empty match condition applies to all eligible alert episodes in the space.
* **Frequency** - Controls how often the action policy can invoke its workflows for the same group of alert episodes, and how alert episodes batch before a workflow is invoked. If a workflow was already invoked within the frequency interval that you chose, the alert episode waits. For available options, refer to [Action policy reference](action-policy-reference.md).

If any gate stops the alert episode, the workflow is not invoked for that action policy. Multiple action policies can apply to the same alert episode, and each one checks the gates independently, with no precedence or merging between them. An alert episode blocked by one action policy can still invoke a workflow through a second action policy with different conditions. If no action policy applies to an alert episode, no workflow is invoked and no notification is sent.

## How action policies are evaluated [how-action-policies-evaluated]

{{kib}} runs a background process called the dispatcher that checks for eligible alert episodes on a short interval (around 5 seconds) and evaluates action policies against them. The dispatcher runs on its own cycle, separate from the rule schedule.

For each enabled action policy that is not snoozed, the dispatcher works through the following steps:

| Step | Action |
|------|--------|
| 1 | Check whether the alert episode is acknowledged, snoozed, or marked inactive. If so, stop processing it. |
| 2 | {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` Check the policy scope. If the scope is empty, continue. Otherwise, the rule has to carry at least one selected tag when you set tags, and the episode has to match the KQL expression when you set one. If either check fails, stop this action policy and continue with the next one. Other enabled action policies still evaluate the alert episode. <br> {applies_to}`stack: removed 9.6+, experimental =9.5` {applies_to}`serverless: unavailable` Check whether the alert episode matches the action policy's KQL. If not, stop evaluating this action policy and move to the next one. The alert episode continues to be evaluated by other enabled action policies. |
| 3 | Determine how the alert episodes in scope batch into notification groups. |
| 4 | Check whether a workflow has already been invoked for this notification group recently. If so, wait. |
| 5 | Invoke the configured workflows, on the dispatcher's next polling cycle (roughly every 5 seconds). |

:::{tip}
If an action policy already applied to an alert episode, a severity change does not re-trigger it. A severity change can still bring the alert episode into a different action policy's scope for the first time and invoke a workflow. For details and examples, refer to [Manage severity escalation notifications](severity-escalation.md).
:::

## Related pages

- [Create and configure an action policy](create-configure-action-policy.md): Set up policy scope, grouping, frequency, and workflow destinations.
- [Manage action policies](manage-action-policies.md): Enable, disable, snooze, edit, or delete your action policies.
- [Action policy reference](action-policy-reference.md): Look up match condition fields, grouping modes, and frequency options.
