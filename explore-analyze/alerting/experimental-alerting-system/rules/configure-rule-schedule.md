---
navigation_title: Schedule and lookback
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How the execution interval and lookback window control when a rule evaluates and how much data it covers each time in the experimental alerting system."
---

# Schedule and lookback in the {{alerting-v2-system}} [schedule-lookback]

Schedule and lookback are required settings for rules in the {{alerting-v2-system}}. They control how often a rule runs and how far back it looks when evaluating data. This page describes both fields, lists the accepted values and bounds, and includes guidance on choosing appropriate values for different monitoring scenarios.

Both fields accept duration strings such as `30s`, `5m`, `2h`, or `7d`. Refer to [Duration format](yaml-rule-schema-reference.md#duration-format) for supported units.

## Execution interval [schedule-execution-interval]

The execution interval (`schedule.every`) determines how frequently the rule evaluates. The minimum is `5s` and the maximum is `365d`. Values outside that range are rejected.

## Lookback window [schedule-lookback-window]

The lookback window (`schedule.lookback`) determines the time range that the {{esql}} query covers. The minimum is `5s` and the maximum is `365d`.

If the lookback is shorter than the execution interval, evaluations can miss data between runs. Use a lookback at least as long as the execution interval unless you have a deliberate reason not to.

## When to use a short or long interval and lookback [schedule-when-to-use]

Use a short execution interval (seconds to a few minutes) when:

* The condition being monitored can develop quickly and fast detection is critical. Examples include a burst of failed authentication attempts or a spike in HTTP error rate.
* Notification latency matters and you need the rule to fire close to when the breach occurs.

Use a longer execution interval (tens of minutes or more) when:

* The condition develops slowly and near-real-time detection isn't required. Examples include disk utilization for capacity planning or a weekly job failure check.
* You want to reduce evaluation cost. Longer intervals lower the frequency of query execution against your data.

Use a short lookback window when:

* Your data arrives reliably and with low latency, and you want to avoid re-scanning data that older evaluations already covered.
* You are running high-frequency rules where a narrow window keeps each evaluation focused on recent data.

Use a longer lookback window when:

* The condition you're detecting can develop across multiple events spread over time, and a narrow window might miss the full picture.
* You are setting up a new rule and want to verify the query covers the expected data before tightening the window.
* Ingestion lag means events arrive later than their timestamps, and a wider window ensures late-arriving data is still evaluated.

Avoid setting the lookback shorter than the execution interval. If the lookback doesn't cover the full gap between evaluations, events that arrive between runs can be missed.

## Examples [schedule-examples]

### High-frequency security rule

Create a rule that detects a burst of failed login attempts. Because the threat can develop quickly and needs fast detection, the interval is set to **1 minute** and the lookback to **5 minutes**. The 5-minute lookback is five times the interval, so a burst that straddles two evaluation windows is never missed.

```esql
FROM logs-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend  // Covers the 5-minute lookback on each evaluation
| STATS failed_logins = COUNT_IF(event.outcome == "failure") BY user.name
| WHERE failed_logins > 10
| KEEP user.name, failed_logins
```

The `?_tstart` and `?_tend` parameters are automatically bound to the lookback window, so the query always covers exactly the configured 5-minute range.

### Cost-optimized infrastructure rule

Create a rule that monitors disk utilization for capacity planning. Fast response isn't critical, so the interval is set to **15 minutes** and the lookback to **30 minutes**. The wider window smooths out brief spikes that don't indicate a real capacity problem, reducing evaluation cost without sacrificing coverage.

```esql
FROM metrics-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend  // Covers the 30-minute lookback on each evaluation
| STATS max_disk_pct = MAX(system.filesystem.used.pct) BY host.name, system.filesystem.mount_point
| WHERE max_disk_pct > 0.90
| KEEP host.name, system.filesystem.mount_point, max_disk_pct
```
