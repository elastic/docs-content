---
navigation_title: Connection modes
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: elasticsearch
---
# Remote cluster connection modes

When you configure a remote cluster, the local cluster needs a way to connect to the nodes of the remote cluster. {{es}} supports two connection modes to handle different network architectures:

- **Proxy mode**: The local cluster connects through a reverse proxy or load balancer, which forwards traffic to the appropriate nodes in the remote cluster. You can configure this mode using either the {{kib}} UI or the {{es}} API.
- **Sniff mode**: The local cluster discovers the remote cluster’s gateway nodes and connects to them directly. This mode can only be configured using the {{es}} API.

::::{note}
Connection modes work independently of [security models](./security-models.md). Both connection modes are compatible with either security model.
::::

The choice between proxy and sniff mode depends on your network architecture and deployment type.  

- **Self-managed clusters:** If direct connections on the publish addresses between {{es}} nodes in both clusters are possible, you can use sniff mode. If direct connectivity is difficult to implement—for example, when clusters are separated by NAT, firewalls, or containerized environments—you can place a reverse proxy or load balancer in front of the remote cluster and use proxy mode instead.  

- **Managed environments ({{ece}}, {{ech}}, {{eck}}):** Direct node-to-node connectivity is generally not feasible, so these deployments always rely on the proxy connection mode.

The following sections describe each method in more detail.

## Proxy mode

In proxy mode, a cluster alias is registered with a name of your choosing and the address of a TCP (layer 4) reverse proxy specified with the `cluster.remote.<cluster_alias>.proxy_address` setting. You must configure this proxy to route connections to one or more nodes of the remote cluster. The service port to forward traffic to depends on the [security model](./security-models.md) in use, as each model uses a different service port.

When you register a remote cluster using proxy mode, {{es}} opens several TCP connections to the proxy address and uses these connections to communicate with the remote cluster. In proxy mode, {{es}} disregards the publish addresses of the remote cluster nodes, which means that the publish addresses of the remote cluster nodes do not need to be accessible to the local cluster.

Proxy mode is not the default connection mode when adding remotes using the {{es}} API, so you must set `cluster.remote.<cluster_alias>.mode: proxy` to use it. Refer to [Proxy mode remote cluster settings](elasticsearch://reference/elasticsearch/configuration-reference/remote-clusters.md#remote-cluster-proxy-settings) for more information about configuring proxy mode.

::::{note}
Remote clusters configured through **{{kib}}** support only proxy mode. You can’t select a connection mode or configure sniff mode from the UI.
::::

## Sniff mode

In sniff mode, a cluster alias is registered with a name of your choosing and a list of addresses of *seed* nodes specified with the `cluster.remote.<cluster_alias>.seeds` setting. When you register a remote cluster using sniff mode, {{es}} retrieves from one of the seed nodes the addresses of up to three *gateway nodes*. Each `remote_cluster_client` node in the local {{es}} cluster then opens several TCP connections to the publish addresses of the gateway nodes. This mode therefore requires that the gateway nodes' publish addresses are accessible to nodes in the local cluster.

Sniff mode is the default connection mode when adding a remote cluster through the {{es}} API. Refer to [Sniff mode remote cluster settings](elasticsearch://reference/elasticsearch/configuration-reference/remote-clusters.md#remote-cluster-sniff-settings) for more information about configuring sniff mode.
