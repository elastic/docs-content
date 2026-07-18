---
navigation_title: Scheduled runs
applies_to:
  stack: ga 9.1
  serverless: ga
products:
  - id: security
  - id: cloud-serverless
---

# Scheduled runs [schedule-discoveries]

:::{note}
{applies_to}`stack: preview 9.4` {applies_to}`serverless: preview` You can also create and manage schedules from the [Attacks page](/solutions/security/ai/attack-discovery/attacks-page.md). Schedules created on either page appear on both.
:::

You can define recurring schedules (for example, daily or weekly) to automatically generate attack discoveries without needing manual runs. For example, you can generate discoveries every 24 hours and send a Slack notification to your SecOps channel if discoveries are found. Notifications are sent using configured [connectors](/deploy-manage/manage-connectors.md), such as Slack or email, and you can customize the notification content to tailor alert context to your needs.

:::{note}
You can still generate discoveries manually at any time, regardless of an active schedule.
:::

:::::{applies-switch}

::::{applies-item} stack: ga 9.1-9.4

To create a new schedule:

1. In the top-right corner, select **Schedule**.
2. In the **Attack discovery schedule** flyout, select **Create new schedule**.
3. Enter a name for the new schedule.
4. Select the LLM connector to use for generating discoveries, or add a new one.
5. Use the KQL query bar, time filter, and alerts slider to customize the set of alerts that will be analyzed.
6. Define the schedule's frequency (for example, every 24 hours).
7. Optionally, select the [connectors](/deploy-manage/manage-connectors.md) to use for receiving notifications, and define their actions.
8. Click **Create & enable schedule**.

After creating new schedules, you can view their status, modify them or delete them from the **Attack discovery schedule** flyout.

:::{tip}
Scheduled discoveries are shown with a **Scheduled Attack discovery** icon ({icon}`calendar`). Click the icon to view the schedule that created it.
:::

::::

::::{applies-item} { "stack": "ga 9.5+", "serverless": "ga" }

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

::::

:::::

<!-- Per item 4 of docs-content-internal#1448, scheduled runs become an "always-on agent" in 9.5, every N-hour run is inspected by the attack-discovery-generator skill (ground-truthing retrieval, cross-skill corroboration, detection-gap closure), and discoveries land in the UI with notifications routed to any existing Alerting Framework connector (Slack, ServiceNow, Jira, PagerDuty, Cases, Email, Webhook). This page is also the linked "Scheduled runs" entry in the run-attack-discovery.md overview. Content deferred to a separate PR, not included here. -->
