---
navigation_title: Rule events
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Rule events are the append-only documents Kibana writes to .rule-events for every matching row. Use them to replay alert episodes, investigate signals, and build dashboards in the experimental alerting system."
---

# Rule events in the {{alerting-v2-system}} [rule-reference]

When a scheduled rule run finds a match, {{kib}} writes a **rule event** to `.rule-events`. Each matching row in a run becomes its own event, and {{kib}} never overwrites those events. Signal mode and Alert mode both begin from this same document. Based on the rule's mode, {{kib}} either records the event as a signal or tracks it as an alert episode.

Use this page to query `.rule-events` with confidence: replay an episode's history, investigate a signal, or build dashboards from rule output. For the stored schema, refer to [Rule event data model](../alerts/rule-event-data-model.md). For the complete field list, refer to [Field reference](../alerts/field-reference.md#rule-events-field-schema).

:::{important}
The `.rule-events` and `.alert-actions` data streams are [system indices](/reference/glossary/index.md#glossary-system-index). {{kib}} manages their versioning, retention, and lifecycle through [index lifecycle management (ILM)](/manage-data/lifecycle/index-lifecycle-management.md). Older backing indices are deleted automatically when the retention window expires. Do not change mappings or index settings for these streams yourself.
:::

## What a rule event is [what-is-a-rule-event]

A rule event is the record of one result from one rule run. {{kib}} writes one event per matching row, per run, to `.rule-events`. It never updates those events in place. Each event is a snapshot of that moment: the rule that produced it, the payload from your query (`data`), and a `type` of `signal` or `alert`.

Most events come from a matching row (`status: breached`). For Alert-mode rules, {{kib}} can also write events when the condition clears (`status: recovered`) or when the query finds no data (`status: no_data`). {{kib}} writes those events the same way: one new document, never an overwrite.

The `type` field on a rule event isn't the same as the `kind` field on the rule. `kind` is how you configure the rule (Signal mode or Alert mode). `type` is what that run wrote. For how `kind` is set, refer to [Rule mode](configure-rule-mode.md).

## How Signal mode and Alert mode use rule events [rule-events-by-mode]

| Mode | What {{kib}} writes | What you work with |
| --- | --- | --- |
| Signal | A rule event with `type: signal`. No `episode.*` fields. | The event itself. That event is the signal. |
| Alert | A rule event with `type: alert` and `episode.*` fields. | An alert episode: the grouping of events that share an `episode.id`, visible on the **Alerts** page. |

### Signal mode

In Signal mode, the rule event is the whole output. {{kib}} writes it and stops. Signals don't open an episode, don't appear on the **Alerts** page, and skip action policy evaluation and workflow invocation. They accumulate in `.rule-events` and are queryable in Discover.

For query examples, refer to [Query signals](../alerts/query-signals.md).

### Alert mode

In Alert mode, the rule event isn't the episode. The event carries `episode.id`, `episode.status`, and `episode.status_count`. An **alert episode** is the grouping of those events that share an `episode.id`. There's no separate episode document type.

The first event opens the episode. Later events from later runs advance it through lifecycle states until the condition clears. Because events are never overwritten, `episode.status` on a given event is the lifecycle stage at that evaluation, not a live field that {{kib}} updates later. To replay an episode, query every event with that `episode.id`.

Go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Alerts** to view the current state of each episode.

## Query the append-only stream [query-rule-events]

The `.rule-events` data stream is append-only. {{kib}} writes a new document on every matching row of every run. Existing documents are never updated. To view the full history of an episode, query `.rule-events` filtered by `episode.id`:

```esql
FROM .rule-events
| WHERE episode.id == "<episode-id>"
| SORT @timestamp ASC
```

For signal-focused query examples, refer to [Query signals](../alerts/query-signals.md). For lifecycle replay and incident tracing, refer to [Query alert history in Discover](../alerts/query-alerts-and-signals-in-discover.md).

## Related pages

- [{{esql}} query](configure-rule-query.md): How the base query and alert condition shape what's written to `.rule-events`.
- [Rules](../rules.md): What rules do and how they fit into the broader {{alerting-v2-system}}.
- [Rule mode](configure-rule-mode.md): How Signal mode and Alert mode determine whether {{kib}} records each rule event as a signal or tracks it as an alert episode.
- [Query signals](../alerts/query-signals.md): Query Signal mode output in Discover and correlate signals with Alert mode rules.
- [View and manage alerts](../alerts/view-and-manage-alerts.md): Where lifecycle-tracked episodes appear in the UI, with triage actions and episode details.
