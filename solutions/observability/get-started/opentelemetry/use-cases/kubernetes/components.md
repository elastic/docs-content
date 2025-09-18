---
navigation_title: Components description
description: Description of components involved in Kubernetes observability with OpenTelemetry, including Operator, Collectors, Helm Chart, and auto-instrumentation.
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

# Components description

Getting started with OpenTelemetry for Kubernetes observability requires an understanding of the following components, their functions, and interactions: 

- OpenTelemetry Operator
- Collectors
- Kube-stack Helm Chart
- Auto-instrumentation resources

## OpenTelemetry Operator

The OpenTelemetry Operator is a [Kubernetes Operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) implementation designed to manage OpenTelemetry resources in a Kubernetes environment.

The operator defines and oversees the following Custom Resource Definitions (CRDs):

- [OpenTelemetry Collectors](https://github.com/open-telemetry/opentelemetry-collector): Agents responsible for receiving, processing, and exporting telemetry data such as logs, metrics, and traces.
- [Instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic): Leverages OpenTelemetry instrumentation libraries to automatically instrument workloads.

All signals including logs, metrics, and traces are processed by the collectors and sent directly to {{es}} using the [Elasticsearch exporter](elastic-agent://reference/edot-collector/components/elasticsearchexporter.md). A collector's processor pipeline replaces the traditional APM server functionality for handling application traces.

## Kube-stack Helm Chart

The [kube-stack Helm chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack) manages the installation of the operator, including its CRDs. It also configures a suite of collectors, which instrument various Kubernetes components to add observability and monitoring.

The chart is installed with a provided default `values.yaml` file that can be customized when needed.

## DaemonSet collectors

The OpenTelemetry components deployed within the DaemonSet collectors are responsible for observing specific signals from each node. To ensure complete data collection, these components must be deployed on every node in the cluster. Failing to do so results in partial and potentially incomplete data.

The DaemonSet collectors handle the following data:

- Host Metrics: Collects host metrics specific to each node, through the hostmetrics receiver.
- Kubernetes Metrics: Captures metrics related to the Kubernetes infrastructure on each node.
- Logs: Uses the filelog receiver to gather logs from all Pods running on the respective node.
- OTLP Traces Receiver: Opens an HTTP and a GRPC port on the node to receive OTLP trace data.

## Deployment collector

The OpenTelemetry components deployed within a Deployment collector focus on gathering data at the cluster level rather than at individual nodes. Unlike DaemonSet collectors, which need to be deployed on every node, a Deployment collector operates as a standalone instance.

The Deployment collector handles the following data:

- Kubernetes Events: Monitors and collects events occurring across the entire Kubernetes cluster.
- Cluster Metrics: Captures metrics that provide insights into the overall health and performance of the Kubernetes cluster.

## Auto-instrumentation

The Helm chart is configured to enable zero-code instrumentation using the [Operator's Instrumentation resource](https://github.com/open-telemetry/opentelemetry-operator/?tab=readme-ov-file#opentelemetry-auto-instrumentation-injection) for the following programming languages:

- Go
- Java
- Node.js
- Python
- .NET
