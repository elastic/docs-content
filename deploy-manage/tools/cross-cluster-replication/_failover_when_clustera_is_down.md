---
navigation_title: Failover when clusterA is down
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_failover_when_clustera_is_down.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Uni-directional recovery: failover when clusterA is down [_failover_when_clustera_is_down]

1. Promote the follower indices in `clusterB` into regular indices so that they accept writes. This can be achieved by:

    * First, pause indexing following for the follower index.
    * Next, close the follower index.
    * Unfollow the leader index.
    * Finally, open the follower index (which at this point is a regular index).

    ```console
    ### On clusterB ###
    POST /kibana_sample_data_ecommerce2/_ccr/pause_follow
    POST /kibana_sample_data_ecommerce2/_close
    POST /kibana_sample_data_ecommerce2/_ccr/unfollow
    POST /kibana_sample_data_ecommerce2/_open
    ```

2. On the client side ({{ls}}, {{beats}}, {{agent}}), manually re-enable ingestion of `kibana_sample_data_ecommerce2` and redirect traffic to the `clusterB`. You should also redirect all search traffic to the `clusterB` cluster during this time. You can simulate this by ingesting documents into this index. You should notice this index is now writable.

    ```console
    ### On clusterB ###
    POST kibana_sample_data_ecommerce2/_doc/
    {
      "user": "kimchy"
    }
    ```


