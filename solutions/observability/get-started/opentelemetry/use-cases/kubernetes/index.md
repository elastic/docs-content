---
navigation_title: Kubernetes observability
description: Detailed description of the Kubernetes setup for EDOT, including components and customization guidance.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_collector: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Kubernetes observability with EDOT

The [quickstart guides](/solutions/observability/get-started/opentelemetry/quickstart/index.md) for Kubernetes install a set of different EDOT Collectors and EDOT SDKs to cover collection of OpenTelemetry data for infrastructure monitoring, logs collection and application monitoring.

The Kubernetes setup relies on the OpenTelemetry Operator, configured to automate orchestration of EDOT as follows:

* EDOT Collector Cluster: Collection of cluster metrics.
* EDOT Collector Daemon: Collection of node metrics, logs, and application telemetry.
* EDOT Collector Gateway: Preprocessing, aggregation, and ingestion of data into Elastic.
* EDOT SDKs: Annotated applications are auto-instrumented with [EDOT SDKs](opentelemetry://reference/edot-sdks/index.md).

The following diagram summarizes the previous components and how they interact with Elastic:

![K8s-architecture](../../images/EDOT-K8s-architecture.png)

Read on to learn how to:

- Install the [OpenTelemetry Operator](https://github.com/open-telemetry/opentelemetry-operator/) using the [kube-stack Helm chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack).
- Use the EDOT Collectors to send Kubernetes logs, metrics, and application traces to an {{es}} cluster.
- Use the operator for applications [auto-instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic/) in all supported languages.
