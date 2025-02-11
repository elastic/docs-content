---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-create-deployment.html
---

# Create an Elastic Cloud Hosted deployment [ec-create-deployment]

An Elastic Cloud deployment includes Elastic Stack components such as Elasticsearch, Kibana, and other features, allowing you to store, search, and analyze your data. You can spin up a proof-of-concept deployment to learn more about what Elastic can do for you.

::::{note}
To explore Elasticsearch Service and its solutions, create your first deployment by following one of these [getting started guides](https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/getting-started-guides.html). If you are instead interested in serverless Elastic Cloud, check the [serverless documentation](https://docs.elastic.co/serverless).
::::


You can also create a deployment using the [Elastic Cloud API](https://www.elastic.co/docs/api/doc/cloud/group/endpoint-deployments). This can be an interesting alternative for more advanced needs, such as for [creating a deployment encrypted with your own key](../../security/encrypt-deployment-with-customer-managed-encryption-key.md).

1. Log in to your [cloud.elastic.co](https://cloud.elastic.co/login) account and select **Create deployment** from the Elasticsearch Service main page:

    :::{image} ../../../images/cloud-ec-login-first-deployment.png
    :alt: Log in to create a deployment
    :::


Once you are on the **Create deployment** page, you can create the deployment with the defaults assigned, where you can edit the basic settings, or configure more advanced settings.

1. From the main **Settings**, you can change the cloud provider and region that host your deployment, the stack version, and the hardware profile, or restore data from another deployment (**Restore snapshot data**):

    :::{image} ../../../images/cloud-ec-create-deployment.png
    :alt: Create deployment
    :::

    Cloud provider
    :   The cloud platform where you’ll deploy your deployment. We support: Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure. You do not need to provide your own keys.

    Region
    :   The cloud platform’s region your deployment will live. If you have compliance or latency requirements, you can create your deployment in any of our [supported regions](https://www.elastic.co/guide/en/cloud/current/ec-reference-regions.html). The region should be as close as possible to the location of your data.

    Hardware profile
    :   This allows you to configure the underlying virtual hardware that you’ll deploy your Elastic Stack on. Each hardware profile provides a unique blend of storage, RAM and vCPU sizes. You can select a hardware profile that’s best suited for your use case. For example CPU Optimized if you have a search-heavy use case that’s bound by compute resources. For more details, check the [hardware profiles](ec-configure-deployment-settings.md#ec-hardware-profiles) section. You can also view the [virtual hardware details](https://www.elastic.co/guide/en/cloud/current/ec-reference-hardware.html) which powers hardware profiles. With the **Advanced settings** option, you can configure the underlying virtual hardware associated with each profile.

    Version
    :   The Elastic Stack version that will get deployed. Defaults to the latest version. Our [version policy](available-stack-versions.md) describes which versions are available to deploy.

2. Expand **Advanced settings** to configure your deployment for encryption using a customer-managed key, autoscaling, storage, memory, and vCPU. Check [Customize your deployment](configure.md) for more details.

    ::::{tip}
    Trial users won’t find the Advanced settings when they create their first deployment. This option is available on the deployment’s edit page once the deployment is created.
    ::::

3. Select **Create deployment**. It takes a few minutes before your deployment gets created. While waiting, you are prompted to save the admin credentials for your deployment which provides you with superuser access to Elasticsearch. Keep these credentials safe as they are shown only once. These credentials also help you [add data using Kibana](../../../manage-data/ingest.md). If you need to refresh these credentials, you can [reset the password](../../users-roles/cluster-or-deployment-auth/built-in-users.md).
4. Once the deployment is ready, select **Continue** to open the deployment’s main page. From here, you can start [ingesting data](../../../manage-data/ingest.md) or simply [try a sample data](../../../explore-analyze/overview/kibana-quickstart.md#gs-get-data-into-kibana) set to get started.

    At any time, you can manage and [adjust the configuration](configure.md) of your deployment to your needs, add extra layers of [security](../../users-roles/cluster-or-deployment-auth.md), or (highly recommended) set up [health monitoring](../../monitor/stack-monitoring.md).

    :::{image} ../../../images/cloud-ec-deployment-mainpage.png
    :alt: ESS Deployment main page
    :::


