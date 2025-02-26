---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-logs.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-logs.html
---

# Logs [apm-logs]

The **Logs** tab shows contextual logs for the selected service.

Logs provide detailed information about specific events, and are crucial to successfully debugging slow or erroneous transactions.

If you’ve correlated your application’s logs and traces, you never have to search for relevant data; it’s already available to you. Viewing log and trace data together allows you to quickly diagnose and solve problems.

To learn how to correlate your logs with your instrumented services, refer to [Stream application logs](../../../solutions/observability/logs/stream-application-logs.md).

:::{image} ../../../images/observability-logs.png
:alt: Example view of the Logs tab in Applications UI
:class: screenshot
:::

::::{tip}
Logs displayed on this page are filtered on `service.name`
::::

## Integrate with logging frameworks [apm-logs-correlation]
```{applies_to}
stack: all
```

Elastic APM integrates with popular logging frameworks, making it easy to correlate your logs and traces. This enables you to:

* View the context of a log and the parameters provided by a user
* View all logs belonging to a particular trace
* Easily move between logs and traces when debugging application issues

See the [Stream application logs](../../../solutions/observability/logs/stream-application-logs.md) guide to get started.