---
applies:
  ece:
navigation_title: Elastic Cloud Enterprise
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-enable-ccs.html
---

# Remote clusters with {{ece}} [ece-enable-ccs]

You can configure an {{ece}} deployment to remotely access or (be accessed by) a cluster from:

* Another deployment of your ECE installation
* A deployment running on a different ECE installation
* An {{ech}} deployment
* A deployment running on an {{eck}} installation
* A self-managed installation


## Prerequisites [ece-ccs-ccr-prerequisites]

To use CCS or CCR, your environment must meet the following criteria:

* Local and remote clusters must be in compatible versions. Review the [{{es}} version compatibility](https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters-cert.html#remote-clusters-prerequisites-cert) table.

    * System deployments cannot be used as remote clusters or have remote clusters.

* Proxies must answer TCP requests on the port 9400. Check the [prerequisites for the ports that must permit outbound or inbound traffic](../deploy/cloud-enterprise/ece-networking-prereq.md).
* Load balancers must pass-through TCP requests on port 9400. Check the [configuration details](../deploy/cloud-enterprise/ece-load-balancers.md).

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
    * [From an {{ech}} deployment](https://www.elastic.co/guide/en/cloud/current/ec-remote-cluster-ece.html)
    * [From a self-managed cluster](https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters.html)



## Enable Remote clusters in {{kib}} [ece-enable-ccr]

If your deployment was created before ECE version `2.9.0`, the Remote clusters page in {kib} must be enabled manually from the **Security** page of your deployment, by selecting **Enable CCR** under **Trust management**.


## Remote clusters and traffic filtering [ece-ccs-ccr-traffic-filtering]

::::{note}
Traffic filtering isn’t supported for cross-cluster operations initiated from an {{ece}} environment to a remote {{ech}} deployment.
::::


For remote clusters configured using TLS certificate authentication, [traffic filtering](../security/traffic-filtering.md) can be enabled to restrict access to deployments that are used as a local or remote cluster without any impact to cross-cluster search or cross-cluster replication.

Traffic filtering for remote clusters supports 2 methods:

* [Filtering by IP addresses and Classless Inter-Domain Routing (CIDR) masks](../security/ip-traffic-filtering.md)
* Filtering by Organization or {{es}} cluster ID with a Remote cluster type filter. You can configure this type of filter from the **Platform** > **Security** page of your environment or using the [{{ece}} API](https://www.elastic.co/docs/api/doc/cloud-enterprise) and apply it from each deployment’s **Security** page.

::::{note}
When setting up traffic filters for a remote connection to an {{ece}} environment, you also need to upload the region’s TLS certificate of the local cluster to the {{ece}} environment’s proxy. You can find that region’s TLS certificate in the Security page of any deployment of the environment initiating the remote connection.
::::
