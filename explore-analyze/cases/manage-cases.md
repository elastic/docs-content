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
description: Edit case details, perform bulk actions, and export or import cases between spaces or across stack upgrades.
---

# Manage cases [manage-cases]

Edit case details, perform bulk actions like deleting or updating multiple cases at once, and export or import cases between spaces or when upgrading to a new stack version.

## Edit case details [edit-case-details]

To view a case, go to the **Cases** page and select its name. From the case details page you can:

- Edit the description.
- Add or edit comments. 
- {applies_to}`stack: ga 9.2+` Paste images directly into comments using {kbd}`cmd+v` (Mac) or {kbd}`ctrl+v` (Windows/Linux). Pasted images are preformatted in Markdown.
- Update assignees, status, and severity.
- Add or change connectors and push updates to external systems.

To attach alerts, files, observables, or visualizations to a case, refer to [Attach objects to cases](attach-objects-to-cases.md).

## Bulk-manage cases [bulk-manage-cases]

From the **Cases** page, select one or more cases to perform bulk actions such as deleting cases or changing their status, severity, assignees, or tags.

## Export and import cases [export-import-cases]

Use export and import to move cases between {{kib}} spaces. Exports are saved as newline-delimited JSON (`.ndjson`) files and include user actions, text string comments, and Lens visualizations. 

Files and alerts attached to the case are **not** included; you must re-add them after importing. Before importing cases, also ensure that any referenced data (such as Lens visualizations, Timelines, or alerts) already exists in the destination space, otherwise those references won't work.

### Export cases [cases-export]

1. Find **Saved Objects** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Filter by type or search by case title to find the cases you want to export.
3. Select one or more cases, then click **Export**.
4. In the export dialog, keep **Include related objects** enabled to include connectors, then click **Export**.

### Import cases [cases-import]

1. Find **Saved Objects** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Import**.
2. Select the `.ndjson` file containing the exported cases.
3. Configure the import options and click **Import**.
4. Review the import log, then click **Done**.

If the imported case had connectors attached, you'll be prompted to re-authenticate them. Click **Go to connectors** and complete the required steps.