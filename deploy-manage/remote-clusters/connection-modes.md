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
# Remote clusters connection modes

When you configure a remote cluster, the local cluster needs a way to connect to the nodes of the remote cluster. {{es}} supports two connection modes to handle different network architectures:

- **Sniff mode**: The local cluster discovers the remote cluster’s gateway nodes and connects to them directly.
- **Proxy mode**: The local cluster connects through a reverse proxy or load balancer, which forwards traffic to the appropriate nodes in the remote cluster.

The choice between sniff and proxy mode depends on your network architecture and deployment type.  

- **Self-managed environments:** If direct connections on the publish addresses between {{es}} nodes in both clusters are possible, you can use sniff mode. If direct connectivity is difficult to implement—for example, when clusters are separated by NAT, firewalls, or containerized environments—you can place a reverse proxy or load balancer in front of the remote cluster and use proxy mode instead.  

- **Managed environments ({{ece}}, {{ech}}, {{eck}}):** Direct node-to-node connectivity is generally not feasible, so these deployments always rely on the proxy connection mode.

::::{note}
Connection modes are independent of [security models](./security-models.md). Connection modes define *how* the local cluster reaches the remote cluster (directly to node publish addresses or through a reverse proxy/load balancer), while security models determine *which service* is used and *how authentication and authorization* are handled between the clusters.
::::

The following sections describe each method in more detail.

## Sniff mode
```{applies_to}
deployment:
  self: ga
```

In sniff mode, a cluster alias is registered with a name of your choosing and a list of addresses of *seed* nodes specified with the `cluster.remote.<cluster_alias>.seeds` setting. When you register a remote cluster using sniff mode, {{es}} retrieves from one of the seed nodes the addresses of up to three *gateway nodes*. Each `remote_cluster_client` node in the local {{es}} cluster then opens several TCP connections to the publish addresses of the gateway nodes. This mode therefore requires that the gateway nodes' publish addresses are accessible to nodes in the local cluster.

Sniff mode is the default connection mode when adding a remote cluster. See [Sniff mode remote cluster settings](remote-clusters-settings.md#remote-cluster-sniff-settings) for more information about configuring sniff mode.

::::{note}
The sniff mode is not supported in {{ech}} and {{ece}} deployments, and it's not recommended in {{eck}} due to its complexity. Use proxy mode instead.
::::


## Proxy mode

In proxy mode, a cluster alias is registered with a name of your choosing and the address of a TCP (layer 4) reverse proxy specified with the `cluster.remote.<cluster_alias>.proxy_address` setting. You must configure this proxy to route connections to one or more nodes of the remote cluster. When you register a remote cluster using proxy mode, {{es}} opens several TCP connections to the proxy address and uses these connections to communicate with the remote cluster. In proxy mode {{es}} disregards the publish addresses of the remote cluster nodes which means that the publish addresses of the remote cluster nodes do not need to be accessible to the local cluster.

Proxy mode is not the default connection mode, so you must set `cluster.remote.<cluster_alias>.mode: proxy` to use it. See [Proxy mode remote cluster settings](remote-clusters-settings.md#remote-cluster-proxy-settings) for more information about configuring proxy mode.

## Connection modes: comparison

| Aspect                  | Sniff mode                                                                                       | Proxy mode                                                                                   |
|-------------------------|--------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| **Default**             | Yes                                                                                              | No (must be explicitly configured)                                                           |
| **How it connects**     | Local cluster connects directly to remote gateway node publish addresses discovered from seeds   | Local cluster connects to a single configured address; the reverse proxy or load balancer forwards traffic to remote nodes |
| **Network requirements**| Local cluster must be able to reach the remote cluster’s gateway node publish addresses          | Only the proxy address must be reachable; no need for local cluster to resolve internal remote addresses |
| **Configuration**       | Configure remote seeds (`cluster.remote.<alias>.seeds`)                                          | Configure proxy address (`cluster.remote.<alias>.proxy_address`) and set mode to `proxy`      |
| **Node discovery**      | Dynamic: local cluster discovers remote gateway nodes through the seed list                      | Static: all traffic goes through the reverse proxy                                                   |
| **Deployment types**    | Self-managed                                                                                     | Self-managed, {{ece}}, {{ech}}, and {{eck}}                                                  |
| **Use cases**           | Clusters with direct network reachability between nodes (e.g., same VPC or peered networks)      | Clusters separated by firewalls, NAT, or when exposing only a single ingress point is required |
