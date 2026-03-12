---
navigation_title: Schedule and lookback
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Configure how often a Kibana alerting v2 rule runs and how far back it looks when evaluating data."
---

# Kibana alerting v2 schedule and lookback [schedule-lookback-v2]

The schedule and lookback settings control how often a rule runs and how far back it looks when evaluating data.

## Execution interval

The execution interval (`schedule.every`) determines how frequently the rule evaluates. Set this based on how quickly you need to detect conditions:

| Interval | Use case |
|---|---|
| `1m` | Critical infrastructure metrics that need near-real-time detection |
| `5m` | Standard application monitoring |
| `15m` | Trend-based alerting or cost-sensitive monitoring |
| `1h` | Daily digest or low-priority checks |

The rule executor runs on each interval via Task Manager. If a rule evaluation takes longer than the interval, the next execution starts as soon as the previous one completes.

## Lookback window

The lookback window (`schedule.lookback`) determines the time range that the ES|QL query covers. The system applies a time filter to your query:

```
WHERE @timestamp > NOW() - <lookback>
```

Choose a lookback window that is at least as long as the execution interval to avoid gaps in coverage. Common patterns:

| Execution interval | Lookback window | Coverage |
|---|---|---|
| `1m` | `5m` | Overlapping — each evaluation covers the last 5 minutes |
| `5m` | `5m` | Contiguous — each evaluation covers exactly the preceding interval |
| `5m` | `15m` | Overlapping — useful for aggregations that need more data points |

### When to use a longer lookback

- **No-data detection**: Use a lookback of several hours (for example, `12h`) so the query can find the last data point from a host that stopped reporting.
- **SLO burn rate**: Use multiple time windows within the query to compare short-term and long-term error rates.
- **Change detection**: Use a lookback long enough to establish a baseline period for comparison.

### Performance considerations

Longer lookback windows query more data and may take longer to execute. If query performance is a concern:

- Use `STATS` aggregations to reduce the volume of data processed.
- Avoid `WHERE` filters on high-cardinality fields without aggregation.
- Consider increasing the execution interval to reduce overall query load.

## Time field

By default, rules use `@timestamp` as the time field for the lookback filter. If your data uses a different time field, set the `time_field` property in the rule definition:

```yaml
time_field: "event.created"
```
