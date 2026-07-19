---
navigation_title: Configure settings
description: "Customize which alerts Attack Discovery analyzes, and enable analysis of non-ECS fields, using the settings menu."
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Configure Attack Discovery settings [configure-attack-discovery-settings]

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
