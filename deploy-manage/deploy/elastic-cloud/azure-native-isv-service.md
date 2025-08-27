---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-azure-marketplace-native.html
applies_to:
  deployment:
    ess: ga
  serverless: preview
products:
  - id: cloud-hosted
---

# Azure Native ISV Service [ec-azure-marketplace-native]

The {{ecloud}} Azure Native ISV Service allows you to deploy managed instances of the {{stack}} directly in Azure, through the Azure integrated marketplace. The service brings the following benefits:

* **Easy deployment for managed {{stack}} instances**

    {{stack}} instances managed by Elastic are deployed directly from the Azure console. This provides the complete {{stack}} experience with all commercial features.

* **Integrated billing**

    You are billed directly to your Azure account; no need to configure billing details in Elastic. See [Integrated billing](#ec-azure-integration-billing-summary) for details, as well as the [Billing FAQ](#ec-azure-integration-billing-faq).

* **Easy consolidation of your Azure logs in Elastic**

    Use a single-step setup to ingest logs from your Azure services into the {{stack}}.


::::{tip}
The full product name in the Azure integrated marketplace is _{{ecloud}} (Elasticsearch) - An Azure Native ISV Service_.
::::



## Integrated billing [ec-azure-integration-billing-summary]

Azure Native ISV Service includes integrated billing: Elastic resource costs are posted to your Azure subscription through the Microsoft Commercial Marketplace. You can create various {{ecloud}} resources (deployments) across different Azure subscriptions, with all of the costs associated with an {{ecloud}} organization posted to a single Azure subscription.

Note the following terms:

* **Azure Marketplace SaaS ID**: This is a unique identifier that’s generated one time by Microsoft Commercial Marketplace when a user creates their first Elastic resource (deployment) using the Microsoft Azure (Portal, API, SDK, or Terraform). This is mapped to a User ID and Azure Subscription ID
* **{{ecloud}} organization**: An [organization](../../users-roles/cloud-organization.md) is the foundational construct under which everything in {{ecloud}} is grouped and managed. An organization is created as a step during the creation of your first Elastic resource (deployment), whether that’s done through Microsoft Azure (Portal, API, SDK, or Terraform). The initial member of the {{ecloud}} organization can then invite other users.
* **Elastic resource (deployment)**: An {{ecloud}} deployment helps you manage an {{es}} cluster and instances of other Elastic products in one place. You can work with Elastic deployments from within the Azure ecosystem. Multiple users in the {{ecloud}} organization can create different deployments from different Azure subscriptions. They can also create deployments from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).

The following diagram shows the mapping between Microsoft Azure IDs, {{ecloud}} organization IDs, and your Elastic resources (deployments).

:::{image} /deploy-manage/images/cloud-ec-azure-billing-mapping.png
:alt: Azure to {{ecloud}} mappings
:::

