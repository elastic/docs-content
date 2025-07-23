---
navigation_title: Node moves and system maintenance
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-deployment-node-move.html
applies_to:
  deployment:
    ess: all
products:
  - id: cloud-hosted
---

# Understanding node moves and system maintenance [node-moves-system-maintenance]

To ensure that your deployment nodes are located on healthy hosts, Elastic vacates nodes to perform essential system maintenance or to remove a host with hardware issues from service. These tasks cannot be skipped or delayed.

You can subscribe to the [status page](https://status.elastic.co/) to be notified about planned maintenance or actions that have been taken to respond to incidents.

If events on your deployment don’t correlate to any items listed on the status page, the events are due to minor essential maintenance performed on only a subset of {{ech}} deployments.

When {{ech}} undergoes system maintenance, the following message appears on the [activity page](../../deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md):

```sh
Move nodes off of allocator [allocator_id] due to essential system maintenance.
```

This page explains the causes and impact of node moves and system maintenance, and how to mitigate any possible risks to your deployment.

::::{note}
You can also [configure email notifications](#configure-email-notification) to be alerted when this situation occurs.
::::

## Possible causes [possible-cause]

Potential causes of system maintenance include, but not limited to, situations like the following:

* A host where the Cloud Service Provider (CSP), like AWS, GCP, or Azure, has reported upcoming hardware deprecation or identified issues requiring remediation.
* Abrupt host termination by the CSP due to underlying infrastructure problems.
* Mandatory host operating system (OS) patching or upgrades for security or compliance reasons.
* Other scheduled maintenance announced on the [Elastic status page](https://status.elastic.co/).

## Behavior difference [behavior-difference]

Depending on the cause, the maintenance behaviors may differ.

* During planned operations, such as hardware upgrades or host patches, the system attempts to gracefully move the node to another host before shutting down the original one. This process allows shard relocation to complete ahead of time, minimizing any potential disruption.

* If a node’s host experiences an unexpected outage, the system automatically vacates the node and displays a related `Don't attempt to gracefully move shards` message on the [activity page](../../deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md), skipping the check to ensure the node’s shards have been moved before shutdown.

## Impact and mitigation [impact-mitigation]

The following sections describe how your deployment behaves during maintenance, and how to reduce risks of data loss.

### Service availability

The system will automatically try to recover the vacated node’s data from replicas or snapshots. If your cluster has [high availability (HA)](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md#ec-ha) configured, all search and indexing requests should continue to work within the reduced capacity until the node is replaced.

Overall, having replicas and multiple availability zones helps minimize service interruption.

### Data resiliency 

The system maintenance process always attempts to recover the vacated node's data from replicas or snapshots. However, if the deployment is not configured with high availability, the maintenance process might not be able to recover the data from the vacated node.

Configuring multiple availability zones helps your deployment remain available for indexing and search requests if one zone becomes unavailable. However, this alone does not guarantee data availability. If an index has no replica shards and its primary shard is located on a node that must be vacated, data loss might occur if the system is unable to move the node gracefully during the maintenance activity.

To minimize this risk and keep your data accessible, ensure that your deployment follows [high availability best practices](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md#ec-ha):
- Use at least two availability zones for production systems, and three for mission-critical systems.
- Configure one or more [replica shards](/deploy-manage/distributed-architecture/clusters-nodes-shards.md) for each index, except for searchable snapshot indices.

As long as these recommendations are followed, system maintenance processes should not impact the availability of the data in the deployment.

### Performance stability

The performance impact of system maintenance depends on how well the deployment is sized. Well-provisioned deployments with sufficient buffer capacity typically remain unaffected, while deployments already operating near their limits might experience slowdowns, or even intermittent request failures, during node vacating.

High availability assumes not just redundancy in data and zones, but also the ability to absorb the loss or restart of a node without service disruption. To learn more, refer to [Plan for production](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md#ec-ha).

At a minimum, you should size your deployment to tolerate the temporary loss of one node in order to avoid single points of failure and ensure proper HA. For critical systems, ensure that the deployment can continue operating even in the event of losing an entire availability zone.

::::{admonition} Availability zones and sizing recommendations
Increasing the number of zones should not be used to add more resources. The concept of zones is meant for high availability (two zones) and fault tolerance (three zones), but neither will work if the cluster relies on the resources from those zones to be operational.

You should scale up the resources within a single zone until the cluster can take the full load, adding some buffer to be prepared for a peak of requests. You should then scale out by adding additional zones depending on your requirements: two zones for high availability, three zones for fault tolerance.
::::


## Configure email notifications [configure-email-notification]

You can configure email alerts for system maintenance by following these steps: 

1. Enable [Stack monitoring](/deploy-manage/monitor/stack-monitoring/ece-ech-stack-monitoring.md#enable-logging-and-monitoring-steps) (logs and metrics) on your deployment. Only metrics collection is required for these notifications to work.

2. In the deployment used as the destination of Stack monitoring:

  * Create [Stack monitoring default rules](/deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md#_create_default_rules).

  * (Optional) Configure an email [connector](kibana://reference/connectors-kibana/email-action-type.md). If you prefer, use the preconfigured `Elastic-Cloud-SMTP` email connector.

  * Edit the rule  **Cluster alerting** > **{{es}} nodes changed** and select the email connector.

::::{note}
If you have only one master node in your cluster, no notification will be sent during the master node vacate. {{kib}} needs to communicate with the master node in order to send a notification. You can avoid this by shipping your deployment metrics to a dedicated monitoring cluster when you enable logging and monitoring.
::::

