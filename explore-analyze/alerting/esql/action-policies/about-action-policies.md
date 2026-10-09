---
navigation_title: About action policies
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "Action policies decide whether and when an alert invokes a workflow. Eligibility, policy scope, and frequency gates control each dispatcher decision."
---

# About action policies [about-action-policies]

:::{include} /explore-analyze/alerting/esql/_snippets/v2-system-note.md
:::

In {{alerting-v2-system}}, an action policy is the gating layer between an alert and a workflow. It decides whether and when to invoke a workflow by running the alert through a sequence of gates, and a workflow runs only once the alert clears every gate.

This page explains how rules and action policies work together, the gates an alert must pass, and how the dispatcher evaluates them.

## How rules and action policies work together [rules-and-action-policies]

A rule detects a condition and opens alerts. A rule doesn't store which action policies apply to its alerts. Instead, {{kib}} evaluates each action policy in the space against every [eligible](#action-policy-gates) alert, and invokes a workflow for the ones that pass every gate.

Because of that separation, a single action policy can apply to alerts from many rules. An action policy scoped to `severity: "critical"` applies to every critical alert, regardless of which rule produced it. The separation also means you change how alerts are routed by editing the action policy, not the rule's detection logic.

To narrow which alerts an action policy applies to, set its [scope](create-configure-action-policy.md#matcher). An action policy with an empty scope applies to every eligible alert in the space.

{applies_to}`serverless: ga` {applies_to}`stack: experimental 9.6+` To apply an action policy to specific rules, give the policy and those rules the same [routing tag](create-configure-action-policy.md#routing-tags). A policy applies to alerts from every rule that has at least one of its routing tags, including rules you tag after you create the policy. The link doesn't depend on the rule's ID, name, or rule tags. You can rename a rule or reorganize its rule tags without changing which policies apply.

## How action policies gate alerts [action-policy-gates]

A workflow runs only when the alert passes every gate. {{kib}} checks the gates in this order:

| Gate | What it checks |
|------|----------------|
| Alert eligibility | Whether the alert is acknowledged, snoozed, resolved, or in a maintenance window. Any of these stops it. |
| Policy scope {applies_to}`serverless: ga` {applies_to}`stack: experimental 9.6+` | Whether the alert's rule has at least one of the policy's [routing tags](create-configure-action-policy.md#routing-tags), and whether the alert matches the policy's [KQL](../../../query-filter/languages/kql.md) expression. If the policy has both, the alert has to pass both. An empty scope passes every eligible alert in the space. |
| Match conditions {applies_to}`stack: removed 9.6+, experimental =9.5` {applies_to}`serverless: unavailable` | Whether the alert matches the policy's [KQL](../../../query-filter/languages/kql.md) expression. An empty expression passes every eligible alert in the space. |
| Frequency | Whether a workflow already ran for the alert's notification group within the policy's frequency interval. If it did, the alert waits. |

If any gate stops the alert, {{kib}} doesn't invoke a workflow for that action policy. Multiple action policies can apply to the same alert, and {{kib}} checks the gates separately for each one, with no precedence or merging between them.

An alert blocked by one action policy can still invoke a workflow through a second action policy with different conditions. If no action policy applies to an alert, no workflow is invoked and no notification is sent.

## How the dispatcher evaluates action policies [how-action-policies-evaluated]

{{kib}} runs a background process called the dispatcher that checks for eligible alerts on a short interval (around 5 seconds) and evaluates action policies against them. The dispatcher runs on its own cycle, separate from the rule schedule, so a notification can arrive a few seconds after the rule that produced the alert.

On each cycle, the dispatcher works through the following steps:

| Step | Action |
|------|--------|
| 1 | Collect the alerts that pass the eligibility check, and the action policies that are enabled and not snoozed. |
| 2 | Run each action policy through the remaining [gates](#action-policy-gates), stopping that policy at the first gate the alert fails. A failure in one action policy doesn't stop the others. |
| 3 | Invoke the workflows for each notification group that clears every gate. |

:::{tip}
If an action policy already applied to an alert, a severity change does not re-trigger it. A severity change can still bring the alert into a different action policy's scope for the first time and invoke a workflow. For details and examples, refer to [Manage severity escalation notifications](severity-escalation.md).
:::

## Related pages

- [Create and configure an action policy](create-configure-action-policy.md): Set up policy scope, grouping, frequency, and workflow destinations.
- [Manage action policies](manage-action-policies.md): Enable, disable, snooze, edit, or delete your action policies.
- [Action policy reference](action-policy-reference.md): Look up match condition fields, grouping modes, and frequency options.
- [Reduce notification noise](reduce-notification-noise.md): Acknowledge, snooze, or resolve alerts so they stop at the eligibility gate.
