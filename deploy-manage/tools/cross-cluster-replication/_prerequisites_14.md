---
navigation_title: Prerequisites
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_prerequisites_14.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Prerequisites for uni-directional disaster recovery [_prerequisites_14]

Before completing this tutorial, [set up cross-cluster replication](set-up-cross-cluster-replication.md) to connect two clusters and configure a follower index.

In this tutorial, `kibana_sample_data_ecommerce` is replicated from `clusterA` to `clusterB`.

```console
## On clusterB ###
PUT _cluster/settings
{
  "persistent": {
    "cluster": {
      "remote": {
        "clusterA": {
          "mode": "proxy",
          "skip_unavailable": "true",
          "server_name": "clustera.es.region-a.gcp.elastic-cloud.com",
          "proxy_socket_connections": "18",
          "proxy_address": "clustera.es.region-a.gcp.elastic-cloud.com:9400"
        }
      }
    }
  }
}
```

```console
## On clusterB ###
PUT /kibana_sample_data_ecommerce2/_ccr/follow?wait_for_active_shards=1
{
  "remote_cluster": "clusterA",
  "leader_index": "kibana_sample_data_ecommerce"
}
```

::::{important} 
Writes (such as ingestion or updates) should occur only on the leader index. Follower indices are read-only and will reject any writes.
::::


