---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/example-kubernetes-fleet-managed-agent-helm.html
---

# Example: Install Fleet-managed Elastic Agent on Kubernetes using Helm [example-kubernetes-fleet-managed-agent-helm]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


This example demonstrates how to install {{fleet}}-managed {{agent}} on a {{k8s}} system using a Helm chart, gather {{k8s}} metrics and send them to an {{es}} cluster in {{ecloud}}, and then view visualizations of those metrics in {{kib}}.

For an overview of the {{agent}} Helm chart and its benefits, refer to [Install {{agent}} on Kubernetes using Helm](/reference/ingestion-tools/fleet/install-on-kubernetes-using-helm.md).

This guide takes you through these steps:

* [Install {{agent}}](#agent-fleet-managed-helm-example-install-agent)
* [Install the Kubernetes integration](#agent-fleet-managed-helm-example-install-integration)
* [Tidy up](#agent-fleet-managed-helm-example-tidy-up)


## Prerequisites [agent-fleet-managed-helm-example-prereqs]

To get started, you need:

* A local install of the [Helm](https://helm.sh/) {{k8s}} package manager.
* An [{{ecloud}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body) hosted {{es}} cluster on version 8.16 or higher.
* An active {{k8s}} cluster.
* A local clone of the [elastic/elastic-agent](https://github.com/elastic/elastic-agent/tree/8.16) GitHub repository. Make sure to use the `8.16` branch to ensure that {{agent}} has full compatibility with the Helm chart.


## Install {{agent}} [agent-fleet-managed-helm-example-install-agent]

1. Open your {{ecloud}} deployment, and from the navigation menu select **Fleet**.
2. From the **Agents** tab, select **Add agent**.
3. In the **Add agent** UI, specify a policy name and select **Create policy**. Leave the **Collect system logs and metrics** option selected.
4. Scroll down in the **Add agent** flyout to the **Install Elastic Agent on your host** section.
5. Select the **Linux TAR** tab and copy the values for `url` and `enrollment-token`. You’ll use these when you run the `helm install` command.
6. Open a terminal shell and change into a directory in your local clone of the `elastic-agent` repo.
7. Copy this command.

    ```sh
    helm install demo ./deploy/helm/elastic-agent \
    --set agent.fleet.enabled=true \
    --set agent.fleet.url=<Fleet-URL> \
    --set agent.fleet.token=<Fleet-token> \
    --set agent.fleet.preset=perNode
    ```

    Note that the command has these properties:

    * `helm install` runs the Helm CLI install tool.
    * `demo` gives a name to the installed chart. You can choose any name.
    * `./deploy/helm/elastic-agent` is a local path to the Helm chart to install (in time it’s planned to have a public URL for the chart).
    * `--set agent.fleet.enabled=true` enables {{fleet}}-managed {{agent}}. The CLI parameter overrides the default `false` value for `agent.fleet.enabled` in the {{agent}} [values.yaml](https://github.com/elastic/elastic-agent/blob/main/deploy/helm/elastic-agent/values.yaml) file.
    * `--set agent.fleet.url=<Fleet-URL>` sets the address where {{agent}} will connect to {{fleet}} in your {{ecloud}} deployment, over port 443 (again, overriding the value set by default in the {{agent}} [values.yaml](https://github.com/elastic/elastic-agent/blob/main/deploy/helm/elastic-agent/values.yaml) file).
    * `--set agent.fleet.token=<Fleet-token>` sets the enrollment token that {{agent}} uses to authenticate with {{fleet}}.
    * `--set agent.fleet.preset=perNode` enables {{k8s}} metrics on `per node` basis. You can alternatively set cluster wide metrics (`clusterWide`) or kube-state-metrics (`ksmSharded`).

        ::::{tip}
        For a full list of all available YAML settings and descriptions, refer to the [{{agent}} Helm Chart Readme](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent).
        ::::

8. Update the command to replace:

    1. `<Fleet-URL>` with the URL that you copied earlier.
    2. `<Fleet-token>` with the enrollment token that you copied earlier.

        After your updates, the command should look something like this:

        ```sh
        helm install demo ./deploy/helm/elastic-agent \
        --set agent.fleet.enabled=true \
        --set agent.fleet.url=https://256575858845283fxxxxxxxd5265d2b4.fleet.us-central1.gcp.foundit.no:443 \
        --set agent.fleet.token=eSVvFDUvSUNPFldFdhhZNFwvS5xxxxxxxxxxxxFEWB1eFF1YedUQ1NWFXwr== \
        --set agent.fleet.preset=perNode
        ```

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
    :class: screenshot
    :::

12. In {{fleet}}, open the **Agents** tab and see that an **Agent-pernode-demo-#** agent is running.
13. Select the agent to view its details.
14. On the **Agent details** tab, on the **Integrations** pane, expand `system-1` to confirm that logs and metrics are incoming. You can click either the `Logs` or `Metrics` link to view details.

    :::{image} images/helm-example-nodes-logs-and-metrics.png
    :alt: Screen capture of the Logs and Metrics view on the Integrations pane
    :class: screenshot
    :::



## Install the Kubernetes integration [agent-fleet-managed-helm-example-install-integration]

Now that you’ve {{agent}} and data is flowing, you can set up the {{k8s}} integration.

1. In your {{ecloud}} deployment, from the {{kib}} menu open the **Integrations** page.
2. Run a search for `Kubernetes` and then select the {{k8s}} integration card.
3. On the {{k8s}} integration page, click **Add Kubernetes** to add the integration to your {{agent}} policy.
4. Scroll to the bottom of **Add Kubernetes integration** page. Under **Where to add this integration?*** select the ***Existing hosts** tab. On the **Agent policies** menu, select the agent policy that you created previously in the [Install {{agent}}](#agent-fleet-managed-helm-example-install-agent) steps.

    You can leave all of the other integration settings at their default values.

5. Click **Save and continue**. When prompted, select to **Add Elastic Agent later** since you’ve already added it using Helm.
6. On the {{k8s}} integration page, open the **Assets** tab and select the **[Metrics Kubernetes] Pods** dashboard.

    On the dashboard, you can view the status of your {{k8s}} pods, including metrics on memory usage, CPU usage, and network throughput.

    :::{image} images/helm-example-fleet-metrics-dashboard.png
    :alt: Screen capture of the Metrics Kubernetes pods dashboard
    :class: screenshot
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

As a reminder, for full details about using the {{agent}} Helm chart refer to the [{{agent}} Helm Chart Readme](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent).
