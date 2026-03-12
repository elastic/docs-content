---
navigation_title: Snooze and disable rules
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Temporarily suppress notifications with per-series snooze or stop rule execution by disabling a Kibana alerting v2 rule."
---

# Snooze and disable Kibana alerting v2 rules [snooze-disable-rules-v2]

You can temporarily suppress notifications or stop rule execution entirely. Kibana alerting v2 provides granular control at the rule and series level.

## Disable a rule

Disabling a rule stops it from executing. No queries run, no events are written, and no notifications are sent.

To disable a rule:

1. Navigate to the rules list.
2. Click the actions menu on the rule row.
3. Select **Disable**.

To re-enable, select **Enable** from the same menu. Bulk enable/disable is also available.

When you re-enable a rule, it resumes execution on the next scheduled interval. Any active episodes from before the disable continue their lifecycle from where they left off.

## Snooze notifications

Snoozing suppresses notifications for a rule's alerts without stopping the rule from executing. The rule continues to evaluate data and produce alert events, but no notifications are sent through notification policies for the snoozed scope.

### Per-series snooze

In Kibana alerting v2, snooze operates per series (a specific rule and group key combination), not per rule. This means you can snooze notifications for a specific host or service without silencing alerts from other hosts monitored by the same rule.

For example, if a rule groups by `host.name`, you can snooze `host-a` while continuing to receive notifications for `host-b` and `host-c`.

To snooze a series:

1. Open the alert inbox or rule details.
2. Find the alert for the series you want to snooze.
3. Click **Snooze** and select a duration.

### Snooze durations

Snooze supports:

- Fixed durations: 3 minutes, 1 hour, 8 hours, 1 day, 1 week.
- Custom duration: specify any number of minutes, hours, or days.
- Snooze until: set a specific date and time.

Snooze auto-expires. After the duration passes, notifications resume automatically.

### What happens during snooze

- The rule continues running and producing alert events.
- Alert lifecycle tracking continues (pending, active, recovering transitions still occur).
- The dispatcher records suppressed outcomes with reason `snooze` instead of dispatching to workflows.
- After snooze expires, any active alerts that would trigger notifications begin doing so on the next dispatcher run.

## Disable vs. snooze

| Action | Rule executes | Events written | Notifications sent |
|---|---|---|---|
| **Enabled** | Yes | Yes | Yes |
| **Snoozed** | Yes | Yes | No (for snoozed scope) |
| **Disabled** | No | No | No |

Choose **snooze** when you want to continue monitoring and recording data but suppress noise (for example, during a known deployment). Choose **disable** when you want to stop all activity for the rule.
