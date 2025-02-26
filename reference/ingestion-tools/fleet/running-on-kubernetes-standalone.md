---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/running-on-kubernetes-standalone.html
---

# Run Elastic Agent Standalone on Kubernetes [running-on-kubernetes-standalone]

## What you need [_what_you_need_3]

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



### Step 1: Download the {{agent}} manifest [_step_1_download_the_agent_manifest_3]

::::{note}
You can find {{agent}} Docker images [here](https://www.docker.elastic.co/r/elastic-agent/elastic-agent).
::::


Download the manifest file:

```sh
curl -L -O https://raw.githubusercontent.com/elastic/elastic-agent/v9.0.0/deploy/kubernetes/elastic-agent-standalone-kubernetes.yaml
```

::::{note}
You might need to adjust [resource limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) of the {{agent}} container in the manifest. Container resource usage depends on the number of data streams and the environment size.
::::


This manifest includes the Kubernetes integration to collect Kubernetes metrics and System integration to collect system level metrics and logs from nodes.

The {{agent}} is deployed as a [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/) to ensure that there is a running instance on each node of the cluster. These instances are used to retrieve most metrics from the host, such as system metrics, Docker stats, and metrics from all the services running on top of Kubernetes. These metrics are accessed through the deployed `kube-state-metrics`. Notice that everything is deployed under the `kube-system` namespace by default. To change the namespace, modify the manifest file.

Moreover, one of the Pods in the DaemonSet will constantly hold a *leader lock* which makes it responsible for handling cluster-wide monitoring. You can find more information about leader election configuration options at [leader election provider](/reference/ingestion-tools/fleet/kubernetes_leaderelection-provider.md). The leader pod will retrieve metrics that are unique for the whole cluster, such as Kubernetes events or [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics). We make sure that these metrics are retrieved from the leader pod by applying the following [condition](/reference/ingestion-tools/fleet/elastic-agent-kubernetes-autodiscovery.md) in the manifest, before declaring the data streams with these metricsets:

```yaml
...
inputs:
  - id: kubernetes-cluster-metrics
    condition: ${kubernetes_leaderelection.leader} == true
    type: kubernetes/metrics
    # metricsets with the state_ prefix and the metricset event
...
```

For Kubernetes Security Posture Management (KSPM) purposes, the {{agent}} requires read access to various types of Kubernetes resources, node processes, and files. To achieve this, read permissions are granted to the {{agent}} for the necessary resources, and volumes from the hosting node’s file system are mounted to allow accessibility to the {{agent}} pods.

::::{tip}
The size and the number of nodes in a Kubernetes cluster can be large at times, and in such a case the Pod that will be collecting cluster level metrics might require more runtime resources than you would like to dedicate to all of the pods in the DaemonSet. The leader which is collecting the cluster wide metrics may face performance issues due to resource limitations if under-resourced. In this case users might consider avoiding the use of a single DaemonSet with the leader election strategy and instead run a dedicated standalone {{agent}} instance for collecting cluster wide metrics using a Deployment in addition to the DaemonSet to collect metrics for each node. Then both the Deployment and the DaemonSet can be resourced independently and appropriately. For more information check the [Scaling {{agent}} on {{k8s}}](/reference/ingestion-tools/fleet/scaling-on-kubernetes.md) page.
::::



### Step 2: Connect to the {{stack}} [_step_2_connect_to_the_stack]

Set the {{es}} settings before deploying the manifest:

```yaml
- name: ES_USERNAME
  value: "elastic" <1>
- name: ES_PASSWORD
  value: "passpassMyStr0ngP@ss" <2>
- name: ES_HOST
  value: "https://somesuperhostiduuid.europe-west1.gcp.cloud.es.io:9243" <3>
```

1. The basic authentication username used to connect to {{es}}.
2. The basic authentication password used to connect to {{kib}}.
3. The {{es}} host to communicate with.


Refer to [Environment variables](/reference/ingestion-tools/fleet/agent-environment-variables.md) for all available options.


### Step 3: Configure tolerations [_step_3_configure_tolerations]

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


### Step 4: Deploy the {{agent}} [_step_4_deploy_the_agent]

To deploy {{agent}} to Kubernetes, run:

```sh
kubectl create -f elastic-agent-standalone-kubernetes.yaml
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



### Step 5: View your data in {{kib}} [_step_5_view_your_data_in_kib_2]

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

2. You can see data flowing in by going to **Analytics → Discover** and selecting the index `metrics-*`, or even more specific, `metrics-kubernetes.*`. If you can’t see these indexes, [create a data view](/explore-analyze/find-and-organize/data-views.md) for them.
3. You can see predefined dashboards by selecting **Analytics→Dashboard**, or by [installing assets through an integration](/reference/ingestion-tools/fleet/view-integration-assets.md).


## Red Hat OpenShift configuration [_red_hat_openshift_configuration]

If you are using Red Hat OpenShift, you need to specify additional settings in the manifest file and enable the container to run as privileged.

1. In the manifest file, modify the `agent-node-datastreams` ConfigMap and adjust inputs:

    * `kubernetes-cluster-metrics` input:

        * If `https` is used to access `kube-state-metrics`, add the following settings to all `kubernetes.state_*` datasets:

            ```yaml
              bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
              ssl.certificate_authorities:
                - /var/run/secrets/kubernetes.io/serviceaccount/service-ca.crt
            ```

    * `kubernetes-node-metrics` input:

        * Change the `kubernetes.controllermanager` data stream condition to:

            ```yaml
            condition: ${kubernetes.labels.app} == 'kube-controller-manager'
            ```

        * Change the `kubernetes.scheduler` data stream condition to:

            ```yaml
            condition: ${kubernetes.labels.app} == 'openshift-kube-scheduler'
            ```

        * The `kubernetes.proxy` data stream configuration should look like:

            ```yaml
            - data_stream:
                dataset: kubernetes.proxy
                type: metrics
              metricsets:
                - proxy
              hosts:
                - 'localhost:29101'
              period: 10s
            ```

        * Add the following settings to all data streams that connect to `https://${env.NODE_NAME}:10250`:

            ```yaml
              bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
              ssl.certificate_authorities:
                - /path/to/ca-bundle.crt
            ```

            ::::{note}
            `ca-bundle.crt` can be any CA bundle that contains the issuer of the certificate used in the Kubelet API. According to each specific installation of OpenShift this can be found either in `secrets` or in `configmaps`. In some installations it can be available as part of the service account secret, in `/var/run/secrets/kubernetes.io/serviceaccount/service-ca.crt`. When using the [OpenShift installer](https://github.com/openshift/installer/blob/master/docs/user/gcp/install.md) for GCP, mount the following `configmap` in the elastic-agent pod and use `ca-bundle.crt` in `ssl.certificate_authorities`:
            ::::


            ```shell
            Name:         kubelet-serving-ca
            Namespace:    openshift-kube-apiserver
            Labels:       <none>
            Annotations:  <none>

            Data
            ====
            ca-bundle.crt:
            ```

2. Grant the `elastic-agent` service account access to the privileged SCC:

    ```shell
    oc adm policy add-scc-to-user privileged system:serviceaccount:kube-system:elastic-agent
    ```

    This command enables the container to be privileged as an administrator for OpenShift.

3. If the namespace where elastic-agent is running has the `"openshift.io/node-selector"` annotation set, elastic-agent might not run on all nodes. In this case consider overriding the node selector for the namespace to allow scheduling on any node:

    ```shell
    oc patch namespace kube-system -p \
    '{"metadata": {"annotations": {"openshift.io/node-selector": ""}}}'
    ```

    This command sets the node selector for the project to an empty string.



### Autodiscover targeted Pods [_autodiscover_targeted_pods]

Refer to [Kubernetes autodiscovery with {{agent}}](/reference/ingestion-tools/fleet/elastic-agent-kubernetes-autodiscovery.md) for more information.


