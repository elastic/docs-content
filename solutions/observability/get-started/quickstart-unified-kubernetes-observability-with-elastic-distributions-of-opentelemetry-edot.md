---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/monitor-k8s-otel-edot.html
  - https://www.elastic.co/guide/en/serverless/current/monitor-k8s-otel-edot.html
---

# Quickstart: Unified Kubernetes Observability with Elastic Distributions of OpenTelemetry (EDOT) [monitor-k8s-otel-edot]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


In this quickstart guide, you’ll learn how to send Kubernetes logs, metrics, and application traces to Elasticsearch, using the [OpenTelemetry Operator](https://github.com/open-telemetry/opentelemetry-operator/) to orchestrate [Elastic Distributions of OpenTelemetry](https://github.com/elastic/opentelemetry/tree/main) (EDOT) Collectors and SDK instances.

All the components will be deployed through the [opentelemetry-kube-stack](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack) helm chart. They include:

* [OpenTelemetry Operator](https://github.com/open-telemetry/opentelemetry-operator/).
* `DaemonSet` EDOT Collector configured for node level metrics.
* `Deployment` EDOT Collector configured for cluster level metrics.
* `Instrumentation` object for applications [auto-instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic/).

For a more detailed description of the components and advanced configuration, refer to the [elastic/opentelemetry](https://github.com/elastic/opentelemetry/blob/main/docs/kubernetes/operator/README.md) GitHub repository.


## Prerequisites [_prerequisites_2]

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack v9
:sync: stack

* An {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data. This quickstart is available for all Elastic deployment models. To get started quickly, try out our hosted {{ess}} on [{{ecloud}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
* A running Kubernetes cluster (v1.23 or newer).
* [Kubectl](https://kubernetes.io/docs/reference/kubectl/).
* [Helm](https://helm.sh/docs/intro/install/).
* (optional) [Cert-manager](https://cert-manager.io/docs/installation/), if you opt for automatic generation and renewal of TLS certificates.

:::

:::{tab-item} Serverless
:sync: serverless

* An {{obs-serverless}} project. To learn more, refer to [Create an Observability project](../../../solutions/observability/get-started/create-an-observability-project.md).
* A running Kubernetes cluster (v1.23 or newer).
* [Kubectl](https://kubernetes.io/docs/reference/kubectl/).
* [Helm](https://helm.sh/docs/intro/install/).
* (optional) [Cert-manager](https://cert-manager.io/docs/installation/), if you opt for automatic generation and renewal of TLS certificates.

:::

::::

## Collect your data [_collect_your_data_2]

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack v9
:sync: stack

1. In {{kib}}, go to the **Observability** UI and click **Add Data**.
2. Under **What do you want to monitor?** select **Kubernetes**, and then select **OpenTelemetry: Full Observability**.

    :::{image} ../../../images/observability-quickstart-k8s-otel-entry-point.png
    :alt: Kubernetes-OTel entry point
    :class: screenshot
    :::

3. Follow the on-screen instructions to install all needed components.

    ::::{note}
    The default installation deploys the OpenTelemetry Operator with a self-signed TLS certificate valid for 365 days. This certificate **won’t be renewed** unless the Helm Chart release is manually updated. Refer to the [cert-manager integrated installation](https://github.com/elastic/opentelemetry/blob/main/docs/kubernetes/operator/README.md#cert-manager) guide to enable automatic certificate generation and renewal using [cert-manager](https://cert-manager.io/docs/installation/).

    ::::


    Deploy the OpenTelemetry Operator and EDOT Collectors using the kube-stack Helm chart with the provided `values.yaml` file. You will run a few commands to:

    * Add the helm chart repository needed for the installation.
    * Create a namespace.
    * Create a secret with an API Key and the {{es}} endpoint to be used by the collectors.
    * Install the `opentelemetry-kube-stack` helm chart with the provided `values.yaml`.
    * Optionally, for instrumenting applications, apply the corresponding `annotations` as shown in {{kib}}.

:::

:::{tab-item} Serverless
:sync: serverless

1. [Create a new {{obs-serverless}} project](../../../solutions/observability/get-started/create-an-observability-project.md), or open an existing one.
2. In your {{obs-serverless}} project, go to **Add Data**.
3. Under **What do you want to monitor?** select **Kubernetes**, and then select **OpenTelemetry: Full Observability**.

    :::{image} ../../../images/serverless-quickstart-k8s-otel-entry-point.png
    :alt: Kubernetes-OTel entry point
    :class: screenshot
    :::

4. Follow the on-screen instructions to install all needed components.

    ::::{note}
    The default installation deploys the OpenTelemetry Operator with a self-signed TLS certificate valid for 365 days. This certificate **won’t be renewed** unless the Helm Chart release is manually updated. Refer to the [cert-manager integrated installation](https://github.com/elastic/opentelemetry/blob/main/docs/kubernetes/operator/README.md#cert-manager) guide to enable automatic certificate generation and renewal using [cert-manager](https://cert-manager.io/docs/installation/).

    ::::


    Deploy the OpenTelemetry Operator and EDOT Collectors using the kube-stack Helm chart with the provided `values.yaml` file. You will run a few commands to:

    * Add the helm chart repository needed for the installation.
    * Create a namespace.
    * Create a secret with an API Key and the {{es}} endpoint to be used by the collectors.
    * Install the `opentelemetry-kube-stack` helm chart with the provided `values.yaml`.
    * Optionally, for instrumenting applications, apply the corresponding `annotations` as shown in {{kib}}.


:::

::::



## Visualize your data [_visualize_your_data]

After installation is complete and all relevant data is flowing into Elastic, the **Visualize your data** section provides a link to the **[OTEL][Metrics Kubernetes]Cluster Overview** dashboard used to monitor the health of the cluster.

:::{image} ../../../images/observability-quickstart-k8s-otel-dashboard.png
:alt: Kubernetes overview dashboard
:class: screenshot
:::


## Troubleshooting and more [_troubleshooting_and_more]

* To troubleshoot deployment and installation, refer to [installation verification](https://github.com/elastic/opentelemetry/tree/main/docs/kubernetes/operator#installation-verification).
* For application instrumentation details, refer to [Instrumenting applications with EDOT SDKs on Kubernetes](https://github.com/elastic/opentelemetry/blob/main/docs/kubernetes/operator/instrumenting-applications.md).
* To customize the configuration, refer to [custom configuration](https://github.com/elastic/opentelemetry/tree/main/docs/kubernetes/operator#custom-configuration).
* Refer to [Observability overview](../../../solutions/observability/get-started/what-is-elastic-observability.md) for a description of other useful features.