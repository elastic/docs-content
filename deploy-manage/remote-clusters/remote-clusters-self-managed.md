---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters.html
---

# Remote clusters (self-managed) [remote-clusters]

You can connect a local cluster to other {{es}} clusters, known as *remote clusters*. Remote clusters can be located in different datacenters or geographic regions, and contain indices or data streams that can be replicated with {{ccr}} or searched by a local cluster using {{ccs}}.


## {{ccr-cap}} [remote-clusters-ccr]

With [{{ccr}}](https://www.elastic.co/guide/en/elasticsearch/reference/current/xpack-ccr.html), you ingest data to an index on a remote cluster. This *leader* index is replicated to one or more read-only *follower* indices on your local cluster. Creating a multi-cluster architecture with {{ccr}} enables you to configure disaster recovery, bring data closer to your users, or establish a centralized reporting cluster to process reports locally.


## {{ccs-cap}} [remote-clusters-ccs]

[{{ccs-cap}}](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cross-cluster-search.html) enables you to run a search request against one or more remote clusters. This capability provides each region with a global view of all clusters, allowing you to send a search request from a local cluster and return results from all connected remote clusters. For full {{ccs}} capabilities, the local and remote cluster must be on the same [subscription level](https://www.elastic.co/subscriptions).


## Add remote clusters [add-remote-clusters]

::::{note}
The instructions that follow describe how to create a remote connection from a self-managed cluster. You can also set up {{ccs}} and {{ccr}} from an [{{ess}} deployment](https://www.elastic.co/guide/en/cloud/current/ec-enable-ccs.html) or from an [{{ece}} deployment](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-enable-ccs.html).
::::


To add remote clusters, you can choose between [two security models](#remote-clusters-security-models) and [two connection modes](#sniff-proxy-modes). Both security models are compatible with either of the connection modes.


### Security models [remote-clusters-security-models]

API key based security model
:   For clusters on version 8.14 or later, you can use an API key to authenticate and authorize cross-cluster operations to a remote cluster. This model offers administrators of both the local and the remote cluster fine-grained access controls. [Add remote clusters using API key authentication](remote-clusters-api-key.md).

Certificate based security model
:   Uses mutual TLS authentication for cross-cluster operations. User authentication is performed on the local cluster and a user’s role names are passed to the remote cluster. In this model, a superuser on the local cluster gains total read access to the remote cluster, so it is only suitable for clusters that are in the same security domain. [Add remote clusters using TLS certificate authentication](remote-clusters-cert.md).

    ::::{admonition} Deprecated in 9.0.0.
    :class: warning

    Use [API key based security model](remote-clusters-api-key.md) instead.
    ::::



### Connection modes [sniff-proxy-modes]

$$$sniff-mode$$$

Sniff mode
:   In sniff mode, a cluster alias is registered with a name of your choosing and a list of addresses of *seed* nodes specified with the `cluster.remote.<cluster_alias>.seeds` setting. When you register a remote cluster using sniff mode, {{es}} retrieves from one of the seed nodes the addresses of up to three *gateway nodes*. Each `remote_cluster_client` node in the local {{es}} cluster then opens several TCP connections to the publish addresses of the gateway nodes. This mode therefore requires that the gateway nodes' publish addresses are accessible to nodes in the local cluster.

    Sniff mode is the default connection mode. See [Sniff mode remote cluster settings](remote-clusters-settings.md#remote-cluster-sniff-settings) for more information about configuring sniff mode.

    $$$gateway-nodes-selection$$$
    The *gateway nodes* selection depends on the following criteria:

    * **version**: Remote nodes must be compatible with the cluster they are registered to.
    * **role**: By default, any non-[master-eligible](https://www.elastic.co/guide/en/elasticsearch/reference/current/node-roles-overview.html#master-node-role) node can act as a gateway node. Dedicated master nodes are never selected as gateway nodes.
    * **attributes**: You can define the gateway nodes for a cluster by setting [`cluster.remote.node.attr.gateway`](remote-clusters-settings.md#cluster-remote-node-attr) to `true`. However, such nodes still have to satisfy the two above requirements.


$$$proxy-mode$$$

Proxy mode
:   In proxy mode, a cluster alias is registered with a name of your choosing and the address of a TCP (layer 4) reverse proxy specified with the `cluster.remote.<cluster_alias>.proxy_address` setting. You must configure this proxy to route connections to one or more nodes of the remote cluster. When you register a remote cluster using proxy mode, {{es}} opens several TCP connections to the proxy address and uses these connections to communicate with the remote cluster. In proxy mode {{es}} disregards the publish addresses of the remote cluster nodes which means that the publish addresses of the remote cluster nodes need not be accessible to the local cluster.

    Proxy mode is not the default connection mode, so you must set `cluster.remote.<cluster_alias>.mode: proxy` to use it. See [Proxy mode remote cluster settings](remote-clusters-settings.md#remote-cluster-proxy-settings) for more information about configuring proxy mode.

    Proxy mode has the same [version compatibility requirements](#gateway-nodes-selection) as sniff mode.
