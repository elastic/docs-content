---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-configuration.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Configure standalone Elastic Agents [elastic-agent-configuration]

::::{tip}
To get started quickly, use {{kib}} to create and download a standalone policy file. You’ll still need to deploy and manage the file, though. For more information, refer to [Create a standalone {{agent}} policy](/reference/fleet/create-standalone-agent-policy.md) or try out our example: [Use standalone {{agent}} to monitor nginx](/reference/fleet/example-standalone-monitor-nginx.md).
::::


Standalone {{agent}}s are manually configured and managed locally on the systems where they are installed. They are useful when you are not interested in centrally managing agents in {{fleet}}, either due to your company’s security requirements, or because you prefer to use another configuration management system.

To configure standalone {{agent}}s, specify settings in the `elastic-agent.yml` policy file deployed with the agent. Prior to installation, the file is located in the extracted {{agent}} package. After installation, the file is copied to the directory described in [Installation layout](/reference/fleet/installation-layout.md). To apply changes after installation, you must modify the installed file.

For installation details, refer to [Install standalone {{agent}}s](/reference/fleet/install-standalone-elastic-agent.md).

Alternatively, you can put input configurations in YAML files into the folder `{path.config}/inputs.d` to separate your configuration into multiple smaller files. The YAML files in the `inputs.d` folder should contain input configurations only. Any other configurations are ignored. The files are reloaded at the same time as the standalone configuration.

::::{tip}
The first line of the configuration must be `inputs`. Then you can list the inputs you would like to run. Each input in the policy must have a unique value for the `id` key. If the `id` key is missing its value defaults to the empty string `""`.
::::


```yaml
inputs:
  - id: unique-logfile-id
    type: logfile
    data_stream.namespace: default
    paths: [/path/to/file]
    use_output: default

  - id: unique-system-metrics-id
    type: system/metrics
    data_stream.namespace: default
    use_output: default
    streams:
      - metricsets:
          - cpu
        data_stream.dataset: system.cpu
```

## Minimum configuration [elastic-agent-configuration-minimum]

To run a standalone {{agent}}, the `elastic-agent.yml` file needs two things: an output that describes where to send data, and at least one input that describes what to collect.

```yaml
outputs:
  default: <1>
    type: elasticsearch
    hosts: ['https://my-deployment.es.us-central1.gcp.cloud.es.io:443']
    api_key: 'example-key' <2>

inputs:
  - type: system/metrics <3>
    id: unique-system-metrics-id <4>
    streams:
      - metricsets:
          - cpu
        data_stream.dataset: system.cpu
```

1. Inputs write to the output named `default` unless they specify a different one with `use_output`.
2. The agent needs credentials to write to {{es}}. Refer to [Grant standalone {{agent}}s access to {{es}}](/reference/fleet/grant-access-to-elasticsearch.md) for the required privileges and the steps to create an API key.
3. The input type. Refer to [{{agent}} inputs](/reference/fleet/elastic-agent-inputs-list.md) for the full list.
4. Each input must have a unique ID.

To collect data that requires an ingest pipeline or dashboards, you also need to install the corresponding integration assets. Refer to [Install standalone {{agent}}s](/reference/fleet/install-standalone-elastic-agent.md) for the full installation procedure.

The following sections describe the other settings you might need to configure. For a full reference example, refer to the [elastic-agent.reference.yml](/reference/fleet/elastic-agent-reference-yaml.md) file.

The settings described here are available for standalone {{agent}}s. Settings for {{fleet}}-managed agents are specified through the UI. You do not set them explicitly in a policy file.


















