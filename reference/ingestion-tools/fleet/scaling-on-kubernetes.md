---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/scaling-on-kubernetes.html
---

# Scaling Elastic Agent on Kubernetes [scaling-on-kubernetes]

For more information on how to deploy {{agent}} on {{k8s}}, please review these pages:

* [Run {{agent}} on Kubernetes managed by {{fleet}}](/reference/ingestion-tools/fleet/running-on-kubernetes-managed-by-fleet.md).
* [Run {{agent}} Standalone on Kubernetes](/reference/ingestion-tools/fleet/running-on-kubernetes-standalone.md).


### Observability at scale [_observability_at_scale]

This document summarizes some key factors and best practices for using [Elastic {{observability}}](/solutions/observability/get-started/quickstart-monitor-kubernetes-cluster-with-elastic-agent.md) to monitor {{k8s}} infrastructure at scale. Users need to consider different parameters and adjust {{stack}} accordingly. These elements are affected as the size of {{k8s}} cluster increases:

* The amount of metrics being collected from several {{k8s}} endpoints
* The {{agent}}'s resources to cope with the high CPU and Memory needs for the internal processing
* The {{es}} resources needed due to the higher rate of metric ingestion
* The Dashboard’s visualizations response times as more data are requested on a given time window

The document is divided in two main sections:

