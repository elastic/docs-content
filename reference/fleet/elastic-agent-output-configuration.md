---
navigation_title: Outputs
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-output-configuration.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Configure outputs for standalone {{agent}}s [elastic-agent-output-configuration]


The `outputs` section of the `elastic-agent.yml` file specifies where to send data. You can specify multiple outputs to pair specific inputs with specific outputs.

An output named `default` is required. {{agent}} sends data to it from any input that doesn't specify another output with `use_output`. {{agent}} monitoring data also goes to the `default` output, unless you choose a different output in the [monitoring settings](/reference/fleet/elastic-agent-monitoring-configuration.md).

This example configures two outputs: `default` and `monitoring`:

```yaml
outputs:
  default:
    type: elasticsearch
    hosts: ["localhost:9200"]
    api_key: "my_api_key"

  monitoring:
    type: elasticsearch
    hosts: ["localhost:9200"]
    api_key: "my_monitoring_api_key"
```

{{agent}} currently supports these outputs:

* [{{es}}](/reference/fleet/elasticsearch-output.md)
* [Kafka](/reference/fleet/kafka-output.md)
* [{{ls}}](/reference/fleet/logstash-output.md)

## Turn off default processors for an output [elastic-agent-output-default-processors]

```{applies_to}
stack: ga 9.6+
```

Depending on the input, {{agent}} uses its default processors to add host, cloud, Docker, and {{k8s}} metadata to the events it collects. To turn off some or all of these processors only for the data sent to a specific output, add `default_processors` to that output.

The `default_processors` setting accepts the same options for every output type:

* `enabled`: Turns all four processors on or off at once. Set to `false` to turn them all off.
* `add_host_metadata`, `add_cloud_metadata`, `add_docker_metadata`, and `add_kubernetes_metadata`: Turn the individual processors on or off. Set a processor to `false` to turn it off. The processors you don't list stay on.

Individual processor settings take precedence over `enabled`. For example, to keep only cloud metadata, set `enabled` to `false` and `add_cloud_metadata` to `true`.

An output's `default_processors` setting can only turn processors off. If you turn off a processor for all outputs in the [default processors feature flag](/reference/fleet/elastic-agent-standalone-feature-flags.md#elastic-agent-standalone-feature-flag-default-processors), setting it to `true` for a specific output doesn't turn it back on.

Turning off a processor removes the fields it adds. Check that the dashboards, alerts, and other features you use don't rely on those fields.

An output's `default_processors` setting also applies to the monitoring data that {{agent}} sends to that output. To choose which output receives monitoring data, refer to [Configure monitoring for standalone {{agent}}s](/reference/fleet/elastic-agent-monitoring-configuration.md).

In this example, data sent to the `default` output doesn't include Docker or {{k8s}} metadata, and data sent to the `monitoring` output doesn't include any of the four types of metadata:

```yaml
outputs:
  default:
    type: elasticsearch
    hosts: ["localhost:9200"]
    api_key: "my_api_key"
    default_processors:
      add_docker_metadata: false
      add_kubernetes_metadata: false

  monitoring:
    type: elasticsearch
    hosts: ["localhost:9200"]
    api_key: "my_monitoring_api_key"
    default_processors:
      enabled: false
```

For {{fleet}}-managed {{agents}}, add `default_processors` to the **Advanced YAML configuration** of the output in {{fleet}}. Refer to the [{{es}}](/reference/fleet/es-output-settings.md#es-output-settings-yaml-config), [{{ls}}](/reference/fleet/ls-output-settings.md#ls-output-settings-yaml-config), or [Kafka](/reference/fleet/kafka-output-settings.md#kafka-output-settings-yaml-config) output settings.

