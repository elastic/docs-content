# Analyze unassigned shards using the {{es}} API [ech-analyze_shards_with-api]

You can retrieve information about the status of your cluster, indices, and shards using the {{es}} API. To access the API you can either use the [Kibana Dev Tools Console](../../../explore-analyze/query-filter/tools/console.md), or the [Elasticsearch API console](../../../deploy-manage/deploy/elastic-cloud/ech-api-console.md). This section shows you how to:

* [Check cluster health](ech-analyze_shards_with-api.md#ech-check-cluster-health)
* [Check unhealthy indices](ech-analyze_shards_with-api.md#ech-check-unhealthy-indices)
* [Check which shards are unassigned](ech-analyze_shards_with-api.md#ech-check-which-unassigned-shards)
* [Check why shards are unassigned](ech-analyze_shards_with-api.md#ech-check-why-unassigned-shards)
* [Check Elasticsearch cluster logs](ech-analyze_shards_with-api.md#ech-check-es-cluster-logs)


## Check cluster health [ech-check-cluster-health]

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


## Check unhealthy indices [ech-check-unhealthy-indices]

Use the [cat indices API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-indices) to get the status of individual indices. Specify the `health` parameter to limit the results to a particular status, for example `?v&health=red` or `?v&health=yellow`.

```json
GET /_cat/indices?v&health=red
```

This command returns any indices that have unassigned primary shards (red status):

```json
red   open    filebeat-7.10.0-2022.01.07-000014 C7N8fxGwRxK0JcwXH18zVg  1 1
red   open    filebeat-7.9.3-2022.01.07-000015  Ib4UIJNVTtOg6ovzs011Lq  1 1
```

For more information, refer to [Fix a red or yellow cluster status](../../../troubleshoot/elasticsearch/red-yellow-cluster-status.md#fix-red-yellow-cluster-status).


## Check which shards are unassigned [ech-check-which-unassigned-shards]

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


## Check why shards are unassigned [ech-check-why-unassigned-shards]

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


## Check {{es}} cluster logs [ech-check-es-cluster-logs]

To determine the allocation issue, you can [check the logs](ech-monitoring-setup.md#ech-check-logs). This is easier if you have set up a dedicated monitoring deployment.

