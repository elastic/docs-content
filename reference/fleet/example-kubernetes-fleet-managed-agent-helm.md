---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/example-kubernetes-fleet-managed-agent-helm.html
---

# Example: Install Fleet-managed Elastic Agent on Kubernetes using Helm [example-kubernetes-fleet-managed-agent-helm]

This example demonstrates how to install a {{fleet}}-managed {{agent}} on a {{k8s}} system using a Helm chart, collect {{k8s}} metrics and logs using the [Kubernetes Integration](integration-docs://reference/kubernetes/index.md), and send the data to an {{es}} cluster in {{ecloud}} for visualization in {{kib}}.

For an overview of the {{agent}} Helm chart and its benefits, refer to [Install {{agent}} on Kubernetes using Helm](/reference/fleet/install-on-kubernetes-using-helm.md).

::::{note}
This guide deploys a single set of {{agent}} DaemonSet pods to collect all metrics, which works well for small to medium-sized {{k8s}} clusters. 

For larger clusters, or when kube-state-metrics (KSM) metrics collection becomes a performance bottleneck, we recommend a more scalable architecture: move the KSM metric collection to a separate set of agents deployed as sidecars alongside KSM, with autosharding enabled.

This can be easily implemented with the Helm chart. For details, refer to the [KSM autosharding example](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent/examples/fleet-managed-ksm-sharding).
::::

This guide takes you through these steps:

* [Add the Elastic Helm repository](#preparations)
* [Install {{agent}}](#agent-fleet-managed-helm-example-install-agent)
* [Install the Kubernetes integration](#agent-fleet-managed-helm-example-install-integration)
* [Tidy up](#agent-fleet-managed-helm-example-tidy-up)

## Prerequisites [agent-fleet-managed-helm-example-prereqs]

To get started, you need:

* A local install of the [Helm](https://helm.sh/) {{k8s}} package manager.
* An [{{ech}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body) {{es}} cluster on version 8.18 or higher, with an [Integrations Server](/deploy-manage/deploy/elastic-cloud/ec-customize-deployment-components.md#ec_integrations_server) component included.
* An active {{k8s}} cluster.

## Installation overview

The installation and configuration steps shown in this example deploys the following components to monitor your Kubernetes cluster:

* {{agent}}, deployed as a `DaemonSet`, connected to {{fleet}}, and configured to collect:
    * Host level metrics and logs through the [System Integration](integration-docs://reference/system/index.md). This enables the monitoring of Kubernetes nodes at OS level.
    * Kubernetes node and cluster-level metrics and logs through the [Kubernetes Integration](integration-docs://reference/kubernetes/index.md). For cluster-level metrics collection, one of the agents will act as a [leader](./kubernetes_leaderelection-provider.md).
* A default installation of `kube-state-metrics` (KSM), configured as a dependency of the chart. KSM is required by the Kubernetes integration to collect cluster-level metrics.

By default, all resources are installed in the namespace defined by your current `kubectl` context. You can override this by specifying a different namespace using the `--namespace` option during installation.

% we will uncomment the next line when the use cases are documented in the landing page :)
% For other architectures and use cases, refer to [Advanced use cases](./install-on-kubernetes-using-helm.md#advanced-use-cases).

## Add the Elastic Helm repository [preparations]

Before installing, add the Elastic Helm repository and verify the available versions of the `elastic-agent` chart. If the repository is already configured, run `helm repo update` to ensure you have the latest package information.

1. Set up Helm repository:

    ```sh
    helm repo add elastic https://helm.elastic.co/
    helm repo update
    ```

2. Verify chart versions:

    ```sh
    helm search repo elastic-agent --versions
    ```

    The previous command returns something similar to:

    ```sh
    NAME                 	CHART VERSION	APP VERSION	DESCRIPTION
    elastic/elastic-agent	9.0.0        	9.0.0      	Elastic-Agent Helm Chart
    elastic/elastic-agent	8.18.0       	8.18.0     	Elastic-Agent Helm Chart
    ```

## Install {{agent}} [agent-fleet-managed-helm-example-install-agent]

1. Open your {{ecloud}} deployment, and from the navigation menu select **Fleet**.
2. From the **Agents** tab, select **Add agent**.
3. In the **Add agent** UI, specify a policy name and select **Create policy**. Leave the **Collect system logs and metrics** option selected.
4. Scroll down in the **Add agent** flyout to the **Install Elastic Agent on your host** section.
5. Select the **Linux TAR** tab and copy the values for `url` and `enrollment-token`. You’ll use these when you run the `helm install` command.
6. Open a terminal shell on your local system where the Helm tool is installed and you have access to the {{k8s}} cluster.
7. Copy and prepare the command to install the chart:

    ```sh
    helm install demo elastic/elastic-agent \
    --set agent.fleet.enabled=true \
    --set system.enabled=true \
    --set agent.fleet.url=<Fleet-URL> \ # Substitute Fleet-URL with the URL that you copied earlier
    --set agent.fleet.token=<Fleet-token> \ # Substitute Fleet-token with the enrollment token that you copied earlier.
    --set agent.fleet.preset=perNode
    ```

    Note that the command has these properties:

    * `helm install`: Runs the Helm CLI install tool. Use `helm upgrade` to modify or update an existing release.
    * `demo`: The name for this specific installation of the chart, known as the **release name**. You can choose any name you like.
    * `elastic/elastic-agent`: The name of the chart to install, using the format `<repository>/<chart-name>`.
    * `--set agent.fleet.enabled=true`: Enables {{fleet}}-managed {{agent}}, which is disabled (`false`) by default.
    * `--set system.enabled=true`: Adds the required volumes and mounts to enable host monitoring through the System integration.
    * `--set agent.fleet.url=<Fleet-URL>`: Specifies the address where {{agent}} connects to {{fleet}} Server in your {{ecloud}} deployment.
    * `--set agent.fleet.token=<Fleet-token>`: Sets the enrollment token that {{agent}} uses to authenticate with {{fleet}} Server.
    * `--set agent.fleet.preset=perNode`: Runs the agent as a `DaemonSet`, to collect node-level metrics and logs. Refer to [](install-on-kubernetes-using-helm.md) for more details and use cases for this parameter.

    After your updates, the command should be similar to:

    ```sh
    helm install demo elastic/elastic-agent \
    --set agent.fleet.enabled=true \
    --set system.enabled=true \
    --set agent.fleet.url=https://256575858845283fxxxxxxxd5265d2b4.fleet.us-central1.gcp.foundit.no:443 \
    --set agent.fleet.token=eSVvFDUvSUNPFldFdhhZNFwvS5xxxxxxxxxxxxFEWB1eFF1YedUQ1NWFXwr== \
    --set agent.fleet.preset=perNode
    ```

    ::::{tip}
    For a full list of all available values settings and descriptions, refer to the [{{agent}} Helm Chart Readme](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent) and default [values.yaml](https://github.com/elastic/elastic-agent/blob/main/deploy/helm/elastic-agent/values.yaml).

    The following options could be useful for special use cases:
    * `--namespace <namespace>`: Allows to install all resources in a specific namespace.
    * `--version <version>`: Installs a specific version of the Helm chart and {{agent}}. Refer to [Preparations](#preparations) to check available versions.
    * `--set agent.version=<version>`: Installs a specific version of {{agent}}. By default, the chart installs the agent version that matches its own.
    * `--set-file agent.fleet.ca.value=/local-path/to/fleet-ca.crt`: Provides the CA certificate used by the {{fleet}} Server. This is typically needed when the server uses a certificate signed by a private CA. Not required for {{fleet}} Servers running on {{ecloud}}.
    * `--set agent.fleet.insecure=true`: Use this option to skip the {{fleet}} certificate verification if your {{fleet}} Server uses a self-signed certificate, such as when installed in quickstart mode. Not required for {{fleet}} Servers running on {{ecloud}}. Note that this option is not recommended for production environments.
    * `--set kube-state-metrics.enabled=false`: In case you already have KSM installed in your cluster, and you don't want to install a second instance.
    * `--set kube-state-metrics.fullnameOverride=ksm`: If you want to deploy KSM with a different release name (it defaults to `kube-state-metrics`). This can be useful if you have already a default installation of KSM and you want a second one.
    ::::

9. Run the command.

    The command output should confirm that {{agent}} has been installed:

    ```sh
    ...
    Installed agent:
      - perNode [daemonset - managed mode]
    ...
    ```

10. Run the `kubectl get pods -n default` command to confirm that the {{agent}} pod is running:

    ```sh
    NAME                       READY   STATUS    RESTARTS      AGE
    agent-pernode-demo-86mst   1/1     Running   0          12s
    ```

11. In the **Add agent** flyout, wait a minute or so for confirmation that {{agent}} has successfully enrolled with {{fleet}} and that data is flowing:

    :::{image} images/helm-example-nodes-enrollment-confirmation.png
    :alt: Screen capture of Add Agent UI showing that the agent has enrolled in Fleet
    :screenshot:
    :::

12. In {{fleet}}, open the **Agents** tab and see that an **Agent-pernode-demo-#** agent is running.
13. Select the agent to view its details.
14. On the **Agent details** tab, on the **Integrations** pane, expand `system-1` to confirm that logs and metrics are incoming. You can click either the `Logs` or `Metrics` link to view details.

    :::{image} images/helm-example-nodes-logs-and-metrics.png
    :alt: Screen capture of the Logs and Metrics view on the Integrations pane
    :screenshot:
    :::

## Install the Kubernetes integration [agent-fleet-managed-helm-example-install-integration]

Now that you’ve {{agent}} and data is flowing, you can set up the {{k8s}} integration.

1. In your {{ecloud}} deployment, from the {{kib}} menu open the **Integrations** page.
2. Run a search for `Kubernetes` and then select the {{k8s}} integration card.
3. On the {{k8s}} integration page, click **Add Kubernetes** to add the integration to your {{agent}} policy.
4. Scroll to the bottom of **Add Kubernetes integration** page. Under **Where to add this integration?** select the **Existing hosts** tab. On the **Agent policies** menu, select the agent policy that you created previously in the [Install {{agent}}](#agent-fleet-managed-helm-example-install-agent) steps.

    You can leave all of the other integration settings at their default values. For details about the available inputs and data sets, refer to the [Kubernetes Integration](integration-docs://reference/kubernetes/index.md) documentation.

    ::::{important}
    All inputs under the **Collect Kubernetes metrics from kube-state-metrics** section default to `kube-state-metrics:8080` as the destination host. This works if you deployed KSM (kube-state-metrics) alongside {{agent}} during the chart installation, which is the default behavior, as both components are installed in the same namespace.

    If your KSM instance runs in a different namespace than {{agent}}, or if it uses a different service name, update the `host` setting in each data set of the integration to point to the KSM service.
    ::::

5. Click **Save and continue**. When prompted, select to **Add Elastic Agent later** since you’ve already added it using Helm.
6. On the {{k8s}} integration page, open the **Assets** tab and select the **[Metrics Kubernetes] Pods** dashboard.

    On the dashboard, you can view the status of your {{k8s}} pods, including metrics on memory usage, CPU usage, and network throughput.

    :::{image} images/helm-example-fleet-metrics-dashboard.png
    :alt: Screen capture of the Metrics Kubernetes pods dashboard
    :screenshot:
    :::


You’ve successfully installed {{agent}} using Helm, and your {{k8s}} metrics data is available for viewing in {{kib}}.


## Tidy up [agent-fleet-managed-helm-example-tidy-up]

After you’ve run through this example, run the `helm uninstall` command to uninstall {{agent}}.

```sh
helm uninstall demo
```

The uninstall should be confirmed as shown:

```sh
release "demo" uninstalled
```

## Next steps

For full details about using the {{agent}} Helm chart refer to the [{{agent}} Helm Chart Readme](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent).

Refer also to the [examples](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent/examples) section of the GitHub repository for advanced use cases, such as integrating {{agent}}s with [KSM autosharding](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent/examples/fleet-managed-ksm-sharding), or configuring [mutual TLS authentication](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent/examples/fleet-managed-certificates) between {{agent}}s and the {{fleet}} Server.