---
navigation_title: Reduce notification noise
applies_to:
  stack: preview
  serverless: preview
products:
  - id: kibana
description: "How to reduce notification noise in the {{alerting-v2-system}} using acknowledge, snooze, and deactivate to silence alert episodes."
---

# Reduce notification noise for the {{alerting-v2-system}} [reduce-notification-noise]

Acknowledge, snooze, and deactivate are part of the {{alerting-v2-system}} in {{kib}}. Each one silences notifications for an alert episode at a different scope. When an alert episode is silenced, the dispatcher stops processing it before any action policy matching, grouping, or frequency evaluation runs. For an overview of where this fits in the full dispatch cycle, refer to [Notifications and actions in {{alerting-v2-system}}](../notifications-actions.md).

## Silencing mechanisms [silencing-mechanisms]

Three mechanisms let you silence notifications, each at a different scope:

| Mechanism | Scope | When to use |
|---|---|---|
| Acknowledge | Per alert episode | You're actively investigating a breach and want to silence notifications for it without closing the alert episode. Clear the acknowledgment when you're done to restore notifications. |
| Snooze | Per series (group) | You want to quiet an entire alert series for a defined period, for example, during a known noisy window for a specific host. Snooze expires automatically at the end of the duration. |
| Deactivate | Per alert episode | You want to manually close an alert episode that hasn't recovered automatically. Deactivating marks the alert episode as inactive and stops notifications for it. Unlike acknowledge, this closes the alert episode rather than silencing it while leaving it active. |

Each mechanism is stored as a separate document in `.alert-actions`, so the full gating history for an episode is queryable in Discover.

### Snooze scope

Snooze applies at the group level (by `group_hash`), not per individual alert episode. When you snooze one alert episode, every alert episode sharing the same group (all rows with the same `rule_id` and `group_hash`) is silenced for the duration. Snoozing one row in the alerts table silences the entire series for that rule.

<!-- TODO: Uncomment when PR #6524 (alerts) is merged:
For instructions on snoozing and unsnoozing single or multiple episodes, refer to [View and manage alerts](../alerts/view-and-manage-alerts.md#snooze-episode).
-->

## Related pages

<!-- TODO: Uncomment when PR #6524 (alerts) is merged:
- [View and manage alerts](../alerts/view-and-manage-alerts.md) to apply gating actions from the alerts table or episode detail page.
- [{{alerting-v2-system}} alerts](../alerts.md) to understand alert episode lifecycle, series, and where alert data is stored.
-->
- [Notifications and actions in {{alerting-v2-system}}](../notifications-actions.md) to learn how action policies route and throttle alert episodes after silencing.
- [Create and configure an action policy](create-configure-action-policy.md) to set up the policies that run after gating checks pass.
- [Action policy reference](action-policy-reference.md) to look up match condition fields, grouping modes, and frequency options.
