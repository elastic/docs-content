---
applies_to:
  deployment:
    ess: all
  serverless: all
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# Manage usage and cost notifications [billing-notifications]

To help you better understand your costs and to manage spending, you can configure email alerts to be sent when your monthly usage or your credit consumption reaches a speicified threshold. You can also opt to receive a biweekly sumary of your organization's usage and estimated costs for the previous month.

To configure email notifications for your {{ecloud}} billing:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From a deployment or project on the home page, select **Manage**.
3. From the lower navigation menu, select **Billing and Subscription**.
4. Follow the steps bellow to set up or change any of the following types of email notifications.

## Configure budget emails

Budget alerts can be sent when your organization's total monthly usage exceeds a threshold defined in a configurable budget.

To create a budget and configure budget emails:

1. Open the **Notifications** page.
2. Select **Set budget** to specify your budget details:
    1. Give your budget a name.
    1. Specify a target value in [Elastic Consumption Units](/deploy-manage/cloud-organization/billing/ecu.md). The amount you've spent will be tracked against the this target.
    
    The budget scope is automatically fixed to your entire {{ecloud}} organization. Alert emails are configured automatically based on the configured budget:
     - A warning email is sent when the organization's usage reaches 75% of the specified target amount.
     - An overage email is sent when the organization's usage reaches 100% of the specified target amount.
     
     Email notifications are sent to the addresses associated with the Organization owner and Billing admin [user roles](/deploy-manage/users-roles/cloud-organization/user-roles.md#ec_organization_level_roles).

1. Click **Save** to confirm your settings.
1. Enable **Budget email**.

    You can navigate to the **Notifications** page at any time to view or update your budget, and to view the used versus total remaining ECU for your organization.

## Configure usage summmary emails

You can select to have a summary of your organization's usage sent on a biweekly basis. Notifications contain details about your organization's usage for the previous month as well as estimated costs.

To configure usage summary emails:

1. Open the **Notifications** page.
1. Enable **Usage summary email**.

    The notifications will be sent to the Organization owner and Billing admin on the second Friday of each month.


## Configure credit consumption emails

Credit consumption alerts can be sent when your organization has used a set percentage of [available credits](/deploy-manage/cloud-organization/billing/ecu.md#view-available-credits).

To configure credit consumption emails:

1. Open the **Notifications** page.
1. Enable **Credit consumption email**.

    Alerts are triggered to be sent when your credit consumption reaches any of the set thresholds: 33%, 25%, and 16% of active credits remaining. These thresholds are set automatically and cannot be configured.
