---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
description: A quick tour of the Streams UI and its main capabilities.
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Quick tour

This is a quick visual overview of the main steps to get started with Streams in {{kib}}. It covers how to get data in, organize it into streams, parse and enrich your logs, set retention policies, and monitor data quality.

This tour is an ideal way to familiarize yourself with the Streams UI and its core workflows. You can follow along directly in your {{ecloud}} or self-managed {{es}} environment.


:::::{stepper}

::::{step} Get data in
Send logs via OpenTelemetry, Fluentd, Fluentbit, or an Elastic integration. For agentless ingest, send directly to the `/logs` endpoint.
::::

::::{step} Organize your data

:::{dropdown} From {{kib}}
- Select **Streams** from the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).
- Open the data stream for a specific document from **Discover**. To do this, expand the details flyout for a document that's stored in a data stream, and select **Stream** or an action associated with the document's data stream. Streams then opens filtered to the selected data stream.
:::

:::{dropdown} Using the API
{applies_to}`stack: preview 9.1` {applies_to}`serverless: preview` You can also access Streams features using the Streams API. Refer to the [Streams API documentation]({{kib-apis}}group/endpoint-streams) for more information.
:::
::::

::::{step} Parse and process
Streams automatically organizes your logs by source and component. Accept, adjust, or add [**partitions**](./organize-your-data.md) manually. Use the [**Processing** tab](./parse-and-process.md) to parse and extract fields from log messages. Accept AI-generated GROK rules or write your own.
::::

::::{step} Configure retention
Use the [**Retention** tab](./configure-retention.md) to define how long each stream stores data and to review ingestion volume.
::::

::::{step} Manage data quality
Use the [**Data quality** column](./monitor-and-fix-data-quality.md) to filter your streams by data quality status.
::::

:::::

::::::

## Alternatives paths to manage log data in Elastic

Streams is not the only way, consider these alternatives depending on your needs:

- **Elastic Agent integrations**: Pre-built integrations with automatic parsing and dashboards for
  common data sources. Best when your sources are covered by the
  [Elastic integration catalog](https://www.elastic.co/integrations).
- **Logstash pipelines**: Highly customizable, code-first pipeline configuration. Best for complex
  transformations or when you need to fan out to multiple destinations.
- **{{es}} ingest pipelines**: Low-level pipeline configuration via the ES API. Best for teams who
  already manage {{es}} directly and want fine-grained control without a UI.
