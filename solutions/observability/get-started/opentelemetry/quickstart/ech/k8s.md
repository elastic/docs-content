---
navigation_title: Kubernetes
description: Learn how to set up the {{agent}} and EDOT SDKs in a Kubernetes environment with Elastic Cloud Hosted to collect metrics, logs, and traces using the Managed OTLP Endpoint.
applies_to:
  deployment:
    ech: ga
products:
  - id: cloud-hosted
  - id: observability
  - id: edot-collector
---

# Quickstart for Kubernetes on {{product.cloud-hosted}}

Learn how to set up the {{agent}} and EDOT SDKs in a {{k8s}} environment with {{ech}} (ECH) to collect host metrics, logs, and application traces. This quickstart uses the [{{motlp}}](opentelemetry://reference/motlp.md), which is the recommended ingestion path for ECH.

## Guided setup

:::{include} ../../_snippets/guided-instructions.md
:::

If you need to manage credentials manually, for example, to use them in automation or to configure multiple environments, follow the steps below.

## Prerequisites

- An {{ech}} deployment running version 9.0 or later.
- Helm version 3.9+ up to and including {{helm-version}}.

## Manual installation

Follow these steps to deploy the {{agent}} and EDOT SDKs in {{k8s}} with ECH:

:::::{stepper}

::::{step} Add the repository to Helm

Run the following command to add the charts repository to Helm:

```bash
helm repo add open-telemetry "https://open-telemetry.github.io/opentelemetry-helm-charts" --force-update
```

::::

::::{step} Find your endpoint and create an API key

:::{include} ../../_snippets/retrieve-credentials-ech-motlp.md
:::

::::

::::{step} Configure your credentials

Replace `<ELASTIC_OTLP_ENDPOINT>` and `<ELASTIC_API_KEY>` in the following command to create a namespace and a secret with your credentials.

```bash
kubectl create namespace opentelemetry-operator-system
kubectl create secret generic elastic-secret-otel \
--namespace opentelemetry-operator-system \
--from-literal=elastic_otlp_endpoint='<ELASTIC_OTLP_ENDPOINT>' \
--from-literal=elastic_api_key='<ELASTIC_API_KEY>'
```

:::{note}
On Windows PowerShell, replace backslashes (`\`) with backticks (`` ` ``) for line continuation and single quotes (`'`) with double quotes (`"`).
:::

::::

::::{step} Install the Operator

Install the OpenTelemetry Operator using the `kube-stack` Helm chart with the `managed_otlp` values file:

```bash subs=true
helm install opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
--namespace opentelemetry-operator-system \
--values 'https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v{{version.edot_collector}}/deploy/helm/edot-collector/kube-stack/managed_otlp/values.yaml' \
--version '{{kube-stack-version}}'
```

The Operator provides a deployment of the {{agent}} and configuration environment variables. This allows SDKs and instrumentation to send data to the {{agent}} without further configuration.

For details about the pipelines, refer to [Managed OTLP Endpoint](elastic-agent://reference/edot-collector/config/default-config-k8s.md#managed-otlp-endpoint).

::::

::::{step} Auto-instrument applications

Add a language-specific annotation to your namespace by replacing `<LANGUAGE>` with one of the supported values (`nodejs`, `java`, `python`, `dotnet`, or `go`) in the following command.

```bash
kubectl annotate namespace YOUR_NAMESPACE instrumentation.opentelemetry.io/inject-<LANGUAGE>="opentelemetry-operator-system/elastic-instrumentation"
```

The OpenTelemetry Operator automatically provides the OTLP endpoint configuration and authentication to the SDKs through environment variables. Restart your deployment to ensure the annotations and auto-instrumentations are applied.

For languages where auto-instrumentation is not available, manually instrument your application. See the [Setup section in the corresponding SDK](opentelemetry://reference/edot-sdks/index.md).

::::

::::{step} Install the content packs

Install the **[Kubernetes OpenTelemetry Assets](integration-docs://reference/kubernetes_otel.md)** and **[System OpenTelemetry Assets](integration-docs://reference/system_otel.md)** integrations in {{kib}}.

::::

::::{step} Explore your data

Go to {{kib}} and select **Dashboards** to explore your newly collected data.

::::

:::::

## Using the `elasticsearch` exporter

If you need to write telemetry directly to {{es}} (for example, for pipeline customizations not yet supported through {{motlp}}), use the following configuration instead.

Create the secret with your {{es}} endpoint:

```bash
kubectl create namespace opentelemetry-operator-system
kubectl create secret generic elastic-secret-otel \
--namespace opentelemetry-operator-system \
--from-literal=elastic_endpoint='<ELASTICSEARCH_ENDPOINT>' \
--from-literal=elastic_api_key='<ELASTIC_API_KEY>'
```

Install the Operator using the standard values file:

```bash subs=true
helm install opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
--namespace opentelemetry-operator-system \
--values 'https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v{{version.edot_collector}}/deploy/helm/edot-collector/kube-stack/values.yaml' \
--version '{{kube-stack-version}}'
```

For details about the pipelines, refer to [Direct ingestion into {{es}}](elastic-agent://reference/edot-collector/config/default-config-k8s.md#direct-ingestion-into-elasticsearch).

## Troubleshooting

The following issues might occur.

### API key prefix not found

The following error is due to an improperly formatted API key, and typically occurs when credentials are configured manually:

```txt
Exporting failed. Dropping data.
{"kind": "exporter", "data_type": }
"Unauthenticated desc = ApiKey prefix not found"
```

For a Collector, format the header as `"Authorization": "ApiKey <api-key>"`. For an SDK, format it as `"Authorization=ApiKey <api-key>"`.

For additional troubleshooting, refer to [Troubleshooting common issues with the {{agent}}](/troubleshoot/ingest/opentelemetry/edot-collector/index.md) and [Troubleshooting the EDOT SDKs](/troubleshoot/ingest/opentelemetry/edot-sdks/index.md).
