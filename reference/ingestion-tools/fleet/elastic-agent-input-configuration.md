---
navigation_title: "Inputs"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-input-configuration.html
---

# Configure inputs for standalone {{agent}}s [elastic-agent-input-configuration]


The `inputs` section of the `elastic-agent.yml` file specifies how {{agent}} locates and processes input data.

* [Sample metrics input configuration](#elastic-agent-input-configuration-sample-metrics)
* [Sample log files input configuration](#elastic-agent-input-configuration-sample-logs)


## Sample metrics input configuration [elastic-agent-input-configuration-sample-metrics]

By default {{agent}} collects system metrics, such as CPU, memory, network, and file system metrics, and sends them to the default output. For example, to define datastreams for `cpu`, `memory`, `network` and `filesystem` metrics, this is the configuration:

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

1. The name of the input. Refer to [{{agent}} inputs](/reference/ingestion-tools/fleet/elastic-agent-inputs-list.md) for the list of what’s available.
2. A unique ID for the input.
3. A user-defined namespace.
4. The name of the `output` to use. If not specified, `default` will be used.
5. The set of enabled module metricsets.Refer to the {{metricbeat}} [System module](beats://docs/reference/metricbeat/metricbeat-module-system.md) for a list of available options. The metricset fields can be configured.

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

1. The name of the input. Refer to [{{agent}} inputs](/reference/ingestion-tools/fleet/elastic-agent-inputs-list.md) for the list of what’s available.
2. A unique ID for the input.
3. A unique ID for the data stream to track the state of the ingested files.
4. The streams block is required only if multiple streams are used on the same input. Refer to the {{filebeat}} [filestream](beats://docs/reference/filebeat/filebeat-input-filestream.md) documentation for a list of available options. Also, specifically for the `filestream` input type, refer to the [simplified log ingestion](/reference/ingestion-tools/fleet/elastic-agent-simplified-input-configuration.md) for an example of ingesting a set of logs specified as an array.


The input in this example harvests all files in the path `/var/log/*.log`, that is, all logs in the directory `/var/log/` that end with `.log`. All patterns supported by [Go Glob](https://golang.org/pkg/path/filepath/#Glob) are also supported here.

To fetch all files from a predefined level of subdirectories, use this pattern: `/var/log/*/*.log`. This fetches all `.log` files from the subfolders of `/var/log`. It does not fetch log files from the `/var/log` folder itself. Currently it is not possible to recursively fetch all files in all subdirectories of a directory.




