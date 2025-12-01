---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_connect_to_a_remote_cluster.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Connect to a remote cluster [_connect_to_a_remote_cluster]

To replicate an index on a remote cluster (Cluster A) to a local cluster (Cluster B), you configure Cluster A as a remote on Cluster B.

:::{image} /deploy-manage/images/elasticsearch-reference-ccr-tutorial-clusters.png
:alt: ClusterA contains the leader index and ClusterB contains the follower index
:::

To configure a remote cluster in {{kib}}:

1. Set up a [secure connection](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#add-remote-clusters) as needed.
2. Go to the **Remote Clusters** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
3. Select the appropriate connection type.
4. Specify the {{es}} endpoint URL, or the IP address or host name of the remote cluster (`ClusterA`) followed by the transport port (defaults to `9300`). For example, `cluster.es.eastus2.staging.azure.foundit.no:9400` or `192.168.1.1:9300`.

::::{dropdown} API example
You can also use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) to add a remote cluster:

```console
PUT /_cluster/settings
{
  "persistent" : {
    "cluster" : {
      "remote" : {
        "leader" : {
          "seeds" : [
            "127.0.0.1:9300" <1>
          ]
        }
      }
    }
  }
}
```

1. Specifies the hostname and transport port of a seed node in the remote cluster.


You can verify that the local cluster is successfully connected to the remote cluster.

```console
GET /_remote/info
```

The API response indicates that the local cluster is connected to the remote cluster with cluster alias `leader`.

```console-result
{
  "leader" : {
    "seeds" : [
      "127.0.0.1:9300"
    ],
    "connected" : true,
    "num_nodes_connected" : 1, <1>
    "max_connections_per_cluster" : 3,
    "initial_connect_timeout" : "30s",
    "skip_unavailable" : true,
    "mode" : "sniff"
  }
}
```

1. The number of nodes in the remote cluster the local cluster is connected to.


::::


