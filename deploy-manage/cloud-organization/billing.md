---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-billing.html
  - https://www.elastic.co/guide/en/serverless/current/general-manage-billing.html
  - https://www.elastic.co/guide/en/serverless/current/general-billing-stop-project.html
applies_to:
  deployment:
    ess: all
  serverless: all
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# Billing

Elastic charges a recurring fee for using our offerings on {{ecloud}}. In this section, you'll learn about the dimensions used to calculate your bill, how to monitor account usage, how to manage billing, and more.

## Pricing model

{{ecloud}} pricing and billing is based on your usage across a number of dimensions. These dimensions are different for {{ech}} deployments and {{serverless-full}} projects. Each {{serverless-full}} project type also has its own billing dimensions.

* [](/deploy-manage/cloud-organization/billing/cloud-hosted-deployment-billing-dimensions.md)
* [](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md)
  * [](/deploy-manage/cloud-organization/billing/elasticsearch-billing-dimensions.md)
  * [](/deploy-manage/cloud-organization/billing/elastic-observability-billing-dimensions.md)
  * [](/deploy-manage/cloud-organization/billing/security-billing-dimensions.md)

For more information, you can also refer to our [{{ech}}](https://www.elastic.co/pricing) and [{{serverless-full}}](https://www.elastic.co/pricing/serverless-search) pricing pages.

## Billing models

Depending on your organization's needs, you can use one of several billing models. These models impact who bills you for your usage, and how often you're billed.

[Learn more](/deploy-manage/cloud-organization/billing/billing-models.md).

## Manage your subscription and billing in {{ecloud}}

You can explore and manage billing, as well as your {{ecloud}} subscription, from the **Billing** section of the {{ecloud}} Console.

* [Add your billing details](/deploy-manage/cloud-organization/billing/add-billing-details.md)
* [View your billing history](/deploy-manage/cloud-organization/billing/view-billing-history.md)
* [Manage your notifications](/deploy-manage/cloud-organization/billing/manage-billing-notifications.md)
* [Manage your subscription](/deploy-manage/cloud-organization/billing/manage-subscription.md)
* [Monitor and analyze your account usage](/deploy-manage/cloud-organization/billing/monitor-analyze-usage.md)

You might also want to [update the contacts that receive billing emails](/deploy-manage/cloud-organization/billing/update-billing-operational-contacts.md)

For any other questions that you have about billing, refer to our [billing FAQ](/deploy-manage/cloud-organization/billing/billing-faq.md).

## Stop charges for a deployment or project

To stop charges for an {{ecloud}} deployment or project, you need to [delete it](/deploy-manage/uninstall/delete-a-cloud-deployment.md).

When a deployment or project is deleted, all data is lost. Billing for usage is by the hour and any outstanding charges for usage before you deleted the deployment or project will still appear on your next bill.
