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

### Filter types for remote clusters traffic

Network security for remote cluster incoming connections using API key authentication supports two types of filters:

* [IP filters](/deploy-manage/security/ip-filtering.md), which allow traffic based on IP addresses or CIDR ranges. These can be difficult to manage in orchestrated environments, where the source IP of individual {{es}} instances may change.  
* [Remote cluster filters](/deploy-manage/security/remote-cluster-filtering.md), which allow filtering by organization ID or {{es}} cluster ID. This method is more reliable and recommended, as it combines mTLS with API key authentication for stronger security.

### Use cases for remote clusters and network security [use-cases-network-security]

Network security is supported to control remote cluster traffic in the following scenarios:

* Local and remote clusters are {{ech}} deployments in the same organization
* Local and remote clusters are {{ech}} deployments in different organizations 
* Local and remote clusters are {{ece}} deployments in the same ECE environment
* Local and remote clusters are {{ece}} deployments in different ECE environments
* The local deployment is on {{ech}} and the remote deployment is on an {{ece}} environment

::::{note}
Network security isn’t supported for cross-cluster operations initiated from an {{ece}} environment to a remote {{ech}} deployment.
::::

Refer to [Remote cluster filtering](/deploy-manage/security/remote-cluster-filtering.md) for instructions on creating and applying remote cluster filters in ECH or ECE.