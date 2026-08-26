---
navigation_title: Rule event data model
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Alert episodes and signals share .rule-events and most fields in the experimental alerting system. Alert documents add episode lifecycle fields, and triage actions are written to .alert-actions."
---

# Rule event data model in the {{alerting-v2-system}} [rule-event-data-model]

This page explains what the {{alerting-v2-system}} writes, where it writes it, and how alert episode and signal documents relate.

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

Alert episodes carry three additional fields, prefixed `episode.*`, for tracking lifecycle state (`episode.id`, `episode.status`, `episode.status_count`). Alert episodes track an ongoing problem, so they carry these fields.

For the full field list, including field types and which fields apply to signals versus alert events, refer to [Field reference](field-reference.md#rule-events-field-schema).

## How {{kib}} records evaluation and triage data [how-kib-records-evaluation-triage-data]

{{kib}} writes rule output to the following append-only data streams, both managed through ILM and queryable with {{esql}} in Discover:

- **`.rule-events`** - {{kib}} writes one document for each rule evaluation and never overwrites them. This stream holds both signals and alert episode evaluations.
- **`.alert-actions`** - Records every triage action taken on an episode (for example, acknowledge, snooze, and resolve). Only alert episodes produce documents here.

## Related pages

- [Query signals](query-signals.md): Query examples against signals.
- [Query {{alerting-v2-system}} alert history in Discover](query-alerts-and-signals-in-discover.md): Episode lifecycle and triage queries.