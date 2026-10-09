---
navigation_title: Errors UI
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-errors.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-errors.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Errors UI in Elastic APM [apm-errors]

Use the **Errors** page to investigate exceptions and logged errors from your services. Errors captured by APM agents, or reported manually with APM agent APIs, are grouped by similar exception or log messages.

Returning an HTTP 5xx status code alone doesn't create an exception or an error event. An exception or logged error must also be captured to appear on this page.

For OpenTelemetry exception logs that aren't grouped as APM errors, refer to [Errors from logs](#apm-errors-from-logs).

## APM errors [apm-error-groups]

Selecting an error group ID or error message brings you to the **Error group**.

:::{image} /solutions/images/observability-apm-error-group.png
:alt: APM Error group
:screenshot:
:::

The error group details page visualizes the number of error occurrences over time and compared to a recent time range. This allows you to quickly determine if the error rate is changing or remaining constant. You’ll also see the top 5 affected transactions—enabling you to quickly narrow down which transactions are most impacted by the selected error.

Further down, you’ll see an Error sample. The error shown is always the most recent to occur. The sample includes the exception message, culprit, stack trace where the error occurred, and additional contextual information to help debug the issue—all of which can be copied with the click of a button.

In some cases, you might also see a Transaction sample ID. This feature allows you to make a connection between the errors and transactions, by linking you to the specific transaction where the error occurred. This allows you to see the whole trace, including which services the request went through.

## Errors from logs [apm-errors-from-logs]
```{applies_to}
stack: ga 9.5+
serverless: ga
```

The **APM errors** section contains error groups and charts. The **Errors from logs** section lists OpenTelemetry exception logs that haven't been processed into APM error documents. Each row is an individual log with its exception message, type, and occurrence time. These logs have no error group and don't contribute to the APM error counts or charts.

Use the page's Kibana Query Language (KQL) search bar and time range to filter both **APM errors** and **Errors from logs**. The **APM errors** section is hidden when it has no errors to display and matching exception logs are available.

The logs table displays up to 500 of the most recent matching logs. Its search field filters those rows by message or type. To find logs outside that list, refine the page's KQL query or narrow the time range.

Click an exception message to inspect that log in **Discover**, or click **Open in Discover** to explore the matching exception logs.

## Investigate errors from a trace [apm-errors-from-trace]
```{applies_to}
stack: ga 9.5+
serverless: ga
```

In the [trace waterfall](/solutions/observability/apm/trace-sample-timeline.md) on an APM transaction details page, click **View error** or **View *x* errors** (if there is more than one). This opens the service's **Errors** page. The page's KQL query filters by the trace ID and the selected span or transaction ID, whether the errors are APM errors, OpenTelemetry exception logs, or both.

Clear the KQL query to explore errors across the service within the selected time range.
