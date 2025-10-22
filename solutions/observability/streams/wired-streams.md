---
applies_to:
  stack: preview 9.2
  serverless: preview
products:
  - id: observability
  - id: cloud-serverless
---

# Wired streams [streams-wired-streams]

With wired streams, all logs are sent to a single `/logs` endpoint, from which you can route data into child streams based on [partitioning](./management/partitioning.md) rules you set up manually or with the help of AI suggestions.

For more on wired streams, refer to:
- [Wired streams field naming](#streams-wired-streams-field-naming)
- [Turn on wired streams](#streams-wired-streams-enable)
- [Send data to wired streams](#streams-wired-streams-ship)
- [View wired streams in Discover](#streams-wired-streams-discover)

## Wired streams field naming [streams-wired-streams-field-naming]

Wired streams store and process data in a normalized OpenTelemetry (OTel)–compatible format. This format aligns Elastic Common Schema (ECS) fields with OTel semantic conventions so all data is consistently structured and OTTL-expressible.

When data is ingested into a wired stream, it’s automatically translated into this normalized format:
- Standard ECS documents are converted to OTel fields (`message → body.text`, `severity_text → log.level`, `host.name → resource.attributes.host.name`, and so on).
- Custom fields are stored under `attributes.*`.

To preserve backward-compatible querying, Streams creates aliases that mirror existing `logs-*.otel-*` data streams behavior. This allows queries to use either ECS or OTel field names interchangeably.

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

To send data to wired streams, configure your shippers to send data to the `/logs` endpoint. To do this, complete the following configurations for your shipper:

::::{tab-set}

:::{tab-item} OpenTelemetry
```yaml
processors:
  transform/logs-streams:
    log_statements:
      - context: resource
        statements:
          - set(attributes["elasticsearch.index"], "logs")
service:
  pipelines:
    logs:
      receivers: [myreceiver] # works with any logs receiver
      processors: [transform/logs-streams]
      exporters: [elasticsearch, otlp] # works with either
```
:::

:::{tab-item} Filebeat
```yaml
filebeat.inputs:
  - type: filestream
    id: my-filestream-id
    index: logs
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
:::

:::{tab-item} Logstash
```json
output {
  elasticsearch {
    hosts => ["<elasticsearch-host>"]
    api_key => "<your-api-key>"
    index => "logs"
    action => "create"
  }
}
```
:::

:::{tab-item} Fleet
Use the **Custom Logs (Filestream)** integration to send data to wired streams:

1. Find **Fleet** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select the **Settings** tab.
1. Under **Outputs**, find the output you want to use to send data to streams, and select the {icon}`pencil` icon.
1. Turn on **Write to logs streams**.
1. Add the **Custom Logs (Filestream)** integration to an agent policy.
1. Enable the **Use the "logs" data stream** setting in the integration configuration under **Change defaults**.
1. Under **Where to add this integration**, select an agent policy that uses the output you configured in step 4.
:::

::::

## View wired streams in Discover [streams-wired-streams-discover]

To view wired log streams in Discover:

1. Manually [create a data view](../../../explore-analyze/find-and-organize/data-views.md#settings-create-pattern) for the wired streams index pattern (`logs,logs.*`).
1. add the wireds streams index pattern (`logs,logs.*`) to the `observability:logSources` {{kib}} advanced setting, which you can open from the navigation menu or by using the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).

## Next steps

After sending your data to wired streams:

- [Partition data](./management/partitioning.md): Use the **Partitioning** tab to send data into meaningful child streams.
- [Extract fields](./management/extract.md): Use the **Processing** tab to filter and analyze your data effectively.
- [Map fields](./management/schema.md): Use the **Schema** tab to make fields easier to query.