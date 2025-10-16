---
navigation_title: On self-managed {{stack}}
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters.html
applies_to:
  deployment:
    self: ga
products:
  - id: elasticsearch
---

# Remote clusters on self-managed installations [remote-clusters]

The instructions that follow describe how to create a remote connection from a self-managed cluster. You can also set up {{ccs}} and {{ccr}} from an [{{ech}} deployment](/deploy-manage/remote-clusters/ec-enable-ccs.md) or from an [{{ece}} deployment](/deploy-manage/remote-clusters/ece-enable-ccs.md).


## Add remote clusters [add-remote-clusters]

To add remote clusters, you can choose between [two security models](#remote-clusters-security-models) and [two connection modes](#sniff-proxy-modes). Both security models are compatible with either of the connection modes.


### Security models [remote-clusters-security-models]

API key
:   For clusters on {{stack}} 8.14 or later, you can use an API key to authenticate and authorize cross-cluster operations to a remote cluster. This model offers administrators of both the local and the remote cluster fine-grained access controls. [Add remote clusters using API key authentication](remote-clusters-api-key.md).

TLS certificate (deprecated in {{stack}} 9.0.0)
:   Uses mutual TLS authentication for cross-cluster operations. User authentication is performed on the local cluster and a user’s role names are passed to the remote cluster. In this model, a superuser on the local cluster gains total read access to the remote cluster, so it is only suitable for clusters that are in the same security domain. [Add remote clusters using TLS certificate authentication](remote-clusters-cert.md).


### Connection modes [sniff-proxy-modes]

$$$sniff-mode$$$

Sniff mode
:   In sniff mode, a cluster alias is registered with a name of your choosing and a list of addresses of *seed* nodes specified with the `cluster.remote.<cluster_alias>.seeds` setting. When you register a remote cluster using sniff mode, {{es}} retrieves from one of the seed nodes the addresses of up to three *gateway nodes*. Each `remote_cluster_client` node in the local {{es}} cluster then opens several TCP connections to the publish addresses of the gateway nodes. This mode therefore requires that the gateway nodes' publish addresses are accessible to nodes in the local cluster.

    Sniff mode is the default connection mode. See [Sniff mode remote cluster settings](elasticsearch://reference/elasticsearch/configuration-reference/remote-clusters.md#remote-cluster-sniff-settings) for more information about configuring sniff mode.

    $$$gateway-nodes-selection$$$
    The *gateway nodes* selection depends on the following criteria:

    * **version**: Remote nodes must be compatible with the cluster they are registered to.
    * **role**: By default, any non-[master-eligible](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#master-node-role) node can act as a gateway node. Dedicated master nodes are never selected as gateway nodes.
    * **attributes**: You can define the gateway nodes for a cluster by setting [`cluster.remote.node.attr.gateway`](elasticsearch://reference/elasticsearch/configuration-reference/remote-clusters.md#cluster-remote-node-attr) to `true`. However, such nodes still have to satisfy the two above requirements.


$$$proxy-mode$$$

Proxy mode
:   In proxy mode, a cluster alias is registered with a name of your choosing and the address of a TCP (layer 4) reverse proxy specified with the `cluster.remote.<cluster_alias>.proxy_address` setting. You must configure this proxy to route connections to one or more nodes of the remote cluster. When you register a remote cluster using proxy mode, {{es}} opens several TCP connections to the proxy address and uses these connections to communicate with the remote cluster. In proxy mode {{es}} disregards the publish addresses of the remote cluster nodes which means that the publish addresses of the remote cluster nodes need not be accessible to the local cluster.

    Proxy mode is not the default connection mode, so you must set `cluster.remote.<cluster_alias>.mode: proxy` to use it. See [Proxy mode remote cluster settings](elasticsearch://reference/elasticsearch/configuration-reference/remote-clusters.md#remote-cluster-proxy-settings) for more information about configuring proxy mode.

    Proxy mode has the same [version compatibility requirements](#gateway-nodes-selection) as sniff mode.
