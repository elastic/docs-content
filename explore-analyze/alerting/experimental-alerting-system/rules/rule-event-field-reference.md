---
navigation_title: Rule events
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Rule events are the append-only documents Kibana writes to .rule-events for every matching row. Use them to replay alert episodes, investigate events that aren't part of an episode, and build dashboards in the experimental alerting system."
---

# Rule events in the {{alerting-v2-system}} [rule-reference]

When a rule finds a match, {{kib}} writes a **rule event** to `.rule-events`. Each matching row in a run becomes its own event, and {{kib}} never overwrites those events. The rule's configuration determines whether that event is grouped into an alert episode. Events that aren't part of an episode have `type: signal`.

Use this page to query `.rule-events` with confidence: replay an episode's history, investigate events with `type: signal`, or build dashboards from rule output. For the stored schema, refer to [Rule event data model](../alerts/rule-event-data-model.md). For the complete field list, refer to [Field reference](../alerts/field-reference.md#rule-events-field-schema).

:::{important}
The `.rule-events` and `.alert-actions` data streams are [system indices](/reference/glossary/index.md#glossary-system-index). {{kib}} manages their versioning, retention, and lifecycle through [index lifecycle management (ILM)](/manage-data/lifecycle/index-lifecycle-management.md). Older backing indices are deleted automatically when the retention window expires. Do not change mappings or index settings for these streams yourself.
:::

## What a rule event is [what-is-a-rule-event]

A rule event is the record of one result from one rule run. {{kib}} writes one event per matching row, per run, to `.rule-events`. It never updates those events in place. Each event is a snapshot of that moment: the rule that produced it, the payload from your query (`data`), and a `type` of `signal` or `alert`.

Most events come from a matching row (`status: breached`). When {{kib}} tracks an alert episode, it can also write events when the condition clears (`status: recovered`) or when the query finds no data (`status: no_data`). {{kib}} writes those events the same way: one new document, never an overwrite.

Each event has a `type` of `signal` or `alert`, matching the `kind` you set when you created the rule. For how `kind` is set, refer to [Rule mode](configure-rule-mode.md).

## Which events are grouped into an episode [rule-events-by-mode]

| `type` | What {{kib}} writes | What you work with |
| --- | --- | --- |
| `signal` | A rule event with no `episode.*` fields. | Queryable in Discover. |
| `alert` | A rule event with `episode.*` fields. | An alert episode: the grouping of events that share an `episode.id`, visible on the **Alerts** page. |

### Events that stay available for later analysis (`type: signal`)

{{kib}} writes a rule event with `type: signal`. These events stay in `.rule-events`. They don't appear on **Alerts** and aren't evaluated by action policies or lifecycle triggers. They are queryable in Discover.

For query examples, refer to [Query signals](../alerts/query-signals.md).

### Events that form an alert episode (`type: alert`)

Events with `type: alert` carry `episode.id`, `episode.status`, and `episode.status_count`. An **alert episode** is the grouping of those events that share an `episode.id`.

The first event opens the episode. Later events from later runs advance it through lifecycle states until the condition clears. Because events are never overwritten, `episode.status` on a given event is the lifecycle stage at that evaluation, not a live field that {{kib}} updates later. To replay an episode, query every event with that `episode.id`.

Go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Alerts** to view the current state of each episode.

## Query `.rule-events` to replay an episode [query-rule-events]

The `.rule-events` data stream is append-only. {{kib}} writes a new document on every matching row of every run. Existing documents are never updated. To view the full history of an episode, query `.rule-events` filtered by `episode.id`:

```esql
FROM .rule-events
| WHERE episode.id == "<episode-id>"
| SORT @timestamp ASC
```

For query examples for events with `type: signal`, refer to [Query signals](../alerts/query-signals.md). For lifecycle replay and incident tracing, refer to [Query alert history in Discover](../alerts/query-alerts-and-signals-in-discover.md).

## Related pages

- [{{esql}} query](configure-rule-query.md): How the base query and alert condition shape what's written to `.rule-events`.
- [Rules](../rules.md): What rules do and how they fit into the broader {{alerting-v2-system}}.
- [Rule mode](configure-rule-mode.md): How Rule mode determines whether {{kib}} groups each rule event into an alert episode or keeps it available for later analysis.
- [Query signals](../alerts/query-signals.md): Query events with `type: signal` in Discover and use them as input to a rule that opens an episode.
- [View and manage alerts](../alerts/view-and-manage-alerts.md): Where lifecycle-tracked episodes appear in the UI, with triage actions and episode details.
