---
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
navigation_title: Logs and metrics
---

# Azure Native Service logs and metrics

$$$ec-azure-logs-and-metrics$$$
$$$azure-integration-monitor$$$

The [{{ecloud}} Azure Native Service](/deploy-manage/deploy/elastic-cloud/azure-native-isv-service.md) simplifies logging for Azure services with the {{stack}}. This integration supports:

* Azure subscription logs
* Azure resources logs (check [Supported categories for Azure Resource Logs](https://docs.microsoft.com/en-us/azure/azure-monitor/essentials/resource-logs-categories?WT.mc_id=Portal-Azure_Marketplace_Elastic) for examples)

::::{note}
If you want to send platform logs to a deployment that has [network security policies](/deploy-manage/security/network-security.md) applied, then you need to contact [the Elastic Support Team](azure-native-isv-service-troubleshooting.md#azure-integration-support) to perform additional configurations. Refer support to the article [Azure++ Resource Logs blocked by Traffic Filters](https://support.elastic.co/knowledge/18603788).
::::


## Unsupported log types

The following log types are not supported as part of this integration:

* Azure tenant logs
* Logs from Azure compute services, such as Virtual Machines


## Configure log ingestion

::::{note}
If your Azure resources and Elastic deployment or project are in different subscriptions, before creating diagnostic settings confirm that the `Microsoft.Elastic` resource provider is registered in the subscription in which the Azure resources exist. If not, register the resource provider following these steps:

1. In Azure, navigate to **Subscriptions → Resource providers**.
2. Search for `Microsoft.Elastic` and check that it is registered.

If you already created diagnostic settings before the `Microsoft.Elastic` resource provider was registered, delete and add the diagnostic setting again.
::::

In the Azure portal, configure the ingestion of Azure logs into either a new or existing {{ecloud}} deployment or project:

* When creating a new deployment or project, use the **Logs & metrics** tab in Azure to specify the log type and a key/value tag pair. Any Azure resources that match on the tag value automatically send log data to the {{ecloud}} deployment or project, once it's been created.

:::{image} /deploy-manage/images/cloud-ec-marketplace-azure004.png
:alt: The Logs & Metrics tab on the Create Elastic Resource page
:::

* For existing deployments or projects, configure Azure logs from the [resource overview page](https://portal.azure.com/#browse/Microsoft.Elastic%2Fmonitors) in the Azure portal.

::::{important}
Note the following restrictions for logging:

* Only logs from non-compute Azure services are ingested as part of the configuration detailed in this document. Logs from compute services, such as Virtual Machines, into the {{stack}} will be added in a future release.

* The Azure services must be in one of the [supported regions](cloud://reference/cloud-hosted/ec-regions-templates-instances.md#ec-azure_regions). All regions will be supported in the future.
::::

::::{note}
Your Azure logs might sometimes contain references to a user `Liftr_Elastic`. This user is created automatically by Azure as part of the integration with {{ecloud}}.
::::


## Monitor ingestion status

To check which of your Azure resources are currently being monitored, navigate to your {{es}} deployment or project and open the **Monitored resources** tab. Each resource shows one of the following status indicators:

| Status | Description |
| --- | --- |
| **Sending** | Logs are currently being sent to the {{es}} cluster. |
| **Logs not configured** | Log collection is currently not configured for the resource. Open the **Edit tags** link to configure which logs are collected. For details about tagging resources, check [Use tags to organize your Azure resources and management hierarchy](https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources?tabs=json) in the Azure documentation. |
| **N/A** | Monitoring is not available for this resource type. |
| **Limit reached** | Azure resources can send diagnostic data to a maximum of five outputs. Data is not being sent to the {{es}} cluster because the output limit has already been reached. |
| **Failed** | Logs are configured but failed to ship to the {{es}} cluster. For help resolving this problem you can [contact Support](azure-native-isv-service-troubleshooting.md#azure-integration-support). |
| **Region not supported** | The Azure resource must be in one of the [supported regions](cloud://reference/cloud-hosted/ec-regions-templates-instances.md#ec-azure_regions). |


$$$azure-integration-ingest-metrics$$$

## Ingest metrics

Metrics are not supported as part of the current {{ecloud}} Azure Native Service. This will be implemented in a future phase. Metrics can still be collected from all Azure services using {{metricbeat}}. For details, check [Ingest other Azure metrics using the {{metricbeat}} Azure module](../../../solutions/observability/cloud/monitor-microsoft-azure-with-beats.md#azure-step-four).


$$$azure-integration-vm-extensions$$$

## Monitor virtual machines

You can monitor your Azure virtual machines by installing the {{agent}} VM extension. Once enabled, the VM extension downloads the {{agent}}, installs it, and enrols it to {{fleet-server}}. The {{agent}} will then send system related logs and metrics to the {{ecloud}} deployment or project, where you can find pre-built system dashboards showing the health and performance of your virtual machines.

:::{image} /deploy-manage/images/cloud-ec-marketplace-azure010.png
:alt: A dashboard showing system metrics for the VM
:::

### Enable and disable VM extensions

To enable or disable a VM extension:

1. In Azure, navigate to your {{es}} deployment or project.
2. Select the **Virtual machines** tab.
3. Select one or more virtual machines.
4. Choose **Install Extension** or **Uninstall Extension**.

:::{image} /deploy-manage/images/cloud-ec-marketplace-azure011.png
:alt: The Virtual Machines page in Azure
:::

While it's possible to enable or disable a VM extension directly from the VM itself, we recommend always enabling or disabling your {{es}} VM extensions from within the context of your {{es}} deployment or project.

### Manage the {{agent}} VM extension

Once installed on the virtual machine, you can manage {{agent}} either from {{fleet}} or locally on the host where it's installed. We recommend managing the VM extension through {{fleet}}, because it makes handling and upgrading the agents considerably easier. For more information on {{agent}}, check [Manage your {{agents}}](/reference/fleet/install-elastic-agents.md).

### Operating system compatibility

The Azure {{agent}} VM extension is supported on the following operating systems:

| **Platform** | **Version** |
| --- | --- |
| Windows | 2008r2+ |
| CentOS | 6.10+ |
| Debian | 9,10 |
| Oracle | 6.8+ |
| RHEL | 7+ |
| Ubuntu | 16+ |
