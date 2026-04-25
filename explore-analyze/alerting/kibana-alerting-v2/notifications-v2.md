---
navigation_title: Notifications
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "How {{alerting-v2}} action policies route alert episodes to notifications: matchers, grouping, throttling, and workflow destinations."
---

# {{alerting-v2}} notifications

After a rule produces alert episodes, action policies decide what to do about them: who gets notified, how often, and through which channel.

This page explains how action policies work. For creating and configuring them step by step, refer to [Create and configure an action policy](notifications/create-configure-action-policy-v2.md).

## What is an action policy [action-policies-v2]

$$$action-policies-v2$$$

An action policy is a saved object in your space that controls notification routing. It's not attached to a rule. It's global within the space, so when an episode is produced, the system evaluates all enabled, unsnoozed policies in the space and decides which ones apply.

Each policy has four controls:

| Control | What it does |
| --- | --- |
| Matcher (optional KQL) | Filters which episodes this policy applies to. An empty matcher matches all episodes in the space. |
| Dispatch per (grouping) | Controls how episodes batch into notifications: one per episode, one per defined group, or one digest for all. |
| Frequency (throttling) | Controls how often the policy can notify for the same group. |
| Destinations | One or more workflows to invoke when all conditions are met. |

## How policies apply to rules

Action policies don't reference rules directly. You scope a policy using KQL over episode and rule fields, for example `rule.labels: "checkout"` or `data.severity: "critical"`. A policy applies to every matching episode in the space, from any rule.

Multiple policies can match the same episode, and each runs independently. There's no precedence or merging between them. If no policy matches an episode, no notification is sent. This is intentional.

## How action policies are evaluated [how-action-policies-evaluated-v2]

$$$how-action-policies-evaluated-v2$$$

When an episode is eligible for dispatch, the system processes each enabled, unsnoozed policy in order:

1. **Suppression:** Is the episode acknowledged, snoozed, or deactivated? If so, skip dispatch.
2. **Matcher:** Does the episode match the policy's KQL? If not, skip this policy.
3. **Grouping:** How should matching episodes batch into notification groups?
4. **Throttle:** Has a notification already gone out for this group recently? If so, wait.
5. **Destinations:** Send to the policy's workflow destinations.

The dispatcher runs on a short interval (around 10 seconds). Notifications don't arrive on the exact rule schedule; they follow the dispatcher's own cycle.

### Possible outcomes [possible-outcomes]

Each notification attempt results in one of the following outcomes.

| Outcome | What it means |
| --- | --- |
| `dispatched` | A notification was sent. |
| `throttled` | Dispatch was suppressed due to throttle timing. |
| `suppressed` | The episode was suppressed before dispatch (acknowledged, snoozed, or deactivated). |
| `unmatched` | No policy matched this episode; no workflow ran. |
| `error` | Processing failed. Check {{kib}} logs. |

You can query these outcomes in Discover through the `.alert-actions` data stream.

## Why policies are separate from rules

Rules don't own policies. A rule can't say "notify team X when it fires." Instead, team X creates an action policy that uses a KQL matcher to pick up matching episodes.

This design means:
- One policy can cover episodes from many rules.
- You can update routing without touching any rule.
- Rules can be created without any notification policy, which is useful for testing.

When you're ready to route notifications, go to [Create and configure an action policy](notifications/create-configure-action-policy-v2.md).

$$$matcher-v2$$$
$$$reduce-noise-grouping-v2$$$
$$$throttle-v2$$$
$$$create-manage-action-policies-v2$$$
