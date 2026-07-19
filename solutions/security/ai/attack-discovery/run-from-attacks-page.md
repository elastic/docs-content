---
navigation_title: Attacks page
description: "Schedule recurring Attack Discovery runs directly from the Attacks page."
applies_to:
  stack: preview 9.4
  serverless: preview
products:
  - id: security
  - id: cloud-serverless
---

# Run from the Attacks page [run-from-attacks-page]

The **Attacks** page pairs with the [**Attack Discovery**](/solutions/security/ai/attack-discovery/attack-discovery.md) page, which is where you manually generate new discoveries using large language models (LLMs):

- Go to **Attack Discovery** to run LLM analysis on demand and create new attack discoveries.
- Go to **Attacks** for day-to-day triage of all attacks (manual and scheduled), and to manage their investigation lifecycle.

This page describes how to run Attack Discovery directly from the **Attacks** page by scheduling recurring runs. The scheduling flow is the same as on the Attack Discovery page, and schedules you create on either page appear on both. To trigger a one-off, on-demand run instead, use the [Attack Discovery page](/solutions/security/ai/attack-discovery/run-from-attack-discovery-page.md). For guidance on which page to use for your version, refer to [Manage saved discoveries](/solutions/security/ai/attack-discovery/manage-saved-discoveries.md).

## Prerequisites [run-from-attacks-page-prerequisites]

The **Attacks** page requires the same privileges as Attack Discovery. Refer to [Role-based access control (RBAC) for Attack Discovery](/solutions/security/ai/attack-discovery/grant-access.md) for details.

:::{important}
To access the Attacks page, you must turn on the [**Enable alerts and attacks alignment**](/solutions/security/get-started/configure-advanced-settings.md#enable-alerts-and-attacks-alignment) setting under **Security Solution** in **Advanced Settings**.
:::

## Schedule runs [attacks-page-schedule-runs]

You can define recurring schedules (for example, daily or weekly) to automatically generate attack discoveries without needing manual runs. For example, you can generate discoveries every 24 hours and send a Slack notification to your SecOps channel if discoveries are found. Notifications are sent using configured [connectors](/deploy-manage/manage-connectors.md), such as Slack or email, and you can customize the notification content to tailor alert context to your needs.

To create a new schedule:

1. In the top-right corner, select **Schedule**.
2. In the **Attack discovery schedule** flyout, select **Create new schedule**.
3. Enter a name for the new schedule.
4. Select the LLM connector to use for generating discoveries, or add a new one.
5. Use the KQL query bar, time filter, and alerts slider to customize the set of alerts that will be analyzed.
6. Define the schedule's frequency (for example, every 24 hours).
7. Optionally, select the [connectors](/deploy-manage/manage-connectors.md) to use for receiving notifications, and define their actions.
8. Click **Create & enable schedule**.

After creating new schedules, you can view their status, modify them, or delete them from the **Attack discovery schedule** flyout. You can also act on multiple schedules at once:

1. In the schedule table, select the checkbox next to each schedule you want to act on.
2. Select **Bulk actions**, then choose one of the following:

    * **Enable** to enable the selected schedules.
    * **Disable** to disable the selected schedules.
    * **Delete** to delete the selected schedules. You'll be asked to confirm before the schedules are removed.

Bulk actions apply only to the schedules you've explicitly selected in the table.

To manage schedules programmatically, use the [Attack discovery API]({{kib-apis}}group/endpoint-security-attack-discovery-api), which includes endpoints for bulk-enabling, bulk-disabling, and bulk-deleting schedules.

:::{tip}
Scheduled discoveries are shown with a **Scheduled Attack discovery** icon ({icon}`calendar`). Click the icon to view the schedule that created it.
:::
