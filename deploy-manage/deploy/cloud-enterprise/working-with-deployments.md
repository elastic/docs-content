---
applies_to:
  deployment:
    ece: all
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-stack-getting-started.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-administering-deployments.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-monitoring-deployments.html
---

# Manage deployments [ece-stack-getting-started]

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/339

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece-stack-getting-started.md
%      Notes: 9 child and sub-child docs (some of them are about "adding data to Elasticsearch" which might fit better somewhere else. we need to analyze that. We are missing https://www.elastic.co/guide/en/cloud-enterprise/current/ece-administering-deployments.html.... on purpose?
% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece-administering-deployments.md
%      Notes: probably just a redirect
% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece-change-deployment.md
%      Notes: another redirect
% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece-monitoring-deployments.md
%      Notes: mostly redirect

⚠️ **This page is a work in progress.** ⚠️

The documentation team is working to combine content pulled from the following pages:

* [/raw-migrated-files/cloud/cloud-enterprise/ece-stack-getting-started.md](/raw-migrated-files/cloud/cloud-enterprise/ece-stack-getting-started.md)
* [/raw-migrated-files/cloud/cloud-enterprise/ece-administering-deployments.md](/raw-migrated-files/cloud/cloud-enterprise/ece-administering-deployments.md)
* [/raw-migrated-files/cloud/cloud-enterprise/ece-change-deployment.md](/raw-migrated-files/cloud/cloud-enterprise/ece-change-deployment.md)
* [/raw-migrated-files/cloud/cloud-enterprise/ece-monitoring-deployments.md](/raw-migrated-files/cloud/cloud-enterprise/ece-monitoring-deployments.md)

% from the post-install instructions
% * [Set up traffic filters](../../security/traffic-filtering.md) to restrict traffic to your deployment to only trusted IP addresses or VPCs.


## Introducing deployments [ece_introducing_deployments]

**The Elastic Stack, managed through {{ecloud}} deployments.**

Elastic Cloud Enterprise allows you to manage one or more instances of the Elastic Stack through **deployments**.

A *deployment* helps you manage an Elasticsearch cluster and instances of other Elastic products, like Kibana or APM instances, in one place. Spin up, scale, upgrade, and delete your Elastic Stack products without having to manage each one separately. In a deployment, everything works together.

**Hardware profiles to optimize deployments for your usage.**

You can optimize the configuration and performance of a deployment by selecting a **hardware profile** that matches your usage.

*Hardware profiles* are presets that provide a unique blend of storage, memory and vCPU for each component of a deployment. They support a specific purpose, such as a hot-warm architecture that helps you manage your data storage retention.

You can use these presets, or start from them to get the unique configuration you need. They can vary slightly from one cloud provider or region to another to align with the available virtual hardware.

All of these profiles are based on *deployment templates*, which are a reusable configuration of Elastic products that you can deploy. With the flexibility of Elastic Cloud Enterprise, you can take it a step further by customizing a deployment template to your own needs.

## How to operate Elastic Cloud Enterprise? [ece_how_to_operate_elastic_cloud_enterprise]

**Where to start?**

* Try one of our solutions by following our [getting started guides](https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/getting-started-guides.html).
* [Create a deployment](../../../deploy-manage/deploy/cloud-enterprise/create-deployment.md) - Get up and running very quickly. Select your desired configuration and let Elastic deploy Elasticsearch, Kibana, and the Elastic products that you need for you. In a deployment, everything works together, everything runs on hardware that is optimized for your use case.
* [Connect your data to your deployment](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-cloud-ingest-data.html) - Ingest and index the data you want, from a variety of sources, and take action on it.


## Administering deployments [ece-administering-deployments]

Care and feeding of your deployments is important. Take a look at the things you can do to keep your deployments and the Elastic Stack running smoothly:

* [Change your deployment configuration](../../../deploy-manage/deploy/cloud-enterprise/working-with-deployments.md) to provide additional resources, for example. For many changes, your deployment can continue to handle search and indexing workloads without interruption.
* [Stop routing requests or pause nodes](../../../deploy-manage/maintenance/ece/deployments-maintenance.md) to perform corrective actions that might otherwise be difficult to complete.
* [Terminate a deployment](../../../deploy-manage/uninstall/delete-a-cloud-deployment.md) to stop all running instances and delete all data in the deployment.
* [Restart a deployment](../../../deploy-manage/maintenance/start-stop-services/restart-an-ece-deployment.md) that has become unresponsive, for example.
* [Restore a deployment](../../../deploy-manage/uninstall/delete-a-cloud-deployment.md) a deployment that had been terminated.
* [Delete a deployment](../../../deploy-manage/uninstall/delete-a-cloud-deployment.md) if you no longer need it.
* [Perform maintenance on the Kibana instance](../../../deploy-manage/maintenance.md) associated with the deployment.
* [Work with snapshots](../../../deploy-manage/tools/snapshot-and-restore.md) to recover from a failure or to recover from accidental deletion.
* [Keep your deployments healthy](../../../deploy-manage/deploy/cloud-enterprise/working-with-deployments.md) by monitoring key performance metrics.
* [Secure your clusters](../../../deploy-manage/users-roles/cluster-or-deployment-auth.md) to prevent unauthorized access from unwanted traffic or users and to preserve the integrity of your data with message authentication and SSL/TLS encryption.
* [Access the Elasticsearch API console](../../../explore-analyze/query-filter/tools/console.md) - Work with the Elasticsearch RESTful API directly from the Cloud UI.

TBD: EDU  where to put this:
### Other actions

From the deployment page you can also:

* Access to different feature sections like 
* 

**Kibana** page you can also:

* Terminate your Kibana instance, which stops it. The information is stored in your Elasticsearch cluster, so stopping and restarting should not risk your Kibana information.
* Restart it after stopping.
* Upgrade your Kibana instance version if it is out of sync with your Elasticsearch cluster.
* Delete to fully remove the instance, wipe it from the disk, and stop charges.


TBD - Link to monitoring and troubleshooting perhaps

## Keep your clusters healthy [ece-monitoring-deployments]

Elastic Cloud Enterprise monitors many aspects of your installation, but some issues require a human to resolve them. Use this section to learn how you can:

* [Find clusters](/troubleshoot/deployments/elastic-cloud.md) that have issues.
* [Move affected nodes off an allocator](../../../deploy-manage/maintenance/ece/move-nodes-instances-from-allocators.md), if the allocator fails.
* [Enable deployment logging and monitoring](../../../deploy-manage/monitor/stack-monitoring/ece-stack-monitoring.md) to keep an eye on the performance of deployments and debug stack and solution issues.

In addition to the monitoring of clusters that is described here, don’t forget that Elastic Cloud Enterprise also provides [monitoring information for your entire installation](../../../deploy-manage/monitor/orchestrators/ece-platform-monitoring.md). You can you also monitor the physical hosts machines on which Elastic Cloud Enterprise is installed.




