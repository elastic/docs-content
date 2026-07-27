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

Browse the case list, edit case details, and perform bulk actions like deleting or updating multiple cases. You can also export and import cases between spaces or when upgrading to a new stack version.

## View and organize the case list [view-case-list]

```{applies_to}
stack: ga 9.5
```

The **Cases** page lists all the cases you can access. A summary at the top of the page shows counts for open, in-progress, and closed cases, along with the average time to close.

Use the view toggle to switch between two layouts:

- **List view** (default): Shows each case as a card with its ID, title, severity, status, alert count, assignees, author, last updated date, and comment count.
- **Table view**: Shows cases in rows and columns.

The following controls are shared across both views:

- **Sort**: In List view, order cases by newest or oldest first.
- **Fields** (List view) or **Columns** (Table view): Select which optional details to show. Options include tags, category, comments, alerts, events, dates, connector, external incident, description, and custom or template fields. You can also drag to reorder them.
- **Search and filters**: Narrow the list by text, status, severity, tags, categories, assignees, solution, or date range.

## Edit case details [edit-case-details]

To view a case, go to the **Cases** page and select its name. From the case details page you can:

- Edit the description.
- Add or edit comments. 
- {applies_to}`stack: ga 9.2+` Paste images directly into comments using {kbd}`cmd+v` (Mac) or {kbd}`ctrl+v` (Windows/Linux). Pasted images are preformatted in Markdown.
- Update assignees, status, and severity.
- Add or change connectors and push updates to external systems.
- {applies_to}`stack: ga 9.5` Edit the case title inline from the header.
- {applies_to}`stack: ga 9.5` [Send the case to an AI chat conversation](analyze-cases-with-ai.md) to summarize it or use it as context.

To attach alerts, files, observables, or visualizations to a case, refer to [Attach objects to cases](attach-objects-to-cases.md).

### Work with the case details view [case-details-view]

```{applies_to}
stack: ga 9.5
```

The case details page organizes information into editable sections:

- The **description** appears in its own panel that you can collapse or expand. An indicator shows when you have unsaved draft changes.
- A collapsible sidebar groups case attributes into sections you can edit in place, each with confirm and cancel controls:
  - **Attributes**: Assignees, severity, participants, tags, and category.
  - **Template fields**: Custom and template fields. When you apply a template, this section's title changes to the template's name (for example, **Compromised Account**).
  - **{{connectors-ui}}**: The external system the case is pushed to.

  Collapse the sidebar to give the main case content more room.

### Filter the activity feed [filter-case-activity]

```{applies_to}
stack: ga 9.5
```

The activity feed tracks a case's comments and history. To find specific entries, use the search box, filter by type (comments or history) or author, and sort by newest or oldest first. Select **Show more** to load additional entries, or clear the filters to return to the full feed.

## Apply a template to a case [apply-case-template]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

You can apply a different [case template](manage-case-templates.md) to an existing case. Open the case, select **Apply template** from the case actions menu, then choose an enabled template. Applying a template updates the case's fields. It doesn't change the case's existing connector.

## Bulk-manage cases [bulk-manage-cases]

From the **Cases** page, select one or more cases to perform bulk actions such as deleting cases or changing their status, severity, assignees, or tags.

## Export and import cases [export-import-cases]

Use export and import to move cases between {{kib}} spaces. Exports are saved as newline-delimited JSON (`.ndjson`) files and include user actions, text string comments, and any attached Lens visualizations, dashboards, maps, or Discover sessions that reference a saved object.

:::{note}
Files, alerts, and Timelines attached to the case are **not** included. You must re-add them after importing. 

Before importing cases, also ensure that any referenced saved objects (such as Lens visualizations, dashboards, maps, or Discover sessions) already exist in the destination space, otherwise those references won't work.
:::

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