---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-azure-marketplace-native.html
applies_to:
  deployment:
    ess: ga
  serverless: ga
navigation_title: Azure Native Service
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# {{ecloud}} Azure Native Service [ec-azure-marketplace-native]

The {{ecloud}} Azure Native Service allows you to deploy managed instances of the {{stack}} directly in Azure, through the Microsoft Marketplace. The service brings the following benefits:

* **Easy deployment for managed {{stack}} instances**

    {{stack}} instances managed by Elastic are deployed directly from the Azure portal. This provides the complete {{stack}} experience with all available features.

* **Integrated billing**

    You are billed directly to your Azure account; no need to configure billing details in Elastic. See [Integrated billing](#ec-azure-integration-billing-summary) for details.

* **Easy consolidation of your Azure logs in Elastic**

    Use a single-step setup to ingest logs from your Azure services into the {{stack}}. For details, refer to [Azure Native Service logs and metrics](azure-native-isv-service-logs-metrics.md).

::::{tip}
The full product name in the Microsoft Marketplace is _Elasticsearch - Search & Vector Database (Free 7-Day Trial)_.
::::

$$$ec-azure-integration-faq$$$

## Prerequisites [azure-integration-get-started]

$$$azure-integration-regions$$$
$$$azure-integration-existing-email$$$
$$$ec-supported-regions$$$

Before setting up an {{ecloud}} deployment or project through the Azure Native Service, review the following requirements:

* Your Azure account role for the subscription must be set to **Owner** or **Contributor**. For details and steps to assign roles, refer to [Roles and permissions](https://learn.microsoft.com/en-us/marketplace/roles-permissions#roles-and-permissions-1) in the Azure documentation.
* If you already have an {{ecloud}} account, you can sign in with your existing credentials during setup. Your new resource will be linked to an existing organization or a new one will be created. For details on how accounts and organizations work together, refer to [Subscribe from a marketplace](subscribe-from-marketplace.md#ec-marketplace-org-relationship).
* You must have a payment method registered on your Azure subscription. If you have a non-payment subscription, such as a [Virtual Studio Subscription](https://visualstudio.microsoft.com/subscriptions/), you can't create an {{ecloud}} deployment. Refer to the Azure [Purchase errors](https://learn.microsoft.com/en-us/azure/partner-solutions/elastic/troubleshoot#marketplace-purchase-errors) troubleshooting documentation for more information.
* To single sign-on into your {{ecloud}} deployment or project from Azure, you need to request approval from your Azure administrator.

## Create a deployment or {{serverless-short}} project [ec-azure-integration-getting-started]

To create a deployment or {{serverless-short}} project directly from the Azure portal, go to [the list of {{ecloud}} resources in the Azure portal](https://portal.azure.com/#browse/Microsoft.Elastic%2Fmonitors) and select **Create**. On the next page, select your hosting type: **{{serverless-short}}** or **Cloud Hosted**.

The selected resource is created for you.

If you select **{{serverless-short}}**, then the project is [sized automatically for you](/deploy-manage/deploy/elastic-cloud/serverless.md#_benefits_of_serverless_projects) and adjusts to your usage.

If you select **Cloud Hosted**, a deployment is created with **16GB of RAM** and **560GB of storage**, across **two availability zones** for redundancy. The size of the deployment, both RAM and storage, can be changed [directly in the {{ecloud}} console](/deploy-manage/deploy/elastic-cloud/configure.md). Usage charges are based on the deployment size, so size your instance efficiently. The deployment defaults to the latest available version of the {{stack}}. Check our [Version policy](available-stack-versions.md) to learn more about when new versions are made available and old versions are removed from service.

### Alternative creation methods [azure-integration-cli-api]

You can create and manage {{ecloud}} deployments and projects using a variety of tools:

* **Azure tools**
    * The Azure portal
    * [Azure Terraform](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/elastic_cloud_elasticsearch)
    * The [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/elastic?view=azure-cli-latest)
    * The Azure [REST API](https://docs.microsoft.com/en-us/rest/api/elastic)
    * [PowerShell](https://docs.microsoft.com/en-us/powershell/module/az.elastic/?view=azps-8.0.0#elastic)

* **Official Azure SDKs**
    * [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/README.md)
    * [Java](https://github.com/Azure/azure-sdk-for-java/blob/azure-resourcemanager-elastic_1.0.0-beta.1/README.md)
    * [.NET](https://github.com/Azure/azure-sdk-for-net/blob/main/README.md)
    * [Rust](https://github.com/Azure/azure-sdk-for-rust/blob/main/services/README.md)

* **{{ecloud}}**
    * The {{ecloud}} [console](https://cloud.elastic.co?page=docs&placement=docs-body)
    * The {{ecloud}} [REST API](cloud://reference/cloud-hosted/ec-api-restful.md)
    * The {{ecloud}} [command line tool](ecctl://reference/index.md) (ECCTL)
    * The {{ecloud}} [Terraform provider](https://registry.terraform.io/providers/elastic/ec/latest/docs)
  
    Refer to [Tools and APIs](/deploy-manage/deploy/elastic-cloud/tools-apis.md) for a complete list.

    :::{note}
    When you use any of the {{ecloud}} methods to create a deployment or project, it will not be available in the Azure portal. To have the necessary metadata to be visible in the Azure portal, {{ecloud}} resources need to be created in Microsoft Azure.
    :::

## Access your deployment or project [azure-integration-how-to-access]

$$$azure-integration-whats-included$$$
$$$azure-integration-modify-deployment$$$
$$$ec-azure-integration-managing-deployment$$$

Navigate to the [{{ecloud}} overview page](https://portal.azure.com/#browse/Microsoft.Elastic%2Fmonitors) in the Azure portal and select a resource.

You have a few options to access your deployment or project:

* **{{es}} endpoint** -- the URL for communicating with {{es}} directly
* **{{kib}} endpoint** -- the UI for your deployment or project, a great way for new users to get started
* **{{ecloud}}** -- Open the **Advanced Settings** link to access the deployment or project in the {{ecloud}} console. You can use this interface to alter your deployment or project settings, or perform other administrative tasks. For more details, refer to the following sections:
  * [{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md#ec_how_to_operate_elasticsearch_service)
  * [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md#get-started)

## Multi-org accounts and the Azure portal [ec-azure-multi-org-limitations]

Unlike {{aws}} and {{gcp}}, the Azure portal does not provide an organization picker during resource creation. When your account has a single organization, the Azure portal automatically adds new resources to that organization and can handle trial conversion. When your account has multiple organizations, the portal may not be able to determine which organization to target.

The following limitations apply:

- **Multiple Azure MP organizations:** You can't create resources from the Azure portal. Create resources directly from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) instead, where you can select the specific organization to use.
- **Multiple eligible trial organizations:** You can't convert a trial from the Azure portal. To resolve this, leave the other trial organizations so that only one eligible organization remains. Alternatively, use the [{{aws}}](aws-marketplace.md) or [{{gcp}}](google-cloud-platform-marketplace.md) marketplace instead, which support an organization picker during sign-up.

## Trials and existing accounts [ec-azure-integration-trials]

$$$azure-integration-prior-cloud-account$$$
If you already have an {{ecloud}} account, you can sign in with your existing credentials when creating an Elastic resource in the Azure portal. If your account has a single organization, the resource is added to that organization. If you have multiple organizations, refer to [Multi-org accounts and the Azure portal](#ec-azure-multi-org-limitations).

### Convert a trial to Azure Native Service [azure-integration-convert-trial]

If you have an existing {{ecloud}} trial, you can convert it to a Microsoft Marketplace subscription. For step-by-step instructions, refer to [Convert a trial to a marketplace subscription](marketplace-trial-conversion.md#ec-marketplace-trial-conversion-azure).

Keep in mind:

* When creating resources in the trial account, specify Azure as the cloud provider so that the organization is [eligible for conversion](marketplace-trial-conversion.md#ec-marketplace-conversion-candidates).
* To convert your trial to the Microsoft Marketplace, [create a resource](#ec-azure-integration-getting-started) in the Azure portal. Delete this resource if you don't need it. After you create the new resource, your marketplace subscription is ready.
* Any resources created during your trial won't show up in the Azure portal, because they weren't created in Azure, but they are still accessible through the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) and you are billed for their usage.

### Start a trial from Microsoft Marketplace [azure-integration-native-trials]

You can start a 7-day trial by creating a deployment through the Microsoft Marketplace. The following restrictions apply:

* During the 7-day trial period, you can create up to one deployment and three serverless projects. If you want to convert to a paid subscription before the end of the trial period, contact `support@elastic.co`.
* After 7 days, the trial will automatically convert to a paid offering. If you don't want to convert your trial, then you can delete the resource you created in the Azure portal. You can also contact Elastic Support to unsubscribe, which might result in your resources being deleted after a grace period.
* You can sign up for only one trial per user account. After the trial expires, you can't start another trial. If you need a trial extension, reach out to Elastic Support.

## Pricing [azure-integration-pricing]

$$$azure-integration-subscription-levels$$$

Pricing is pay-as-you-go per hour for each {{ecloud}} deployment or project created. Charges are applied to your Azure bill at the end of the month. 

When you create your first deployment or project, the subscription defaults to the Enterprise subscription, which grants premium support response time SLAs. For {{ech}} deployments, the subscription also controls the features that are available. In {{ech}}, this Enterprise subscription includes advanced {{stack}} features like {{ml}}. 

For an overview of all of the subscription levels available, refer to [subscription levels](https://elastic.co/pricing). To learn how to change your subscription level, refer to [](/deploy-manage/cloud-organization/billing/manage-subscription.md).

To learn about Elastic charges related to your deployments or projects, refer to the following resources:
* [](/deploy-manage/cloud-organization/billing/cloud-hosted-deployment-billing-dimensions.md)
* [](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md)
* [{{ecloud}} pricing table](https://cloud.elastic.co/cloud-pricing-table)

To estimate your costs, you can use the following calculators:
* [{{ech}} pricing calculator](https://cloud.elastic.co/pricing)
* [{{serverless-full}} pricing calculator](https://cloud.elastic.co/pricing/serverless)


## Integrated billing [ec-azure-integration-billing-summary]

Azure Native Service includes integrated billing: Elastic resource costs are posted to your Azure subscription through the Microsoft Commercial Marketplace. You can create various {{ecloud}} resources (deployments and projects) across different Azure subscriptions, with all of the costs associated with an {{ecloud}} organization posted to a single Azure subscription.

The integrated billing process involves the following concepts:

* **Microsoft Marketplace SaaS ID**: This is a unique identifier that's generated one time by Microsoft Commercial Marketplace when a user creates their first Elastic resource (deployment or project) using the Microsoft Azure (Portal, API, SDK, or Terraform). This is mapped to a User ID and Azure Subscription ID.
* **{{ecloud}} organization**: An [organization](/deploy-manage/cloud-organization.md) is the foundational construct under which everything in {{ecloud}} is grouped and managed. An organization is created as a step during the creation of your first Elastic resource, whether that's done through Microsoft Azure (Portal, API, SDK, or Terraform). The initial member of the {{ecloud}} organization can then invite other users.
* **Elastic resource (deployment or project)**: An {{ecloud}} deployment or project helps you manage an {{es}} cluster and instances of other Elastic products in one place. You can work with Elastic resources from within the Azure ecosystem. Multiple users in the {{ecloud}} organization can create different resources from different Azure subscriptions. They can also create resources from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).

The following diagram shows the mapping between Microsoft Azure IDs, {{ecloud}} organization IDs, and your Elastic resources (deployments).

% TODO: update diagram for multi-org
:::{image} /deploy-manage/images/cloud-ec-azure-billing-mapping.png
:alt: Azure to {{ecloud}} mappings
:::

The following diagram shows how your {{ecloud}} organization costs are reported in Microsoft Azure.

:::{image} /deploy-manage/images/cloud-ec-azure-billing-reporting.png
:alt: Azure to {{ecloud}} mappings
:::

### Resubscribe to Azure [azure-resubscribe-flow]

If your organization is currently unsubscribed from the Microsoft Marketplace, you can resubscribe through any of your existing Azure deployments in the Azure portal:

1. Open one of your deployments or projects to view its overview page.
2. From the left navigation pane, select **Connected Elastic Cloud Resources**.

:::{image} /deploy-manage/images/azure-reconnect-window.png
:alt: The resubscription illustration
:::

3. Click **Resubscribe**. A new window should appear.
4. Choose the subscription you want to resubscribe to and confirm.

### Cost visibility in Azure [ec-azure-integration-billing-faq]


#### Subscription used for billing [azure-integration-billing-which-subscription]

$$$azure-integration-billing-which-subscription$$$

The Microsoft Marketplace integrated billing posts all of the Elastic resource costs related to an {{ecloud}} organization to the Azure subscription you used to create your first-ever Elastic resource, even if your individual Elastic resources (deployments and projects) are spread across different Azure subscriptions.

$$$azure-integration-billing-different-deployments$$$
To have different Elastic resources' costs reported to different Azure subscriptions, they need to be in separate {{ecloud}} organizations. To create a separate organization, [create a new Elastic resource](#ec-azure-integration-getting-started) from the Azure portal. A new organization is created as part of the resource creation process.

#### How costs are reported

$$$azure-integration-billing-deployments$$$

The costs for Elastic resources are reported for an {{ecloud}} organization as a single line item, reported against the Marketplace SaaS ID. This includes the resources created using the Azure portal, API, SDK, or CLI, and also those created directly from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) in the respective {{ecloud}} organization.

$$$azure-integration-billing-elastic-costs$$$

The costs associated with Elastic resources are reported under **unassigned** in the Azure portal. Refer to [Understand your Azure external services charges](https://learn.microsoft.com/en-us/azure/cost-management-billing/understand/understand-azure-marketplace-charges) in the Microsoft Documentation to understand Elastic resource costs. For granular Elastic resource costs, refer to [Monitor and analyze your account usage](/deploy-manage/cloud-organization/billing/monitor-analyze-usage.md).

$$$azure-integration-billing-instance-values$$$

#### Invoice values

* **Instance name/ID** The Microsoft Marketplace SaaS identifier that represents an {{ecloud}} organization. For Microsoft Azure, `Microsoft.SaaS` (namespace) resources are used for billing Marketplace Resources -- in this case, Elastic.

    For instance: Elastic Organization `Org1` is associated with a Marketplace SaaS (Microsoft.SaaS) asset `AzureElastic_GUID_NAME`. The Elastic resources (`Microsoft.Elastic`) `E1`, `E2`, and `E3` within `Org1` are all mapped to `AzureElastic_GUID_NAME`.

* `Microsoft.SaaS` (Instance name) asset is shown in the Microsoft Marketplace invoice and represents costs related to an {{ecloud}} organization and not individual Elastic resources. To understand the cost breakdown for individual Elastic resources, refer to [Monitor and analyze your account usage](../../cloud-organization/billing/monitor-analyze-usage.md).

## Users and access [ec-azure-integration-users-access]

[User access](/deploy-manage/users-roles.md#cloud-organization-level) is managed within the {{ecloud}} organization, or at the deployment level.

There are several options to integrate Microsoft authentication with {{ecloud}}:
* {{serverless-full}} projects and {{ech}} deployments: [Configure SAML single sign-on](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md). Refer to [](/deploy-manage/users-roles/cloud-organization/register-elastic-cloud-saml-in-microsoft-entra-id.md) for a Microsoft Entra ID example.
* {{ech}} deployments: [Configure Azure Active Directory single sign-on](/deploy-manage/users-roles/cluster-or-deployment-auth/saml-entra.md).

{{ecloud}} is not automatically integrated with Azure:

* [{{ecloud}} RBAC capabilities](../../users-roles/cloud-organization/user-roles.md) are available only from the {{ecloud}} Console and is not integrated with Azure portal. Users who interact with Elastic resources from Azure portal will not be recognized by the {{ecloud}} RBAC policies.

$$$azure-integration-authorization-access$$$
* Elastic is not currently integrated with Azure user management. Azure users who deploy {{es}} on Azure view and manage their own cluster through the Cloud console. Other Azure users in the same tenant cannot access clusters through the Cloud console other than those that they themselves created.

    When trying to access resources such as {{es}}, {{kib}}, or {{product.apm}} in a deployment or project that was created by another Azure user, the following error is shown:

    ```txt
    To access the resource [r:/<resource-type>/<resource-id>], the user must have the required authorization.
    ```

### Allow multiple users to create resources in an organization [azure-integration-multiple-users]

$$$azure-integration-no-inbox$$$

Multiple Azure users can deploy to the same {{ecloud}} organization. Before another user creates a native resource from the Azure portal, invite them to your {{ecloud}} organization at [https://cloud.elastic.co/account/members](https://cloud.elastic.co/account/members). When they create the resource, it will get added to the existing organization instead of creating a new one, allowing you to benefit from consolidated billing, RBAC, and other benefits of an {{ecloud}} organization.

You can add Azure users as members of your organization even if they don't have an inbox. Reach out to Elastic support.

## Azure tenant information [azure-integration-azure-tenant]

{{es}} resources deployed in an Azure tenant are managed by Elastic. The management capabilities associated with this tenant are the same as used to run Elastic's managed service, which also allows users to deploy on Azure. {{es}} is not deployed into your Azure tenant.

$$$azure-integration-azure-tenant-info$$$
After you subscribe to {{ecloud}} through the Azure Native Service, Elastic has access to the following Azure tenant information:

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

Elastic can also access data from {{ecloud}} Azure Native Service features, including [resource and activity log data](https://docs.microsoft.com/en-us/azure/azure-monitor/essentials/platform-logs-overview). This data is available when [log ingestion](azure-native-isv-service-logs-metrics.md#configure-log-ingestion) is configured. By default, Elastic does not have access to this information.

## Delete a resource or Azure resource group [ec-azure-integration-delete]

$$$azure-integration-delete-deployment$$$
Delete the deployment directly from the Azure portal. The delete operation performs clean-up activities in the Elastic console to ensure any running components are removed, so that no additional charges occur.

$$$azure-integration-delete-resource-group$$$
If you delete an Azure Resource Group containing {{ecloud}} resources, the latter will be deleted automatically. However, you should not delete the Azure Resource Group containing the first deployment or project that you created. The usage associated with any other Elastic deployment created outside of the first resource group will continue to get reported and charged against this resource group. If you want to stop all charges to this Resource Group, you should delete the individual deployments.

## Troubleshooting

To troubleshoot issues with the Azure Native Service, refer to [](azure-native-isv-service-troubleshooting.md).
