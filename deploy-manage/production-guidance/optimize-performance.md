---
navigation_title: Performance optimizations
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/how-to.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
---

# {{es}} performance optimizations [how-to]

{{es}}'s default settings provide a good out-of-box experience for basic operations like full text search, highlighting, aggregations, and indexing.

However, there are a number of optimizations you can make to improve performance for your use case. This section includes both deployment-level configuration suggestions and usage-level guidance to optimize the performance of your cluster.

Use the following topics to explore relevant strategies:

* [General recommendations](general-recommendations.md)
* [Tune for indexing speed](optimize-performance/indexing-speed.md)
* [Tune for search speed](optimize-performance/search-speed.md)
* [Tune approximate kNN search](optimize-performance/approximate-knn-search.md)
* [Tune for disk usage](optimize-performance/disk-usage.md)
* [Size your shards](optimize-performance/size-shards.md)

::::{note}
Many {{es}} options come with different performance considerations and trade-offs. The best way to determine the optimal configuration for your use case is through [testing with your own data and queries](https://www.elastic.co/elasticon/conf/2016/sf/quantitative-cluster-sizing).
::::
