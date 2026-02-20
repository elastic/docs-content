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
---

# Manage cases [manage-cases]

After creating a case, you can update it with additional information, add supporting materials, and share it with others or external systems.

## Manage existing cases [manage-case]

From the **Cases** page, you can select multiple cases and use bulk actions to delete them or change their attributes.

To view a case, select its name. From the case details page, you can edit the description, add comments, update assignees, change status and severity, add connectors, and push updates to external systems. 

{applies_to}`stack: ga 9.2+` You can also paste images directly into comments using {kbd}`cmd+c` (Mac) or {kbd}`ctrl+v` (Windows/Linux). Pasted images are preformatted in Markdown. 

## Add context and supporting materials [add-case-context]

Provide additional context by adding [alerts](#add-case-alerts), [files](#add-case-files), and [Lens visualizations](#cases-lens-visualization) to your case. In {{elastic-sec}}, you can also add [events](/solutions/security/investigate/security-cases-features.md#cases-add-events), [observables](/solutions/security/investigate/security-cases-features.md#add-case-observables), [indicators](/solutions/security/investigate/indicators-of-compromise.md#review-indicator-in-case), and more.

### Add alerts [add-case-alerts]

Escalate alerts and track them in a single place by attaching them to cases. To examine the alerts, select the **Alerts** tab in the case. In the table, alerts are organized from oldest to newest. To view alert details, select the **View details** button.

To find the **Alerts** tab:

- {applies_to}`stack: ga 9.3+`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga 9.0-9.2`: Go to the case's details page.  

You can add up to 1,000 alerts to a case.

### Add files [add-case-files]

After you create a case, you can upload and manage files on the **Files** tab. To find the tab:

- {applies_to}`stack: ga 9.3`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga 9.0-9.2`: Go to the case's details page.

To download or delete the file or copy the file hash to your clipboard, open the action menu {icon}`boxes_horizontal`. The available hash functions are MD5, SHA-1, and SHA-256.

When you upload a file, a comment is added to the case activity log. To view an image, select its name in the activity or file list. Uploaded files are also accessible from the **Files** management page.

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