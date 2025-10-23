---
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

The **Logs** tab shows contextual logs for the selected service.

Logs provide detailed information about specific events, and are crucial to successfully debugging slow or erroneous transactions.

If you’ve correlated your application’s logs and traces, you never have to search for relevant data; it’s already available to you. Viewing log and trace data together allows you to quickly diagnose and solve problems.

To learn how to correlate your logs with your instrumented services, refer to [Stream application logs](/solutions/observability/logs/stream-application-logs.md).

:::{image} /solutions/images/observability-logs.png
:alt: Example view of the Logs tab in Applications UI
:screenshot:
:::

::::{tip}
Logs displayed on this page are filtered on `service.name`
::::

### View enhanced logs [apm-enhanced-logs]
```{applies_to}
stack: preview 9.0
```

For an enhanced logs view with additional information including the log pattern, the number of events for each log, change type, and the time the change occurred, turn on the `observability:newLogsOverview` [advanced setting](kibana://reference/advanced-settings.md#kibana-search-settings).

## Integrate with logging frameworks [apm-logs-correlation]
```{applies_to}
stack: all
```

Elastic APM integrates with popular logging frameworks, making it easy to correlate your logs and traces. This enables you to:

* View the context of a log and the parameters provided by a user
* View all logs belonging to a particular trace
* Easily move between logs and traces when debugging application issues

See the [Stream application logs](/solutions/observability/logs/stream-application-logs.md) guide to get started.