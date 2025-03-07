---
applies_to:
  deployment:
    ece: all
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-create-deployment.html
---

# Create a deployment

An ECE deployment is a fully managed Elastic Stack environment running on {{ece}}. It includes {{es}}, {{kib}}, and optional features like Machine Learning, or an Integrations (Fleet & APM) Server.

Each deployment is based on a [deployment template](./deployment-templates.md), which defines its resources, default topology, scaling policies, and available features. Deployments can be customized based on workload requirements, including autoscaling, snapshot settings, and security configurations.

To create a deployment in ECE:

1. From the Cloud UI, select **Create deployment**.

    :::{image} ../../../images/cloud-enterprise-ece-create-deployment.png
    :alt: Create a deployment
    :::

    On the **Create deployment** page, you can edit the basic settings or adjust advanced configurations. **Advanced settings** allow you to modify deployment parameters defined by the selected template, such as autoscaling, storage, memory, data tiers, and additional {{stack}} components.

2. Set a name for your deployment.

3. Select a deployment template.

::::{tip}
* Refer to [](./deployment-templates.md) for more information about deployment templates, including descriptions of the default system templates.
* If the system templates do not meet your requirements, you can [modify them](./ece-configuring-ece-configure-system-templates.md) or [create your own custom templates](../../../deploy-manage/deploy/cloud-enterprise/ece-configuring-ece-create-templates.md).
::::

4. Choose your {{stack}} version. To manage available versions, refer to [](./manage-elastic-stack-versions.md).

5. Optionally, [use snapshots](../../tools/snapshot-and-restore/cloud-enterprise.md) to back up your data or [restore data from another deployment](../../tools/snapshot-and-restore/ece-restore-across-clusters.md).

::::{tip}
    Restoring a snapshot can help with major version upgrades by creating a separate, non-production deployment where you can test, for example. Or, make life easier for your developers by providing them with a development environment that is populated with real data.
::::

6. Select **Advanced settings**, to configure your deployment for [autoscaling](../../autoscaling/ece-autoscaling.md), storage, memory, and data tiers. Check [Customize your deployment](../../../deploy-manage/deploy/cloud-enterprise/customize-deployment.md) for more details.

7. Select **Create deployment**. It takes a few minutes before your deployment gets created.

   While waiting, you are prompted to save the admin credentials for your deployment which provides you with superuser access to Elasticsearch. Write down the password for the `elastic` user and keep it somewhere safe. These credentials also help you [add data using Kibana](../../../manage-data/ingest.md). If you need to refresh these credentials, you can [reset the password](../../../deploy-manage/users-roles/cluster-or-deployment-auth/manage-elastic-user-cloud.md).

8. Once the deployment is ready, select **Continue** to open the deployment’s main page.

After a deployment is spun up, you can scale the size and add other features; however, the instance configuration and computing ratios cannot be changed. If you need to change an existing deployment to another template, we recommend [migrating your data](../../../manage-data/migrate.md).

## Next steps

After creating your deployment, you may want to:

* [Access {{kib}}](./access-kibana.md)
* [Connect your applications to {{es}}](./connect-elasticsearch.md) to start [ingesting data](../../../manage-data/ingest.md)
* Learn how to configure and [manage your deployment](./working-with-deployments.md)