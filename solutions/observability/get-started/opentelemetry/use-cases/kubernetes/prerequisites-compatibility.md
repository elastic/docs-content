---
navigation_title: Prerequisites and compatibility
description: Prerequisites and compatibility information for monitoring Kubernetes with {{edot}}.
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

# Prerequisites and compatibility for Kubernetes observability with {{edot}} [k8s-edot-prerequisites]

Before setting up observability for Kubernetes, make sure you have the following:

- Elastic Stack (self-managed or [Elastic Cloud](https://www.elastic.co/cloud)) version 8.16.0 or higher, or an [{{es-serverless}}](/solutions/search.md) project.

- A Kubernetes version supported by the OpenTelemetry Operator. Refer to the operator's [compatibility matrix](https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/getting-started/compatibility.md#compatibility-matrix) for more details.

- If you opt for automatic certificate generation and renewal on the OpenTelemetry Operator, install [cert-manager](https://cert-manager.io/docs/installation/) in the Kubernetes cluster. By default, the operator uses a self-signed certificate and doesn't require cert-manager.

## Compatibility matrix

The minimum supported version of the Elastic Stack for OpenTelemetry-based monitoring on Kubernetes is `8.16.0`. Different Elastic Stack releases support specific versions of the [kube-stack Helm chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack).

Use the values file and installation instructions for your deployment mode:

| Deployment mode | Values file | Installation instructions |
| --- | --- | --- |
| Direct ingestion into {{es}} | `kube-stack/values.yaml` | [Deploy {{edot}} for Kubernetes observability](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/deployment.md) |
| {{motlp}} on {{ech}} | `kube-stack/managed_otlp/values.yaml` | [Quickstart for Kubernetes on {{ech}}](/solutions/observability/get-started/opentelemetry/quickstart/ech/k8s.md) |
| {{motlp}} on {{serverless-short}} | `kube-stack/managed_otlp/values.yaml` | [Quickstart for Kubernetes on {{serverless-full}}](/solutions/observability/get-started/opentelemetry/quickstart/serverless/k8s.md) |

:::{important}
For Elastic Stack `8.16.0`, use the [values file](https://raw.githubusercontent.com/elastic/opentelemetry/refs/heads/8.16/resources/kubernetes/operator/helm/values.yaml) from the `elastic/opentelemetry` repository instead.
:::

The latest supported kube-stack Helm chart version is {{kube-stack-version}}.
