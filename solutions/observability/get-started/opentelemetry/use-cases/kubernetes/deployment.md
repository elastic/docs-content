---
navigation_title: Deployment
description: Instructions for deploying EDOT components for Kubernetes monitoring, using guided onboarding or manual steps.
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

# Deployment

You can use the [guided onboarding](#deploy-using-the-guided-onboarding) or [deploy all components manually](#manual-deployment)

## Deploy using the guided onboarding

The guided onboarding simplifies deploying your Kubernetes components by setting up an [API Key](/deploy-manage/api-keys/elasticsearch-api-keys.md) and the needed [Integrations](integration-docs://reference/index.md) in the background.

Follow these steps to use the guided onboarding:

1. In {{kib}}, navigate to **Observability** → **Add data**.
2. Select **Kubernetes**, then choose **Kubernetes monitoring with EDOT Collector**.
3. Follow the instructions to install the OpenTelemetry Operator using the Helm chart and the provided `values.yaml`.

When installing the OpenTelemetry Operator:

- Make sure the `elastic_endpoint` shown in the installation command is valid for your environment. If not, replace it with the correct {{es}} endpoint.
- The `elastic_api_key` shown in the installation command corresponds to an API key created by {{kib}} when the onboarding process is initiated.

:::{note}
The default installation deploys an OpenTelemetry Operator with a self-signed TLS certificate.
To automatically generate and renew certificates, refer to [cert-manager integrated installation](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/customization.md#cert-manager-integrated-installation) for instructions on customizing the `values.yaml` file before running the `helm install` command.
:::

## Manual deployment

Follow these steps for a manual deployment of all components.

### Elastic Stack preparations

Before installing the operator do the following:

1. Create an [API Key](/deploy-manage/api-keys/elasticsearch-api-keys.md).

2. Install the following integrations in {{kib}}:
    - `System`
    - `Kubernetes`
    - `Kubernetes OpenTelemetry Assets`

When using the [{{kib}} onboarding UX](#deploy-using-the-guided-onboarding), the previous actions are automatically handled by {{kib}}.

### Operator installation

Follow these steps to install the operator:

1. Create the `opentelemetry-operator-system` Kubernetes namespace:

    ```bash
    $ kubectl create namespace opentelemetry-operator-system
    ```

2. Create a secret in the new namespace with the following command:

   ```bash
   kubectl create -n opentelemetry-operator-system secret generic elastic-secret-otel \
     --from-literal=elastic_endpoint='YOUR_ELASTICSEARCH_ENDPOINT' \
     --from-literal=elastic_api_key='YOUR_ELASTICSEARCH_API_KEY'
   ```

   Don't forget to replace:

   - `YOUR_ELASTICSEARCH_ENDPOINT`: {{es}} endpoint (**with `https://` prefix**). For example: `https://1234567.us-west2.gcp.elastic-cloud.com:443`.
   - `YOUR_ELASTICSEARCH_API_KEY`: {{es}} API Key created in the previous step.

3. If you need to [customize the configuration](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/customization.md), copy the `values.yaml` file and adapt it to your needs. Refer to the [compatibility matrix](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/prerequisites-compatibility.md#compatibility-matrix) for a complete list of available manifests in the `release branches`. 

4. Run the following commands to deploy the `opentelemetry-kube-stack` Helm chart, using the appropriate values file:

    ```bash subs=true
    helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
    helm repo update
    helm upgrade --install --namespace opentelemetry-operator-system opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack \
          --values 'https://raw.githubusercontent.com/elastic/elastic-agent/refs/tags/v{{version.edot_collector}}/deploy/helm/edot-collector/kube-stack/values.yaml' \
          --version {{kube-stack-version}}
    ```

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
