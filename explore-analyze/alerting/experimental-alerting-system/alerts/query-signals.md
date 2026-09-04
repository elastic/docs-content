---
navigation_title: Query signals
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Query rule events with type signal using ES|QL in Discover. Filter by rule, build dashboards from detection history, and use them as input to a rule that opens an episode."
---

# Query {{alerting-v2-system}} signals in Discover [query-signals-discover] 

Use {{esql}} in Discover to query `.rule-events` for events with `type: signal`. This page covers the fields to filter on, example queries, and how to save that history as a Discover session or dashboard.

## Before you begin

- You have at least one rule that writes events with `type: signal`. For how that is set, refer to [Rule mode](../rules/configure-rule-mode.md).
- Your role can query `.rule-events` in Discover. For privilege details, refer to [Configure access](../get-started/configure-access.md#alerting-data-investigation-privileges).

The examples on this page use {{esql}} (`FROM .rule-events`). You don't need a data view for those queries. If you query `.rule-events` with KQL instead, add it as a data view first. Follow the steps in [Before you begin](query-alerts-and-signals-in-discover.md#add-data-views-before-begin) on the alert history page, using the `.ds-.rule-events-*` index pattern.

## Key fields for these queries [signal-key-fields]

These fields matter most when you query `.rule-events`. Filter with `type == "signal"` to exclude events that belong to an alert episode.

| Field | Why it matters |
|---|---|
| `type` | Filter with `type == "signal"` to exclude events that belong to an alert episode. |
| `@timestamp` | When {{kib}} wrote the document. Use for time ranges and sorting. |
| `rule.id` | Scope results to one rule. |
| `status` | Always `breached` for events with `type: signal`. These events don't include `recovered` or `no_data`. |
| `group_hash` | Identifies the series the event belongs to when the rule uses grouping. |
| `severity` | Optional. Set when the query emits a recognized `severity` column value. |
| `data` | Rule-defined payload from the source query. Useful for investigation and dashboards. |

For the full field list, refer to [Field reference](field-reference.md#rule-events-field-schema). For how the shared schema works conceptually, refer to [Rule event data model](rule-event-data-model.md).

## Common queries [common-signal-queries]

Open **Discover** and run {{esql}} against `.rule-events`. The following examples cover common workflows.

### List recent events [basic-signal-query]

Returns the most recent events with `type: signal`.

```esql
FROM .rule-events
| WHERE type == "signal"
| SORT @timestamp DESC
| KEEP @timestamp, rule.id, status, severity, group_hash, data
| LIMIT 100
```

### Scope events to one rule [signals-by-rule]

Returns events with `type: signal` from a single rule. Replace `my-signal-rule-id` with the rule's ID.

```esql
FROM .rule-events
| WHERE type == "signal" AND rule.id == "my-signal-rule-id"
| SORT @timestamp DESC
| KEEP @timestamp, status, severity, group_hash, data
```

### Correlate events in a follow-on rule [correlate-signals-alert-rule]

Events with `type: signal` are useful for investigation, and as input to a rule that watches accumulated events and groups matches into an episode. For example, one rule records administrator API calls. A separate rule queries those events and groups matches into an episode only when call volume spikes.

Create a rule whose query reads from `.rule-events`, filters to the first rule's events with `type: signal`, and applies a threshold:

```esql
FROM .rule-events
| WHERE type == "signal"
  AND rule.id == "admin-api-calls"
  AND status == "breached"
| EVAL bucket = BUCKET(@timestamp, 15 minutes)
| STATS event_count = COUNT(*) BY bucket
| WHERE event_count > 10
```

When this follow-on rule finds a match, {{kib}} writes a rule event and groups it into an alert episode. An action policy can evaluate the episode and invoke a workflow. The first rule keeps recording without paging anyone on every individual call.

:::{tip}
You can also correlate events from more than one rule in a single query, for example combining administrator API call events with error-rate events, so neither source pages on its own.
:::

## Build a Discover session or dashboard [signals-dashboards]

After you have a working query:

1. In **Discover**, save the search so you can reopen it during investigations.
2. Optionally create a visualization from the saved search, for example a count of events over time broken down by `rule.id` or `severity`.
3. Add the visualization to a dashboard that your team uses for incident review.

Because `.rule-events` is append-only, dashboards show the full history retained by [index lifecycle management (ILM)](/manage-data/lifecycle/index-lifecycle-management.md), not only the current state.

## Related pages

- [Rule mode](../rules/configure-rule-mode.md): How configuration determines whether {{kib}} groups matches into an alert episode or keeps them available for later analysis.
- [Rule events](../rules/rule-event-field-reference.md): What {{kib}} writes to `.rule-events` and how `type` relates to episodes.
- [Rule event data model](rule-event-data-model.md): Shared `.rule-events` schema for `signal` and `alert` events.
- [Query {{alerting-v2-system}} alert history in Discover](query-alerts-and-signals-in-discover.md): Episode lifecycle, triage history, and incident-tracing queries.
- [How the {{alerting-v2-system}} works](../how-it-works.md#how-signal-mode-works): End-to-end walkthrough of the path where a rule writes events with `type: signal` for later analysis.
