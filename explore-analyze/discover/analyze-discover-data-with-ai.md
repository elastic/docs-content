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

If you want to know what is behind your {{esql}} results without writing the aggregation queries yourself, you can ask an AI agent. An agent is an AI assistant that answers questions about your data in a chat. In **Discover**, the agent runs aggregation queries on the full data behind your results, charts the main finding, and suggests follow-up queries. If your query already aggregates the data, for example with `STATS`, the agent works from the rows shown instead and runs at most one extra query. It does this with the [`discover-data-analysis` skill](../ai-features/agent-builder/builtin-skills-reference.md#agent-builder-discover-data-analysis-skill), a built-in set of instructions and tools for this task. [{{agent-builder}}](../ai-features/elastic-agent-builder.md) provides the agents and skills.

## Before you begin

- Make sure **Discover** is in {{esql}} mode. Classic mode doesn't support this functionality. To switch, refer to [Switch to Discover's {{esql}} mode](switch-esql-mode.md#switch-discover-query-mode).
- Make sure {{agent-builder}} is available for your deployment or project. On {{stack}}, it requires an Enterprise [subscription](https://www.elastic.co/pricing). On {{serverless-short}}, it requires the appropriate [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md#project-features-add-ons). The agent also needs an AI model to answer with. {{ech}} and {{serverless-short}} include preconfigured models. On other deployments, configure a model first. Refer to [Get started with {{agent-builder}}](../ai-features/agent-builder/get-started.md).
- Run a query so results are loaded in the table.

## Start an analysis

1. Select the **AI Agent** button in the {{kib}} header, or press {kbd}`cmd+;` (Mac) or {kbd}`ctrl+;` (Windows and Linux), to open the agent chat.

   The agent automatically receives your current query, columns, sample rows, and time range as context.

2. Ask the agent to analyze your data. For example, enter `analyze this data`, or ask a more specific question such as `Which hosts have the most errors?`.
3. Review the agent's findings, the inline visualization, and the suggested drill-down queries. A drill-down query narrows the analysis to one group or value. Each query comes with a copy button. To run one in a new **Discover** tab, ask the agent to open it.

**Result:** The agent answers in the chat with its findings, a chart of the main result, and suggested queries.

After the first answer, keep asking. For example, ask whether two fields are related, how this week compares with last week, or what the values in one column look like.

## How the analysis adapts to your data [context-aware-deep-analysis]

When your data matches one of the [context-aware experiences](discover-get-started.md#context-aware-discover), the agent receives guidance for that type of data, so the analysis fits it:

- **Logs**: Groups by `log.level`, `service.name`, `host.name`, and `event.dataset`. It surfaces error and warning frequency and shifts in level distribution.
- **Metrics**: Uses the {{esql}} `TS` source command for time series data streams, runs `TS_INFO` first to discover metric names, types, and dimension fields, then aggregates with the right function for each metric type (`RATE` or `SUM` for counters, `AVG`, `MAX`, `MIN`, or `PERCENTILE` for gauges, `PERCENTILE` for histograms).
- **Application performance monitoring (APM) traces**: Focuses on latency percentiles of transaction and span durations, throughput by transaction or span name, and error rate by `event.outcome`.
- **OpenTelemetry (OTel) traces**: Focuses on latency percentiles of `duration`, throughput by service and span kind, and error rate by `status.code`.

If your query doesn't match any of those experiences, the agent infers the analysis strategy from the column names and types in the results instead.

## Next steps

- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.6+` To see the current documents without leaving the conversation, ask the agent to show them in an interactive **Discover** table. Refer to [Discover tables in chat](../ai-features/agent-builder/agent-builder-discover-tables.md).

## Related pages

- [AI assistance in the {{esql}} editor](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-ai-assistance)
- [How Discover works](discover-get-started.md)