The following diagram shows how your {{ecloud}} organization costs are reported in Microsoft Azure. You can also refer to our [Billing FAQ](#ec-azure-integration-billing-faq) on this page.

:::{image} /deploy-manage/images/cloud-ec-azure-billing-reporting.png
:alt: Azure to {{ecloud}} mappings
:::


## Frequently asked questions [ec-azure-integration-faq]

Check the following sections to learn more about the Azure Native ISV Service:

* **Getting started**

    * [How do I get started?](#azure-integration-get-started)
    * [What is the pricing for this offer?](#azure-integration-pricing)
    * [Which Azure regions are supported?](#azure-integration-regions)
    * [Which {{ecloud}} subscription levels are available?](#azure-integration-subscription-levels)
    * [How can I change my {{ecloud}} subscription level?](#azure-integration-change-subscription)
    * [Can I subscribe using an email address from another Elastic account?](#azure-integration-existing-email)
    * [Is the {{ecloud}} Azure Native ISV Service connected with Azure user management?](#azure-integration-azure-user-management)
    * [Does {{ecloud}} Azure Native ISV Service support recently introduced {{ecloud}} RBAC capability?](#azure-integration-azure-rbac)
    * [I already have an {{ecloud}} account, can I use this service?](#azure-integration-prior-cloud-account)
    * [Can I sign up for an {{ecloud}} trial account and then convert to the {{ecloud}} Azure Native ISV Service?](#azure-integration-convert-trial)
    * [Does {{es}} get deployed into my tenant in Azure?](#azure-integration-azure-tenant)
    * [What Azure tenant information does Elastic have access to?](#azure-integration-azure-tenant-info)
    * [What other methods are available to deploy {{es}}?](#azure-integration-cli-api)
    * [How do I migrate my data from the classic Azure marketplace account to the {{ecloud}} Azure Native ISV Service?](#azure-integration-migrate)
    * [Can multiple Azure users deploy to the same {{ecloud}} organization?](#azure-integration-multiple-users)
    * [Can I invite users to my organization, even if they cannot receive emails?](#azure-integration-no-inbox)

* **Billing**

    * [Which Azure Subscription will be billed for my Elastic resources?](#azure-integration-billing-which-subscription)
    * [How do I get different Elastic resources (deployments) charges to different Azure Subscriptions?](#azure-integration-billing-different-deployments)
    * [Why can’t I see Elastic resources costs in Azure Cost Explorer?](#azure-integration-billing-elastic-costs)
    * [Why don’t I see my individual Elastic resources (deployments) in the Azure Marketplace Invoice?](#azure-integration-billing-deployments)
    * [Why can’t I find Instance ID and Instance Name values from Azure Marketplace Invoice in the Azure Portal?](#azure-integration-billing-instance-values)

* **Managing your {{ecloud}} deployment**

    * [What is included in my {{ecloud}} deployment?](#azure-integration-whats-included)
    * [How can I access my {{ecloud}} deployment?](#azure-integration-how-to-access)
    * [How can I modify my {{ecloud}} deployment?](#azure-integration-modify-deployment)
    * [How can I delete my {{ecloud}} deployment?](#azure-integration-delete-deployment)
    * [Can I delete the Azure Resource Group containing my deployment?](#azure-integration-delete-resource-group)

* **Configuring logs and metrics**

    * [How do I monitor my existing Azure services?](#azure-integration-monitor)
    * [How do I ingest metrics from my Azure services?](#azure-integration-ingest-metrics)
    * [How can I monitor my Azure virtual machines in {{es}}?](#azure-integration-vm-extensions)

* **Troubleshooting**

    * [I receive an error message about not having required authorization.](#azure-integration-authorization-access)
    * [My {{ecloud}} deployment creation failed.](#azure-integration-deployment-failed-network-security)
    * [I can’t SSO into my {{ecloud}} deployment.](#azure-integration-failed-sso)
    * [I see some deployments in the {{ecloud}} console but not in the Azure Portal.](#azure-integration-cant-see-deployment)
    * [My {{ecloud}} Azure Native ISV Service logs are not being ingested.](#azure-integration-logs-not-ingested)

* **Support**

    * [How do I get support?](#azure-integration-support)
    * [How can I change my subscription level / support level?](#azure-integration-change-level)



## Getting started [ec-azure-integration-getting-started]

$$$azure-integration-get-started$$$How do I get started with {{ecloud}}?
:   {{ecloud}} is available as an offering through the Azure console.

    **Prerequisites**

    There are a few requirements to check before setting up an {{ecloud}} deployment:

    * In Azure your account role for the subscription is set as *Owner* or *Contributor*. For details and steps to assign roles, check [Permission to purchase](https://docs.microsoft.com/en-us/marketplace/azure-purchasing-invoicing#permission-to-purchase) in the Azure documentation.
    * You cannot use an email address that already has an {{ecloud}} account. Use a different Azure account to set up the {{es}} resource, or [contact the Elastic Support Team](#azure-integration-support) for assistance.
    * You must have a credit card registered on your Azure subscription. If you have a non-payment subscription, such as a [Virtual Studio Subscription](https://visualstudio.microsoft.com/subscriptions/), you can’t create an {{ecloud}} deployment. Refer to the Azure [Purchase errors](https://docs.microsoft.com/en-us/azure/partner-solutions/elastic/troubleshoot#purchase-errors) troubleshooting documentation for more information.
    * In order to single sign-on into your {{ecloud}} deployment from Azure you need to request approval from your Azure administrator.

    **Getting started**

    To create a deployment directly from the Azure portal, go to [the list of {{ecloud}} deployments in the Azure portal](https://portal.azure.com/#view/HubsExtension/BrowseResource/resourceType/Microsoft.Elastic%2Fmonitors) and select `Create`.

    When you create an {{ecloud}} deployment, an {{stack}} cluster is created for you. The size of this deployment is **16GB of RAM** and **560GB of storage**, across **two availability zones** for redundancy. The size of the deployment, both RAM and storage, is changed directly in the Elastic console. Usage charges are based on the deployment size, so size your instance efficiently. The deployment defaults to the latest available version of the {{stack}}. Check our [Version policy](available-stack-versions.md) to learn more about when new versions are made available and old versions are removed from service.


$$$azure-integration-pricing$$$What is the pricing for this offer?
:   Pricing is pay-as-you-go per hour for each {{ecloud}} deployment created. Note that there is no free trial period for the offering. Charges are applied to your Azure bill at the end of the month. Use the {{ecloud}} [Pricing Calculator](https://www.elastic.co/cloud/elasticsearch-service/pricing?page=docs&placement=docs-body) to size a deployment and view the corresponding hourly rate.

    Elastic charges include:

    * [Hourly consumption based on your active deployments](https://cloud.elastic.co/pricing)
    * [Data transfer and snapshot storage charges](https://cloud.elastic.co/deployment-pricing-table)


$$$azure-integration-regions$$$Which Azure regions are supported?
:   Here is the [list of available Azure regions](cloud://reference/cloud-hosted/ec-regions-templates-instances.md#ec-azure_regions) supported in {{ecloud}}.

$$$azure-integration-subscription-levels$$$Which {{ecloud}} subscription levels are available?
:   The subscription defaults to the Enterprise subscription, granting immediate access to advanced {{stack}} features like machine learning, and premium support response time SLAs. {{ecloud}} offers a number of different [subscription levels](https://elastic.co/pricing).

$$$azure-integration-change-subscription$$$How can I change my {{ecloud}} subscription level?
:   Modify your subscription level on the billing page in the Elastic console.

    1. Select a deployment to open the deployment overview page.
    2. Select the **Advanced Settings** link to access your deployment in the {{ecloud}} console.
    3. In the {{ecloud}} console, select your account avatar icon at the top of the page, and then choose **Account & Billing**.
    4. Select the **Billing** tab and choose **Change my subscription**.

        :::{image} /deploy-manage/images/cloud-ec-marketplace-azure009.png
        :alt: The Elastic Account Billing page with Advanced Settings highlighted
        :::

    5. Select the [subscription level](https://elastic.co/pricing) that you’d like.

        :::{image} /deploy-manage/images/cloud-ec-marketplace-azure006.png
        :alt: The Update Subscription page showing Standard
        :::


$$$azure-integration-existing-email$$$Can I subscribe using an email address from another Elastic account?
:   Your email address is associated with only one Elastic account. For a workaround, check [Sign up using an email address from another Cloud account](create-an-organization.md).

$$$azure-integration-azure-user-management$$$Is the {{ecloud}} Azure Native ISV Service connected with Azure user management?
:   No. Elastic is not currently integrated with Azure user management. Azure users who deploy {{es}} on Azure view and manage their own cluster through the Cloud console. Other Azure users in the same tenant cannot access clusters through the Cloud console other than those that they themselves created.

    When trying to access resources such as {{es}}, {{kib}}, or APM in a deployment that was created by another Azure user, the following error is shown:

    :::{image} /deploy-manage/images/cloud-ec-marketplace-azure026.png
    :alt: Error message displayed in the {{ecloud}} console: To access the resource {resource-name}
    :::

    Share deployment resources directly with other Azure users by [configuring Active Directory single sign-on with the {{es}} cluster](/deploy-manage/users-roles/cluster-or-deployment-auth/oidc-examples.md#ec-securing-oidc-azure).


$$$azure-integration-azure-rbac$$$Does {{ecloud}} Azure Native ISV Service support recently introduced {{ecloud}} RBAC capability?
:   Yes. Currently [{{ecloud}} RBAC capability](../../users-roles/cloud-organization/user-roles.md) is available only from the {{ecloud}} Console and is not integrated with Azure Portal. This means that the users who will interact with Elastic resources from Azure Portal will not be recognized by the {{ecloud}} RBAC policies.

$$$azure-integration-prior-cloud-account$$$I already have an {{ecloud}} account, can I use this service?
:   Yes. If you already have an {{ecloud}} account with the same email address as your Azure account you may need to contact `support@elastic.co`.

$$$azure-integration-convert-trial$$$Can I sign up for an {{ecloud}} trial account and then convert to the {{ecloud}} Azure Native ISV Service?
:   Yes. You can start a [free {{ecloud}} trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body) and then convert your account over to Azure. There are a few requirements:

    * Make sure when creating deployments in the trial account you specify Azure as the cloud provider.
    * To convert your trial to the Azure marketplace you need to create a deployment in the Azure console. Just delete the new deployment if you don’t need it. After you create the new deployment your marketplace subscription is ready.
    * Any deployments created during your trial won’t show up in the Azure console, since they weren’t created in Azure, but they are still accessible through the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) and you are billed for their usage.


$$$azure-integration-azure-tenant$$$Does {{es}} get deployed into my tenant in Azure?
:   No. {{es}} resources deployed in an Azure tenant are managed by Elastic. The management capabilities associated with this tenant are the same as used to run Elastic’s managed service, which also allows users to deploy on Azure.

$$$azure-integration-azure-tenant-info$$$What Azure tenant information does Elastic have access to?
:   After you subscribe to {{ecloud}} through the Azure Native ISV Service, Elastic has access to the following Azure tenant information:

    * Data defined in the marketplace [Saas fulfillment Subscription APIs](https://docs.microsoft.com/en-us/azure/marketplace/partner-center-portal/pc-saas-fulfillment-subscription-api).
    * The following additional data:
        * Marketplace subscription ID
        * Marketplace plan ID
        * Azure Account ID
        * Azure Tenant ID
        * Company
        * First name
        * Last name
        * Country


    Elastic can also access data from {{ecloud}} Azure Native ISV Service features, including [resource and activity log data](https://docs.microsoft.com/en-us/azure/azure-monitor/essentials/platform-logs-overview). This data is available to Elastic only if you enable it. By default, Elastic does not have access to this information.


$$$azure-integration-cli-api$$$What other methods are available to deploy {{es}}?
:   Use any of the following methods:

    * **Deploy using Azure tools**
        * The Azure console
        * [Azure Terraform](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/elastic_cloud_elasticsearch)
        * The [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/elastic?view=azure-cli-latest)
        * The Azure [REST API](https://docs.microsoft.com/en-us/rest/api/elastic)
        * [PowerShell](https://docs.microsoft.com/en-us/powershell/module/az.elastic/?view=azps-8.0.0#elastic)

    * **Deploy using official Azure SDKs**
        * [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/README.md)
        * [Java](https://github.com/Azure/azure-sdk-for-java/blob/azure-resourcemanager-elastic_1.0.0-beta.1/README.md)
        * [.NET](https://github.com/Azure/azure-sdk-for-net/blob/main/README.md)
        * [Rust](https://github.com/Azure/azure-sdk-for-rust/blob/main/services/README.md)

    * **Deploy using {{ecloud}}**
        * The {{ecloud}} [console](https://cloud.elastic.co?page=docs&placement=docs-body)
        * The {{ecloud}} [REST API](cloud://reference/cloud-hosted/ec-api-restful.md)
        * The {{ecloud}} [command line tool](ecctl://reference/index.md)
        * The {{ecloud}} [Terraform provider](https://registry.terraform.io/providers/elastic/ec/latest/docs)

            Note that when you use any of the {{ecloud}} methods, the {{es}} deployment will not be available in Azure.


$$$azure-integration-migrate$$$How do I migrate my data from the classic Azure marketplace account to the native integration?
:   First create a new account configured with {{ecloud}} Azure Native ISV Service, then perform the migration as follows:
    1. From your classic Azure marketplace account, navigate to the deployment and [configure a custom snapshot repository using Azure Blog Storage](../../tools/snapshot-and-restore/ec-azure-snapshotting.md).
    2. Using the newly configured snapshot repository, [create a snapshot](../../tools/snapshot-and-restore/create-snapshots.md) of the data to migrate.
    3. Navigate to Azure and log in as the user that manages the {{es}} resources.
    4. Before proceeding, ensure the new account is configured according to the [prerequisites](#azure-integration-get-started).
    5. Create a [new {{es}} resource](#azure-integration-get-started) for each existing deployment that needs migration from the classic Azure account.
    6. In the new {{es}} resource, follow the steps in [Restore from a snapshot](../../../manage-data/migrate.md#ec-restore-snapshots) to register the custom snapshot repository from Step 1.
    7. In the same set of steps, restore the snapshot data from the snapshot repository that you registered.
    8. Confirm the data has moved successfully into your new {{es}} resource on Azure.
    9. To remove the old Azure subscription and the old deployments, go to the [Azure SaaS page](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.SaaS%2Fresources) and unsubscribe from the {{ecloud}} ({{es}}) marketplace subscription. This action triggers the existing deployments termination.

$$$azure-integration-multiple-users$$$Can multiple Azure users deploy to the same {{ecloud}} organization?
:   Yes! Before another user creates a native resource from the Azure Portal, invite them to your {{ecloud}} organization at [https://cloud.elastic.co/account/members](https://cloud.elastic.co/account/members). When they create the resource, it will get added to the existing organization instead of creating a new one, and allow you to benefit from consolidated billing, RBAC, and other benefits of an {{ecloud}} organization.


$$$azure-integration-no-inbox$$$Can I invite users to my organization, even if they cannot receive emails?
:   You can add Azure users as members of your organization even if they don’t have an inbox. Reach out to Elastic support.


## Billing [ec-azure-integration-billing-faq]

$$$azure-integration-billing-which-subscription$$$Which Azure Subscription will be billed for my Elastic resources?
:   The Azure Marketplace integrated billing posts all of the Elastic deployment/resources costs related to an {{ecloud}} organization to the Azure subscription you used to create your first-ever Elastic deployment/resource. This is the case even if your individual Elastic resources (deployments) are spread across different Azure subscriptions. For more detail, refer to [Integrated billing](#ec-azure-integration-billing-summary).

$$$azure-integration-billing-different-deployments$$$How do I get different Elastic deployment/resources charges to different Azure Subscriptions?
:   See [Integrated billing](#ec-azure-integration-billing-summary). To have different Elastic deployment/resources costs reported to different Azure subscriptions, they need to be in separate {{ecloud}} organizations. To create a separate {{ecloud}} organization from an Azure subscription, you will need to subscribe as a user who is not already part of an existing {{ecloud}} organization.

$$$azure-integration-billing-elastic-costs$$$Why can’t I see Elastic resources costs in Azure Cost Explorer?
:   The costs associated with Elastic resources (deployments) are reported under unassigned in the Azure Portal. Refer to [Understand your Azure external services charges](https://learn.microsoft.com/en-us/azure/cost-management-billing/understand/understand-azure-marketplace-charges) in the Microsoft Documentation to understand Elastic resources/deployments costs. For granular Elastic resources costs, refer to [Monitor and analyze your acccount usage](../../cloud-organization/billing/monitor-analyze-usage.md).

$$$azure-integration-billing-deployments$$$Why don’t I see my individual Elastic resources (deployments) in the Azure Marketplace Invoice?
:   The way Azure Marketplace Billing Integration works today, the costs for Elastic resources (deployments) are reported for an {{ecloud}} organization as a single line item, reported against the Marketplace SaaS ID. This includes the Elastic deployments created using the Azure Portal, API, SDK, or CLI, and also the Elastic deployments created directly from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) in the respective {{ecloud}} organization. For granular Elastic resources costs refer to [Monitor and analyze your acccount usage](../../cloud-organization/billing/monitor-analyze-usage.md). As well, for more detail refer to [Integrated billing](#ec-azure-integration-billing-summary).

    :::{image} /deploy-manage/images/cloud-ec-azure-billing-example.png
    :alt: Example billing report in the {{ecloud}} console
    :::


$$$azure-integration-billing-instance-values$$$Why can’t I find Instance ID and Instance Name values from Azure Marketplace Invoice in the Azure Portal?
:   With {{ecloud}} Azure Native ISV Service, the "instance name/ID" shown in the Azure Marketplace invoice is the Azure Marketplace SaaS identifier that represents an {{ecloud}} organization. For Microsoft Azure, `Microsoft.SaaS` (namespace) resources are used for billing Marketplace Resources - in this case, Elastic.

    For instance: Elastic Organization `Org1` is associated with a Marketplace SaaS (Microsoft.SaaS) asset `AzureElastic_GUID_NAME`. The Elastic resources (`Microsoft.Elastic`) `E1`, `E2`, and `E3` within `Org1` are all mapped to `AzureElastic_GUID_NAME`.

    `Microsoft.SaaS` (Instance name) asset is shown in the Azure Marketplace invoice and represents costs related to an {{ecloud}} organization and not individual Elastic resources (deployments). To see the cost breakdown for individual Elastic resources (deployments), refer to [Monitor and analyze your acccount usage](../../cloud-organization/billing/monitor-analyze-usage.md).

    :::{image} /deploy-manage/images/cloud-ec-azure-missing-instance-id.png
    :alt: Instance ID not found error in Azure console
    :::



## Managing your {{ecloud}} deployment [ec-azure-integration-managing-deployment]

$$$azure-integration-whats-included$$$What is included in my {{ecloud}} deployment?
:   Each {{ecloud}} deployment includes:

    * An {{es}} cluster
    * A {{kib}} instance which provides data visualization and a front-end for the {{stack}}
    * An APM server that allows you to easily collect application traces

$$$azure-integration-how-to-access$$$How can I access my {{ecloud}} deployment?
:   Navigate to the deployment overview page in Azure:

    Select a deployment to open the deployment overview page.

    Then you have a few options to access your deployment:

    * **{{es}} endpoint** - the URL for the {{es}} cluster itself
    * **{{kib}} endpoint** - the UI for the {{stack}}, a great way for new users to get started
    * **{{ecloud}}** - Open the **Advanced Settings** link to access the deployment in the {{ecloud}} console, to change the size of the deployment or upgrade it.


$$$azure-integration-modify-deployment$$$How can I modify my {{ecloud}} deployment?
:   Modify your {{ecloud}} deployment in the {{ecloud}} console, which is accessed from the Azure UI through the **Advanced Settings** link on the deployment overview page. In the {{ecloud}} console you can perform [a number of actions against your deployment](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md#ec_how_to_operate_elasticsearch_service).

$$$azure-integration-delete-deployment$$$How can I delete my {{ecloud}} deployment?
:   Delete the deployment directly from the Azure console. The delete operation performs clean-up activities in the Elastic console to ensure any running components are removed, so that no additional charges occur.

$$$azure-integration-delete-resource-group$$$Can I delete the Azure Resource Group containing my deployment?
:   If you delete an Azure Resource Group containing {{ecloud}} resources, the latter will be deleted automatically. However, you should not delete the Azure Resource Group containing the first deployment you created. The usage associated with any other Elastic deployment created outside of the first resource group will continue to get reported and charged against this resource group. If you want to stop all charges to this Resource Group, you should delete the individual deployments.


## Configuring logs and metrics [ec-azure-logs-and-metrics]

$$$azure-integration-monitor$$$How do I monitor my existing Azure services?
:   The {{ecloud}} Azure Native ISV Service simplifies logging for Azure services with the {{stack}}. This integration supports:

    * Azure subscription logs
    * Azure resources logs (check [Supported categories for Azure Resource Logs](https://docs.microsoft.com/en-us/azure/azure-monitor/essentials/resource-logs-categories?WT.mc_id=Portal-Azure_Marketplace_Elastic) for examples)


::::{note}
If you want to send platform logs to a deployment that has [network security policies](/deploy-manage/security/network-security.md) applied, then you need to contact [the Elastic Support Team](#azure-integration-support) to perform additional configurations. Refer support to the article [Azure++ Resource Logs blocked by Traffic Filters](https://support.elastic.co/knowledge/18603788).

::::


The following log types are not supported as part of this integration:

* Azure tenant logs
* Logs from Azure compute services, such as Virtual Machines

::::{note}
If your Azure resources and Elastic deployment are in different subscriptions, before creating diagnostic settings confirm that the `Microsoft.Elastic` resource provider is registered in the subscription in which the Azure resources exist. If not, register the resource provider following these steps:

1. In Azure, navigate to **Subscriptions → Resource providers**.
2. Search for `Microsoft.Elastic` and check that it is registered.

If you already created diagnostic settings before the `Microsoft.Elastic` resource provider was registered, delete and add the diagnostic setting again.

::::


In the Azure console, configure the ingestion of Azure logs into either a new or existing {{ecloud}} deployment:

* When creating a new deployment, use the **Logs & metrics** tab in Azure to specify the log type and a key/value tag pair. Any Azure resources that match on the tag value automatically send log data to the {{ecloud}} deployment, once it’s been created.

:::{image} /deploy-manage/images/cloud-ec-marketplace-azure004.png
:alt: The Logs & Metrics tab on the Create Elastic Resource page
:::

* For existing deployments configure Azure logs from the deployment overview page in the Azure console.

::::{important}
Note that following restrictions for logging:

* Only logs from non-compute Azure services are ingested as part of the configuration detailed in this document. Logs from compute services, such as Virtual Machines, into the {{stack}} will be added in a future release.

* The Azure services must be in one of the [supported regions](cloud://reference/cloud-hosted/ec-regions-templates-instances.md#ec-azure_regions). All regions will be supported in the future.

::::


::::{note}
Your Azure logs may sometimes contain references to a user `Liftr_Elastic`. This user is created automatically by Azure as part of the integration with {{ecloud}}.
::::


To check which of your Azure resources are currently being monitored, navigate to your {{es}} deployment and open the **Monitored resources** tab. Each resource shows one of the following status indicators:

* *Sending* - Logs are currently being sent to the {{es}} cluster.
* *Logs not configured* - Log collection is currently not configured for the resource. Open the **Edit tags** link to configure which logs are collected. For details about tagging resources, check [Use tags to organize your Azure resources and management hierarchy](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources?tabs=json) in the Azure documentation.
* *N/A* - Monitoring is not available for this resource type.
* *Limit reached* - Azure resources can send diagnostic data to a maximum of five outputs. Data is not being sent to the {{es}} cluster because the output limit has already been reached.
* *Failed* - Logs are configured but failed to ship to the {{es}} cluster. For help resolving this problem you can [contact Support](#azure-integration-support).
* *Region not supported* - The Azure resource must be in one of the [supported regions](#ec-supported-regions).

$$$azure-integration-ingest-metrics$$$How do I ingest metrics from my Azure services?
:   Metrics are not supported as part of the current {{ecloud}} Azure Native ISV Service. This will be implemented in a future phase. Metrics can still be collected from all Azure services using Metricbeat. For details, check [Ingest other Azure metrics using the Metricbeat Azure module](../../../solutions/observability/cloud/monitor-microsoft-azure-with-beats.md#azure-step-four).

$$$azure-integration-vm-extensions$$$How can I monitor my Azure virtual machines in {{es}}?
:   You can monitor your Azure virtual machines by installing the Elastic Agent VM extension. Once enabled, the VM extension downloads the Elastic Agent, installs it, and enrols it to the Fleet Server. The Elastic Agent will then send system related logs and metrics to the {{ecloud}} cluster where you can find pre-built system dashboards showing the health and performance of your virtual machines.

    :::{image} /deploy-manage/images/cloud-ec-marketplace-azure010.png
    :alt: A dashboard showing system metrics for the VM
    :::

    **Enabling and disabling VM extensions**

    To enable or disable a VM extension:

    1. In Azure, navigate to your {{es}} deployment.
    2. Select the **Virtual machines** tab
    3. Select one or more virtual machines
    4. Choose **Install Extension** or **Uninstall Extension**.

    :::{image} /deploy-manage/images/cloud-ec-marketplace-azure011.png
    :alt: The Virtual Machines page in Azure
    :::

    While it’s possible to enable or disable a VM extension directly from the VM itself, we recommend always enabling or disabling your {{es}} VM extensions from within the context of your {{es}} deployment.

    **Managing the Elastic Agent VM extension**

    Once installed on the virtual machine, you can manage Elastic Agent either from Fleet or locally on the host where it’s installed. We recommend managing the VM extension through Fleet, because it makes handling and upgrading the agents considerably easier. For more information on the Elastic Agent, check [Manage your Elastic Agents](/reference/fleet/install-elastic-agents.md).

    **Operating system compatibility matrix**

    The Azure Elastic Agent VM extension is supported on the following operating systems:

    | **Platform** | **Version** |
    | --- | --- |
    | Windows | 2008r2+ |
    | CentOS | 6.10+ |
    | Debian | 9,10 |
    | Oracle | 6.8+ |
    | RHEL | 7+ |
    | Ubuntu | 16+ |



## Troubleshooting [ec-azure-integration-troubleshooting]

This section describes some scenarios that you may experience onboarding to {{ecloud}} through the Azure console. If you’re running into issues you can always [get support](#azure-integration-support).

$$$azure-integration-authorization-access$$$I receive an error message about not having the required authorization.
:   When trying to access {{ecloud}} resources, you may get an error message indicating that *the user must have the required authorization.*

    :::{image} /deploy-manage/images/cloud-ec-marketplace-azure026.png
    :alt: Error message displayed in the {{ecloud}} console: To access the resource {resource-name}
    :::

    Elastic is not currently integrated with Azure user management, so sharing deployment resources through the Cloud console with other Azure users is not possible. However, sharing direct access to these resources is possible. For details, check [Is the {{ecloud}} Azure Native ISV Service connected with Azure user management?](#azure-integration-azure-user-management).


$$$azure-integration-deployment-failed-network-security$$$My {{ecloud}} deployment creation failed.
:   When creating a new {{ecloud}} deployment, the deployment creation may fail with a `Your deployment failed` error. The process results with a status message such as:

    ```txt
    {
      "code": "DeploymentFailed",
      "message": "At least one resource deployment operation failed. Please list deployment operations for details. Please see https://aka.ms/DeployOperations for usage details.",
      "details": [
        {
          "code": "500",
          "message": "An error occurred during deployment creation. Please try again. If the problem persists, please contact support@elastic.co."
        }
      ]
    ```

    One possible cause of a deployment creation failure is the default network security policies. Deployments fail to create if a previously created network security policy has enabled the **Include by default** option. When this option is enabled, traffic to the deployment is blocked, including traffic that is part of the {{ecloud}} Azure Native ISV Service. As a result, some of the integration components are not successfully provisioned and the deployment creation fails.

    Follow these steps to resolve the problem:

    1. Login to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
    2. Go to the [Network security page](https://cloud.elastic.co/deployment-features/traffic-filters).
    3. Edit the traffic filter and disable the **Include by default** option.
    4. In Azure, create a new {{ecloud}} deployment.
    5. After the deployment has been created successfully, go back to the [Network security page](https://cloud.elastic.co/deployment-features/traffic-filters) in {{ecloud}} and re-enable the **Include by default** option.


If your deployment still does not create successfully, [contact the Elastic Support Team](#azure-integration-support) for assistance.

$$$azure-integration-failed-sso$$$I can’t SSO into my {{ecloud}} deployment.
:   When you try to access your {{ecloud}} deployment using single sign-on, the access may fail due to missing permission required by your Azure environment.

    You can review your user consent settings configuration following the instructions in [Configure how users consent to applications](https://docs.microsoft.com/en-us/azure/active-directory/manage-apps/configure-user-consent?tabs=azure-portal). To resolve this problem, contact your Azure Administrator.


$$$azure-integration-cant-see-deployment$$$I see some deployments in the {{ecloud}} console but not in the Azure Portal.
:   Elastic Deployments created using the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), the [{{es}} Service API](cloud://reference/cloud-hosted/ec-api-restful.md), or the [{{ecloud}} Terraform provider](https://registry.terraform.io/providers/elastic/ec/latest/docs) are only visible through the {{ecloud}} Console. To have the necessary metadata to be visible in the Azure Portal, {{ecloud}} deployments need to be created in Microsoft Azure.

::::{note}
Mimicking this metadata by manually adding tags to an {{ecloud}} deployment will not work around this limitation. Instead, it will prevent you from being able to delete the deployment using the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
::::


$$$azure-integration-logs-not-ingested$$$My {{ecloud}} Azure Native ISV Service logs are not being ingested.
:   * When you set up monitoring for your Azure services, if your Azure and Elastic resources are in different subscriptions, you need to make sure that the `Microsoft.Elastic` resource provider is registered in the subscription in which the Azure resources exist. Check [How do I monitor my existing Azure services?](#azure-integration-monitor) for details.
* If you are using [network security policies](/deploy-manage/security/network-security.md), reach out to [the Elastic Support Team](#azure-integration-support).



## Getting support [ec-getting-support]

$$$azure-integration-support$$$How do I get support?
:   Support is provided by Elastic. To open a support case:

    1. Navigate to the deployment overview page in the Azure console.
    2. Click **New support request** from the menu.
    3. Click the link to launch the Elastic console and provide further details.

        The Elastic Support team responds based on the SLA response time of your subscription.

        :::{image} /deploy-manage/images/cloud-ec-marketplace-azure005.png
        :alt: The New Support Request page in Azure
        :::


    In case your {{ecloud}} resource is not fully set up and you’re not able to access the Support page, you can always send an email to `support@elastic.co`.


$$$azure-integration-change-level$$$How can I change my subscription level / support level?
:   Your Elastic subscription level includes the support level. Check [How can I change my {{ecloud}} subscription level?](#azure-integration-change-subscription) to make an update.


$$$ec-supported-regions$$$
