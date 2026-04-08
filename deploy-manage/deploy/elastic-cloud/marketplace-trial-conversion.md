---
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# Convert a trial to a marketplace subscription [ec-marketplace-trial-conversion]

If you started with an {{ecloud}} trial and want to pay through a cloud marketplace instead of adding a credit card directly, you can convert your trial to a marketplace subscription. Your existing deployments, projects, and data are preserved during the conversion.

## Before you begin

- You must have an active {{ecloud}} trial. If your trial has expired, you have 30 days to subscribe before your data is permanently deleted.
- You need access to one of the supported marketplaces: [{{aws}} Marketplace](aws-marketplace.md), [Azure Marketplace](azure-native-isv-service.md), or [{{gcp}} Marketplace](google-cloud-platform-marketplace.md).
- The email address associated with your {{ecloud}} trial must match the credentials you use during the marketplace sign-up process.

## Convert your trial [ec-marketplace-trial-conversion-steps]

% TODO: confirm exact UI labels per marketplace from Figma designs

::::::{stepper}
:::::{step} Create your {{ecloud}} trial
If you haven't already, [sign up](create-an-organization.md) for an {{ecloud}} trial using the email address you prefer. This is the email address that will be associated with your marketplace subscription.
:::::
:::::{step} Subscribe through your marketplace
Log into your cloud provider's marketplace and find the {{ecloud}} offering. Select **Sign up** (or the equivalent action for your marketplace).

::::{tab-set}
:::{tab-item} {{aws}} Marketplace
Go to the [{{ecloud}} listing on the {{aws}} Marketplace](https://aws.amazon.com/marketplace/pp/prodview-voru33wi6xs7k) and click **View purchase options**, then **Subscribe** and **Set Up Your Account**.
:::
:::{tab-item} Azure Marketplace
Go to the [{{ecloud}} ({{es}}) - An Azure Native ISV Service](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/elastic.ec-azure-pp) listing in the Azure portal. Select **Subscribe** and follow the prompts to create an Elastic resource.
:::
:::{tab-item} {{gcp}} Marketplace
Go to the [{{ecloud}} listing on the {{gcp}} Marketplace](https://console.cloud.google.com/marketplace/product/elastic-prod/elastic-cloud). Select **Subscribe**, accept the terms, and choose **Sign up with Elastic**.
:::
::::
:::::
:::::{step} Sign in with your existing credentials
When prompted to create a new account or sign in, choose to **sign in** with the {{ecloud}} credentials from your existing trial.
:::::
:::::{step} Select the organization to convert
What happens next depends on how many organizations your account belongs to:

- **Single organization:** Your trial organization is automatically converted to the marketplace subscription. Billing through the marketplace begins immediately.
- **Multiple organizations:** You are prompted to select which organization you want to convert to the marketplace subscription. Only eligible organizations are shown.

% TODO: confirm auto-convert behavior for single org and add detail on the selection UI from Figma
:::::
::::::

## Which organizations can be converted [ec-marketplace-conversion-candidates]

% TODO: confirm full eligibility criteria with PM/engineering

Not all organizations are eligible for marketplace conversion. An organization can be converted if it meets the following conditions:

- The organization is on a **trial** subscription (not already linked to another billing source).
- The organization does not already have a credit card or another marketplace subscription attached.

If you belong to multiple organizations and none are eligible for conversion, you may need to create a new organization through the marketplace sign-up flow instead.

## After conversion [ec-marketplace-post-conversion]

After your trial is converted:

- All existing deployments and projects in the converted organization are preserved.
- Billing starts through the marketplace immediately. There is no additional trial period.
- Your subscription level may change depending on the marketplace. Check your marketplace-specific page for details: [{{aws}}](aws-marketplace.md), [Azure](azure-native-isv-service.md), [{{gcp}}](google-cloud-platform-marketplace.md).
- To monitor your usage and costs, go to **Billing > Usage** in the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
