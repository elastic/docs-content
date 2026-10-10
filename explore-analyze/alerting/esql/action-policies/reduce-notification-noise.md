---
navigation_title: Reduce notification noise
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "Silence alert notifications by acknowledging, snoozing, or resolving alerts, or with a maintenance window."
---

# Reduce notification noise [reduce-notification-noise]

{{alerting-v2-system-cap}} has several mechanisms that can silence notifications for an alert. When an alert is silenced, the dispatcher stops processing it before it evaluates any action policy against it. For where this fits in the full dispatch cycle, refer to [About action policies](about-action-policies.md).

## Silencing mechanisms [silencing-mechanisms]

The following mechanisms let you silence notifications, each at a different scope:

| Mechanism | Scope | When to use |
|---|---|---|
| Acknowledge | Per alert | You're actively investigating a breach and want to silence notifications for it without closing the alert. Clear the acknowledgment when you're done to restore notifications. |
| Snooze | Per series (group) | You want to quiet an entire alert series for a defined period, for example, during a known noisy window for a specific host. Snooze expires automatically at the end of the duration. |
| [Resolve](../alerts/triage-alert-episodes.md#close-and-reopen-episodes) | Per alert | You've fixed the underlying problem and want to close the alert without waiting for the rule to detect recovery. Resolving closes the alert and stops its notifications. If the rule's condition still matches on its next run, a new alert starts for the series, and action policies can send notifications for it. |
| [Maintenance window](../../alerts/maintenance-windows.md) | All action policies in a space | You want to pause all action policy dispatching in a space for a planned maintenance period. All active action policies stop dispatching; rule evaluation and alert recording continue. Maintenance windows are configured separately from action policies. |

### Snooze scope [snooze-scope]

Snooze applies at the group level (by `group_hash`), not for each individual alert. When you snooze one alert, every alert sharing the same group (all rows with the same `rule_id` and `group_hash`) is silenced for the duration. Snoozing one row in the alerts table silences the entire series for that rule.

:::{note}
Snoozing an alert differs from snoozing an action policy. When you snooze an action policy, the dispatch mechanism is paused and every series the action policy processes is silenced. When you snooze an alert, you target one specific series before action policy matching runs, silencing it regardless of which action policy handles it. Use action policy snooze when you want to pause all workflow invocations from a given action policy, for example, during planned maintenance on a destination system.
:::

## Related pages

- [About action policies](about-action-policies.md): Understand how the eligibility, scope, and frequency gates work after silencing.
- [Create and configure an action policy](create-configure-action-policy.md): Set up the action policies that run after alert silencing checks pass.
- [Triage alerts](../alerts/triage-alert-episodes.md): Acknowledge, snooze, or resolve alerts from the **Alerts** page.
