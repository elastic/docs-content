---
navigation_title: Your first rule query
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Write your first ES|QL rule query in Kibana's experimental alerting system. Covers the minimum query structure and how to adapt it to your data."
---

# Your first rule query in the {{alerting-v2-system}} [first-rule-query]

If you're new to {{esql}} or to writing rules, this page shows the simplest query structure that a rule needs. It requires only a basic familiarity with your data.

## The simplest rule query

This query returns one row for every log entry at `ERROR` level in the lookback window. No aggregation happens. Each matching event becomes its own alert event. Use this pattern when any single occurrence of a condition is worth alerting on: any critical error log, any failed authentication attempt, any payment rejection.

```esql
FROM logs-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend  // Scope to the rule's configured lookback window
| WHERE level == "ERROR"                                // The alert condition: every match is a breach
| KEEP service.name, message, @timestamp               // Fields stored on each alert event
```

Every row the query returns is treated as a breach. If the query returns nothing, no alert fires.

### What each part does

| Part | Purpose in a rule |
| --- | --- |
| `FROM logs-*` | The index or data stream to query. |
| `WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend` | Scopes the query to the rule's lookback window. `?_tstart` and `?_tend` are bound automatically at runtime. Always include this filter to avoid scanning your entire index on every evaluation. |
| `WHERE level == "ERROR"` | The alert condition. Only rows that pass this filter generate an alert event. |
| `KEEP service.name, message, @timestamp` | The fields stored on each alert event. Only fields in `KEEP` are available for routing, grouping, and triage. |

### How to adapt this query

To use this query with your own data, change three things:

1. **Index**: Replace `logs-*` with the index or data stream that holds your data.
2. **Alert condition**: Replace `level == "ERROR"` with the field name and value that defines a breach in your data. For example: `event.outcome == "failure"`, `http.response.status_code >= 500`, or `process.name == "malware.exe"`.
3. **KEEP fields**: Replace the field list with whatever you need for triage. Include any fields you plan to use for grouping, routing, or displaying in the alert detail view.

## Other query patterns [first-rule-query-next-steps]

This pattern alerts on individual events. If you want to alert only when a count or rate crosses a threshold rather than on individual occurrences, the [threshold query pattern](esql-threshold-queries.md) is the next step.
