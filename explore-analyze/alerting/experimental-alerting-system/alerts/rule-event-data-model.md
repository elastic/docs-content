---
navigation_title: Rule event data model
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "The experimental alerting system stores signals and events that belong to an alert episode in .rule-events. Episode lifecycle fields apply only to type alert. Triage actions go to .alert-actions." 
---

# Rule event data model in the {{alerting-v2-system}} [rule-event-data-model]

{{kib}} writes **rule events** to `.rule-events`. An alert episode is the grouping of those events that share an `episode.id`. This page covers where that data lives, which fields each `type` uses, and where triage actions go. For what a rule event is and how it connects to alert episodes, refer to [Rule events](../rules/rule-event-field-reference.md).

## What `type` records on each event [how-rule-mode-determines-output]

Every time a rule finds a match, {{kib}} writes a rule event to `.rule-events`. The event's `type` is either `signal` or `alert`:

| `type` | What the event represents |
| --- | --- |
| `signal` | A **signal**. Queryable in Discover for later analysis. |
| `alert` | One evaluation in an alert episode. The episode is the grouping of events that share an `episode.id`. |

:::{note}
Action policies only evaluate alert episodes, so events with `type: signal` never reach a policy or a workflow.
:::

## Shared index and schema [shared-index-and-schema]

Signals and events that belong to an alert episode share `.rule-events` and many of the same fields, including `data`, the payload from your rule's query. Filter with `WHERE type == "signal"` or `WHERE type == "alert"`.

Only `type: alert` events carry the `episode.*` fields that track lifecycle state (`episode.id`, `episode.status`, `episode.status_count`). Query those events by `episode.id` to replay an episode. Signal events don't include episode fields.

For the full field list, including field types and which fields apply to signals versus events that belong to an alert episode, refer to [Field reference](field-reference.md#rule-events-field-schema).

## How {{kib}} records evaluation and triage data [how-kib-records-evaluation-triage-data]

{{kib}} writes rule output to the following append-only data streams, both managed through [index lifecycle management (ILM)](/manage-data/lifecycle/index-lifecycle-management.md) and queryable with {{esql}} in Discover:

- **`.rule-events`** - {{kib}} writes one rule event per matching row, per run, and never overwrites them. When {{kib}} tracks an alert episode, it can also write `recovered` and `no_data` events. This stream holds signals (events with `type: signal`) and events that belong to an alert episode (`type: alert`).
- **`.alert-actions`** - Records every triage action taken on an episode (for example, acknowledge, snooze, and resolve). Only alert episodes produce documents here.

## Related pages

- [Rule events](../rules/rule-event-field-reference.md): What a rule event is and how it connects to signals and alert episodes.
- [Query signals](query-signals.md): Query examples against signals.
- [Query {{alerting-v2-system}} alert history in Discover](query-alerts-and-signals-in-discover.md): Episode lifecycle and triage queries.
