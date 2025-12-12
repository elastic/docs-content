---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/example-kubernetes-standalone-agent-helm.html
applies_to:
  stack: ga 8.18
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Example: Install standalone Elastic Agent on Kubernetes using Helm [example-kubernetes-standalone-agent-helm]

This example shows how to install the standalone {{agent}} on a {{k8s}} system using a Helm chart, collect {{k8s}} metrics and logs, and send them to an {{es}} cluster in {{ecloud}} for visualization in {{kib}}.

Although this tutorial uses an {{ech}} deployment, you can adapt the same steps for other deployment types. For self-managed, {{eck}}, or {{ece}} deployments, you might need to provide the {{es}} CA certificate during the {{agent}} installation, as outlined in the following sections.

For an overview of the {{agent}} Helm chart and its benefits, refer to [Install {{agent}} on Kubernetes using Helm](/reference/fleet/install-on-kubernetes-using-helm.md).

This guide takes you through these steps:

* [Add the Elastic Helm repository](#preparations)
* [Install {{agent}}s](#agent-standalone-helm-example-install)
* [Update {{agent}} configuration examples](#agent-standalone-helm-example-upgrade)
* [Tidy up](#agent-standalone-helm-example-tidy-up)

## Prerequisites [agent-standalone-helm-example-prereqs]

To get started, you need:

* A local install of the [Helm](https://helm.sh/) {{k8s}} package manager.
* An [{{ech}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body) {{es}} cluster on version 8.18 or higher. An {{serverless-full}} project also meets this requirement.
* An [{{es}} API key](/reference/fleet/grant-access-to-elasticsearch.md#create-api-key-standalone-agent) with the privileges described in the referenced document.
* An active {{k8s}} cluster.

<!--
% We will uncomment this as soon as we document other authentication options in the main page
::::{note}
This example uses an API key for authentication and authorization, but the Helm chart supports other methods too. Refer to [link to main page](link-tbd.md) for more details.
::::
-->

## Installation overview

The installation and configuration steps shown in this example deploy the following components to monitor your Kubernetes cluster:

* A default installation of [`kube-state-metrics` (KSM)](https://github.com/kubernetes/kube-state-metrics), configured as a dependency of the Helm chart. KSM is required by the Kubernetes integration to collect cluster-level metrics.

* A group of standalone {{agent}}s, deployed as a [Kubernetes DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/), and configured to collect the following host level data:
    * Host level metrics and logs through the [System Integration](integration-docs://reference/system/index.md). This enables the monitoring of your Kubernetes nodes at OS level. {{agent}} Pods will collect system metrics and logs from their own hosts.
    * Kubernetes node-level metrics and logs through the [Kubernetes Integration](integration-docs://reference/kubernetes/index.md): This integration collects {{k8s}} metrics and Pods' logs related to the node where each {{agent}} Pod runs. It focuses on node-level visibility only, not cluster-wide metrics, which are handled separately.

* A standalone {{agent}}, deployed as a `Deployment` of 1 replica, and configured to collect {{k8s}} cluster-level metrics and events through the [Kubernetes integration](integration-docs://reference/kubernetes/index.md): This complements the node-level data gathered by the DaemonSet, providing full visibility into the cluster's state and workloads. Some of this data is retrieved from kube-state-metrics.

By default, all resources are installed in the namespace defined by your current `kubectl` context. You can override this by specifying a different namespace using the `--namespace` option during installation.

<!--
% maybe not needed, as ksm autosharding in this case is just an extra flag during install
::::{note}
The proposed approach of an {{agent}} DaemonSet for node-level data and a Deployment for cluster-level data works well for small to medium-sized {{k8s}} clusters.

For larger clusters, or when kube-state-metrics (KSM) metrics collection becomes a performance bottleneck, we recommend a more scalable architecture: move the KSM metric collection to a separate set of agents deployed as sidecars alongside KSM, with autosharding enabled.

This can be easily implemented with the Helm chart. For details, refer to the [KSM autosharding example](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent/examples/fleet-managed-ksm-sharding).
::::

% we will uncomment the next line when the use cases are documented in the landing page :)
% For other architectures and use cases, refer to [Advanced use cases](./install-on-kubernetes-using-helm.md#advanced-use-cases).
-->

## Step 1: Add the Elastic Helm repository [preparations]

:::{include} _snippets/agent_add_helm_repository.md
:::

## Step 2: Install {{agent}}s [agent-standalone-helm-example-install]

1. Open your {{ecloud}} deployment, and from the navigation menu select **Manage this deployment**.
2. In the **Applications** section, copy the {{es}} endpoint and make a note of the endpoint value.
3. Open a terminal shell on your local system where the Helm tool is installed and you have access to the {{k8s}} cluster.
4. Copy and prepare the command to install the chart:

    ```sh
    helm install demo elastic/elastic-agent \
    --set kubernetes.enabled=true \
    --set system.enabled=true \
    --set outputs.default.type=ESPlainAuthAPI \
    --set outputs.default.url=<ES-endpoint>:443 \ <1>
    --set outputs.default.api_key="API_KEY" <2>
    ```
    1. Substitute <ES-endpoint> with the {{es}} endpoint value that you copied earlier. Be sure to include the right port, as the agent might default to port 9200 if no port is specified.
    2. Substitute API_KEY with your [API key in `Beats` format](/reference/fleet/grant-access-to-elasticsearch.md#create-api-key-standalone-agent).

    The command has these properties:

    * `helm install`: Runs the Helm CLI install tool. You can use `helm upgrade` to modify or update an installed release.
    * `demo`: The name for this specific installation of the chart, known as the **release name**. You can choose any name.
    * `elastic/elastic-agent`: The name of the chart to install, using the format `<repository>/<chart-name>`.
    * `--set kubernetes.enabled=true`: Adds and configures the {{k8s}} integration. This setting is enabled by default.
    * `--set system.enabled=true`: Adds and configures the system integration, which is disabled by default.
    * `--set outputs.default.type=ESPlainAuthAPI`: Sets the authentication method for the {{es}} output to require an API key. This setting defaults to `ESPlainAuthBasic`.
    * `--set outputs.default.api_key="API_KEY"`: Sets the API key that {{agent}} will use to authenticate with your {{es}} cluster.
    * `--set outputs.default.url=<ES-endpoint>:443`: Sets the address of the {{es}} endpoint, where the {{agent}} will send all collected data.

    After your updates, the command should be similar to:

    ```sh
    helm install demo elastic/elastic-agent \
    --set kubernetes.enabled=true \
    --set system.enabled=true \
    --set outputs.default.type=ESPlainAuthAPI \
    --set outputs.default.url=https://demo.es.us-central1.gcp.foundit.no:443 \
    --set outputs.default.api_key="A6ecaHNTJUFFcJI6esf4:5HJPxxxxxxxPS4KwSBeVEs"
    ```

    ::::{tip}
    For a full list of all available values settings and descriptions, refer to the [{{agent}} Helm Chart Readme](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent) and default [values.yaml](https://github.com/elastic/elastic-agent/blob/main/deploy/helm/elastic-agent/values.yaml).

    The following options could be useful for special use cases:
    * `--namespace <namespace>`: Allows to install all resources in a specific namespace.
    * `--version <version>`: Installs a specific version of the Helm chart and {{agent}}. Refer to [Preparations](#preparations) to check available versions.
    * `--set agent.version=<version>`: Installs a specific version of {{agent}}. By default, the chart installs the agent version that matches its own.
    * `--set-file 'outputs.default.certificate_authorities[0].value=/local-path/to/es-ca.crt'`: Specifies the CA certificate that {{agent}} should trust when connecting to {{es}}. This is typically required when {{es}} uses a certificate signed by a private CA. Not needed for clusters hosted on {{ecloud}}.
    * `--set kube-state-metrics.enabled=false`: Prevents the installation of kube-state-metrics. Useful if KSM is already installed in your cluster.
    * `--set kubernetes.state.host`: Sets the kube-state-metrics endpoint used in the Kubernetes integration input streams. Useful if you already have KSM installed and you are not deploying it with the chart.
    * `--set kubernetes.state.enabled=false`: Disables all input streams related to kube-state-metrics in the Kubernetes integration configuration.
    * `--set kube-state-metrics.fullnameOverride=ksm`: Overrides the default release name (`kube-state-metrics`) used for the KSM deployment. Useful if you already have a KSM instance deployed and want to install a second one with a different name.    
    * `--set kubernetes.state.agentAsSidecar.enabled=true`: Enables [KSM autosharding](https://github.com/kubernetes/kube-state-metrics?tab=readme-ov-file#automated-sharding) by deploying KSM as a `StatefulSet` with {{agents}} as sidecar containers. This setup is useful and recommended for large Kubernetes clusters to distribute the metric collection load. To scale KSM in this configuration, use the `kube-state-metrics.replicas` setting.
    ::::

6. Run the command.

    The command output should confirm that two {{agents}} have been installed (one `DaemonSet` and one `Deployment`), along with the {{k8s}} and system integrations, and that kube-state-metrics has also been deployed in the same namespace.

    ```sh
    ...
    Release "demo" is installed at "default" namespace

    Installed agents:
    - clusterWide [deployment - standalone mode]
    - perNode [daemonset - standalone mode]

    Installed kube-state-metrics at "default" namespace.

    Installed integrations:
    - kubernetes [built-in chart integration]
    - system [built-in chart integration]
    ...
    ```

7. Run the `kubectl get pods -n default` command to confirm that the {{agent}} pods are running:

    ```sh
    NAME                                      READY   STATUS    RESTARTS   AGE
    agent-clusterwide-demo-5fc46c54d5-7vhjz   1/1     Running   0          5m35s
    agent-pernode-demo-2fp77                  1/1     Running   0          5m34s
    agent-pernode-demo-q9f8n                  1/1     Running   0          5m34s
    agent-pernode-demo-twrtw                  1/1     Running   0          5m35s
    kube-state-metrics-6bc97757c4-x9rkg       1/1     Running   0          5m35s
    ```

8. In your {{ecloud}} deployment, from the {{kib}} menu open the **Integrations** page.
9. Run a search for `Kubernetes` and then select the {{k8s}} integration card.
10. On the {{k8s}} integration **Settings** page, select **Install Kubernetes**. This installs the dashboards, {{es}} indexes, and other assets used to monitor your {{k8s}} cluster.
11. On the {{k8s}} integration page, open the **Assets** tab and select the **[Metrics Kubernetes] Nodes** dashboard.

    On the dashboard, you can view the status of your {{k8s}} nodes, including metrics on memory, CPU, and filesystem usage, network throughput, and more.

    :::{image} images/helm-example-nodes-metrics-dashboard.png
    :alt: Screen capture of the Metrics Kubernetes nodes dashboard
    :screenshot:
    :::

12. On the {{k8s}} integration page, open the **Assets** tab and select the **[Metrics Kubernetes] Pods** dashboard. As with the nodes dashboard, on this dashboard you can view the status of your {{k8s}} pods, including various metrics on memory, CPU, and network throughput.

    :::{image} images/helm-example-pods-metrics-dashboard.png
    :alt: Screen capture of the Metrics Kubernetes pods dashboard
    :screenshot:
    :::


## Update {{agent}} configuration [agent-standalone-helm-example-upgrade]

Now that you have {{agent}} installed, collecting, and sending data successfully, let’s try changing the agent configuration settings.

### Example: disable kube-state-metrics and input streams

In the previous installation example, two {{agents}}, per-node and cluster-wide, were installed, along with kube-state-metrics. Let’s suppose that you don’t need metrics related to kube-state-metrics and would like to upgrade your configuration accordingly.

::::{note}
This is only an example of how to update the configuration of an installed Helm chart. Disabling kube-state-metrics will prevent several Kubernetes dashboards in {{kib}} from displaying data.
::::

The following values will help achieve that goal:

* `kubernetes.state.enabled=false`: Disables all input streams related to kube-state-metrics in the Kubernetes integration configuration of the cluster-wide {{agent}}.
* `kube-state-metrics.enabled=false`: Prevents the installation of the kube-state-metrics component.

To update the configuration of an installed release:

1. Start by copying the same command you used previously to install {{agent}}, for example:

    ```sh
    helm install demo elastic/elastic-agent \
    --set kubernetes.enabled=true \
    --set system.enabled=true \
    --set outputs.default.type=ESPlainAuthAPI \
    --set outputs.default.url=https://demo.es.us-central1.gcp.foundit.no:443 \
    --set outputs.default.api_key="A6ecaHNTJUFFcJI6esf4:5HJPxxxxxxxPS4KwSBeVEs"
    ```

2. Update the command as follows:

    1. Replace `install` with `upgrade`, keeping the same release name (`demo` in this example).
    2. Modify the parameters as needed:

        ```sh
        helm upgrade demo elastic/elastic-agent \
        --set kubernetes.enabled=true \
        --set system.enabled=true \
        --set kubernetes.state.enabled=false \
        --set kube-state-metrics.enabled=false \
        --set outputs.default.type=ESPlainAuthAPI \
        --set outputs.default.url=https://demo.es.us-central1.gcp.foundit.no:443 \
        --set outputs.default.api_key="A6ecaHNTJUFFcJI6esf4:5HJPxxxxxxxPS4KwSBeVEs"
        ```

3. Run the command.

    After running the command, kube-state-metrics will no longer be running, and the `agent-clusterwide-demo` instance will be configured without any state-related data streams.

    The upgrade output should look similar to the following:

    ```sh
    ...
    Installed agents:
    - clusterWide [deployment - standalone mode]
    - perNode [daemonset - standalone mode]

    Installed integrations:
    - kubernetes [built-in chart integration]
    - system [built-in chart integration]
    ...
    ```

    To review the full contents of the installed release, run:

    ```sh
    helm get manifest demo
    ```

You’ve upgraded your configuration to run without the kube-state-metrics service. You can similarly upgrade your agent to change other settings defined in the in the {{agent}} [values.yaml](https://github.com/elastic/elastic-agent/blob/main/deploy/helm/elastic-agent/values.yaml) file.

### Example: change {{agent}}'s running mode [agent-standalone-helm-example-change-mode]

By default {{agent}} runs under the `elastic` user account. For some use cases you may want to temporarily change an agent to run with higher privileges.

1. Run the `kubectl get pods -n default` command to view the running {{agent}} pods:

    ```sh
    NAME                                      READY   STATUS    RESTARTS   AGE
    agent-clusterwide-demo-7b5df89b75-sfhd7   1/1     Running   0          14m
    agent-pernode-demo-fm6tr                  1/1     Running   0          14m
    agent-pernode-demo-hh6xb                  1/1     Running   0          14m
    agent-pernode-demo-szrp9                  1/1     Running   0          14m
    ```

2. Now, run the `kubectl exec` command to enter one of the running {{agents}}, substituting the correct pod name returned from the previous command. For example:

    ```sh
    kubectl exec -it pods/agent-pernode-demo-fm6tr -- bash
    ```

3. From inside the pod, run the Linux `ps aux` command to view the running processes.

    ```sh
    ps aux
    ```

    The results should be similar to the following:

    ```sh
    USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    elastic+           1  0.0  0.0   1936   416 ?        Ss   21:04   0:00 /usr/bin/tini -- /usr/local/bin/docker-entrypoint -c /etc/elastic-agent/agent.yml -e
    elastic+          10  0.2  1.3 2555252 132804 ?      Sl   21:04   0:13 elastic-agent container -c /etc/elastic-agent/agent.yml -e
    elastic+          37  0.6  2.0 2330112 208468 ?      Sl   21:04   0:37 /usr/share/elastic-agent/data/elastic-agent-d99b09/components/agentbeat metricbeat -E
    elastic+          38  0.2  1.7 2190072 177780 ?      Sl   21:04   0:13 /usr/share/elastic-agent/data/elastic-agent-d99b09/components/agentbeat filebeat -E se
    elastic+          56  0.1  1.7 2190136 175896 ?      Sl   21:04   0:11 /usr/share/elastic-agent/data/elastic-agent-d99b09/components/agentbeat metricbeat -E
    elastic+          68  0.1  1.8 2190392 184140 ?      Sl   21:04   0:12 /usr/share/elastic-agent/data/elastic-agent-d99b09/components/agentbeat metricbeat -E
    elastic+          78  0.7  2.0 2330496 204964 ?      Sl   21:04   0:48 /usr/share/elastic-agent/data/elastic-agent-d99b09/components/agentbeat filebeat -E se
    elastic+         535  0.0  0.0   3884  3012 pts/0    Ss   22:47   0:00 bash
    elastic+         543  0.0  0.0   5480  2360 pts/0    R+   22:47   0:00 ps aux
    ```

4. In the command output, {{agent}} is currently running as the `elastic` user:

    ```sh
    elastic+          10  0.2  1.3 2555252 132804 ?      Sl   21:04   0:13 elastic-agent container -c /etc/elastic-agent/agent.yml -e
    ```

5. Run `exit` to leave the {{agent}} pod.
6. Run the `helm upgrade` command again, this time adding the parameter `--set agent.unprivileged=false` to override the default `true` value for that setting.

    ```sh
    helm upgrade demo elastic/elastic-agent \
    --set kubernetes.enabled=true \
    --set system.enabled=true \
    --set outputs.default.type=ESPlainAuthAPI \
    --set outputs.default.url=<ES-endpoint>:443 \
    --set outputs.default.api_key="API_KEY" \
    --set agent.unprivileged=false
    ```

7. Run the `kubectl get pods -n default` command to view the running {{agent}} pods:

    ```sh
    NAME                                      READY   STATUS    RESTARTS   AGE
    agent-clusterwide-demo-77c65f6c7b-trdms   1/1     Running   0          5m18s
    agent-pernode-demo-s6s7z                  1/1     Running   0          5m18s
    agent-pernode-demo-v6rf8                  1/1     Running   0          5m18s
    agent-pernode-demo-6zx8l                  1/1     Running   0          5m18s
    ```

8. Re-run the `kubectl exec` command to enter one of the running {{agents}}, substituting the correct pod name. For example:

    ```sh
    kubectl exec -it pods/agent-pernode-demo-s6s7z -- bash
    ```

9. From inside the pod, run the Linux `ps aux` command to view the running processes.

    ```sh
    USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    root       1  0.0  0.0   1936   452 ?        Ss   23:10   0:00 /usr/bin/tini -- /usr/local/bin/docker-entrypoint -c /etc/elastic-agent/agent.yml -e
    root       9  0.9  1.3 2488368 135920 ?      Sl   23:10   0:01 elastic-agent container -c /etc/elastic-agent/agent.yml -e
    root      27  0.9  1.9 2255804 203128 ?      Sl   23:10   0:01 /usr/share/elastic-agent/data/elastic-agent-d99b09/components/agentbeat metricbeat -E
    root      44  0.3  1.8 2116148 187432 ?      Sl   23:10   0:00 /usr/share/elastic-agent/data/elastic-agent-d99b09/components/agentbeat metricbeat -E
    root      64  0.3  1.8 2263868 188892 ?      Sl   23:10   0:00 /usr/share/elastic-agent/data/elastic-agent-d99b09/components/agentbeat metricbeat -E
    root      76  0.4  1.8 2190136 190972 ?      Sl   23:10   0:00 /usr/share/elastic-agent/data/elastic-agent-d99b09/components/agentbeat filebeat -E se
    root     100  1.2  2.0 2256316 207692 ?      Sl   23:10   0:01 /usr/share/elastic-agent/data/elastic-agent-d99b09/components/agentbeat filebeat -E se
    root     142  0.0  0.0   3752  3068 pts/0    Ss   23:12   0:00 bash
    root     149  0.0  0.0   5480  2376 pts/0    R+   23:13   0:00 ps aux
    ```

10. Run `exit` to leave the {{agent}} pod.

You’ve upgraded the {{agent}} privileges to run as `root`. To change the settings back, you can re-run the `helm upgrade` command with `--set agent.unprivileged=true` to return to the default `unprivileged` mode.


## Tidy up [agent-standalone-helm-example-tidy-up]

After you’ve run through this example, run the `helm uninstall` command to uninstall {{agent}}.

```sh
helm uninstall demo
```

The uninstall should be confirmed as shown:

```sh
release "demo" uninstalled
```

## Next steps

For full details about using the {{agent}} Helm chart, refer to the [{{agent}} Helm Chart Readme](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent).

Refer to the [examples](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent/examples) section of the GitHub repository for advanced use cases.