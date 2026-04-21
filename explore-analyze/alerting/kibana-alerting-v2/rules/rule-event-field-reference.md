---
navigation_title: Rule and event fields
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Reference for {{alerting-v2}} rule configuration fields and documents written to `.rule-events`."
---

# Rule event and field reference [rule-reference-v2]

$$$rule-reference-v2$$$

This page lists technical fields for rule configuration and rule event documents written to `.rule-events`. For alert actions in `.alert-actions`, see [Alert states and fields reference](../alerts/alert-states-and-fields-reference.md#alert-states-reference-v2). For action policy dispatch outcomes, see [Action policy reference](../notifications/action-policy-reference.md#action-policy-reference-v2).

:::{important}
The `.rule-events` and `.alert-actions` data streams are [system indices](/reference/glossary/index.md#glossary-system-index). {{kib}} manages their versioning, retention, and lifecycle. Do not change mappings or index settings for these streams yourself.
:::

## Schedule and lookback

These fields control when a rule runs and how far back its {{esql}} query looks on each evaluation.

| Field | Description |
|---|---|
| schedule.every | Execution interval; minimum 5 seconds, maximum 365 days. |
| schedule.lookback | Time range the {{esql}} query covers; must not exceed 365 days; should be at least `schedule.every` to avoid gaps. |

## Activation thresholds

These fields are only available in Alert mode. They control how many consecutive breaches, or how long a condition must persist, before an episode transitions from `pending` to `active`.

| Field | Description |
|---|---|
| pending_count | Consecutive breaches required. |
| pending_timeframe | Minimum duration the condition must persist. |
| pending_operator | How to combine count and timeframe (`AND` or `OR`). |

## Recovery thresholds

These fields are only available in Alert mode. They control how many consecutive recoveries, or how long the condition must be clear, before an episode transitions from `recovering` to `inactive`.

| Field | Description |
|---|---|
| recovering_count | Consecutive recoveries required. |
| recovering_timeframe | Minimum duration for recovery. |
| recovering_operator | How to combine count and timeframe (`AND` or `OR`). |

## No-data handling

These settings determine what the rule records when the {{esql}} query returns no rows on an evaluation.

| Behavior | Effect |
|---|---|
| no_data (default) | Record a no-data event. |
| last_status | Carry forward the previous status. |
| recover | Treat absence as recovery. |

## Rule grouping

Grouping is configured in YAML. The fields listed here control how the rule partitions results into independent series, each with its own lifecycle.

| Key | Description |
|---|---|
| grouping.fields | Array of field names; must align with `STATS ... BY` in the {{esql}} query. |

## Rule event documents

Each time a rule evaluates, {{kib}} writes one document per matched series to `.rule-events`. The `type` field determines the document kind:

- **signal:** A point-in-time record that the query matched. Useful for querying history or chaining into follow-on rules. Signal documents do not include `episode.*` fields.
- **alert:** A lifecycle-tracked episode visible in the alert inbox, episode details, and triage views. Alert documents include `episode.*` fields and represent a breach that stays open until the condition clears.

Both kinds share the base fields below. Only `alert` documents add the [Episode fields](#episode-fields) listed further down.

### Signal and alert fields

These fields appear on all `.rule-events` documents, regardless of whether the rule is in Detect or Alert mode.

| Field | Type | Required | Description |
|---|---|---|---|
| @timestamp | date | Yes | When this document was written to `.rule-events`. |
| scheduled_timestamp | date | No | Scheduled execution time for this rule run. |
| rule.id | keyword | Yes | Rule identifier. |
| rule.version | long | Yes | Rule version at the time this event was emitted. |
| group_hash | keyword | Yes | Series identity key for grouped evaluations. |
| data | flattened | Yes | Payload from the {{esql}} query output. Shape depends on your rule. |
| status | keyword | Yes | One of: `breached`, `recovered`, `no_data`. |
| source | keyword | Yes | Origin of this event. Product-specific identifier. |
| type | keyword | Yes | `signal` or `alert`. Application field on each rule event document written by {{kib}}. |

:::{admonition} Fields not stored as a dedicated column
There is no top-level or nested `duration` field on `.rule-events` documents. For triage or reporting, derive duration from [Query alerts and signals in Discover](../alerts/query-alerts-and-signals-in-discover.md#explore-alerts-discover-v2), the alert UI, or your own queries over timestamps and episode identifiers.
:::

### Episode fields

These fields only appear on documents with `type: alert`, written by rules running in Alert mode. They carry the lifecycle state for the episode associated with the matched series.

| Field | Type | Description |
|---|---|---|
| episode.id | keyword | Episode identifier for this series. |
| episode.status | keyword | One of: `inactive`, `pending`, `active`, `recovering`. |
| episode.status_count | long | Count of consecutive evaluations in the current `episode.status`. Only set when `episode.status` is `pending` or `recovering`. |
