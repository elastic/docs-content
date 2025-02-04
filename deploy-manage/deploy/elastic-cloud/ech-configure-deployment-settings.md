---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-configure-deployment-settings.html
---

# What deployment settings are available? [ech-configure-deployment-settings]

The following deployment settings are available:


## Cloud provider [echcloud_provider] 

Selects a cloud platform where your {{es}} clusters, {{kib}} instance, and other {{stack}} components will be hosted. Elasticsearch Add-On for Heroku currently supports Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure.


## Region [echregion] 

Regions represent data centers in a geographic location, where your deployment will be located. When choosing a region, the general rule is to choose one as close to your application servers as possible in order to minimize network delays.

::::{tip} 
You can select your cloud platform and region only when you create a new deployment, so pick ones that works for you. They cannot be changed later. Different deployments can use different platforms and regions.
::::



## Version [echversion] 

Elastic Stack uses a versions code that is constructed of three numbers separated by dots: the leftmost number is the number of the major release, the middle number is the number of the minor release and the rightmost number is the number of the maintenance release (e.g., 8.3.2 means major release 8, minor release 3 and maintenance release 2).

You might sometimes notice additional versions listed in the user interface beyond the versions we currently support and maintain, such as [release candidate builds](ech-version-policy.md#ech-release-builds) and older versions. If a version is listed in the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body), it can be deployed.

To learn about how we support {{es}} versions in Elasticsearch Add-On for Heroku, check [Version Policy](ech-version-policy.md).

You can always upgrade {{es}} versions, but you cannot downgrade. To learn more about upgrading versions of {{es}} and best practices for major version upgrades, check [Version Upgrades](../../upgrade/deployment-or-cluster.md).


## Snapshot source [echsnapshot_source] 

To create a deployment from a snapshot, select the snapshot source. You need to [configure snapshots](../../tools/snapshot-and-restore.md) and establish a snapshot lifecycle management policy and repository before you can restore from a snapshot. The snapshot options depend on the stack version the deployment is running.


## Name [echname] 

This setting allows you to assign a more human-friendly name to your cluster which will be used for future reference in the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body). Common choices are dev, prod, test, or something more domain specific.

