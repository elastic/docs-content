# Create a hosted deployment [ece-create-deployment]

An Elastic Cloud deployment includes Elastic Stack components such as Elasticsearch, Kibana, and other features, allowing you to store, search, and analyze your data. You can spin up a proof-of-concept deployment to learn more about what Elastic can do for you.

::::{note}
To explore Elastic Cloud Enterprise and its solutions, create your first deployment by following one of these [getting started guides](https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/getting-started-guides.html). If you are instead interested in serverless Elastic Cloud, check the [serverless documentation](https://docs.elastic.co/serverless).
::::


To get up and running with your deployment quickly:

1. From the Cloud UI, select **Create deployment**.

    :::{image} ../../../images/cloud-enterprise-ece-create-deployment.png
    :alt: Create a deployment
    :::

    Once you are on the **Create deployment** page, you can edit the basic settings, or configure more advanced settings.

2. Select **Create deployment**. It takes a few minutes for your deployment to be created. While waiting, you are prompted to save the `admin` credentials for your deployment which provides you with superuser access to Elasticsearch. Keep these credentials safe as they are shown only once.

    * **Default**. A template to get you started and for backwards compatibility with existing deployments. The default template is suitable for search and general all-purpose workloads that don’t require more specialized resources.
    * **Cross-cluster Search**. A lightweight hub to manage remote connections for running Elasticsearch queries across multiple deployments and indices.
    * [**Elastic Security**](../../../solutions/security.md). Provides an overview of the events and alerts from your environment. Elastic Security helps you defend your organization from threats before damage and loss occur.
    * [**Elastic Observability**](../../../solutions/observability/get-started/what-is-elastic-observability.md). Enables you to monitor and apply analytics in real time to events happening across all your environments. You can analyze log events, monitor the performance metrics for the host or container that it ran in, trace the transaction, and check the overall service availability.


If these system templates are not suitable for your use case, you can [create your own deployment templates](../../../deploy-manage/deploy/cloud-enterprise/ece-configuring-ece-create-templates.md).

1. Choose your Elastic Stack version.
2. Optionally, use snapshots to back up your data or restore data from another deployment.

    Restoring a snapshot can help with major version upgrades by creating a separate, non-production deployment where you can test, for example. Or, make life easier for your developers by providing them with a development environment that is populated with real data.

3. Select **Advanced settings**, to configure your deployment for autoscaling, storage, memory, and vCPU. Check [Customize your deployment](../../../deploy-manage/deploy/cloud-enterprise/customize-deployment.md) for more details.
4. Select **Create deployment**. It takes a few minutes before your deployment gets created.

    While waiting, you are prompted to save the admin credentials for your deployment which provides you with superuser access to Elasticsearch. Write down the password for the `elastic` user (or the `admin` user for version 2.x) and keep it somewhere safe. These credentials also help you [add data using Kibana](../../../manage-data/ingest.md). If you need to refresh these credentials, you can [reset the password](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).

5. Once the deployment is ready, select **Continue** to open the deployment’s main page. From here, you can start ingesting data or simply [try a sample data](../../../explore-analyze/index.md#gs-get-data-into-kibana) set to get started.

    :::{image} ../../../images/cloud-enterprise-ece-deployment-mainpage.png
    :alt: ECE Deployment main page
    :::


After a deployment is spun up, you can scale the size and add other features; however, the instance configuration and computing ratios cannot be changed. If you need to change an existing deployment to another template, we recommend [migrating your data](../../../manage-data/migrate.md).




