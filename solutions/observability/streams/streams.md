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

# Streams

Streams lets you parse, structure, and organize your log data so you can query it immediately, without writing Grok expressions or maintaining custom pipelines.

When an incident occurs, Streams gets you to answers faster. AI-powered detection continuously scans your logs for critical signals and surfaces what matters. Instead of manually scanning thousands of log lines, you get a prioritized list of what matters.

## What you can do with Streams

**Organize logs automatically**
:   Streams uses AI to partition your log data by source and component, without manual regex rules or pipeline configuration. As new log formats arrive, Streams continues to learn and extend its partitioning automatically.

**Get meaning from logs**
:   The AI-powered processing pipeline detects log formats and generates parsing rules that extract structured fields from unstructured text. You get clean, queryable data without writing a single Grok expression.

**Reduce time spent on managing pipelines**
:   Streams uses AI to simplify parsing, enrichment, partitioning, and schema updates. You can start investigating issues within minutes, rather than spending weeks on pipeline setup and data engineering.

**Control storage costs**
:   By surfacing the most critical logs and automatically structuring data for efficient storage, Streams lets you retain high-value data without discarding important information, reducing overall storage costs.

## Before you get started

To use Streams, you need the following prerequisites:

- {{ech}} ({{stack}} 9.2+) or {{serverless-short}}
- A [generative AI connector](kibana://reference/connectors-kibana/gen-ai-connectors.md) to use AI features like pipeline suggestion, partition suggestions, and significant events. Any generative AI connector works, including [Elastic Managed LLMs](kibana://reference/connectors-kibana/elastic-managed-llm.md), which requires no external account or API key.

    :::{note}
    A {{ml}} node is not required. Streams' AI features use the generative AI connector and do not depend on {{ml}} infrastructure.
    :::

You also need {{kib}} access with the following permissions:

::::{applies-switch}

:::{applies-item} serverless:
Streams requires one of the following {{serverless-full}} roles:

- Admin: Able to manage all Streams
- Editor/Viewer: Has limited access to Streams, cannot perform all actions

:::

:::{applies-item} stack:
To manage all streams, you need the following permissions:

- **Cluster permissions**: `manage_index_templates`, `manage_ingest_pipelines`, `manage_pipeline`, `read_pipeline`
- **Data stream level permissions**: `read`, `write`, `create`, `manage`, `monitor`, `manage_data_stream_lifecycle`, `read_failure_store`, `manage_failure_store`, `manage_ilm`.

To view streams, you need the following permissions:
- **Data stream level**: `read`, `view_index_metadata`, `monitor`

For more information, refer to [Cluster privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) and [Granting privileges for data streams and aliases](../../../deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md).

:::

::::


## Get started with Streams

Follow these main steps to get started with Streams in {{kib}}. You can find links to send data to Streams, organize your data, parse and enrich your logs, set retention policies, and monitor data quality.

This overview helps you familiarize yourself with the Streams UI and its core workflows. You can follow along directly in your {{ech}} or {{serverless-short}} environment.

Open **Streams** from the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).

:::::{stepper}

::::{step} Get data in
Streams supports two ingestion paths:

- **[Ingest new data](./get-data-in.md#get-data-in-wired)**: Send logs to a managed endpoint for new ingestion. Data lands in a managed hierarchy with inheritance, partitioning, and cascading configuration. Best for new deployments, custom logs, and mixed-format sources.
- **[Work with existing data](./get-data-in.md#get-data-in-classic)**: Work with data already flowing into {{es}}. No migration or configuration changes required.
::::

::::{step} Organize your data

:::{note}
Organizing your data using partitions is only available when sending data to the `logs.otel` or `logs.ecs` managed endpoints. If you're using data that is already flowing to {{es}}, skip this step.
:::

Use the [**Partitioning**](./organize-your-data.md) tab to route subsets of your stream data into dedicated child streams. Each child stream inherits the parent's configuration but can be managed independently with its own retention policy, processing rules, and field mappings.

Create partitions manually using field-based conditions, or let AI analyze your data and suggest groupings.

::::

::::{step} Parse and process
Use the [**Processing**](./parse-and-process.md) tab to build a document processing pipeline that extracts structured fields from raw log messages:

- **Suggest a pipeline**: Let AI analyze sample documents and generate a complete processor pipeline.
- **Manually add processors**: Select and configure individual processors when you know which transformations you need.
- **Add conditions**: Attach Boolean expressions to run processors only when certain criteria are met.

After adding processors, the **Data preview** simulates results, so you can verify field extraction before saving.
::::

::::{step} Configure retention
Use the [**Retention**](./configure-retention.md) tab to control how long each stream stores data and manage storage costs. Review storage size, ingestion averages, and tier distribution before choosing a retention method:

- **[Inherit retention](./configure-retention.md#streams-configure-retention-steps)**: Use settings from the stream's index template or parent stream.
- **[Set a retention period](./configure-retention.md#streams-configure-retention-steps)**: Define a minimum number of days before data is deleted.
- **[Follow an {{ilm}} ({{ilm-init}}) policy](./configure-retention.md#streams-configure-retention-steps)**: Apply an existing {{ilm-init}} policy to automate data movement through lifecycle phases.
::::

::::{step} Manage data quality
The **Data quality** column on the **Streams** main page shows each stream's health (**Good**, **Degraded**, or **Poor**) at a glance, and lets you filter by health status. Select a stream or open the [**Data quality**](./manage-data-quality.md) tab to examine more closely and resolve issues.

When documents fail during ingestion, Streams preserves them in a [failure store](./manage-data-quality.md#streams-data-quality-failure) rather than dropping them, so you can inspect what went wrong and fix the processor using the actual failing documents.
::::

:::::

