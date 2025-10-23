---
navigation_title: Unavailable shards
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-scenario_why_are_shards_unavailable.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/echscenario_why_are_shards_unavailable.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-analyze_shards_with-api.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-analyze_shards_with-kibana.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-remediate-issues-allocation-explain-API.html
applies_to:
  deployment:
    ess: all
products:
  - id: cloud-hosted
---

# Diagnose unavailable shards [ec-scenario_why_are_shards_unavailable]

This section describes how to analyze unassigned shards using the Elasticsearch APIs and Kibana.

* [Analyze unassigned shards using the Elasticsearch API](/troubleshoot/monitoring/unavailable-shards.md#ec-analyze_shards_with-api)
* [Analyze unassigned shards using the Kibana UI](/troubleshoot/monitoring/unavailable-shards.md#ec-analyze_shards_with-kibana)
* [Remediate common issues returned by the cluster allocation explain API](#ec-remediate-issues-allocation-explain-API)

{{es}} distributes the documents in an index across multiple shards and distributes copies of those shards across multiple nodes in the cluster. This both increases capacity and makes the cluster more resilient, ensuring your data remains available if a node goes down.

A healthy (green) cluster has a primary copy of each shard and the required number of replicas are assigned to different nodes in the cluster.

If a cluster has unassigned replica shards, it is functional but vulnerable in the event of a failure. The cluster is unhealthy and reports a status of yellow.

If a cluster has unassigned primary shards, some of your data is unavailable. The cluster is unhealthy and reports a status of red.

A formerly-healthy cluster might have unassigned shards because nodes have dropped out or moved, are running out of disk space, or are hitting allocation limits.

If a cluster has unassigned shards, you might see an error message such as this on the Elastic Cloud console:

:::{image} /troubleshoot/images/cloud-ec-unhealthy-deployment.png
:alt: Unhealthy deployment error message
:::

If your issue is not addressed here, then [contact Elastic support for help](/troubleshoot/index.md).

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::

## Analyze unassigned shards using the {{es}} API [ec-analyze_shards_with-api]

You can retrieve information about the status of your cluster, indices, and shards using the {{es}} API. To access the API you can either use the [Kibana Dev Tools Console](/explore-analyze/query-filter/tools/console.md), or the [Elasticsearch API console](cloud://reference/cloud-hosted/ec-api-console.md). If you have your own way to run the {{es}} API, check [How to access the API](cloud://reference/cloud-hosted/ec-api-access.md). This section shows you how to:

* [Check cluster health](/troubleshoot/monitoring/unavailable-shards.md#ec-check-cluster-health)
* [Check unhealthy indices](/troubleshoot/monitoring/unavailable-shards.md#ec-check-unhealthy-indices)
* [Check which shards are unassigned](/troubleshoot/monitoring/unavailable-shards.md#ec-check-which-unassigned-shards)
* [Check why shards are unassigned](/troubleshoot/monitoring/unavailable-shards.md#ec-check-why-unassigned-shards)
* [Check Elasticsearch cluster logs](/troubleshoot/monitoring/unavailable-shards.md#ec-check-es-cluster-logs)


#### Check cluster health [ec-check-cluster-health]

Use the [Cluster health API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health):

```json
GET /_cluster/health/
```

This command returns the cluster status (green, yellow, or red) and shows the number of unassigned shards:

```json
{
  "cluster_name" : "xxx",
  "status" : "red",
  "timed_out" : false,
  "number_of_nodes" : "x",
  "number_of_data_nodes" : "x",
  "active_primary_shards" : 116,
  "active_shards" : 229,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 1,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_inflight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 98.70689655172413
}
```


#### Check unhealthy indices [ec-check-unhealthy-indices]

Use the [cat indices API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-indices) to get the status of individual indices. Specify the `health` parameter to limit the results to a particular status, for example `?v&health=red` or `?v&health=yellow`.

```json
GET /_cat/indices?v&health=red
```

This command returns any indices that have unassigned primary shards (red status):

```json
red   open    filebeat-7.10.0-2022.01.07-000014 C7N8fxGwRxK0JcwXH18zVg  1 1
red   open    filebeat-7.9.3-2022.01.07-000015  Ib4UIJNVTtOg6ovzs011Lq  1 1
```

For more information, refer to [Fix a red or yellow cluster status](/troubleshoot/elasticsearch/red-yellow-cluster-status.md#fix-red-yellow-cluster-status).


#### Check which shards are unassigned [ec-check-which-unassigned-shards]

Use the [cat shards API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-shards):

```json
GET /_cat/shards/?v
```

This command returns the index name, followed by the shard type and shard status:

```json
filebeat-7.10.0-2022.01.07-000014 0   P   UNASSIGNED
filebeat-7.9.3-2022.01.07-000015  1   P   UNASSIGNED
filebeat-7.9.3-2022.01.07-000015  2   r   UNASSIGNED
```


#### Check why shards are unassigned [ec-check-why-unassigned-shards]

To understand why shards are unassigned, run the [Cluster allocation explain API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-allocation-explain).

Running the API call `GET _cluster/allocation/explain` retrieves an allocation explanation for unassigned primary shards, or replica shards.

For example, if `_cat/health` shows that the primary shard of shard 1 in the `filebeat-7.9.3-2022.01.07-000015` index is unassigned, you can get the allocation explanation with the following request:

```json
GET _cluster/allocation/explain
{
  "index": "filebeat-7.9.3-2022.01.07-000015",
  "shard": 1,
  "primary": true
}
```

The response is as follows:

```json
{
  "index": "filebeat-7.9.3-2022.01.07-000015",
  "shard": 1,
  "primary": true,
  "current_state": "unassigned",
  "unassigned_info": {
    "reason": "CLUSTER_RECOVERED",
    "at": "2022-04-12T13:06:36.125Z",
    "last_allocation_status": "no_valid_shard_copy"
  },
  "can_allocate": "no_valid_shard_copy",
  "allocate_explanation": "cannot allocate because a previous copy of the primary shard existed but can no longer be found on the nodes in the cluster",
  "node_allocation_decisions": [
    {
      "node_id": "xxxx",
      "node_name": "instance-0000000005",
      (... skip ...)
      "node_decision": "no",
      "store": {
        "found": false
      }
    }
  ]
}
```


#### Check {{es}} cluster logs [ec-check-es-cluster-logs]

To determine the allocation issue, you can [check the logs](/deploy-manage/monitor.md#logging). This is easier if you have set up a dedicated monitoring deployment.


## Analyze unassigned shards using the Kibana UI [ec-analyze_shards_with-kibana]

If you are shipping logs and metrics to a monitoring deployment, go through the following steps.

1. Select your deployment from the {{es}} Service panel and navigate to the **Logs and metrics** page.
2. Click **Enable**.
3. Choose the deployment where to send your logs and metrics.
4. Click **Save**. It might take a few minutes to apply the configuration changes.
5. Click **View** to open the Kibana UI and get more details on metrics and logs.

:::{image} /troubleshoot/images/cloud-ec-logs-metrics-page.png
:alt: Log and metrics page
:::

The unhealthy indices appear with a red or yellow status.

:::{image} /troubleshoot/images/cloud-ec-red-yellow-indices.png
:alt: Unhealthy indices in red or yellow status
:::


## Remediate common issues returned by the cluster allocation explain API [ec-remediate-issues-allocation-explain-API]

Here’s how to resolve the most common causes of unassigned shards reported by the cluster allocation explain API.

* [Disk is full](/troubleshoot/monitoring/unavailable-shards.md#ec-disk-full)
* [A node containing data has moved to a different host](/troubleshoot/monitoring/unavailable-shards.md#ec-node-moved-to-another-host)
* [Unable to assign shards based on the allocation rule](/troubleshoot/monitoring/unavailable-shards.md#ec-cannot-assign-shards-on-allocation-rule)
* [The number of eligible data nodes is less than the number of replicas](/troubleshoot/monitoring/unavailable-shards.md#ec-eligible-data-nodes-less-than-replicas)
* [A snapshot issue prevents searchable snapshot indices from being allocated](/troubleshoot/monitoring/unavailable-shards.md#ec-searchable-snapshot-indices-not-allocated)
* [Maximum retry times exceeded](/troubleshoot/monitoring/unavailable-shards.md#ec-max-retry-exceeded)
* [Max shard per node reached the limit](/troubleshoot/monitoring/unavailable-shards.md#ec-max-shard-per-node)

If your issue is not addressed here, then [contact Elastic support for help](/troubleshoot/index.md).

### Disk is full [ec-disk-full]

**Symptom**

If the disk usage exceeded the threshold, you may get one or more of the following messages:

`the node is above the high watermark cluster setting [cluster.routing.allocation.disk.watermark.high=90%], using more disk space than the maximum allowed [90.0%], actual free: [9.273781776428223%]`

`unable to force allocate shard to [%s] during replacement, as allocating to this node would cause disk usage to exceed 100%% ([%s] bytes above available disk space)`

`the node is above the low watermark cluster setting [cluster.routing.allocation.disk.watermark.low=85%], using more disk space than the maximum allowed [85.0%], actual free: [14.119771122932434%]`

`after allocating [[restored-xxx][0], node[null], [P], recovery_source[snapshot recovery [Om66xSJqTw2raoNyKxsNWg] from xxx/W5Yea4QuR2yyZ4iM44fumg], s[UNASSIGNED], unassigned_info[[reason=NEW_INDEX_RESTORED], at[2022-03-02T10:56:58.210Z], delayed=false, details[restore_source[xxx]], allocation_status[fetching_shard_data]]] node [GTXrECDRRmGkkAnB48hPqw] would have more than the allowed 10% free disk threshold (8.7% free), preventing allocation`

**Resolutions**

Review the topic for your deployment architecture:

* [Full disk on single-node deployment](/troubleshoot/monitoring/unavailable-nodes.md#ec-single-node-deployment-disk-used)
* [Full disk on multiple-nodes deployment](/troubleshoot/monitoring/unavailable-nodes.md#ec-multiple-node-deployment-disk-used)

To learn more, review the following topics:

* [Cluster-level shard allocation and routing settings](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md)
* [Fix watermark errors](/troubleshoot/elasticsearch/fix-watermark-errors.md)


### A node containing data has moved to a different host [ec-node-moved-to-another-host]

**Symptom**

During the routine system maintenance performed by Elastic, it might happen that a node moves to a different host. If the indices are not configured with replica shards, the shard data on the {{es}} node that is moved will be lost, and you might get one or more of these messages:

`cannot allocate because a previous copy of the primary shard existed but can no longer be found on the nodes in the cluster`

**Resolutions**

Configure an [highly available cluster](/deploy-manage/production-guidance.md) to keep your service running. Also, consider taking the following actions to bring your deployment back to health and recover your data from the snapshot.

* [Close the red indices](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-close)
* [Restore the indices](/deploy-manage/tools/snapshot-and-restore.md) from the last successful snapshot

For more information, check also [Designing for resilience](/deploy-manage/production-guidance/availability-and-resilience.md).


### Unable to assign shards based on the allocation rule [ec-cannot-assign-shards-on-allocation-rule]

**Symptom**

When shards cannot be assigned, due to [data tier allocation](/manage-data/lifecycle/data-tiers.md#data-tier-allocation) or [attribute-based allocation](/deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md), you might get one or more of these messages:

`node does not match index setting [index.routing.allocation.include] filters [node_type:\"cold\"]`

`index has a preference for tiers [data_cold] and node does not meet the required [data_cold] tier`

`index has a preference for tiers [data_cold,data_warm,data_hot] and node does not meet the required [data_cold] tier`

`index has a preference for tiers [data_warm,data_hot] and node does not meet the required [data_warm] tier`

`this node's data roles are exactly [data_frozen] so it may only hold shards from frozen searchable snapshots, but this index is not a frozen searchable snapshot`

**Resolutions**

* Make sure nodes are available in each data tier and have sufficient disk space.
* [Check the index settings](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-indices) and ensure shards can be allocated to the expected data tier.
* Check the [ILM policy](/manage-data/lifecycle/index-lifecycle-management.md) and check for issues with the [allocate action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-allocate.md).
* Inspect the [index templates](/manage-data/data-store/templates.md) and check for issues with the index settings.


### The number of eligible data nodes is less than the number of replicas [ec-eligible-data-nodes-less-than-replicas]

**Symptom**

Unassigned replica shards are often caused by there being fewer eligible data nodes than the configured number_of_replicas.

**Resolutions**

* Add more [eligible data nodes or more availability zones](/deploy-manage/deploy/elastic-cloud/ec-customize-deployment-components.md) to ensure resiliency.
* Adjust the `number_of_replicas` [setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) for your indices to the number of eligible data nodes -1.


### A snapshot issue prevents searchable snapshot indices from being allocated [ec-searchable-snapshot-indices-not-allocated]

**Symptom**

Some snapshots operations might be impacted, as shown in the following example:

`failed shard on node [Yc_Jbf73QVSVYSqZT8HPlA]: failed recovery, failure RecoveryFailedException[[restored-my_index-2021.32][1]: … SnapshotMissingException[[found-snapshots:2021.08.25-my_index-2021.32-default_policy-_j2k8it9qnehe1t-2k0u6a/iOAoyjWLTyytKkW3_wF1jw] is missing]; nested: NoSuchFileException[Blob object [snapshots/52bc3ae2030a4df8ab10559d1720a13c/indices/WRlkKDuPSLW__M56E8qbfA/1/snap-iOAoyjWLTyytKkW3_wF1jw.dat] not found: The specified key does not exist. (Service: Amazon S3; Status Code: 404; Error Code: NoSuchKey; Request ID: 4AMTM1XFMTV5F00V; S3 Extended Request ID:`

**Resolutions**

Upgrade to {{es}} version 7.17.0 or later, which resolves bugs that affected  snapshot operations in earlier versions. Check [Upgrade versions](/deploy-manage/upgrade/deployment-or-cluster.md) for more details.

If you can’t upgrade, you can recreate the snapshot repository as a workaround.

The bugs also affect searchable snapshots. If you still have data in the cluster but cannot restore from the searchable snapshot, you can try reindexing and recreating the searchable snapshot:

* Reindex all the affected indices to new regular indices
* Remove the affected frozen indices
* Take the snapshot and mount the indices again


### Max shard per node reached the limit [ec-max-shard-per-node]

**Symptom**

The parameter [`cluster.max_shards_per_node`](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-max-shards-per-node) limits the total number of primary and replica shards for the cluster. If your cluster has a number of shards beyond this limit, you might get the following message:

`Validation Failed: 1: this action would add [2] shards, but this cluster currently has [1000]/[1000] maximum normal shards open`

**Resolutions**

Delete unnecessary indices, add more data nodes, and [avoid oversharding](/deploy-manage/production-guidance/optimize-performance/size-shards.md) as too many shards can overwhelm your cluster. If you cannot take these actions, and you’re confident your changes won’t destabilize the cluster, you can temporarily increase the limit using the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) and retry the action. For more details, check [Troubleshoot shard-related errors](/deploy-manage/production-guidance/optimize-performance/size-shards.md#troubleshoot-shard-related-errors).


### Maximum retry times exceeded [ec-max-retry-exceeded]

**Symptom**

The cluster will attempt to allocate a shard a few times, before giving up and leaving the shard unallocated. On {{es}} Service,  `index.allocation.max_retries` defaults to 5. If allocation fails after the maximum number of retries, you might get the following message:

`shard has exceeded the maximum number of retries [%d] on failed allocation attempts - manually call [/_cluster/reroute?retry_failed=true] to retry, [%s]`

**Resolutions**

Run [`POST /_cluster/reroute?retry_failed=true`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-reroute) API to retry. If it still fails, rerun the [Cluster allocation explain](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-allocation-explain) API to diagnose the problem.