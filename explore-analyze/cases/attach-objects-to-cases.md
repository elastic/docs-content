---
navigation_title: Attach objects
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/manage-cases.html
  - https://www.elastic.co/guide/en/security/current/cases-open-manage.html
  - https://www.elastic.co/guide/en/observability/current/manage-cases.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-open-manage.html
  - https://www.elastic.co/guide/en/serverless/current/observability-create-a-new-case.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: cloud-serverless
description: Attach alerts, files, observables, and Lens visualizations to cases to provide context and supporting materials.
---

# Attach objects to cases [attach-objects-to-cases]

After [creating a case](create-cases.md), you can attach supporting materials to build a complete picture of an incident. Add [alerts](#add-case-alerts) to escalate and track detections, [files](#add-case-files) like screenshots or logs as evidence, [observables](#add-case-observables) such as IP addresses or file hashes to identify patterns, and [Lens visualizations](#cases-lens-visualization) to illustrate trends with charts and graphs. 

In {{elastic-sec}}, you can also attach [events](/solutions/security/investigate/security-cases.md#cases-add-events) and [threat intelligence indicators](/solutions/security/investigate/indicators-of-compromise.md#review-indicator-in-case) to connect cases to known threats.

## Supported object types [supported-object-types]

| Object | Description | Stack | Serverless |
| --- | --- | --- | --- |
| [Alerts](#add-case-alerts) | Attach alerts to escalate and track detections. | Security, Observability | Security, Observability |
| [Files](#add-case-files) | Upload screenshots, logs, or other supporting files. | Security, Observability, Stack Management | Security, Observability |
| [Observables](#add-case-observables) | Add IP addresses, file hashes, domains, or URLs to identify patterns. | Security, Stack Management | Security |
| [Lens visualizations](#cases-lens-visualization) | Embed charts and graphs to illustrate event and alert data. | Security, Observability, Stack Management | Security, Observability |
| [Events](/solutions/security/investigate/security-cases.md#cases-add-events) | Attach host, network, or user events from Timeline. | Security | Security |
| [Indicators](/solutions/security/investigate/indicators-of-compromise.md#attach-indicator-to-case) | Link threat intelligence indicators to document evidence of compromise. | Security | Security |
| [Timelines](/solutions/security/investigate/security-cases.md#cases-timeline) | Preserve investigation context by linking Timeline queries and filters. | Security | Security |

## Add alerts [add-case-alerts]

Escalate alerts and track them in a single place by attaching them to cases. 

To add alerts, select **More actions (…)** on a single alert or use the **Bulk actions** menu for multiple alerts, then choose **Add to a new case** or **Add to existing case**. You can add up to 1,000 alerts to a case.

After adding alerts, you can review them from the **Alerts** tab in the case. Alerts are organized from oldest to newest, and you can select **View details** to inspect individual alerts. To find the **Alerts** tab:

- {applies_to}`stack: ga 9.3+`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga 9.0-9.2`: Go to the case's details page.  

## Add files [add-case-files]

After you create a case, you can upload and manage files on the **Files** tab. To find the tab:

- {applies_to}`stack: ga 9.3+`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga 9.0-9.2`: Go to the case's details page.

To download or delete the file or copy the file hash to your clipboard, open the action menu {icon}`boxes_horizontal`. The available hash functions are MD5, SHA-1, and SHA-256.

When you upload a file, a comment is added to the case activity log. To view an image, select its name in the activity or file list. Uploaded files are also accessible from the **Files** management page.

## Add observables [add-case-observables]

Observables are discrete pieces of data relevant to an investigation, such as IP addresses, file hashes, domain names, or URLs. By attaching observables to cases, you can spot patterns across incidents or events. For example, if the same malicious IP appears in multiple cases, you may be dealing with a coordinated attack or shared threat infrastructure. This correlation helps you assess the true scope of an incident and prioritize your response.

From the **Observables** tab, you can view and manage case observables:

- {applies_to}`stack: ga 9.3+`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga 9.0-9.2`: Go to the case's details page.  

You can manually add observables to cases or with the appropriate subscription, auto-extract them from alerts. Each case supports up to 50 observables.

:::{note}
Auto-extracting observables is only available in {{sec-serverless}} and {{elastic-sec}} 9.2+.
:::

To manually add an observable:

1. Select **Add observable** from the **Observables** tab.
2. Provide the necessary details:

    * **Type**: Select a type for the observable. You can choose a preset type or a [custom one](/explore-analyze/cases/configure-case-settings.md#cases-observable-types).
    * **Value**: Enter a value for the observable. The value must align with the type you select.
    * **Description** (Optional): Provide additional information about the observable.

3. Select **Add observable**.

After adding an observable to a case, you can remove or edit it using the action menu {icon}`boxes_horizontal`. To find related investigations, check the **Similar cases** tab for other cases that share the same observables.

## Add Lens visualizations [cases-lens-visualization]

```{applies_to}
stack: beta
```

Add Lens visualizations to case descriptions or comments to portray event and alert data through charts and graphs. You can add them from dashboard panels or create visualizations directly in a case. To add a visualization from a dashboard, open a panel's menu, select the action menu {icon}`boxes_horizontal`, then **Add to existing case** or **Add to new case**.

To create a visualization in a case:

1. Click **Visualization** to open the visualization dialog.
2. Select an existing visualization from your Visualize Library or create a new one. Use an absolute time range so the visualization remains consistent over time.
3. (Optional) Click **Save to library** to save the visualization for reuse. Enter a title and description, then save.
4. Click **Save and return** to go back to your case.
5. Click **Preview** to see how the visualization will appear, then click **Add Comment** to attach it.

To modify a visualization after adding it, click **Open Visualization** in the case comment menu.
