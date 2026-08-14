---
description: Duplicate a Kibana data view to reuse its settings, or to get an editable copy of a managed data view.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Duplicate a data view [duplicate-data-view]

Duplicating a data view creates an editable copy. Use a copy when you want to try different field formatting or a different index pattern without affecting the original, or when you need a similar {{data-source}} for another use case.

{applies_to}`stack: ga 9.2` Duplicating is also how you customize a [managed](../data-views.md#managed-data-views) {{data-source}}. You can't edit a managed {{data-source}} directly.

## Before you begin [duplicate-data-view-prereqs]

You need the same privileges required to [create a data view](create-data-view.md#create-data-view-prereqs), and an existing data view to duplicate.

## Duplicate a data view [duplicate-data-view-steps]

1. Open **Discover** or **Lens**.

   :::{note}
   Duplication isn't available from the **Data Views** management page.
   :::

2. In the data view menu, select the data view that you want to duplicate.
3. Still in the data view menu, select **Manage this data view**. A flyout with more details about the data view opens. For a managed {{data-source}}, it indicates that you can't edit it directly.

   ![Manage this data view option](/explore-analyze/images/manage-this-data-view.png "Manage this data view option =50%")

4. Select **Duplicate**. A similar flyout opens where you can adjust the settings of the new copy.
5. Finish your edits, then select **Save data view to Kibana** or **Use without saving**.

If you save it to {{kib}}, the new, editable {{data-source}} appears in the data view menu and on the **Data Views** management page, separate from the one you duplicated.

## Related pages

* [Data views](../data-views.md)
* [Create a data view](create-data-view.md)
