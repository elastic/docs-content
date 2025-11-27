---
description: Learn how to monitor your Kubernetes cluster infrastructure with minimal configuration using Elastic Agent and kubectl commands.
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-quickstarts-k8s-logs-metrics.html
  - https://www.elastic.co/guide/en/observability/current/monitor-k8s-logs-metrics-with-elastic-agent.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-serverless
  - id: observability
---

# Quickstart: Monitor your Kubernetes cluster with {{agent}} [monitor-k8s-logs-metrics-with-elastic-agent]

In this quickstart guide, you'll learn how to create the Kubernetes resources required to monitor your cluster infrastructure by using a single command to download, install, and configure {{agent}} in your Kubernetes cluster.

:::{tip}
We recommend using the [Elastic Distribution of OpenTelemetry (EDOT) Collector](/solutions/observability/get-started/quickstart-unified-kubernetes-observability-with-elastic-distributions-of-opentelemetry-edot.md) as the preferred way to collect Kubernetes logs, metrics, and application traces using OpenTelemetry.
:::

:::{note}
In {{stack}} versions 9.0 and 9.1, the quickstart uses [Kubectl](https://kubernetes.io/docs/reference/kubectl/) to install {{agent}} in a Kubernetes cluster. However, these versions also support using [Helm](https://helm.sh/docs/) charts, which is now the preferred method for installing {{agent}} on Kubernetes. If your cluster is on version 9.0 or 9.1, we recommend that you follow the [Install Elastic Agent on Kubernetes using Helm](/reference/fleet/install-on-kubernetes-using-helm.md) guide to deploy {{agent}}.
:::

## Prerequisites [_prerequisites_2]

:::::{tab-set}
:group: stack-serverless

::::{tab-item} {{serverless-short}}
:sync: serverless

* An {{obs-serverless}} project. To learn more, refer to [Create an Observability project](/solutions/observability/get-started.md).
* A user with the **Admin** role or higher (required to onboard system logs and metrics). To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).
* A running Kubernetes cluster with internet access
* [Helm](https://helm.sh/docs/)
::::

::::{tab-item} {{stack}} 9.2 and later
:sync: stack-9.2

* A running {{stack}} deployment, either self-managed or orchestrated by platforms like {{ech}}, {{ece}}, or {{eck}}, with internet access. To get started quickly, try out [{{ecloud}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
* A user with the `superuser` [built-in role](elasticsearch://reference/elasticsearch/roles.md) or the privileges required to onboard data.

:::{dropdown} Expand to view required privileges
* [**Cluster**](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster): `['monitor', 'manage_own_api_key']`
* [**Index**](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices): `{ names: ['logs-*-*', 'metrics-*-*'], privileges: ['auto_configure', 'create_doc'] }`
* [**Kibana**](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md): `{ spaces: ['*'], feature: { fleet: ['all'], fleetv2: ['all'] } }`
:::

* A running Kubernetes cluster with internet access
* [Helm](https://helm.sh/docs/)
::::

::::{tab-item} {{stack}} 9.0-9.1
:sync: stack-9.0-9.1

* A running {{stack}} deployment, either self-managed or orchestrated by platforms like {{ech}}, {{ece}}, or {{eck}}, with internet access. To get started quickly, try out [{{ecloud}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
* A user with the `superuser` [built-in role](elasticsearch://reference/elasticsearch/roles.md) or the privileges required to onboard data.

:::{dropdown} Expand to view required privileges
* [**Cluster**](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster): `['monitor', 'manage_own_api_key']`
* [**Index**](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices): `{ names: ['logs-*-*', 'metrics-*-*'], privileges: ['auto_configure', 'create_doc'] }`
* [**Kibana**](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md): `{ spaces: ['*'], feature: { fleet: ['all'], fleetv2: ['all'] } }`
:::

* A running Kubernetes cluster with internet access
* [Kubectl](https://kubernetes.io/docs/reference/kubectl/)
::::

:::::

## Limitations [monitor-k8s-with-agent-limitations]

The installation command provided by the UI during the quickstart cannot be used as-is to install {{agent}} in an air-gapped environment. For an air-gapped environment with a self-managed {{stack}} deployment or orchestrator such as [{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md), refer to the following resources:

- [Install Elastic Agent air-gapped](/deploy-manage/deploy/self-managed/air-gapped-install.md#air-gapped-elastic-agent)
- [Install Elastic Agent on Kubernetes using Helm](/reference/fleet/install-on-kubernetes-using-helm.md)
- [Deploy Elastic Agent in standalone mode with ECK](/deploy-manage/deploy/cloud-on-k8s/standalone-elastic-agent.md)
- [Run Elastic Agent in an air-gapped environment](/reference/fleet/air-gapped.md)

## Collect your data [_collect_your_data_2]

:::::{tab-set}
:group: stack-serverless

::::{tab-item} {{serverless-short}}
:sync: serverless

1. Go to your [{{obs-serverless}}](/solutions/observability/get-started.md) project, then go to **Add data**.
2. In the **What do you want to monitor?** section, select **Kubernetes**, and then select **Elastic Agent: Logs & Metrics**.
3. To install {{agent}} on your host, copy and run the install command.

    By running this command, you use the Helm package manager to install and configure an instance of the {{agent}} Helm chart with additional deployment-specific data such as the API key generated by {{kib}} for the acting user.

    The Helm chart also includes a default installation of [`kube-state-metrics` (KSM)](https://github.com/kubernetes/kube-state-metrics), which is required by the Kubernetes integration to collect cluster-level metrics.

    If you encounter an error during the installation, refer to [Troubleshooting](#monitor-k8s-with-agent-troubleshooting).

    :::{dropdown} Details about the install command
    The install command provided by the UI may be similar to:

    ```sh subs=true
    helm repo add elastic https://helm.elastic.co/ && helm install elastic-agent elastic/elastic-agent --version {{version.stack}} -n kube-system --set outputs.default.url=https:<elasticsearch-url>:443 --set kubernetes.onboardingID=<internal-id> --set kubernetes.enabled=true --set outputs.default.type=ESPlainAuthAPI --set outputs.default.api_key=$(echo "<api-key>" | base64 -d)
    ```

    Where:

    - `elastic-agent` is the name of the specific installation of the Helm chart, known as **release name**.
    - `elastic/elastic-agent` defines the name of the chart to install, using the format `<repository>/<chart-name>`.
    - {{version.stack}} is the version of the {{agent}} Helm chart to be installed.
    - `kube-system` is the namespace where {{agent}} is to be installed.
    - `--set` parameters add configuration values specific to the serverless project, the acting user, and the deployment method of the Helm chart.

       Refer to [Install standalone Elastic Agent on Kubernetes using Helm](/reference/fleet/example-kubernetes-standalone-agent-helm.md#agent-standalone-helm-example-install) for a more detailed explanation of the configuration options used.
    :::

4. Go back to the **Kubernetes: Logs & Metrics** page in {{kib}}.

    There might be a slight delay before data is ingested. When ready, you will see the message **We are monitoring your cluster**.

5. Click **Explore Kubernetes cluster** to navigate to dashboards and explore your data.

::::

::::{tab-item} {{stack}} 9.2 and later
:sync: stack-9.2

1. In {{kib}}, go to the **Observability** overview page, and click **Add Data**.
2. In the **What do you want to monitor?** section, select **Kubernetes**, and then select **Elastic Agent: Logs & Metrics**.
3. To install {{agent}} on your host, copy and run the install command.

    By running this command, you use the Helm package manager to install and configure an instance of the {{agent}} Helm chart with additional deployment-specific data such as the API key generated by {{kib}} for the acting user.

    The Helm chart also includes a default installation of [`kube-state-metrics` (KSM)](https://github.com/kubernetes/kube-state-metrics), which is required by the Kubernetes integration to collect cluster-level metrics.

    If you encounter an error during the installation, refer to [Troubleshooting](#monitor-k8s-with-agent-troubleshooting).

    :::{dropdown} Details about the install command
    The install command provided by the UI may be similar to:

    ```sh subs=true
    helm repo add elastic https://helm.elastic.co/ && helm install elastic-agent elastic/elastic-agent --version {{version.stack}} -n kube-system --set outputs.default.url=https:<elasticsearch-url>:443 --set kubernetes.onboardingID=<internal-id> --set kubernetes.enabled=true --set outputs.default.type=ESPlainAuthAPI --set outputs.default.api_key=$(echo "<api-key>" | base64 -d)
    ```

    Where:

    - `elastic-agent` is the name of the specific installation of the Helm chart, known as **release name**.
    - `elastic/elastic-agent` defines the name of the chart to install, using the format `<repository>/<chart-name>`.
    - {{version.stack}} is the version of the {{agent}} Helm chart to be installed.
    - `kube-system` is the namespace where {{agent}} is to be installed.
    - `--set` parameters add configuration values specific to the serverless project, the acting user, and the deployment method of the Helm chart.

       Refer to [Install standalone Elastic Agent on Kubernetes using Helm](/reference/fleet/example-kubernetes-standalone-agent-helm.md#agent-standalone-helm-example-install) for a more detailed explanation of the configuration options used.
    :::

4. Go back to the **Kubernetes: Logs & Metrics** page in {{kib}}.

    There might be a slight delay before data is ingested. When ready, you will see the message **We are monitoring your cluster**.

5. Click **Explore Kubernetes cluster** to navigate to dashboards and explore your data.

::::

::::{tab-item} {{stack}} 9.0-9.1
:sync: stack-9.0-9.1

1. In {{kib}}, go to the **Observability** UI and click **Add Data**.
2. In the **What do you want to monitor?** section, select **Kubernetes**, and then select **Elastic Agent: Logs & Metrics**.

3. To install {{agent}} on your host, copy and run the install command.

    By running this command, you use `kubectl kustomize` to download a manifest file, inject deployment-specific data such as the API key generated by {{kib}} for the acting user, and create the Kubernetes resources for {{agent}}.

4. Go back to the **Kubernetes: Logs & Metrics** page in {{kib}}.

    There might be a slight delay before data is ingested. When ready, you will see the message **We are monitoring your cluster**.

5. Click **Explore Kubernetes cluster** to navigate to dashboards and explore your data.

::::

:::::

## Visualize your data [_visualize_your_data_2]

After installation is complete and all relevant data is flowing into Elastic, the **Visualize your data** section allows you to access the Kubernetes Cluster Overview dashboard that can be used to monitor the health of the cluster.

:::{image} /solutions/images/observability-quickstart-k8s-overview.png
:alt: Kubernetes overview dashboard
:screenshot:
:::

Furthermore, you can access other useful prebuilt dashboards for monitoring Kubernetes resources, for example running pods per namespace, as well as the resources they consume, like CPU and memory.

Refer to [Observability overview](/solutions/observability.md) for a description of other useful features.

## Uninstall {{agent}} from the Kubernetes cluster [monitor-k8s-with-agent-delete-agent]

::::{tab-set}
:group: stack-serverless

:::{tab-item} {{serverless-short}}
:sync: serverless

To uninstall {{agent}} and the Kubernetes resources installed with Helm, run:

```sh
helm uninstall <release-name> -n <namespace> <1>
```
1. Substitute `<release-name>` with the release name and `<namespace>` with the namespace used in the quickstart command described in the [Collect your data](#_collect_your_data_2) section.

If you used the default values from the quickstart, the command would be:

```sh
helm uninstall elastic-agent -n kube-system
```
:::

:::{tab-item} {{stack}} 9.2 and later
:sync: stack-9.2

To uninstall {{agent}} and the Kubernetes resources installed with Helm, run:

```sh
helm uninstall <release-name> -n <namespace> <1>
```
1. Substitute `<release-name>` with the release name and `<namespace>` with the namespace used in the quickstart command described in the [Collect your data](#_collect_your_data_2) section.

If you used the default values from the quickstart, the command would be:

```sh
helm uninstall elastic-agent -n kube-system
```
:::

:::{tab-item} {{stack}} 9.0-9.1
:sync: stack-9.0-9.1

To uninstall {{agent}} and the Kubernetes resources installed with `kubectl`:

1. Copy the `kubectl` quickstart command for installing {{agent}} described in the [Collect your data](#_collect_your_data_2) section.
2. Replace `| kubectl apply -f-` with `| kubectl delete -f-`, then run the command.
:::

::::

## Troubleshooting [monitor-k8s-with-agent-troubleshooting]

### `kube-state-metrics` is already installed

If you're using `helm` to install {{agent}} in your Kubernetes cluster, you may encounter an error if `kube-state-metrics` is already installed in the same namespace where {{agent}} is to be installed. In this case, add the option `--set kube-state-metrics.enabled=false` to the install command provided by the UI to skip the installation of `kube-state-metrics`.

### The `elastic` repository already exists

If you're using `helm` to install {{agent}} in your Kubernetes cluster and the `elastic` repository is already configured on your host, replace the `helm repo add elastic https://helm.elastic.co/ ` part of the command provided by the UI with `helm repo update elastic` to ensure the repository is updated with the latest package information.