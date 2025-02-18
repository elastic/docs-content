---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-configure-deployment-settings.html
---

# What deployment settings are available? [ec-configure-deployment-settings]

The following deployment settings are available:


## Cloud provider [ec_cloud_provider] 

Selects a cloud platform where your {{es}} clusters and {{kib}} instances will be hosted. Elasticsearch Service currently supports Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure.


## Region [ec_region] 

Regions represent data centers in a geographic location, where your deployment will be located. When choosing a region, the general rule is to choose one as close to your application servers as possible in order to minimize network delays.

::::{tip} 
You can select your cloud platform and region only when you create a new deployment, so pick ones that works for you. They cannot be changed later. Different deployments can use different platforms and regions.
::::



## Hardware profile [ec-hardware-profiles] 

Elastic Cloud deploys Elastic Stack components into a *hardware profile* which provides a unique blend of storage, memory and vCPU. This gives you more flexibility to choose the hardware profile that best fits for your use case. For example, *Compute Optimized* deploys Elasticsearch on virtual hardware that provides high [vCPU](../../monitor/monitoring-data/ec-vcpu-boost-instance.md) which can help search-heavy use cases return queries quickly.

Under the covers, hardware profiles leverage virtualized instances from a cloud provider, such as Amazon Web Services, Google Compute Platform, and Microsoft Azure. You don’t interact with the cloud provider directly, but we do document what we use for your reference. To learn more, check [Elasticsearch Service Hardware](https://www.elastic.co/guide/en/cloud/current/ec-reference-hardware.html).

The components of the Elastic Stack that we support as part of a deployment are called *instances* and include:

* Elasticsearch data tiers and master nodes
* Machine Learning (ML) nodes
* Kibana instances
* APM and Fleet instances
* Integrations Server instances

When you [create your deployment](create-an-elastic-cloud-hosted-deployment.md), you can choose the hardware profile that best fits your needs, and configure it with the **Advanced settings** option. Depending on the cloud provider that you select, you can adjust the size of Elasticsearch nodes, or configure your Kibana and APM & Fleet instances. As your usage evolves, you can [change the hardware profile](ec-change-hardware-profile.md) of your deployment.

::::{note} 
Elastic Agent, Beats, and Logstash are components of the Elastic Stack that are not included in the hardware profiles as they are installed outside of Elastic Cloud.
::::



## Version [ec_version] 

Elastic Stack uses a versions code that is constructed of three numbers separated by dots: the leftmost number is the number of the major release, the middle number is the number of the minor release and the rightmost number is the number of the maintenance release (e.g., 8.3.2 means major release 8, minor release 3 and maintenance release 2).

You might sometimes notice additional versions listed in the user interface beyond the versions we currently support and maintain, such as [release candidate builds](available-stack-versions.md#ec-release-builds) and older versions. If a version is listed in the [Elasticsearch Service Console](https://cloud.elastic.co?page=docs&placement=docs-body), it can be deployed.

To learn about how we support {{es}} versions in Elasticsearch Service, check [Version Policy](available-stack-versions.md).

You can always upgrade {{es}} versions, but you cannot downgrade. To learn more about upgrading versions of {{es}} and best practices for major version upgrades, check [Version Upgrades](../../upgrade/deployment-or-cluster.md).


## Snapshot source [ec_snapshot_source] 

To create a deployment from a snapshot, select the snapshot source. You need to [configure snapshots](../../tools/snapshot-and-restore.md) and establish a snapshot lifecycle management policy and repository before you can restore from a snapshot. The snapshot options depend on the stack version the deployment is running.


## Name [ec_name] 

This setting allows you to assign a more human-friendly name to your cluster which will be used for future reference in the [Elasticsearch Service Console](https://cloud.elastic.co?page=docs&placement=docs-body). Common choices are dev, prod, test, or something more domain specific.

