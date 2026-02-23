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
description: View and edit case details, export and import cases between spaces, and manage case attributes.
---

# Manage cases [manage-cases]

After creating a case, you can update it with additional information, add supporting materials, and share it with others or external systems.

## Manage existing cases [manage-case]

From the **Cases** page, you can select multiple cases and use bulk actions to delete them or change their attributes.

To view a case, select its name. From the case details page, you can edit the description, add comments, update assignees, change status and severity, add connectors, and push updates to external systems. 

{applies_to}`stack: ga 9.2+` You can also paste images directly into comments using {kbd}`cmd+v` (Mac) or {kbd}`ctrl+v` (Windows/Linux). Pasted images are preformatted in Markdown. 

To add context and supporting materials like alerts, files, observables, and visualizations, refer to [Attach objects to cases](attach-objects-to-cases.md).

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