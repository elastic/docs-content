---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-enable-ccs.html
---

# Enable cross-cluster search and cross-cluster replication [ece-enable-ccs]

[Cross-cluster search (CCS)](/solutions/search/cross-cluster-search.md) allows you to configure multiple remote clusters across different locations and to enable federated search queries across all of the configured remote clusters.

[Cross-cluster replication (CCR)](/deploy-manage/tools/cross-cluster-replication.md) allows you to replicate indices across multiple remote clusters regardless of where they’re located. This provides tremendous benefit in scenarios of disaster recovery or data locality.

These remote clusters could be:

* Another {{es}} cluster of your ECE installation
* An {{es}} cluster in a remote ECE installation
* An {{es}} cluster hosted on {{ecloud}}
* Any other self-managed {{es}} cluster


## Prerequisites [ece-ccs-ccr-prerequisites]

To use CCS or CCR, your environment must meet the following criteria:

* Local and remote clusters must be in compatible versions. Review the [{{es}} version compatibility](/deploy-manage/remote-clusters/remote-clusters-cert.md#remote-clusters-prerequisites-cert) table.

    * System deployments cannot be used as remote clusters or have remote clusters.

* Proxies must answer TCP requests on the port 9400. Check the [prerequisites for the ports that must permit outbound or inbound traffic](../deploy/cloud-enterprise/ece-networking-prereq.md).
* Load balancers must pass-through TCP requests on port 9400. Check the [configuration details](../deploy/cloud-enterprise/ece-load-balancers.md).

The steps, information, and authentication method required to configure CCS and CCR can vary depending on where the clusters you want to use as remote are hosted.

* Connect remotely to other clusters from your Elastic Cloud Enterprise deployments

    * [Access other deployments of the same Elastic Cloud Enterprise environment](ece-remote-cluster-same-ece.md)
    * [Access deployments of a different Elastic Cloud Enterprise environment](ece-remote-cluster-other-ece.md)
    * [Access deployments of an {{ess}} environment](ece-remote-cluster-ece-ess.md)
    * [Access clusters of a self-managed environment](ece-remote-cluster-self-managed.md)
    * [Access deployments of an ECK environment](ece-enable-ccs-for-eck.md)

* Use clusters from your Elastic Cloud Enterprise deployments as remote

    * [From another deployment of the same Elastic Cloud Enterprise environment](ece-remote-cluster-same-ece.md)
    * [From a deployment of another Elastic Cloud Enterprise environment](ece-remote-cluster-other-ece.md)
    * [From an {{ess}} deployment](/deploy-manage/remote-clusters/ec-remote-cluster-ece.md)
    * [From a self-managed cluster](/deploy-manage/remote-clusters/remote-clusters-self-managed.md)



## Enable CCR and the Remote Clusters UI in Kibana [ece-enable-ccr]

If your deployment was created before ECE version `2.9.0`, CCR won’t be enabled by default and you won’t find the Remote Clusters UI in Kibana even though your deployment meets all the [criteria](#ece-ccs-ccr-prerequisites).

To enable these features, go to the **Security** page of your deployment and under **Trust management** select **Enable CCR**.


## Remote clusters and traffic filtering [ece-ccs-ccr-traffic-filtering]

::::{note}
Traffic filtering isn’t supported for cross-cluster operations initiated from an {{ece}} environment to a remote {{ess}} deployment.
::::


For remote clusters configured using TLS certificate authentication, [traffic filtering](../security/traffic-filtering.md) can be enabled to restrict access to deployments that are used as a local or remote cluster without any impact to cross-cluster search or cross-cluster replication.

Traffic filtering for remote clusters supports 2 methods:

* [Filtering by IP addresses and Classless Inter-Domain Routing (CIDR) masks](../security/ip-traffic-filtering.md)
* Filtering by Organization or Elasticsearch cluster ID with a Remote cluster type filter. You can configure this type of filter from the **Platform** > **Security** page of your environment or using the [Elastic Cloud Enterprise API](https://www.elastic.co/docs/api/doc/cloud-enterprise) and apply it from each deployment’s **Security** page.

::::{note}
When setting up traffic filters for a remote connection to an {{ece}} environment, you also need to upload the region’s TLS certificate of the local cluster to the {{ece}} environment’s proxy. You can find that region’s TLS certificate in the Security page of any deployment of the environment initiating the remote connection.
::::
