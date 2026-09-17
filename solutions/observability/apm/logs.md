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

The **Logs** tab in Elastic Application Performance Monitoring (APM) shows application and container log events for a service so you can troubleshoot slow or failed transactions. Select a service, then select **Logs**. The tab applies the selected environment, query, and time range.

:::{image} /solutions/images/observability-logs.png
:alt: Logs tab showing log events for a service
:screenshot:
:::

## View log events

The tab opens with **Log Events**, which lists individual events.

## Group logs by pattern [apm-enhanced-logs]
```{applies_to}
stack: preview 9.0+
serverless: preview
```

Select **Log Events**, then select **Log Patterns** to group similar messages. Each pattern shows its event count, change type, and change time.

The [`observability:newLogsOverview`](kibana://reference/advanced-settings.md#observability-new-logs-overview) advanced setting controls log pattern grouping:

* {applies_to}`stack: preview 9.0-9.1` The setting is off by default. Turn it on to use **Log Patterns**.
* {applies_to}`{"stack": "preview 9.2+", "serverless": "preview"}` The setting is on by default. Turn it off to hide **Log Patterns**.

The **Logs** tab searches indices that match the patterns configured in `observability:logSources`. To include custom log indices, see [](/solutions/observability/logs/log-data-sources.md).

## Correlate logs and traces [apm-logs-correlation]

To send application logs and correlate them with traces, refer to [](/solutions/observability/logs/stream-application-logs.md).