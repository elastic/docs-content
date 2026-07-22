---
navigation_title: Scheduled runs
description: "Create and manage recurring Attack Discovery schedules from the Attacks view under Detections."
applies_to:
  stack: preview =9.4, ga 9.5+
  serverless: ga
products:
  - id: security
  - id: cloud-serverless
---

# Schedule runs from the Attacks view [schedule-runs-from-attacks-page]

Create a schedule so Attack Discovery runs automatically at intervals you choose. From the **Attacks** view, define how often analysis runs, which alerts to include, and optionally notify your team when discoveries are found. 

:::::{applies-switch}

::::{applies-item} { "stack": "ga 9.5+", "serverless": "ga" }

:::{important}
Turning on [**Attack Discovery Workflows**](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) does not update existing schedules. Open and save each schedule again while the setting is on, or create a new schedule. Later runs then use the workflow-backed path for alert retrieval, generation, and validation. Each time the Attack Discovery skill runs, {{agent-builder}} opens a new conversation.
:::

To create a schedule:

1. Go to **Detections > Views > Attacks**, then select **Schedule > Create new schedule**.
2. Name the schedule and choose an LLM connector for generation.
3. [Configure which alerts to analyze](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md). For example, keep skill retrieval on and add an {{esql}} query to focus on high-severity alerts.
4. Set how often the schedule runs, such as every 24 hours.
5. (Optional) Add notification [connectors](/deploy-manage/manage-connectors.md) and actions, then select **Create & enable schedule**. Supported notification connectors include Slack, {{sn}}, {{jira}}, PagerDuty, Cases, Email, and {{webhook}}.

For an existing schedule, open it from **Schedule**, update settings as needed, and save it again.

::::

::::{applies-item} stack: preview =9.4

To create a schedule:

1. Go to **Detections > Views > Attacks**.
2. In the top-right corner, select **Schedule**.
3. In the **Attack discovery schedule** flyout, select **Create new schedule**.
4. Enter a name for the schedule.
5. Select the LLM connector to use for generating discoveries, or add a new one.
6. [Configure which alerts to analyze](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md#attacks-page-schedule-alert-selection).
7. Define the schedule's frequency (for example, every 24 hours).
8. Optionally select notification [connectors](/deploy-manage/manage-connectors.md) and define their actions. For example, send a Slack or email notification when discoveries are found.
9. Select **Create & enable schedule**.

::::

:::::

From the schedule flyout, you can edit, enable, disable, or delete schedules. To change several at once, select them in the table and use **Bulk actions**. To manage schedules programmatically, use the [Attack discovery API]({{kib-apis}}group/endpoint-security-attack-discovery-api).

Scheduled discoveries show a calendar icon. For how to recognize scheduled versus manually generated attacks, refer to [Recognize manually generated and scheduled attacks](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md#manually-generated-attacks).

After discoveries appear from a schedule, [manage them from the Attacks view](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md). If a scheduled run fails, [troubleshoot it with AI](/solutions/security/ai/attack-discovery/troubleshoot-runs-from-attacks-page.md).
