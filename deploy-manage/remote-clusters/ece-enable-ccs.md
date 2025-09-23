---
navigation_title: On Elastic Cloud Enterprise
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-enable-ccs.html
applies_to:
  deployment:
    ece: ga
products:
  - id: cloud-enterprise
---

# Remote clusters on {{ece}} [ece-enable-ccs]

You can configure an {{ece}} deployment to either connect to remote clusters or accept connections from:

* Another deployment of your ECE installation
* A deployment running on a different ECE installation
* An {{ech}} deployment
* A deployment running on an {{eck}} installation
* A self-managed installation

$$$ece-ccs-ccr-network-security$$$
::::{note}
Refer to [Remote clusters and network security](/deploy-manage/remote-clusters.md#network-security) for details on how remote clusters interact with network security filters and the implications for your deployments.
::::

## Prerequisites [ece-ccs-ccr-prerequisites]

To use CCS or CCR, your environment must meet the following criteria:

* The local and remote clusters must run on compatible versions of {{es}}. Review the version compatibility table.
  
  :::{include} _snippets/remote-cluster-certificate-compatibility.md
  :::
  
* Proxies must answer TCP requests on the port 9400. Check the [prerequisites for the ports that must permit outbound or inbound traffic](../deploy/cloud-enterprise/ece-networking-prereq.md).
* Load balancers must pass-through TCP requests on port 9400. Check the [configuration details](../deploy/cloud-enterprise/ece-load-balancers.md).
* If your deployment was created before ECE version `2.9.0`, the Remote clusters page in {{kib}} must be enabled manually from the **Security** page of your deployment, by selecting **Enable CCR** under **Trust management**.

::::{note}
System deployments cannot be used as remote clusters or have remote clusters.
::::

## Set up remote clusters with {{ece}}

The steps, information, and authentication method required to configure CCS and CCR can vary depending on where the clusters you want to use as remote are hosted.

* Connect remotely to other clusters from your {{ece}} deployments

    * [Access other deployments of the same {{ece}} environment](ece-remote-cluster-same-ece.md)
    * [Access deployments of a different {{ece}} environment](ece-remote-cluster-other-ece.md)
    * [Access deployments of an {{ecloud}} environment](ece-remote-cluster-ece-ess.md)
    * [Access clusters of a self-managed environment](ece-remote-cluster-self-managed.md)
    * [Access deployments of an ECK environment](ece-enable-ccs-for-eck.md)

* Use clusters from your {{ece}} deployments as remote

    * [From another deployment of the same {{ece}} environment](ece-remote-cluster-same-ece.md)
    * [From a deployment of another {{ece}} environment](ece-remote-cluster-other-ece.md)
    * [From an {{ech}} deployment](/deploy-manage/remote-clusters/ec-remote-cluster-ece.md)
    * [From a self-managed cluster](/deploy-manage/remote-clusters/remote-clusters-self-managed.md)
    * [From an ECK environment](ece-enable-ccs-for-eck.md)

## Remote clusters and network security [ece-ccs-ccr-network-security]

If you have [network security filters](/deploy-manage/security/ece-filter-rules.md) applied to your deployment, then you might need to take extra steps to allow a cluster to make requests to your cluster. Some remote cluster configurations are not compatible with network security, including incoming connections from {{eck}} and self-managed clusters. To learn more, refer to [Remote clusters and network security](/deploy-manage/remote-clusters.md#network-security).