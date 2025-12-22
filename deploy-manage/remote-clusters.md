---
applies_to:
  deployment:
    ece: ga
    eck: ga
    ess: ga
    self: ga
  serverless: unavailable
---

# Remote clusters [remote-clusters]

By setting up **remote clusters**, you can connect an {{es}} cluster to other {{es}} clusters. Remote clusters can be located in different data centers, geographic regions, and run on a different type of environment: {{ech}}, {{ece}}, {{eck}}, or self-managed.

Remote clusters are especially useful in two cases:

- **Cross-cluster replication**
  With [cross-cluster replication](/deploy-manage/tools/cross-cluster-replication.md), or CCR, you ingest data to an index on a remote cluster. This leader index is replicated to one or more read-only follower indices on your local cluster. Creating a multi-cluster architecture with cross-cluster replication enables you to configure disaster recovery, bring data closer to your users, or establish a centralized reporting cluster to process reports locally.

- **Cross-cluster search**
  [Cross-cluster search](/explore-analyze/cross-cluster-search.md), or CCS, enables you to run a search request against one or more remote clusters. This capability provides each region with a global view of all clusters, allowing you to send a search request from a local cluster and return results from all connected remote clusters. For full {{ccs}} capabilities, the local and remote cluster must be on the same [subscription level](https://www.elastic.co/subscriptions).

:::{include} ./remote-clusters/_snippets/terminology.md
:::

## Security models and connection modes

When configuring remote clusters, you can choose between two security models and two connection modes. Both security models are compatible with either connection mode.

- [Security models](./remote-clusters/security-models.md): API key–based authentication (recommended) or TLS certificate–based authentication (deprecated).
- [Connection modes](./remote-clusters/connection-modes.md): Sniff mode (direct connections to {{es}} nodes) or proxy mode (connections through a reverse proxy or load balancer endpoint).

::::{note}
In managed or orchestrated environments, such as {{ech}}, {{ece}}, and {{eck}}, you can select the security model, but the connection mode is effectively limited to *proxy*. This is because sniff mode requires {{es}} nodes publish addresses to be directly reachable across clusters, which is generally not practical in containerized deployments.
::::

## Setup

Depending on the environment the local and remote clusters are deployed on and the security model you wish to use, the exact details needed to add a remote cluster vary but generally follow the same path:

1. **Configure trust between clusters.** In the settings of the local deployment or cluster, configure the trust security model that your remote connections will use to access the remote cluster. This step involves specifying API keys or certificates retrieved from the remote clusters.

2. **Establish the connection.** In {{kib}} on the local cluster, finalize the connection by specifying each remote cluster's details.

Find the instructions with details on the supported security models and available connection modes for your specific scenario:

- [Remote clusters on {{ech}}](remote-clusters/ec-enable-ccs.md)
- [Remote clusters on {{ece}}](remote-clusters/ece-enable-ccs.md)
- [Remote clusters on {{eck}}](remote-clusters/eck-remote-clusters.md)
- [Remote clusters on self-managed installations](remote-clusters/remote-clusters-self-managed.md)

## Remote clusters and network security [network-security]
```{applies_to}
deployment:
  ece: ga
  ess: ga
```

In {{ech}} (ECH) and {{ece}} (ECE), the remote clusters functionality interacts with [network security](/deploy-manage/security/network-security.md) traffic filtering rules in different ways, depending on the [security model](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#remote-clusters-security-models) you use.

* **TLS certificate–based authentication (deprecated):**
  For remote clusters configured using the TLS certificate–based security model, network security policies or rule sets have no effect on remote clusters functionality. Connections established with this method (mTLS) are already considered secure and are always accepted, regardless of any filtering policies or rule sets applied on the local or remote deployment to restrict other traffic.

* **API key–based authentication (recommended):**
  When remote clusters use the API key–based authentication model, network security policies or rule sets on the **destination (remote) deployment** do affect remote cluster functionality if enabled. In this case, you can use traffic filters to explicitly control which deployments are allowed to connect to the remote cluster service endpoint.

  ::::{note}
  Because of [how network security works](/deploy-manage/security/network-security.md#how-network-security-works):
    * If network security is disabled, all traffic is allowed by default, and remote clusters work without requiring any specific filtering policy.
    * If network security is enabled on the remote cluster, apply a [remote cluster filter](/deploy-manage/security/remote-cluster-filtering.md#create-remote-cluster-filter) to allow incoming connections from the local clusters. Without this filter, the connections are blocked.
  ::::

This section explains how remote clusters interact with network security when using API key–based authentication, and describes the supported use cases.

### Filter types and supported use cases for remote cluster traffic [use-cases-network-security]

With API key–based authentication, remote clusters require the local cluster (A) to trust the transport SSL certificate presented by the remote cluster server (B). When network security is enabled on the destination cluster (B), it’s also necessary to explicitly allow the incoming traffic from cluster A. This can be achieved using different types of traffic filters:

* [Remote cluster filters](/deploy-manage/security/remote-cluster-filtering.md), available exclusively in ECH and ECE. They allow filtering by organization ID or {{es}} cluster ID and are the recommended option, as they combine mTLS with API key authentication for stronger security.

* [IP filters](/deploy-manage/security/ip-filtering.md), which allow traffic based on IP addresses or CIDR ranges.

The applicable filter type for the remote cluster depends on the local and remote deployment types:

| Remote cluster → <br>Local cluster ↓  | Elastic Cloud Hosted | Elastic Cloud Enterprise | Self-managed / Elastic Cloud on Kubernetes |
|-------------------------|----------------------|--------------------------|--------------------------------------------|
| **Elastic Cloud Hosted** | [Remote cluster filter](/deploy-manage/security/remote-cluster-filtering.md) | [IP filter](/deploy-manage/security/ip-filtering.md) | [IP filter](/deploy-manage/security/ip-filtering.md) or [Kubernetes network policy](/deploy-manage/security/k8s-network-policies.md) |
| **Elastic Cloud Enterprise** | [IP filter](/deploy-manage/security/ip-filtering.md) | [Remote cluster filter](/deploy-manage/security/remote-cluster-filtering.md) / [IP filter](/deploy-manage/security/ip-filtering.md) (\*) | [IP filter](/deploy-manage/security/ip-filtering.md) or [Kubernetes network policy](/deploy-manage/security/k8s-network-policies.md) |
| **Self-managed / Elastic Cloud on Kubernetes** | [IP filter](/deploy-manage/security/ip-filtering.md) | [IP filter](/deploy-manage/security/ip-filtering.md) | [IP filter](/deploy-manage/security/ip-filtering.md) or [Kubernetes network policy](/deploy-manage/security/k8s-network-policies.md) |

(*) For ECE, remote cluster filters apply when both clusters are in the **same environment**. Use IP filters when the clusters belong to **different environments**.

::::{note}
When using self-managed security mechanisms (such as firewalls), keep in mind that remote clusters with API key–based authentication use port `9443` by default. Specify this port if a destination port is required.
::::