---
navigation_title: Run from Attack Discovery page
description: "Manually run Attack Discovery or set up a recurring schedule from the Attack Discovery page."
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Run from the Attack Discovery page [run-from-attack-discovery-page]

Use this page when you are a SOC analyst working from the dedicated **Attack Discovery** experience. Configure which alerts get analyzed, manually run Attack Discovery, and set up a recurring schedule so it can run automatically.

::::{applies-switch}

:::{applies-item} { "stack": "ga 9.5+", "serverless": "ga" }

Prefer the **Attacks** view at **Detections > Views > Attacks** for manual runs, schedules, and triage next to related alerts. Refer to [Run from the Attacks view](/solutions/security/ai/attack-discovery/run-from-attacks-page.md). Continue with this page if you prefer the dedicated Attack Discovery experience.

:::

:::{applies-item} stack: preview =9.4

Use this page for manual runs. Create and manage schedules from here or from the **Attacks** page. For triage next to related alerts, refer to [Manage discoveries from the Attacks view](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md).

:::

::::

## Before you begin [run-from-attack-discovery-page-before-you-begin]

To use the **Attack Discovery** page, you need:

* `All` for **Attack discovery**, plus at least `Read` for {{rules-ui}} and **Alerts**. For the full privilege list, refer to [Grant access to Attack Discovery](/solutions/security/ai/attack-discovery/grant-access.md).
* {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` Optionally turn on the [**Attack Discovery Workflows**](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) advanced setting if you want workflow-backed runs and AI troubleshooting from this page.

## Set up Attack Discovery [set-up-attack-discovery]

By default, Attack Discovery analyzes up to 100 alerts from the last 24 hours, but you can customize how many and which alerts it analyzes using the settings menu. To open it, click the settings icon next to the **Run** button.

{applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` When the [**Attack Discovery Workflows**](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) advanced setting is turned on, the primary settings experience for skill, query, and workflow retrieval is the **Attack discovery settings** flyout on the [Attacks view](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md). This page keeps the classic settings menu described below.

:::{note}
:applies_to: stack: ga =9.0
In {{stack}} 9.0.x, the **Run** button is called **Generate**.
:::

::::{image} /solutions/images/security-attack-discovery-settings.png
:alt: Attack Discovery's settings menu
:screenshot:
:width: 60%
::::

You can select which alerts Attack Discovery processes by filtering based on a KQL query, the time and date selector, and the **Number of alerts** slider. Note that sending more alerts than your chosen LLM can handle may result in an error. Under **Alert summary** you can view a summary of the selected alerts grouped by various fields, and under **Alerts preview** you can view more details about the selected alerts.

:::{admonition} How to add non-ECS fields to Attack Discovery
Attack Discovery is designed for use with alerts based on data that complies with ECS, and by default only analyses ECS-compliant fields. However, you can enable Attack Discovery to review additional fields by following these steps:

1.  Select an alert with some of the non-ECS fields you want to analyze, and go to its details flyout. From here, use the **Ask AI Assistant** or **Add to chat** button to open an AI chat.
2.  At the bottom of the chat window, the alert's information appears. Click **Edit** to open the anonymization window to this alert's fields.
3.  Search for and select the non-ECS fields you want Attack Discovery to analyze. Set them to **Allowed**.
4.  Check the `Update presets` box to add the allowed fields to the space's default anonymization settings.

The next time you run Attack Discovery it will be able to analyze the selected fields.
:::

## Manually run Attack Discovery [attack-discovery-generate-discoveries]

Manually run Attack Discovery when you want to start analysis yourself, instead of waiting for a schedule. You’ll need to select an LLM connector before you can analyze alerts.

To get started:

1. Click the **Attack Discovery** page from {{elastic-sec}}'s navigation menu.
2. Do one of the following:
   - {applies_to}`stack: ga 9.1+` Click the settings icon next to the **Run** button, then in the settings menu, select an existing connector from the dropdown menu, or add a new one.
   - {applies_to}`stack: ga =9.0` Select an existing connector from the dropdown menu, or add a new one.

   :::{admonition} Recommended models
   While Attack Discovery is compatible with many different models, refer to the [Large language model performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md) to see which models perform best.

   :::

3. Once you’ve selected a connector, do one of the following to start the analysis:
   - {applies_to}`stack: ga 9.1+` Click **Save and run**.
   - {applies_to}`stack: ga =9.0` Click **Generate**.
   
It may take from a few seconds up to several minutes to generate discoveries, depending on the number of alerts and the model you selected. Once the analysis is complete, any threats it identifies will appear as discoveries. Click each one’s title to expand or collapse it. Click **Run** at any time to start the Attack Discovery process again with the selected alerts.

::::{important}
Attack Discovery uses the same data anonymization settings as [Elastic AI Assistant](/solutions/security/ai/ai-assistant.md). To configure which alert fields are sent to the LLM and which of those fields are obfuscated, use the Elastic AI Assistant settings. Consider the privacy policies of third-party LLMs before sending them sensitive data.
::::

## Schedule runs [schedule-discoveries]

```{applies_to}
stack: ga 9.1
serverless: ga
```

:::::{applies-switch}

::::{applies-item} { "stack": "ga 9.5+", "serverless": "ga" }

For the primary schedule experience, use [Schedule runs from the Attacks view](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md) at **Detections > Views > Attacks**. You can still create and manage schedules from this page if you prefer the dedicated Attack Discovery experience. You can generate discoveries manually at any time, regardless of an active schedule.

::::

::::{applies-item} stack: ga 9.1-9.4

{applies_to}`stack: preview =9.4` For schedules from the **Attacks** page, use the same steps as [Schedule runs from the Attacks view](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md). Schedules created on either page appear on both.

You can define recurring schedules (for example, daily or weekly) so Attack Discovery generates discoveries without manual runs. For example, run every 24 hours and send a Slack notification when discoveries are found. Notifications use configured [connectors](/deploy-manage/manage-connectors.md), such as Slack or email.

You can still generate discoveries manually at any time, regardless of an active schedule.

To create a schedule from this page:

1. In the top-right corner, select **Schedule**.
2. In the **Attack discovery schedule** flyout, select **Create new schedule**.
3. Enter a name for the schedule.
4. Select the LLM connector to use for generating discoveries, or add a new one.
5. Use the KQL query bar, time filter, and alerts slider to choose which alerts to analyze.
6. Define the schedule's frequency (for example, every 24 hours).
7. Optionally select notification [connectors](/deploy-manage/manage-connectors.md) and define their actions.
8. Select **Create & enable schedule**.

After you create schedules, you can view, edit, or delete them from the **Attack discovery schedule** flyout. Scheduled discoveries show a calendar icon. Select the icon to open the schedule that created the discovery.

::::

:::::

## Open workflow execution details [attack-discovery-page-troubleshoot]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

After a run finishes, the success or failure banner can show a details button if you have workflow-read privileges. The button opens the workflow execution details flyout.

From that flyout, a failed, canceled, or dismissed run (or any failed analysis step) offers a way to troubleshoot with AI. Refer to [Troubleshoot a run with AI](/solutions/security/ai/attack-discovery/troubleshoot-runs-from-attacks-page.md).
