---
navigation_title: Alerts
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Alert episodes in {{alerting-v2}}: lifecycle states, series and episodes, signals versus alerts, and where to find them."
---

# Alerts

When a rule runs in Alert mode, it maintains _alert episodes_, which are ongoing records of an issue from first breach through recovery. This is what you triage on the **Alerts** page.

An episode isn't a single event. It's the full story of one issue on one series. It covers when the condition first triggered, what state it's in right now, and when it recovered. Each rule evaluation appends to that history. Nothing is overwritten.

## Alert lifecycle [alert-lifecycle-v2]

Every alert episode moves through these states:

```
inactive → pending → active → recovering → inactive
```

| State | What it means |
| --- | --- |
| Inactive | Problem fully resolved. You get a recovery notification. |
| Pending | Errors detected, but the system is waiting to confirm it's a real problem before fully alerting. |
| Active | Problem confirmed and ongoing. This is when you get notified. |
| Recovering | Errors have stopped, but the system is waiting to confirm it's truly resolved. |

Activation and recovery thresholds control how many consecutive evaluations must agree, or how long the condition must persist, before transitioning. Refer to [Configure a rule](rules/configure-a-rule-v2.md#activation-recovery-thresholds-v2) to learn more about these settings.

### Alert episode example

Suppose a service starts throwing errors at 10:00am and stops at 10:45am. Your rule runs in Alert mode every 5 seconds. Here's how one episode covers the entire incident, from detection to resolution:

1. **10:00am** - The rule detects errors. A new episode is created. With no activation threshold configured, it moves immediately from `pending` to `active`.
2. **10:00am–10:45am** - The rule continues detecting errors on every run. The **same episode** stays `active`. No new episodes are created.
3. **10:45am** - Errors stop. The episode moves to `recovering`. Without a recovery threshold, it transitions immediately to `inactive`.

One problem is tracked in one episode, even though the rule ran hundreds of times while the condition was ongoing.

## Series

A series is the ongoing relationship between a rule and one specific thing it monitors.

Your rule monitors services. Each service it tracks has its own series, one for `checkout-service`, one for `payment-service`, and so on. A series exists for as long as that rule keeps monitoring that service.

Think of it like a patient's medical file. The file exists as long as the patient is in the system. Individual health incidents come and go, but the file persists.

### How series and episodes relate

An episode lives inside a series. A series can contain many episodes over its lifetime, one for each time that service had a problem.

```
Series: checkout-service
│
├── Episode 1: errors on April 10 (active → inactive)
├── Episode 2: errors on April 15 (active → inactive)
└── Episode 3: errors on April 18 (active right now)
```

The series is the container. Episodes are the individual problems that happened within it. When the series breaches again after recovering, a new episode starts.

This means you can track "the checkout service was broken from 02:14 to 03:21" and "the payment service was broken at the same time" as separate episodes, even when both come from the same rule.

:::{tip}
Snooze operates at the series level, not the episode level. If you snooze `checkout-service`, you're saying "stop notifying me about anything from this service for the next X hours", regardless of how many new episodes start during that time. You're silencing a specific ongoing situation, not just one alert.
:::

### A practical way to think about it

| Concept | Analogy |
| --- | --- |
| Rule | A security camera watching the building |
| Series | The camera's feed for one specific door |
| Episode | A specific incident caught on that feed |
| Rule events | The individual video frames |

The camera runs continuously (rule), always watching door 3 (series). One night someone breaks in. That's an episode. The frames captured during the break-in are the rule events.

## Signals versus alerts

Every time a rule finds a match, it writes a document to `.rule-events`. Whether that document is a signal or an alert depends on the rule's mode — and that choice determines whether the system just records what happened or actively tracks it through to resolution.

A **signal** is a one-time observation. The system writes it and moves on — no lifecycle, no notifications, no follow-up. A **alert** participates in an episode. The system links it to every other document from the same problem, tracks the lifecycle states, and routes notifications through action policies.

| Type | What it is | When it's created |
| --- | --- | --- |
| Signal | A point-in-time record that the query matched (`type: signal`). Stored in `.rule-events`. | Rules in Detect mode |
| Alert | A lifecycle-tracked episode with `type: alert` and `episode.*` fields. Stored in `.rule-events`. | Rules in Alert mode |

A rule in Detect mode only writes signals. It never opens episodes, so action policies have nothing to match against.

## Where alerts live

Alert events are stored in `.rule-events`. Triage actions (acknowledge, snooze, resolve) are stored in `.alert-actions`. Both are queryable in Discover.

The **Alerts** page (**{{manage-app}} > V2 Alerting Preview > Alerts**) shows the current state of every episode in your space, filterable by rule, status, and tags.

### Data stream storage and retention

Both `.rule-events` and `.alert-actions` are data streams, append-only, time-series stores optimized for writes. On every rule evaluation, {{kib}} writes a **new document** to `.rule-events` rather than updating the previous one. Each document is a point-in-time snapshot. The `episode.status` field records the lifecycle state the episode was in at that exact evaluation. Nothing is overwritten.

Because every evaluation produces its own document, you can reconstruct the full history of an episode by querying all documents that share the same `episode.id`. Refer to [Query alerts and signals in Discover](alerts/query-alerts-and-signals-in-discover-v2.md#explore-alerts-discover-v2) for example queries.

Retention is managed automatically through ILM. Older backing indices move through storage tiers and are deleted when the retention window expires. You do not need to manually remove documents. {{kib}} manages versioning, retention, and lifecycle for both streams. Do not change their mappings or index settings.

## Where to go next

- [View, manage, and reference alerts](alerts/view-manage-and-reference-alerts-v2.md): Open the alert episodes table, triage active episodes, and acknowledge, snooze, or resolve them.
- [Query alerts and signals in Discover](alerts/query-alerts-and-signals-in-discover-v2.md): Use {{esql}} to query `.rule-events` and `.alert-actions` for ad hoc analysis and dashboards.
- [Alert states and fields reference](alerts/alert-states-and-fields-reference-v2.md): Look up lifecycle states, field names, and episode document structure.
- [Notifications](notifications-v2.md): Set up action policies to route alert episodes to the right people and channels.
