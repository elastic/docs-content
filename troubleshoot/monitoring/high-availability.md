---
navigation_title: "Cluster performance metrics"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-scenario_is_my_cluster_really_highly_available.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/echscenario_is_my_cluster_really_highly_available.html
---

# Troubleshoot cluster availability using performance metrics [ec-scenario_is_my_cluster_really_highly_available]

% TODO: Edit edit edit

You created a new {{ech}} deployment that uses three availability zones and index replicas, because you want to use the [cluster for production](/deploy-manage/production-guidance/plan-for-production-elastic-cloud.md#ec-ha). It’s a mission-critical deployment and you need it to be able to handle user requests at all times. Your cluster has been up and running for some time and it seems to handle its workload well. But is this cluster really highly available, given its current workload?

To answer this question, let’s take a look at CPU usage in the **Cluster Performance Metrics** section in the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body):

:::{image} /images/cloud-metrics-cpu.png
:alt: CPU usage over time
:::

Cluster performance metrics are shown per node and are color-coded to indicate which running {{es}} instance they belong to. In this case, you can notice that, from about 22:05 until just before 22:30, two out of three nodes are consistently close to maxing out their CPU resources at 100%. The third node seems to average somewhere under the 50% mark most of the time.

This CPU usage graph indicates that your cluster is load-balancing between the nodes in the different availability zones as designed, but the workload is too high to be able to handle the loss of an availability zone. For a cluster to be able to handle the failure of a node, it should be considered at capacity when it uses 50% of its resources. In this case, two of the nodes are already maxed out and the third one is around 50%. If any one of the three nodes were to fail, the volume of user requests would overwhelm the remaining nodes. On smaller clusters up to and including 8 GB of RAM, CPU boosting can temporarily relieve some of the pressure, but you should not rely on this feature for high availability. On larger clusters, CPU boosting is not available.

Even if your cluster is performing well, you still need to make sure that there is sufficient spare capacity to deal with the outage of an entire availability zone. For this cluster to remain highly available at all times, you either need to increase its size or reduce its workload.
