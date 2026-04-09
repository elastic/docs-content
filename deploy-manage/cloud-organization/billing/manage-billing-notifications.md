---
navigation_title: Manage budgets
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# Manage budgets and notifications [billing-notifications]

To help you understand costs and manage spending on {{ecloud}}, you can create budgets and configure email alerts when month-to-date usage for the budget's scope reaches the defined thresholds. When you create a budget, you can review how it compares to your usage over the past six months.

When configured, any email notifications are sent to users who are members of the Organization owner or Billing admin [user role](/deploy-manage/users-roles/cloud-organization/user-roles.md#ec_organization_level_roles). To set or change the addresses of these users, follow [Update billing and operational contacts](/deploy-manage/cloud-organization/billing/update-billing-operational-contacts.md).

To configure budgets and email notifications for your {{ecloud}} billing:

1. Log in to [{{ecloud}}](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the navigation menu, select **Billing**.
3. Follow the steps in [Configure budget emails](#configure-budget-emails) to set up the email notifications you'd like to receive.

Note that [Credit consumption emails](#configure-credit-consumption-emails) are also shown on the **Billing** page, but these notifications are not configurable.

## Configure budget emails [configure-budget-emails]

Budget alerts are sent when month-to-date usage for the budget's scope reaches the thresholds set for that budget. When you create or edit a budget, you choose one of two scopes:

* **Organization**: Usage for your entire {{ecloud}} organization is tracked against the budget target, including resources you create later.
* **Cloud resource**: Usage is tracked only for the cloud resources you select, such as {{ech}} deployments, {{serverless-short}} projects, or connected clusters. In the selector, resources are grouped by type (for example, **Cloud Hosted**, **{{serverless-short}}**, and **Cloud Connect**).

To create a budget:

1. Open the **Budgets and notifications** page.
1. Select **Add budget**.
1. In the **Scope** step, choose **Organization** or **Cloud resource**. If you choose **Cloud resource**, select every instance that should count towards the budget (you can select more than one).
1. In the **Configuration** step, specify your budget details:
    1. Give your budget a **Name**.
    1. Review the **Time range**: budgets are always **Monthly**, and usage resets on the first day of each calendar month.
    1. Enter a **Target amount (ECU)** in [Elastic Consumption Units](/deploy-manage/cloud-organization/billing/ecu.md). A cost trend chart shown next to the form summarizes historical usage for your chosen scope over the **last six months** so you can compare it to your target.
1. In the **Alerts** step, review the preset notification thresholds and recipients. These settings are currently fixed and cannot be edited.

   Alert emails are tied to the budget and use automatically defined thresholds:

   * A warning email is sent when usage for the selected scope reaches 75% of the specified target.
   * An overage email is sent when usage reaches 100% of the specified target.

   Notifications are sent to organization owners and billing admins.

1. Select **Create budget**.

New budgets are active by default, so notifications are on after you create them. To stop or resume emails for a budget, open **Budgets and notifications**, find the budget in the table, and choose **Deactivate** or **Activate** under **Actions**.

After creating a budget, you can return to **Budgets and notifications** to view or edit it, check **Current vs Budgeted (ECU)** for its scope, and expand cloud-resource budgets to review usage per instance in the subtable.

::::{note}
If you edit a budget scoped to cloud resources, resources that no longer exist are removed from the selectable list and shown in a callout.
::::

## Credit consumption emails [configure-credit-consumption-emails]

Credit consumption alerts are sent when your organization has used a certain percentage of [available credits](/deploy-manage/cloud-organization/billing/ecu.md#view-available-credits). These alerts are set automatically and can't be configured.

Alerts are triggered to be sent when your credit consumption reaches one of the set thresholds: 33%, 25%, and 16% of active credits remaining.
