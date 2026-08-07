---
navigation_title: Rule event data model
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Alert episodes and signals share the .rule-events data stream and most fields. Alert documents add episode.* lifecycle fields; triage actions go to .alert-actions."
---

# Rule event data model in the {{alerting-v2-system}} [alert-data-model]

This page explains what the {{alerting-v2-system}} writes, where it writes it, and how alert episode and signal documents relate. Use it when you're querying `.rule-events` and need to know which fields apply to signals, alert episodes, or both.

## How rule mode determines what gets written [how-rule-mode-determines-output]

Every time a rule finds a match, it writes a document to `.rule-events`. Whether that document is a signal or an alert depends on the rule's mode. Both document kinds share the same data stream and most of the same fields.

| Type | What it is | When it's created |
| --- | --- | --- |
| Signal | A point-in-time record that the query matched (`type: signal`). | Rules in Signal mode |
| Alert | A lifecycle-tracked episode with `type: alert` and `episode.*` fields. | Rules in Alert mode |

:::{note}
A rule in Signal mode only writes signals. It never opens alert episodes, so action policies have nothing to match against.
:::

## Shared index and schema [shared-index-and-schema]

Alert episodes and signals are both written to `.rule-events` and share many of the same fields, including `data`, which holds the payload from your rule's query. The `type` field tells you which kind of document you're looking at, `signal` or `alert`, so you can filter for one or the other in a query (for example, `WHERE type == "signal"`).

Alert episodes carry three additional fields, prefixed `episode.*`, for tracking lifecycle state (`episode.id`, `episode.status`, `episode.status_count`). Alert episodes track an ongoing problem, so they carry these fields; signals don't.

This table shows the full field list, with the alert-only fields marked.

| Field | Type | Signal | Alert episode | Description |
|---|---|---|---|---|
| `@timestamp` | date | ✅ | ✅ | When the evaluation ran |
| `scheduled_timestamp` | date | ✅ | ✅ | The scheduled time for this evaluation |
| `rule.id` | keyword | ✅ | ✅ | ID of the rule that produced this event |
| `rule.version` | long | ✅ | ✅ | Version of the rule at evaluation time |
| `group_hash` | keyword | ✅ | ✅ | Identifies the series this event belongs to |
| `status` | keyword | ✅ | ✅ | Outcome of a single evaluation (`breached`, `recovered`, or `no_data`) |
| `type` | keyword | ✅ | ✅ | Whether this document is a signal or an alert |
| `severity` | keyword | ✅ | ✅ | Severity level assigned by the rule |
| `data` | flattened | ✅ | ✅ | Rule-defined payload from the source query |
| `source` | keyword | ✅ | ✅ | Source that produced the event |
| `space_id` | keyword | ✅ | ✅ | {{kib}} space where the rule lives |
| `episode.id` | keyword | — | ✅ | ID of the alert episode |
| `episode.status` | keyword | — | ✅ | Lifecycle state (`inactive`, `pending`, `active`, or `recovering`) |
| `episode.status_count` | long | — | ✅ | Count of consecutive evaluations in the current status, set only for pending or recovering |

For query examples against signals, refer to [Observe and analyze signals](../observe-and-analyze-signals.md). For episode lifecycle and triage queries, refer to [Query {{alerting-v2-system}} alert history in Discover](query-alerts-and-signals-in-discover.md). For the same fields in reference form, plus the `.alert-actions` stream, refer to [Field reference](field-reference.md).

## How {{kib}} records evaluation and triage data [how-kib-records-evaluation-triage-data]

{{kib}} writes rule output to the following append-only data streams, both managed through ILM and queryable with {{esql}} in Discover:

- **`.rule-events`** - {{kib}} writes one document for each rule evaluation and never overwrites them. This stream holds both signals and alert episode evaluations.
- **`.alert-actions`** - Records every triage action taken on an episode (for example, acknowledge, snooze, and resolve). Only alert episodes produce documents here.
