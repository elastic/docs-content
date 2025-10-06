---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-planning.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Plan for production

{{ecloud}} Hosted supports a wide range of configurations. With such flexibility comes great freedom, but also the first rule of deployment planning: Your deployment needs to be matched to the workloads that you plan to run on your {{es}} clusters and {{kib}} instances. Specifically, this means two things:
* [Does your data need to be highly available?](elastic-cloud-hosted-planning.md#ec-ha)
* [Do you know when to scale?](elastic-cloud-hosted-planning.md#ec-workloads)

## Does your data need to be highly available? [ec-ha]

With {{ecloud}}, your deployment can be spread across as many as three separate availability zones, each hosted in its own, separate data center. Why this matters:

 * Data centers can have issues with availability. Internet outages, earthquakes, floods, or other events could affect the availability of a single data center. With a single availability zone, you have a single point of failure that can bring down your deployment.
 * Multiple availability zones help your deployment remain available. This includes your {{es}} cluster, provided that your cluster is sized so that it can sustain your workload on the remaining data centers and that your indices are configured to have at least one replica.
 * Multiple availability zones enable you to perform changes to resize your deployment with zero downtime.

We recommend that you use at least two availability zones for production and three for mission-critical systems. Just one zone might be sufficient, if your {{es}} cluster is mainly used for testing or development and downtime is acceptable, but should never be used for production.

:::{admonition} Make sure a single zone can serve your whole workload
Increasing the number of zones should not be used to add more resources. The concept of zones is meant for High Availability (2 zones) and Fault Tolerance (3 zones), but neither will work if the cluster relies on the resources from those zones to be operational.
:::

With multiple {{es}} nodes in multiple availability zones you have the recommended hardware. The next step is to ensure proper index replication. Each index, with the exception of searchable snapshot indices, should have one or more replicas. Use the [index settings API](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-indices-get-settings-1) to find any indices without replicas:

```sh
GET _all/_settings/index.number_of_replicas
```

Moreover, a high availability (HA) cluster requires at least three master-eligible nodes. For clusters that have fewer than six {{es}} nodes, any data node in the hot tier will also be a master-eligible node. You can achieve this by having hot nodes (serving as both data and master-eligible nodes) in three availability zones, or by having data nodes in two zones and a tiebreaker (will be automatically added if you choose two zones). For clusters that have six {{es}} nodes and beyond, dedicated master-eligible nodes are introduced. When your cluster grows, consider separating dedicated master-eligible nodes from dedicated data nodes. We recommend using at least 4GB RAM for dedicated master nodes.

The data in your {{es}} clusters is also backed up every 30 minutes, 4 hours, or 24 hours, depending on which snapshot interval you choose. These regular intervals provide an extra level of redundancy. We do support [snapshot and restore](/deploy-manage/tools/snapshot-and-restore.md), regardless of whether you use one, two, or three availability zones. However, with only a single availability zone and in the event of an outage, it might take a while for your cluster come back online. Using a single availability zone also leaves your cluster exposed to the risk of data loss, if the backups you need are not useable (failed or partial snapshots missing the indices to restore) or no longer available by the time that you realize that you might need the data (snapshots have a retention policy).

::::{warning}
Clusters that use only one availability zone are not highly
available and are at risk of data loss. To safeguard against data loss,
you must use at least two availability zones.
::::


::::{warning}
Indices with no replica, except for searchable snapshot indices,
are not highly available. You should use replicas to mitigate against
possible data loss.
::::


::::{warning}
Clusters that only have one master node are not highly available and are at risk of data loss. You must have three master-eligible nodes.
::::

## Do you know when to scale? [ec-workloads]

Knowing how to scale your deployment is critical, especially when unexpected workloads hits. Don't forget to [check your performance metrics](../../monitor/access-performance-metrics-on-elastic-cloud.md) to make sure your deployments are healthy and can cope with your workloads.

Scaling with {{ecloud}} is easy: 

* Turn on [deployment autoscaling](/deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md) to let {{ecloud}} manage your deployments by adjusting their available resources automatically.
* Or, if you prefer manual control, log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), select your deployment, select *Edit*, and either increase the number of zones or the size per zone.

The recommendation is to scale up the resources within a single zone until the cluster can take the full load (add some buffer to be prepared for a peak of requests), then scale out by adding additional zones depending on your requirements: two zones for High Availability, three zones for Fault Tolerance. 

## Minimum size recommendations for production use [ec-minimum-recommendations]

To ensure optimal performance and cluster stability in your production environment, we recommend adhering to the following minimum size guidelines. Deviating from these recommendations may lead to performance issues and cluster instability. For an enhanced user experience, consider planning your deployment capacity above these minimum recommendations, and adjust sizing based on your specific use case.

* **{{es}} nodes / instances**: For production systems, we recommend that each {{es}} node / instance in your cluster has at least 4 GB of RAM.
* **Clusters with logs and monitoring enabled**: Enabling logs and monitoring requires additional resources. For production systems with these features enabled, we recommend allocating at least 4 GB of RAM per {{es}} node / instance.
* **Clusters with dedicated master nodes**: For clusters with dedicated master nodes, we advise using at least 4 GB of RAM for each dedicated master node.

