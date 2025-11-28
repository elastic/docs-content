---
navigation_title: Kubernetes
description: Learn how to set up the EDOT Collector and EDOT SDKs in a Kubernetes environment to collect host metrics, logs and application traces.
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

# Quickstart for Kubernetes on self-managed deployments

Learn how to set up the EDOT Collector and EDOT SDKs in a Kubernetes environment to collect host metrics, logs and application traces.

## Guided setup

:::{include} ../../_snippets/guided-instructions.md
:::

## Prerequisites

To use the EDOT Collector chart, you need Helm version 3.9+ up to and including {{helm-version}}.

## Manual installation

Follow these steps to deploy the EDOT Collector and EDOT OTel SDKs in Docker.

:::::{stepper}

::::{step} Add the OpenTelemetry repository to Helm

```bash
helm repo add open-telemetry 'https://open-telemetry.github.io/opentelemetry-helm-charts' --force-update
```
::::

::::{step} Set up credentials

Retrieve your [{{es}} endpoint](/solutions/search/search-connection-details.md) and [API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) and replace both in the following command to create a namespace and a secret with your credentials.

```bash
kubectl create namespace opentelemetry-operator-system
kubectl create secret generic elastic-secret-otel \
--namespace opentelemetry-operator-system \
--from-literal=elastic_endpoint='<ELASTICSEARCH_ENDPOINT>' \
--from-literal=elastic_api_key='<ELASTIC_API_KEY>'
```

::::

::::{step} Install the operator

Install the OpenTelemetry Operator using the `kube-stack` Helm chart with the pre-configured `values.yaml` file.

```bash subs=true
helm install opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
--namespace opentelemetry-operator-system \
--values 'https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v{{version.edot_collector}}/deploy/helm/edot-collector/kube-stack/values.yaml' \
--version '{{kube-stack-version}}'
```

::::

::::{step} Auto-instrument applications

Add a language-specific annotation to your namespace by replacing `<LANGUAGE>` with one of the supported values (`nodejs`, `java`, `python`, `dotnet` or `go`) in the following command. 

```bash
kubectl annotate namespace YOUR_NAMESPACE instrumentation.opentelemetry.io/inject-<LANGUAGE>="opentelemetry-operator-system/elastic-instrumentation"
```

Restart your deployment to ensure the annotations and auto-instrumentations are applied.

For languages where auto-instrumentation is not available, you will need to manually instrument your application. See the [Setup section in the corresponding SDK](opentelemetry://reference/edot-sdks/index.md).
::::

::::{step} Install the content packs

Install the **[Kubernetes OpenTelemetry Assets](integration-docs://reference/kubernetes_otel.md)** and **[System OpenTelemetry Assets](integration-docs://reference/system_otel.md)** integrations in {{kib}}.

::::

::::{step} Explore your data

Go to {{kib}} and select **Dashboards** to explore your newly collected data.

::::
:::::

## Troubleshooting

Having issues with EDOT? Refer to the [Troubleshooting common issues with the EDOT Collector](/troubleshoot/ingest/opentelemetry/edot-collector/index.md) and [Troubleshooting the EDOT SDKs](/troubleshoot/ingest/opentelemetry/edot-sdks/index.md) for help.