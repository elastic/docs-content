---
applies_to:
  stack: preview 9.2
  serverless: preview
description: Explore trace data in Discover using the traces profile.
products:
  - id: observability
---

# Explore traces in Discover [explore-traces-discover]

:::{important}
This functionality is experimental and not supported. It may change or be removed at anytime.
:::

**Discover** offers a dedicated experience for exploring trace data. When **Discover** detects data in `traces-*` indices, it automatically selects relevant fields and enables features that help you investigate distributed traces more effectively. The traces experience includes a pre-selected set of trace fields in the data grid, a structured overview of each document's key attributes, latency comparisons for similar spans, and a waterfall visualization of the full trace timeline.

If you're just getting started with **Discover** and want to learn its main principles, you should get familiar with the [default experience](/explore-analyze/discover.md).

:::{image} /solutions/images/discover-traces-main.png
:alt: Discover showing trace data with the traces profile active, including pre-selected columns for service name, transaction name, span name, and duration.
:screenshot:
:::

## Requirements [traces-discover-requirements]

### Data recognition [traces-data-recognition]

By default, data stored in `traces-*` indices is recognized as trace data and triggers the **Discover** experience described on this page.

### Required {{kib}} privileges [traces-kibana-privileges]

Viewing trace data in **Discover** requires at least `read` privileges for **Discover**.

For more information, refer to [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

## Load trace data [load-trace-data]

The traces experience is available in:

* **{{data-source-cap}} mode**: Select a {{data-source}} that matches a `traces-*` index pattern from the **Discover** main page.

* **{{esql}} mode**: Select **Try {{esql}}** and use the `FROM` command to query your trace data:

    ```esql
    FROM traces-*
    ```

    You can also query a specific index:

    ```esql
    FROM traces-apm-default
    ```

## Traces-specific features [traces-specific-features]

When **Discover** recognizes trace data, it pre-selects a set of relevant fields as columns in the data grid: `service.name`, `transaction.name`, `span.name`, `transaction.duration.us`, `span.duration.us`, and `event.outcome`.

### Overview charts ({{esql}}) [traces-overview-charts]

In {{esql}} mode, **Discover** displays three summary charts above the results:

- **Latency**: Average response time over the selected time range.
- **Error Rate**: Percentage of failed trace events over time.
- **Throughput**: Number of trace events per unit of time.

:::{image} /solutions/images/discover-traces-esql-charts.png
:alt: {{esql}} mode showing Latency, Error Rate, and Throughput summary charts above the trace results.
:screenshot:
:::

### Trace document overview [trace-document-overview]

Select any row to open the document detail panel. The **Overview** tab shows the key attributes of the selected trace document:

- **Span ID** and **Span name**: Identify the specific operation.
- **Trace ID**: Links all documents that belong to the same trace.
- **Service name**: The service that generated this span.
- **Duration**: How long the operation took, and what percentage of the total trace duration it represents.
- **Start time**: When the operation started.
- **Type** and **Subtype**: The category of the operation, for example `db` / `postgresql` or `external` / `http`.

:::{image} /solutions/images/discover-traces-document-overview.png
:alt: The Overview tab in the document detail panel showing span attributes including Trace ID, Service name, Duration as a percentage of trace, and a latency chart in the Similar spans section.
:screenshot:
:::

### Similar spans [similar-spans]

The **Similar spans** section shows a latency chart for spans with the same type and name across your data. Use this view to compare the selected span's performance against historical samples and identify outliers.

:::{image} /solutions/images/discover-traces-document-similar-spans.png
:alt: The Similar spans section in the document detail panel showing a latency chart for spans with the same type and name, with an Open in Discover link.
:screenshot:
:::

Select **Open in Discover** to open a filtered view of all similar spans.

### Trace waterfall [trace-waterfall]

The **Trace** section shows a condensed waterfall of the trace the selected document belongs to. Each row represents a span or transaction, positioned on a timeline to show when it started and how long it took.

:::{image} /solutions/images/discover-traces-document-trace.png
:alt: The Trace section in the document detail panel showing a mini waterfall with spans and a link to expand the full trace timeline.
:screenshot:
:::

Select **Expand trace timeline** to open the full-screen waterfall view.

### Expanded trace timeline [expanded-trace-timeline]

The expanded trace timeline shows all spans and transactions in a trace in a full-screen waterfall view. A color-coded legend identifies which service each span belongs to. Failed spans are highlighted to help you quickly locate errors.

:::{image} /solutions/images/discover-traces-timeline.png
:alt: The expanded trace timeline showing a waterfall visualization with spans from multiple services, including duration labels and failure badges.
:screenshot:
:::

### Logs [traces-logs]

The **Logs** section shows log entries correlated with the selected trace. Select **Open in Discover** to explore those logs in context.