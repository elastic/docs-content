---
navigation_title: Rule and event fields
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Field reference for rule configuration and .rule-events documents in Kibana's experimental alerting system. Covers schedule, activation thresholds, and rule event output fields."
---

# Rule event and field reference in the {{alerting-v2-system}} [rule-reference]

Rule event fields are part of the {{alerting-v2-system}} in {{kib}}. This page lists technical fields for rule configuration and rule event documents written to `.rule-events`.
<!-- TODO: Uncomment when PRs #6524 (alerts) and #6525 (workflows/notifications) are merged:
For alert actions in `.alert-actions`, refer to [Alert states and fields reference](../alerts/alert-states-and-fields-reference.md#alert-states-reference). For action policy dispatch outcomes, refer to [Action policy reference](../notifications/action-policy-reference.md#action-policy-reference).
-->

:::{important}
The `.rule-events` and `.alert-actions` data streams are [system indices](/reference/glossary/index.md#glossary-system-index). {{kib}} manages their versioning, retention, and lifecycle through ILM. Older backing indices are deleted automatically when the retention window expires. Do not change mappings or index settings for these streams yourself.
:::

## Schedule and lookback

These fields control when a rule runs and how far back its {{esql}} query looks on each evaluation.

| Field | Description |
|---|---|
| `schedule.every` | Execution interval; minimum 5 seconds, maximum 365 days. |
| `schedule.lookback` | Time range the {{esql}} query covers; must not exceed 365 days; should be at least `schedule.every` to avoid gaps. |

## Activation thresholds

These fields are only available in Alert mode. They control how many consecutive breaches, or how long a condition must persist, before an episode transitions from `pending` to `active`.

| Field | Description |
|---|---|
| `pending_count` | Consecutive breaches required. |
| `pending_timeframe` | Minimum duration the condition must persist. |
| `pending_operator` | How to combine count and timeframe (`AND` or `OR`). |

## Recovery thresholds

These fields are only available in Alert mode. They control how many consecutive recoveries, or how long the condition must be clear, before an episode transitions from `recovering` to `inactive`.

| Field | Description |
|---|---|
| `recovering_count` | Consecutive recoveries required. |
| `recovering_timeframe` | Minimum duration for recovery. |
| `recovering_operator` | How to combine count and timeframe (`AND` or `OR`). |

## No-data handling

These settings determine what the rule records when the {{esql}} query returns no rows on an evaluation.

| Behavior | Effect |
|---|---|
| `emit` | Record a no-data event. |
| `last_known_status` | Carry forward the previous status. |
| `recover` | Treat absence as recovery. |
| `none` | Disable no-data detection. |

## Rule grouping

Grouping is configured in YAML. The fields listed here control how the rule partitions results into independent series, each with its own lifecycle.

| Key | Description |
|---|---|
| `grouping.fields` | Array of field names; must align with `STATS ... BY` in the {{esql}} query. |

## Rule event documents

Each time a rule evaluates, {{kib}} writes one document per matched series to `.rule-events`. The `type` field determines the document kind:

- **signal:** A point-in-time record that the query matched. Useful for querying history or chaining into follow-on rules. Signal documents don't include `episode.*` fields.
- **alert:** A lifecycle-tracked episode visible in the alert inbox, episode details, and triage views. Alert documents include `episode.*` fields and represent a breach that stays open until the condition clears.

Both kinds share the base fields below. Only `alert` documents add the [Episode fields](#episode-fields) listed further down.

:::{note}
`.rule-events` is a data stream, so it is append-only. A new document is written on every rule evaluation; existing documents are never updated. Each document is a snapshot of that moment: the `episode.status` field records the lifecycle stage the episode was in at that evaluation. To view the full history of an episode, query all documents that share the same `episode.id`.
<!-- TODO: Uncomment when PR #6524 (alerts) is merged:
Refer to [Query alerts and signals in Discover](../alerts/query-alerts-and-signals-in-discover.md#explore-alerts-discover) for example queries.
-->
:::

### Signal and alert fields

These fields appear on all `.rule-events` documents, regardless of whether the rule is in Signal or Alert mode.

| Field | Type | Required | Description |
|---|---|---|---|
| `@timestamp` | date | Yes | When this document was written to `.rule-events`. |
| `scheduled_timestamp` | date | No | Scheduled execution time for this rule run. |
| `rule.id` | keyword | Yes | Rule identifier. |
| `rule.version` | long | Yes | Rule version at the time this event was emitted. |
| `group_hash` | keyword | Yes | Series identity key for grouped evaluations. |
| `data` | flattened | Yes | Payload from the {{esql}} query output. Shape depends on your rule. |
| `status` | keyword | Yes | One of: `breached`, `recovered`, `no_data`. |
| `source` | keyword | Yes | Origin of this event. Product-specific identifier. |
| `type` | keyword | Yes | `signal` or `alert`. Application field on each rule event document written by {{kib}}. |

:::{admonition} Fields not stored as a dedicated column
There's no top-level or nested `duration` field on `.rule-events` documents. For triage or reporting, derive duration from the alert UI or your own queries over timestamps and episode identifiers.
<!-- TODO: Uncomment when PR #6524 (alerts) is merged and restore full sentence:
For triage or reporting, derive duration from [Query alerts and signals in Discover](../alerts/query-alerts-and-signals-in-discover.md#explore-alerts-discover), the alert UI, or your own queries over timestamps and episode identifiers.
-->
:::

### Episode fields [episode-fields]

These fields only appear on documents with `type: alert`, written by rules running in Alert mode. They carry the lifecycle state for the episode associated with the matched series.

| Field | Type | Description |
|---|---|---|
| `episode.id` | keyword | Episode identifier for this series. |
| `episode.status` | keyword | One of: `inactive`, `pending`, `active`, `recovering`. |
| `episode.status_count` | long | Count of consecutive evaluations in the current `episode.status`. Only set when `episode.status` is `pending` or `recovering`. |
| `severity` | keyword | Severity level from the most recent breached event. One of: `info`, `low`, `medium`, `high`, `critical`. Not set when the query output does not include a `severity` column, or when the value does not match a recognized level. Never set on `recovered` or `no_data` events. |
