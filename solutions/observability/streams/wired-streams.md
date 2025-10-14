---
applies_to:
  stack: preview 9.2
  serverless: preview
products:
  - id: observability
  - id: cloud-serverless
---

# Send data to wired streams [streams-wired-streams]

With wired streams, all logs are sent to a single `/logs` endpoint, from which you can route data into child streams based on [partitioning](./management/partitioning.md) rules you set up manually or with the help of AI suggestions.

To send data to wired streams, you need to:
- [Turn on wired streams](#streams-wired-streams-enable)
- [Configure your data shipper](#streams-wired-streams-ship)

## Turn on wired streams [streams-wired-streams-enable]

To turn on wired streams:

1. From the Streams page, open **Settings**.
1. Turn on **Enable wired streams**.

## Configure your data shipper [streams-wired-streams-ship]

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
Use the **Custom Logs (Filestream)** integration to send data to Wired Streams:

1. find **Fleet** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select the **Settings** tab.
1. Under **Outputs**, find the output you want to use to send data to Streams, and select the {icon}`pencil` icon.
1. Turn on **Write to logs streams**.
1. Add the** Custom Logs (Filestream)** integration to an agent policy.
1. Enable the **Use the "logs" data stream** setting in the integration configuration under **Change defaults**.
1. Under **Where to add this integration**, select an agent policy that uses the output you configured in **Step 4**.
:::

::::

## Next steps

After sending your data to wired streams:

- [Partition data](./management/partitioning.md) using the **Partitioning** tab to send data into meaningful child streams.
- [Extract fields](./extract.md) using the **Processing** tab to filter and analyze your data effectively.
- [Map fields](./schema.md) using the **Schema** tab to make fields easier to query.