---
description: Delete a Kibana data view you no longer need. Deleting a data view does not delete Elasticsearch data, but it breaks saved objects that reference it.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Delete a data view

When you delete a {{data-source}}, you can't recover its field formatters, runtime fields, source filters, or field popularity data. Deleting a {{data-source}} doesn't remove any indices or data documents from {{es}}.

::::{warning}
Deleting a {{data-source}} breaks all visualizations, saved Discover sessions, and other saved objects that reference it.
::::

## Before you begin [delete-data-view-prereqs]

You need a role with the **Data View Management** {{kib}} privilege and the `view_index_metadata` {{es}} privilege. Refer to [Defining roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).

{applies_to}`stack: ga 9.4` You can't delete [managed data views](../data-views.md#managed-data-views). On the **Data Views** management page, the delete action isn't available for these data views, and they can't be selected for bulk deletion. To use a modified version of a managed data view, [duplicate it](duplicate-data-view.md) instead.

## Delete a data view [delete-data-view-steps]

1. Go to the **Data Views** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Find the {{data-source}} that you want to delete, then select ![Delete icon](/explore-analyze/images/kibana-delete.png "") in the **Actions** column.

The {{data-source}} and its saved settings are removed from the **Data Views** page.

## Related pages

* [Data views](../data-views.md)
* [Duplicate a data view](duplicate-data-view.md)
