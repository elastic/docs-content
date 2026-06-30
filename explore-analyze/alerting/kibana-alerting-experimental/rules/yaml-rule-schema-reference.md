---
navigation_title: YAML rule schema reference
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "YAML rule definitions in Kibana's experimental alerting system support fields for detection mode, schedule, query, grouping, and recovery. Reference tables list all valid field values."
---

# YAML rule schema reference for the {{alerting-v2-system}} [yaml-rule-schema-reference]


YAML rule schema is part of the {{alerting-v2-system}} in {{kib}}. This page lists valid fields for YAML rule definitions. For examples and authoring guidance, refer to [Create rules using the YAML editor](create-rule-with-yaml.md).

## Base rule fields

These four fields are required on every rule, regardless of format or mode. The value of `query.format` determines which additional query fields are required.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `kind` | string | `alert` or `signal` | Whether the rule tracks ongoing episodes (`alert`) or records point-in-time observations (`signal`). |
| `metadata.name` | string | Any string | The name of the rule. Max 256 characters. |
| `schedule.every` | duration | Any duration string | How often the rule runs. For example: `5s`, `1m`, `5m`. Minimum interval applies. |
| `query.format` | string | `composed` or `standalone` | The query structure the rule uses. `standalone` means each condition (breach, recovery, no-data) is a separate, self-contained ES\|QL query. `composed` means you write one base query and each condition is a pipe segment appended to it. The UI always creates `standalone` rules. |

### Fields for `query.format: composed`

Use `composed` when breach, recovery, and no-data conditions all start from the same data shape. Define that shape once in the base query and each condition adds only what differs.

| Field | Type | Description |
|---|---|---|
| `query.base` | ES\|QL string | Base query that runs on every evaluation. Time filters are applied automatically using the lookback window. Required. |
| `query.breach.segment` | ES\|QL segment string | Appendable ES\|QL segment for breach detection. Written as a pipe command, for example `\| WHERE count > 5`. Required. |
| `query.recovery.segment` | ES\|QL segment string | Appendable ES\|QL segment for recovery detection. Required when `recovery_strategy` is `query`. |

### Fields for `query.format: standalone`

Use `standalone` when conditions need full independence. Each query can target different indices, apply different filters, or return a completely different shape.

| Field | Type | Description |
|---|---|---|
| `query.breach.query` | Full ES\|QL string | Full ES\|QL query for breach detection. Required. |
| `query.recovery.query` | Full ES\|QL string | Full ES\|QL query for recovery detection. Required when `recovery_strategy` is `query`. |
| `query.no_data.query` | Full ES\|QL string | Full ES\|QL query that detects presence of data. Required when `no_data_strategy` is not `none`. Only supported on `standalone` format. |

## Metadata fields

These optional fields add descriptive information to a rule for identification, ownership, and filtering. None affect rule evaluation behavior.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `metadata.description` | string | Any string | Optional description of what the rule monitors. Max 1,024 characters. |
| `metadata.owner` | string | Any string | Team or person responsible for the rule. Max 256 characters. |
| `metadata.tags` | array of strings | Array of strings | Labels for filtering and organization. Max 20 tags, each max 128 characters. |

## Schedule fields

These fields control how far back each evaluation looks and which timestamp field is used for the time range filter. Both are optional, but omitting `schedule.lookback` means the query runs without a time bound.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `schedule.lookback` | duration | Any duration string | How far back in time the query searches on each run. For example: `5m`, `24h`. |
| `time_field` | string | Any field name | The timestamp field used for the lookback window filter. Max 128 characters. Defaults to `@timestamp`. |

## Recovery strategy

The `recovery_strategy` field is optional. When omitted, the rule emits no recovery events and active alert episodes don't close automatically.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `recovery_strategy` | string | `no_breach`, `query`, or `none` | How recovery is detected. <br><br> -`no_breach`: Recovers an episode when its active group no longer appears in the breach results. <br> - `query`: Evaluates a separate recovery query defined in `query.recovery.segment` (composed) or `query.recovery.query` (standalone) <br> - `none`: Turns off recovery. |

:::{note}
Signal-mode rules (`kind: signal`) must omit `recovery_strategy` or set it to `none`. Any other value fails validation.
:::

## State transition fields

Only valid when `kind: alert`. Controls how many consecutive detections are required before an episode becomes active or recovers.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `state_transition.pending_operator` | string | `AND` or `OR` | Whether both the count and timeframe must be met (`AND`) or either one (`OR`) before becoming active. |
| `state_transition.pending_count` | integer | Integer ≥ 0 | Number of consecutive breaches required before the episode becomes active. |
| `state_transition.pending_timeframe` | duration | Any duration string | Time window within which the breach count must be met. For example: `5m`. |
| `state_transition.recovering_operator` | string | `AND` or `OR` | Whether both the count and timeframe must be met (`AND`) or either one (`OR`) before recovering. |
| `state_transition.recovering_count` | integer | Integer ≥ 0 | Number of consecutive clear evaluations required before the episode recovers. |
| `state_transition.recovering_timeframe` | duration | Any duration string | Time window within which the recovery count must be met. For example: `5m`. |

## Grouping fields

Use grouping to split a rule's detections into independent series, one per unique combination of field values. This lets a single rule track multiple subjects — such as CPU usage per host — without creating a separate rule for each. Each series maintains its own alert episode lifecycle.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `grouping.fields` | array of strings | Array of field names | Fields to group results by. Each unique combination becomes its own series. Max 16 fields, each max 256 characters. |

## No-data strategy

Use `no_data_strategy` to control what the rule does when an evaluation returns no results. This matters when data sources can go silent: without a no-data strategy, a quiet data source and a healthy one look identical to the rule.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `no_data_strategy` | string | `emit`, `last_known_status`, `recover`, or `none` | Optional. What happens when the rule evaluates and returns no results. `emit` records a no-data event. `last_known_status` holds the last known status. `recover` forces recovery. `none` disables no-data detection. |

:::{note}
No-data detection is only supported with `query.format: standalone`. Setting `no_data_strategy` to any active value on a `composed` rule has no effect because `query.no_data.query` can only be defined on a standalone query. Signal-mode rules (`kind: signal`) must omit `no_data_strategy` or set it to `none`.
:::

## Artifact fields

Artifacts let you attach reference material — such as a runbook — directly to a rule. The content is stored with the rule and displayed in the rule detail view so responders have context when an alert fires. All artifact fields are optional.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `artifacts[].id` | string | Any string | Artifact identifier. Required. Max 256 characters. |
| `artifacts[].type` | string | Any string | The type of artifact being attached. For example: `runbook`. |
| `artifacts[].value` | string | Any string | The content of the artifact. Accepts markdown. Runbooks are rendered as markdown in the rule detail view. |

## Duration format

All duration fields accept the following units:

| Unit | Example | Meaning |
|---|---|---|
| `s` | `30s` | Seconds |
| `m` | `5m` | Minutes |
| `h` | `1h` | Hours |
| `d` | `7d` | Days |
