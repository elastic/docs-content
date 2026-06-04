---
navigation_title: YAML rule schema reference
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Complete field reference for YAML rule definitions in the {{alerting-v2}}: required fields, metadata, schedule, grouping, state transitions, no-data handling, and duration format."
---

# YAML rule schema reference for {{alerting-v2}} [yaml-rule-schema-reference]


YAML rule schema is part of the {{alerting-v2}} in {{kib}}. This page lists valid fields for YAML rule definitions. For examples and authoring guidance, refer to [Create rules using the YAML editor](create-rule-with-yaml.md).

## Required fields

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `kind` | string | `alert` or `signal` | Whether the rule tracks ongoing episodes (`alert`) or records point-in-time observations (`signal`). |
| `metadata.name` | string | Max 256 characters | The name of the rule. |
| `schedule.every` | duration | For example, `5s`, `1m`, `5m` | How often the rule runs. Minimum interval applies. |
| `evaluation.query.base` | string | Valid {{esql}} query, max 10,000 characters | The query that checks your data on each run. |

## Metadata fields

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `metadata.description` | string | Max 1,024 characters | Optional description of what the rule monitors. |
| `metadata.owner` | string | Max 256 characters | Team or person responsible for the rule. |
| `metadata.tags` | array of strings | Max 100 tags | Labels for filtering and organization. |

## Schedule fields

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `schedule.lookback` | duration | For example, `5m`, `24h` | How far back in time the query searches on each run. |
| `time_field` | string | Any valid field name, max 128 characters | The timestamp field used for the lookback window filter. Defaults to `@timestamp`. |

## Recovery policy fields

The `recovery_policy` field is optional. When absent, the rule emits no recovery events and active alert episodes don't close automatically. Omitting `recovery_policy` is only possible when creating a rule via the API or Agent Builder. Rules created through the Kibana UI always include `recovery_policy.type: no_breach` by default.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `recovery_policy.type` | string | `no_breach` or `query` | How recovery is detected. `no_breach` recovers when the query returns no breach results for the active group. `query` uses a separate recovery query. |
| `recovery_policy.query.base` | string | Valid {{esql}} query | Required when `recovery_policy.type` is `query`. The query that checks whether the condition has cleared. |

## State transition fields

Only valid when `kind: alert`. Controls how many consecutive detections are required before an episode becomes active or recovers.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `state_transition.pending_operator` | string | `AND` or `OR` | Whether both the count and timeframe must be met (`AND`) or either one (`OR`) before becoming active. |
| `state_transition.pending_count` | integer | 0 or more | Number of consecutive breaches required before the episode becomes active. |
| `state_transition.pending_timeframe` | duration | For example, `5m` | Time window within which the breach count must be met. |
| `state_transition.recovering_operator` | string | `AND` or `OR` | Whether both the count and timeframe must be met (`AND`) or either one (`OR`) before recovering. |
| `state_transition.recovering_count` | integer | 0 or more | Number of consecutive clear evaluations required before the episode recovers. |
| `state_transition.recovering_timeframe` | duration | For example, `5m` | Time window within which the recovery count must be met. |

## Grouping fields

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `grouping.fields` | array of strings | Max 16 fields, each max 256 characters | Fields to group results by. Each unique combination becomes its own series. |

<!--[CONTENT NEEDED for M2: The `grouping` key is being renamed to `track_by` in M2 (for example, `track_by: { fields: [host.name] }`). The rename is not cosmetic: the old name implied a direct relationship to the ES|QL `STATS ... BY` clause, which caused confusion. `track_by` captures the actual intent — which fields identify the thing you're monitoring.

Two additional behaviors change with this rename:

- **New default**: When `track_by` is omitted, the rule creates one stable series per rule, computed from `sha256(ruleId + spaceId)`. The current `grouping` default is broken — with no fields specified it generates a per-row, per-execution hash that changes every run, orphaning episodes on every evaluation.
- **New `series.*` document fields**: M2 adds `series.key` (the internal hash, replacing `group_hash`) and `series.tracked_by` (a structured object of the field names and values, for example `{"host.name": "web-01"}`).

Update this section to replace `grouping.fields` with `track_by.fields`, document the new default behavior, and add the `series.*` output fields. Until M2 ships, `grouping.fields` remains the correct field name.]
-->

## No-data fields

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `no_data.behavior` | string | `no_data`, `last_status`, or `recover` | What happens when the query returns no results. `no_data` records a no-data event. `last_status` keeps the current status. `recover` closes any active episode. |
| `no_data.timeframe` | duration | For example, `5m` | How long the query must return no results before the no-data behavior applies. |

## Artifact fields

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `artifacts[].type` | string | For example, `runbook` | The type of artifact being attached. |
| `artifacts[].value` | string | Markdown content | The content of the artifact. Runbooks are rendered as markdown in the rule detail view. |

## Notification policy fields

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `notification_policies[].ref` | string | Format: `policies/<id>` | Links a notification policy to the rule. |

## Duration format

All duration fields accept the following units:

| Unit | Example | Meaning |
|---|---|---|
| `s` | `30s` | Seconds |
| `m` | `5m` | Minutes |
| `h` | `1h` | Hours |
| `d` | `7d` | Days |
