---
navigation_title: Rule event data model
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Signal and alert rule events share the .rule-events data stream and most fields. Alert events add episode.* lifecycle fields; triage actions go to .alert-actions."
---

# Rule event data model in the {{alerting-v2-system}} [rule-event-data-model]

This page explains how Signal mode and Alert mode rule events relate, and where {{kib}} stores them.

## How rule mode determines what gets written [how-rule-mode-determines-output]

Every time a rule finds a match, it writes a [rule event](../rules/rule-event-field-reference.md) to `.rule-events`. Whether that event is a signal or an alert depends on the rule's mode. Both kinds share the same data stream and most of the same fields.

| Type | What it is | When it's created |
| --- | --- | --- |
| Signal | A `type: signal` rule event. A point-in-time record that the query matched. | Rules in Signal mode |
| Alert | A `type: alert` rule event with `episode.*` fields. Events that share `episode.id` form an alert episode. | Rules in Alert mode |

:::{note}
A rule in Signal mode only writes signals. It never opens alert episodes, so action policies have nothing to match against.
:::

## Shared index and schema [shared-index-and-schema]

Alert episodes and signals are both written to `.rule-events` as rule events and share many of the same fields, including `data`, which holds the payload from your rule's query. The `type` field tells you which kind of rule event you're looking at, `signal` or `alert`, so you can filter for one or the other in a query (for example, `WHERE type == "signal"`).

Alert-mode rule events carry three additional fields, prefixed `episode.*`, for tracking lifecycle state (`episode.id`, `episode.status`, `episode.status_count`). Those fields group events that share an `episode.id` into an alert episode. Signal events don't include them.

For the full field list, including field types and which fields apply to signals versus alert events, refer to [Field reference](field-reference.md#rule-events-field-schema).

## How {{kib}} records evaluation and triage data [how-kib-records-evaluation-triage-data]

{{kib}} writes rule output to the following append-only data streams, both managed through ILM and queryable with {{esql}} in Discover:

- **`.rule-events`** - {{kib}} writes one document per result row, per rule run, and never overwrites them. This stream holds both `type: signal` and `type: alert` rule events.
- **`.alert-actions`** - Records every triage action taken on an episode (for example, acknowledge, snooze, and resolve). Only alert episodes produce documents here.

## Related pages

- [Rule events](../rules/rule-event-field-reference.md): What a rule event is and how Signal mode and Alert mode use those events.
- [Observe and analyze signals](../observe-and-analyze-signals.md): Query examples against signals.
- [Query {{alerting-v2-system}} alert history in Discover](query-alerts-and-signals-in-discover.md): Episode lifecycle and triage queries.