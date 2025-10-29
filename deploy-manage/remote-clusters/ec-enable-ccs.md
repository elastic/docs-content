---
navigation_title: On Elastic Cloud Hosted
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-enable-ccs.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Remote clusters on {{ech}} [ec-enable-ccs]

You can configure an {{ech}} deployment to either connect to remote clusters or accept connections from:

* Another {{ech}} deployment of your {{ecloud}} organization, across any region or cloud provider (AWS, GCP, Azure…)
* An {{ech}} deployment of another {{ecloud}} organization
* A deployment in an {{ece}} installation
* A deployment in an {{eck}} installation
* A self-managed installation.

::::{note}
Refer to [Remote clusters and network security](/deploy-manage/remote-clusters.md#network-security) for details on how remote clusters interact with network security policies and the implications for your deployments.
::::


## Prerequisites [ec-ccs-ccr-prerequisites]

To use CCS or CCR, your deployments must meet the following criteria:

* The local and remote clusters must run on compatible versions of {{es}}. Review the version compatibility table.
  
  :::{include} _snippets/remote-cluster-certificate-compatibility.md
  :::

* If your deployment was created before February 2021, the **Remote clusters** page in {{kib}} must be enabled manually from the **Security** page of your deployment, by selecting **Enable CCR** under **Trust management**.

## Set up remote clusters with {{ech}}

The steps, information, and authentication method required to configure CCS and CCR can vary depending on where the clusters you want to use as remote are hosted.

* Connect remotely to other clusters from your {{ech}} deployments

    * [Access other deployments of the same {{ecloud}} organization](ec-remote-cluster-same-ess.md)
    * [Access deployments of a different {{ecloud}} organization](ec-remote-cluster-other-ess.md)
    * [Access deployments of an {{ECE}} environment](ec-remote-cluster-ece.md)
    * [Access clusters of a self-managed environment](ec-remote-cluster-self-managed.md)
    * [Access deployments of an ECK environment](ec-enable-ccs-for-eck.md)

* Use clusters from your {{ech}} deployments as remote

    * [From another deployment of your {{ecloud}} organization](ec-remote-cluster-same-ess.md)
    * [From a deployment of another {{ecloud}} organization](ec-remote-cluster-other-ess.md)
    * [From an ECE deployment](ece-remote-cluster-ece-ess.md)
    * [From a self-managed cluster](remote-clusters-self-managed.md)
    * [From an ECK environment](ec-enable-ccs-for-eck.md)

## Remote clusters and network security [ec-ccs-ccr-network-security]

If you have [network security policies](/deploy-manage/security/network-security-policies.md) applied to the remote cluster, you might need to take extra steps on the remote side to allow traffic from the local cluster. Some remote cluster configurations have limited compatibility with network security. To learn more, refer to [Remote clusters and network security](/deploy-manage/remote-clusters.md#network-security).