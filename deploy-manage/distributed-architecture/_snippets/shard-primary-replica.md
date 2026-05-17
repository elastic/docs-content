<!-- Snippet used by:
     /manage-data/data-store/index-basics.md
     /deploy-manage/distributed-architecture/clusters-nodes-shards.md -->
There are two types of shards:

* **Primary shards**: Every document belongs to exactly one primary shard. The number of primary shards is fixed at index creation, either through an [index template](/manage-data/data-store/templates.md) or the [`index.number_of_shards`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-number-of-shards) setting in the create index request.
* **Replica shards**: These are copies of primary shards that provide redundancy and serve read requests. You can adjust the number of replicas at any time using the [`index.number_of_replicas`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#dynamic-index-number-of-replicas) setting. Changing the replica count does not interrupt indexing or query operations.
