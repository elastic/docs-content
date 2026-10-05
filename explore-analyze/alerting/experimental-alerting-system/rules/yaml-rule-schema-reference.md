---
navigation_title: YAML rule schema reference
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "YAML rule definitions in the experimental alerting system support fields for detection mode, schedule, query, grouping, and recovery. Reference tables list all valid field values."
---

# YAML rule schema reference for the {{alerting-v2-system}} [yaml-rule-schema-reference]

This page lists valid fields for YAML rule definitions in the {{alerting-v2-system}}. For authoring guidance, refer to [Create an {{esql}} rule](create-esql-rule.md).

## Base rule fields

Every rule must set `kind`, `metadata.name`, and `schedule.every`.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `kind` | string | `alert` or `signal` | Whether the rule tracks ongoing alert episodes (`alert`) or records point-in-time observations (`signal`). Set when the rule is created and can't be modified when editing the rule. |
| `metadata.name` | string | Any string | Rule name. Must be unique within the {{kib}} space. Max 256 characters. |
| `schedule.every` | duration | Any duration string | How often the rule runs. For example: `5s`, `1m`, `5m`. Minimum interval applies. |

## Query fields

These fields define the ES\|QL query the rule runs on each evaluation.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `query.base` | ES\|QL string | A full query, including `FROM` | Required. ES\|QL query that selects the data to evaluate. {{kib}} applies the time filter from `schedule.lookback` using `time_field`. <br><br> Required only when `query.format` is `composed`. {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` |
| `query.breach.segment` {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` | ES\|QL segment string | A clause with no `FROM` | Optional. Appended to `query.base`, for example `WHERE avg_cpu > 0.85`. If you omit it, every row returned by `query.base` is a match. |
| `query.format` {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` | string | `composed` or `standalone` | Required. The query structure the rule uses. `standalone` means each condition (breach, recovery, no-data) is a separate, self-contained ES\|QL query. `composed` means you write one base query and each condition is a pipe segment appended to it. The UI always creates `standalone` rules. |

### Fields for `query.format: composed`
```{applies_to}
stack: experimental =9.5
serverless: unavailable
```

Use `composed` when breach, recovery, and no-data conditions all start from the same data shape. Define that shape once in the base query and each condition adds only what differs.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `query.breach.segment` | ES\|QL segment string | | Required. ES\|QL segment appended to the base query for breach detection. Write it as a pipe command, for example `\| WHERE count > 5`. |
| `query.recovery.segment` | ES\|QL segment string | | ES\|QL segment appended to the base query for recovery detection. Required when `recovery_strategy` is `query`. |

### Fields for `query.format: standalone`
```{applies_to}
stack: experimental =9.5
serverless: unavailable
```

Use `standalone` when conditions need full independence. Each query can target different indices, apply different filters, or return a completely different shape.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `query.breach.query` | Full ES\|QL string | | Required. Full ES\|QL query for breach detection. |
| `query.recovery.query` | Full ES\|QL string | | Full ES\|QL query for recovery detection. Required when `recovery_strategy` is `query`. |
| `query.no_data.query` | Full ES\|QL string | | Full ES\|QL query that detects presence of data. Required when `no_data_strategy` is not `none`. |

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
| `time_field` | string | Any field name | The timestamp field used for the lookback window filter. Defaults to `@timestamp`. <br><br> Max character limits: <br> - 256 {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` <br> - 128 {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` |

## Recovery strategy [recovery-strategy]

:::::{applies-switch}

::::{applies-item} { serverless: ga, stack: experimental 9.6+ }

Set `recovery` on every rule with `kind: alert`. Omit `recovery` when `kind` is `signal`. An alert rule that omits it fails validation, and a signal rule that sets it fails validation.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `recovery.strategy` | string | `no_breach`, `condition`, `query`, or `manual` | How the alert episode recovers. <br><br> - `no_breach`: Recovers the alert episode when its group no longer appears in the breach results. The rule form calls this **Default recovery**. <br> - `condition`: Recovers the alert episode when `query.base` plus `recovery.segment` returns the group. Requires `query.breach`. The rule form calls this **Custom recovery**. <br> - `query`: Recovers the alert episode when `recovery.query` returns the group. Set this in YAML. The rule form does not offer it. <br> - `manual`: Does not recover automatically. Close the alert episode with a user action. The rule form calls this **No recovery**. |
| `recovery.segment` | ES\|QL segment string | A clause with no `FROM` | Required when `recovery.strategy` is `condition`. Appended to `query.base`, for example `WHERE avg_cpu < 0.60`. |
| `recovery.query` | ES\|QL string | A full query, including `FROM` | Required when `recovery.strategy` is `query`. |

:::{note}
Do not set `state_transition.recovering` when `recovery.strategy` is `manual`. The API rejects that combination.
:::

::::

::::{applies-item} stack: experimental =9.5

The `recovery_strategy` field is optional. When omitted, the rule emits no recovery events and active alert episodes don't close automatically.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `recovery_strategy` | string | `no_breach`, `query`, or `none` | How recovery is detected. <br><br> -`no_breach`: Recovers an alert episode when its active group no longer appears in the breach results. <br> - `query`: Evaluates a separate recovery query defined in `query.recovery.segment` (composed) or `query.recovery.query` (standalone) <br> - `none`: Turns off recovery. |

:::{note}
Rules with `kind: signal` must omit `recovery_strategy` or set it to `none`. Any other value fails validation.
:::

::::

:::::

## State transition fields [state-transition-fields]

:::::{applies-switch}

::::{applies-item} { serverless: ga, stack: experimental 9.6+ }

Only valid when `kind` is `alert`. `pending` and `recovering` are optional. If you include either object, set `count` or `timeframe`. An empty phase object fails validation. Set `operator` only when you set both `count` and `timeframe`.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `state_transition.pending.count` | integer | Integer, 0–1000 | Consecutive matches required before the alert episode becomes active. Set to `0` to open it on the first match. |
| `state_transition.pending.timeframe` | duration | Any duration string | How long the condition must hold before the alert episode becomes active, for example `5m`. |
| `state_transition.pending.operator` | string | `and` or `or` | If you set both `count` and `timeframe`, `and` requires both and `or` requires either. |
| `state_transition.recovering.count` | integer | Integer, 0–1000 | Consecutive recoveries required before the alert episode becomes inactive. Set to `0` to close it on the first recovery. |
| `state_transition.recovering.timeframe` | duration | Any duration string | How long the condition must hold before the alert episode becomes inactive, for example `5m`. |
| `state_transition.recovering.operator` | string | `and` or `or` | If you set both `count` and `timeframe`, `and` requires both and `or` requires either. |

:::{note}
The API rejects `state_transition.recovering` when `recovery.strategy` is `manual`.
:::

::::

::::{applies-item} stack: experimental =9.5

Only valid when `kind: alert`. Controls how many consecutive detections are required before an alert episode becomes active or recovers.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `state_transition.pending_operator` | string | `AND` or `OR` | Whether both the count and timeframe must be met (`AND`) or either one (`OR`) before becoming active. |
| `state_transition.pending_count` | integer | Integer, 0–1000 | Number of consecutive breaches required before the alert episode becomes active. Set to `0` to skip the pending phase and transition directly to active on the first breach. |
| `state_transition.pending_timeframe` | duration | Any duration string | How long the condition must remain continuously breached before the alert episode becomes active. For example: `5m`. |
| `state_transition.recovering_operator` | string | `AND` or `OR` | Whether both the count and timeframe must be met (`AND`) or either one (`OR`) before recovering. |
| `state_transition.recovering_count` | integer | Integer, 0–1000 | Number of consecutive clear evaluations required before the alert episode recovers. Set to `0` to skip the recovering phase and transition directly to inactive on recovery. |
| `state_transition.recovering_timeframe` | duration | Any duration string | How long the condition must remain continuously non-breaching before the alert episode recovers. For example: `5m`. |

::::

:::::

## Grouping fields

Use grouping to split a rule's detections into independent series, one per unique combination of field values. This lets a single rule track multiple subjects without creating a separate rule for each, for example, tracking CPU usage per host. Each series maintains its own alert episode lifecycle.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `grouping.fields` | array of strings | Array of field names | Fields to group results by. Each unique combination becomes its own series. Max 16 fields, each max 256 characters. |

## No-data strategy

:::::{applies-switch}

::::{applies-item} { serverless: ga, stack: experimental 9.6+ }

Set `no_data` on every rule with `kind: alert`. Omit `no_data` when `kind` is `signal`. An alert rule that omits it fails validation, and a signal rule that sets it fails validation.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `no_data.strategy` | string | `ignore`, `keep_last`, `resolve`, or `alert` | What the rule does when a group has no data. <br><br> - `ignore`: Does not check whether a group still has data. Missing groups do not produce `no_data` events. The rule form calls this **Do nothing**. <br> - `keep_last`: Holds the alert episode's current status when the rule finds no data. The rule form calls this **Keep last known status**. <br> - `resolve`: Closes the alert episode the first time the rule finds no data for that group. The rule form calls this **Recover immediately**. <br> - `alert`: Marks an existing alert episode active when the rule finds no data. It does not open an alert episode for a group that has not breached. Create and update requests reject `alert`. |
| `no_data.query` | ES\|QL string | A full query, including `FROM` | Optional presence query. Allowed when `no_data.strategy` is `keep_last`, `resolve`, or `alert`. If you omit it, the rule uses `query.base` as the presence query, and the rule must set `query.breach`. Do not set `no_data.query` when the strategy is `ignore`. |

:::{note}
Any strategy other than `ignore` requires `query.breach` or `no_data.query`. The rule uses that query to tell a group with no data apart from a group that stopped breaching.
:::

::::

::::{applies-item} stack: experimental =9.5

Use `no_data_strategy` to control what the rule does when an evaluation returns no results. This matters when data sources can go silent. Without this setting, a quiet data source and a healthy one look identical to the rule.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `no_data_strategy` | string | `emit`, `last_known_status`, `recover`, or `none` | Optional. What happens when the rule evaluates and returns no results. `emit` records a no-data event. `last_known_status` holds the last known status. `recover` forces recovery. `none` disables no-data detection. |

:::{note}
No-data detection is only supported with `query.format: standalone`. Setting `no_data_strategy` to any active value on a `composed` rule has no effect because `query.no_data.query` can only be defined on a standalone query. Rules with `kind: signal` must omit `no_data_strategy` or set it to `none`.
:::

::::

:::::

## Artifact fields

Artifacts let you attach reference material directly to a rule, such as a runbook or a linked dashboard. {{kib}} stores the artifact with the rule and displays it on the rule details page, so responders have context when an alert fires.

The `artifacts` array is optional and accepts up to 100 entries. Every artifact needs `id` and `type`. Use `data` or `value` for the content, as shown in the following table.

| Field | Type | Accepted values | Description |
|---|---|---|---|
| `artifacts[].id` | string | Any string | Required. Unique identifier for the artifact within the rule's artifacts array. {{kib}} rejects the rule if two artifacts share an id. <br><br> Max character limits: <br> - 150 {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` <br> - 256 {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` |
| `artifacts[].type` | string | Any string | Use `runbook` or `dashboard`. Other strings are allowed. Max 128 characters. |
| `artifacts[].data` {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` | object | Type-specific object | Required. Holds the fields specific to type, such as `data.content` or `data.dashboard_id`. Max 32 fields. |
| `artifacts[].data.content` {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` | string | Non-empty string | The Markdown body of a runbook. {{kib}} displays it on the **Runbook** tab of the rule details page. Required when `type` is `runbook`. Max 50,000 characters. |
| `artifacts[].data.dashboard_id` {applies_to}`{ serverless: ga, stack: experimental 9.6+ }` | string | Non-empty string | ID of the dashboard to link. Required when `type` is `dashboard`. Max 1,024 characters. |
| `artifacts[].value` {applies_to}`{ stack: experimental =9.5, serverless: unavailable }` | string | Any string | Required. Runbook Markdown (max 50,000 characters) or a dashboard ID (max 1,024 characters). |

The following example attaches a runbook and a dashboard to the same rule.

::::{applies-switch}

:::{applies-item} { serverless: experimental, stack: experimental 9.6+ }

```yaml
artifacts:
  - id: checkout-runbook
    type: runbook                                          <1>
    data:
      content: |                                           <2>
        Fires when checkout error rate exceeds 10%.
  - id: checkout-errors-dashboard
    type: dashboard
    data:
      dashboard_id: "8ac12f90-3d2b-11ef-9a4e-0242ac120002" <3>
```

1. `type` determines which `data` field the artifact requires.
2. The runbook Markdown goes in `data.content`.
3. The dashboard ID goes in `data.dashboard_id`.

If {{kib}} loads a rule that still uses `value`, it converts that field to `data`. Write new YAML with `data`.
:::

:::{applies-item} stack: experimental =9.5

```yaml
artifacts:
  - id: checkout-runbook
    type: runbook
    value: |                                      <1>
      Fires when checkout error rate exceeds 10%.
  - id: checkout-errors-dashboard
    type: dashboard
    value: "8ac12f90-3d2b-11ef-9a4e-0242ac120002" <2>
```

1. The runbook Markdown goes in `value`.
2. The dashboard ID goes in `value`.
:::

::::

## Duration format [duration-format]

All duration fields accept the following units:

| Unit | Example | Meaning |
|---|---|---|
| `s` | `30s` | Seconds |
| `m` | `5m` | Minutes |
| `h` | `1h` | Hours |
| `d` | `7d` | Days |

## Related pages

- [Create an {{esql}} rule](create-esql-rule.md): Author rules using the YAML editor, with a live sandbox for previewing results.
- [Configure a rule](configure-a-rule.md): Field-by-field guidance for each setting, with examples and when-to-use recommendations.
