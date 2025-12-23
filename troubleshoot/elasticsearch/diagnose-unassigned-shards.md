---
navigation_title: Unassigned shards
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/diagnose-unassigned-shards.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

% marciw move to a new Unassigned shards subsection

# Diagnose unassigned shards [diagnose-unassigned-shards]

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::

There are multiple reasons why shards might get unassigned, ranging from misconfigured allocation settings to lack of disk space.

In order to diagnose the unassigned shards in your deployment use the following steps:


:::::::{tab-set}

::::::{tab-item} Using Kibana Dev Tools

To diagnose the unassigned shards from {{kib}}, follow these steps:

1. Open your deployment’s side navigation menu (placed under the Elastic logo in the upper left corner) and go to **Dev Tools > Console**.

    :::{image} /troubleshoot/images/elasticsearch-reference-kibana-console.png
    :alt: {{kib}} Console
    :screenshot:
    :::

2. View the unassigned shards using the [cat shards API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-shards).

    ```console
    GET _cat/shards?v=true&h=index,shard,prirep,state,node,unassigned.reason&s=state&format=json
    ```

    The response looks like this:

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

3. To understand why an unassigned shard is not being assigned and what action you must take to allow {{es}} to assign it, use the [cluster allocation explanation API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-allocation-explain).

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


    The response looks like this:

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

    4. The current state of the shard.
    5. The reason for the shard originally becoming unassigned.
    6. Whether to allocate the shard.
    7. Whether to allocate the shard to the particular node.
    8. The decider which led to the `no` decision for the node.
    9. An explanation as to why the decider returned a `no` decision, with a helpful hint pointing to the setting that led to the decision.

6. The explanation in our case indicates the index allocation configurations are not correct. To review your allocation settings, use the [get index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) and [cluster get settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings) APIs.

    ```console
    GET my-index-000001/_settings?flat_settings=true&include_defaults=true

    GET _cluster/settings?flat_settings=true&include_defaults=true
    ```

7. Change the settings using the [update index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) and [cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) APIs to the correct values to allow the index to be allocated.

For more guidance on fixing the most common causes for unassigned shards, follow [](red-yellow-cluster-status.md#fix-red-yellow-cluster-status), refer to [](/troubleshoot/elasticsearch/cluster-allocation-api-examples.md), or contact [Elastic Support](https://support.elastic.co).
::::::

::::::{tab-item} Using the {{es}} API
To diagnose the unassigned shards, follow the next steps:

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


    The response looks like this:

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

    4. The current state of the shard.
    5. The reason for the shard originally becoming unassigned.
    6. Whether to allocate the shard.
    7. Whether to allocate the shard to the particular node.
    8. The decider which led to the `no` decision for the node.
    9. An explanation as to why the decider returned a `no` decision, with a helpful hint pointing to the setting that led to the decision.

3. The explanation in our case indicates the index allocation configurations are not correct. To review your allocation settings, use the [get index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) and [cluster get settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-settings) APIs.

    ```console
    GET my-index-000001/_settings?flat_settings=true&include_defaults=true

    GET _cluster/settings?flat_settings=true&include_defaults=true
    ```

4. Change the settings using the [update index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) and [cluster update settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) APIs to the correct values in order to allow the index to be allocated.

For more guidance on fixing the most common causes for unassinged shards follow [this guide](red-yellow-cluster-status.md#fix-red-yellow-cluster-status), see [these examples](https://www.elastic.co/docs/troubleshoot/elasticsearch/cluster-allocation-api-examples), or contact [Elastic Support](https://support.elastic.co).
::::::

:::::::
Watch [this video](https://www.youtube.com/watch?v=v2mbeSd1vTQ) for a walkthrough of monitoring allocation health.

## Common issues

The following sections provide advice for resolving some of the common causes for unassigned shards.

### Conflicting settings

A primary shard might be unassigned due to conflicting settings.
View [this video](https://www.youtube.com/watch?v=5z3n2VgusLE) for a walkthrough of troubleshooting a node and index setting mismatch.

### Maximum number of retries exceeded [maximum-retries-exceeded]

When {{es}} is unable to allocate a shard, it attempts to retry allocation up to the maximum number of retries allowed.
After this, {{es}} stops attempting to allocate the shard to prevent infinite retries, which might impact cluster performance.
You can use an API to [reroute the cluster]({{es-apis}}operation/operation-cluster-reroute), which allocates the shard if the issue preventing allocation has been resolved.

### No valid shard copy [no-shard-copy]

If a shard is unassigned with an allocation status of `no_valid_shard_copy`, you should make sure that all nodes are in the cluster. If all the nodes containing in-sync copies of a shard are lost, then you can recover the data for the shard.

View [this video](https://www.youtube.com/watch?v=6OAg9IyXFO4) for a walkthrough of troubleshooting `no_valid_shard_copy`.
