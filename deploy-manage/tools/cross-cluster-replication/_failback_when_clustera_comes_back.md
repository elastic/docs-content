---
navigation_title: Failback when clusterA comes back
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_failback_when_clustera_comes_back.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Uni-directional recovery: failback when clusterA comes back [_failback_when_clustera_comes_back]

When `clusterA` comes back, `clusterB` becomes the new leader and `clusterA` becomes the follower.

1. Set up remote cluster `clusterB` on `clusterA`.

    ```console
    ### On clusterA ###
    PUT _cluster/settings
    {
      "persistent": {
        "cluster": {
          "remote": {
            "clusterB": {
              "mode": "proxy",
              "skip_unavailable": "true",
              "server_name": "clusterb.es.region-b.gcp.elastic-cloud.com",
              "proxy_socket_connections": "18",
              "proxy_address": "clusterb.es.region-b.gcp.elastic-cloud.com:9400"
            }
          }
        }
      }
    }
    ```

2. Existing data needs to be discarded before you can turn any index into a follower. Ensure the most up-to-date data is available on `clusterB` prior to deleting any indices on `clusterA`.

    ```console
    ### On clusterA ###
    DELETE kibana_sample_data_ecommerce
    ```

3. Create a follower index on `clusterA`, now following the leader index in `clusterB`.

    ```console
    ### On clusterA ###
    PUT /kibana_sample_data_ecommerce/_ccr/follow?wait_for_active_shards=1
    {
      "remote_cluster": "clusterB",
      "leader_index": "kibana_sample_data_ecommerce2"
    }
    ```

4. The index on the follower cluster now contains the updated documents.

    ```console
    ### On clusterA ###
    GET kibana_sample_data_ecommerce/_search?q=kimchy
    ```

    ::::{tip}
    If a soft delete is merged away before it can be replicated to a follower the following process will fail due to incomplete history on the leader, see [index.soft_deletes.retention_lease.period](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#ccr-index-soft-deletes-retention-period) for more details.
    ::::


