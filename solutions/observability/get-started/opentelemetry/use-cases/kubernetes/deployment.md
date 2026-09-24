---
navigation_title: Deployment
description: Instructions for deploying {{edot}} components for Kubernetes monitoring, using guided onboarding or manual steps.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_collector: ga
products:
  - id: cloud-serverless
  - id: cloud-hosted
  - id: observability
  - id: edot-collector
---

# Deploy {{edot}} for Kubernetes observability [k8s-edot-deployment]

You can use the [guided onboarding](#deploy-using-the-guided-onboarding) or [deploy all components manually](#manual-deployment).

The deployment uses different Helm values files depending on where {{es}} is hosted. For {{serverless-full}} and {{ech}}, the recommended path uses the [Managed OTLP endpoint](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md), which handles data enrichment server-side. For self-managed {{stack}}, {{ece}} (ECE), and {{eck}} (ECK), data is sent directly to {{es}} using the `elasticsearch` exporter.

## Deploy using the guided onboarding

The guided onboarding simplifies deploying your Kubernetes components by setting up an API key and the needed integrations in the background.

Follow these steps to use the guided onboarding:

1. In {{kib}}, navigate to **Observability** → **Add data**.
2. Select **Kubernetes**, then choose **Kubernetes monitoring with {{agent}}**.
3. Follow the instructions to install the OpenTelemetry Operator using the Helm chart and the provided `values.yaml`.

When installing the OpenTelemetry Operator:

:::::{applies-switch}

::::{applies-item} serverless:
- Make sure the `elastic_otlp_endpoint` shown in the installation command is valid for your {{serverless-full}} project. This is a Managed OTLP endpoint URL, not an {{es}} URL.
- The `elastic_api_key` shown in the installation command corresponds to an API key created by {{kib}} when the onboarding process is initiated.
::::

::::{applies-item} ech:
- Make sure the `elastic_otlp_endpoint` shown in the installation command is valid for your {{ech}} deployment. This is a Managed OTLP endpoint URL, not an {{es}} URL.
- The `elastic_api_key` shown in the installation command corresponds to an API key created by {{kib}} when the onboarding process is initiated.
::::

::::{applies-item} { self:, ece:, eck: }
- Make sure the `elastic_endpoint` shown in the installation command is valid for your environment. If not, replace it with the correct {{es}} endpoint.
- The `elastic_api_key` shown in the installation command corresponds to an API key created by {{kib}} when the onboarding process is initiated.
::::

:::::

:::{note}
The default installation deploys an OpenTelemetry Operator with a self-signed TLS certificate.
To automatically generate and renew certificates, refer to [cert-manager integrated installation](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/customization.md#cert-manager-integrated-installation) for instructions on customizing the `values.yaml` file before running the `helm install` command.
:::

## Manual deployment

Follow these steps for a manual deployment of all components.

### Elastic Stack preparations

Before installing the operator, retrieve your credentials and install the required integrations.

:::::{applies-switch}

::::{applies-item} serverless:
:::{include} ../../_snippets/serverless-endpoint-api.md
:::
::::

::::{applies-item} ech:
:::{include} ../../_snippets/retrieve-credentials-ech-motlp.md
:::
::::

::::{applies-item} { self:, ece:, eck: }
Create an [API Key](/deploy-manage/api-keys/elasticsearch-api-keys.md).
::::

:::::

Install the **[Kubernetes OpenTelemetry Assets](integration-docs://reference/kubernetes_otel.md)** and **[System OpenTelemetry Assets](integration-docs://reference/system_otel.md)** integrations in {{kib}}.

When using the [{{kib}} onboarding UX](#deploy-using-the-guided-onboarding), the previous actions are automatically handled by {{kib}}.

### Operator installation

Follow these steps to install the operator:

1. Create the `opentelemetry-operator-system` Kubernetes namespace:

    ```bash
    kubectl create namespace opentelemetry-operator-system
    ```

Create a secret with your credentials and install the Helm chart for your deployment type:

:::::{applies-switch}

::::{applies-item} serverless:
Replace `<ELASTIC_OTLP_ENDPOINT>` and `<ELASTIC_API_KEY>` in the following command to create a secret with your credentials.

```bash
kubectl create secret generic elastic-secret-otel \
--namespace opentelemetry-operator-system \
--from-literal=elastic_otlp_endpoint='<ELASTIC_OTLP_ENDPOINT>' \
--from-literal=elastic_api_key='<ELASTIC_API_KEY>'
```

Install the OpenTelemetry Operator using the `kube-stack` Helm chart with the `managed_otlp` values file:

```bash subs=true
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update
helm upgrade --install --namespace opentelemetry-operator-system opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
--values 'https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v{{version.edot_collector}}/deploy/helm/edot-collector/kube-stack/managed_otlp/values.yaml' \
--version '{{kube-stack-version}}'
```

For details about the pipelines, refer to [Managed OTLP Endpoint](elastic-agent://reference/edot-collector/config/default-config-k8s.md#managed-otlp-endpoint).
::::

::::{applies-item} ech:
Replace `<ELASTIC_OTLP_ENDPOINT>` and `<ELASTIC_API_KEY>` in the following command to create a secret with your credentials.

```bash
kubectl create secret generic elastic-secret-otel \
--namespace opentelemetry-operator-system \
--from-literal=elastic_otlp_endpoint='<ELASTIC_OTLP_ENDPOINT>' \
--from-literal=elastic_api_key='<ELASTIC_API_KEY>'
```

:::{note}
On Windows PowerShell, replace backslashes (`\`) with backticks (`` ` ``) for line continuation and single quotes (`'`) with double quotes (`"`).
:::

Install the OpenTelemetry Operator using the `kube-stack` Helm chart with the `managed_otlp` values file:

```bash subs=true
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update
helm upgrade --install --namespace opentelemetry-operator-system opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
--values 'https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v{{version.edot_collector}}/deploy/helm/edot-collector/kube-stack/managed_otlp/values.yaml' \
--version '{{kube-stack-version}}'
```

For details about the pipelines, refer to [Managed OTLP Endpoint](elastic-agent://reference/edot-collector/config/default-config-k8s.md#managed-otlp-endpoint).
::::

::::{applies-item} { self:, ece:, eck: }
Create a secret in the new namespace with the following command:

```bash
kubectl create -n opentelemetry-operator-system secret generic elastic-secret-otel \
  --from-literal=elastic_endpoint='YOUR_ELASTICSEARCH_ENDPOINT' \
  --from-literal=elastic_api_key='YOUR_ELASTICSEARCH_API_KEY'
```

Replace:

- `YOUR_ELASTICSEARCH_ENDPOINT`: {{es}} endpoint (**with `https://` prefix**). For example: `https://1234567.us-west2.gcp.elastic-cloud.com:443`.
- `YOUR_ELASTICSEARCH_API_KEY`: {{es}} API Key created in the previous step.

Run the following commands to deploy the `opentelemetry-kube-stack` Helm chart:

```bash subs=true
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update
helm upgrade --install --namespace opentelemetry-operator-system opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
      --values 'https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v{{version.edot_collector}}/deploy/helm/edot-collector/kube-stack/values.yaml' \
      --version {{kube-stack-version}}
```

This configuration includes the `elasticapm` connector and processor, which handle {{product.apm}} trace aggregations locally. When using the Managed OTLP endpoint, this processing happens server-side instead. For details about the pipelines, refer to [Direct ingestion into {{es}}](elastic-agent://reference/edot-collector/config/default-config-k8s.md#direct-ingestion-into-elasticsearch).
::::

:::::

If you need to [customize the configuration](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/customization.md), copy the values file you used and adapt it to your needs. Refer to the [compatibility matrix](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/prerequisites-compatibility.md#compatibility-matrix) for a complete list of available manifests in the `release branches`.

## Verify the installation

Perform the following checks to verify that everything is running properly:

### Check Pods status

Ensure the following components are running without errors:

   - Operator Pod
   - DaemonSet Collector Pod
   - Deployment Collector Pod

### Validate instrumentation object

Confirm that the Instrumentation object is deployed and configured with a valid endpoint.

### Kibana dashboard check

Verify that the **[OTEL][Metrics Kubernetes] Cluster Overview** dashboard in {{kib}} is displaying data correctly.

### Log data availability in Kibana

In **{{kib}} Discover**, confirm the availability of data under the `__logs-*__` data view.

### Metrics data availability in Kibana

In **{{kib}} Discover**, ensure data is available under the `__metrics-*__` data view.
