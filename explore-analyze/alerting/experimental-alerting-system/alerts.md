---
navigation_title: Alerts
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Alert episodes in the experimental alerting system track a problem from first detection through recovery. Alert episodes belong to a series that groups recurrences of the same condition."
---

# Alerts in the {{alerting-v2-system-cap}} [alerts]

In the {{alerting-v2-system}}, {{kib}} tracks each problem as an **alert episode**: the grouping of [rule events](rules/rule-event-field-reference.md) that share `episode.id`, from first detection through recovery.

This page explains the core concepts you need to work with the {{alerting-v2-system}}: how alert episodes move through lifecycle states, and how series group alert episodes over time for the same monitored subject.

## Alert episode lifecycle states [alert-episode-lifecycle]

Every alert episode moves through these states:

```
inactive → pending → active → recovering → inactive
```

| State | What it means |
| --- | --- |
| Inactive | Problem fully resolved. An action policy can invoke a workflow to send a recovery notification. |
| Pending | Errors detected, but the system is waiting to confirm it's a real problem before the alert episode becomes active. |
| Active | Problem confirmed and ongoing. An action policy can evaluate the alert episode and invoke a workflow. |
| Recovering | Errors have stopped, but the system is waiting to confirm it's truly resolved. |

:::{dropdown} Example: A checkout-latency alert episode moving through all four states
A checkout-latency rule runs every 5 minutes. It has an activation threshold of 2 consecutive breaches and a recovery threshold of 2 consecutive clears. The alert episode opens only after consecutive breaches meet the activation threshold and closes only after consecutive clears meet the recovery threshold. The system waits for confirmation in both directions. An action policy matches this rule's alert episodes and invokes a workflow that notifies on-call when the alert episode becomes `active` and when it recovers.

1. **14:00**: Routine check. p95 is within budget. No alert episode yet. The series is `inactive`.
2. **14:05**: p95 jumps to 3.1s. The rule detects the first breach. {{kib}} writes a rule event, opens the alert episode in `pending`, and starts counting consecutive breaches.
3. **14:10**: p95 is still elevated. The second consecutive breach meets the activation threshold. The alert episode moves from `pending` to `active`. The action policy invokes the workflow, which pages the engineer.
4. **14:10–14:45**: Every evaluation finds high latency. The alert episode stays `active`. {{kib}} doesn't open new alert episodes. One alert episode tracks one problem, no matter how many times the rule evaluates while the condition holds.
5. **14:50**: p95 drops back under 2s. The first clean check moves the alert episode from `active` to `recovering`. The system starts counting consecutive clears.
6. **14:55**: A second consecutive clear meets the recovery threshold. The alert episode moves from `recovering` to `inactive`. The engineer receives a recovery notification.

**What this illustrates:**

- **`inactive` is the resting state.** The series exists but isn't tracking a problem.
- **`pending` is the confirmation gate on the way in.** Without it, a brief latency spike at 14:05 opens and immediately closes an alert episode, creating noise. The threshold filters that out.
- **`active` is the steady state of an ongoing problem.** The alert episode accumulates evaluations without branching, covering the entire outage from first confirmation to first clear.
- **`recovering` is the confirmation gate on the way out.** Without it, a single good evaluation at 14:50 closes the alert episode, even if latency bounces back up at 14:55. The threshold prevents premature resolution.
- **`inactive` again marks confirmed recovery.** The alert episode closes and the recovery notification fires only after the condition has cleared consistently.
:::

## Alert episodes exist within a series [series-overview]

A series is the ongoing relationship between a rule and one specific thing it monitors. It exists for as long as that rule keeps monitoring that thing, and can contain many alert episodes over its lifetime, one for each time that thing had a problem.

Think of it like a patient's medical file. The file persists as long as the patient is in the system. Individual health incidents come and go, but the file stays. Each incident is an alert episode in the same series.

:::{tip}
Snooze operates at the series level, not the alert episode level. If you snooze `checkout-service`, you're silencing all notifications from that series for the next X hours, regardless of how many new alert episodes start during that time.
:::

## What to do next with alerts [alerts-next-steps]

From here, you can view, manage, and query alert episode data, and query `.rule-events` in Discover.

- [View and manage alerts](alerts/view-and-manage-alerts.md): Open the alert episodes table, triage active alert episodes, and acknowledge, snooze, or resolve them.
- [Rule events](rules/rule-event-field-reference.md): What {{kib}} writes to `.rule-events` and how those events belong to an alert episode.
- [Query {{alerting-v2-system}} alert history in Discover](alerts/query-alerts-and-signals-in-discover.md): Use {{esql}} to query `.rule-events` and `.alert-actions` for exploratory analysis and dashboards.

:::{important} - How to use the {{alerting-v2-system}} documentation
Because the {{alerting-v2-system}} is still evolving, its UI can change before general availability. Rather than pointing to an exact button or menu, the documentation focuses on the underlying concepts and behavior. If something doesn't match what you see in the {{kib}} UI, look for the closest equivalent instead. The concepts and behaviors described in the documentation still apply.
:::
