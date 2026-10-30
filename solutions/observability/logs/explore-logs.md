---
navigation_title: Explore logs
description: Search, filter, and tail logs in Discover, aggregate them with ES|QL, find patterns and anomalies with machine learning, and alert on log conditions.
applies_to:
  stack: ga
  serverless:
    observability: ga
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-logs.html
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Explore logs [monitor-logs]

**Discover** is where you work with logs in Elastic. Instead of logging in to servers and tailing files, you search, filter, and tail every log you've ingested in one place, then aggregate with {{esql}}, hand unusual patterns to {{ml}}, and turn what you find into rules. When you're investigating an incident, that means narrowing to the relevant events, inspecting their fields and context, and pivoting to the affected service, host, or trace. This page maps those tasks to the pages that teach them.

## Search and tail logs in Discover [logs-explore-discover]

From the navigation menu, go to **Discover** and select the **All logs** {{data-source}}. It shows every data stream matched by the `observability:logSources` advanced setting, so logs from all your sources appear together. To focus on one source, create a {{data-source}} for its index pattern. In **{{esql}}** mode, query the same data with `FROM logs-*`.

Expand a document to open the log details: the message broken into fields, similar errors, the stream it belongs to, and for application logs the stack trace and trace summary. If the message hasn't been parsed into fields, **Parse content in Streams** takes you to the stream to fix that.

Refer to [Explore logs in Discover](/solutions/observability/logs/discover-logs.md). To change which index patterns count as logs, refer to [Configure log data sources](/solutions/observability/logs/log-data-sources.md).

## Filter and aggregate [logs-explore-aggregate]

Filter with {{kib}} Query Language (KQL) in the **Discover** query bar to narrow to a host, a level, or a time range. Aggregate to answer questions the documents table can't: how many errors per service in the last hour, which hosts log the most warnings. Use {{esql}} `STATS` in **Discover** for interactive work and Query DSL aggregations from the API when you script it.

Refer to [Filter and aggregate logs](/solutions/observability/logs/filter-aggregate-logs.md). Both depend on parsed fields. If yours are missing, start with [Process logs](/solutions/observability/logs/process.md).

## Find patterns and anomalies [logs-explore-patterns]

When you have more log lines than you can read, let Elastic group them:

[Run a pattern analysis on log data](/solutions/observability/logs/run-pattern-analysis-on-log-data.md)
:   From a text field in **Discover**, select **Run pattern analysis** to group messages by pattern and see how often each occurs. Use it first: it needs no setup and works on any text field.

[Categorize log entries](/solutions/observability/logs/categorize-log-entries.md)
:   Create an {{anomaly-job}} that clusters messages into categories over time and flags categories whose count is unusual. Requires `all` privileges for {{ml-app}}.

[Inspect log anomalies](/solutions/observability/logs/inspect-log-anomalies.md)
:   Create an {{anomaly-job}} on the log rate to catch drops and spikes per partition, such as a service that stopped logging.

## Alert on logs [logs-explore-alert]

When a search is worth repeating, make it a rule. Pick the rule type by the condition you want to catch:

[Log threshold rule](/solutions/observability/incident-management/create-log-threshold-rule.md) {applies_to}`serverless: unavailable`
:   Alert when the number of log messages matching a query crosses a threshold in a time window, optionally grouped by a field or as a ratio of two queries. It queries the `observability:logSources` index patterns.

[Custom threshold rule](/solutions/observability/incident-management/create-custom-threshold-rule.md)
:   Alert on an aggregation over any {{data-source}}, including logs. Use this on {{serverless-full}}, and anywhere you want one rule type across logs and metrics.

[Degraded docs rule](/solutions/observability/incident-management/create-a-degraded-docs-rule.md) {applies_to}`stack: ga 9.1+` {applies_to}`serverless: ga`
:   Alert when the share of documents with ignored fields in a {{data-source}} rises above a threshold. Use it to catch parsing and mapping problems before they hide data.

For actions, snoozing, and the other rule types, refer to [Create and manage rules](/solutions/observability/incident-management/create-manage-rules.md).

## Check data quality [logs-explore-quality]

If a search returns less than you expect, the logs might be arriving with ignored or malformed fields. The **Data Set Quality** page shows the share of degraded documents per data set and lets you open the affected documents in **Discover**. Refer to [Data set quality](/solutions/observability/data-set-quality-monitoring.md).

## Related pages [logs-explore-related]

- [Process logs](/solutions/observability/logs/process.md)
- [Manage logs storage](/solutions/observability/logs/manage-storage.md)
- [Discover](/explore-analyze/discover.md): the general Discover documentation, for features that aren't log-specific.
