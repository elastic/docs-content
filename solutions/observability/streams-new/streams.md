---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
description: Streams provides a centralized UI for extracting fields, setting retention, routing data, and managing Elasticsearch data streams.
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

# Streams-new

Streams allows you to automatically parse, structure, and organize your log data so you can query it immediately, without writing Grok expressions or maintaining custom pipelines.

When an incident hits, Streams gets you to answers faster. AI-powered detection continuously scans your logs for critical signals and surfaces what matters. Instead of manually scanning thousands of log lines, you get a prioritized list of what matters.

## Use Streams to...

**Organize logs automatically**
:   Streams uses AI to partition your log data by source and component, without manual regex rules or pipeline configuration. As new log formats arrive, Streams continues to learn and extend its partitioning automatically.

**Get meaning from logs**
:   The AI-powered processing pipeline detects log formats and generates parsing rules that extract structured fields from unstructured text. You get clean, queryable data without writing a single GROK expression.

**Solve incidents in minutes, not hours**
:   Significant Events detection continuously scans your streams for critical signals: out-of-memory errors, crash loops, certificate expirations, and anomalies. 

**Reduce time spent on managing pipelines**
:   Streams uses AI to simplify parsing, enrichment, partitioning, and schema updates. You can start investigating issues within minutes, rather than spending weeks on pipeline setup and data engineering.

**Control storage costs**
:   By surfacing the most critical logs and automatically structuring data for efficient storage, Streams allows you to retain high-value data without discarding important information, reducing overall storage costs.


## Quick tour

This is a quick overview of the main steps to get started with Streams in {{kib}}. It covers how to get data in, organize it into streams, parse and enrich your logs, set retention policies, and monitor data quality.

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
Use the [**Data quality** column](./manage-data-quality.md) to filter your streams by data quality status.
::::

:::::

::::::

