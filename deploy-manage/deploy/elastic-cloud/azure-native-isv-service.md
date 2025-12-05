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
    * [Overview, prerequisites, and regions](#azure-integration-get-started)
    * [Pricing and subscription options](#azure-integration-pricing)
    * [Accounts and identity behavior](#azure-integration-existing-email)
    * [Trial conversion and tenant model](#azure-integration-convert-trial)
    * [Deployment methods and migration](#azure-integration-cli-api)
    * [Organization membership scenarios](#azure-integration-multiple-users)

* **Billing**
    * [Azure subscription billing and cost allocation](#azure-integration-billing-which-subscription)
    * [Cost visibility in Azure and Elastic](#azure-integration-billing-elastic-costs)
    * [Invoice details and instance identifiers](#azure-integration-billing-instance-values)

* **Managing your {{ecloud}} deployment**
    * [Deployment components and access options](#azure-integration-whats-included)
    * [Lifecycle operations: modify and delete](#azure-integration-modify-deployment)
    * [Resource groups and deletion behavior](#azure-integration-delete-resource-group)

* **Configuring logs and metrics**
    * [Monitoring Azure services and log ingestion](#azure-integration-monitor)
    * [Metrics ingestion and virtual machine monitoring](#azure-integration-ingest-metrics)

* **Troubleshooting**
    * [Authorization, SSO, and deployment visibility](#azure-integration-azure-user-management)
    * [Deployment failures and network security](#azure-integration-deployment-failed-network-security)
    * [Log ingestion issues](#azure-integration-logs-not-ingested)

* **Support**
    * [Support channels and subscription changes](#azure-integration-support)



## Getting started [ec-azure-integration-getting-started]

$$$azure-integration-get-started$$$
### Overview, prerequisites, and regions

{{ecloud}} is available as an offering through the Azure console and can be created directly from the [list of {{ecloud}} deployments in the Azure portal](https://portal.azure.com/#view/HubsExtension/BrowseResource/resourceType/Microsoft.Elastic%2Fmonitors) by selecting `Create`.

Before setting up an {{ecloud}} deployment, ensure:

* Your Azure account role for the subscription is set as *Owner* or *Contributor*. For details and steps to assign roles, check [Permission to purchase](https://docs.microsoft.com/en-us/marketplace/azure-purchasing-invoicing#permission-to-purchase) in the Azure documentation.
* You are not using an email address that already has an {{ecloud}} account. Use a different Azure account to set up the {{es}} resource, or [contact the Elastic Support Team](#azure-integration-support) for assistance.
* Your Azure subscription has a credit card registered. If you have a non-payment subscription, such as a [Visual Studio Subscription](https://visualstudio.microsoft.com/subscriptions/), you can’t create an {{ecloud}} deployment. Refer to the Azure [Purchase errors](https://docs.microsoft.com/en-us/azure/partner-solutions/elastic/troubleshoot#purchase-errors) troubleshooting documentation for more information.
* To single sign-on into your {{ecloud}} deployment from Azure, you need to request approval from your Azure administrator.

When you create an {{ecloud}} deployment, an {{stack}} cluster is created for you. The default size of this deployment is **16GB of RAM** and **560GB of storage**, across **two availability zones** for redundancy. You can change the size of the deployment, both RAM and storage, from the Elastic console. Usage charges are based on the deployment size, so size your instance efficiently. The deployment defaults to the latest available version of the {{stack}}. Check our [Version policy](available-stack-versions.md) to learn more about when new versions are made available and old versions are removed from service.

The list of supported Azure regions for {{ecloud}} is available here:
[Supported Azure regions](cloud://reference/cloud-hosted/ec-regions-templates-instances.md#ec-azure_regions).

<a id="azure-integration-regions"></a>

$$$azure-integration-pricing$$$
### Pricing and subscription options

The Azure Native ISV Service uses a pay-as-you-go hourly pricing model for each {{ecloud}} deployment. There is no free trial period for this specific offering. Charges are applied to your Azure bill at the end of the month.

Elastic charges include:

* [Hourly consumption based on your active deployments](https://cloud.elastic.co/pricing)
* [Data transfer and snapshot storage charges](https://cloud.elastic.co/deployment-pricing-table)

You can use the {{ecloud}} [Pricing Calculator](https://www.elastic.co/cloud/elasticsearch-service/pricing?page=docs&placement=docs-body) to size a deployment and view the corresponding hourly rate.

By default, the subscription level is **Enterprise**, which grants immediate access to advanced {{stack}} features, such as machine learning, and premium support SLAs. {{ecloud}} offers multiple [subscription levels](https://elastic.co/pricing).

You can change your subscription level from the billing page in the {{ecloud}} console:

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

<a id="azure-integration-subscription-levels"></a>
<a id="azure-integration-change-subscription"></a>

$$$azure-integration-existing-email$$$
### Accounts and identity management

Your email address can be associated with only one Elastic account. If you need to use an email address that is already tied to another {{ecloud}} account, see [Sign up using an email address from another Cloud account](create-an-organization.md) for a suggested workaround.

{{ecloud}} Azure Native ISV Service is **not** integrated with Azure user management. Azure users who deploy {{es}} on Azure view and manage their own clusters through the {{ecloud}} console. Other Azure users in the same tenant cannot access clusters through the {{ecloud}} console unless they are explicitly granted access via identity federation or organization membership.

When trying to access resources such as {{es}}, {{kib}}, or APM in a deployment created by another Azure user, the following error is shown:

:::{image} /deploy-manage/images/cloud-ec-marketplace-azure026.png
:alt: Error message displayed in the {{ecloud}} console: To access the resource {resource-name}
:::

You can share deployment resources directly with other Azure users by [configuring Active Directory single sign-on with the {{es}} cluster](/deploy-manage/users-roles/cluster-or-deployment-auth/oidc-examples.md#ec-securing-oidc-azure).

[{{ecloud}} RBAC capability](../../users-roles/cloud-organization/user-roles.md) is available from the {{ecloud}} console and applies to resources managed there. These RBAC policies are not integrated with the Azure Portal; users interacting with Elastic resources from the Azure Portal are not recognized by {{ecloud}} RBAC policies.

If you already have an {{ecloud}} account with the same email address as your Azure account, you can still use this service. In some cases you may need to contact `support@elastic.co` for assistance aligning the accounts.

<a id="azure-integration-azure-user-management"></a>
<a id="azure-integration-azure-rbac"></a>
<a id="azure-integration-prior-cloud-account"></a>

$$$azure-integration-convert-trial$$$
### Trial conversion and tenant model

You can start a [free {{ecloud}} trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body) and later convert your account to use the Azure Native ISV Service.

When doing so:

* Ensure that trial deployments are created using **Azure** as the cloud provider.
* To convert your trial to the Azure marketplace integration, you must create at least one deployment from the Azure Portal. You can delete this deployment later if you do not need it. After the deployment is created, your marketplace subscription is ready.
* Deployments created during your trial outside of Azure will not appear in the Azure Portal. They remain accessible via the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) and will be billed for their usage.

{{es}} resources deployed through the Azure Native ISV Service are managed by Elastic. They run in Elastic’s Azure infrastructure rather than inside your own Azure tenant. The management capabilities associated with these resources are the same as those used for Elastic’s managed service on other cloud providers.

After you subscribe to {{ecloud}} through the Azure Native ISV Service, Elastic has access to:

* Data defined in the marketplace [SaaS fulfillment Subscription APIs](https://docs.microsoft.com/en-us/azure/marketplace/partner-center-portal/pc-saas-fulfillment-subscription-api).
* Additional data such as:
    * Marketplace subscription ID
    * Marketplace plan ID
    * Azure Account ID
    * Azure Tenant ID
    * Company
    * First name
    * Last name
    * Country

Elastic can also access data from {{ecloud}} Azure Native ISV Service features, including [resource and activity log data](https://docs.microsoft.com/en-us/azure/azure-monitor/essentials/platform-logs-overview), but only if you enable these integrations. By default, Elastic does not have access to this information.

<a id="azure-integration-azure-tenant"></a>
<a id="azure-integration-azure-tenant-info"></a>

$$$azure-integration-cli-api$$$
### Deployment methods and migration

You can deploy {{es}} using a variety of methods:

* **Azure tools**
    * Azure Portal
    * [Azure Terraform](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/elastic_cloud_elasticsearch)
    * [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/elastic?view=azure-cli-latest)
    * Azure [REST API](https://docs.microsoft.com/en-us/rest/api/elastic)
    * [PowerShell](https://docs.microsoft.com/en-us/powershell/module/az.elastic/?view=azps-8.0.0#elastic)

* **Official Azure SDKs**
    * [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/README.md)
    * [Java](https://github.com/Azure/azure-sdk-for-java/blob/azure-resourcemanager-elastic_1.0.0-beta.1/README.md)
    * [.NET](https://github.com/Azure/azure-sdk-for-net/blob/main/README.md)
    * [Rust](https://github.com/Azure/azure-sdk-for-rust/blob/main/services/README.md)

* **Deploy using {{ecloud}}**
    * {{ecloud}} [console](https://cloud.elastic.co?page=docs&placement=docs-body)
    * {{ecloud}} [REST API](cloud://reference/cloud-hosted/ec-api-restful.md)
    * {{ecloud}} [command line tool](ecctl://reference/index.md)
    * {{ecloud}} [Terraform provider](https://registry.terraform.io/providers/elastic/ec/latest/docs)

Note that when you use any of the {{ecloud}} methods directly, the resulting {{es}} deployment will not be visible in the Azure Portal.

To migrate your data from the classic Azure marketplace account to the Azure Native ISV Service:

1. From your classic Azure marketplace account, navigate to the deployment and [configure a custom snapshot repository using Azure Blob Storage](../../tools/snapshot-and-restore/ec-azure-snapshotting.md).
2. Using the newly configured snapshot repository, [create a snapshot](../../tools/snapshot-and-restore/create-snapshots.md) of the data to migrate.
3. Navigate to Azure and log in as the user that manages the {{es}} resources.
4. Before proceeding, ensure the new account is configured according to the [prerequisites](#azure-integration-get-started).
5. Create a [new {{es}} resource](#azure-integration-get-started) for each existing deployment that needs migration from the classic Azure account.
6. In the new {{es}} resource, follow the steps in [Restore from a snapshot](../../../manage-data/migrate.md#ec-restore-snapshots) to register the custom snapshot repository from Step 1.
7. In the same set of steps, restore the snapshot data from the snapshot repository that you registered.
8. Confirm that the data has moved successfully into your new {{es}} resource on Azure.
9. To remove the old Azure subscription and the old deployments, go to the [Azure SaaS page](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.SaaS%2Fresources) and unsubscribe from the {{ecloud}} ({{es}}) marketplace subscription. This action triggers termination of the existing deployments.

<a id="azure-integration-migrate"></a>

$$$azure-integration-multiple-users$$$
### Organization membership scenarios

Multiple Azure users can deploy resources into the same {{ecloud}} organization. Before another user creates a native resource from the Azure Portal, invite them to your {{ecloud}} organization at [https://cloud.elastic.co/account/members](https://cloud.elastic.co/account/members). When they create the resource, it is added to the existing organization instead of creating a new one. This allows you to benefit from consolidated billing, RBAC, and other organization-level capabilities.

You can also add Azure users as members of your organization even if they don’t have an inbox. Reach out to Elastic Support for help onboarding these users.

<a id="azure-integration-no-inbox"></a>

## Billing [ec-azure-integration-billing-faq]

$$$azure-integration-billing-which-subscription$$$
### Azure subscription billing and cost allocation

The Azure Native ISV Service posts all Elastic deployment costs for an {{ecloud}} organization to **the Azure subscription used to create the first Azure-native deployment**, regardless of where later deployments are created.

To charge different Azure subscriptions, deployments must belong to **different {{ecloud}} organizations**.

---

$$$azure-integration-billing-elastic-costs$$$
### Cost visibility in Azure and Elastic

Azure Marketplace shows Elastic costs as **Marketplace charges**, sometimes grouped under **Unassigned**.  
For detailed per-deployment usage, use the Elastic Cloud Console:

**Account & Billing → Usage**

---

$$$azure-integration-billing-instance-values$$$
### Invoice details and instance identifiers

Azure invoices display a single **SaaS resource identifier** that corresponds to the {{ecloud}} organization.  
This is expected: Azure does not list Elastic deployments individually in Marketplace invoices.

Use Elastic’s usage reporting for detailed cost breakdowns.

## Managing your {{ecloud}} deployment

$$$azure-integration-whats-included$$$
### Deployment components and access options

Each {{ecloud}} deployment includes:
* an {{es}} cluster
* a {{kib}} instance
* an APM server

From the Azure deployment overview page, you can open:
* **{{es}} endpoint**
* **{{kib}} endpoint**
* **Advanced Settings** → full management in the {{ecloud}} console

---

$$$azure-integration-modify-deployment$$$
### Lifecycle operations: modify and delete

All scaling, upgrades, and configuration changes happen in the {{ecloud}} console.

Deleting a deployment in Azure triggers full cleanup in Elastic Cloud and stops billing.

---

$$$azure-integration-delete-resource-group$$$
### Resource groups and deletion behavior

Deleting an Azure Resource Group also deletes its {{ecloud}} resources.

Do **not** delete the Resource Group containing your first Azure-native deployment, as charges may continue from other deployments.

To stop billing, delete deployments individually before removing the Resource Group.

## Configuring logs and metrics

$$$azure-integration-monitor$$$
### Monitoring existing Azure services

The {{ecloud}} Azure Native ISV Service simplifies logging for Azure services with the {{stack}}. This integration supports:

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
Note the following restrictions for logging:

* Only logs from non-compute Azure services are ingested as part of the configuration detailed in this document. Logs from compute services, such as Virtual Machines, into the {{stack}} will be added in a future release.

* The Azure services must be in one of the [supported regions](cloud://reference/cloud-hosted/ec-regions-templates-instances.md#ec-azure_regions). All regions will be supported in the future.
  ::::

::::{note}
Your Azure logs may sometimes contain references to a user `Liftr_Elastic`. This user is created automatically by Azure as part of the integration with {{ecloud}}.
::::

To check which of your Azure resources are currently being monitored, navigate to your {{es}} deployment and open the **Monitored resources** tab. Each resource shows one of the following status indicators:

* *Sending* - Logs are currently being sent to the {{es}} cluster.
* *Logs not configured* - Log collection is currently not configured for the resource. Open the **Edit tags** link to configure which logs are collected. For details about tagging, check [Use tags to organize your Azure resources and management hierarchy](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources?tabs=json).
* *N/A* - Monitoring is not available for this resource type.
* *Limit reached* - Azure resources can send diagnostic data to a maximum of five outputs. Data is not being sent to the {{es}} cluster because the output limit has already been reached.
* *Failed* - Logs are configured but failed to ship. For help resolving this problem you can [contact Support](#azure-integration-support).
* *Region not supported* - The Azure resource must be in one of the [supported regions](#ec-supported-regions).

$$$azure-integration-ingest-metrics$$$
### Ingesting metrics from Azure services

Metrics are not supported as part of the current {{ecloud}} Azure Native ISV Service. This will be added in a future release.

Metrics can still be collected from all Azure services using Metricbeat. For details, check [Ingest other Azure metrics using the Metricbeat Azure module](../../../solutions/observability/cloud/monitor-microsoft-azure-with-beats.md#azure-step-four).

$$$azure-integration-vm-extensions$$$
### Monitoring Azure virtual machines

You can monitor Azure virtual machines by installing the Elastic Agent VM extension. Once enabled:

1. The VM extension downloads the Elastic Agent
2. Installs it
3. Enrolls it to Fleet Server
4. Sends system logs and metrics to your {{ecloud}} cluster  
   (where dashboards display VM health and performance)

:::{image} /deploy-manage/images/cloud-ec-marketplace-azure010.png
:alt: A dashboard showing system metrics for the VM
:::

#### Enabling and disabling VM extensions

To enable or disable a VM extension:

1. In Azure, navigate to your {{es}} deployment.
2. Select the **Virtual machines** tab.
3. Select one or more virtual machines.
4. Choose **Install Extension** or **Uninstall Extension**.

:::{image} /deploy-manage/images/cloud-ec-marketplace-azure011.png
:alt: The Virtu
:::

## Troubleshooting [ec-azure-integration-troubleshooting]

This section describes some scenarios that you may experience onboarding to {{ecloud}} through the Azure console. If you’re running into issues you can always [get support](#azure-integration-support).

$$$azure-integration-authorization-access$$$
### Authorization errors related to required access

When trying to access {{ecloud}} resources, you may get an error message indicating that *the user must have the required authorization.*

:::{image} /deploy-manage/images/cloud-ec-marketplace-azure026.png
:alt: Error message displayed in the {{ecloud}} console: To access the resource {resource-name}
:::

Elastic is not currently integrated with Azure user management, so sharing deployment resources through the Cloud console with other Azure users is not possible. However, sharing direct access to these resources is possible. For details, check [Is the {{ecloud}} Azure Native ISV Service connected with Azure user management?](#azure-integration-azure-user-management).

$$$azure-integration-deployment-failed-network-security$$$
### Deployment creation failures related to network security policies

When creating a new {{ecloud}} deployment, the deployment creation may fail with a `Your deployment failed` error. The process can result in:

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
}
```
A common cause is **network security policies** with **Include by default** enabled.  
This blocks required traffic and prevents the Azure Native ISV Service components from provisioning.

#### Resolution steps:

1. Log into the {{ecloud}} Console  
   https://cloud.elastic.co?page=docs&placement=docs-body

2. Go to:  
   Network security page  
   https://cloud.elastic.co/deployment-features/traffic-filters

3. Edit the traffic filter → **Disable** “Include by default”

4. Go back to Azure → Create the {{ecloud}} deployment

5. After successful creation → Re-enable “Include by default” (optional)

If the deployment continues to fail, contact Elastic Support.


### Single sign-on (SSO) failures $$$azure-integration-failed-sso$$$

If SSO into your {{ecloud}} deployment fails, required Azure permissions may be missing.

Review Azure user consent settings:  
https://docs.microsoft.com/en-us/azure/active-directory/manage-apps/configure-user-consent?tabs=azure-portal

Contact your Azure Administrator to adjust permissions.


### Deployments visible in Elastic Cloud but not in the Azure Portal  $$$azure-integration-cant-see-deployment$$$

Deployments created using:

- {{ecloud}} Console
- {{es}} Service API
- {{ecloud}} Terraform provider

…are **not visible in Azure**, because Azure-native metadata is only attached when the deployment is created from Azure.

NOTE: Adding Azure-native metadata manually (such as copying tags) will **break deletion from Elastic Cloud**.


### Log ingestion issues  $$$azure-integration-logs-not-ingested$$$

Log ingestion may fail if:

1. Azure and Elastic resources are in **different subscriptions** and  
   `Microsoft.Elastic` provider is **not registered** in the subscription containing the Azure resources.

   See: How do I monitor my existing Azure services? (#azure-integration-monitor)

2. Network security policies interfere with diagnostic traffic.

If issues persist, contact Elastic Support.


## Getting support [ec-getting-support]

### Getting support  $$$azure-integration-support$$$

Support is provided by Elastic.

To open a support case from Azure:

1. Open the deployment overview page in the Azure portal.
2. Select **New support request**.
3. Follow the link to open the Elastic Cloud console and provide additional details.

Elastic Support responses follow your subscription SLA.

(IMAGE: cloud-ec-marketplace-azure005.png)

If you cannot access the Elastic support interface (for example, your deployment never finished creating), you may email:

support@elastic.co


### Changing subscription or support level  $$$azure-integration-change-level$$$

Your support level is determined by your Elastic subscription level.

To adjust your subscription level, see:  
How can I change my {{ecloud}} subscription level? (#azure-integration-change-subscription)

$$$ec-supported-regions$$$
