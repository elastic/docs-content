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

This page explains the core concepts you need to work with {{alerting-v2-system}}: how alerts move through lifecycle states, and how series group alerts over time for the same monitored subject.

## Alert lifecycle states [alert-episode-lifecycle]

Every alert moves through these states:

```
inactive → pending → active → recovering → inactive
```

| State | What it means |
| --- | --- |
| Inactive | Problem fully resolved. An action policy can invoke a workflow to send a recovery notification. |
| Pending | Errors detected, but the system is waiting to confirm it's a real problem before the alert becomes active. |
| Active | Problem confirmed and ongoing. An action policy can evaluate the alert and invoke a workflow. |
| Recovering | Errors have stopped, but the system is waiting to confirm it's truly resolved. |

:::{dropdown} Example: A checkout-latency alert moving through all four states
A checkout-latency rule runs every 5 minutes. It has an activation threshold of 2 consecutive breaches and a recovery threshold of 2 consecutive clears. The alert opens only after consecutive breaches meet the activation threshold and closes only after consecutive clears meet the recovery threshold. The system waits for confirmation in both directions. An action policy matches this rule's alerts and invokes a workflow that notifies on-call when the alert becomes `active` and when it recovers.

1. **14:00**: Routine check. p95 is within budget. No alert yet. The series is `inactive`.
2. **14:05**: p95 jumps to 3.1s. The rule detects the first breach. {{kib}} writes a rule event, opens the alert in `pending`, and starts counting consecutive breaches.
3. **14:10**: p95 is still elevated. The second consecutive breach meets the activation threshold. The alert moves from `pending` to `active`. The action policy invokes the workflow, which pages the engineer.
4. **14:10–14:45**: Every evaluation finds high latency. The alert stays `active`. {{kib}} doesn't open new alerts. One alert tracks one problem, no matter how many times the rule evaluates while the condition holds.
5. **14:50**: p95 drops back under 2s. The first clean check moves the alert from `active` to `recovering`. The system starts counting consecutive clears.
6. **14:55**: A second consecutive clear meets the recovery threshold. The alert moves from `recovering` to `inactive`. The engineer receives a recovery notification.

**What this illustrates:**

- **`inactive` is the resting state.** The series exists but isn't tracking a problem.
- **`pending` is the confirmation gate on the way in.** Without it, a brief latency spike at 14:05 opens and immediately closes an alert, creating noise. The threshold filters that out.
- **`active` is the steady state of an ongoing problem.** The alert accumulates evaluations without branching, covering the entire outage from first confirmation to first clear.
- **`recovering` is the confirmation gate on the way out.** Without it, a single good evaluation at 14:50 closes the alert, even if latency bounces back up at 14:55. The threshold prevents premature resolution.
- **`inactive` again marks confirmed recovery.** The alert closes and the recovery notification fires only after the condition has cleared consistently.
:::

## Alerts exist within a series [series-overview]

A series is the ongoing relationship between a rule and one specific thing it monitors. It exists for as long as that rule keeps monitoring that thing, and can contain many alerts over its lifetime, one for each time that thing had a problem.

Think of it like a patient's medical file. The file persists as long as the patient is in the system. Individual health incidents come and go, but the file stays. Each incident is an alert in the same series.

:::{tip}
Snooze operates at the series level, not the alert level. If you snooze `checkout-service`, you're silencing all notifications from that series for the next X hours, regardless of how many new alerts start during that time.
:::

## What to do next with alerts [alerts-next-steps]

From here, you can view, manage, and query alert data, and query `.rule-events` in Discover.

- [View and manage alerts](alerts/view-and-manage-alerts.md): Open the alerts table, triage active alerts, and acknowledge, snooze, or resolve them.
- [Rule events](rules/rule-event-field-reference.md): What {{kib}} writes to `.rule-events` and how those events belong to an alert.
- [Query alert history in Discover](alerts/query-alerts-and-signals-in-discover.md): Use {{esql}} to query `.rule-events` and `.alert-actions` for exploratory analysis and dashboards.
