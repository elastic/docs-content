---
navigation_title: Rule authoring
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Write ES|QL detection queries for rules in Kibana's experimental alerting system. Choose Signal or Alert mode, structure base queries and conditions, and assign severity levels."
---

# Rule authoring in the {{alerting-v2-system}} [author-rules]

Rules in the {{alerting-v2-system}} use {{esql}} queries to detect problems in your data. When you create a rule, you choose whether it should fire notifications or just record matches, define the detection logic, and optionally set severity levels.

This page explains the concepts behind rule modes, detection logic, and severity. For other rule settings such as schedules, grouping, and lifecycle thresholds, refer to [Configure a rule](configure-a-rule.md). When you're ready to create a rule, use the [rule builder](create-rule-from-rule-builder.md), [YAML editor](create-rule-with-yaml.md), or [Discover](create-rule-from-discover.md).

## Rule modes

Whether a rule fires notifications or just records matches is determined by its mode. Rules can run in Signal or Alert mode. The mode available to you depends on how the rule is created.

| Mode | What it does |
| --- | --- |
| Signal | Records query matches as signals. No alert episodes, no notifications. Good for testing a query or building a data history without alerting anyone. |
| Alert | Records matches and maintains alert episodes with lifecycle states. Alert episodes appear on the **Alerts** page and can be matched by action policies for notifications. |

## Define the detection logic [esql-query-structure]

The detection logic is an {{esql}} query that tells the rule what to look for. Every query has two parts: the base query and the alert conditions.

### Base query (required)  
The base query is the main {{esql}} expression. Use `FROM` to point the rule at the indices or data streams to read. The query itself defines the scope. 

The base query shapes results with `STATS`, `WHERE`, and `EVAL`, and controls which fields are stored with `KEEP`. It runs on every evaluation, even when no match occurs, which is what enables no-data detection and recovery. The [{{esql}} reference](elasticsearch://reference/query-languages/esql.md) covers all available commands and processing functions.

### Alert conditions (optional)  
The alert conditions query is the `WHERE` clause that's applied after the base query. Only rows that pass the alert condition are treated as breaches. Without an alert condition, every row returned by the base query is a breach.

```esql
// Base query: compute average CPU per host
FROM metrics-*
| WHERE @timestamp >= ?_tstart AND @timestamp < ?_tend
| STATS avg_cpu = AVG(system.cpu.total.pct) BY host.name
// Alert condition: only rows above the threshold count as breaches
| WHERE avg_cpu > 0.9
```

The `KEEP` command controls which fields appear on each stored alert event. Only the fields you `KEEP` are available for policy matchers, grouping keys, and triage in the Alerts UI.

## Severity levels [severity-levels]

To assign severity to alert episodes, include a column named `severity` in your {{esql}} query and add it to your `KEEP` list. The framework maps it to one of five fixed levels: `info`, `low`, `medium`, `high`, or `critical`.

Severity is used by action policy matchers for routing and triage. For details on how severity is stored and made available to matchers, refer to [Configure a rule](configure-a-rule.md).

## Next steps

Once you understand the query structure, explore [{{esql}} query patterns](esql-query-patterns.md) for advanced use cases including SLO burn rate queries, no-data detection, persistent breach detection, and unsupported operations.

<!--
## Rule forms [rule-forms]

[CONTENT NEEDED for M2: UI. This page needs a procedure once rule forms are finalized: what forms are available, what each one pre-fills in the ES|QL query or YAML, and how to start from a form versus authoring a rule from scratch. Verify the name "rule forms" and the available form types against the shipped product before publishing.]
-->
