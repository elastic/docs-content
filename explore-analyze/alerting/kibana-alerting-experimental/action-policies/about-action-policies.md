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

## Why policies are separate from rules [policies-separate-from-rules]

Policies are independent of rules. A single global policy can cover alert episodes from many rules, so a policy matching `severity: "critical"` applies regardless of which rule produced the alert episode. You can also update notification routing without touching any rule, and you can create rules without any action policy, which is useful for testing detection logic before wiring up notifications.

When you do need routing that is specific to one rule, create a per-rule policy and bind it to that rule at creation.

## How alert episodes are gated [action-policy-gates]

The three gates are suppression, match conditions, and frequency:

* **Suppression** - Suppression checks whether the alert episode should be silenced. Episodes that are acknowledged, snoozed, or inside a maintenance window are stopped here and no workflow is invoked. For details on each mechanism and its scope, refer to [Reduce notification noise](reduce-notification-noise.md).
* **Match conditions** - Match conditions filter which alert episodes the policy applies to. You define them using [KQL](../../../query-filter/languages/kql.md). An empty match condition applies to all alert episodes within the policy's scope.
* **Frequency** - Frequency controls how often the policy can invoke its workflows for the same group of episodes, and how episodes batch before a workflow is invoked. Options are one notification per alert episode, one per notification group, or one digest for all matching episodes. If a workflow was already invoked within the cooldown period, the episode waits.

If any gate stops the episode, the workflow is not invoked for that policy.

:::{note}
Because each action policy evaluates alert episodes independently, an episode that is blocked by one policy can still trigger a workflow through a second policy with different conditions.
:::

## How policy types differ [policy-types]

Policies can be global or per-rule. Global policies apply across all rules in a space and suit most use cases. Per-rule policies apply to a single rule and give you precise control over routing for that rule without affecting anything else in the space.

### Global policies

A global policy applies to all alert episodes in the space, from any rule. When an alert episode is produced, the dispatcher evaluates all enabled global policies that are not snoozed. Global is the default type and suits most use cases.

### Per-rule policies

A per-rule policy is scoped to a single rule. It applies only to alert episodes produced by that specific rule. Use a per-rule policy when routing is specific to one rule and you do not want it to affect other rules in the space. The rule association is set at creation and cannot be changed.

## How policies apply to rules [how-policies-apply]

How a policy applies depends on whether it is global or per-rule. Multiple policies can match the same alert episode, and each runs independently. There is no precedence or merging between them. If no policy matches an alert episode, no workflow is invoked and no notification is sent.

### Global policies

Global policies don't reference rules directly. You scope them using KQL over alert episode and rule fields, for example `rule.tags: "checkout"` or `data.severity: "critical"`. A global policy applies to every matching alert episode in the space, from any rule.

### Per-rule policies

Per-rule policies are bound to a specific rule at creation. They apply only to alert episodes from that rule, and you can still use match conditions to filter further within that rule's alert episodes.

## How action policies are evaluated [how-action-policies-evaluated]

{{kib}} runs a background process called the dispatcher that checks for eligible alert episodes on a short interval (around 5 seconds) and evaluates action policies against them. The dispatcher runs on its own cycle, separate from the rule schedule.

For each enabled policy that is not snoozed, the dispatcher works through the following steps:

1. **Gating:** Is the alert episode acknowledged, snoozed, or deactivated? If so, skip. Refer to [Reduce notification noise](reduce-notification-noise.md) to learn more.
2. **Matcher:** Does the alert episode match the policy's KQL? If not, skip this policy.
3. **Grouping:** How should matching alert episodes batch into notification groups?
4. **Frequency:** Has a workflow already been invoked for this notification group recently? If so, wait.
5. **Destinations:** Invoke the configured workflows.

Workflow invocations may not happen immediately after a rule evaluates.

:::{tip}
Severity changes can cause a policy to match an episode for the first time, which fires a notification even if the episode is not new. For example, if a policy is scoped to `severity: "critical"` and an episode escalates from `low` to `critical`, the policy fires because it has no prior notification record for that episode. However, a severity change alone does not re-trigger a policy that already matched the episode. Only a status change or the expiry of a time-based throttle can do that. For details and examples, refer to [Severity escalation and de-escalation](common-action-policy-scenarios.md#severity-escalation).
:::

## Next steps

- [Create and configure an action policy](create-configure-action-policy.md) to set up policy type, match conditions, grouping, frequency, and workflow destinations.
- [Manage action policies](manage-action-policies.md) to enable, disable, snooze, edit, or delete the policies in your space.
- [Action policy reference](action-policy-reference.md) to look up available match condition fields, grouping modes, and frequency options.
