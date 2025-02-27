# Upgrade versions [ec-upgrade-deployment]

::::{important} 
Beginning with Elastic Stack version 8.0, instructions for upgrading {{ech}} deployments can be found in [Upgrading on Elastic Cloud](../../../deploy-manage/upgrade/deployment-or-cluster.md). The following instructions apply for upgrading to Elastic Stack versions 7.x and previous.
::::


::::{note} 
You should upgrade the monitoring cluster before the production cluster. In general, the monitoring cluster and the clusters being monitored should run the same version of the stack. A monitoring cluster cannot monitor production clusters that run newer versions of the stack. If necessary, the monitoring cluster can monitor production clusters running the latest release of the previous major version.
::::


When upgrading the version of an existing cluster, either a minor or major upgrade is performed. The difference is that a minor upgrade takes you from 6.8.2 to 6.8.3, while a major upgrade takes you from 6.8 to 7.17.

If you are upgrading to version 6.7 and later, minor or major upgrades to highly available deployments require little to no downtime as a rolling upgrade is performed.

Major version upgrades sometimes require other changes due to breaking changes or discontinued features. For example, some special considerations apply when [upgrading to Elasticsearch 5.0](https://www.elastic.co/guide/en/cloud/current/ec-upgrading-v5.html). Our recommended approach for major version upgrades is to create a new deployment with the latest major version you want to upgrade to, reindex everything and make sure index requests are temporarily sent to both clusters. With the new cluster ready, tested, and working, you can then remove the old deployment.

If you are upgrading to version 6.6 and earlier, major upgrades require a full cluster restart to complete the upgrade process.

Patch releases also require no downtime when upgrading highly available deployments. A patch fix release takes you from 5.5.1 to 5.5.3, for example.


## Before you begin [ec_before_you_begin_9] 

When upgrading from one recent major Elasticsearch version to the next, we recommend that you prepare ahead of time to make the process go smoothly. To learn more, see:

* [Upgrade to Elasticsearch 7.x](https://www.elastic.co/guide/en/cloud/current/ec-upgrading-v7.html)
* [Upgrade to Elasticsearch 6.x](https://www.elastic.co/guide/en/cloud/current/ec-upgrading-v6.html)
* [Upgrade to Elasticsearch 5.x](https://www.elastic.co/guide/en/cloud/current/ec-upgrading-v5.html)

::::{warning} 
If you have a custom plugin installed, you must [update the plugin](../../../deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md#ec-update-bundles-and-plugins) so that it matches the Elasticsearch version that you are upgrading to. When the custom plugin does not match the Elasticsearch version, the upgrade fails.
::::


To successfully replace and override a plugin which is being upgraded, the `name` attribute contained in the `plugin-descriptor.properties` file must be the exact same as the currently installed plugin’s `name` attribute. If the attributes do not match, the new plugin bundle will be added to the cluster as a completely new and separate plugin.


## Perform the upgrade [ec_perform_the_upgrade] 

To upgrade a cluster in {{ech}}:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. In the **Deployment version** section, select **Upgrade**.
4. Select a new version.

    If you perform a major version upgrade, the UI provides a link to our migration helper tool that helps you to determine if a direct upgrade is feasible. You can also check our [Elastic Stack upgrade guide](https://www.elastic.co/products/upgrade_guide).

5. Optional: Make any other changes that are needed, such as increasing the capacity or adding plugins.
6. Select **Upgrade** and then **Confirm upgrade**. The new configuration takes a few minutes to create.
7. If you are upgrading to version 6.6 and earlier, major upgrades require a full cluster restart to complete the upgrade process.
8. If you had Kibana enabled, the UI will prompt you to also upgrade Kibana. The Kibana upgrade takes place separately from the Elasticsearch version upgrade and needs to be triggered manually:

    1. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.
    2. From your deployment menu, select **Kibana**.
    3. If the button is available, select **Upgrade Kibana**. If the button is not available, Kibana does not need to be upgraded further.
    4. Confirm the upgrade.





