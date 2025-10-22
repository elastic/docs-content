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
  [Cross-cluster search](/solutions/search/cross-cluster-search.md), or CCS, enables you to run a search request against one or more remote clusters. This capability provides each region with a global view of all clusters, allowing you to send a search request from a local cluster and return results from all connected remote clusters. For full {{ccs}} capabilities, the local and remote cluster must be on the same [subscription level](https://www.elastic.co/subscriptions).

::::{note} about terminology
In the case of remote clusters, the {{es}} cluster or deployment initiating the connection and requests is often referred to as the **local cluster**, while the {{es}} cluster or deployment receiving the requests is referred to as the **remote cluster**.
::::

## Security models and connection modes

When configuring remote clusters, you can choose between two security models and two connection modes. Both security models are compatible with either connection mode.

You can learn more in the following documents:

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

- [Remote clusters with {{ech}}](remote-clusters/ec-enable-ccs.md)
- [Remote clusters with {{ece}}](remote-clusters/ece-enable-ccs.md)
- [Remote clusters with {{eck}}](remote-clusters/eck-remote-clusters.md)
- [Remote clusters with self-managed installations](remote-clusters/remote-clusters-self-managed.md)