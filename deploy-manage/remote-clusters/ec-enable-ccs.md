---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-enable-ccs.html
---

# Enable cross-cluster search and cross-cluster replication [ec-enable-ccs]

[Cross-cluster search (CCS)](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cross-cluster-search.html) allows you to configure multiple remote clusters across different locations and to enable federated search queries across all of the configured remote clusters.

[Cross-cluster replication (CCR)](https://www.elastic.co/guide/en/elasticsearch/reference/current/xpack-ccr.html) allows you to replicate indices across multiple remote clusters regardless of where they’re located. This provides tremendous benefit in scenarios of disaster recovery or data locality.

These remote clusters could be:

* Another {{es}} cluster of your {{ecloud}} organization across any region or cloud provider (AWS, GCP, Azure…​)
* An {{es}} cluster of another {{ecloud}} organization
* An {{es}} cluster in an {{ece}} installation
* Any other self-managed {{es}} cluster


## Prerequisites [ec-ccs-ccr-prerequisites]

To use CCS or CCR, your deployments must meet the following criteria:

* Local and remote clusters must be in compatible versions. Review the [{{es}} version compatibility](https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters-cert.html#remote-clusters-prerequisites-cert) table.

The steps, information, and authentication method required to configure CCS and CCR can vary depending on where the clusters you want to use as remote are hosted.

* Connect remotely to other clusters from your Elasticsearch Service deployments

    * [Access other deployments of the same Elasticsearch Service organization](ec-remote-cluster-same-ess.md)
    * [Access deployments of a different Elasticsearch Service organization](ec-remote-cluster-other-ess.md)
    * [Access deployments of an {{ECE}} environment](ec-remote-cluster-ece.md)
    * [Access clusters of a self-managed environment](ec-remote-cluster-self-managed.md)
    * [Access deployments of an ECK environment](ec-enable-ccs-for-eck.md)

* Use clusters from your Elasticsearch Service deployments as remote

    * [From another deployment of your Elasticsearch Service organization](ec-remote-cluster-same-ess.md)
    * [From a deployment of another Elasticsearch Service organization](ec-remote-cluster-other-ess.md)
    * [From an ECE deployment](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-enable-ccs.html)
    * [From a self-managed cluster](https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters.html)



## Enable CCR and the Remote Clusters UI in Kibana [ec-enable-ccr]

If your deployment was created before February 2021, CCR won’t be enabled by default and you won’t find the Remote Clusters UI in Kibana even though your deployment meets all the [criteria](#ec-ccs-ccr-prerequisites).

To enable these features, go to the **Security** page of your deployment and under **Trust management** select **Enable CCR**.

::::{note}
CCR is not supported for indices used by Enterprise Search.
::::



## Remote clusters and traffic filtering [ec-ccs-ccr-traffic-filtering]

::::{note}
Traffic filtering isn’t supported for cross-cluster operations initiated from an {{ece}} environment to a remote {{ess}} deployment.
::::


For remote clusters configured using TLS certificate authentication, [traffic filtering](../security/traffic-filtering.md) can be enabled to restrict access to deployments that are used as a local or remote cluster without any impact to cross-cluster search or cross-cluster replication.

Traffic filtering for remote clusters supports 2 methods:

* [Filtering by IP addresses and Classless Inter-Domain Routing (CIDR) masks](../security/ip-traffic-filtering.md)
* Filtering by Organization or Elasticsearch cluster ID with a Remote cluster type filter. You can configure this type of filter from the **Features** > **Traffic filters** page of your organization or using the [Elasticsearch Service API](https://www.elastic.co/docs/api/doc/cloud) and apply it from each deployment’s **Security** page.

::::{note}
When setting up traffic filters for a remote connection to an {{ece}} environment, you also need to upload the region’s TLS certificate of the local cluster to the {{ece}} environment’s proxy. You can find that region’s TLS certificate in the Security page of any deployment of the environment initiating the remote connection.
::::
