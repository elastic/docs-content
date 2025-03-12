---
navigation_title: "Set up cross-cluster replication"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-getting-started-tutorial.html

applies_to:
  deployment:
    eck: 
    ess: 
    ece: 
    self: 
---



# Set up cross-cluster replication [ccr-getting-started-tutorial]


Use this guide to set up {{ccr}} (CCR) between clusters in two datacenters. Replicating your data across datacenters provides several benefits:

* Brings data closer to your users or application server to reduce latency and response time
* Provides your mission-critical applications with the tolerance to withstand datacenter or region outages

In this guide, you’ll learn how to:

* Configure a [remote cluster](../../remote-clusters.md) with a leader index
* Create a follower index on a local cluster
* Create an auto-follow pattern to automatically follow time series indices that are periodically created in a remote cluster

You can manually create follower indices to replicate specific indices on a remote cluster, or configure auto-follow patterns to replicate rolling time series indices.

::::{tip}
If you want to replicate data across clusters in the cloud, you can [configure remote clusters on {{{ecloud}}](/deploy-manage/remote-clusters/ec-enable-ccs.md). Then, you can [search across clusters](../../../solutions/search/cross-cluster-search.md) and set up {{ccr}}.
::::







