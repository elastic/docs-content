---
navigation_title: "Node moves and outages"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-deployment-node-move.html
---

# Troubleshoot node moves and outages [ec-deployment-node-move]

To ensure that your nodes are located on healthy hosts, we vacate nodes to perform routine system maintenance or to remove a host with hardware issues from service.

All major scheduled maintenance and incidents can be found on the Elastic [status page](https://status.elastic.co/). You can subscribe to that page to be notified about updates.

If events on your deployment don’t correlate to any items listed on the status page, the events are due to minor routine maintenance performed on only a subset of {{ech}} deployments.

**What is the impact?**

During the routine system maintenance, having replicas and multiple availability zones ensures minimal interruption to your service. When nodes are vacated, as long as you have high availability, all search and indexing requests are expected to work within the reduced capacity until the node is back to normal.

**How can I be notified when a node is changed?**

To receive an email when nodes are added or removed from your deployment:

1. Follow the first five steps in [Getting notified about deployment health issues](../../deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md).
2. At Step 6, to choose the alert type for when a node is changed, select **CLUSTER HEALTH** → **Nodes changed** → **Edit alert**.

::::{note}
If you have only one master node in your cluster, during the master node vacate no notification will be sent. Kibana needs to communicate with the master node in order to send a notification. One way to avoid this is by shipping your deployment metrics to a dedicated monitoring cluster, which you can configure in Step 2 of [Getting notified about deployment health issues](../../deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md) when you enable logging and monitoring.
::::



## Node host outages [ec-node-host-outages]

If a node’s host experiences an outage, the system automatically vacates the node and displays a related `Don't attempt to gracefully move shards` message on the [**Activity**](../../deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md) page. Since the node is unavailable, the system skips checks that ensure the node’s shards have been moved before shutting down the node.

Unless overridden or unable, the system will automatically recover the vacated node’s data from replicas or snapshots. If your cluster has high availability, all search and indexing requests should work within the reduced capacity until the node is back to normal.
