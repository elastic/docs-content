---
description: Delete a Kibana data view you no longer need, and understand what breaks when you do.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Delete a data view [delete-data-view]

When you delete a {{data-source}}, you cannot recover the associated field formatters, runtime fields, source filters, and field popularity data. Deleting a {{data-source}} does not remove any indices or data documents from {{es}}.

{applies_to}`stack: ga 9.4` You can't delete managed data views — refer to [Data views](../data-views.md#data-views-how-you-get-one) for what that means. On the **Data Views** management page, the delete action isn't available for these data views, and they can't be selected for bulk deletion. To use a modified version of a managed data view, [duplicate it](duplicate-data-view.md) instead.

::::{warning}
Deleting a {{data-source}} breaks all visualizations, saved Discover sessions, and other saved objects that reference the data view.
::::

## Before you begin [delete-data-view-prereqs]

You need the same privileges required to [create a data view](create-data-view.md#create-data-view-prereqs).

## Delete a data view [delete-data-view-steps]

1. Go to the **Data Views** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Find the {{data-source}} that you want to delete, and then select ![Delete icon](/explore-analyze/images/kibana-delete.png "") in the **Actions** column.

The {{data-source}} and its saved settings are removed from the **Data Views** page.

## Related pages

* [Data views](../data-views.md)
* [Duplicate a data view](duplicate-data-view.md)
