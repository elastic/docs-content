---
navigation_title: Reduce notification noise
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "How to reduce notification noise using acknowledge, snooze, and deactivate to silence alerts."
---

# Reduce notification noise [reduce-notification-noise]

{{alerting-v2-system-cap}} has several mechanisms that can silence notifications for an alert. When an alert is silenced, the dispatcher stops processing it before it evaluates any action policy against it.

This page covers when to use each silencing mechanism and how the scope of an alert snooze differs from the scope of an action policy snooze. For an overview of where this fits in the full dispatch cycle, refer to [About action policies](about-action-policies.md).

## Silencing mechanisms [silencing-mechanisms]

The following mechanisms let you silence notifications, each at a different scope:

| Mechanism | Scope | When to use |
|---|---|---|
| Acknowledge | Per alert | You're actively investigating a breach and want to silence notifications for it without closing the alert. Clear the acknowledgment when you're done to restore notifications. |
| Snooze | Per series (group) | You want to quiet an entire alert series for a defined period, for example, during a known noisy window for a specific host. Snooze expires automatically at the end of the duration. |
| Deactivate | Per alert | You manually [activated](../alerts/triage-alert-episodes.md) an alert and now want to return it to normal automatic recovery behavior. Deactivating doesn't close the alert. It resumes automatic recovery detection, so the alert closes on its own the next time the rule evaluates as recovered. |
| [Maintenance window](../../alerts/maintenance-windows.md) | All action policies in a space | You want to pause all action policy dispatching in a space for a planned maintenance period. All active action policies stop dispatching; rule evaluation and alert recording continue. Maintenance windows are configured separately from action policies. |

### Snooze scope [snooze-scope]

Snooze applies at the group level (by `group_hash`), not for each individual alert. When you snooze one alert, every alert sharing the same group (all rows with the same `rule_id` and `group_hash`) is silenced for the duration. Snoozing one row in the alerts table silences the entire series for that rule.

:::{note}
Snoozing an alert differs from snoozing an action policy. When you snooze an action policy, the dispatch mechanism is paused and every series the action policy processes is silenced. When you snooze an alert, you target one specific series before action policy matching runs, silencing it regardless of which action policy handles it. Use action policy snooze when you want to pause all workflow invocations from a given action policy, for example, during planned maintenance on a destination system.
:::

## Related pages

- [About action policies](about-action-policies.md): Understand how the eligibility, scope, and frequency gates work after silencing.
- [Create and configure an action policy](create-configure-action-policy.md): Set up the action policies that run after alert silencing checks pass.
- [Triage alerts](../alerts/triage-alert-episodes.md): Acknowledge, snooze, or deactivate alerts from the **Alerts** page.
