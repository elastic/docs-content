---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/example-kubernetes-standalone-agent-helm.html
---

# Example: Install standalone Elastic Agent on Kubernetes using Helm [example-kubernetes-standalone-agent-helm]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


This example demonstrates how to install standalone {{agent}} on a Kubernetes system using a Helm chart, gather Kubernetes metrics and send them to an {{es}} cluster in {{ecloud}}, and then view visualizations of those metrics in {{kib}}.

For an overview of the {{agent}} Helm chart and its benefits, refer to [Install {{agent}} on Kubernetes using Helm](/reference/ingestion-tools/fleet/install-on-kubernetes-using-helm.md).

This guide takes you through these steps:

* [Install {{agent}}](#agent-standalone-helm-example-install)
* [Upgrade your {{agent}} configuration](#agent-standalone-helm-example-upgrade)
* [Change {{agent}}'s running mode](#agent-standalone-helm-example-change-mode)
* [Tidy up](#agent-standalone-helm-example-tidy-up)


## Prerequisites [agent-standalone-helm-example-prereqs]

To get started, you need:

* A local install of the [Helm](https://helm.sh/) {{k8s}} package manager.
* An [{{ecloud}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body) hosted {{es}} cluster on version 8.16 or higher.
* An [{{es}} API key](/reference/ingestion-tools/fleet/grant-access-to-elasticsearch.md#create-api-key-standalone-agent).
* An active {{k8s}} cluster.
* A local clone of the [elastic/elastic-agent](https://github.com/elastic/elastic-agent/tree/8.16) GitHub repository. Make sure to use the `8.16` branch to ensure that {{agent}} has full compatibility with the Helm chart.


## Install {{agent}} [agent-standalone-helm-example-install]

1. Open your {{ecloud}} deployment, and from the navigation menu select **Manage this deployment**.
2. In the **Applications** section, copy the {{es}} endpoint and make a note of the endpoint value.
3. Open a terminal shell and change into a directory in your local clone of the `elastic-agent` repo.
4. Copy this command.

    ```sh
    helm install demo ./deploy/helm/elastic-agent \
    --set kubernetes.enabled=true \
    --set outputs.default.type=ESPlainAuthAPI \
    --set outputs.default.url=<ES-endpoint>:443 \
    --set outputs.default.api_key="API_KEY"
    ```

    Note that the command has these properties:

    * `helm install` runs the Helm CLI install tool.
    * `demo` gives a name to the installed chart. You can choose any name.
    * `./deploy/helm/elastic-agent` is a local path to the Helm chart to install (in time it’s planned to have a public URL for the chart).
    * `--set kubernetes.enabled=true` enables the {{k8s}} integration. The CLI parameter overrides the default `false` value for `kubernetes.enabled` in the {{agent}} [values.yaml](https://github.com/elastic/elastic-agent/blob/main/deploy/helm/elastic-agent/values.yaml) file.
    * `--set outputs.default.type=ESPlainAuthAPI` sets the authentication method for the {{es}} output to require an API key (again, overriding the value set by default in the {{agent}} [values.yaml](https://github.com/elastic/elastic-agent/blob/main/deploy/helm/elastic-agent/values.yaml) file).
    * `--set outputs.default.url=<ES-endpoint>:443` sets the address of your {{ecloud}} deployment, where {{agent}} will send its output over port 443.
    * `--set outputs.default.api_key="API_KEY"` sets the API key that {{agent}} will use to authenticate with your {{es}} cluster.

        ::::{tip}
        For a full list of all available YAML settings and descriptions, refer to the [{{agent}} Helm Chart Readme](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent).
        ::::

5. Update the command to replace:

    1. `<ES-endpoint>` with the {{es}} endpoint value that you copied earlier.
    2. `<API_KEY>` with your API key name.

        After your updates, the command should look something like this:

        ```sh
        helm install demo ./deploy/helm/elastic-agent \
        --set kubernetes.enabled=true \
        --set outputs.default.type=ESPlainAuthAPI \
        --set outputs.default.url=https://demo.es.us-central1.gcp.foundit.no:443 \
        --set outputs.default.api_key="A6ecaHNTJUFFcJI6esf4:5HJPxxxxxxxPS4KwSBeVEs"
        ```

6. Run the command.

    The command output should confirm that three {{agents}} have been installed as well as the {{k8s}} integration:

    ```sh
    ...
    Installed agents:
      - clusterWide [deployment - standalone mode]
      - ksmSharded [statefulset - standalone mode]
      - perNode [daemonset - standalone mode]

    Installed integrations:
      - kubernetes [built-in chart integration]
    ...
    ```

7. Run the `kubectl get pods -n default` command to confirm that the {{agent}} pods are running:

    ```sh
    NAME                                      READY   STATUS    RESTARTS   AGE
    agent-clusterwide-demo-77c65f6c7b-trdms   1/1     Running   0          5m18s
    agent-ksmsharded-demo-0                   2/2     Running   0          5m18s
    agent-pernode-demo-c7d75                  1/1     Running   0          5m18s
    ```

8. In your {{ecloud}} deployment, from the {{kib}} menu open the **Integrations** page.
9. Run a search for `Kubernetes` and then select the {{k8s}} integration card.
10. On the {{k8s}} integration page, select **Install Kubernetes assets**. This installs the dashboards, {{es}} indexes, and other assets used to monitor your {{k8s}} cluster.
11. On the {{k8s}} integration page, open the **Assets** tab and select the **[Metrics Kubernetes] Nodes** dashboard.

    On the dashboard, you can view the status of your {{k8s}} nodes, including metrics on memory, CPU, and filesystem usage, network throughput, and more.

    :::{image} images/helm-example-nodes-metrics-dashboard.png
    :alt: Screen capture of the Metrics Kubernetes nodes dashboard
    :class: screenshot
    :::

12. On the {{k8s}} integration page, open the **Assets** tab and select the **[Metrics Kubernetes] Pods** dashboard. As with the nodes dashboard, on this dashboard you can view the status of your {{k8s}} pods, including various metrics on memory, CPU, and network throughput.

    :::{image} images/helm-example-pods-metrics-dashboard.png
    :alt: Screen capture of the Metrics Kubernetes pods dashboard
    :class: screenshot
    :::



## Upgrade your {{agent}} configuration [agent-standalone-helm-example-upgrade]

Now that you have {{agent}} installed, collecting, and sending data successfully, let’s try changing the agent configuration settings.

In the previous install example, three {{agent}} nodes were installed. One of these nodes, `agent-ksmsharded-demo-0`, is installed to enable the [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics) service. Let’s suppose that you don’t need those metrics and would like to upgrade your configuration accordingly.

1. Copy the command that you used earlier to install {{agent}}:

    ```sh
    helm install demo ./deploy/helm/elastic-agent \
    --set kubernetes.enabled=true \
    --set outputs.default.type=ESPlainAuthAPI \
    --set outputs.default.url=<ES-endpoint>:443 \
    --set outputs.default.api_key="API_KEY"
    ```

2. Update the command as follows:

    1. Change `install` to upgrade.
    2. Add a parameter `--set kubernetes.state.enabled=false`. This will override the default `true` value for the setting `kubernetes.state` in the {{agent}} [values.yaml](https://github.com/elastic/elastic-agent/blob/main/deploy/helm/elastic-agent/values.yaml) file.

        ```sh
        helm upgrade demo ./deploy/helm/elastic-agent \
        --set kubernetes.enabled=true \
        --set kubernetes.state.enabled=false \
        --set outputs.default.type=ESPlainAuthAPI \
        --set outputs.default.url=<ES-endpoint>:443 \
        --set outputs.default.api_key="API_KEY"
        ```

3. Run the command.

    The command output should confirm that now only two {{agents}} are installed together with the {{k8s}} integration:

    ```sh
    ...
    Installed agents:
      - clusterWide [deployment - standalone mode]
      - perNode [daemonset - standalone mode]

    Installed integrations:
      - kubernetes [built-in chart integration]
    ...
    ```


You’ve upgraded your configuration to run only two {{agents}}, without the kube-state-metrics service. You can similarly upgrade your agent to change other settings defined in the in the {{agent}} [values.yaml](https://github.com/elastic/elastic-agent/blob/main/deploy/helm/elastic-agent/values.yaml) file.


## Change {{agent}}'s running mode [agent-standalone-helm-example-change-mode]

By default {{agent}} runs under the `elastic` user account. For some use cases you may want to temporarily change an agent to run with higher privileges.

1. Run the `kubectl get pods -n default` command to view the running {{agent}} pods:

    ```sh
    NAME                                      READY   STATUS    RESTARTS   AGE
    agent-clusterwide-demo-77c65f6c7b-trdms   1/1     Running   0          5m18s
    agent-pernode-demo-c7d75                  1/1     Running   0          5m18s
    ```

2. Now, run the `kubectl exec` command to enter one of the running {{agents}}, substituting the correct pod name returned from the previous command. For example:

    ```sh
    kubectl exec -it pods/agent-pernode-demo-c7d75 -- bash
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

4. In the command output, note that {{agent}} is currently running as the `elastic` user:

    ```sh
    elastic+          10  0.2  1.3 2555252 132804 ?      Sl   21:04   0:13 elastic-agent container -c /etc/elastic-agent/agent.yml -e
    ```

5. Run `exit` to leave the {{agent}} pod.
6. Run the `helm upgrade` command again, this time adding the parameter `--set agent.unprivileged=false` to override the default `true` value for that setting.

    ```sh
    helm upgrade demo ./deploy/helm/elastic-agent \
    --set kubernetes.enabled=true \
    --set kubernetes.state.enabled=false \
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

As a reminder, for full details about using the {{agent}} Helm chart refer to the [{{agent}} Helm Chart Readme](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent).
