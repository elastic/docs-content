---
navigation_title: Manage cases
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
description: Update cases with alerts, files, visualizations, and comments. Export and import cases between spaces.
---

# Manage cases [manage-cases]

After creating a case, you can update it with additional information, add supporting materials, and share it with others or external systems.

## Manage existing cases [manage-case]

From the **Cases** page, you can select multiple cases and use bulk actions to delete them or change their attributes.

To view a case, select its name. From the case details page, you can edit the description, add comments, update assignees, change status and severity, add connectors, and push updates to external systems. 

{applies_to}`stack: ga 9.2+` You can also paste images directly into comments using {kbd}`cmd+v` (Mac) or {kbd}`ctrl+v` (Windows/Linux). Pasted images are preformatted in Markdown. 

## Add context and supporting materials [add-case-context]

Provide additional context by adding [alerts](#add-case-alerts), [files](#add-case-files), [observables](#add-case-observables), and [Lens visualizations](#cases-lens-visualization) to your case. In {{elastic-sec}}, you can also add [events](/solutions/security/investigate/security-cases-features.md#cases-add-events), [indicators](/solutions/security/investigate/indicators-of-compromise.md#review-indicator-in-case), and more.

### Add alerts [add-case-alerts]

Escalate alerts and track them in a single place by attaching them to cases. To examine the alerts, select the **Alerts** tab in the case. In the table, alerts are organized from oldest to newest. To view alert details, select the **View details** button.

To find the **Alerts** tab:

- {applies_to}`stack: ga 9.3+`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga 9.0-9.2`: Go to the case's details page.  

You can add up to 1,000 alerts to a case.

### Add files [add-case-files]

After you create a case, you can upload and manage files on the **Files** tab. To find the tab:

- {applies_to}`stack: ga 9.3+`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga 9.0-9.2`: Go to the case's details page.

To download or delete the file or copy the file hash to your clipboard, open the action menu {icon}`boxes_horizontal`. The available hash functions are MD5, SHA-1, and SHA-256.

When you upload a file, a comment is added to the case activity log. To view an image, select its name in the activity or file list. Uploaded files are also accessible from the **Files** management page.

### Add observables [add-case-observables]

:::{note}
Observables are not available in {{observability}} for {{stack}} or {{serverless-short}}.
:::

Observables are discrete pieces of data relevant to an investigation, such as IP addresses, file hashes, domain names, or URLs. By attaching observables to cases, you can spot patterns across incidents or events. For example, if the same malicious IP appears in multiple cases, you may be dealing with a coordinated attack or shared threat infrastructure. This correlation helps you assess the true scope of an incident and prioritize your response.

From the **Observables** tab, you can view and manage case observables:

- {applies_to}`stack: ga 9.3+`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga 9.0-9.2`: Go to the case's details page.  

You can manually add observables to cases or with the appropriate subscription, auto-extract them from alerts. Each case supports up to 50 observables.

:::{note}
 Auto-extracting observables is only available for {{elastic-sec}} in {{sec-serverless}} and {{stack}} 9.2+.
:::

To manually add an observable:

1. Select **Add observable** from the **Observables** tab.
2. Provide the necessary details:

    * **Type**: Select a type for the observable. You can choose a preset type or a [custom one](/explore-analyze/cases/configure-case-settings.md#cases-observable-types).
    * **Value**: Enter a value for the observable. The value must align with the type you select.
    * **Description** (Optional): Provide additional information about the observable.

3. Select **Add observable**.

After adding an observable to a case, you can remove or edit it using the action menu {icon}`boxes_horizontal`. To find related investigations, check the **Similar cases** tab for other cases that share the same observables.

### Add Lens visualizations [cases-lens-visualization]

::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::

Add Lens visualizations to case descriptions or comments to portray event and alert data through charts and graphs. You can add them from dashboard panels or create visualizations directly in a case. To add a visualization from a dashboard, open a panel's menu, select the action menu {icon}`boxes_horizontal`, then **Add to existing case** or **Add to new case**.

To create a visualization in a case:

1. Click **Visualization** to open the visualization dialog.
2. Select an existing visualization from your Visualize Library or create a new one. Use an absolute time range so the visualization remains consistent over time.
3. (Optional) Click **Save to library** to save the visualization for reuse. Enter a title and description, then save.
4. Click **Save and return** to go back to your case.
5. Click **Preview** to see how the visualization will appear, then click **Add Comment** to attach it.

To modify a visualization after adding it, click **Open Visualization** in the case comment menu.

## Export cases [cases-export]

1. Find **Saved Objects** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Filter by type or search by case title to find the cases you want to export.
3. Select one or more cases, then click **Export**.
4. In the export dialog, keep **Include related objects** enabled to include connectors, then click **Export**.

Case data including user actions, text string comments, and Lens visualizations are exported to a newline-delimited JSON (`.ndjson`) file. Files and alerts that were attached to the case **won't** be exported. You must re-add them after importing the case.

## Import cases [cases-import]

::::{important}
Before importing Lens visualizations, Timelines, or alerts into a space, ensure their data is present. Without it, they won't work after being imported.
::::

1. Find **Saved Objects** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Import**.
2. Select the `.ndjson` file containing the exported cases.
3. Configure the import options and click **Import**.
4. Review the import log, then click **Done**.

If the imported case had connectors attached, you'll be prompted to re-authenticate them. Click **Go to connectors** and complete the required steps.