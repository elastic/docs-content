# Upgrade versions [ece-upgrade-deployment]

::::{important}
Beginning with Elastic Stack version 8.0, instructions for upgrading your Elastic Cloud Enterprise stack version can be found in [Upgrading on Elastic Cloud](../../../deploy-manage/upgrade/deployment-or-cluster.md). The following instructions apply for upgrading to Elastic Stack versions 7.x and previous.
::::


::::{note}
You should upgrade the monitoring cluster before the production cluster. In general, the monitoring cluster and the clusters being monitored should run the same version of the stack. A monitoring cluster cannot monitor production clusters that run newer versions of the stack. If necessary, the monitoring cluster can monitor production clusters running the latest release of the previous major version.
::::


When upgrading the version of an existing cluster, either a minor or major upgrade is performed. The difference is that a minor upgrade takes you from 6.2 to 6.3, while a major upgrade takes you from 6 to 7.

If you are upgrading to version 6.7 and later, minor or major upgrades to highly available deployments require little to no downtime as a rolling upgrade is performed.

Major version upgrades sometimes require other changes due to breaking changes or discontinued features. For example, some special considerations apply when [upgrading to Elasticsearch 5.0](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-upgrading-v5.html). Our recommended approach for major version upgrades is to create a new deployment with the latest major version you want to upgrade to, reindex everything and make sure index requests are temporarily sent to both clusters. With the new cluster ready, tested, and working, you can then remove the old deployment.

If you are upgrading to version 6.6 and earlier, major upgrades require a full cluster restart to complete the upgrade process.

Patch releases also require no downtime when upgrading highly available deployments. A patch fix release takes you from 5.5.1 to 5.5.3, for example.


## Before you begin [ece_before_you_begin_13]

When upgrading from one recent major Elasticsearch version to the next, we recommend that you prepare ahead of time to make the process go smoothly. To learn more, see:

* [Upgrade to Elasticsearch 7.x](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-upgrading-v7.html)
* [Upgrade to Elasticsearch 6.x](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-upgrading-v6.html)
* [Upgrade to Elasticsearch 5.x](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-upgrading-v5.html)


## Perform the upgrade [ece_perform_the_upgrade]

To upgrade a cluster in Elastic Cloud Enterprise:

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. Select **Upgrade**.
4. Select one of the available software versions. Let the user interface guide you through the steps for upgrading a deployment. When you save your changes, your deployment configuration is updated to the new version.

    ::::{tip}
    You cannot downgrade after upgrading, so plan ahead to make sure that your applications still work after upgrading. For more information on changes that might affect your applications, check [Breaking changes](asciidocalypse://docs/elasticsearch/docs/release-notes/breaking-changes.md).
    ::::

5. If you are upgrading to version 6.6 and earlier, major upgrades require a full cluster restart to complete the upgrade process.
