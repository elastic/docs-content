---
navigation_title: Cluster allocation API examples
---

# Using the cluster allocation API for troubleshooting

Troubleshooting shard allocation issues in an {{es}} cluster can be complex, especially when dealing with unassigned shards or rebalancing issues. The [cluster allocation explain API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-allocation-explain) helps diagnose these problems by providing detailed, node-by-node explanations of allocation decisions.

This page walks you through common scenarios to show how the API can guide you in resolving allocation issues efficiently.

## Unassigned primary shard

### Conflicting settings

The following request gets an allocation explanation for an unassigned primary
shard.

<!--
```console
PUT my-index-000001?master_timeout=1s&timeout=1s
{
  "settings": {
    "index.routing.allocation.include._name": "nonexistent_node",
    "index.routing.allocation.include._tier_preference": null
  }
}
```
-->

```console
GET _cluster/allocation/explain
{
  "index": "my-index-000001",
  "shard": 0,
  "primary": true
}
```

% TEST[continued]

The API response indicates the shard can only be allocated to a nonexistent
node.

```console-result
{
  "index" : "my-index-000001",
  "shard" : 0,
  "primary" : true,
  "current_state" : "unassigned",                 <1>
  "unassigned_info" : {
    "reason" : "INDEX_CREATED",                   <2>
    "at" : "2017-01-04T18:08:16.600Z",
    "last_allocation_status" : "no"
  },
  "can_allocate" : "no",                          <3>
  "allocate_explanation" : "Elasticsearch isn't allowed to allocate this shard to any of the nodes in the cluster. Choose a node to which you expect this shard to be allocated, find this node in the node-by-node explanation, and address the reasons which prevent Elasticsearch from allocating this shard there.",
  "node_allocation_decisions" : [
    {
      "node_id" : "8qt2rY-pT6KNZB3-hGfLnw",
      "node_name" : "node-0",
      "transport_address" : "127.0.0.1:9401",
      "roles" : ["data", "data_cold", "data_content", "data_frozen", "data_hot", "data_warm", "ingest", "master", "ml", "remote_cluster_client", "transform"],
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

% TESTRESPONSE[s/"at" : "[^"]*"/"at" : $body.$_path/]
% TESTRESPONSE[s/"node_id" : "[^"]*"/"node_id" : $body.$_path/]
% TESTRESPONSE[s/"transport_address" : "[^"]*"/"transport_address" : $body.$_path/]
% TESTRESPONSE[s/"roles" : \[("[a-z_]*",)*("[a-z_]*")\]/"roles" : $body.$_path/]
% TESTRESPONSE[s/"node_attributes" : \{\}/"node_attributes" : $body.$_path/]

1. The current state of the shard.
2. The reason for the shard originally becoming unassigned.
3. Whether to allocate the shard.
4. Whether to allocate the shard to the particular node.
5. The decider which led to the `no` decision for the node.
6. An explanation as to why the decider returned a `no` decision, with a helpful hint pointing to the setting that led to the decision. In this example, a newly created index has [an index setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) that requires that it only be allocated to a node named `nonexistent_node`, which does not exist, so the index is unable to allocate.

Refer to [this video](https://www.youtube.com/watch?v=5z3n2VgusLE) for a walkthrough of troubleshooting a node and index setting mismatch.

### Maximum number of retries exceeded [maximum-number-of-retries-exceeded]

The following response contains an allocation explanation for an unassigned
primary shard that has reached the maximum number of allocation retry attempts.

```console-result
{
  "index" : "my-index-000001",
  "shard" : 0,
  "primary" : true,
  "current_state" : "unassigned",
  "unassigned_info" : {
    "at" : "2017-01-04T18:03:28.464Z",
    "failed shard on node [mEKjwwzLT1yJVb8UxT6anw]: failed recovery, failure RecoveryFailedException",
    "reason": "ALLOCATION_FAILED",
    "failed_allocation_attempts": 5,
    "last_allocation_status": "no",
  },
  "can_allocate": "no",
  "allocate_explanation": "cannot allocate because allocation is not permitted to any of the nodes",
  "node_allocation_decisions" : [
    {
      "node_id" : "3sULLVJrRneSg0EfBB-2Ew",
      "node_name" : "node_t0",
      "transport_address" : "127.0.0.1:9400",
      "roles" : ["data_content", "data_hot"],
      "node_decision" : "no",
      "store" : {
        "matching_size" : "4.2kb",
        "matching_size_in_bytes" : 4325
      },
      "deciders" : [
        {
          "decider": "max_retry",
          "decision" : "NO",
          "explanation": "shard has exceeded the maximum number of retries [5] on failed allocation attempts - manually call [POST /_cluster/reroute?retry_failed&metric=none] to retry, [unassigned_info[[reason=ALLOCATION_FAILED], at[2024-07-30T21:04:12.166Z], failed_attempts[5], failed_nodes[[mEKjwwzLT1yJVb8UxT6anw]], delayed=false, details[failed shard on node [mEKjwwzLT1yJVb8UxT6anw]: failed recovery, failure RecoveryFailedException], allocation_status[deciders_no]]]"
        }
      ]
    }
  ]
}
```

% NOTCONSOLE

When {{es}} is unable to allocate a shard, it will attempt to retry allocation up to
the maximum number of retries allowed. After this, {{es}} will stop attempting to
allocate the shard in order to prevent infinite retries which may impact cluster
performance. Run the [cluster reroute](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-reroute) API to retry allocation, which
will allocate the shard if the issue preventing allocation has been resolved.

### No valid shard copy

The following response contains an allocation explanation for an unassigned
primary shard that was previously allocated.

```console-result
{
  "index" : "my-index-000001",
  "shard" : 0,
  "primary" : true,
  "current_state" : "unassigned",
  "unassigned_info" : {
    "reason" : "NODE_LEFT",
    "at" : "2017-01-04T18:03:28.464Z",
    "details" : "node_left[OIWe8UhhThCK0V5XfmdrmQ]",
    "last_allocation_status" : "no_valid_shard_copy"
  },
  "can_allocate" : "no_valid_shard_copy",
  "allocate_explanation" : "Elasticsearch can't allocate this shard because there are no copies of its data in the cluster. Elasticsearch will allocate this shard when a node holding a good copy of its data joins the cluster. If no such node is available, restore this index from a recent snapshot."
}
```

% NOTCONSOLE

If a shard is unassigned with an allocation status of `no_valid_shard_copy`, then you should [make sure that all nodes are in the cluster](red-yellow-cluster-status.md#fix-cluster-status-recover-nodes). If all the nodes containing in-sync copies of a shard are lost, then you can [recover the data for the shard](red-yellow-cluster-status.md#fix-cluster-status-restore).

Refer to [this video](https://www.youtube.com/watch?v=6OAg9IyXFO4) for a walkthrough of troubleshooting `no_valid_shard_copy`.

## Unassigned replica shard

### Allocation delayed

The following response contains an allocation explanation for a replica that's
unassigned due to <<delayed-allocation,delayed allocation>>.

```console-result
{
  "index" : "my-index-000001",
  "shard" : 0,
  "primary" : false,
  "current_state" : "unassigned",
  "unassigned_info" : {
    "reason" : "NODE_LEFT",
    "at" : "2017-01-04T18:53:59.498Z",
    "details" : "node_left[G92ZwuuaRY-9n8_tc-IzEg]",
    "last_allocation_status" : "no_attempt"
  },
  "can_allocate" : "allocation_delayed",
  "allocate_explanation" : "The node containing this shard copy recently left the cluster. Elasticsearch is waiting for it to return. If the node does not return within [%s] then Elasticsearch will allocate this shard to another node. Please wait.",
  "configured_delay" : "1m",                      <1>
  "configured_delay_in_millis" : 60000,
  "remaining_delay" : "59.8s",                    <2>
  "remaining_delay_in_millis" : 59824,
  "node_allocation_decisions" : [
    {
      "node_id" : "pmnHu_ooQWCPEFobZGbpWw",
      "node_name" : "node_t2",
      "transport_address" : "127.0.0.1:9402",
      "roles" : ["data_content", "data_hot"],
      "node_decision" : "yes"
    },
    {
      "node_id" : "3sULLVJrRneSg0EfBB-2Ew",
      "node_name" : "node_t0",
      "transport_address" : "127.0.0.1:9400",
      "roles" : ["data_content", "data_hot"],
      "node_decision" : "no",
      "store" : {                                 <3>
        "matching_size" : "4.2kb",
        "matching_size_in_bytes" : 4325
      },
      "deciders" : [
        {
          "decider" : "same_shard",
          "decision" : "NO",
          "explanation" : "a copy of this shard is already allocated to this node [[my-index-000001][0], node[3sULLVJrRneSg0EfBB-2Ew], [P], s[STARTED], a[id=eV9P8BN1QPqRc3B4PLx6cg]]"
        }
      ]
    }
  ]
}
```

% NOTCONSOLE

1. The configured delay before allocating a replica shard that does not exist due to the node holding it leaving the cluster.
2. The remaining delay before allocating the replica shard.
3. Information about the shard data found on a node.

### Allocation throttled

The following response contains an allocation explanation for a replica that's
queued to allocate but currently waiting on other queued shards.

```console-result
{
  "index" : "my-index-000001",
  "shard" : 0,
  "primary" : false,
  "current_state" : "unassigned",
  "unassigned_info" : {
    "reason" : "NODE_LEFT",
    "at" : "2017-01-04T18:53:59.498Z",
    "details" : "node_left[G92ZwuuaRY-9n8_tc-IzEg]",
    "last_allocation_status" : "no_attempt"
  },
  "can_allocate": "throttled",
  "allocate_explanation": "Elasticsearch is currently busy with other activities. It expects to be able to allocate this shard when those activities finish. Please wait.",
  "node_allocation_decisions" : [
    {
      "node_id" : "3sULLVJrRneSg0EfBB-2Ew",
      "node_name" : "node_t0",
      "transport_address" : "127.0.0.1:9400",
      "roles" : ["data_content", "data_hot"],
      "node_decision" : "no",
      "deciders" : [
        {
          "decider": "throttling",
          "decision": "THROTTLE",
          "explanation": "reached the limit of incoming shard recoveries [2], cluster setting [cluster.routing.allocation.node_concurrent_incoming_recoveries=2] (can also be set via [cluster.routing.allocation.node_concurrent_recoveries])"
        }
      ]
    }
  ]
}
```

% NOTCONSOLE

This is a transient message that might appear when a large amount of shards are allocating.

## Assigned shard

### Cannot remain on current node

The following response contains an allocation explanation for an assigned shard.
The response indicates the shard is not allowed to remain on its current node
and must be reallocated.

```console-result
{
  "index" : "my-index-000001",
  "shard" : 0,
  "primary" : true,
  "current_state" : "started",
  "current_node" : {
    "id" : "8lWJeJ7tSoui0bxrwuNhTA",
    "name" : "node_t1",
    "transport_address" : "127.0.0.1:9401",
    "roles" : ["data_content", "data_hot"]
  },
  "can_remain_on_current_node" : "no",            <1>
  "can_remain_decisions" : [                      <2>
    {
      "decider" : "filter",
      "decision" : "NO",
      "explanation" : "node does not match index setting [index.routing.allocation.include] filters [_name:\"nonexistent_node\"]"
    }
  ],
  "can_move_to_other_node" : "no",                <3>
  "move_explanation" : "This shard may not remain on its current node, but Elasticsearch isn't allowed to move it to another node. Choose a node to which you expect this shard to be allocated, find this node in the node-by-node explanation, and address the reasons which prevent Elasticsearch from allocating this shard there.",
  "node_allocation_decisions" : [
    {
      "node_id" : "_P8olZS8Twax9u6ioN-GGA",
      "node_name" : "node_t0",
      "transport_address" : "127.0.0.1:9400",
      "roles" : ["data_content", "data_hot"],
      "node_decision" : "no",
      "weight_ranking" : 1,
      "deciders" : [
        {
          "decider" : "filter",
          "decision" : "NO",
          "explanation" : "node does not match index setting [index.routing.allocation.include] filters [_name:\"nonexistent_node\"]"
        }
      ]
    }
  ]
}
```

% NOTCONSOLE

1. Whether the shard is allowed to remain on its current node.
2. The deciders that factored into the decision of why the shard is not allowed to remain on its current node.
3. Whether the shard is allowed to be allocated to another node.

### Must remain on current node

The following response contains an allocation explanation for a shard that must
remain on its current node. Moving the shard to another node would not improve
cluster balance.

```console-result
{
  "index" : "my-index-000001",
  "shard" : 0,
  "primary" : true,
  "current_state" : "started",
  "current_node" : {
    "id" : "wLzJm4N4RymDkBYxwWoJsg",
    "name" : "node_t0",
    "transport_address" : "127.0.0.1:9400",
    "roles" : ["data_content", "data_hot"],
    "weight_ranking" : 1
  },
  "can_remain_on_current_node" : "yes",
  "can_rebalance_cluster" : "yes",                <1>
  "can_rebalance_to_other_node" : "no",           <2>
  "rebalance_explanation" : "Elasticsearch cannot rebalance this shard to another node since there is no node to which allocation is permitted which would improve the cluster balance. If you expect this shard to be rebalanced to another node, find this node in the node-by-node explanation and address the reasons which prevent Elasticsearch from rebalancing this shard there.",
  "node_allocation_decisions" : [
    {
      "node_id" : "oE3EGFc8QN-Tdi5FFEprIA",
      "node_name" : "node_t1",
      "transport_address" : "127.0.0.1:9401",
      "roles" : ["data_content", "data_hot"],
      "node_decision" : "worse_balance",          <3>
      "weight_ranking" : 1
    }
  ]
}
```

% NOTCONSOLE

1. Whether rebalancing is allowed on the cluster.
2. Whether the shard can be rebalanced to another node.
3. The reason the shard cannot be rebalanced to the node, in this case indicating that it offers no better balance than the current node.

### No arguments

If you call the API with no arguments, {{es}} retrieves an allocation explanation
for an arbitrary unassigned primary or replica shard, returning any unassigned primary shards first.

```console
GET _cluster/allocation/explain
```

% TEST[catch:bad_request]

If the cluster contains no unassigned shards, the API returns a `400` error.