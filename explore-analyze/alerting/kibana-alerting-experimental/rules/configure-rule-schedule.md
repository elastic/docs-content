---
navigation_title: Schedule and lookback
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Configure the execution schedule and lookback window for rules in Kibana's experimental alerting system."
---

# Schedule and lookback in the {{alerting-v2-system}} [schedule-lookback]

The schedule and lookback settings control how often a rule runs and how far back it looks when evaluating data.

Both fields accept duration strings such as `30s`, `5m`, `2h`, or `7d`. Refer to [Duration format](yaml-rule-schema-reference.md#duration-format) for supported units.

## Execution interval

The execution interval (`schedule.every`) determines how frequently the rule evaluates. The minimum is `5s` and the maximum is `365d`. Values outside that range are rejected.

## Lookback window

The lookback window (`schedule.lookback`) determines the time range that the {{esql}} query covers. The minimum is `5s` and the maximum is `365d`.

If the lookback is shorter than the execution interval, evaluations can miss data between runs. Use a lookback at least as long as the execution interval unless you have a deliberate reason not to.

## Examples

### High-frequency security rule

This rule detects a burst of failed login attempts. Because the threat can develop quickly and needs fast detection, the interval is set to **1 minute** and the lookback to **5 minutes**. The 5-minute lookback is five times the interval, so a burst that straddles two evaluation windows is never missed.

```esql
FROM logs-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend  // Covers the 5-minute lookback on each evaluation
| STATS failed_logins = COUNT_IF(event.outcome == "failure") BY user.name
| WHERE failed_logins > 10
| KEEP user.name, failed_logins
```

The `?_tstart` and `?_tend` parameters are automatically bound to the lookback window, so the query always covers exactly the configured 5-minute range.

### Cost-optimized infrastructure rule

This rule monitors disk utilization for capacity planning. Fast response isn't critical, so the interval is set to **15 minutes** and the lookback to **30 minutes**. The wider window smooths out brief spikes that don't indicate a real capacity problem, reducing evaluation cost without sacrificing coverage.

```esql
FROM metrics-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend  // Covers the 30-minute lookback on each evaluation
| STATS max_disk_pct = MAX(system.filesystem.used.pct) BY host.name, system.filesystem.mount_point
| WHERE max_disk_pct > 0.90
| KEEP host.name, system.filesystem.mount_point, max_disk_pct
```
