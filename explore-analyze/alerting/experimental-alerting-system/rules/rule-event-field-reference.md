---
navigation_title: Rule events
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How Kibana records rule matches as rule events in the experimental alerting system, and how Signal mode and Alert mode use those events."
---

# Rule events in the {{alerting-v2-system}} [rule-reference]

When a rule's query finds a match, {{kib}} records it as a rule event in `.rule-events`. One run can write several events if the query returns more than one matching row. {{kib}} never overwrites a rule event. Each later run adds new events, so you can look back at every match the rule found.

This page explains what a rule event is and how Signal mode and Alert mode use those events. For how the shared schema works conceptually, refer to [Rule event data model](../alerts/rule-event-data-model.md). For the complete field list, refer to [Field reference](../alerts/field-reference.md#rule-events-field-schema).

:::{important}
The `.rule-events` and `.alert-actions` data streams are [system indices](/reference/glossary/index.md#glossary-system-index). {{kib}} manages their versioning, retention, and lifecycle through [index lifecycle management (ILM)](/manage-data/lifecycle/index-lifecycle-management.md). Older backing indices are deleted automatically when the retention window expires. Do not change mappings or index settings for these streams yourself.
:::

## How rule events connect to signals and alert episodes [rule-events-signals-episodes]

The rule's mode determines what happens after {{kib}} writes the event. Both kinds share `.rule-events` and most fields. The `type` field is `signal` or `alert`.

- **Signal mode**: Each match is a `type: signal` rule event. That event is the whole output. It has no `episode.*` fields, doesn't open an alert episode, and doesn't trigger notifications. Query these events in Discover, build dashboards from them, or feed them into a follow-on Alert mode rule. Refer to [Observe and analyze signals](../observe-and-analyze-signals.md).
- **Alert mode**: Each match is a `type: alert` rule event with `episode.*` fields. An [alert episode](../alerts.md) is the grouping of those events that share the same `episode.id` as the problem moves through `pending`, `active`, `recovering`, and `inactive`. Action policies evaluate the episode, not each individual event.

Alert mode rules also write new rule events when a series recovers or reports no data. Those events still belong to the episode and can move it to `recovering` or `inactive`.

## Append-only history [rule-events-append-only]

The `.rule-events` data stream is append-only. {{kib}} writes a new document on every rule evaluation that produces a result. Existing documents are never updated. Each document is a snapshot of that moment.

For an alert episode, `episode.status` records the lifecycle stage at that evaluation. To see the full history of an episode, query `.rule-events` filtered by `episode.id`:

```esql
FROM .rule-events
| WHERE episode.id == "<episode-id>"
| SORT @timestamp ASC
```

For signal-focused query examples, refer to [Observe and analyze signals](../observe-and-analyze-signals.md). For lifecycle replay and incident tracing, refer to [Query alert history in Discover](../alerts/query-alerts-and-signals-in-discover.md).

## Related pages

- [{{esql}} query](configure-rule-query.md): How the base query and alert condition shape what's written to `.rule-events`.
- [Rules](../rules.md): What rules do and how they fit into the broader {{alerting-v2-system}}.
- [How the {{alerting-v2-system}} works](../how-it-works.md): End-to-end Alert mode and Signal mode walkthroughs, both starting from a rule event.
- [Observe and analyze signals](../observe-and-analyze-signals.md): Query Signal mode output in Discover and correlate signals with Alert mode rules.
- [View and manage alerts](../alerts/view-and-manage-alerts.md): Where lifecycle-tracked episodes appear in the UI, with triage actions and episode details.
