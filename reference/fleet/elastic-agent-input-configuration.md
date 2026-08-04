---
navigation_title: Inputs
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-input-configuration.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Configure inputs for standalone {{agent}}s [elastic-agent-input-configuration]


The `inputs` section of the `elastic-agent.yml` file specifies how {{agent}} locates and processes input data.

* [Find the settings available for an input](#elastic-agent-input-configuration-available-settings)
* [Sample metrics input configuration](#elastic-agent-input-configuration-sample-metrics)
* [Sample log files input configuration](#elastic-agent-input-configuration-sample-logs)


## Find the settings available for an input [elastic-agent-input-configuration-available-settings]

{{agent}} does not define a separate set of settings for each input. Apart from a small number of fields that {{agent}} handles itself, the settings you specify on an input or a stream are passed through unchanged to the underlying collector, such as {{filebeat}} or {{metricbeat}}.

This means you can use any setting documented for the corresponding {{beats}} input or module, even if it doesn't appear in the examples on this page. To find the settings available for an input, look up its `type` in [{{agent}} inputs](/reference/fleet/elastic-agent-inputs-list.md), then follow the link to the {{beats}} documentation for that input or module.

{{agent}} handles the following input fields itself rather than passing them through:

| Setting | Description |
| --- | --- |
| `type` | Required. The type of the input. Must match an input listed in [{{agent}} inputs](/reference/fleet/elastic-agent-inputs-list.md). |
| `id` | A unique ID for the input, used in logging and event metadata. If omitted, it defaults to the input type. |
| `use_output` | The name of the output to write to. Must match an output defined in the same policy. Defaults to `default`. |
| `log_level` | The log level for this input. One of `error`, `warn`, `info`, `debug`, or `trace`. |

For example, the {{metricbeat}} [System module](beats://reference/metricbeat/metricbeat-module-system.md) documents a `cpu.metrics` setting, and `period` is a [standard {{metricbeat}} module option](beats://reference/metricbeat/configuration-metricbeat.md). Both can be set directly on a stream:

```yaml
- type: system/metrics
  id: unique-system-metrics-id
  data_stream.namespace: default
  use_output: default
  streams:
    - metricsets:
        - cpu
      data_stream.dataset: system.cpu
      period: 10s <1>
      cpu.metrics: [percentages, normalized_percentages] <2>
```

1. How often the metricsets are collected.
2. Which CPU metrics to report. Supported values are `percentages`, `normalized_percentages`, and `ticks`. Defaults to `[percentages]`.


## Sample metrics input configuration [elastic-agent-input-configuration-sample-metrics]

By default {{agent}} collects system metrics, such as CPU, memory, network, and file system metrics, and sends them to the default output. For example, to define data streams for `cpu`, `memory`, `network` and `filesystem` metrics, this is the configuration:

```yaml
- type: system/metrics <1>
  id: unique-system-metrics-id <2>
  data_stream.namespace: default <3>
  use_output: default <4>
  streams:
    - metricsets: <5>
      - cpu
      data_stream.dataset: system.cpu <6>
    - metricsets:
      - memory
      data_stream.dataset: system.memory
    - metricsets:
      - network
      data_stream.dataset: system.network
    - metricsets:
      - filesystem
      data_stream.dataset: system.filesystem
```

1. The name of the input. Refer to [{{agent}} inputs](/reference/fleet/elastic-agent-inputs-list.md) for the list of what’s available.
2. A unique ID for the input.
3. A user-defined namespace.
4. The name of the `output` to use. If not specified, `default` will be used.
5. The set of enabled module metricsets. Refer to the {{metricbeat}} [System module](beats://reference/metricbeat/metricbeat-module-system.md) for a list of available options. Any of these options can be set on the stream, as described in [Find the settings available for an input](#elastic-agent-input-configuration-available-settings).

6. A user-defined dataset. It can contain anything that makes sense to signify the source of the data.



## Sample log files input configuration [elastic-agent-input-configuration-sample-logs]

To enable {{agent}} to collect log files, you can use a configuration like the following.

```yaml
- type: filestream <1>
  id: your-input-id <2>
  streams:
    - id: your-filestream-stream-id <3>
      data_stream: <4>
        dataset: generic
      paths:
        - /var/log/*.log
```

1. The name of the input. Refer to [{{agent}} inputs](/reference/fleet/elastic-agent-inputs-list.md) for the list of what’s available.
2. A unique ID for the input.
3. A unique ID for the data stream to track the state of the ingested files.
4. The streams block is required only if multiple streams are used on the same input. Refer to the {{filebeat}} [filestream](beats://reference/filebeat/filebeat-input-filestream.md) documentation for a list of available options. Also, specifically for the `filestream` input type, refer to the [simplified log ingestion](/reference/fleet/elastic-agent-simplified-input-configuration.md) for an example of ingesting a set of logs specified as an array.


The input in this example harvests all files in the path `/var/log/*.log`, that is, all logs in the directory `/var/log/` that end with `.log`. All patterns supported by [Go Glob](https://golang.org/pkg/path/filepath/#Glob) are also supported here.

To fetch all files from a predefined level of subdirectories, use this pattern: `/var/log/*/*.log`. This fetches all `.log` files from the subfolders of `/var/log`. It does not fetch log files from the `/var/log` folder itself. Currently it is not possible to recursively fetch all files in all subdirectories of a directory.




