---
navigation_title: Event field reference
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Field reference for Kibana alerting v2 alert event documents in .alerts-events-*, including common fields, alert-only fields, and the index mapping."
---

# Kibana alerting v2 alert event field reference [alert-event-field-reference-v2]

Kibana alerting v2 rules write alert event documents to the `.alerts-events-*` data stream. This page describes the fields in each document.

## Common fields

These fields are present on every alert event document, regardless of whether the rule is in detect mode (`type: signal`) or alert mode (`type: alert`).

| Field | Type | Description |
|---|---|---|
| `@timestamp` | `date` | When this alert event document was written |
| `scheduled_timestamp` | `date` | The scheduled execution timestamp for the rule run that emitted this event |
| `rule.id` | `keyword` | The rule identifier |
| `rule.version` | `long` | The rule version at the time this event was emitted |
| `group_hash` | `keyword` | Series identity key, computed from the rule ID and grouping field values |
| `data` | `flattened` | Event payload containing the ES\|QL query output. Fields are accessed as `data.field_name` |
| `status` | `keyword` | Event status: `breached`, `recovered`, or `no_data` |
| `source` | `keyword` | Source of this event (for example, `internal` for rules) |
| `type` | `keyword` | Event type: `signal` (detect mode) or `alert` (alert mode) |

### `status` values

| Value | Meaning |
|---|---|
| `breached` | The rule condition was met for this group |
| `recovered` | The group was previously breaching but is no longer (detected by group hash comparison) |
| `no_data` | The rule returned no results and `no_data` behavior is configured |

### `type` values

| Value | Meaning |
|---|---|
| `signal` | Produced by a detect-mode rule (`kind: signal`). No lifecycle tracking |
| `alert` | Produced by an alert-mode rule (`kind: alert`). Includes episode fields |

## Alert-only fields

These fields are present only when `type` is `alert`. They are not applicable for signal events.

| Field | Type | Description |
|---|---|---|
| `episode.id` | `keyword` | The episode identifier. Groups all events in one lifecycle arc |
| `episode.status` | `keyword` | The current episode state: `inactive`, `pending`, `active`, or `recovering` |
| `episode.status_count` | `long` | Count of consecutive evaluations in the current status. Used for count-based state transitions. Only set for `pending` and `recovering` statuses |

### `episode.status` values

| Value | Meaning |
|---|---|
| `inactive` | The condition is not met |
| `pending` | The condition is met but activation thresholds are not yet satisfied |
| `active` | The condition is met and activation thresholds are satisfied. The alert is actionable |
| `recovering` | The condition is no longer met but recovery thresholds are not yet satisfied |

## The `data` field

The `data` field stores the ES|QL query output as a flattened object. The fields in `data` depend on what your query returns — specifically, the fields in the `KEEP` command (or all output fields if `KEEP` is not used).

For example, if your query is:

```esql
FROM metrics-*
| STATS avg_cpu = AVG(system.cpu.total.pct) BY host.name
| WHERE avg_cpu > 0.9
| KEEP host.name, avg_cpu
```

The resulting `data` field contains:

```json
{
  "data": {
    "host.name": "host-a",
    "avg_cpu": 0.95
  }
}
```

Access these fields in notification policy matchers, Discover queries, and rules on alerts using `data.field_name` syntax (for example, `data.host.name`, `data.avg_cpu`).

### Flattened mapping

The `data` field uses the `flattened` field type. This means:

- All values are stored as keywords.
- Numeric operations require explicit type conversion in ES|QL (`TO_DOUBLE`, `TO_INTEGER`).
- Nested objects are dot-delimited (for example, `data.host.name`).

## Index mapping

The `.alerts-events-*` data stream uses this mapping:

```json
{
  "dynamic": false,
  "properties": {
    "@timestamp": { "type": "date" },
    "scheduled_timestamp": { "type": "date" },
    "rule": {
      "properties": {
        "id": { "type": "keyword" },
        "version": { "type": "long" }
      }
    },
    "group_hash": { "type": "keyword" },
    "data": { "type": "flattened" },
    "status": { "type": "keyword" },
    "source": { "type": "keyword" },
    "type": { "type": "keyword" },
    "episode": {
      "properties": {
        "id": { "type": "keyword" },
        "status": { "type": "keyword" },
        "status_count": { "type": "long" }
      }
    }
  }
}
```

`dynamic: false` means that only the fields listed in the mapping are indexed. The `data` field captures all query output as a flattened type, but additional top-level fields not in the mapping are ignored.

## Alert actions fields

Alert actions (acknowledge, snooze, deactivate, fire, suppress) are stored in a separate `.alerts-actions` index. Key fields:

| Field | Type | Description |
|---|---|---|
| `action` | `keyword` | Action type: `ack`, `unack`, `snooze`, `unsnooze`, `deactivate`, `activate`, `fire`, `suppress`, `notified` |
| `rule_id` | `keyword` | The rule identifier |
| `group_hash` | `keyword` | The series identity |
| `episode_id` | `keyword` | The episode identifier (null for series-scoped actions like snooze) |
| `reason` | `keyword` | For `suppress` actions: `ack`, `deactivate`, `snooze`, or `throttled` |
| `@timestamp` | `date` | When the action was recorded |
