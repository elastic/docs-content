---
navigation_title: Elastic Agent as an OTel Collector
applies_to:
  stack: ga 9.3+
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# {{agent}} as an OpenTelemetry Collector [elastic-agent-otel-collector]

Starting with version 9.3, {{agent}} runs the [Elastic Distribution of OpenTelemetry (EDOT) Collector](elastic-agent://reference/edot-collector/index.md). Rather than managing separate {{beats}} sub-processes, the agent collects data through an embedded OpenTelemetry (OTel) Collector process, leveraging the extensibility and interoperability of the OTel ecosystem. This architecture brings OTel capabilities while maintaining compatibility with existing {{beats}}-based workflows and integrations.

This transition is incremental: in 9.3, agent self-monitoring uses the OTel runtime by default, while data collection inputs will be migrated to run as OTel receivers over subsequent releases. Existing integrations and agent configurations continue to work without disruption.

## Architecture overview [architecture-overview]

Previously {{agent}} acted as a supervisor that launched and managed individual {{beats}} processes to collect telemetry ({{filebeat}}, {{metricbeat}}, and others), each running as a separate sub-process. 

With the new {{agent}} OTel Collector architecture:

*  {{agent}} embeds the EDOT Collector as its runtime, eliminating the overhead associated with managing separate sub-processes.
* Instead of running as individual {{beats}} processes, Beat inputs can run inside the EDOT Collector as [Beat receivers](#beat-receivers).
* {{agent}} leverages OTel receivers and pipelines to ingest, process, and export telemetry data in a unified, standard manner within a single OTel Collector process, reducing the agent's footprint.
* OTel-native receivers and pipelines run in the same Collector alongside Beat receivers.
* Backward compatibility is preserved: existing {{beats}}-based integrations continue to work through Beat receivers without configuration changes.

:::{image} images/elastic-agent-otel-architecture.png
:alt: Diagram showing data ingestion with Beat receivers and OTel receivers as part of an OTel Collector
:::

:::{note}
In {{agent}} 9.3 and later, the component that implements {{beats}}-based integrations is named `elastic-otel-collector`. For more information, refer to [{{agent}} installation flavors](/reference/fleet/install-elastic-agents.md#elastic-agent-installation-flavors).
:::

## Beat receivers [beat-receivers]

A _Beat receiver_ is a Beat input and its associated processors, wrapped to run as an OTel receiver inside the EDOT Collector. Beat receivers produce the exact same data, formatted according to the [Elastic Common Schema](ecs://reference/index.md) (ECS), as current Beat inputs. Beat receivers don't output data in the OTLP schema.

When Beat receivers are enabled, {{agent}} automatically translates the relevant parts of its standalone or {{fleet}}-generated `elastic-agent.yml` file into an OTel Collector configuration. 

The data path works as follows:

1. A Beat input (like `filestream`) collects data.
2. Beat-specific processors transform the data.
3. The data passes through OTel processing.
4. An exporter ({{es}}, {{ls}}, or Kafka) writes the data to the output destination.
5. As with {{beats}} and {{agent}} configurations for Beat inputs, data can be processed by ingest pipelines before being stored in {{es}}.

:::{image} images/elastic-agent-otel-architecture-beat-receiver.png
:alt: Diagram showing data ingestion with a Beat receiver
:::

### Configuration compatibility [beat-receivers-compatibility]

The introduction of Beat receivers does not require configuration changes. Upgrading to 9.3 changes the internal runtime of {{agent}} to use Beat receivers by default, but inputs and outputs remain consistent for integration data.

**{{fleet}}-managed agents:** The same {{beats}}-based integration packages continue to work. These packages configure the relevant Beat receivers automatically. Assets such as dashboards, alerts, and ingest pipelines remain unchanged.

**Standalone agents:** Existing standalone configurations are accepted as before. {{agent}} generates the OTel Collector configuration internally.

This example shows a {{filebeat}} input configuration and its respective generated OTel configuration:

:::{image} images/elastic-agent-otel-architecture-beat-receiver-config.png
:alt: Beat input configuration translated into an OTel configuration
:::

## {{agent}} as a hybrid agent [hybrid-elastic-agent]

The term _hybrid agent_ refers to an {{agent}} that collects data using two methods at the same time:

* **{{beats}}-based data collection:** The agent uses Beat inputs or Beat receivers to collect ECS-formatted data.
* **OTel-native data collection:** The agent uses standard OTel Collector receivers to ingest telemetry data using OTLP, with the data following semantic conventions.

Both methods run inside the same OTel Collector process. This is what makes the agent "hybrid": it combines traditional {{beats}}-based data collection and OTel-native data collection within a single agent instance, rather than requiring separate tools for each. This reduces memory consumption compared to running separate Beat sub-processes alongside a standalone OTel Collector.

In practice, a single `elastic-agent.yml` can contain both an `inputs` and `outputs` section for {{beats}}-based data collection and `receivers`, `exporters`, and `service.pipelines` sections for OTel-based data collection.

This example shows a hybrid agent configuration that collects system auth logs through a Beat input and monitors an HTTP endpoint through an OTel receiver.

```yaml
inputs:
  - id: filestream-system-66cab0a6-6fa3-46b1-9af1-2ea171fbd885
    type: filestream
    data_stream:
      namespace: default
    streams:
      - id: filestream-system.auth-66cab0a6-6fa3-46b1-9af1-2ea171fbd885
        data_stream:
          dataset: system.auth
        paths:
          - /var/log/auth*.log

outputs:
  default:
    type: elasticsearch
    hosts: [127.0.0.1:9200]
    api_key: "your-api-key"

receivers:
  httpcheck/httpcheck-6d24bb0d-5349-4714-a7ea-2088abcb928b:
    collection_interval: 30s
    targets:
      - method: "GET"
        endpoints:
            - https://example.com

exporters:
  debug/default:
    verbosity: detailed

service:
  pipelines:
    metrics/httpcheck-6d24bb0d-5349-4714-a7ea-2088abcb928b:
      receivers: [httpcheck/httpcheck-6d24bb0d-5349-4714-a7ea-2088abcb928b]
      exporters: [debug/default]
```

## OpenTelemetry integrations [otel-integrations]

```{applies_to}
stack: preview 9.2+
```

The {{integrations}} catalog offers packages that bundle application-specific configuration and assets. ECS-based integrations include an agent configuration and {{es}} and {{kib}} assets (dashboards, alerts, ingest pipelines). A similar approach exists for OTel-native data collection:

* **OpenTelemetry input packages** contain the configuration required for the OTel receiver and related pipeline components.
* **Content packages** contain the corresponding set of assets (dashboards, visualizations, and more) for the application whose data is ingested through the OTel receiver.

The same agent policy can include both ECS-based integrations and OpenTelemetry input packages. When you add an OpenTelemetry input package to your agent policy, it configures the OTel receiver section of the hybrid agent configuration. Once data is ingested into {{es}}, the relevant OTel assets are automatically installed when available.

For more details on OpenTelemetry input packages and their configuration, refer to [Collect OpenTelemetry data with {{agent}} integrations](/reference/fleet/otel-integrations.md).

:::{tip}
The same automatic asset deployment applies when using a standalone EDOT Collector: once data is ingested through the collector, it triggers the automatic installation of the relevant OTel assets when available.
:::

## Collector type comparison [collector-comparison]

Depending on your environment, you can use {{agent}} (as described on this page), the standalone [EDOT Collector](elastic-agent://reference/edot-collector/index.md), or a third-party OpenTelemetry Collector to send OTel data to Elastic. The following table highlights the differences between these options in terms of management capabilities and feature support:

| Collector | {{fleet}} central monitoring | {{fleet}} central management | Beat receivers | {{ls}} exporter | {{elastic-defend}} | Cloud Security | Profiler |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Hybrid agent ({{fleet}}-managed) | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") |
| Hybrid agent (standalone) | Planned | ![no](images/red-x.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") | ![no](images/red-x.svg "") | ![no](images/red-x.svg "") |
| EDOT Collector | Planned | Planned | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") | ![no](images/red-x.svg "") | ![no](images/red-x.svg "") |
| Upstream OTel Collector | Planned | Planned | ![no](images/red-x.svg "") | ![no](images/red-x.svg "") | ![no](images/red-x.svg "") | ![no](images/red-x.svg "") | ![no](images/red-x.svg "") |

*Planned* indicates that support is on the roadmap and not yet generally available.

:::{note}
A standalone hybrid {{agent}} can enroll into {{fleet}} in the field if an in-place upgrade to {{fleet}}-managed is required. The standalone EDOT Collector does not support enrollment into {{fleet}}.
:::

## Frequently asked questions [faq]

:::{dropdown} Does the data collected by a hybrid agent go through ingest pipelines?

It depends on which receiver collected the data.

Data collected by a Beat receiver is written by the {{es}} exporter. As with traditional {{agent}} and {{beats}}, this data is processed by ingest pipelines, schematized, and stored in the appropriate data stream.

Data collected by an OTel-native receiver follows OpenTelemetry semantic conventions. When this data arrives at the Elastic cluster, it bypasses ingest pipelines and is stored directly in an OTel-specific data stream.
:::

:::{dropdown} Can you configure Beat receivers in a standalone EDOT Collector?

Yes. To configure Beat receivers in a standalone [EDOT Collector](elastic-agent://reference/edot-collector/index.md), provide a standard OTel Collector configuration and configure Beat receivers manually as `filebeatreceiver` or `metricbeatreceiver`. For example:

```yaml
receivers:
    filebeatreceiver:
        filebeat:
            inputs:
                - data_stream:
                    dataset: generic
                  id: filestream-receiver
                  index: logs-generic-default
                  paths:
                    - /var/log/*.log
                  type: filestream
    metricbeatreceiver:
        metricbeat:
            modules:
                - data_stream:
                    dataset: system.cpu
                  index: metrics-system.cpu-default
                  metricsets:
                    - cpu
                  module: system
```
:::

:::{dropdown} What are the differences between hybrid {{agent}}, EDOT Collector, and a third-party OpenTelemetry Collector?

The main difference is management support. Hybrid {{agent}} can be managed by {{fleet}}. The EDOT Collector does not support {{fleet}} enrollment or central management. Some features, such as {{elastic-defend}}, are only available under {{fleet}} management and cannot be used with the EDOT Collector alone. Refer to the [collector type comparison](#collector-comparison) table for a full breakdown.
:::

:::{dropdown} What is the future of {{agent}} in standalone mode?

Standalone {{agent}} use cases can now be addressed using the EDOT Collector. A practical advantage of the standalone {{agent}} today is that it can be upgraded to {{fleet}}-managed in the field without having to reinstall it.
:::

:::{dropdown} Can data collected with third-party OTel Collectors trigger the automatic installation of relevant assets?

The automatic asset installation from OTel content packages currently works only for data ingested by an EDOT Collector or a hybrid {{agent}}. Data ingested with a third-party OpenTelemetry Collector does not trigger automatic asset installation.
:::

:::{dropdown} Will there be a separate operating system support matrix?

No, the [Elastic system support matrix](https://www.elastic.co/support/matrix) does not change. Where Elastic does not provide {{agent}} support for a specific operating system, you can deploy a third-party OpenTelemetry Collector supported by that vendor and send data to Elastic. For example, Red Hat provides an OTel Collector for OpenShift that can be configured to send data to Elastic. The same configuration can also be used with the EDOT Collector on operating systems that Elastic supports.
:::
