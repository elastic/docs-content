# Plan for production [ech-planning]

Elasticsearch Add-On for Heroku supports a wide range of configurations. With such flexibility comes great freedom, but also the first rule of deployment planning: Your deployment needs to be matched to the workloads that you plan to run on your {{es}} clusters and {{kib}} instances. Specifically, this means two things:

* [Does your data need to be highly available?](../../../deploy-manage/production-guidance/plan-for-production-elastic-cloud.md#ech-ha)
* [Do you know when to scale?](../../../deploy-manage/production-guidance/plan-for-production-elastic-cloud.md#ech-workloads)


## Does your data need to be highly available? [ech-ha] 

With Elasticsearch Add-On for Heroku, your deployment can be spread across as many as three separate availability zones, each hosted in its own, separate data center. Why this matters:

* Data centers can have issues with availability. Internet outages, earthquakes, floods, or other events could affect the availability of a single data center. With a single availability zone, you have a single point of failure that can bring down your deployment.
* Multiple availability zones help your deployment remain available. This includes your {{es}} cluster, provided that your cluster is sized so that it can sustain your workload on the remaining data centers and that your indices are configured to have at least one replica.
* Multiple availability zones enable you to perform changes to resize your deployment with zero downtime.

We recommend that you use at least two availability zones for production and three for mission-critical systems. Just one zone might be sufficient, if your {{es}} cluster is mainly used for testing or development and downtime is acceptable, but should never be used for production.

With multiple {{es}} nodes in multiple availability zones you have the recommended hardware, the next thing to consider is having the recommended index replication. Each index, with the exception of searchable snapshot indexes, should have one or more replicas. Use the index settings API to find any indices with no replica:

```sh
GET _all/_settings/index.number_of_replicas
```

Moreover, a high availability (HA) cluster requires at least three master-eligible nodes. For clusters that have fewer than six {{es}} nodes, any data node in the hot tier will also be a master-eligible node. So, this can be achieved by having hot nodes (serving as both data and master-eligible nodes) in three availability zones, or by having data nodes in two zones and a tiebreaker (will be automatically added if you choose two zones). For clusters that have six {{es}} nodes and beyond, dedicated master-eligible nodes are introduced. When your cluster grows, it becomes important to consider separating dedicated master-eligible nodes from dedicated data nodes.

The data in your {{es}} clusters is also backed up every 30 minutes, 4 hours, or 24 hours, depending on which snapshot interval you choose. These regular intervals provide an extra level of redundancy. We do support [snapshot and restore](../../../deploy-manage/tools/snapshot-and-restore.md), regardless of whether you use one, two, or three availability zones. However, with only a single availability zone and in the event of an outage, it might take a while for your cluster come back online. Using a single availability zone also leaves your cluster exposed to the risk of data loss, if the backups you need are not useable (failed or partial snapshots missing the indices to restore) or no longer available by the time that you realize that you might need the data (snapshots have a retention policy).

::::{warning} 
Clusters that use only one availability zone are not highly available and are at risk of data loss. To safeguard against data loss, you must use at least two availability zones.
::::


::::{warning} 
Indices with no replica, except for searchable snapshot indices, are not highly available. You should use replicas to mitigate against possible data loss.
::::


::::{warning} 
Clusters that only have one master node are not highly available and are at risk of data loss. You must have three master-eligible nodes.
::::



## Do you know when to scale? [ech-workloads] 

Knowing how to scale your deployment is critical, especially when unexpected workloads hits. Don’t forget to [check your performance metrics](/deploy-manage/monitor/monitoring-data/access-performance-metrics-on-elastic-cloud.md) to make sure your deployments are healthy and can cope with your workloads.

Scaling with Elasticsearch Add-On for Heroku is easy:

* Turn on [deployment autoscaling](../../../deploy-manage/autoscaling.md) to let Elasticsearch Add-On for Heroku manage your deployments by adjusting their available resources automatically.
* Or, if you prefer manual control, log in to the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body), select your deployment, select **Edit deployment** from the **Actions** dropdown, and either increase the number of zones or the size per zone.

Refer to [Sizing {{es}}: Scaling up and out](https://www.elastic.co/blog/found-sizing-elasticsearch) to identify which questions to ask yourself when determining which cluster size is the best fit for your {{es}} use case.

