---
navigation_title: Query signals
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Query Signal mode rule events with ES|QL in Discover. Filter by rule, build dashboards from detection history, and correlate signals with Alert mode rules in the experimental alerting system."
---

# Query {{alerting-v2-system}} signals in Discover [query-signals-discover] 

When a Signal mode rule runs on its schedule, {{kib}} writes each match to `.rule-events` as a rule event with `type: signal`. That event is the signal. Signals don't open alert episodes and they skip action policy evaluation and workflow invocation. Use them to build detection history, investigate incidents in Discover, create dashboards, or feed follow-on Alert mode rules that correlate activity across sources.

This page shows how to query signals, which fields matter most, and how to turn signal history into Discover sessions and dashboards.

## Before you begin

- You have at least one rule running in [Signal mode](../rules/configure-rule-mode.md).
- Your role can query `.rule-events` in Discover. For privilege details, refer to [Configure access](../get-started/configure-access.md#alerting-data-investigation-privileges).
- You've added `.rule-events` as a data view. If you haven't, follow the steps in [Before you begin](query-alerts-and-signals-in-discover.md#add-data-views-before-begin) on the alert history page, using the `.ds-.rule-events-*` index pattern.

## Key fields for signal queries [signal-key-fields]

Alert-mode and Signal-mode rules both write to `.rule-events` and share most of the same fields. Use `type` to filter for signals only. Signal events don't include `episode.*` fields.

| Field | Why it matters for signals |
|---|---|
| `type` | Filter with `type == "signal"` to exclude Alert-mode rule events. |
| `@timestamp` | When {{kib}} wrote the document. Use for time ranges and sorting. |
| `rule.id` | Scope results to one Signal mode rule. |
| `status` | Always `breached` for signals. Signal-mode rules don't write `recovered` or `no_data`. |
| `group_hash` | Identifies the series the signal belongs to when the rule uses grouping. |
| `severity` | Optional. Set when the query emits a recognized `severity` column value. |
| `data` | Rule-defined payload from the source query. Useful for investigation and dashboards. |

For the full field list, refer to [Field reference](field-reference.md#rule-events-field-schema). For how the shared schema works conceptually, refer to [Rule event data model](rule-event-data-model.md).

## Common signal queries [common-signal-queries]

Open **Discover**, select your `.rule-events` data view, and run {{esql}} against the stream. The following examples cover common signal workflows.

### List recent signals [basic-signal-query]

Returns the most recent Signal-mode rule events across all Signal mode rules.

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

### Correlate signals in an Alert mode rule [correlate-signals-alert-rule]

Signal mode is useful on its own for investigation, and as input to an Alert mode rule that watches accumulated signals. For example, a Signal mode rule records administrator API calls. A separate Alert mode rule queries those signals and opens an episode only when call volume spikes.

Create an Alert mode rule whose query reads from `.rule-events`, filters to the Signal mode rule's output, and applies a threshold:

```esql
FROM .rule-events
| WHERE type == "signal"
  AND rule.id == "admin-api-calls"
  AND status == "breached"
| EVAL bucket = BUCKET(@timestamp, 15 minutes)
| STATS signal_count = COUNT(*) BY bucket
| WHERE signal_count > 10
```

When this Alert mode rule finds a match, {{kib}} tracks the event as an alert episode. An action policy can evaluate the episode and invoke a workflow. The underlying Signal mode rule keeps recording without paging anyone on every individual call.

:::{tip}
You can also correlate signals from more than one Signal mode rule in a single Alert mode query, for example combining administrator API call signals with error-rate signals, so neither source pages on its own.
:::

## Build a Discover session or dashboard from signals [signals-dashboards]

After you have a working signal query:

1. In **Discover**, save the search so you can reopen it during investigations.
2. Optionally create a visualization from the saved search, for example a count of signals over time broken down by `rule.id` or `severity`.
3. Add the visualization to a dashboard that your team uses for incident review.

Because `.rule-events` is append-only, dashboards show the full history retained by [index lifecycle management (ILM)](/manage-data/lifecycle/index-lifecycle-management.md), not only the current state.

## Related pages

- [Rule mode](../rules/configure-rule-mode.md): When to use Signal mode versus Alert mode.
- [Rule events](../rules/rule-event-field-reference.md): What {{kib}} writes to `.rule-events` and how a signal relates to an Alert-mode event.
- [Rule event data model](rule-event-data-model.md): Shared `.rule-events` schema for Signal-mode and Alert-mode events.
- [Query {{alerting-v2-system}} alert history in Discover](query-alerts-and-signals-in-discover.md): Episode lifecycle, triage history, and incident-tracing queries.
- [How the {{alerting-v2-system}} works](../how-it-works.md#how-signal-mode-works): End-to-end Signal mode walkthrough.
