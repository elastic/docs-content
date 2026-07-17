---
navigation_title: Threshold queries
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Write ES|QL threshold queries for rules in Kibana's experimental alerting system. Covers single-series and grouped rules using STATS aggregation."
---

# Threshold queries in the {{alerting-v2-system}} [esql-threshold-queries]

A threshold query aggregates your data first, then applies an alert condition to the result. Use this pattern when a single matching event isn't enough to warrant an alert. You want to know whether a metric (count, rate, average) has crossed a limit over a time window.

This page covers two variants: a single-series threshold that produces one result for all your data, and a grouped threshold that tracks each subject (host, service, user) independently.

## Single-series threshold

This query counts HTTP 5xx responses and error rates over the lookback window and alerts when the error rate for any service exceeds 10%.

```esql
FROM logs-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend  // Scope to the rule's configured lookback window
| STATS
    error_count = COUNT_IF(http.response.status_code >= 500),  // Count only error responses
    total_count = COUNT(*)                                     // Count all requests for the denominator
  BY service.name
| EVAL error_rate = error_count / total_count  // Compute error rate as a fraction (0–1)
| WHERE error_rate > 0.10                      // Alert condition: services above 10% error rate are breaches
| KEEP service.name, error_rate, error_count, total_count
```

One window, one aggregate per service, one threshold check. The result is either a breach or no breach for each service.

## Grouped threshold

Adding `BY` to the `STATS` command splits the result into one row per unique field value. Each row is evaluated independently against the alert condition, and each breach creates its own alert series.

This query tracks average CPU usage per host and alerts when any host exceeds 90%:

```esql
FROM metrics-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS avg_cpu = AVG(system.cpu.total.pct) BY host.name  // One result row per host
| WHERE avg_cpu > 0.90                                    // Each host above the threshold is a breach
| KEEP host.name, avg_cpu
```

Without the `BY host.name` clause, the query would produce a single average across all hosts combined. A cluster-wide spike might push the average above the threshold even if no single host is the problem. Grouping by host gives each host its own alert episode with its own lifecycle. If host A recovers but host B stays critical, those are tracked separately.

The `BY` fields you use here must match the grouping configuration in the rule. Refer to [Rule grouping](configure-rule-grouping.md) for how to align them.

## More detection patterns [esql-threshold-queries-next-steps]

If both of these patterns don't fit your use case, the next pages cover more specific detection problems:

- [No-data detection](esql-no-data-detection.md): when a host or source stops reporting entirely
- [SLO burn rate](esql-slo-burn-rate.md): when you need to check error budget consumption across multiple time windows
- [Persistent breach detection](esql-persistent-breach.md): when you only want to alert if a condition has been continuously true
