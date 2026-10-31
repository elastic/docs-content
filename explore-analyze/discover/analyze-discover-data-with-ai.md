---
navigation_title: Analyze data with AI
applies_to:
  serverless: preview
  stack: preview 9.5
products:
  - id: kibana
type: how-to
description: Ask an AI agent to analyze the full dataset behind your Discover ES|QL query, chart the main finding, and suggest drill-down queries.
---

# Analyze your data with AI in Discover


**Discover** integrates with [{{agent-builder}}](../ai-features/elastic-agent-builder.md) to provide AI-powered analysis of your {{esql}} query results. The [`discover-data-analysis` skill](../ai-features/agent-builder/builtin-skills-reference.md#agent-builder-discover-data-analysis-skill) runs aggregation queries against the full dataset behind your current view, renders a chart for the main finding, and proposes drill-down queries you can run in a new tab.

This feature is available only when **Discover** is in [{{esql}} mode](use-esql.md). To write or fix the query itself with AI, use the [AI assistance in the {{esql}} editor](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-ai-assistance).

To start an analysis:

1. Switch to {{esql}} mode and run a query so results are loaded in the table.
2. Select the **AI Agent** button in the {{kib}} header, or press {kbd}`cmd+;` (Mac) / {kbd}`ctrl+;` (Windows and Linux), to open the agent chat.

   The agent automatically receives your current query, columns, sample rows, and time range as context.

3. Ask the agent to analyze your data. For example, prompt it with `analyze this data` or a more specific question.
4. Review the agent's findings, the inline visualization, and the suggested drill-down queries.

You can also ask the agent for follow-up analyses, including correlations between fields, time-over-time comparisons, and field statistics for specific columns.

{applies_to}`serverless: preview` {applies_to}`stack: preview 9.6+` To see the current documents without leaving the conversation, ask the agent to show them in an interactive **Discover** table. Refer to [Discover tables in chat](../ai-features/agent-builder/agent-builder-discover-tables.md).

## Context-aware deep analysis

When your data matches one of the [context-aware experiences](discover-get-started.md#context-aware-discover), the agent receives shape-specific guidance so the analysis is tailored to the data type:

* **Logs**: Groups by `log.level`, `service.name`, `host.name`, and `event.dataset`. It surfaces error and warning frequency and shifts in level distribution.
* **Metrics**: Uses the {{esql}} `TS` source command for time series data streams, runs `TS_INFO` first to discover metric names, types, and dimension fields, then aggregates with the right function for each metric type (`RATE` or `SUM` for counters, `AVG`, `MAX`, `MIN`, or `PERCENTILE` for gauges, `PERCENTILE` for histograms).
* **APM traces**: Focuses on latency percentiles of transaction and span durations, throughput by transaction or span name, and error rate by `event.outcome`.
* **OTel traces**: Focuses on latency percentiles of `duration`, throughput by service and span kind, and error rate by `status.code`.

If your query doesn't match any context-aware profile, the agent infers the analysis strategy from the column names and types in the results instead.

## Related pages

- [Discover tables in chat](../ai-features/agent-builder/agent-builder-discover-tables.md)
- [Introduction to Discover](discover-get-started.md)
