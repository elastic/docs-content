---
navigation_title: ES|QL query
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "How to structure the ES|QL detection query for a rule in the experimental alerting system. Covers the base query, the optional alert condition that gates which rows become breaches, and dynamic parameters for time bounds and configurable thresholds."
---

# {{esql}} query in the {{alerting-v2-system}} [esql-query-rule]

Every rule in the {{alerting-v2-system}} uses an {{esql}} query to define what to evaluate. The query consists of a base query that shapes and filters the data and an optional alert condition that determines which rows become alert events. For more advanced use cases, the query also supports [dynamic values](#dynamic-query-values) for filtering by the evaluation window or setting configurable thresholds through the rule form.

## Base query [query-base]

The base query is the main {{esql}} expression. Use `FROM` to point the rule at the indices or data streams to read. Shape results with `STATS`, `WHERE`, and `EVAL`, and control which fields are stored with `KEEP`. The base query runs on every evaluation, even when no match occurs, which is what enables no-data detection and recovery. The [{{esql}} reference](elasticsearch://reference/query-languages/esql.md) covers all available commands and processing functions.

This query counts HTTP 5xx errors per service over the lookback window and stores only the fields needed for triage.

```esql
FROM logs-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS error_count = COUNT_IF(http.response.status_code >= 500) BY service.name
| KEEP service.name, error_count
```

Without an alert condition, every row returned by this query is treated as a breach, so the rule fires for every service that logged at least one 5xx error.

## Alert condition [query-alert-condition]

The alert condition is an optional `WHERE` clause appended after the base query. Only rows that pass the condition are treated as breaches. Use an alert condition when the base query returns aggregate results and you only want to alert when a value crosses a threshold.

This example extends the base query above to only fire when a service exceeds 10 errors.

```esql
FROM logs-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS error_count = COUNT_IF(http.response.status_code >= 500) BY service.name
| KEEP service.name, error_count
// Alert condition: only services with more than 10 errors become breaches
| WHERE error_count > 10
```

The `KEEP` command controls which fields appear on each stored alert event. Only the fields in `KEEP` are available for action policy matchers, grouping keys, and triage.

You don't have to write the base query and alert condition as two separate steps yourself. When writing {{esql}} directly, the query sandbox can [derive this split automatically](create-esql-rule.md#sandbox-split-editor) from a single query, or you can switch to manual control over the split.

## When to add an alert condition [query-when-to-use]

Add an alert condition when:

* Your base query returns aggregate results (for example, counts or averages per group) and you only want to alert when a value crosses a specific threshold. Without an alert condition, every row returned by the base query is treated as a breach.
* You want to keep filtering logic out of the base query and express the threshold separately for clarity.

Skip the alert condition when:

* Every row returned by the base query should be treated as a breach. This applies when the query filters directly for specific error events where any match warrants attention.
* All filtering can be expressed cleanly in a single `WHERE` clause without a two-stage query.

## Use dynamic values in your rule query [dynamic-query-values]

{{esql}} rule queries support two kinds of parameters that make queries more dynamic. The executor injects time bounds automatically, and you define form variables when creating a rule. You don't need either to write a working rule, but they're useful for scoping queries precisely to the evaluation window or making thresholds configurable without editing the query.

### Filter your query to the evaluation window (`?_tstart` and `?_tend`) [time-bound-parameters]

`?_tstart` and `?_tend` are reserved parameter names that the rule executor binds automatically on every evaluation. They hold the start and end timestamps of the lookback window, so you can scope a query to exactly the period the rule is evaluating.

```esql
FROM logs-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS error_count = COUNT(*) BY service.name
| WHERE error_count > 10
```

These parameters work across all rule creation methods.

### Set configurable values in the rule form (`?param`) [form-variables]

When creating a rule through the form, you can use `?param` placeholders, such as `?threshold`, as {{esql}} Control variables. The form resolves these variables and embeds their values into the query before saving. The stored rule and the YAML representation of it contains the resolved values, not the placeholder tokens.

## Examples

### Scoping a query to the evaluation window

This query counts HTTP errors per service over the rule's lookback window. `?_tstart` and `?_tend` are bound automatically at runtime, so the query always covers exactly the configured window regardless of when the rule runs.

```esql
FROM logs-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS error_count = COUNT_IF(http.response.status_code >= 500) BY service.name
| WHERE error_count > 0
| KEEP service.name, error_count
```

If you omit the time filter, the query scans the full index on every evaluation, which increases query cost and can return stale matches from earlier runs.

### Using a form variable for a configurable threshold

This query uses `?threshold` as a form variable so the threshold can be set in the rule form UI without editing the query directly. When the rule is saved, the form resolves `?threshold` to its configured value and embeds it. The stored query contains the literal number, not the placeholder.

```esql
FROM logs-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS p99_latency = PERCENTILE(http.response_time, 99) BY service.name
| WHERE p99_latency > ?threshold
| KEEP service.name, p99_latency
```

Because `?threshold` is resolved before saving, YAML and API representations of this rule always show the resolved value.
