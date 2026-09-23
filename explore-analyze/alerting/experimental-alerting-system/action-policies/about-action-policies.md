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

| Gate | What it checks |
|------|----------------|
| Episode eligibility | Whether the alert episode is acknowledged, snoozed, or in a maintenance window. Any of these stops it. |
| Policy scope {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` | Whether the alert episode's rule carries at least one of the policy's tags, and whether the alert episode matches the policy's [KQL](../../../query-filter/languages/kql.md) expression. If both are set on the policy, they both have to pass. An empty scope passes every eligible alert episode in the space. |
| Match conditions {applies_to}`stack: removed 9.6+, experimental =9.5` {applies_to}`serverless: unavailable` | Whether the alert episode matches the policy's [KQL](../../../query-filter/languages/kql.md) expression. An empty expression passes every eligible alert episode in the space. |
| Frequency | Whether a workflow already ran for the alert episode's notification group within the policy's frequency interval. If it did, the alert episode waits. |

If any gate stops the alert episode, the workflow is not invoked for that action policy. Multiple action policies can apply to the same alert episode, and each one checks the gates independently, with no precedence or merging between them.

An alert episode blocked by one action policy can still invoke a workflow through a second action policy with different conditions. If no action policy applies to an alert episode, no workflow is invoked and no notification is sent.

## How the dispatcher evaluates action policies [how-action-policies-evaluated]

{{kib}} runs a background process called the dispatcher that checks for eligible alert episodes on a short interval (around 5 seconds) and evaluates action policies against them. The dispatcher runs on its own cycle, separate from the rule schedule, so a notification can arrive a few seconds after the rule that produced the alert episode.

On each cycle, the dispatcher works through the following steps:

| Step | Action |
|------|--------|
| 1 | Collect the alert episodes that pass the eligibility check, and the action policies that are enabled and not snoozed. |
| 2 | Run each action policy through the remaining [gates](#action-policy-gates), stopping that policy at the first gate the alert episode fails. The other action policies still evaluate the alert episode. |
| 3 | Invoke the workflows for each notification group that clears every gate, on the next polling cycle. |

:::{tip}
If an action policy already applied to an alert episode, a severity change does not re-trigger it. A severity change can still bring the alert episode into a different action policy's scope for the first time and invoke a workflow. For details and examples, refer to [Manage severity escalation notifications](severity-escalation.md).
:::

## Related pages

- [Create and configure an action policy](create-configure-action-policy.md): Set up policy scope, grouping, frequency, and workflow destinations.
- [Manage action policies](manage-action-policies.md): Enable, disable, snooze, edit, or delete your action policies.
- [Action policy reference](action-policy-reference.md): Look up match condition fields, grouping modes, and frequency options.
- [Reduce notification noise](reduce-notification-noise.md): Acknowledge, snooze, or deactivate alert episodes so they stop at the eligibility gate.
