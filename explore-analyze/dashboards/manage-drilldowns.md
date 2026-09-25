---
navigation_title: Manage drilldowns
description: Edit, copy, delete, or reuse a drilldown on a dashboard panel.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: how-to
---

# Manage drilldowns [manage-drilldowns]

You can edit a drilldown, copy it, or delete it. You can also reuse a drilldown from another panel on the same dashboard.

For the dashboard, URL, and Discover types, refer to [Drilldowns](drilldowns.md).

## Before you begin [manage-drilldowns-requirements]

To manage a drilldown, you need:

:::{include} _snippets/drilldown-access.md
:::

The panel already has a drilldown. To reuse one, another panel on the same dashboard already has a drilldown this panel can run.

## Edit, copy, or delete a drilldown [edit-copy-or-delete-a-drilldown]

1. Open the panel menu that includes the drilldown, then select **Manage drilldowns**.
2. On the **Manage** tab, use the following options:

    * To change a drilldown, select **Edit**, make your changes, then select **Save**.
    * To make another copy on the same panel, select **Copy**, then select **Create drilldown**. The name ends with `(copy)`.
    * To delete a drilldown, select it, then select **Delete ({count})**.

## Reuse a drilldown on another panel [reuse-a-drilldown-on-another-panel]

To reuse a drilldown from another panel on the same dashboard, open {icon}`plus_in_circle` **Create drilldown** on the panel that should get it. When another panel already has a drilldown this panel can run, **Copy existing drilldown** lists it, with the source panel title under the drilldown name. Select **Copy**, then select **Create drilldown**. If this panel does not support the trigger, the name shows a warning.

## Related pages [manage-drilldowns-related-pages]

* [Drilldowns](drilldowns.md)
* [Create a dashboard drilldown](create-dashboard-drilldown.md)
* [Create a URL drilldown](create-url-drilldown.md)
* [Create a Discover drilldown](create-discover-drilldown.md)
