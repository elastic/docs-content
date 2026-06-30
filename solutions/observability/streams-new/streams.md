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

**Reduce time spent on managing pipelines**
:   Streams uses AI to simplify parsing, enrichment, partitioning, and schema updates. You can start investigating issues within minutes, rather than spending weeks on pipeline setup and data engineering.

**Control storage costs**
:   By surfacing the most critical logs and automatically structuring data for efficient storage, Streams allows you to retain high-value data without discarding important information, reducing overall storage costs.


## Get started with Streams

This is a quick overview of the main steps to get started with Streams in {{kib}}. You'll find links to send data to Streams, organize your data, parse and enrich your logs, set retention policies, and monitor data quality.

This tour is an ideal way to familiarize yourself with the Streams UI and its core workflows. You can follow along directly in your {{ecloud}} or self-managed {{es}} environment.


:::::{stepper}

::::{step} Get data in
Streams supports two ingestion paths:

- **[Ingest new data](./get-data-in.md#get-data-in-wired)**: Use wired streams to send logs to a managed endpoint for new ingestion. Data lands in a managed hierarchy with inheritance, partitioning, and cascading configuration. Best for new deployments, custom logs, and mixed-format sources.
- **[Work with existing data](./get-data-in.md#get-data-in-classic)**: Use classic streams to work with data already flowing into {{es}}. No migration or configuration changes required.
::::

::::{step} Organize your data

Use [**partitioning**](./organize-your-data.md) to route subsets of your wired stream data into dedicated child streams. Each child stream inherits the parent's configuration but can be managed independently with its own retention policy, processing rules, and field mappings.

Create partitions manually using field-based conditions, or let AI analyze your data and suggest groupings.

:::{note}
Partitioning is only available when sending data to the `logs.otel` or `logs.ecs` endpoints (wired streams). If you're using classic streams, skip this step.
:::
::::

::::{step} Parse and process
Use the [**Processing** tab](./parse-and-process.md) to build a document processing pipeline that extracts structured fields from raw log messages:

- **Suggest a pipeline**: Let AI analyze sample documents and generate a complete processor pipeline.
- **Manually add processors**: Select and configure individual processors when you know which transformations you need.
- **Add conditions**: Attach Boolean expressions to run processors only when certain criteria are met.

After adding processors, use the **Data preview** tab to simulate results and verify field extraction before saving.
::::

::::{step} Configure retention
Use the [**Retention** tab](./configure-retention.md) to control how long each stream stores data and manage storage costs. Review storage size, ingestion averages, and tier distribution before choosing a retention method:

- **[Inherit retention](./configure-retention.md#streams-configure-retention-steps)**: Use settings from the stream's index template or parent stream.
- **[Set a retention period](./configure-retention.md#streams-configure-retention-steps)**: Define a minimum number of days before data is deleted.
- **[Follow an {{ilm-init}} policy](./configure-retention.md#streams-configure-retention-steps)**: Apply an existing {{ilm-init}} policy to automate data movement through lifecycle phases.
::::

::::{step} Manage data quality
Use the [**Data quality** tab](./manage-data-quality.md) to monitor and resolve data quality issues. The **Data quality** column on the main Streams page shows each stream's health — **Good**, **Degraded**, or **Poor** — at a glance.

When documents fail during ingestion, Streams preserves them in a [failure store](./manage-data-quality.md#streams-data-quality-failure) rather than dropping them, so you can inspect what went wrong and fix the processor using the actual failing documents.
::::

:::::

::::::

