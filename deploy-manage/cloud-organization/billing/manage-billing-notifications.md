---
navigation_title: Manage budgets and notifications
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# Manage budgets and notifications [billing-notifications]

To help you understand costs and manage spending on {{ecloud}}, you can create budgets that track resource usage and send email notifications when month-to-date usage reaches specified thresholds. Budgets can be scoped to specific {{ecloud}} resources or to your entire organization.

You can associate each budget with specific [user roles](/deploy-manage/users-roles/cloud-organization/user-roles.md) in your organization. Users with those roles receive email notifications when budget alerts are triggered. You select the roles as part of the budget creation workflow described in the following section.

::::{note}
[Credit consumption email notifications](#configure-credit-consumption-emails) are separate from budget notifications and apply to organizations using prepaid credits. They are triggered automatically based on remaining credit balance and cannot be configured.
::::

## Configure billing budgets [configure-budget-emails]

To create a budget:

1. Log in to [{{ecloud}}](https://cloud.elastic.co?page=docs&placement=docs-body) and go to **Billing** > **Budgets and notifications**.
1. Select **Add budget**.
1. In the **Scope** step, choose how the budget is applied:
    * **Organization**: Tracks usage for your entire {{ecloud}} organization, including resources you create later.
    * **Cloud resource**: Tracks usage only for the selected resources, such as {{ech}} deployments, {{serverless-short}} projects, or connected clusters. In the selector, resources are grouped by type (for example, **Cloud Hosted**, **{{serverless-short}}**, and **Cloud Connect**), and you can select more than one.
1. In the **Configuration** step, specify your budget details:
    1. Give your budget a **Name**.
    1. Review the **Time range**: budgets are always **Monthly**, and usage resets on the first day of each calendar month.
    1. Enter a **Target amount (ECU)** in [Elastic Consumption Units](/deploy-manage/cloud-organization/billing/ecu.md). A cost trend chart shown next to the form summarizes historical usage for your chosen scope over the **last six months** so you can compare it to your target.
1. In the **Alerts** step, configure when and who to notify:

    **Notification thresholds**

    Alert emails use fixed thresholds:

    * A warning email is sent when usage for the selected scope reaches **75%** of the specified target.
    * An overage email is sent when usage reaches **100%** of the specified target.

    **Recipients**

    Select which user roles should receive alert notifications. You must choose at least one option:

    * **Elastic Cloud organization**: **Organization owner** and/or **Billing admin**.
    * **Cloud resource permissions** (only for cloud-resource budgets): Users with **Admin**, **Editor**, or **Viewer** roles on the selected resources. If the budget includes multiple resources, users must have the selected roles on all of them to receive notifications.

1. Select **Create budget**.

New budgets are active by default, so notifications are on after you create them. To stop or resume emails for a budget, open **Budgets and notifications**, find the budget in the table, and choose **Deactivate** or **Activate** under **Actions**.

After creating a budget, you can return to **Budgets and notifications** to view or edit it, check **Current vs Budgeted (ECU)** for its scope, and expand cloud-resource budgets to review usage per resource in the subtable.

::::{note}
If you edit a budget scoped to cloud resources, resources that no longer exist are removed from the selectable list and shown in a callout.
::::

## Credit consumption emails [configure-credit-consumption-emails]

Credit consumption alerts are sent when your organization has used a certain percentage of [available credits](/deploy-manage/cloud-organization/billing/ecu.md#view-available-credits). These alerts are set automatically and can't be configured.

Alerts are triggered to be sent when your credit consumption reaches one of the set thresholds: 33%, 25%, 16%, and 0% of active credits remaining.
