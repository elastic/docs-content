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

Streams supports the following ways to ingest data depending on where your data is today:

- **[Ingest new data](#get-data-in-wired)**: Use wired streams to send logs to a managed endpoint for new ingestion. Data lands in a managed hierarchy with inheritance, partitioning, and cascading configuration.
Best for new deployments, custom logs, and mixed-format sources.
- **[Work with existing data](#get-data-in-classic)**: Use classic streams to work with data already flowing into {{es}}. No migration or configuration changes required.

## Prerequisites [get-data-in-prerequisites]

Streams requires the following permissions:

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

::::

## Ingest new data [get-data-in-wired]

```{applies_to}
stack: preview 9.2+
serverless: preview
```

Wired streams send your documents to a managed endpoint, from which you can route data into child streams based on [partitioning](./organize-your-data.md) rules. Child streams automatically inherit mappings, lifecycle settings, and processors from the parent, and configuration changes propagate through the hierarchy.

To send data to a wired stream, configure your shipper to point to the appropriate endpoint:

:::::{tab-set}

::::{tab-item} OpenTelemetry
:::{note}
Set the index based on your {{stack}} version:

- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.4+` Set the index to `logs.otel` or `logs.ecs`, depending on which endpoint you want to use.
- {applies_to}`stack: preview 9.2-9.3` Set the index to `logs`. Only the `logs` endpoint is available in these versions.
:::

```yaml
processors:
  transform/logs-streams:
    log_statements:
      - context: resource
        statements:
          - set(attributes["elasticsearch.index"], "logs.otel") # Set to `logs.otel` or `logs.ecs` (serverless and stack 9.4+), or `logs` (stack 9.2–9.3)
service:
  pipelines:
    logs:
      receivers: [myreceiver] # works with any logs receiver
      processors: [transform/logs-streams]
      exporters: [elasticsearch, otlp] # works with either
```
::::

::::{tab-item} Filebeat
:::{note}
Set the index based on your {{stack}} version:

- {applies_to}`stack: preview 9.2-9.3` Set the index to `logs`. Only the `logs` endpoint is available in these versions.
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.4+` Set the index to `logs.otel` or `logs.ecs`, depending on which endpoint you want to use.
:::

```yaml
filebeat.inputs:
  - type: filestream
    id: my-filestream-id
    index: logs.otel # Set to `logs.otel` or `logs.ecs` (serverless and stack 9.4+), or logs (stack 9.2–9.3)
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

- {applies_to}`stack: preview 9.2-9.3` Set the index to `logs`. Only the `logs` endpoint is available in these versions.
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.4+` Set the index to `logs.otel` or `logs.ecs`, depending on which endpoint you want to use.
:::

```json
output {
  elasticsearch {
    hosts => ["<elasticsearch-host>"]
    api_key => "<your-api-key>"
    index => "logs.otel" # Set to `logs.otel` or `logs.ecs` (serverless and stack 9.4+), or `logs` (stack 9.2–9.3)
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

- {applies_to}`stack: preview 9.2-9.3` Set the endpoint to `logs`. Only the `logs` endpoint is available in these versions.
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.4+` Set the endpoint to `logs.otel` or `logs.ecs`, depending on which endpoint you want to use.
:::

Send data to the endpoint using the [Bulk API]({{es-apis}}operation/operation-bulk):

```json
POST /logs.otel/_bulk # Set to `logs.otel` or `logs.ecs` (serverless or stack 9.4+), or `logs` (stack 9.2–9.3)
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

## Work with existing data [get-data-in-classic]

Classic streams let you use the Streams UI to extract fields and configure data retention for data that's already being ingested into {{es}} without additional configuration.

Classic streams:

- Are based on existing data streams, index templates, and component templates.
- Can follow the data retention policy set in the existing index template.
- Do not support hierarchical inheritance or cascading configuration updates.

Open classic streams from the following places in {{kib}}:

- Select **Streams** from the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md), and find the data stream in the Streams table.

- Open the data stream for a specific document from **Discover**. To do this, expand the details flyout for a document stored in a data stream, and select **Stream** or an action associated with the document's data stream. Streams then opens filtered to the selected data stream.

You can also access Streams features using the Streams API. {applies_to}`stack: preview 9.1+` {applies_to}`serverless: preview` Refer to the [Streams API documentation]({{kib-apis}}group/endpoint-streams) for more information.

## Next steps [get-data-in-next-steps]

Once your data is flowing into Streams, you can start organizing and enriching it:

- **[Organize your data](./organize-your-data.md)**: Use partitioning to route data subsets into dedicated child streams with independent retention and processing rules. Partitioning is only available for wired streams.
- **[Parse and process](./parse-and-process.md)**: Build a processing pipeline to extract structured fields from raw log messages using AI-generated or manually configured processors.

