---
navigation_title: Rule grouping
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Split Kibana alerting v2 alert event generation by fields like host or service so each entity has independent lifecycle tracking."
---

# Kibana alerting v2 rule grouping [rule-grouping-v2]

Grouping splits alert event generation by one or more fields so that each unique combination of field values produces its own alert series. Each series has independent lifecycle tracking, recovery detection, and per-series snooze.

## How grouping works

When you define grouping fields, the system computes a `group_hash` from the combination of `rule_id` and the values of the grouping fields. This hash uniquely identifies each series.

For example, if you group by `host.name` and three hosts are breaching, the rule produces three separate alert series — one per host. Each series transitions through its own lifecycle independently:

- Host A might be `active` while Host B is `pending`.
- Snoozing Host A does not affect notifications for Host B.
- Host C can recover without affecting the other two.

## Configure grouping

In YAML:

```yaml
grouping:
  fields: [host.name]
```

For multi-field grouping:

```yaml
grouping:
  fields: [host.name, service.name]
```

The grouping fields must correspond to the `BY` clause in your ES|QL query's `STATS` command:

```esql
FROM metrics-*
| STATS avg_cpu = AVG(system.cpu.total.pct) BY host.name, service.name
| WHERE avg_cpu > 0.9
| KEEP host.name, service.name, avg_cpu
```

## No grouping

If no grouping fields are set, the rule produces a single alert series for all results. This is appropriate for aggregate-level monitoring where you do not need per-entity tracking.

## Grouping and recovery

Recovery detection depends on grouping. The rule executor compares group hashes between consecutive evaluations:

- Groups present in the previous evaluation but absent in the current one → `status: recovered`.
- Groups present in both evaluations → lifecycle continues.
- New groups → new episode begins.

This means recovery is automatic: when a host stops breaching, its group hash disappears from the query results, and the system detects recovery.

## Grouping and notification policies

Grouping also affects notification policies. Notification policies have their own `group_by` setting that controls how alerts are batched into notifications:

- **Rule grouping** determines which alert series are created (for example, per `host.name`).
- **Policy grouping** determines how those series are batched into notifications (for example, batch all alerts for the same `host.name` into a single notification).

Notification policy grouping is always scoped per rule — episodes from different rules are never grouped into the same notification.

## Missing values

If a grouping field is missing from some rows, those rows are grouped into a `null` bucket. The null bucket is a valid series with its own lifecycle.
