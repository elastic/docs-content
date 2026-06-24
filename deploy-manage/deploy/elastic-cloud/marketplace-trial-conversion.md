---
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
---

# Convert a trial to a marketplace subscription [ec-marketplace-trial-conversion]

If you started with an {{ecloud}} trial and want to pay through a cloud marketplace instead of adding a credit card directly, you can convert your trial organization to a marketplace subscription. Your existing deployments, projects, and data are preserved during the conversion.

This works for both active and expired trials, as long as the organization is eligible for conversion and the data retention window has not passed.

## Requirements

- An {{ecloud}} trial organization that is [eligible for conversion](#ec-marketplace-conversion-candidates).
- Access to one of the supported marketplaces: [{{aws}} Marketplace](aws-marketplace.md), [Azure Marketplace](azure-native-isv-service.md), or [{{gcp}} Marketplace](google-cloud-platform-marketplace.md).
- The email address associated with your {{ecloud}} account matches the credentials you use during the marketplace sign-up process.
- To convert from the Azure Marketplace: your {{ecloud}} account must only be owner of a single [convertible](#ec-marketplace-conversion-candidates) organization.

## Convert your trial in {{aws}} and {{gcp}} marketplaces [ec-marketplace-trial-conversion-aws-gcp]

For {{aws}} and {{gcp}}, you complete the subscription in the marketplace and then sign in to {{ecloud}} to link the subscription to an organization.

::::::{stepper}
:::::{step} Create your {{ecloud}} trial
If you haven't already, [sign up](create-an-organization.md) for an {{ecloud}} trial using the email address you prefer.
:::::
:::::{step} Subscribe through your marketplace

::::{tab-set}
:::{tab-item} {{aws}} Marketplace
Go to the [{{ecloud}} listing on the {{aws}} Marketplace](https://aws.amazon.com/marketplace/pp/prodview-voru33wi6xs7k) and click **View purchase options**, then **Subscribe** and **Set Up Your Account**.
:::
:::{tab-item} {{gcp}} Marketplace
Go to the [{{ecloud}} listing on the {{gcp}} Marketplace](https://console.cloud.google.com/marketplace/product/elastic-prod/elastic-cloud). Select **Subscribe**, accept the terms, and choose **Sign up with Elastic**.
:::
::::
:::::
:::::{step} Sign in with your existing credentials
When prompted to create a new account or sign in, choose to **sign in** with your existing {{ecloud}} credentials.
:::::
:::::{step} Select the organization to upgrade
The upgrade page shows the cloud provider account that the subscription will be linked to. Confirm this is the correct account before continuing.

What happens next depends on how many organizations your account belongs to:

- **Single convertible trial organization:** You are presented with an option to upgrade the trial to the marketplace subscription. Billing through the marketplace begins immediately upon upgrade.
- **Multiple organizations:** You are shown a list of your eligible organizations. Click the organization you want to upgrade. To also see organizations that aren't eligible, toggle **Show non-convertible organizations**.

You can also choose to **create a new organization** instead of upgrading an existing one. The new organization starts with its own 7-day marketplace trial.

If none of your existing organizations are eligible for upgrading, you can still create a new organization through the marketplace, or refer to [Which organizations can be converted](#ec-marketplace-conversion-candidates) to understand why.
:::::
::::::

## Convert your trial in the Azure Marketplace [ec-marketplace-trial-conversion-azure]

The Azure flow works differently from {{aws}} and {{gcp}} because Elastic resources are created directly from the Azure portal rather than through an Elastic sign-up page.

::::::{stepper}
:::::{step} Create your {{ecloud}} trial
If you haven't already, [sign up](create-an-organization.md) for an {{ecloud}} trial using the email address you prefer. When creating resources during the trial, specify Azure as the cloud provider so that the organization is [eligible for conversion](#ec-marketplace-conversion-candidates).
:::::
:::::{step} Create an Elastic resource from the Azure portal
Go to the [{{ecloud}} ({{es}}) - An Azure Native ISV Service](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/elastic.ec-azure-pp) listing in the Azure portal. Select **Subscribe** and follow the prompts to create an Elastic resource.

When you create the resource, it is linked to your existing trial organization and the trial is converted to an Azure Marketplace subscription. You can delete the new deployment afterward if you don't need it.
:::::
::::::

## Which organizations can be converted [ec-marketplace-conversion-candidates]

Not all organizations are eligible for marketplace conversion. An organization can be converted if it meets the following conditions:

- You are the owner of the organization.
- The organization is on a trial subscription (active or expired).
- The organization does not already have a credit card or another marketplace subscription attached.
- The organization's deployments and projects are hosted on the same cloud provider as the marketplace. For example, an organization with deployments on {{aws}} can only be converted to an {{aws}} Marketplace subscription, not a {{gcp}} Marketplace subscription.

If none of your organizations are eligible, you can create a new organization through the marketplace sign-up flow, or [subscribe directly](/deploy-manage/cloud-organization/billing/add-billing-details.md) with a credit card.

## After conversion [ec-marketplace-post-conversion]

After your trial is converted:

- All existing deployments and projects in the converted organization are preserved.
- Billing starts through the marketplace immediately. There is no additional trial period.
- To monitor your usage and costs, go to **Billing > Usage** in the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
