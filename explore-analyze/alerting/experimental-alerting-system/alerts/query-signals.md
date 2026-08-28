---
navigation_title: Query signals
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Query signals with ES|QL in Discover. Filter by rule, build dashboards from detection history, and use signals as input to a rule that opens an episode."
---

# Query {{alerting-v2-system}} signals in Discover [query-signals-discover] 

Use {{esql}} in Discover to query signals in `.rule-events`. This page covers the fields to filter on, example queries, and how to save that history as a Discover session or dashboard.

## Before you begin

- You have at least one rule that writes signals. For how that is set, refer to [Rule mode](../rules/configure-rule-mode.md).
- Your role can query `.rule-events` in Discover. For privilege details, refer to [Configure access](../get-started/configure-access.md#alerting-data-investigation-privileges).

The examples on this page use {{esql}} (`FROM .rule-events`). You don't need a data view for those queries. If you query `.rule-events` with KQL instead, add it as a data view first. Follow the steps in [Before you begin](query-alerts-and-signals-in-discover.md#add-data-views-before-begin) on the alert history page, using the `.ds-.rule-events-*` index pattern.

## Key fields for signal queries [signal-key-fields]

These fields matter most when you query `.rule-events` for signals. Filter with `type == "signal"`.

| Field | Why it matters for signals |
|---|---|
| `type` | Filter with `type == "signal"` to exclude events that belong to an alert episode. |
| `@timestamp` | When {{kib}} wrote the document. Use for time ranges and sorting. |
| `rule.id` | Scope results to one rule. |
| `status` | Always `breached` for signals. These events don't include `recovered` or `no_data`. |
| `group_hash` | Identifies the series the signal belongs to when the rule uses grouping. |
| `severity` | Optional. Set when the query emits a recognized `severity` column value. |
| `data` | Rule-defined payload from the source query. Useful for investigation and dashboards. |

For the full field list, refer to [Field reference](field-reference.md#rule-events-field-schema). For how the shared schema works conceptually, refer to [Rule event data model](rule-event-data-model.md).

## Common signal queries [common-signal-queries]

Open **Discover** and run {{esql}} against `.rule-events`. The following examples cover common signal workflows.

### List recent signals [basic-signal-query]

Returns the most recent events with `type: signal`.

```esql
FROM .rule-events
| WHERE type == "signal"
| SORT @timestamp DESC
| KEEP @timestamp, rule.id, status, severity, group_hash, data
| LIMIT 100
```

### Scope signals to one rule [signals-by-rule]

Returns signals from a single rule. Replace `my-signal-rule-id` with the rule's ID.

```esql
FROM .rule-events
| WHERE type == "signal" AND rule.id == "my-signal-rule-id"
| SORT @timestamp DESC
| KEEP @timestamp, status, severity, group_hash, data
```

### Correlate signals in a follow-on rule [correlate-signals-alert-rule]

Signals are useful for investigation, and as input to a rule that watches accumulated signals and groups matches into an episode. For example, one rule records administrator API calls. A separate rule queries those signals and groups matches into an episode only when call volume spikes.

Create a rule whose query reads from `.rule-events`, filters to the first rule's signals, and applies a threshold:

```esql
FROM .rule-events
| WHERE type == "signal"
  AND rule.id == "admin-api-calls"
  AND status == "breached"
| EVAL bucket = BUCKET(@timestamp, 15 minutes)
| STATS signal_count = COUNT(*) BY bucket
| WHERE signal_count > 10
```

When this follow-on rule finds a match, {{kib}} writes a rule event and groups it into an alert episode. An action policy can evaluate the episode and invoke a workflow. The first rule keeps recording without paging anyone on every individual call.

:::{tip}
You can also correlate signals from more than one rule in a single query, for example combining administrator API call signals with error-rate signals, so neither source pages on its own.
:::

## Build a Discover session or dashboard from signals [signals-dashboards]

After you have a working signal query:

1. In **Discover**, save the search so you can reopen it during investigations.
2. Optionally create a visualization from the saved search, for example a count of signals over time broken down by `rule.id` or `severity`.
3. Add the visualization to a dashboard that your team uses for incident review.

Because `.rule-events` is append-only, dashboards show the full history retained by [index lifecycle management (ILM)](/manage-data/lifecycle/index-lifecycle-management.md), not only the current state.

## Related pages

- [Rule mode](../rules/configure-rule-mode.md): How configuration determines whether {{kib}} groups matches into an alert episode or leaves them as signals.
- [Rule events](../rules/rule-event-field-reference.md): What {{kib}} writes to `.rule-events` and how a signal relates to an event in an episode.
- [Rule event data model](rule-event-data-model.md): Shared `.rule-events` schema for `signal` and `alert` events.
- [Query {{alerting-v2-system}} alert history in Discover](query-alerts-and-signals-in-discover.md): Episode lifecycle, triage history, and incident-tracing queries.
- [How the {{alerting-v2-system}} works](../how-it-works.md#how-signal-mode-works): End-to-end walkthrough of the path where a rule writes signals for later analysis.
