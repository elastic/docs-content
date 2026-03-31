---
navigation_title: Rule types
applies_to:
  serverless: preview
products:
  - id: kibana
description: "ES|QL query patterns for Kibana alerting v2 rules: threshold, change detection, ratio, no-data, event rate, percentile, SLO burn rate, and more."
---

# Kibana alerting v2 rule types [rule-types-v2]

Rule types are lightweight abstractions that map UI controls to parameterized ES|QL queries. Each rule type represents a common alerting pattern. When you select a rule type in the UI, it generates the corresponding ES|QL query with your parameters filled in.

Advanced users can bypass rule types entirely and write raw ES|QL for full flexibility.

## Threshold

Alert when a metric crosses a static value. The most common pattern for resource monitoring.

```esql
FROM metrics-*
| STATS avg_cpu = AVG(system.cpu.total.pct) BY host.name
| WHERE avg_cpu > 0.9
| KEEP host.name, avg_cpu
```

## Change detection

Alert when a value deviates from a previous period.

```esql
FROM metrics-*
| STATS
    current_cpu = AVG(system.cpu.total.pct) WHERE @timestamp >= NOW() - 15 MINUTES,
    baseline_cpu = AVG(system.cpu.total.pct) WHERE @timestamp < NOW() - 15 MINUTES
  BY host.name
| EVAL change_pct = ((current_cpu - baseline_cpu) / baseline_cpu) * 100
| WHERE ABS(change_pct) > 10
| KEEP host.name, current_cpu, baseline_cpu, change_pct
```

## Ratio

Alert when a ratio crosses a threshold. Common for error rate monitoring.

```esql
FROM logs-*
| STATS
    errors = COUNT(*) WHERE http.response.status_code >= 500,
    total = COUNT(*)
  BY service.name
| EVAL error_rate = errors / total
| WHERE error_rate > 0.1
| KEEP service.name, error_rate, errors, total
```

## No-data

Alert when a previously reporting source stops sending data.

```esql
FROM metrics-*
| STATS last_seen = MAX(@timestamp) BY host.name
| WHERE last_seen < NOW() - 15 MINUTES
| EVAL status = "no data"
| KEEP host.name, status
```

## Event rate

Alert on the rate of events per time unit.

```esql
FROM logs-*
| STATS event_count = COUNT(*) BY host.name
| WHERE event_count > 1000
| KEEP host.name, event_count
```

## Percentile

Alert when a percentile value exceeds a threshold.

```esql
FROM traces-apm-*
| STATS p95_duration = PERCENTILE(transaction.duration.us, 95) BY service.name
| WHERE p95_duration > 5000000
| EVAL p95_ms = p95_duration / 1000
| KEEP service.name, p95_ms
```

## SLO burn rate

Alert when an SLO error budget is burning too fast.

```esql
FROM traces-apm-*
| STATS
    short_errors = COUNT(*) WHERE @timestamp >= NOW() - 5 MINUTES AND http.response.status_code >= 500,
    short_total = COUNT(*) WHERE @timestamp >= NOW() - 5 MINUTES,
    long_errors = COUNT(*) WHERE @timestamp >= NOW() - 1 HOUR AND http.response.status_code >= 500,
    long_total = COUNT(*) WHERE @timestamp >= NOW() - 1 HOUR
  BY service.name
| EVAL
    short_error_rate = short_errors / short_total,
    long_error_rate = long_errors / long_total,
    slo_target = 0.999,
    short_burn = short_error_rate / (1 - slo_target),
    long_burn = long_error_rate / (1 - slo_target)
| WHERE short_burn > 14.4 AND long_burn > 14.4
| KEEP service.name, short_burn, long_burn
```

## Text search

Alert on specific patterns in log messages.

```esql
FROM logs-*
| WHERE message LIKE "*OutOfMemoryError*"
| STATS error_count = COUNT(*) BY host.name
| WHERE error_count > 0
| KEEP host.name, error_count
```

## Raw ES|QL

For any pattern not covered by a rule type, write raw ES|QL directly. The query can use any ES|QL command, including `ENRICH`, `DISSECT`, `GROK`, `MV_EXPAND`, and cross-cluster search.
