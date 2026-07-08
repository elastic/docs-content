---
navigation_title: Reduce notification noise
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How to reduce notification noise in the experimental alerting system using acknowledge, snooze, and deactivate to silence alert episodes."
---

# Reduce notification noise from the {{alerting-v2-system}} [reduce-notification-noise]

Several mechanisms within the {{alerting-v2-system}} can silence notifications for an alert episode. When an alert episode is silenced, the dispatcher stops processing it before any action policy matching, grouping, or frequency evaluation runs.

This page covers when to use each silencing mechanism and how the scope of an alert episode snooze differs from the scope of an action policy snooze. For an overview of where this fits in the full dispatch cycle, refer to [About action policies](about-action-policies.md).

## Silencing mechanisms [silencing-mechanisms]

Three mechanisms let you silence notifications, each at a different scope:

| Mechanism | Scope | When to use |
|---|---|---|
| Acknowledge | Per alert episode | You're actively investigating a breach and want to silence notifications for it without closing the alert episode. Clear the acknowledgment when you're done to restore notifications. |
| Snooze | Per series (group) | You want to quiet an entire alert series for a defined period, for example, during a known noisy window for a specific host. Snooze expires automatically at the end of the duration. |
| Deactivate | Per alert episode | You want to manually close an alert episode that hasn't recovered automatically. Deactivating marks the alert episode as inactive and stops notifications for it. Unlike acknowledge, this closes the alert episode rather than silencing it while leaving it active. |
| [Maintenance window](../../alerts/maintenance-windows.md) | All action policies in a space | You want to pause all action policy dispatching in a space for a planned maintenance period. All active action policies stop dispatching; rule evaluation and episode recording continue. Maintenance windows are configured separately from action policies. |

### Snooze scope

Snooze applies at the group level (by `group_hash`), not for each individual alert episode. When you snooze one alert episode, every alert episode sharing the same group (all rows with the same `rule_id` and `group_hash`) is silenced for the duration. Snoozing one row in the alerts table silences the entire series for that rule.

:::{note}
Snoozing an alert episode differs from snoozing an action policy. When you snooze an action policy, the dispatch mechanism is paused and every series the action policy processes is silenced. When you snooze an alert episode, you target one specific series before action policy matching runs, silencing it regardless of which action policy handles it. Use action policy snooze when you want to pause all notifications from a given action policy, for example, during planned maintenance on a destination system.
:::

## Related pages

- [About action policies](about-action-policies.md): Understand how eligibility checks, match conditions, and frequency gates work after silencing.
- [Create and configure an action policy](create-configure-action-policy.md): Set up the action policies that run after episode silencing checks pass.
- [Action policy reference](action-policy-reference.md): Look up match condition fields, grouping modes, and frequency options.
