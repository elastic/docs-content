---
applies_to:
  stack: preview 9.1+
  serverless: preview
description: Explore trace data in Discover.
products:
  - id: observability
---

# Explore traces in Discover [explore-traces-discover]

:::{important}
This functionality is experimental. It might change or be removed at any time.
:::

**Discover** offers a dedicated experience for exploring trace data. When **Discover** detects data in `traces-*` indices, it automatically enables features that help you investigate distributed traces more effectively. The traces experience includes a preselected set of trace fields in the data grid, a structured overview of each document's key attributes, latency comparisons for similar spans, and a waterfall visualization of the full trace timeline.

If you're getting started with **Discover** and want to learn its main principles, get familiar with the [default experience](/explore-analyze/discover.md).

:::{image} /solutions/images/discover-traces-main.png
:alt: Discover showing trace data with the traces profile active, including preselected columns for service name, transaction name, span name, and duration.
:screenshot:
:::

## Requirements [traces-discover-requirements]

### Data recognition [traces-data-recognition]

Data stored in `traces-*` indices is automatically recognized as trace data and triggers the **Discover** experience described on this page.

### Required {{kib}} privileges [traces-kibana-privileges]

Viewing trace data in **Discover** requires at least `read` privileges for **Discover**.

For more information, refer to [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

## Load trace data [load-trace-data]

The traces experience is available in:

* **{{data-source-cap}} mode**: Select a {{data-source}} that matches a `traces-*` index pattern from the **Discover** main page.

* **{{esql}} mode**: Switch to **{{esql}}** mode and use the `FROM` command to query your trace data:

    ```esql
    FROM traces-*
    ```

    You can also query a specific index:

    ```esql
    FROM traces-apm-default
    ```

## Traces-specific features [traces-specific-features]

When **Discover** recognizes trace data, it preselects a set of relevant fields as columns in the data grid: `service.name`, `transaction.name`, `span.name`, `transaction.duration.us`, `span.duration.us`, and `event.outcome`. You can [reorder, resize, or add new columns](/explore-analyze/discover/document-explorer.md#document-explorer-columns) using the standard **Discover** column controls.

### Overview charts ({{esql}}) [traces-overview-charts]

In {{esql}} mode, **Discover** displays three summary charts above the results:

- **Latency**: Average response time over the selected time range
- **Error Rate**: Percentage of failed trace events over time
- **Throughput**: Number of trace events per unit of time

:::{image} /solutions/images/discover-traces-esql-charts.png
:alt: {{esql}} mode showing Latency, Error Rate, and Throughput summary charts above the trace results.
:screenshot:
:::

### Trace document overview [trace-document-overview]

Select {icon}`expand` in any row to open the document detail panel. The **Overview** tab shows the key attributes of the selected trace document:

- **Span ID** and **Span name**: Identifies the specific operation
- **Trace ID**: Links all documents that belong to the same trace
- **Service name**: The service that generated this span
- **Duration**: How long the operation took, and what percentage of the total trace duration it represents
- **Start time**: When the operation started
- **Type** and **Subtype**: The category of the operation, for example `db` / `postgresql` or `external` / `http`

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

### Trace summary [trace-waterfall]

The **Trace summary** section shows a condensed waterfall of the trace the selected document belongs to. Each row represents a span or transaction, positioned on a timeline to show when it started and how long it took.

:::::{applies-switch}

:::{applies-item} {"stack": "preview 9.4+", "serverless": "preview"}
:::{image} /solutions/images/discover-traces-document-trace-serverless.png
:alt: The Trace summary section in the document detail panel showing a condensed waterfall with spans and links to expand the trace timeline and open in Discover.
:screenshot:
:::
:::

:::{applies-item} {"stack": "preview 9.1-9.3"}
:::{image} /solutions/images/discover-traces-document-trace.png
:alt: The Trace section in the document detail panel showing a mini waterfall with spans and a link to expand the full trace timeline.
:screenshot:
:::
:::

:::::

Select **Expand trace timeline** to open the expanded waterfall view.

#### Expanded trace timeline [expanded-trace-timeline]

The expanded trace timeline shows all spans and transactions in a trace in a dedicated flyout waterfall view. A color-coded legend identifies which service each span belongs to. Failed spans are highlighted to help you quickly locate errors.

:::{tip}
```{applies_to}
stack: preview 9.4+
serverless: preview
```
Turn on **Show critical path** to highlight the sequence of spans that determined the trace's total duration.
:::

:::::{applies-switch}

:::{applies-item} {"stack": "preview 9.4+", "serverless": "preview"}
:::{image} /solutions/images/discover-traces-timeline-serverless.png
:alt: The expanded trace timeline showing a waterfall visualization with spans from multiple services, a Show critical path toggle, service legend, and failure badges.
:screenshot:
:::
:::

:::{applies-item} {"stack": "preview 9.1-9.3"}
:::{image} /solutions/images/discover-traces-timeline.png
:alt: The expanded trace timeline showing a waterfall visualization with spans from multiple services, including duration labels and failure badges.
:screenshot:
:::
:::

:::::

### Logs [traces-logs]

The **Logs** section shows log entries correlated with the selected trace. Select **Open in Discover** to explore those logs in context.

## Inspect GenAI spans [genai-span-details]
```{applies_to}
stack: preview 9.6+
serverless: preview
```

Use the **GenAI** tab to inspect model calls, token usage, and recorded prompts and responses. These views use the `gen_ai.*` attributes defined by the [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai). They work with {{edot}} and other OpenTelemetry instrumentations that record these attributes. For setup instructions, refer to [](/solutions/observability/get-started/opentelemetry/use-cases/llms/index.md).

To open the tab:

1. [Load trace data](#load-trace-data) in **Discover** and select a time range that includes your application's model calls.
2. In the results table, click **View details** {icon}`maximize` for a span or transaction that contains GenAI attributes.
3. Select **GenAI**, next to **Overview**, in the document detail panel. The tab appears only when the selected document contains GenAI attributes with values.

### Details [genai-span-details-fields]

The **Details** section shows the attributes recorded for the selected operation:

| Field | Description |
| --- | --- |
| **Operation** | The operation performed, such as `chat`, from `gen_ai.operation.name`. |
| **Request model** | The model requested by the application, from `gen_ai.request.model`. |
| **Provider** | The provider from `gen_ai.provider.name`, or `gen_ai.system` for instrumentation that uses the older attribute. |
| **Input tokens** | The input token count recorded in `gen_ai.usage.input_tokens`. |
| **Output tokens** | The output token count recorded in `gen_ai.usage.output_tokens`. |

Additional details, such as the response model and request parameters, appear when they are recorded on the span.

In **Discover**, hover over a field value to use **Filter for value** {icon}`plus_circle` or **Filter out value** {icon}`minus_circle`. Hover over a field name to use **Filter for field present** {icon}`filter` or **Toggle column in table**. These actions help you find related model calls or compare their attributes in the results table. Available actions depend on the field and query mode.

### Prompts and responses [genai-span-messages]

When the instrumentation records message content, the **Conversation** section shows prompts and responses with their roles, such as user or assistant. Click **Copy message** {icon}`copy` next to a message to copy its full contents.

The conversation is built from the [`gen_ai.input.messages`](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/registry/attributes/gen-ai.md#gen-ai-input-messages) and [`gen_ai.output.messages`](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/registry/attributes/gen-ai.md#gen-ai-output-messages) attributes, added in version 1.37.0 of the OpenTelemetry semantic conventions. For instrumentation that records `gen_ai.prompt` and `gen_ai.completion` instead, {{kib}} falls back to those attributes. Instrumentation that predates version 1.37.0 records messages as separate events, which the **GenAI** tab doesn't show.

Messages and token counts are recorded separately. A span can include token usage without message content. For message capture settings, refer to the documentation for your instrumentation.

Message values longer than 1,024 characters aren't indexed, so {{kib}} reads them from the document source, matching the span by `_id` or, when that isn't available, by `span.id`. A **Content may be incomplete** message appears only when a query returns neither field, such as an {{esql}} query that uses `KEEP` without `span.id`. To resolve it, add `span.id` to the query, or add `METADATA _id, _index` to the `FROM` command.

You can also [inspect GenAI spans in a trace waterfall](/solutions/observability/apm/trace-sample-timeline.md#genai-trace-waterfall) to see model calls alongside the other operations in a request.
