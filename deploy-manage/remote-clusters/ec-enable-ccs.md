---
navigation_title: Elastic Cloud Hosted
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-enable-ccs.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Remote clusters with {{ech}} [ec-enable-ccs]

You can configure an {{ech}} deployment to remotely access or (be accessed by) a cluster from:

* Another {{ech}} deployment of your {{ecloud}} organization, across any region or cloud provider (AWS, GCP, Azure…)
* An {{ech}} deployment of another {{ecloud}} organization
* A deployment in an {{ece}} installation
* A deployment in an {{eck}} installation
* A self-managed installation.


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

::::{note}
[Network security](../security/network-security.md) isn’t supported for cross-cluster operations initiated from an {{ece}} environment to a remote {{ech}} deployment.
::::

You can use [network security policies](../security/network-security.md) to restrict access to deployments used as a local or remote cluster, without impacting cross-cluster search or cross-cluster replication.

Network security for remote clusters supports the following methods:

* [Filtering by IP addresses and Classless Inter-Domain Routing (CIDR) masks](../security/ip-filtering.md)
* Filtering by Organization or {{es}} cluster ID with a **Remote cluster** private connection policy. You can configure this type of policy from the **Access and security** > **Network security** page of your organization or using the [{{ecloud}} RESTful API](https://www.elastic.co/docs/api/doc/cloud) and apply it from each deployment’s **Security** page.

::::{note}
When setting up network security policies for a remote connection to an {{ece}} environment, you also need to upload the region’s TLS certificate of the local cluster to the {{ece}} environment’s proxy. You can find that region’s TLS certificate in the **Security** page of any deployment of the environment initiating the remote connection. This is regardless of whether you are using API key or TLS Certificates (deprecated) to authenticate remote connections.
::::
