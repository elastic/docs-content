---
navigation_title: Get started
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
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

# Get started with Streams

This hands-on guide will take you through to the core features and common use cases of Streams. Before using Streams, make sure you have the following in place:

- **{{es}} and {{kib}}**: Streams is available from {{es}} 9.1 (API, preview), 9.2 (Wired streams,
  preview), and 9.2+ (GA for classic streams). For {{serverless-full}}, Streams is generally
  available.
- **Log data ingestion**: Logs can be sent to Streams via OpenTelemetry Collector, Fluentd,
  Fluentbit, or through Elastic one-click integrations. No agent deployment is required for
  agentless ingest via the `/logs` endpoint (Logs Streams, tech preview).
- **Required permissions**:
::::{applies-switch}

:::{applies-item} serverless:
Streams requires these {{serverless-full}} roles:
- Admin: Ability to manage all Streams
- Editor/Viewer: Limited access, cannot perform all actions
:::

:::{applies-item} stack:
To manage all streams, you need the following permissions:

- **Cluster permissions**: `manage_index_templates`, `manage_ingest_pipelines`, `manage_pipeline`, `read_pipeline`
- **Data stream level permissions**: `read`, `write`, `create`, `manage`, `monitor`, `manage_data_stream_lifecycle`, `read_failure_store`, `manage_failure_store`, `manage_ilm`.

To view streams, you need the following permissions:
- **Data stream level**: `read`, `view_index_metadata`, `monitor`

For more information, refer to [Cluster privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) and [Granting privileges for data streams and aliases](../../../deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md)

:::

To start using Streams:

::::

:::::{stepper}

::::{step} Ingest log data
Send logs via OpenTelemetry, Fluentd, Fluentbit, or an Elastic integration. For agentless ingest, send directly to the `/logs` endpoint.
::::

::::{step} Access Streams

:::{dropdown} From {{kib}}
- Select **Streams** from the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).
- Open the data stream for a specific document from **Discover**. To do this, expand the details flyout for a document that's stored in a data stream, and select **Stream** or an action associated with the document's data stream. Streams then opens filtered to the selected data stream.
:::

:::{dropdown} Using the API
{applies_to}`stack: preview 9.1` {applies_to}`serverless: preview` You can also access Streams features using the Streams API. Refer to the [Streams API documentation]({{kib-apis}}group/endpoint-streams) for more information.
:::
::::

::::{step} Review AI-suggested partitions
Streams automatically organizes your logs by source and component. Accept, adjust, or add [**partitions**](./management/partitioning.md) manually.
::::

::::{step} Set retention policies
Use the [**Retention** tab](./management/retention.md) to define how long each stream stores data and to review ingestion volume.
::::

::::{step} Configure processing
Use the [**Processing** tab](./management/extract.md) to parse and extract fields from log messages. Accept AI-generated GROK rules or write your own.
::::

::::{step} Manage data quality
Use the [**Data quality** column](./management/data-quality.md) to filter your streams by data quality status.
::::

::::{step} Configure advanced settings
Use the [**Advanced** tab](./management/advanced.md) to view the underlying {{es}} configuration and advanced settings for this stream.
::::

::::{step} Investigate with Significant Events
Review the [**Significant Events** view](./management/significant-events.md) to triage critical signals across your streams.
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

