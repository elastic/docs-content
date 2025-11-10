---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-create-deployment.html
  - https://www.elastic.co/guide/en/cloud/current/ec-prepare-production.html
  - https://www.elastic.co/guide/en/cloud/current/ec-configure-deployment-settings.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-configure-deployment-settings.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Create an {{ech}} deployment [ec-create-deployment]

An {{ecloud}} deployment includes {{stack}} components such as {{es}}, {{kib}}, and other features, allowing you to store, search, and analyze your data. You can spin up a proof-of-concept deployment to learn more about what Elastic can do for you.

:::{note}
You can also create a deployment using the [{{ecloud}} API](https://www.elastic.co/docs/api/doc/cloud/group/endpoint-deployments). This can be an interesting alternative for more advanced needs, such as for [creating a deployment encrypted with your own key](../../security/encrypt-deployment-with-customer-managed-encryption-key.md).
:::

1. Log in to your [cloud.elastic.co](https://cloud.elastic.co/login) account and select **Create deployment** from the {{ecloud}} main page:

    :::{image} /deploy-manage/images/cloud-ec-login-first-deployment.png
    :alt: Log in to create a deployment
    :::

1. Select a solution view for your deployment. Solution views define the navigation and set of features that will be first available in your deployment. You can change it later, or [create different spaces](/deploy-manage/manage-spaces.md) with different solution views within your deployment.

    To learn more about what each solution offers, check [Elasticsearch](/solutions/search/get-started.md), [Observability](/solutions/observability/get-started.md), and [Security](/solutions/security/get-started.md).

1. From the main **Settings**, you can change the cloud provider and region that host your deployment, the stack version, and the hardware profile, or restore data from another deployment (**Restore snapshot data**):

    :::{image} /deploy-manage/images/cloud-ec-create-deployment.png
    :alt: Create deployment
    :width: 50%
    :::

    **Cloud provider**: The cloud platform where you’ll deploy your deployment. We support: Amazon Web Services (AWS), Google Cloud Platform (GCP), and Microsoft Azure. You do not need to provide your own keys.

    **Region**: The cloud platform’s region your deployment will live. If you have compliance or latency requirements, you can create your deployment in any of our [supported regions](cloud://reference/cloud-hosted/regions.md). The region should be as close as possible to the location of your data.

    **Hardware profile**: This allows you to configure the underlying virtual hardware that you’ll deploy your {{stack}} on. Each hardware profile provides a unique blend of storage, RAM and vCPU sizes. You can select a hardware profile that’s best suited for your use case. For example CPU Optimized if you have a search-heavy use case that’s bound by compute resources. For more details, check the [hardware profiles](ec-change-hardware-profile.md) section. You can also view the [virtual hardware details](cloud://reference/cloud-hosted/hardware.md) which powers hardware profiles. With the **Advanced settings** option, you can configure the underlying virtual hardware associated with each profile.

    **Version**: The {{stack}} version that will get deployed. Defaults to the latest version. Our [version policy](available-stack-versions.md) describes which versions are available to deploy.

    **Snapshot source**: To create a deployment from a snapshot, select a snapshot source. You need to [configure snapshots](../../tools/snapshot-and-restore.md) and establish a snapshot lifecycle management policy and repository before you can restore from a snapshot. The snapshot options depend on the stack version the deployment is running.

    **Name**: This setting allows you to assign a more human-friendly name to your cluster which will be used for future reference in the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body). Common choices are dev, prod, test, or something more domain specific.

2. Expand **Advanced settings** to configure your deployment for encryption using a customer-managed key, autoscaling, storage, memory, and vCPU. Check [Customize your deployment](configure.md) for more details.

    ::::{tip}
    Trial users won’t find the Advanced settings when they create their first deployment. This option is available on the deployment’s edit page once the deployment is created.
    ::::

3. Select **Create deployment**. It takes a few minutes before your deployment gets created. While waiting, you are prompted to save the admin credentials for your deployment which provides you with superuser access to {{es}}. Keep these credentials safe as they are shown only once. These credentials also help you [add data using Kibana](../../../manage-data/ingest.md). If you need to refresh these credentials, you can [reset the password](../../users-roles/cluster-or-deployment-auth/built-in-users.md).
4. Once the deployment is ready, select **Continue** to open the deployment’s main page. From here, you can start [ingesting data](../../../manage-data/ingest.md) or simply [try a sample data](../../../explore-analyze/index.md#gs-get-data-into-kibana) set to get started.

    At any time, you can manage and [adjust the configuration](configure.md) of your deployment to your needs, add extra layers of [security](../../users-roles/cluster-or-deployment-auth.md), or (highly recommended) set up [health monitoring](../../monitor/stack-monitoring.md).

    :::{image} /deploy-manage/images/cloud-ec-deployment-mainpage.png
    :alt: ESS Deployment main page
    :::

## Preparing a deployment for production [ec-prepare-production]

To make sure you’re all set for production, consider the following actions:

* [Plan for your expected workloads](/deploy-manage/production-guidance.md) and consider how many availability zones you’ll need.
* [Create a deployment](/deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md) on the region you need and with a hardware profile that matches your use case.
* [Change your configuration](/deploy-manage/deploy/elastic-cloud/ec-customize-deployment-components.md) by turning on autoscaling, adding high availability, or adjusting components of the {{stack}}.
* [Add plugins and extensions](/deploy-manage/deploy/elastic-cloud/add-plugins-extensions.md) to use Elastic supported extensions or add your own custom dictionaries and scripts.
* [Edit settings and defaults](/deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) to fine tune the performance of specific features.
* [Manage your deployment](/deploy-manage/deploy/elastic-cloud/manage-deployments.md) as a whole to restart, upgrade, stop routing, or delete.
* [Set up monitoring](/deploy-manage/monitor/stack-monitoring/ece-ech-stack-monitoring.md) to learn how to configure your deployments for observability, which includes metric and log collection, troubleshooting views, and cluster alerts to automate performance monitoring.

