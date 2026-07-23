---
navigation_title: Get data in
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
description: Learn how to get data into Streams.
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

# Get data into Streams

This page covers the different ways to send data to Streams:

- **[Ingest new data](#get-data-in-wired)**: Use wired streams to send logs to a managed endpoint for new ingestion. Data lands in a managed hierarchy with inheritance, partitioning, and cascading configuration.
Best for new deployments, custom logs, and mixed-format sources.
- **[Work with existing data](#get-data-in-classic)**: Use classic streams to work with data already flowing into {{es}}. No migration or configuration changes required.

## Before you get started [get-data-in-prerequisites]

Streams requires the following permissions:

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

## Ingest new data with wired streams [get-data-in-wired]

```{applies_to}
stack: preview 9.2+
serverless: preview
```

Wired streams send your documents to a managed endpoint, from which you can route data into child streams based on [partitioning](./organize-your-data.md) rules. Child streams automatically inherit mappings, lifecycle settings, and processors from the parent, and configuration changes propagate through the hierarchy.

{applies_to}`{serverless: preview, stack: preview 9.4+}` Two endpoints are available. Use **`logs.otel`** (recommended) when sending OTel-native data or when you want a consistent, normalized format. Streams translates ECS field names to OTel equivalents automatically. Use **`logs.ecs`** when your data already uses ECS field names and you want to preserve them without transformation.

To send data to a wired stream, configure your shipper to point to the appropriate endpoint:

:::::{tab-set}

::::{tab-item} OpenTelemetry
:::{note}
Set the index based on your {{stack}} version:

- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.4+` Set the index to `logs.otel` or `logs.ecs`, depending on the endpoint you want to use.
- {applies_to}`stack: preview 9.2-9.3` Set the index to `logs`. Only the `logs` endpoint is available in these versions.
:::

```yaml
processors:
  transform/logs-streams:
    log_statements:
      - context: resource
        statements:
          - set(attributes["elasticsearch.index"], "logs.otel") # Set to `logs.otel` or `logs.ecs` (Serverless and Stack 9.4+), or `logs` (Stack 9.2–9.3)
service:
  pipelines:
    logs:
      receivers: [myreceiver] # Works with any logs receiver
      processors: [transform/logs-streams]
      exporters: [elasticsearch, otlp] # Works with either
```
::::

::::{tab-item} Filebeat
:::{note}
Set the index based on your {{stack}} version:

- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.4+` Set the index to `logs.otel` or `logs.ecs`, depending on the endpoint you want to use.
- {applies_to}`stack: preview 9.2-9.3` Set the index to `logs`. Only the `logs` endpoint is available in these versions.
:::

```yaml
filebeat.inputs:
  - type: filestream
    id: my-filestream-id
    index: logs.otel # Set to `logs.otel` or `logs.ecs` (Serverless and Stack 9.4+), or logs (Stack 9.2–9.3)
    enabled: true
    paths:
      - /var/log/*.log

# No need to install templates for wired streams
setup:
  template:
    enabled: false

output.elasticsearch:
  hosts: ["<elasticsearch-host>"]
  api_key: "<your-api-key>"
```
::::

::::{tab-item} Logstash
:::{note}
Set the index based on your {{stack}} version:

- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.4+` Set the index to `logs.otel` or `logs.ecs`, depending on the endpoint you want to use.
- {applies_to}`stack: preview 9.2-9.3` Set the index to `logs`. Only the `logs` endpoint is available in these versions.
:::

```json
output {
  elasticsearch {
    hosts => ["<elasticsearch-host>"]
    api_key => "<your-api-key>"
    index => "logs.otel" # Set to `logs.otel` or `logs.ecs` (Serverless and Stack 9.4+), or `logs` (Stack 9.2–9.3)
    action => "create"
  }
}
```
::::

::::{tab-item} Fleet
Use the **Custom Logs (Filestream)** integration to send data to wired streams:

1. Find **{{fleet}}** in the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select the **Settings** tab.
1. Under **Outputs**, find the output you want to use and select the {icon}`pencil` icon.
1. Turn on **Write to logs streams**.
1. Add the **Custom Logs (Filestream)** integration to an agent policy.
1. Enable the **Use the "logs" data stream** setting under **Change defaults**.
1. Under **Where to add this integration**, select an agent policy that uses the output configured in step 4.
::::

::::{tab-item} API
:::{note}
Set the endpoint based on your {{stack}} version:

- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.4+` Set the endpoint to `logs.otel` or `logs.ecs`, depending on the endpoint you want to use.
- {applies_to}`stack: preview 9.2-9.3` Set the endpoint to `logs`. Only the `logs` endpoint is available in these versions.
:::

Send data to the endpoint using the [Bulk API]({{es-apis}}operation/operation-bulk):

```json
POST /logs.otel/_bulk # Set to `logs.otel` or `logs.ecs` (Serverless or Stack 9.4+), or `logs` (Stack 9.2–9.3)
{ "create": {} }
{ "@timestamp": "2025-05-05T12:12:12", "body": { "text": "Hello world!" }, "resource": { "attributes": { "host.name": "my-host-name" } } }
{ "create": {} }
{ "@timestamp": "2025-05-05T12:12:12", "message": "Hello world!", "host.name": "my-host-name" }
```
::::

:::::

### Verify data is flowing

After configuring your data source, confirm data is appearing in Discover.

For wired streams, you first need to make the index pattern available:

1. Manually [create a {{data-source}}](../../../explore-analyze/find-and-organize/data-views.md#settings-create-pattern) for the wired streams index pattern (`logs,logs.*`).
1. Add the wired streams index pattern (`logs,logs.*`) to the `observability:logSources` {{kib}} advanced setting, which you can open from the navigation menu or by using the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).

Once data appears in Discover, you're ready to start organizing, parsing, and configuring retention for your streams.

#### Query unmapped fields [streams-wired-streams-discover-unmapped]
```{applies_to}
stack: preview 9.4
serverless: preview
```

Wired streams can contain fields stored in `_source` that are not explicitly mapped. By default, ES|QL returns an error when a query references an unmapped field. To make unmapped fields queryable, add `SET unmapped_fields = "LOAD";` at the start of your ES|QL query:

```esql
SET unmapped_fields = "LOAD";
FROM logs.otel
| WHERE my_custom_field == "value"
```

When `LOAD` is set, unmapped fields are loaded from `_source` as `keyword` fields, or treated as null if absent from `_source`.

{applies_to}`stack: preview 9.5` When you query a wired stream and the ES|QL editor detects an unknown column error, a **Load unmapped fields** quick fix action is available. Select it to apply this setting automatically.

For a conceptual overview and use cases, refer to [Unmapped fields](elasticsearch://reference/query-languages/esql/esql-unmapped-fields.md). For {{kib}} editor behavior, refer to [Handle unmapped fields with `SET unmapped_fields`](/explore-analyze/query-filter/languages/esql-kibana.md#esql-kibana-unmapped-fields).

## Work with existing data with classic streams [get-data-in-classic]

Classic streams let you use the Streams UI to extract fields and configure data retention for data that's already being ingested into {{es}} without additional configuration.

:::{warning}
Do not reroute or migrate existing data streams to the `logs`, `logs.otel`, or `logs.ecs` endpoints. Classic streams work with your existing data streams in place. No migration is required.
:::

Classic streams:

- Are based on existing data streams, index templates, and component templates.
- Can follow the data retention policy set in the existing index template.
- Do not support hierarchical inheritance or cascading configuration updates.

Open classic streams from the following places in {{kib}}:

- Select **Streams** from the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md), and find the data stream in the Streams table.

- Open the data stream for a specific document from **Discover**. To do this:
    1. From the **Documents** table, select the {icon}`expand` icon for a document to expand the details flyout.
    1. Under **Stream**, select the link to the stream (for example, `logs-generic.default`). The Streams UI opens filtered to the stream that contains the document.

{applies_to}`serverless: preview` {applies_to}`stack: preview 9.1+` You can also access Streams features using the Streams API. Refer to the [Streams API documentation]({{kib-apis}}group/endpoint-streams) for more information.

## Next steps [get-data-in-next-steps]

Once your data is flowing into Streams, you can start organizing and enriching it:

- **[Organize your data](./organize-your-data.md)**: Use partitioning to route data subsets into dedicated child streams with independent retention and processing rules. Partitioning is only available for wired streams.
- **[Parse and process](./parse-and-process.md)**: Build a processing pipeline to extract structured fields from raw log messages using AI-generated or manually configured processors.

