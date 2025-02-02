# Index Shard Allocation [index-modules-allocation]

This module provides per-index settings to control the allocation of shards to nodes:

* [Shard allocation filtering](../../../deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/index-level-shard-allocation.md): Controlling which shards are allocated to which nodes.
* [Delayed allocation](../../../deploy-manage/distributed-architecture/shard-allocation-relocation-recovery/delaying-allocation-when-node-leaves.md): Delaying allocation of unassigned shards caused by a node leaving.
* [Total shards per node](https://www.elastic.co/guide/en/elasticsearch/reference/current/allocation-total-shards.html): A hard limit on the number of shards from the same index per node.
* [Data tier allocation](https://www.elastic.co/guide/en/elasticsearch/reference/current/data-tier-shard-filtering.html): Controls the allocation of indices to [data tiers](../../../manage-data/lifecycle/data-tiers.md).






