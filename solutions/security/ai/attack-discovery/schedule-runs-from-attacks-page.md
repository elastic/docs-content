---
navigation_title: Scheduled runs
description: "Create and manage recurring Attack Discovery schedules from the Attacks view under Detections."
applies_to:
  stack: preview =9.4, ga 9.5+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Schedule runs from the Attacks view [schedule-runs-from-attacks-page]

Create a schedule so Attack Discovery runs automatically at intervals you choose. From the **Attacks** view, define how often analysis runs, which alerts to include, and optionally notify your team when discoveries are found. 

:::::{applies-switch}

::::{applies-item} { "stack": "ga 9.5+", "serverless": {"security": "ga"} }

:::{important}
After you turn on [Attack Discovery Workflows](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows), existing schedules keep their previous configuration until you edit and save them. Each scheduled run also opens a new {{agent-builder}} conversation you can view later from **Workflow execution details**.
:::

To create a schedule:

1. Go to **Detections > Views > Attacks**, then select **Schedule > Create new schedule**.
2. Name the schedule and choose an LLM connector for generation.
3. [Configure which alerts to analyze](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md). For example, keep skill retrieval on and add an {{esql}} query to focus on high-severity alerts.
4. Set how often the schedule runs, such as every 24 hours.
5. (Optional) Add notification [connectors](/deploy-manage/manage-connectors.md) and actions, then select **Create & enable schedule**. Supported notification connectors include Slack, {{sn}}, {{jira}}, PagerDuty, Cases, Email, and {{webhook}}.

::::

::::{applies-item} stack: preview =9.4

To create a schedule:

1. Go to **Detections > Views > Attacks**, then select **Schedule > Create new schedule**.
2. Name the schedule and choose an LLM connector for generation.
3. [Configure which alerts to analyze](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md#attacks-page-schedule-alert-selection).
4. Set how often the schedule runs, such as every 24 hours.
5. (Optional) Add notification [connectors](/deploy-manage/manage-connectors.md) and actions, then select **Create & enable schedule**. For example, send a Slack or email notification when discoveries are found.

::::

:::::

After creating a schedule, you can edit, enable, disable, or delete it. To change several at once, select them in the table and use **Bulk actions**. Schedule management requires the [**Schedules > Allow changes**](/solutions/security/ai/attack-discovery/grant-access.md#ad-schedules-privilege) privilege. To manage schedules programmatically, use the [Attack discovery API]({{kib-apis}}group/endpoint-security-attack-discovery-api).

Scheduled discoveries show a calendar icon. For how to recognize scheduled versus manually generated attacks, refer to [Recognize manually generated and scheduled attacks](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md#manually-generated-attacks).
