---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-configuration.html
---

# Configure standalone Elastic Agents [elastic-agent-configuration]

::::{tip}
To get started quickly, use {{kib}} to create and download a standalone policy file. You’ll still need to deploy and manage the file, though. For more information, refer to [Create a standalone {{agent}} policy](/reference/ingestion-tools/fleet/create-standalone-agent-policy.md) or try out our example: [Use standalone {{agent}} to monitor nginx](/reference/ingestion-tools/fleet/example-standalone-monitor-nginx.md).
::::


Standalone {{agent}}s are manually configured and managed locally on the systems where they are installed. They are useful when you are not interested in centrally managing agents in {{fleet}}, either due to your company’s security requirements, or because you prefer to use another configuration management system.

To configure standalone {{agent}}s, specify settings in the `elastic-agent.yml` policy file deployed with the agent. Prior to installation, the file is located in the extracted {{agent}} package. After installation, the file is copied to the directory described in [Installation layout](/reference/ingestion-tools/fleet/installation-layout.md). To apply changes after installation, you must modify the installed file.

For installation details, refer to [Install standalone {{agent}}s](/reference/ingestion-tools/fleet/install-standalone-elastic-agent.md).

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
      - metricset: cpu
        data_stream.dataset: system.cpu
```

The following sections describe some settings you might need to configure to run an {{agent}} standalone. For a full reference example, refer to the [elastic-agent.reference.yml](/reference/ingestion-tools/fleet/elastic-agent-reference-yaml.md) file.

The settings described here are available for standalone {{agent}}s. Settings for {{fleet}}-managed agents are specified through the UI. You do not set them explicitly in a policy file.


















