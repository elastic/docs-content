---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-infrastructure.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-infrastructure.html
applies_to:
  stack: beta
  serverless: beta
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Infrastructure [observability-apm-infrastructure]

The **Infrastructure** tab provides information about the containers, pods, and hosts that the selected service is linked to. The data sources and navigation behavior depend on whether the service is instrumented with [Elastic {{product.apm}}](#observability-apm-infrastructure-elastic-apm) or [OpenTelemetry (OTel)](#observability-apm-infrastructure-otel).

IT ops and software reliability engineers (SREs) can use this tab to quickly find a service’s underlying infrastructure resources when debugging a problem. Knowing what infrastructure is related to a service allows you to remediate issues by restarting, killing hanging instances, changing configuration, rolling back deployments, scaling up, scaling out, and so on.

::::{tip}
**Why is the infrastructure tab empty?**

If there is no data in the Application UI’s infrastructure tab for a selected service, you can read more about why this happens and how to fix it in the [troubleshooting docs](/troubleshoot/observability/apm/common-problems.md#troubleshooting-apm-infra-data).
::::

## Elastic {{product.apm}}-instrumented services [observability-apm-infrastructure-elastic-apm]

For services instrumented with Elastic {{product.apm}}, the tab uses the following data sources:

* **Pods**: Uses the `kubernetes.pod.name` from the [{{product.apm}} metrics data streams](/solutions/observability/apm/metrics.md).
* **Containers**: Uses the `container.id` from the [{{product.apm}} metrics data streams](/solutions/observability/apm/metrics.md).
* **Hosts**: If the application is containerized—if the {{product.apm}} metrics documents include `container.id`—the `host.name` is used from the infrastructure data streams (filtered by `container.id`). If not, `host.hostname` is used from the {{product.apm}} metrics data streams.

:::{image} /solutions/images/serverless-infra.png
:alt: Example view of the Infrastructure tab in the Applications UI
:screenshot:
:::

## OTel-instrumented services [observability-apm-infrastructure-otel]
```{applies_to}
stack: ga 9.4
serverless: ga
```

For services instrumented with OpenTelemetry, the tab exclusively shows OTel-observed infrastructure. Click-through destinations differ by resource type:

* **Hosts**: Links to the [**Hosts**](/solutions/observability/infra-and-hosts/analyze-compare-hosts.md) UI, which supports OpenTelemetry and its semantic conventions.
* **Containers** and **Pods**: Link to [**Metrics** in Discover](/solutions/observability/infra-and-hosts/discover-metrics.md), as the Containers and Pods UIs do not yet support OTel semantic conventions.

::::{important}
:applies_to: stack: ga 9.4+
The **Infrastructure** tab assumes you're observing the service and its underlying infrastructure (hosts, pods, containers) using the same schema. It infers the schema is inferred from the APM agent name:

**Elastic APM Agent** or **Elastic Agent system integration**: Queries ECS data from Metricbeat or Elastic Agent integrations.

**OTel SDK** or **EDOT SDK**: Queries OpenTelemetry semantic convention (semconv) data from the OTel Collector or EDOT Collector (for example, `hostmetricsreceiver.otel`, `kubeletstatsreceiver.otel`, `dockerstatsreceiver.otel`).
Cross-schema setups show as **N/A**:

- A service instrumented with Elastic APM or Elastic Agent, but running on infrastructure observed only by the OTel Collector.
- A service instrumented with an OTel or EDOT SDK, but running on infrastructure observed only by Metricbeat or the Elastic Agent system, Kubernetes, or Docker integrations.

To see infrastructure metrics, make sure the service instrumentation and the infrastructure collector use the same schema.
::::
