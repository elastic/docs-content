---
navigation_title: Alerts
applies_to:
  stack: experimental 9.5+
  serverless: ga
products:
  - id: kibana
description: "Alerts track a problem from first detection through recovery. Alerts belong to a series that groups recurrences of the same condition."
---

# Alerts [alerts]

:::{include} /explore-analyze/alerting/esql/_snippets/v2-system-note.md
:::

{{alerting-v2-system-cap}} tracks each problem as an **alert**: the grouping of [rule events](rules/rule-event-field-reference.md) that share `episode.id`, from first detection through recovery.

## Alert lifecycle states [alert-episode-lifecycle]

Every alert moves through these states:

```
inactive → pending → active → recovering → inactive
```

| State | What it means |
| --- | --- |
| Inactive | Problem fully resolved, or no problem detected yet. After recovery, an action policy can invoke a workflow to send a recovery notification. |
| Pending | Errors detected, but the system is waiting to confirm it's a real problem before the alert becomes active. This keeps a brief spike from opening and immediately closing an alert. |
| Active | Problem confirmed and ongoing. An action policy can evaluate the alert and invoke a workflow. |
| Recovering | Errors have stopped, but the system is waiting to confirm it's truly resolved. This keeps a single good check from closing an alert while the problem might return. |

:::{dropdown} Example: A checkout-latency alert moving through all four states
A checkout-latency rule runs every 5 minutes. It has an activation threshold of 2 consecutive breaches and a recovery threshold of 2 consecutive clears. An action policy matches this rule's alerts and invokes a workflow that notifies on-call when the alert becomes `active` and when it recovers.

1. **14:00**: Routine check. p95 is within budget. No alert yet. The series is `inactive`.
2. **14:05**: p95 jumps to 3.1s. The rule detects the first breach. {{kib}} writes a rule event, opens the alert in `pending`, and starts counting consecutive breaches.
3. **14:10**: p95 is still elevated. The second consecutive breach meets the activation threshold. The alert moves from `pending` to `active`. The action policy invokes the workflow, which pages the engineer.
4. **14:10–14:45**: Every evaluation finds high latency. The alert stays `active`. {{kib}} doesn't open new alerts. One alert tracks one problem, no matter how many times the rule evaluates while the condition holds.
5. **14:50**: p95 drops back under 2s. The first clean check moves the alert from `active` to `recovering`. The system starts counting consecutive clears.
6. **14:55**: A second consecutive clear meets the recovery threshold. The alert moves from `recovering` to `inactive`. The engineer receives a recovery notification.
:::

## Alerts exist within a series [series-overview]

A series is the ongoing relationship between a rule and one specific thing it monitors. It exists for as long as that rule keeps monitoring that thing, and can contain many alerts over its lifetime, one for each time that thing had a problem.

:::{tip}
Snooze operates at the series level, not the alert level. If you snooze `checkout-service`, you're silencing all notifications from that series for the next X hours, regardless of how many new alerts start during that time.
:::

## What to do next with alerts [alerts-next-steps]

- [View and manage alerts](alerts/view-and-manage-alerts.md): Open the alerts table, triage active alerts, and acknowledge, snooze, or resolve them.
- [Rule events](rules/rule-event-field-reference.md): What {{kib}} writes to `.rule-events` and how those events belong to an alert.
- [Query alert history in Discover](alerts/query-alerts-and-signals-in-discover.md): Use {{esql}} to query `.rule-events` and `.alert-actions` for exploratory analysis and dashboards.
