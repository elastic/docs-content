---
navigation_title: Manual runs
description: "Set up Attack Discovery's alert filtering and manually generate discoveries on demand from the Attack Discovery UI."
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Manual runs [manual-runs]

## Set up Attack Discovery

By default, Attack Discovery analyzes up to 100 alerts from the last 24 hours, but you can customize how many and which alerts it analyzes using the settings menu. To open it, click the settings icon next to the **Run** button.

:::{note}
:applies_to: stack: ga =9.0
In {{stack}} 9.0.0, the **Run** button is called **Generate**.
:::

::::{image} /solutions/images/security-attack-discovery-settings.png
:alt: Attack Discovery's settings menu
:screenshot:
:width: 60%
::::

You can select which alerts Attack Discovery processes by filtering based on a KQL query, the time and date selector, and the **Number of alerts** slider. Note that sending more alerts than your chosen LLM can handle may result in an error. Under **Alert summary** you can view a summary of the selected alerts grouped by various fields, and under **Alerts preview** you can view more details about the selected alerts.

<!-- 9.5 replaces this single-mode alert filtering with three additive retrieval toggles (skill-based retrieval, ES|QL/custom query, and user-authored alert-retrieval workflows) that each contribute to a merged candidate set, plus read-only visibility into the default retrieval/validation workflows and the attack-discovery-generator skill's enrichment behavior — per docs-content-internal#1448. This is the main focus of that issue (more control over which alerts are analyzed, and more insight into how). That update will be added in a separate PR once confirmed in the test environment — not included here. -->

:::{admonition} How to add non-ECS fields to Attack Discovery
Attack Discovery is designed for use with alerts based on data that complies with ECS, and by default only analyses ECS-compliant fields. However, you can enable Attack Discovery to review additional fields by following these steps:

1.  Select an alert with some of the non-ECS fields you want to analyze, and go to its details flyout. From here, use the **Ask AI Assistant** or **Add to chat** button to open an AI chat.
2.  At the bottom of the chat window, the alert's information appears. Click **Edit** to open the anonymization window to this alert's fields.
3.  Search for and select the non-ECS fields you want Attack Discovery to analyze. Set them to **Allowed**.
4.  Check the `Update presets` box to add the allowed fields to the space's default anonymization settings.

The next time you run Attack Discovery it will be able to analyze the selected fields.
:::

## Generate discoveries manually[attack-discovery-generate-discoveries]

You’ll need to select an LLM connector before you can analyze alerts. To get started:

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
