---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-account-usage.html
  - https://www.elastic.co/guide/en/serverless/current/general-monitor-usage.html
applies_to:
  deployment:
    ess: all
  serverless: all
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# Monitor and analyze usage

Information about your current {{ecloud}} subscription usage is available directly from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) and includes:

* Monitor usage for the current month, including month-to-date usage
* For customers with annual prepaid credits, the total value of credits to be applied in the current billing cycle
* Check the usage breakdown for a selected time range
* View usage totals by product

You can check the detailed usage for a selected time range grouped either by product or by resource, such as an {{ech}} deployment or a {{serverless-full}} project.

What you can see on the **Usage** page depends on your {{ecloud}} roles:

* Users with the **Organization owner** or **Billing admin** role can view usage and costs for the entire organization.
* Users with a cloud resource access role or a connected cluster access role can view usage and costs for the {{ech}} deployments, {{serverless-short}} projects, and connected clusters they have access to.

For any resource you have access to, you can view its full available cost history, including costs from before you were granted access.

To access your account usage:

1. Log in to [{{ecloud}}](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the navigation menu, select **Billing > Usage**.

::::{important}
The usage breakdown information visible on the **Usage** page is an estimate, and does not include prepaid credits, free allowances or any discounts. If you're an **Organization owner** or **Billing admin**, check your invoices in the [billing history](/deploy-manage/cloud-organization/billing/view-billing-history.md) to find the exact amount you owe for a given month.
::::

:::{note}
Organization-wide financial details — such as your credit balance, [billing history](/deploy-manage/cloud-organization/billing/view-billing-history.md), and invoices — remain available only to users with the **Organization owner** or **Billing admin** role.
:::