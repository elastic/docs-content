---
description: Use Elastic Application Performance Monitoring (APM) logs to investigate services, group similar events into patterns, and search custom indices.
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-logs.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-logs.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Logs [apm-logs]

To troubleshoot a slow or failed transaction, select a service, then select **Logs**. The tab shows that service's application and container log events, while maintaining any environment, query, and time range filters already set.

From here you can inspect a specific failure, group similar messages to see what's changed, or jump from a correlated log to its trace.

:::{image} /solutions/images/observability-logs.png
:alt: Logs tab grouping service logs into patterns with event counts and timelines
:screenshot:
:::

## View log events

The tab opens with **Log Events** selected, with the table showing each individual event. Use this view when you already have a specific event in mind: an error message, a timestamp, or a `trace.id` from a failed transaction. Select a row to inspect the message and fields, or select **Open logs in Discover** to search the same documents with a wider query.

## Group logs by pattern [apm-enhanced-logs]
```{applies_to}
stack: preview 9.0+
serverless: preview
```

Select **Log Events**, then select **Log Patterns** to group similar messages. Each pattern shows its event count, change type, and change time.

The [`observability:newLogsOverview`](kibana://reference/advanced-settings.md#observability-new-logs-overview) advanced setting controls log pattern grouping:

* {applies_to}`serverless: preview` {applies_to}`stack: preview 9.2+` The setting is on by default. Turn it off to hide **Log Patterns**.
* {applies_to}`stack: preview 9.0-9.1` The setting is off by default. Turn it on to use **Log Patterns**.

The **Logs** tab searches indices that match the patterns configured in `observability:logSources`. To include custom log indices, see [](/solutions/observability/logs/log-data-sources.md).

## Correlate logs and traces [apm-logs-correlation]

To send application logs and correlate them with traces, refer to [](/solutions/observability/logs/stream-application-logs.md).
