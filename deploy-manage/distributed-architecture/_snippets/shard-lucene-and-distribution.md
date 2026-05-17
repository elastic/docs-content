<!-- Snippet used by:
     /manage-data/data-store/index-basics.md
     /deploy-manage/distributed-architecture/clusters-nodes-shards.md -->
Each shard is a self-contained [Apache Lucene](https://lucene.apache.org/) index with practical limits on how much data it can efficiently manage, so splitting data across multiple shards keeps individual shards performant. Distributing those shards across cluster nodes adds horizontal scaling and redundancy.
The right number of shards depends on your data volume, query patterns, and cluster topology — there is no single correct answer. Refer to [shard sizing and distribution recommendations](/deploy-manage/production-guidance/optimize-performance/size-shards.md#sizing-shard-guidelines) for more information and best practices.
