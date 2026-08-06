---
description: Duplicate a Kibana data view to get a starting point for a similar one, or to work around a managed data view's read-only restrictions.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Duplicate a data view [duplicate-data-view]

Duplicating a data view gives you an editable copy to work from. This is useful whenever you want to reuse an existing {{data-source}} as a starting point, for example to try out different field formatting or a different index pattern without affecting the original, or to make a similar {{data-source}} for another use case.

{applies_to}`stack: ga 9.2` It's also the way to customize a **managed** {{data-source}}: managed {{data-sources}} can't be edited directly (refer to [Data views](../data-views.md#data-views-how-you-get-one)), so duplicating one is how you get an editable version.

## Before you begin [duplicate-data-view-prereqs]

You need the same privileges required to [create a data view](create-data-view.md#create-data-view-prereqs), and an existing data view to duplicate.

## Duplicate a data view [duplicate-data-view-steps]

1. Open the {{kib}} application where you want to use the data view, for example **Discover** or **Lens**.

   :::{note}
   Duplication isn't available from the **Data Views** management page.
   :::

2. In the data view selection menu, select the data view that you want to duplicate.
3. Still in the data view selection menu, select **Manage this data view**. A flyout with more details about the data view opens. For a managed {{data-source}}, it indicates that you can't edit it directly.

   ![Manage this data view option](/explore-analyze/images/manage-this-data-view.png "Manage this data view option =50%")

4. Select **Duplicate**. A similar flyout opens where you can adjust the settings of the new copy.
5. Finalize your edits, then select **Save data view to Kibana** or **Use without saving**, depending on your needs.

If you save it to {{kib}}, the new, editable {{data-source}} appears in the data view selection menu and on the **Data Views** management page, separate from the one you duplicated.

## Related pages

* [Data views](../data-views.md)
* [Create a data view](create-data-view.md)
