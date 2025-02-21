---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-fault-detection.html
applies_to:
  stack:
---

# Cluster fault detection [cluster-fault-detection]

The elected master periodically checks each of the nodes in the cluster to ensure that they are still connected and healthy. Each node in the cluster also periodically checks the health of the elected master. These checks are known respectively as *follower checks* and *leader checks*.

Elasticsearch allows these checks to occasionally fail or timeout without taking any action. It considers a node to be faulty only after a number of consecutive checks have failed. You can control fault detection behavior with [`cluster.fault_detection.*` settings](elasticsearch://reference/elasticsearch/configuration-reference/discovery-cluster-formation-settings.md).

If the elected master detects that a node has disconnected, however, this situation is treated as an immediate failure. The master bypasses the timeout and retry setting values and attempts to remove the node from the cluster. Similarly, if a node detects that the elected master has disconnected, this situation is treated as an immediate failure. The node bypasses the timeout and retry settings and restarts its discovery phase to try and find or elect a new master.

$$$cluster-fault-detection-filesystem-health$$$
Additionally, each node periodically verifies that its data path is healthy by writing a small file to disk and then deleting it again. If a node discovers its data path is unhealthy then it is removed from the cluster until the data path recovers. You can control this behavior with the [`monitor.fs.health` settings](elasticsearch://reference/elasticsearch/configuration-reference/discovery-cluster-formation-settings.md).

$$$cluster-fault-detection-cluster-state-publishing$$$
The elected master node will also remove nodes from the cluster if nodes are unable to apply an updated cluster state within a reasonable time. The timeout defaults to 2 minutes starting from the beginning of the cluster state update. Refer to [Publishing the cluster state](cluster-state-overview.md#cluster-state-publishing) for a more detailed description.

## Troubleshooting an unstable cluster [cluster-fault-detection-troubleshooting]

See [*Troubleshooting an unstable cluster*](../../../troubleshoot/elasticsearch/troubleshooting-unstable-cluster.md).


#### Diagnosing `disconnected` nodes [_diagnosing_disconnected_nodes]

See [Diagnosing `disconnected` nodes](../../../troubleshoot/elasticsearch/troubleshooting-unstable-cluster.md#troubleshooting-unstable-cluster-disconnected).


#### Diagnosing `lagging` nodes [_diagnosing_lagging_nodes]

See [Diagnosing `lagging` nodes](../../../troubleshoot/elasticsearch/troubleshooting-unstable-cluster.md#troubleshooting-unstable-cluster-lagging).


#### Diagnosing `follower check retry count exceeded` nodes [_diagnosing_follower_check_retry_count_exceeded_nodes]

See [Diagnosing `follower check retry count exceeded` nodes](../../../troubleshoot/elasticsearch/troubleshooting-unstable-cluster.md#troubleshooting-unstable-cluster-follower-check).


#### Diagnosing `ShardLockObtainFailedException` failures [_diagnosing_shardlockobtainfailedexception_failures]

See [Diagnosing `ShardLockObtainFailedException` failures](../../../troubleshoot/elasticsearch/troubleshooting-unstable-cluster.md#troubleshooting-unstable-cluster-shardlockobtainfailedexception).


#### Diagnosing other network disconnections [_diagnosing_other_network_disconnections]

See [Diagnosing other network disconnections](../../../troubleshoot/elasticsearch/troubleshooting-unstable-cluster.md#troubleshooting-unstable-cluster-network).


