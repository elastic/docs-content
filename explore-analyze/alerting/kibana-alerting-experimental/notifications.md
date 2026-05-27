---
navigation_title: Notifications
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "How {{alerting-v2}} action policies route alert episodes to notifications: matchers, grouping, frequency, and workflow destinations."
---

# Notification routing in {{alerting-v2}}

After a rule produces alert episodes, action policies decide what to do about them: who gets notified, how often, and through which channel.

This page explains how action policies work. For creating and configuring them step by step, refer to [Create and configure an action policy](notifications/create-configure-action-policy.md).

## What is an action policy [action-policies]


An action policy is a saved object in your space that controls notification routing. Policies can be **global** or **per-rule**:

- **Global** policies apply to all episodes in the space, from any rule. When an episode is produced, the dispatcher evaluates all enabled global policies that are not snoozed. Global is the default type and suits most use cases.
- **Per-rule** policies are scoped to a single rule. They apply only to episodes produced by that specific rule. Use a per-rule policy when routing is specific to one rule and you don't want it to affect other rules in the space. The rule association is set at creation and cannot be changed.

Each policy has four controls:

| Control | What it does |
| --- | --- |
| Match conditions (optional KQL) | Filters which episodes this policy applies to. An empty match condition matches all episodes covered by the policy's scope. |
| Notify per | Controls how episodes batch into notifications: one per episode, one per notification group using **Group** mode, or one digest for all. |
| Frequency | Controls how often the policy can notify for the same notification group. |
| Destinations | One or more workflows to invoke when all conditions are met. |

## How policies apply to rules

**Global policies** don't reference rules directly. You scope them using KQL over episode and rule fields, for example `rule.tags: "checkout"` or `data.severity: "critical"`. A global policy applies to every matching episode in the space, from any rule.

**Per-rule policies** are bound to a specific rule at creation. They apply only to episodes from that rule, and you can still use match conditions to filter further within that rule's episodes.

Multiple policies can match the same episode, and each runs independently. There's no precedence or merging between them. If no policy matches an episode, no notification is sent. This is intentional.

## How action policies are evaluated [how-action-policies-evaluated]


{{kib}} runs a background process called the dispatcher that checks for eligible episodes on a short interval (around 10 seconds) and evaluates action policies against them. The dispatcher is separate from the rule schedule. Rules write events on their own cadence, and the dispatcher picks them up asynchronously.

For each enabled policy that is not snoozed, the dispatcher works through the following steps:

1. **Gating:** Is the episode acknowledged, snoozed, or deactivated? If so, skip dispatch. Refer to [Notification gating](notifications/notification-gating.md) to learn more.
2. **Matcher:** Does the episode match the policy's KQL? If not, skip this policy.
3. **Grouping:** How should matching episodes batch into notification groups?
4. **Frequency:** Has a notification already gone out for this notification group recently? If so, wait.
5. **Destinations:** Send to the policy's workflow destinations.

### Notification dispatch outcomes [possible-outcomes]
The dispatcher runs on a short interval (around 5 seconds). Notifications don't arrive on the exact rule schedule. They follow the dispatcher's own cycle.

### Possible outcomes [possible-outcomes]

Each notification attempt results in one of the following outcomes.

| Outcome | What it means |
| --- | --- |
| `dispatched` | A notification was sent. |
| `throttled` | Dispatch was suppressed because the **frequency** interval had not elapsed. |
| `suppressed` | Dispatch was blocked before the notification went out. The episode was acknowledged, snoozed, or deactivated, or the space is currently in a maintenance window. |
| `unmatched` | No policy matched this episode and no workflow ran. |
| `error` | Processing failed. Check {{kib}} logs. |

You can query these outcomes in Discover through the `.alert-actions` data stream.

## Why policies are separate from rules

Policies are independent of rules, which means:
- One global policy can cover episodes from many rules. For example, a policy matching `data.severity: "critical"` applies regardless of which rule produced the episode.
- You can update routing without touching any rule.
- Rules can be created without any action policy, which is useful for testing.

When you do need routing that's specific to one rule, create a per-rule policy and bind it to that rule at creation.

When you're ready to route notifications, go to [Create and configure an action policy](notifications/create-configure-action-policy.md).

