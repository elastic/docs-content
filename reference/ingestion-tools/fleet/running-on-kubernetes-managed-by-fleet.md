---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/running-on-kubernetes-managed-by-fleet.html
---

# Run Elastic Agent on Kubernetes managed by Fleet [running-on-kubernetes-managed-by-fleet]

## What you need [_what_you_need_2]

* [kubectl installed](https://kubernetes.io/docs/tasks/tools/).
* {{es}} for storing and searching your data, and {{kib}} for visualizing and managing it.

  ::::{tab-set}

  :::{tab-item} {{ech}}

  To get started quickly, spin up an [{{ech}}](https://www.elastic.co/cloud/elasticsearch-service) deployment. {{ech}} is available on AWS, GCP, and Azure. [Try it out for free](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
  :::

  :::{tab-item} Self-managed

  To install and run {{es}} and {{kib}}, see [Installing the {{stack}}](/deploy-manage/deploy/self-managed/deploy-cluster.md).
  :::

  ::::

* `kube-state-metrics`.

    You need to deploy `kube-state-metrics` to get the metrics about the state of the objects on the cluster (see the [Kubernetes deployment](https://github.com/kubernetes/kube-state-metrics#kubernetes-deployment) docs). You can do that by first downloading the project:

    ```sh
    gh repo clone kubernetes/kube-state-metrics
    ```

    And then deploying it:

    ```sh
    kubectl apply -k kube-state-metrics
    ```

    ::::{warning}
    On managed Kubernetes solutions, such as AKS, GKE or EKS, {{agent}} does not have the required permissions to collect metrics from [Kubernetes control plane](https://kubernetes.io/docs/concepts/overview/components/#control-plane-components) components, like `kube-scheduler` and `kube-controller-manager`. Audit logs are only available on Kubernetes control plane nodes as well, and hence cannot be collected by {{agent}}. Refer [here](integration-docs://docs/reference/kubernetes.md#kubernetes-scheduler-and-controllermanager) to find more information. For more information about specific cloud providers, refer to [Run {{agent}} on Azure AKS managed by {{fleet}}](/reference/ingestion-tools/fleet/running-on-aks-managed-by-fleet.md), [Run {{agent}} on GKE managed by {{fleet}}](/reference/ingestion-tools/fleet/running-on-gke-managed-by-fleet.md) and [Run {{agent}} on Amazon EKS managed by {{fleet}}](/reference/ingestion-tools/fleet/running-on-eks-managed-by-fleet.md)
    ::::



### Step 1: Download the {{agent}} manifest [_step_1_download_the_agent_manifest]

::::{note}
You can find {{agent}} Docker images [here](https://www.docker.elastic.co/r/elastic-agent/elastic-agent).
::::


Download the manifest file:

```sh
curl -L -O https://raw.githubusercontent.com/elastic/elastic-agent/master/deploy/kubernetes/elastic-agent-managed-kubernetes.yaml
```

::::{note}
You might need to adjust [resource limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) of the {{agent}} container in the manifest. Container resource usage depends on the number of data streams and the environment size.
::::


This manifest includes the Kubernetes integration to collect Kubernetes metrics and System integration to collect system level metrics and logs from nodes.

The {{agent}} is deployed as a [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/) to ensure that there is a running instance on each node of the cluster. These instances are used to retrieve most metrics from the host, such as system metrics, Docker stats, and metrics from all the services running on top of Kubernetes. These metrics are accessed through the deployed `kube-state-metrics`. Notice that everything is deployed under the `kube-system` namespace by default. To change the namespace, modify the manifest file.

Moreover, one of the Pods in the DaemonSet will constantly hold a *leader lock* which makes it responsible for handling cluster-wide monitoring. You can find more information about leader election configuration options at [leader election provider](/reference/ingestion-tools/fleet/kubernetes_leaderelection-provider.md). The leader pod will retrieve metrics that are unique for the whole cluster, such as Kubernetes events or [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics).

For Kubernetes Security Posture Management (KSPM) purposes, the {{agent}} requires read access to various types of Kubernetes resources, node processes, and files. To achieve this, read permissions are granted to the {{agent}} for the necessary resources, and volumes from the hosting node’s file system are mounted to allow accessibility to the {{agent}} pods.

::::{tip}
The size and the number of nodes in a Kubernetes cluster can be large at times, and in such a case the Pod that will be collecting cluster level metrics might require more runtime resources than you would like to dedicate to all of the pods in the DaemonSet. The leader which is collecting the cluster wide metrics may face performance issues due to resource limitations if under-resourced. In this case users might consider avoiding the use of a single DaemonSet with the leader election strategy and instead run a dedicated standalone {{agent}} instance for collecting cluster wide metrics using a Deployment in addition to the DaemonSet to collect metrics for each node. Then both the Deployment and the DaemonSet can be resourced independently and appropriately. For more information check the [Scaling {{agent}} on {{k8s}}](/reference/ingestion-tools/fleet/scaling-on-kubernetes.md) page.
::::



### Step 2: Configure {{agent}} policy [_step_2_configure_agent_policy]

The {{agent}} needs to be assigned to a policy to enable the proper inputs. To achieve Kubernetes observability, the policy needs to include the Kubernetes integration. Refer to [Create a policy](/reference/ingestion-tools/fleet/agent-policy.md#create-a-policy) and [Add an integration to a policy](/reference/ingestion-tools/fleet/agent-policy.md#add-integration) to learn how to configure the [Kubernetes integration](integration-docs://docs/reference/kubernetes.md).


### Step 3: Enroll {{agent}} to the policy [_step_3_enroll_agent_to_the_policy]

Enrollment of an {{agent}} is defined as the action to register a specific agent to a running {{fleet-server}}.

{{agent}} is enrolled to a running {{fleet-server}} by using `FLEET_URL` parameter. Additionally, the `FLEET_ENROLLMENT_TOKEN` parameter is used to connect {{agent}} to a specific {{agent}} policy.

A new `FLEET_ENROLLMENT_TOKEN` will be created upon new policy creation and will be inserted inside the Elastic Agent Manifest during the Guided installation.

Find more information for [Enrollment Tokens](/reference/ingestion-tools/fleet/fleet-enrollment-tokens.md).

To specify different destination/credentials, change the following parameters in the manifest file:

```yaml
- name: FLEET_URL
  value: "https://fleet-server_url:port" <1>
- name: FLEET_ENROLLMENT_TOKEN
  value: "token" <2>
- name: FLEET_SERVER_POLICY_ID
  value: "fleet-server-policy" <3>
- name: KIBANA_HOST
  value: "" <4>
- name: KIBANA_FLEET_USERNAME
  value: "" <5>
- name: KIBANA_FLEET_PASSWORD
  value: "" <6>
```

1. URL to enroll the {{fleet-server}} into. You can find it in {{kib}}. Select **Management → {{fleet}} → Fleet Settings**, and copy the {{fleet-server}} host URL.
2. The token to use for enrollment. Close the flyout panel and select **Enrollment tokens**. Find the Agent policy you created before to enroll {{agent}} into, and display and copy the secret token.
3. The policy ID for {{fleet-server}} to use on itself.
4. The {{kib}} host.
5. The basic authentication username used to connect to {{kib}} and retrieve a `service_token` to enable {{fleet}}.
6. The basic authentication password used to connect to {{kib}} and retrieve a `service_token` to enable {{fleet}}.


If you need to run {{fleet-server}} as well, adjust the `docker run` command above by adding these environment variables:

```yaml
- name: FLEET_SERVER_ENABLE
  value: "true" <1>
- name: FLEET_SERVER_ELASTICSEARCH_HOST
  value: "<elasticsearch-host>" <2>
- name: FLEET_SERVER_SERVICE_TOKEN
  value: "<service-token>" <3>
```

1. Set to `true` to bootstrap {{fleet-server}} on this {{agent}}. This automatically forces {{fleet}} enrollment as well.
2. The Elasticsearch host for Fleet Server to communicate with, for example `http://elasticsearch:9200`.
3. Service token to use for communication with {{es}} and {{kib}}.


Refer to [Environment variables](/reference/ingestion-tools/fleet/agent-environment-variables.md) for all available options.


### Step 4: Configure tolerations [_step_4_configure_tolerations]

Kubernetes control plane nodes can use [taints](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/) to limit the workloads that can run on them. The manifest for standalone {{agent}} defines tolerations to run on these. Agents running on control plane nodes collect metrics from the control plane components (scheduler, controller manager) of Kubernetes. To disable {{agent}} from running on control plane nodes, remove the following part of the DaemonSet spec:

```yaml
spec:
  # Tolerations are needed to run Elastic Agent on Kubernetes control-plane nodes.
  # Agents running on control-plane nodes collect metrics from the control plane components (scheduler, controller manager) of Kubernetes
  tolerations:
    - key: node-role.kubernetes.io/control-plane
      effect: NoSchedule
    - key: node-role.kubernetes.io/master
      effect: NoSchedule
```

Both these two tolerations do the same, but `node-role.kubernetes.io/master` is [deprecated as of Kubernetes version v1.25](https://kubernetes.io/docs/reference/labels-annotations-taints/#node-role-kubernetes-io-master-taint).


### Step 5: Deploy the {{agent}} [_step_5_deploy_the_agent]

To deploy {{agent}} to Kubernetes, run:

```sh
kubectl create -f elastic-agent-managed-kubernetes.yaml
```

To check the status, run:

```sh
$ kubectl -n kube-system get pods -l app=elastic-agent
NAME                            READY   STATUS    RESTARTS   AGE
elastic-agent-4665d             1/1     Running   0          81m
elastic-agent-9f466c4b5-l8cm8   1/1     Running   0          81m
elastic-agent-fj2z9             1/1     Running   0          81m
elastic-agent-hs4pb             1/1     Running   0          81m
```

::::{admonition} Running {{agent}} on a read-only file system
:class: tip

If you’d like to run {{agent}} on Kubernetes on a read-only file system, you can do so by specifying the `readOnlyRootFilesystem` option.

::::



### Step 6: View your data in {{kib}} [_step_6_view_your_data_in_kib]

1. Launch {{kib}}:

    ::::{tab-set}

    :::{tab-item} {{ech}}

    1. [Log in](https://cloud.elastic.co/) to your {{ecloud}} account.
    2. Navigate to the {{kib}} endpoint in your deployment.
    :::

    :::{tab-item} Self-managed

    Point your browser to [http://localhost:5601](http://localhost:5601), replacing `localhost` with the name of the {{kib}} host.

    :::

    ::::

2. To check if your {{agent}} is enrolled in {{fleet}}, go to **Management → {{fleet}} → Agents**.

    :::{image} images/kibana-fleet-agents.png
    :alt: {{agent}}s {{fleet}} page
    :class: screenshot
    :::

3. To view data flowing in, go to **Analytics → Discover** and select the index `metrics-*`, or even more specific, `metrics-kubernetes.*`. If you can’t see these indexes, [create a data view](/explore-analyze/find-and-organize/data-views.md) for them.
4. To view predefined dashboards, either select **Analytics→Dashboard** or [install assets through an integration](/reference/ingestion-tools/fleet/view-integration-assets.md).


