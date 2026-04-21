---
navigation_title: Alerts
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Alert episodes in {{alerting-v2}}: lifecycle states, series and episodes, signals versus alerts, and where to find them."
---

# Alerts

When a rule runs in Alert mode, it maintains alert episodes, ongoing records of an issue from first breach through recovery. This is what you triage on the **Alerts** page.

An episode isn't a single event. It's the full story of one issue on one series. It covers when the condition first triggered, what state it's in right now, and when it recovered. Each rule evaluation appends to that history. Nothing is overwritten.

## Alert lifecycle [alert-lifecycle-v2]

Every alert episode moves through these states:

```
inactive → pending → active → recovering → inactive
```

| State | What it means |
| --- | --- |
| inactive | No breach. The series is healthy and not being tracked. |
| pending | The condition is met, but the rule's activation threshold hasn't been reached yet. This prevents one noisy evaluation from opening an alert. |
| active | The breach is confirmed. The episode is open and actionable. Action policies can route notifications. |
| recovering | The condition has cleared, but the rule's recovery threshold hasn't been met yet. |

Activation and recovery thresholds control how many consecutive evaluations must agree, or how long the condition must persist, before transitioning. Refer to [Configure a rule](rules/configure-a-rule.md#activation-recovery-thresholds-v2) for the settings.

## Series and episodes

When a rule groups by fields (for example `BY host.name`), each unique combination is its own series, identified by `group_hash`. Each series has its own independent lifecycle.

An episode is one lifecycle arc for a series, identified by `episode_id`, from first breach to recovery. When the series breaches again after recovering, a new episode starts.

This lets you track "the checkout service was broken from 02:14 to 03:21" and "the payment service was broken at the same time" as separate episodes, even when both come from the same rule.

## Signals versus alerts

Signals and alerts are two different record types that rules can produce, depending on the rule mode.

| Type | What it is | When it's created |
| --- | --- | --- |
| Signal | A point-in-time record that the query matched (`type: signal`). Stored in `.rule-events`. | Rules in Detect mode |
| Alert | A lifecycle-tracked episode with `type: alert` and `episode.*` fields. Stored in `.rule-events`. | Rules in Alert mode |

A rule in Detect mode only writes signals. It never opens episodes, so action policies have nothing to match against.

## Where alerts live

Alert events are stored in `.rule-events`. Triage actions (acknowledge, snooze, resolve) are stored in `.alert-actions`. Both are queryable in Discover.

The **Alerts** page (**{{manage-app}}** > **Alerts and Insights** > **Rules V2** > **Alerts**) shows the current state of every episode in your space, filterable by rule, status, and tags.

## Where to go next

- [View, manage, and reference alerts](alerts/view-manage-and-reference-alerts.md): Open the alert episodes table, triage active episodes, and acknowledge, snooze, or resolve them.
- [Query alerts and signals in Discover](alerts/query-alerts-and-signals-in-discover.md): Use {{esql}} to query `.rule-events` and `.alert-actions` for ad hoc analysis and dashboards.
- [Alert states and fields reference](alerts/alert-states-and-fields-reference.md): Look up lifecycle states, field names, and episode document structure.
- [Notifications](notifications.md): Set up action policies to route alert episodes to the right people and channels.
