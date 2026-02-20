---
applies_to:
  stack: preview 9.2
  serverless: preview
products:
  - id: observability
  - id: cloud-serverless
---

# Wired streams [streams-wired-streams]

Wired streams send your documents to a wired streams endpoint, from which you can route data into child streams based on [partitioning](./management/partitioning.md) rules you set up manually or with the help of AI suggestions.

:::::{applies-switch}

::::{applies-item} { serverless: preview, stack: preview 9.4+ }

Wired streams use the following endpoints:

- **`logs.otel`**: Normalizes data to OpenTelemetry format (field mapping shown in [field naming table](#streams-wired-streams-field-naming))
- **`logs.ecs`**: Preserves original ECS field names without transformation

:::{warning}
The `/logs` endpoint is deprecated in {{stack}} 9.4. [Reenable wired streams](#streams-wired-streams-enable) to update your deployment or project to use the `logs.otel` and `logs.ecs` endpoints.
:::

::::

::::{applies-item} stack: preview 9.2-9.3

Send logs to the `/logs` endpoint, which normalizes data to OpenTelemetry format.

::::

:::::

For more on wired streams, refer to:
- [Wired streams field naming](#streams-wired-streams-field-naming)
- [Turn on wired streams](#streams-wired-streams-enable)
- [Send data to wired streams](#streams-wired-streams-ship)
- [View wired streams in Discover](#streams-wired-streams-discover)

## Wired streams field naming [streams-wired-streams-field-naming]

::::{applies-switch}

:::{applies-item} { serverless: preview, stack: preview 9.4+ }

Field naming depends on the endpoint you use.

### `logs.ecs` endpoint

Data ingested into the `logs.ecs` endpoint is stored in the original ECS field names without being transformed. The fields remain as shown in the "ECS field" column in the [field naming table](#streams-wired-streams-field-name-table).

### `logs.otel` endpoint

Data ingested into the `logs.otel` endpoint is stored and processed in a normalized OpenTelemetry (OTel)–compatible format. This format aligns ECS fields with OTel semantic conventions so all data is consistently structured and OTTL-expressible.

When data is ingested into a wired stream, it’s automatically translated into this normalized format:
- Standard ECS documents are converted to OTel fields (`message → body.text`, `log.level → severity_text`, `host.name → resource.attributes.host.name`, and so on).
- Custom fields are stored under `attributes.*`.

To preserve backward-compatible querying, Streams creates aliases that mirror existing `logs-*.otel-*` data streams behavior. This allows queries to use either ECS or OTel field names interchangeably.

Refer to the following table for ECS fields and corresponding OTel fields.

:::

:::{applies-item} stack: preview 9.2-9.3

Data ingested into the `/logs` endpoint is stored and processed in a normalized OpenTelemetry (OTel)–compatible format. This format aligns ECS fields with OTel semantic conventions so all data is consistently structured and OTTL-expressible.

Data ingested into a wired stream is automatically translated into this normalized format:
- Streams converts standard ECS documents to OTel fields (`message → body.text`, `log.level → severity_text`, `host.name → resource.attributes.host.name`, and so on).
- Streams stores custom fields under `attributes.*`.

To preserve backward-compatible querying, Streams creates aliases that mirror existing `logs-*.otel-*` data streams behavior. This allows queries to use either ECS or OTel field names interchangeably.

Refer to the following table for ECS fields and corresponding OTel fields.

:::

::::

### Field naming table [streams-wired-streams-field-name-table]

The following table lists the ECS fields and the corresponding OTel fields.

| ECS field | OTel field |
|------------|-------------------------|
| `message` | `body.text` |
| `log.level` | `severity_text` |
| `span.id` | `span_id` |
| `trace.id` | `trace_id` |
| `host.name` | `resource.attributes.host.name` |
| `host.ip` | `resource.attributes.host.ip` |
| `custom_field` | `attributes.custom_field` |

## Turn on wired streams [streams-wired-streams-enable]

To turn on wired streams:

1. Go to the **Streams** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then open **Settings**.
1. Turn on **Enable wired streams**.

## Ship data to streams [streams-wired-streams-ship]

To send data to wired streams, configure your shippers to send data to the appropriate wired streams endpoint. To do this, complete the following configurations for your shipper:

:::::{tab-set}

::::{tab-item} OpenTelemetry
:::{note}
Set the index in the following configuration based on your {{stack}} version:

- {applies_to}`stack: preview 9.2-9.3` Set the index to `logs`. Only the `logs` endpoint is available in these versions.
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.4+` Set the index to `logs.otel` or `logs.ecs`, depending on which endpoint you want to use.
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
Set the index in the following configuration based on your {{stack}} version:

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
Set the index in the following configuration based on your {{stack}} version:

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

1. Find **Fleet** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select the **Settings** tab.
1. Under **Outputs**, find the output you want to use to send data to streams, and select the {icon}`pencil` icon.
1. Turn on **Write to logs streams**.
1. Add the **Custom Logs (Filestream)** integration to an agent policy.
1. Enable the **Use the "logs" data stream** setting in the integration configuration under **Change defaults**.
1. Under **Where to add this integration**, select an agent policy that uses the output you configured in step 4.
::::

::::{tab-item} API
:::{note}
Set the endpoint in the following configuration based on your {{stack}} version:

- {applies_to}`stack: preview 9.2-9.3` Set the endpoint to `logs`. Only the `logs` endpoint is available in these versions.
- {applies_to}`serverless: preview` {applies_to}`stack: preview 9.4+` Set the endpoint to `logs.otel` or `logs.ecs`, depending on which endpoint you want to use.
:::

Send data to the endpoint using the [Bulk API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk). Refer to the following example for more information:

```json
POST /logs.otel/_bulk # Set to `logs.otel` or `logs.ecs` (serverless or stack 9.4+), or `logs` (stack 9.2–9.3)
{ "create": {} }
{ "@timestamp": "2025-05-05T12:12:12", "body": { "text": "Hello world!" }, "resource": { "attributes": { "host.name": "my-host-name" } } }
{ "create": {} }
{ "@timestamp": "2025-05-05T12:12:12", "message": "Hello world!", "host.name": "my-host-name" }
```
::::

:::::

## View wired streams in Discover [streams-wired-streams-discover]

To view wired log streams in Discover:

1. Manually [create a data view](../../../explore-analyze/find-and-organize/data-views.md#settings-create-pattern) for the wired streams index pattern (`logs,logs.*`).
1. add the wireds streams index pattern (`logs,logs.*`) to the `observability:logSources` {{kib}} advanced setting, which you can open from the navigation menu or by using the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).

## Next steps

After sending your data to wired streams:

- [Partition data](./management/partitioning.md): Use the **Partitioning** tab to send data into meaningful child streams.
- [Extract fields](./management/extract.md): Use the **Processing** tab to filter and analyze your data effectively.
- [Map fields](./management/schema.md): Use the **Schema** tab to make fields easier to query.
