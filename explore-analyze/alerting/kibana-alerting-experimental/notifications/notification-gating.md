---
navigation_title: Notification gating
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "How {{alerting-v2}} gates notifications: which mechanisms suppress dispatch before action policies run, their scope, and when to use each."
---

# Notification gating [notification-gating]


Notification gating controls whether a matched alert episode triggers a notification. When an episode is gated, the dispatcher stops processing it before any action policy matcher, grouping, throttle, or destination runs. No notification is sent.

## How gating fits in the dispatcher [gating-in-dispatcher]


When an episode is eligible for dispatch, the dispatcher evaluates each enabled action policy in order:

1. **Gating:** Is the episode acknowledged, snoozed, or deactivated? If so, stop — no notification is sent.
2. **Matcher:** Does the episode match the policy's KQL? If not, skip this policy.
3. **Grouping:** How should matching episodes batch into notification groups?
4. **Throttle:** Has a notification already gone out for this group recently? If so, wait.
5. **Destinations:** Send to the policy's workflow destinations.

Gating is the first step. An episode that is acknowledged, snoozed, or deactivated never reaches routing.

## Gating mechanisms [gating-mechanisms]


Three mechanisms let you gate notifications, each at a different scope:

| Mechanism | Scope | When to use |
|---|---|---|
| Acknowledge | Per episode | You're actively investigating a breach and want to silence notifications for it without closing the episode. Clear the acknowledgement when you're done to restore notifications. |
| Snooze | Per series (group) | You want to quiet an entire alert series for a defined period — for example, during a known noisy window for a specific host. Snooze expires automatically at the end of the duration. |
| Deactivate | Per episode | You want to manually close an episode that hasn't recovered automatically. Deactivating marks the episode as inactive and stops notifications for it. Unlike acknowledge, this closes the episode rather than silencing it while leaving it active. |

Each mechanism is stored as a separate document in `.alert-actions`, so the full gating history for an episode is queryable in Discover.

### Snooze scope

Snooze applies at the group level (by `group_hash`), not per individual episode. When you snooze one episode, every episode sharing the same group — all rows with the same `rule_id` and `group_hash` — is silenced for the duration. Snoozing one row in the alerts table silences the entire series for that rule.

<!-- TODO: Uncomment when PR #6524 (alerts) is merged:
For instructions on snoozing and unsnoozing single or multiple episodes, refer to [View and manage alerts](../alerts/view-and-manage-alerts.md#snooze-episode).
-->

## Related pages

<!-- TODO: Uncomment when PR #6524 (alerts) is merged:
- **[View and manage alerts](../alerts/view-and-manage-alerts.md):** Apply gating actions (acknowledge, snooze, deactivate) from the alerts table or episode detail page.
- **[{{alerting-v2}} alerts](../alerts.md):** Understand alert episode lifecycle, series, and where alert data is stored.
-->
- **[Notifications](../notifications.md):** Set up action policies that control routing, grouping, and throttle after gating.
