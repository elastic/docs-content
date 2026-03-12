---
navigation_title: Using YAML
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Define Kibana alerting v2 rules in YAML for version control and infrastructure-as-code workflows, with full field reference."
---

# Create Kibana alerting v2 rules with YAML [create-rules-yaml-v2]

Define Kibana alerting v2 rules as YAML documents for version control, infrastructure-as-code workflows, and bulk provisioning. The YAML format includes the complete rule definition: ES|QL query, schedule, recovery policy, state transitions, grouping, no-data handling, and notification policy references.

## YAML rule structure

A complete alert-mode rule in YAML:

```yaml
kind: alert

metadata:
  name: checkout-error-rate-by-route
  owner: platform
  labels: ["production", "checkout"]

time_field: "@timestamp"

schedule:
  every: 1m
  lookback: 20m

evaluation:
  query:
    base: |
      FROM metrics-*
      | STATS avg_cpu = AVG(system.cpu.total.pct) BY host.name
      | WHERE env == "production"
    condition: "WHERE avg_cpu > 0.9"

recovery_policy:
  type: query
  query:
    base: |
      FROM metrics-*
      | STATS avg_cpu = AVG(system.cpu.total.pct) BY host.name
    condition: "WHERE avg_cpu < 0.67"

state_transition:
  pending_operator: OR
  pending_count: 3
  pending_timeframe: 5m
  recovering_operator: AND
  recovering_count: 2
  recovering_timeframe: 10m

grouping:
  fields: [host.name]

no_data:
  behavior: no_data
  timeframe: 15m

notification_policies:
  - ref: "policies/service-alerts-v1"
  - ref: "policies/pagerduty-sev1-v1"
```

## Field reference

### Top-level fields

| Field | Type | Required | Description |
|---|---|---|---|
| `kind` | string | Yes | `alert` or `signal` |
| `metadata` | object | Yes | Rule identity and categorization |
| `time_field` | string | No | Time field for lookback filtering. Defaults to `@timestamp` |
| `schedule` | object | Yes | Execution schedule |
| `evaluation` | object | Yes | ES\|QL query configuration |
| `recovery_policy` | object | No | Recovery detection (alert mode only) |
| `state_transition` | object | No | Activation and recovery thresholds (alert mode only) |
| `grouping` | object | No | Fields to group alert events by |
| `no_data` | object | No | Behavior when query returns no results |
| `notification_policies` | array | No | References to notification policies |

### `metadata`

| Field | Type | Required | Description |
|---|---|---|---|
| `metadata.name` | string | Yes | Rule name |
| `metadata.owner` | string | No | Rule owner |
| `metadata.labels` | array | No | Tags for filtering and organization |

### `schedule`

| Field | Type | Required | Description |
|---|---|---|---|
| `schedule.every` | duration | Yes | Execution interval (for example, `1m`, `5m`, `1h`) |
| `schedule.lookback` | duration | No | Time window for query evaluation |

### `evaluation`

| Field | Type | Required | Description |
|---|---|---|---|
| `evaluation.query.base` | string | Yes | Base ES\|QL query |
| `evaluation.query.condition` | string | No | WHERE clause for breaching rows. Required when `no_data` is configured |

### `recovery_policy`

| Field | Type | Required | Description |
|---|---|---|---|
| `recovery_policy.type` | string | Yes | `query` or `no_breach` |
| `recovery_policy.query.base` | string | No | Recovery query (when type is `query`) |
| `recovery_policy.query.condition` | string | No | Recovery condition |

### `state_transition`

| Field | Type | Required | Description |
|---|---|---|---|
| `state_transition.pending_count` | integer | No | Consecutive breaches before activating |
| `state_transition.pending_timeframe` | duration | No | Time window for pending evaluation |
| `state_transition.pending_operator` | string | No | `AND` or `OR` — how to combine count and timeframe |
| `state_transition.recovering_count` | integer | No | Consecutive recoveries before deactivating |
| `state_transition.recovering_timeframe` | duration | No | Time window for recovery evaluation |
| `state_transition.recovering_operator` | string | No | `AND` or `OR` |

### `grouping`

| Field | Type | Required | Description |
|---|---|---|---|
| `grouping.fields` | array | No | Fields to group by (for example, `[host.name, service.name]`) |

### `no_data`

| Field | Type | Required | Description |
|---|---|---|---|
| `no_data.behavior` | string | No | `no_data`, `last_status`, or `recover` |
| `no_data.timeframe` | duration | No | How long before no-data is detected |

## Detect mode example

A minimal detect-mode rule:

```yaml
kind: signal

metadata:
  name: http-500-errors

schedule:
  every: 5m
  lookback: 5m

evaluation:
  query:
    base: |
      FROM logs-*
      | WHERE http.response.status_code >= 500
      | STATS error_count = COUNT(*) BY service.name
      | KEEP service.name, error_count
```

## Toggle between GUI and YAML

In the rule creation UI, you can toggle between the interactive form and YAML mode at any time. Changes made in one mode are reflected in the other. This lets you use the form for quick edits and switch to YAML for full control or to copy the rule definition for version control.

## Update rules

The update API accepts partial payloads. You can update any field except `kind` (changing the kind would require handling active alert transitions). Setting a field to `null` clears it. Omitting a field preserves the existing value.
