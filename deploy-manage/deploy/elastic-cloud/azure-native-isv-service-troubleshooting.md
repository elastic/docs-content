---
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
navigation_title: Troubleshooting
---

# Azure Native Service troubleshooting

$$$ec-azure-integration-troubleshooting$$$

This page describes some scenarios that you might experience [onboarding to {{ecloud}} through the Azure portal](/deploy-manage/deploy/elastic-cloud/azure-native-isv-service.md). If you're running into issues, you can always [get support](#azure-integration-support).


## Authorization errors

When trying to access {{ecloud}} resources such as {{es}}, {{kib}}, or {{product.apm}} in a deployment or project that was created by another Azure user, the following error is shown:

```txt
To access the resource [r:/<resource-type>/<resource-id>], the user must have the required authorization.
```

Elastic is not currently integrated with Azure user management, so sharing {{ecloud}} resources through the Cloud console with other Azure users is not possible. However, sharing direct access to these resources is possible. For details, refer to [Azure user management](/deploy-manage/deploy/elastic-cloud/azure-native-isv-service.md#azure-integration-multiple-users).


## Deployment creation failure [azure-integration-deployment-failed-network-security]

When creating a new {{ecloud}} deployment or project, the resource creation might fail with a `Your deployment failed` error. The process results with a status message such as:

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

One possible cause of a resource creation failure is the default network security policies. Deployments or projects fail to create if a previously created network security policy has enabled the **Apply to future resources by default** option. When this option is enabled, traffic to the deployment or project is blocked, including traffic that is part of the {{ecloud}} Azure Native Service. As a result, some of the integration components are not successfully provisioned and the deployment or project creation fails.

Follow these steps to resolve the problem:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Go to the [Network security page](https://cloud.elastic.co/access-security/network-security).
3. Edit the policy and disable the **Apply to future resources by default** option.
4. In Azure, create a new {{ecloud}} resource.
5. After the deployment has been created successfully, go back to the [Network security page](https://cloud.elastic.co/access-security/network-security) in {{ecloud}} and re-enable the **Apply to future resources by default** option.

If your resource still does not create successfully, [contact the Elastic Support Team](#azure-integration-support) for assistance.


$$$azure-integration-failed-sso$$$

## SSO failures

When you try to access your {{ecloud}} deployment or project using single sign-on, the access might fail due to missing permission required by your Azure environment.

You can review your user consent settings configuration following the instructions in [Configure how users consent to applications](https://docs.microsoft.com/en-us/azure/active-directory/manage-apps/configure-user-consent?tabs=azure-portal). To resolve this problem, contact your Azure Administrator.


$$$azure-integration-cant-see-deployment$$$

## Deployments or projects not visible in Azure portal

Elastic resources created using the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), the [{{es}} Service API](cloud://reference/cloud-hosted/ec-api-restful.md), or the [{{ecloud}} Terraform provider](https://registry.terraform.io/providers/elastic/ec/latest/docs) are only visible through the {{ecloud}} Console. To have the necessary metadata to be visible in the Azure portal, {{ecloud}} resources need to be created in Microsoft Azure.

::::{note}
Mimicking this metadata by manually adding tags to an {{ecloud}} deployment will not work around this limitation. Instead, it will prevent you from being able to delete the deployment using the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
::::


$$$azure-integration-logs-not-ingested$$$

## Logs not being ingested

* When you set up monitoring for your Azure services, if your Azure and Elastic resources are in different subscriptions, you need to make sure that the `Microsoft.Elastic` resource provider is registered in the subscription in which the Azure resources exist. Check [Configure log ingestion](azure-native-isv-service-logs-metrics.md#configure-log-ingestion) for details.
* If you are using [network security policies](/deploy-manage/security/network-security.md), reach out to [the Elastic Support Team](#azure-integration-support).


$$$azure-integration-support$$$
$$$ec-getting-support$$$

## Get support [azure-integration-support]

Support is provided by Elastic. To open a support case:

1. Navigate to the [resource overview page](https://portal.azure.com/#browse/Microsoft.Elastic%2Fmonitors) in the Azure portal.
2. Click **New support request** from the menu.
3. Click the link to open the {{ecloud}} console and provide further details.

    The Elastic Support team responds based on the SLA response time of your subscription.

    :::{image} /deploy-manage/images/cloud-ec-marketplace-azure005.png
    :alt: The New Support Request page in Azure
    :::

In case your {{ecloud}} resource is not fully set up and you're not able to access the Support page, you can always send an email to `support@elastic.co`.
