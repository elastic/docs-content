---
navigation_title: Alerts
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Alert episodes in Kibana's experimental alerting system track one problem from first detection through recovery. Each episode accumulates the full lifecycle history without overwriting past evaluations."
---

# {{alerting-v2-system-cap}} alerts

Alert episodes are part of the {{alerting-v2-system}} in {{kib}}. When a rule fires repeatedly on the same problem, a flat list of events doesn't tell you when the issue started, whether it's still happening, or how long it's been going on. Alert episodes fill that gap. Each alert episode is a persistent record of one issue on one series, from first breach through recovery, with every evaluation appended to the same history. Nothing is overwritten.

<!--[CONTENT NEEDED for M2: UI. Once the navigation and page name have been confirmed, add instructions for opening the Alerts page.]
-->

## Alert lifecycle [alert-lifecycle]

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

<!-- TODO: Uncomment when PR #6523 (rules) is merged:
Activation and recovery thresholds control how many consecutive evaluations must agree, or how long the condition must persist, before transitioning. Refer to [Configure a rule](rules/configure-a-rule.md#activation-recovery-thresholds) to learn more about these settings.
-->
Activation and recovery thresholds control how many consecutive evaluations must agree, or how long the condition must persist, before transitioning.

### Example: First breach opens, first clear closes

A checkout-latency rule runs in Alert mode every 5 minutes. Latency breaches at 14:05 and clears at 14:50:

1. **14:00** - Routine check. p95 is within budget. The alert episode is `inactive`.
2. **14:05** — p95 jumps to 3.1s. The first breach is detected. With no activation threshold, the alert episode opens immediately as `active`.
3. **14:10–14:45** — Every evaluation finds high latency. The same alert episode stays `active`. No new alert episodes are created.
4. **14:50** — p95 drops back under 2s. With no recovery threshold, the alert episode resolves immediately to `inactive`.

One problem is tracked in one alert episode, even though the rule evaluated many times while the condition was ongoing.

<!-- TODO: Add image once alert-episode-example-without-threshold.png is available in explore-analyze/images/
:::{image} ../../images/alert-episode-example-without-threshold.png
:alt: Timeline of a checkout-latency alert episode without thresholds. At 14:05, p95 jumps to 3.1s and the episode opens immediately as active. It stays active through 14:45. At 14:50, p95 drops back under 2s and the episode resolves immediately as inactive.
:::
-->

### Example: Waiting for confirmation before opening and closing

The same checkout-latency rule, now with an activation threshold of 2 consecutive breaches and a recovery threshold of 2 consecutive clears:

1. **14:00** — Routine check. p95 is within budget. The alert episode is `inactive`.
2. **14:05** — p95 jumps to 3.1s. The first breach is detected. The alert episode is created in `pending` and the system starts counting consecutive breaches.
3. **14:10** — p95 is still elevated. The second consecutive breach meets the activation threshold. The alert episode moves from `pending` to `active`, and the engineer is paged.
4. **14:10–14:45** — Latency stays elevated. The alert episode remains `active`.
5. **14:50** — p95 drops back under 2s. The first clean check moves the alert episode to `recovering`. The system starts counting consecutive clears.
6. **14:55** — A second consecutive clear meets the recovery threshold. The alert episode moves from `recovering` to `inactive`.

Thresholds prevent brief spikes from opening alert episodes and transient dips from closing them prematurely. The alert episode waits in `pending` until the problem is confirmed, and waits in `recovering` until the resolution is confirmed.

<!-- TODO: Add image once alert-episode-example-with-activation-threshold.png is available in explore-analyze/images/
:::{image} ../../images/alert-episode-example-with-activation-threshold.png
:alt: Timeline of a checkout-latency alert episode with activation threshold of 2 and recovery threshold of 2. At 14:05, the first breach puts the episode in pending. At 14:10, the second consecutive breach moves it to active. At 14:50, the first clean check moves it to recovering. At 14:55, the second consecutive clear resolves it to inactive.
:::
-->

## Series

A series is the ongoing relationship between a rule and one specific thing it monitors.

Your rule monitors services. Each service it tracks has its own series, one for `checkout-service`, one for `payment-service`, and so on. A series exists for as long as that rule keeps monitoring that service.

Think of it like a patient's medical file. The file exists as long as the patient is in the system. Individual health incidents come and go, but the file persists.

<!-- TODO: Uncomment when PR #6523 (rules) is merged:
For the fields that identify a series in alert event documents, refer to [Rule event and field reference](rules/rule-event-field-reference.md#rule-reference).
-->

### How series and episodes relate

An alert episode lives inside a series. A series can contain many alert episodes over its lifetime, one for each time that service had a problem.

```
Series: checkout-service
│
├── Episode 1: errors on April 10 (active → inactive)
├── Episode 2: errors on April 15 (active → inactive)
└── Episode 3: errors on April 18 (active right now)
```

The series is the container. Alert episodes are the individual problems that happened within it. When the series breaches again after recovering, a new alert episode starts.

This means you can track "the checkout service was broken from 02:14 to 03:21" and "the payment service was broken at the same time" as separate alert episodes, even when both come from the same rule.

:::{tip}
Snooze operates at the series level, not the alert episode level. If you snooze `checkout-service`, you're silencing all notifications from that series for the next X hours, regardless of how many new alert episodes start during that time. You're quieting a specific ongoing situation, not a single alert episode.
:::

### A practical way to think about it

| Concept | Analogy |
| --- | --- |
| Rule | A security camera watching the building |
| Series | The camera's feed for one specific door |
| Alert episode | A specific incident caught on that feed |
| Rule events | The individual video frames |

The camera runs continuously (rule), always watching door 3 (series). One night someone breaks in. That's an alert episode. The frames captured during the break-in are the rule events.

## Signals versus alerts

Every time a rule finds a match, it writes a document to `.rule-events`. Whether that document is a signal or an alert depends on the rule's mode, and that choice determines whether the system only records what happened or actively tracks it through to resolution.

A **signal** is a one-time observation. The system writes it and moves on, no lifecycle, no notifications, no follow-up. An **alert** (`type: alert`) participates in an alert episode. The system links it to every other document from the same problem, tracks the lifecycle states, and routes notifications through action policies.

| Type | What it is | When it's created |
| --- | --- | --- |
| Signal | A point-in-time record that the query matched (`type: signal`). Stored in `.rule-events`. | Rules in Detect mode |
| Alert | A lifecycle-tracked episode with `type: alert` and `episode.*` fields. Stored in `.rule-events`. | Rules in Alert mode |

A rule in Detect mode only writes signals. It never opens alert episodes, so action policies have nothing to match against.

## Where alerts live

Alert events are stored in `.rule-events`. Triage actions (acknowledge, snooze, resolve) are stored in `.alert-actions`. Both are queryable in Discover.

Every time you take an action on an episode — acknowledging it, snoozing it, resolving it, editing its tags — {{kib}} writes a new document to `.alert-actions`. These documents are append-only and can be queried in Discover for auditing and metrics such as mean time to acknowledge (MTTA).
<!-- TODO: Uncomment after PR #6521 merges and toc.yml in this branch is updated to nest files under kibana-alerting-experimental.md. The anchor exists but can't be indexed until the toc parent chain is complete.
For field definitions, refer to [Alert states and fields reference](alerts/alert-states-and-fields-reference.md#alert-states-reference).
-->

<!--[CONTENT NEEDED for M2: UI. "V2 Alerting Preview" is a development-phase navigation label. Once the navigation and page name have been confirmed, add instructions for opening the Alerts page.]
-->

### Kibana spaces

Alert episodes in the {{alerting-v2-system}} are scoped to the Kibana space in which they were created. Alert episodes from one space are not visible when viewing a different space. This matches how other Kibana features behave across spaces.

### Data stream storage and retention

Both `.rule-events` and `.alert-actions` are data streams, append-only, time-series stores optimized for writes. On every rule evaluation, {{kib}} writes a **new document** to `.rule-events` rather than updating the previous one. Each document is a point-in-time snapshot. The `episode.status` field records the lifecycle state the episode was in at that exact evaluation. Nothing is overwritten.

Because every evaluation produces its own document, you can reconstruct the full history of an episode by querying all documents that share the same `episode.id`.
<!-- TODO: Uncomment after PR #6521 merges and toc.yml in this branch is updated to nest files under kibana-alerting-experimental.md. The anchor exists but can't be indexed until the toc parent chain is complete.
Refer to [Query alerts and signals in Discover](alerts/query-alerts-and-signals-in-discover.md#explore-alerts-discover) for example queries.
-->

Retention is managed automatically through ILM. Older backing indices move through storage tiers and are deleted when the retention window expires. You do not need to manually remove documents. {{kib}} manages versioning, retention, and lifecycle for both streams. Do not change their mappings or index settings.

## Related pages

- **[View and manage alerts](alerts/view-and-manage-alerts.md):** Open the alert episodes table, triage active episodes, and acknowledge, snooze, or resolve them.
- **[Query alerts and signals in Discover](alerts/query-alerts-and-signals-in-discover.md):** Use {{esql}} to query `.rule-events` and `.alert-actions` for ad hoc analysis and dashboards.
- **[Alert states and fields reference](alerts/alert-states-and-fields-reference.md):** Look up lifecycle states, field names, and episode document structure.
<!-- TODO: Uncomment when PR #6525 (workflows/notifications) is merged:
- **[Notifications](notifications.md):** Set up action policies to route alert episodes to the right people and channels.
- **[Notification gating](notifications/notification-gating.md):** Understand how acknowledge, snooze, and deactivate control whether an episode triggers a notification.
-->
