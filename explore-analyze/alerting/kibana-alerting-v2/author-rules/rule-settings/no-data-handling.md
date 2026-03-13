---
navigation_title: No-data handling
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Configure Kibana alerting v2 rule behavior when the query returns no results: record no-data, carry forward status, or treat as recovery."
---

# Kibana alerting v2 no-data handling [no-data-handling-v2]

No-data handling controls what happens when a rule executes and the base query returns no results. This is important because the absence of data is ambiguous — it could mean the source stopped reporting (a problem) or the condition is no longer met (recovery).

## How no-data detection works

No-data detection relies on the split between the base query and the alert condition:

1. The rule executor runs `evaluation.query.base` without the alert condition.
2. If the base query returns results but the alert condition filters them all out, the status is `recovered` (data exists, condition not met).
3. If the base query returns no results at all, the status is `no_data`.

This is why `evaluation.query.condition` is required when `no_data` is configured. Without a separate condition, the system cannot distinguish between "no data" and "condition not met."

## Behaviors

Configure the `no_data.behavior` field to control what happens when no data is detected:

### `no_data` (default)

Write a no-data event to the alert events data stream. The event has `status: no_data`. The alert does not recover and does not activate — it stays in a no-data state until data resumes.

Use this when missing data is itself a condition you want to track and investigate.

### `last_status`

Carry forward the previous status. If the alert was `active`, it stays `active`. If it was `inactive`, it stays `inactive`. No new event is written.

Use this when data gaps are expected (for example, batch ingestion) and you do not want them to affect alert state.

### `recover`

Treat the absence of data as recovery. If the alert was `active`, it transitions to `recovering`. This is the simplest behavior but can cause false recoveries if data stops arriving due to an ingestion problem rather than a genuine resolution.

## Timeframe

The `no_data.timeframe` field sets how long to wait before declaring no-data. The rule must see no results for this duration before the no-data behavior activates:

```yaml
no_data:
  behavior: no_data
  timeframe: 15m
```

## Example: host-specific no-data detection

Detect when a specific host stops reporting, with a lookback window long enough to see the host's last data point:

```yaml
evaluation:
  query:
    base: |
      FROM metrics-*
      | STATS last_seen = MAX(@timestamp) BY host.name
    condition: "WHERE last_seen < NOW() - 15 MINUTES"

schedule:
  every: 5m
  lookback: 12h

no_data:
  behavior: no_data
  timeframe: 15m

grouping:
  fields: [host.name]
```

## Example: combined metric and no-data rule

A single rule that alerts on high CPU and detects missing hosts:

```esql
FROM metrics-*
| WHERE @timestamp >= NOW() - 12 HOURS
| STATS
    last_seen = MAX(@timestamp),
    avg_cpu = AVG(system.cpu.system.pct) WHERE @timestamp >= NOW() - 15 MINUTES
  BY host.name
| EVAL avg_cpu = avg_cpu * 100
| EVAL status = CASE(
    last_seen < NOW() - 15 MINUTES, "no data",
    avg_cpu > 90, "alert",
    "ok"
  )
| WHERE status IN ("alert", "no data")
| KEEP host.name, avg_cpu, status
```
