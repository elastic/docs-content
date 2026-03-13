---
navigation_title: Explore alerts and signals in Discover
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Query Kibana alerting v2 alert events in Discover using ES|QL for trend analysis, operational reporting, and ad hoc investigation."
---

# Explore Kibana alerting v2 alerts and signals in Discover [explore-alerts-discover-v2]

Because Kibana alerting v2 alert events are stored as queryable data in standard {{es}} indices, you can explore them in Discover using ES|QL. This enables trend analysis, operational reporting, and ad hoc investigation that goes beyond what the alert inbox provides.

## Query alert events

Open Discover, switch to ES|QL mode, and query the `.alerts-events-*` data stream:

```esql
FROM .alerts-events-*
| WHERE @timestamp > NOW() - 24 HOURS
| STATS alert_count = COUNT(*) BY rule.id, status
| SORT alert_count DESC
```

## Common queries

### Active alerts by rule

```esql
FROM .alerts-events-*
| WHERE @timestamp > NOW() - 1 HOUR AND episode.status == "active"
| STATS active_count = COUNT(*) BY rule.id
| SORT active_count DESC
```

### Alert volume over time

```esql
FROM .alerts-events-*
| WHERE @timestamp > NOW() - 7 DAYS AND status == "breached"
| EVAL hour = DATE_TRUNC(1 HOUR, @timestamp)
| STATS alerts = COUNT(*) BY hour
| SORT hour
```

### Mean time to acknowledge

```esql
FROM .alerts-actions
| WHERE action == "ack"
| STATS avg_ack_time = AVG(duration_to_ack_ms) BY rule_id
| SORT avg_ack_time DESC
```

### Alerts by service and severity

```esql
FROM .alerts-events-*
| WHERE @timestamp > NOW() - 24 HOURS AND status == "breached"
| STATS alert_count = COUNT(*) BY data.service, data.severity
| SORT alert_count DESC
```

### Recovery trends

```esql
FROM .alerts-events-*
| WHERE @timestamp > NOW() - 7 DAYS AND status == "recovered"
| EVAL day = DATE_TRUNC(1 DAY, @timestamp)
| STATS recoveries = COUNT(*) BY day
| SORT day
```

## Build dashboards

Use alert event data to build operational dashboards:

- **Alert volume dashboard** — total alerts, alert rate, alerts by rule, alerts by severity.
- **MTTR dashboard** — mean time to acknowledge and mean time to resolve by rule, service, or team.
- **Top firing rules** — rules producing the most alerts, helping identify noisy rules for tuning.
- **Service health** — alert status by service for a real-time service health overview.

Create visualizations from ES|QL queries in Discover and pin them to dashboards for ongoing visibility.

## Navigate from the alert inbox

You can open Discover directly from the alert inbox or rule details:

- **From the alert inbox** — click **View alert events in Discover** on any alert to open Discover with a query pre-filtered to that alert's events.
- **From rule details** — click **Explore alert events in Discover** to open Discover with the rule's base query pre-populated and a 15-minute time range.

## Signals vs. alerts in Discover

Both signal events (`type: signal`) and alert events (`type: alert`) are stored in the same `.alerts-events-*` data stream. Filter by `type` to work with one or the other:

```esql
FROM .alerts-events-*
| WHERE type == "signal" AND @timestamp > NOW() - 1 HOUR
```

Signal events do not have `episode.*` fields. Alert events include `episode.id`, `episode.status`, and `episode.status_count`.
