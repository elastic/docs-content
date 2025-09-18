---
navigation_title: Upgrade
description: Instructions for upgrading the EDOT Helm chart release for Kubernetes monitoring.
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

# Upgrade

:::{note}
Before upgrading or updating the release configuration, refer to the [compatibility matrix](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/prerequisites-compatibility.md#compatibility-matrix) for a list of supported versions and [customizing configuration](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/customization.md) for a list of supported configurable parameters.
:::

To upgrade an installed release, run a `helm upgrade` command providing the desired chart version and using the correct `values.yaml` for your environment. For example:

```bash subs=true
helm repo update open-telemetry # update information of available charts locally
helm search repo open-telemetry/opentelemetry-kube-stack --versions # list available versions of the chart

helm upgrade --namespace opentelemetry-operator-system opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
--values 'https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v{{version.edot_collector}}/deploy/helm/edot-collector/kube-stack/values.yaml' \
--version {{kube-stack-version}}
```

If [cert-manager integration](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/customization.md#cert-manager-integrated-installation) is disabled, Helm generates a new self-signed TLS certificate with every update, even if there are no actual changes to apply.