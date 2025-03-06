---
navigation_title: Unassigned shards
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/diagnose-unassigned-shards.html
---

% marciw move to a new Unassigned shards subsection

# Diagnose unassigned shards [diagnose-unassigned-shards]

There are multiple reasons why shards might get unassigned, ranging from misconfigured allocation settings to lack of disk space.

In order to diagnose the unassigned shards in your deployment use the following steps:

:::::::{tab-set}

::::::{tab-item} {{ech}}
In order to diagnose the unassigned shards, follow the next steps:

**Use {{kib}}**

1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Hosted deployments** panel, click the name of your deployment.

    ::::{note}
    If the name of your deployment is disabled your {{kib}} instances might be unhealthy, in which case please contact [Elastic Support](https://support.elastic.co). If your deployment doesn’t include {{kib}}, all you need to do is [enable it first](../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
    ::::

3. Open your deployment’s side navigation menu (placed under the Elastic logo in the upper left corner) and go to **Dev Tools > Console**.

    :::{image} ../../images/elasticsearch-reference-kibana-console.png
    :alt: {{kib}} Console
    :class: screenshot
    :::

4. View the unassigned shards using the [cat shards API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-shards).

    ```console
    GET _cat/shards?v=true&h=index,shard,prirep,state,node,unassigned.reason&s=state
    ```

    The response will look like this:

    ```console-result
    [
      {
        "index": "my-index-000001",
        "shard": "0",
        "prirep": "p",
        "state": "UNASSIGNED",
        "node": null,
        "unassigned.reason": "INDEX_CREATED"
      }
    ]
    ```

    Unassigned shards have a `state` of `UNASSIGNED`. The `prirep` value is `p` for primary shards and `r` for replicas.

    The index in the example has a primary shard unassigned.

5. To understand why an unassigned shard is not being assigned and what action you must take to allow {{es}} to assign it, use the [cluster allocation explanation API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-allocation-explain).

    ```console
    GET _cluster/allocation/explain
    {
      "index": "my-index-000001", <1>
      "shard": 0, <2>
      "primary": true <3>
    }
    ```

    1. The index we want to diagnose.
    2. The unassigned shard ID.
    3. Indicates that we are diagnosing a primary shard.


    The response will look like this:

    ```console-result
    {
      "index" : "my-index-000001",
      "shard" : 0,
      "primary" : true,
      "current_state" : "unassigned",                 <1>
      "unassigned_info" : {
        "reason" : "INDEX_CREATED",                   <2>
        "at" : "2022-01-04T18:08:16.600Z",
        "last_allocation_status" : "no"
      },
      "can_allocate" : "no",                          <3>
      "allocate_explanation" : "Elasticsearch isn't allowed to allocate this shard to any of the nodes in the cluster. Choose a node to which you expect this shard to be allocated, find this node in the node-by-node explanation, and address the reasons which prevent Elasticsearch from allocating this shard there.",
      "node_allocation_decisions" : [
        {
          "node_id" : "8qt2rY-pT6KNZB3-hGfLnw",
          "node_name" : "node-0",
          "transport_address" : "127.0.0.1:9401",
          "roles": ["data_content", "data_hot"],
          "node_attributes" : {},
          "node_decision" : "no",                     <4>
          "weight_ranking" : 1,
          "deciders" : [
            {
              "decider" : "filter",                   <5>
              "decision" : "NO",
              "explanation" : "node does not match index setting [index.routing.allocation.include] filters [_name:\"nonexistent_node\"]"  <6>
            }
          ]
        }
      ]
    }
    ```

    1. The current state of the shard.
    2. The reason for the shard originally becoming unassigned.
    3. Whether to allocate the shard.
    4. Whether to allocate the shard to the particular node.
    5. The decider which led to the `no` decision for the node.
    6. An explanation as to why the decider returned a `no` decision, with a helpful hint pointing to the setting that led to the decision.

6. The explanation in our case indicates the index allocation configurations are not correct. To review your allocation settings, use the [get index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) and [cluster get settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings) APIs.

    ```console
    GET my-index-000001/_settings?flat_settings=true&include_defaults=true

    GET _cluster/settings?flat_settings=true&include_defaults=true
    ```

7. Change the settings using the [update index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) and [cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) APIs to the correct values in order to allow the index to be allocated.

For more guidance on fixing the most common causes for unassinged shards please follow [this guide](red-yellow-cluster-status.md#fix-red-yellow-cluster-status) or contact [Elastic Support](https://support.elastic.co).
::::::

::::::{tab-item} Self-managed
In order to diagnose the unassigned shards follow the next steps:

1. View the unassigned shards using the [cat shards API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-shards).

    ```console
    GET _cat/shards?v=true&h=index,shard,prirep,state,node,unassigned.reason&s=state
    ```

    The response will look like this:

    ```console-result
    [
      {
        "index": "my-index-000001",
        "shard": "0",
        "prirep": "p",
        "state": "UNASSIGNED",
        "node": null,
        "unassigned.reason": "INDEX_CREATED"
      }
    ]
    ```

    Unassigned shards have a `state` of `UNASSIGNED`. The `prirep` value is `p` for primary shards and `r` for replicas.

    The index in the example has a primary shard unassigned.

2. To understand why an unassigned shard is not being assigned and what action you must take to allow {{es}} to assign it, use the [cluster allocation explanation API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-allocation-explain).

    ```console
    GET _cluster/allocation/explain
    {
      "index": "my-index-000001", <1>
      "shard": 0, <2>
      "primary": true <3>
    }
    ```

    1. The index we want to diagnose.
    2. The unassigned shard ID.
    3. Indicates that we are diagnosing a primary shard.


    The response will look like this:

    ```console-result
    {
      "index" : "my-index-000001",
      "shard" : 0,
      "primary" : true,
      "current_state" : "unassigned",                 <1>
      "unassigned_info" : {
        "reason" : "INDEX_CREATED",                   <2>
        "at" : "2022-01-04T18:08:16.600Z",
        "last_allocation_status" : "no"
      },
      "can_allocate" : "no",                          <3>
      "allocate_explanation" : "Elasticsearch isn't allowed to allocate this shard to any of the nodes in the cluster. Choose a node to which you expect this shard to be allocated, find this node in the node-by-node explanation, and address the reasons which prevent Elasticsearch from allocating this shard there.",
      "node_allocation_decisions" : [
        {
          "node_id" : "8qt2rY-pT6KNZB3-hGfLnw",
          "node_name" : "node-0",
          "transport_address" : "127.0.0.1:9401",
          "roles": ["data_content", "data_hot"]
          "node_attributes" : {},
          "node_decision" : "no",                     <4>
          "weight_ranking" : 1,
          "deciders" : [
            {
              "decider" : "filter",                   <5>
              "decision" : "NO",
              "explanation" : "node does not match index setting [index.routing.allocation.include] filters [_name:\"nonexistent_node\"]"  <6>
            }
          ]
        }
      ]
    }
    ```

    1. The current state of the shard.
    2. The reason for the shard originally becoming unassigned.
    3. Whether to allocate the shard.
    4. Whether to allocate the shard to the particular node.
    5. The decider which led to the `no` decision for the node.
    6. An explanation as to why the decider returned a `no` decision, with a helpful hint pointing to the setting that led to the decision.

3. The explanation in our case indicates the index allocation configurations are not correct. To review your allocation settings, use the [get index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) and [cluster get settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings) APIs.

    ```console
    GET my-index-000001/_settings?flat_settings=true&include_defaults=true

    GET _cluster/settings?flat_settings=true&include_defaults=true
    ```

4. Change the settings using the [update index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) and [cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) APIs to the correct values in order to allow the index to be allocated.

For more guidance on fixing the most common causes for unassinged shards please follow [this guide](red-yellow-cluster-status.md#fix-red-yellow-cluster-status).
::::::

:::::::
See [this video](https://www.youtube.com/watch?v=v2mbeSd1vTQ) for a walkthrough of monitoring allocation health.

::::{tip}
If you’re using Elastic Cloud Hosted, then you can use AutoOps to monitor your cluster. AutoOps significantly simplifies cluster management with performance recommendations, resource utilization visibility, real-time issue detection and resolution paths. For more information, refer to [Monitor with AutoOps](/deploy-manage/monitor/autoops.md).

::::
