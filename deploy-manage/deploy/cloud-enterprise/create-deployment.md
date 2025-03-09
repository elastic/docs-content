---
applies_to:
  deployment:
    ece: all
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-create-deployment.html
---

# Create a deployment

An ECE deployment is a fully managed Elastic Stack environment running on {{ece}}. It includes {{es}}, {{kib}}, and optional features like Machine Learning or an Integrations (Fleet & APM) Server.

Each deployment is based on a [deployment template](./deployment-templates.md), which defines its resources, default topology, scaling policies, and available features. Deployments can be customized based on workload requirements, including autoscaling, snapshot settings, and security configurations.

To create a deployment in ECE:

1. From the Cloud UI, select **Create deployment**.

    You can quickly create a deployment by setting the basic parameters shown in the UI. If you need more control, select **Advanced settings** to customize the deployment parameters, including autoscaling, storage, memory, data tiers, and additional Elastic Stack components. Refer to [](./customize-deployment.md) for more information.

    :::{image} ../../../images/cloud-enterprise-ece-create-deployment.png
    :alt: Create a deployment
    :::

2. Set a name for your deployment.

3. Select a deployment template.

    ::::{tip}
    * For a description of the available system templates, refer to [](./deployment-templates.md).
    * If the system templates do not meet your requirements, you can [modify them](./ece-configuring-ece-configure-system-templates.md) or [create your own custom templates](../../../deploy-manage/deploy/cloud-enterprise/ece-configuring-ece-create-templates.md).
    ::::

4. Choose your {{stack}} version. To manage available versions, refer to [](./manage-elastic-stack-versions.md).

5. Optionally, [use snapshots](../../tools/snapshot-and-restore/cloud-enterprise.md) to back up your data, or [restore data from another deployment](../../tools/snapshot-and-restore/ece-restore-across-clusters.md).

    ::::{tip}
        Restoring a snapshot can help with major version upgrades by creating a separate, non-production deployment where you can test, for example. Or, make life easier for your developers by providing them with a development environment that is populated with real data.
    ::::

6. Select **Advanced settings** if you want to configure [autoscaling](../../autoscaling/ece-autoscaling.md), adjust storage, memory, or customize data tiers. Refer to [Customize your deployment](../../../deploy-manage/deploy/cloud-enterprise/customize-deployment.md) for more details on the available options.

7. Select **Create deployment**. It takes a few minutes before your deployment gets created.

    ::::{tip}
    While waiting, you will be prompted to save the admin credentials for your deployment, which grant superuser access to Elasticsearch. Write down the password for the `elastic` user and keep it somewhere safe. These credentials also help you [add data using Kibana](../../../manage-data/ingest.md). If you need to refresh these credentials, you can [reset the password](../../../deploy-manage/users-roles/cluster-or-deployment-auth/manage-elastic-user-cloud.md) at any time.
    ::::

8. Once the deployment is ready, select **Continue** to open the deployment’s main page.

After a deployment is spun up, you can scale the size and add other features; however, the instance configuration and computing ratios cannot be changed. If you need to change an existing deployment to another template, we recommend [migrating your data](../../../manage-data/migrate.md).

## Next steps

% TBD, we have to refine a bit this section

That’s it! Now that you are up and running, you may want to:

* [Start exploring with {{kib}}](./access-kibana.md), our open-source visualization tool. If you’re not familiar with adding data, yet, {{kib}} can show you how to index your data into {{es}}.
* [Connect your applications to {{es}}](./connect-elasticsearch.md) to start [ingesting data](../../../manage-data/ingest.md)
* Learn how to configure and [manage your deployment](./working-with-deployments.md)

% From Shaina in Cloud, TBD.

## Preparing a deployment for production [ec-prepare-production]

To make sure you’re all set for production, consider the following actions:

* [Plan for your expected workloads](/deploy-manage/production-guidance/pl) and consider how many availability zones you’ll need.
* [Create a deployment](/deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md) on the region you need and with a hardware profile that matches your use case.
* [Change your configuration](/deploy-manage/deploy/elastic-cloud/ec-customize-deployment-components.md) by turning on autoscaling, adding high availability, or adjusting components of the Elastic Stack.
* [Add extensions and plugins](/deploy-manage/deploy/elastic-cloud/add-plugins-extensions.md) to use Elastic supported extensions or add your own custom dictionaries and scripts.
* [Edit settings and defaults](/deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) to fine tune the performance of specific features.
* [Manage your deployment](/deploy-manage/deploy/elastic-cloud/manage-deployments.md) as a whole to restart, upgrade, stop routing, or delete.
* [Set up monitoring](/deploy-manage/monitor/stack-monitoring/elastic-cloud-stack-monitoring.md) to learn how to configure your deployments for observability, which includes metric and log collection, troubleshooting views, and cluster alerts to automate performance monitoring.


