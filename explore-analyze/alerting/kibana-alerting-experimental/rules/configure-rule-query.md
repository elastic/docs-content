---
navigation_title: ES|QL query
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Configure the ES|QL query and query parameters for rules in Kibana's experimental alerting system."
---

# {{esql}} query in the {{alerting-v2-system}} [esql-query-rule]

Every rule in the {{alerting-v2-system}} uses an {{esql}} query to define what to evaluate. The query has two parts: a base query that shapes and filters the data, and an optional alert condition that determines which rows become alert events. Refer to [{{esql}} query structure](author-rules.md#esql-query-structure) for how the base and alert queries interact.

## Query parameters [query-parameters]

Two types of parameters are available in {{esql}} rule queries: reserved runtime parameters and UI form variables.

**Reserved runtime parameters**

The executor automatically binds `?_tstart` and `?_tend` to the lookback window start and end timestamps on every rule evaluation. Use these to filter your query to the evaluation window:

```esql
FROM logs-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS error_count = COUNT(*) BY service.name
| WHERE error_count > 10
```

These are the only parameters supported across all rule creation methods (rule form, YAML editor, and API).

**Rule form variables**

The rule form supports additional `?param` placeholders, such as `?threshold`, through ES|QL Control variables. The form resolves these variables and inlines their values into the query string before saving. The stored rule and any API or YAML representation contain the resolved values, not the placeholder tokens.

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

This query uses `?threshold` as a form variable so the threshold can be set in the rule form UI without editing the query directly. When the rule is saved, the form resolves `?threshold` to its configured value and inlines it. The stored query contains the literal number, not the placeholder.

```esql
FROM logs-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS p99_latency = PERCENTILE(http.response_time, 99) BY service.name
| WHERE p99_latency > ?threshold
| KEEP service.name, p99_latency
```

Because `?threshold` is resolved before saving, YAML and API representations of this rule always show the resolved value.
