---
description: Learn how to send Kubernetes logs, metrics, and application traces to Elasticsearch using the OpenTelemetry Operator and Elastic Distributions of OpenTelemetry (EDOT).
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-k8s-otel-edot.html
  - https://www.elastic.co/guide/en/serverless/current/monitor-k8s-otel-edot.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# Quickstart: Unified Kubernetes Observability with Elastic Distributions of OpenTelemetry (EDOT) [monitor-k8s-otel-edot]

In this quickstart guide, you’ll learn how to send {{k8s}} logs, metrics, and application traces to {{es}}, using the [OpenTelemetry Operator](https://github.com/open-telemetry/opentelemetry-operator/) to orchestrate [Elastic Distributions of OpenTelemetry](opentelemetry://reference/index.md) (EDOT) Collectors and SDK instances.

All the components will be deployed through the [opentelemetry-kube-stack](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack) helm chart. They include:

* [OpenTelemetry Operator](https://github.com/open-telemetry/opentelemetry-operator/).
* `DaemonSet` EDOT Collector configured for node level metrics.
* `Deployment` EDOT Collector configured for cluster level metrics.
* `Instrumentation` object for applications [auto-instrumentation](https://opentelemetry.io/docs/kubernetes/operator/automatic/).

For a more detailed description of the components and advanced configuration, refer to [elastic/opentelemetry](opentelemetry://reference/index.md).

## Prerequisites [_prerequisites_2]

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack
:sync: stack

* An {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data. This quickstart is available for all Elastic deployment models. To get started quickly, try out [{{ecloud}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
* A running {{k8s}} cluster (v1.23 or later).
* [Kubectl](https://kubernetes.io/docs/reference/kubectl/).
* [Helm](https://helm.sh/docs/intro/install/).
* (optional) [Cert-manager](https://cert-manager.io/docs/installation/), if you opt for automatic generation and renewal of TLS certificates.

:::{important}
EDOT SDKs are tested and supported only with [EDOT Collector Gateway](elastic-agent://reference/edot-collector/modes.md#edot-collector-as-gateway) or [Managed OTel intake](opentelemetry://reference/motlp.md). Using EDOT SDKs directly with {{apm-server}}'s OTel intake is not supported.
:::

:::

:::{tab-item} {{serverless-short}}
:sync: serverless

* An {{obs-serverless}} project. To learn more, refer to [Create an Observability project](/solutions/observability/get-started.md).
* A running {{k8s}} cluster (v1.23 or later).
* [Kubectl](https://kubernetes.io/docs/reference/kubectl/).
* [Helm](https://helm.sh/docs/intro/install/).
* (optional) [Cert-manager](https://cert-manager.io/docs/installation/), if you opt for automatic generation and renewal of TLS certificates.

:::{important}
EDOT SDKs are tested and supported only with [EDOT Collector Gateway](elastic-agent://reference/edot-collector/modes.md#edot-collector-as-gateway) or [Managed OTel intake](opentelemetry://reference/motlp.md). Using EDOT SDKs directly with {{apm-server}}'s OTel intake is not supported.
:::

:::

::::

## Collect your data [_collect_your_data_2]

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack
:sync: stack

1. In {{kib}}, go to the **Observability** UI and click **Add Data**.
2. Under **What do you want to monitor?** select **Kubernetes**, and then select **OpenTelemetry: Full Observability**.

    :::{image} /solutions/images/observability-quickstart-k8s-otel-entry-point.png
    :alt: Kubernetes-OTel entry point
    :screenshot:
    :::

3. Follow the on-screen instructions to install all needed components.

    ::::{note}
    The default installation deploys the OpenTelemetry Operator with a self-signed TLS certificate valid for 365 days. This certificate **won’t be renewed** unless the Helm Chart release is manually updated. Refer to the [cert-manager integrated installation](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/customization.md#cert-manager-integrated-installation) guide to enable automatic certificate generation and renewal using [cert-manager](https://cert-manager.io/docs/installation/).

    ::::


    Deploy the OpenTelemetry Operator and EDOT Collectors using the kube-stack Helm chart with the provided `values.yaml` file. You will run a few commands to:

    * Add the helm chart repository needed for the installation.
    * Create a namespace.
    * Create a secret with an API Key and the {{es}} endpoint to be used by the collectors.
    * Install the `opentelemetry-kube-stack` helm chart with the provided `values.yaml`.
    * Optionally, for instrumenting applications, apply the corresponding `annotations` as shown in {{kib}}.

:::

:::{tab-item} {{serverless-short}}
:sync: serverless

1. [Create a new {{obs-serverless}} project](/solutions/observability/get-started.md), or open an existing one.
2. In your {{obs-serverless}} project, go to **Add Data**.
3. Under **What do you want to monitor?** select **Kubernetes**, and then select **OpenTelemetry: Full Observability**.

    :::{image} /solutions/images/serverless-quickstart-k8s-otel-entry-point.png
    :alt: Kubernetes-OTel entry point
    :screenshot:
    :::

4. Follow the on-screen instructions to install all needed components.

    ::::{note}
    The default installation deploys the OpenTelemetry Operator with a self-signed TLS certificate valid for 365 days. This certificate **won’t be renewed** unless the Helm Chart release is manually updated. Refer to the [cert-manager integrated installation](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/customization.md#cert-manager-integrated-installation) guide to enable automatic certificate generation and renewal using [cert-manager](https://cert-manager.io/docs/installation/).

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

:::{image} /solutions/images/observability-quickstart-k8s-otel-dashboard.png
:alt: Kubernetes overview dashboard
:screenshot:
:::

### Work with Kubernetes logs

You can search and analyze Kubernetes logs using Elastic’s Discover capability. Find **Discover** in the main menu or use the global search field.

:::{image} /solutions/images/screenshot-observability-monitoring-k8s-kubernetes-logs-can-be-searched.png
:alt: Kubernetes logs in Discover
:screenshot:
:::

### Visualize Kubernetes metrics

Kubernetes out-of-the-box dashboards allow you to analyze Kubernetes metrics within Kibana. Go to **Dashboards** → **Analytics** and search for **Kubernetes**. The **Kubernetes Overview** dashboard shows metrics for the entire Kubernetes Cluster. All the nodes, pods, and CPU and memory usage.

:::{image} /solutions/images/screenshot-observability-monitoring-k8s-kubernetes-overview-cluster.png
:alt: Kubernetes overview dashboard
:screenshot:
:::

Kibana allows you to analyze logs with interactive dashboards to derive insights, automate workflows, find anomalies and trends, and more. When you select **Dashboards** → **Analytics**, you can select **Create dashboard** and customize your new dashboard to your needs.

### Set up alerts

Select **Alerts** and then **Create rules**. This allows you to get notifications when various events happen, for example when latency is anomalous, metric aggregation exceeds threshold, and so on. Notifications are sent through email, Jira, Slack, and more.

### Use machine learning to uncover insights

Find **Machine Learning** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Then select **Anomaly Detection** → **Jobs** to create a machine learning job. By setting up machine learning jobs, for example, rather than having an alert when a specific percentage of memory usage has occurred, you can know when the usage is unusual.

:::{image} /solutions/images/screenshot-observability-monitoring-k8s-leverage-machine-learning-to-uncover-insights.png
:alt: Machine learning job
:screenshot:
:::

## Troubleshooting and more [_troubleshooting_and_more]

* To troubleshoot deployment and installation, refer to [installation verification](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/deployment.md#verify-the-installation).
* For application instrumentation details, refer to [Instrumenting applications with EDOT SDKs on Kubernetes](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/instrumenting-applications.md).
* To customize the configuration, refer to [custom configuration](/solutions/observability/get-started/opentelemetry/use-cases/kubernetes/customization.md).
* Refer to [Observability overview](/solutions/observability.md) for a description of other useful features.