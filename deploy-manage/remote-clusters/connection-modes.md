---
navigation_title: Connection modes
applies_to:
  deployment:
    ece: ga
    ess: ga
    eck: ga
    self: ga
  serverless: unavailable
products:
  - id: elasticsearch
---
# Remote cluster connection modes

When you configure a remote cluster, the local cluster needs a way to connect to the nodes of the remote cluster. {{es}} supports two connection modes to handle different network architectures:

- **Sniff mode**: The local cluster discovers the remote cluster’s gateway nodes and connects to them directly.
- **Proxy mode**: The local cluster connects through a reverse proxy or load balancer, which forwards traffic to the appropriate nodes in the remote cluster.

::::{note}
Connection modes work independently of [security models](./security-models.md). Both connection modes are compatible with either security model.
::::

The choice between sniff and proxy mode depends on your network architecture and deployment type.  

- **Self-managed clusters:** If direct connections on the publish addresses between {{es}} nodes in both clusters are possible, you can use sniff mode. If direct connectivity is difficult to implement—for example, when clusters are separated by NAT, firewalls, or containerized environments—you can place a reverse proxy or load balancer in front of the remote cluster and use proxy mode instead.  

- **Managed environments ({{ece}}, {{ech}}, {{eck}}):** Direct node-to-node connectivity is generally not feasible, so these deployments always rely on the proxy connection mode.


The following sections describe each method in more detail.

## Sniff mode
```{applies_to}
deployment:
  self: ga
```

In sniff mode, a cluster alias is registered with a name of your choosing and a list of addresses of *seed* nodes specified with the `cluster.remote.<cluster_alias>.seeds` setting. When you register a remote cluster using sniff mode, {{es}} retrieves from one of the seed nodes the addresses of up to three *gateway nodes*. Each `remote_cluster_client` node in the local {{es}} cluster then opens several TCP connections to the publish addresses of the gateway nodes. This mode therefore requires that the gateway nodes' publish addresses are accessible to nodes in the local cluster.

Sniff mode is the default connection mode when adding a remote cluster. See [Sniff mode remote cluster settings](remote-clusters-settings.md#remote-cluster-sniff-settings) for more information about configuring sniff mode.

::::{note}
Sniff mode is not supported in {{ech}} and {{ece}} deployments. In {{eck}}, sniff mode is not recommended due to its complexity. In these three cases, use proxy mode instead.
::::


## Proxy mode

In proxy mode, a cluster alias is registered with a name of your choosing and the address of a TCP (layer 4) reverse proxy specified with the `cluster.remote.<cluster_alias>.proxy_address` setting. You must configure this proxy to route connections to one or more nodes of the remote cluster. The service port to forward traffic to depends on the [security model](./security-models.md) in use, as each model uses a different service port.

When you register a remote cluster using proxy mode, {{es}} opens several TCP connections to the proxy address and uses these connections to communicate with the remote cluster. In proxy mode, {{es}} disregards the publish addresses of the remote cluster nodes, which means that the publish addresses of the remote cluster nodes do not need to be accessible to the local cluster.

Proxy mode is not the default connection mode, so you must set `cluster.remote.<cluster_alias>.mode: proxy` to use it. See [Proxy mode remote cluster settings](remote-clusters-settings.md#remote-cluster-proxy-settings) for more information about configuring proxy mode.

## Connection mode comparison

The following table summarizes the key differences between sniff and proxy mode to help you choose the most suitable option for your deployment.

| Aspect                  | Sniff mode                                                                                       | Proxy mode                                                                                   |
|-------------------------|--------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| **Default when adding a remote**             | Yes                                                                                              | No (must be explicitly configured)                                                           |
| **Recommended deployment types**    | Self-managed                                                                                     | Self-managed, {{ech}}, {{ece}}, and {{eck}}                                                  |
| **How it connects**     | Local cluster connects directly to remote node addresses, discovered from the configured seeds   | Local cluster connects to a single configured address. The reverse proxy or load balancer forwards traffic to remote nodes. |
| **Node discovery**      | Dynamic: local cluster discovers remote gateway nodes through the seed list                      | None: all traffic goes through the reverse proxy                                                |
| **Network requirements**| Local cluster must be able to reach the remote cluster’s gateway node publish addresses          | Only the proxy address must be reachable; no need for local cluster to connect directly to remote nodes |
| **Configuration**       | Configure remote seeds (`cluster.remote.<alias>.seeds`)                                          | Configure proxy address (`cluster.remote.<alias>.proxy_address`) and set mode to `proxy`      |
| **Use cases**           | Clusters with direct network reachability between nodes (e.g., same VPC or peered networks)      | Clusters separated by firewalls, NAT, or when exposing only a single ingress point is required |