* [Configuration Best Practices](#configuration-practices)
* [Validation and Troubleshooting practices](#validation-and-troubleshooting-practices)


### Configuration best practices [configuration-practices]


#### Configure agent resources [_configure_agent_resources]

The {{k8s}} {{observability}} is based on [Elastic {{k8s}} integration](integration-docs://docs/reference/kubernetes.md), which collects metrics from several components:

* **Per node:**

    * kubelet
    * controller-manager
    * scheduler
    * proxy

* **Cluster wide (such as unique metrics for the whole cluster):**

    * kube-state-metrics
    * apiserver


Controller manager and Scheduler datastreams are being enabled only on the specific node that actually runs based on autodiscovery rules

The default manifest provided deploys {{agent}} as DaemonSet which results in an {{agent}} being deployed on every node of the {{k8s}} cluster.

Additionally, by default one agent is elected as **leader** (for more information visit [Kubernetes LeaderElection Provider](/reference/ingestion-tools/fleet/kubernetes_leaderelection-provider.md)). The {{agent}} Pod which holds the leadership lock is responsible for collecting the cluster-wide metrics in addition to its node’s metrics.

:::{image} images/k8sscaling.png
:alt: {{agent}} as daemonset
:class: screenshot
:::

The above schema explains how {{agent}} collects and sends metrics to {{es}}. Because of Leader Agent being responsible to also collecting cluster-lever metrics, this means that it requires additional resources.

The DaemonSet deployment approach with leader election simplifies the installation of the {{agent}} because we define less {{k8s}} Resources in our manifest and we only need one single Agent policy for our Agents. Hence it is the default supported method for [Managed {{agent}} installation](/reference/ingestion-tools/fleet/running-on-kubernetes-managed-by-fleet.md)


#### Specifying resources and limits in agent manifests [_specifying_resources_and_limits_in_agent_manifests]

Resourcing of your Pods and the Scheduling priority (check section [Scheduling priority](#agent-scheduling)) of them are two topics that might be affected as the {{k8s}} cluster size increases. The increasing demand of resources might result to under-resource the Elastic Agents of your cluster.

Based on our tests we advise to configure only the `limit` section of the `resources` section in the manifest. In this way the `request`'s settings of the `resources` will fall back to the `limits` specified. The `limits` is the upper bound limit of your microservice process, meaning that can operate in less resources and protect {{k8s}} to assign bigger usage and protect from possible resource exhaustion.

```yaml
resources:
    limits:
      cpu: "1500m"
      memory: "800Mi"
```

Based on our [{{agent}} Scaling tests](https://github.com/elastic/elastic-agent/blob/main/docs/elastic-agent-scaling-tests.md), the following table provides guidelines to adjust {{agent}} limits on different {{k8s}} sizes:

Sample Elastic Agent Configurations:

|     |     |     |
| --- | --- | --- |
| No of Pods in K8s Cluster | Leader Agent Resources | Rest of Agents |
| 1000 | cpu: "1500m",  memory: "800Mi" | cpu: "300m",  memory: "600Mi" |
| 3000 | cpu: "2000m",  memory: "1500Mi" | cpu: "400m",  memory: "800Mi" |
| 5000 | cpu: "3000m",  memory: "2500Mi" | cpu: "500m",  memory: "900Mi" |
| 10000 | cpu: "3000m",  memory: "3600Mi" | cpu: "700m",  memory: "1000Mi" |

The above tests were performed with Elastic Agent version 8.7 and scraping period of `10sec` (period setting for the Kubernetes integration). Those numbers are just indicators and should be validated for each different Kubernetes environment and amount of workloads.

#### Proposed agent installations for large scale [_proposed_agent_installations_for_large_scale]

Although daemonset installation is simple, it can not accommodate the varying agent resource requirements depending on the collected metrics. The need for appropriate resource assignment at large scale requires more granular installation methods.

{{agent}} deployment is broken in groups as follows:

* A dedicated {{agent}} deployment of a single Agent for collecting cluster wide metrics from the apiserver
* Node level {{agent}}s(no leader Agent) in a Daemonset
* kube-state-metrics shards and {{agent}}s in the StatefulSet defined in the kube-state-metrics autosharding manifest

Each of these groups of {{agent}}s will have its own policy specific to its function and can be resourced independently in the appropriate manifest to accommodate its specific resource requirements.

Resource assignment led us to alternatives installation methods.

::::{important}
The main suggestion for big scale clusters **is to install {{agent}} as side container along with `kube-state-metrics` Shard**. The installation is explained in details [{{agent}} with Kustomize in Autosharding](https://github.com/elastic/elastic-agent/tree/main/deploy/kubernetes#kube-state-metrics-ksm-in-autosharding-configuration)
::::


The following **alternative configuration methods** have been verified:

1. With `hostNetwork:false`

    * {{agent}} as Side Container within KSM Shard pod
    * For non-leader {{agent}} deployments that collect per KSM shards

2. With `taint/tolerations` to isolate the {{agent}} daemonset pods from rest of deployments

You can find more information in the document called [{{agent}} Manifests in order to support Kube-State-Metrics Sharding](https://github.com/elastic/elastic-agent/blob/main/docs/elastic-agent-ksm-sharding.md).

Based on our [{{agent}} scaling tests](https://github.com/elastic/elastic-agent/blob/main/docs/elastic-agent-scaling-tests.md), the following table aims to assist users on how to configure their KSM Sharding as {{k8s}} cluster scales:

|     |     |     |
| --- | --- | --- |
| No of Pods in K8s Cluster | No of KSM Shards | Agent Resources |
| 1000 | No Sharding can be handled with default KSM config | limits: memory: 700Mi , cpu:500m |
| 3000 | 4 Shards | limits: memory: 1400Mi , cpu:1500m |
| 5000 | 6 Shards | limits: memory: 1400Mi , cpu:1500m |
| 10000 | 8 Shards | limits: memory: 1400Mi , cpu:1500m |

The tests above were performed with Elastic Agent version 8.8 + TSDB Enabled and scraping period of `10sec` (for the Kubernetes integration). Those numbers are just indicators and should be validated per different Kubernetes policy configuration, along with applications that the Kubernetes cluster might include

::::{note}
Tests have run until 10K pods per cluster. Scaling to bigger number of pods might require additional configuration from {{k8s}} Side and Cloud Providers but the basic idea of installing {{agent}} while horizontally scaling KSM remains the same.
::::



#### Agent scheduling [agent-scheduling]

Setting the low priority to {{agent}} comparing to other pods might also result to {{agent}} being in Pending State.The scheduler tries to preempt (evict) lower priority Pods to make scheduling of the higher pending Pods possible.

Trying to prioritise the agent installation before rest of application microservices, [PriorityClasses suggested](https://github.com/elastic/elastic-agent/blob/main/docs/manifests/elastic-agent-managed-gke-autopilot.yaml#L8-L16)


#### {{k8s}} Package configuration [_k8s_package_configuration]

Policy configuration of {{k8s}} package can heavily affect the amount of metrics collected and finally ingested. Factors that should be considered in order to make your collection and ingestion lighter:

* Scraping period of {{k8s}} endpoints
* Disabling log collection
* Keep audit logs disabled
* Disable events dataset
* Disable {{k8s}} control plane datasets in Cloud managed {{k8s}} instances (see more info ** [Run {{agent}} on GKE managed by {{fleet}}](/reference/ingestion-tools/fleet/running-on-gke-managed-by-fleet.md), [Run {{agent}} on Amazon EKS managed by {{fleet}}](/reference/ingestion-tools/fleet/running-on-eks-managed-by-fleet.md), [Run {{agent}} on Azure AKS managed by {{fleet}}](/reference/ingestion-tools/fleet/running-on-aks-managed-by-fleet.md) pages)


#### Dashboards and visualisations [_dashboards_and_visualisations]

The [Dashboard Guidelines](https://github.com/elastic/integrations/blob/main/docs/dashboard_guidelines.md) document provides guidance on how to implement your dashboards and is constantly updated to track the needs of Observability at scale.

User experience regarding Dashboard responses, is also affected from the size of data being requested. As dashboards can contain multiple visualisations, the general consideration is to split visualisations and group them according to the frequency of access. The less number of visualisations tends to improve user experience.


#### Disabling indexing host.ip and host.mac fields [_disabling_indexing_host_ip_and_host_mac_fields]

A new environemntal variable `ELASTIC_NETINFO: false` has been introduced to globally disable the indexing of `host.ip` and `host.mac` fields in your {{k8s}} integration. For more information see [Environment variables](/reference/ingestion-tools/fleet/agent-environment-variables.md).

Setting this to `false` is recommended for large scale setups where the `host.ip` and `host.mac` fields' index size increases. The number of IPs and MAC addresses reported increases significantly as a Kubenetes cluster grows. This leads to considerably increased indexing time, as well as the need for extra storage and additional overhead for visualization rendering.


#### Elastic Stack configuration [_elastic_stack_configuration]

The configuration of Elastic Stack needs to be taken under consideration in large scale deployments. In case of Elastic Cloud deployments the choice of the deployment [{{ecloud}} hardware profile](/deploy-manage/deploy/elastic-cloud/ec-customize-deployment-components.md) is important.

For heavy processing and big ingestion rate needs, the `CPU-optimised` profile is proposed.


### Validation and troubleshooting practices [validation-and-troubleshooting-practices]


#### Define if agents are collecting as expected [_define_if_agents_are_collecting_as_expected]

After {{agent}} deployment, we need to verify that Agent services are healthy, not restarting (stability) and that collection of metrics continues with expected rate (latency).

**For stability:**

If {{agent}} is configured as managed, in {{kib}} you can observe under **Fleet>Agents**

:::{image} images/kibana-fleet-agents.png
:alt: {{agent}} Status
:class: screenshot
:::

Additionally you can verify the process status with following commands:

```bash
kubectl get pods -A | grep elastic
kube-system   elastic-agent-ltzkf                        1/1     Running   0          25h
kube-system   elastic-agent-qw6f4                        1/1     Running   0          25h
kube-system   elastic-agent-wvmpj                        1/1     Running   0          25h
```

Find leader agent:

```bash
❯ k get leases -n kube-system | grep elastic
NAME                                      HOLDER                                                                       AGE
elastic-agent-cluster-leader   elastic-agent-leader-elastic-agent-qw6f4                                     25h
```

Exec into Leader agent and verify the process status:

```bash
❯ kubectl exec -ti -n kube-system elastic-agent-qw6f4 -- bash
root@gke-gke-scaling-gizas-te-default-pool-6689889a-sz02:/usr/share/elastic-agent# ./elastic-agent status
State: HEALTHY
Message: Running
Fleet State: HEALTHY
Fleet Message: (no message)
Components:
  * kubernetes/metrics  (HEALTHY)
                        Healthy: communicating with pid '42423'
  * filestream          (HEALTHY)
                        Healthy: communicating with pid '42431'
  * filestream          (HEALTHY)
                        Healthy: communicating with pid '42443'
  * beat/metrics        (HEALTHY)
                        Healthy: communicating with pid '42453'
  * http/metrics        (HEALTHY)
                        Healthy: communicating with pid '42462'
```

It is a common problem of lack of CPU/memory resources that agent process restart as {{k8s}} size grows. In the logs of agent you

```json
kubectl logs -n kube-system elastic-agent-qw6f4 | grep "kubernetes/metrics"
[ouptut truncated ...]

(HEALTHY->STOPPED): Suppressing FAILED state due to restart for '46554' exited with code '-1'","log":{"source":"elastic-agent"},"component":{"id":"kubernetes/metrics-default","state":"STOPPED"},"unit":{"id":"kubernetes/metrics-default-kubernetes/metrics-kube-state-metrics-c6180794-70ce-4c0d-b775-b251571b6d78","type":"input","state":"STOPPED","old_state":"HEALTHY"},"ecs.version":"1.6.0"}
{"log.level":"info","@timestamp":"2023-04-03T09:33:38.919Z","log.origin":{"file.name":"coordinator/coordinator.go","file.line":861},"message":"Unit state changed kubernetes/metrics-default-kubernetes/metrics-kube-apiserver-c6180794-70ce-4c0d-b775-b251571b6d78 (HEALTHY->STOPPED): Suppressing FAILED state due to restart for '46554' exited with code '-1'","log":{"source":"elastic-agent"}
```

You can verify the instant resource consumption by running `top pod` command and identify if agents are close to the limits you have specified in your manifest.

```bash
kubectl top pod  -n kube-system | grep elastic
NAME                                                             CPU(cores)   MEMORY(bytes)
elastic-agent-ltzkf                                              30m          354Mi
elastic-agent-qw6f4                                              67m          467Mi
elastic-agent-wvmpj                                              27m          357Mi
```


#### Verify ingestion latency [_verify_ingestion_latency]

{{kib}} Discovery can be used to identify frequency of your metrics being ingested.

Filter for Pod dataset:

:::{image} images/pod-latency.png
:alt: {{k8s}} Pod Metricset
:class: screenshot
:::

Filter for State_Pod dataset

:::{image} images/state-pod.png
:alt: {{k8s}} State Pod Metricset
:class: screenshot
:::

Identify how many events have been sent to {{es}}:

```bash
kubectl logs -n kube-system elastic-agent-h24hh -f | grep -i state_pod
[ouptut truncated ...]

"state_pod":{"events":2936,"success":2936}
```

The number of events denotes the number of documents that should be depicted inside {{kib}} Discovery page.

For example, in a cluster with 798 pods, then 798 docs should be depicted in block of ingestion inside {{kib}}.

#### Define if {{es}} is the bottleneck of ingestion [_define_if_es_is_the_bottleneck_of_ingestion]

In some cases maybe the {{es}} can not cope with the rate of data that are trying to be ingested. In order to verify the resource utilisation, installation of an [{{stack}} monitoring cluster](/deploy-manage/monitor/stack-monitoring.md) is advised.

Additionally, in {{ecloud}} deployments you can navigate to **Manage Deployment > Deployments > Monitoring > Performance**. Corresponding dashboards for `CPU Usage`, `Index Response Times` and `Memory Pressure` can reveal possible problems and suggest vertical scaling of {{stack}} resources.

## Relevant links [_relevant_links]

* [Monitor {{k8s}} Infrastructure](/solutions/observability/get-started/quickstart-monitor-kubernetes-cluster-with-elastic-agent.md)
* [Blog: Managing your {{k8s}} cluster with Elastic {{observability}}](https://www.elastic.co/blog/kubernetes-cluster-metrics-logs-monitoring)
