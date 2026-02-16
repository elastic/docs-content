---
navigation_title: Prerequisites and compatibility
description: Prerequisites and compatibility information for monitoring Kubernetes with EDOT.
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

# Prerequisites

Before setting up observability for Kubernetes, make sure you have the following:

- Elastic Stack (self-managed or [Elastic Cloud](https://www.elastic.co/cloud)) version 8.16.0 or higher, or an [{{es-serverless}}](/solutions/search.md) project.

- A Kubernetes version supported by the OpenTelemetry Operator. Refer to the operator's [compatibility matrix](https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/compatibility.md#compatibility-matrix) for more details.

- If you opt for automatic certificate generation and renewal on the OpenTelemetry Operator, install [cert-manager](https://cert-manager.io/docs/installation/) in the Kubernetes cluster. By default, the operator uses a self-signed certificate and doesn't require cert-manager.

## Compatibility matrix

The minimum supported version of the Elastic Stack for OpenTelemetry-based monitoring on Kubernetes is `8.16.0`. Different Elastic Stack releases support specific versions of the [kube-stack Helm chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack).

You can download the values file for a specific {{stack}} version from the following URL:

```
https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v<STACK_VERSION>/deploy/helm/edot-collector/kube-stack/values.yaml
```

Where `<STACK_VERSION>` is the version of the Elastic Stack you are using, for example `9.1.2`.

For Serverless, use the [latest version of the values file](https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v{{version.edot_collector}}/deploy/helm/edot-collector/kube-stack/managed_otlp/values.yaml). For version 8.16.0, use [this chart](https://raw.githubusercontent.com/elastic/opentelemetry/refs/heads/8.16/resources/kubernetes/operator/helm/values.yaml).

:::{important}
When [installing the release](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/deployment.md), make sure you use the right `--version` and `-f <values-file>` parameters.

The latest Helm chart version is {{kube-stack-version}}.
:::
