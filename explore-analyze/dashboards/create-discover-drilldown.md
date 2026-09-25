---
navigation_title: Create a Discover drilldown
description: Create a drilldown that opens Discover from a visualization panel for the documents behind the value you select.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: how-to
---

# Create a Discover drilldown [discover-drilldowns]

A Discover drilldown opens **Discover** from a visualization panel and can carry the time range, filters, and query with it. Use one to read the documents behind a chart value.

For example, a Discover drilldown on a pie chart can open only the documents for the slice you select.

Refer to [Drilldowns](drilldowns.md) to choose a drilldown type and to check values created at query time.

## Before you begin [create-discover-drilldown-requirements]

To create a Discover drilldown, you need:

:::{include} _snippets/drilldown-access.md
:::

The drilldown opens **Discover** from the panel itself.

The following panel types support Discover drilldowns:

* **Visualizations that use a data view**
* {applies_to}`serverless:` {applies_to}`stack: ga 9.5` **Visualizations based on an {{esql}} query**

    On {{esql}} panels, {{kib}} turns the dashboard filters and the dashboard KQL or Lucene query into a `WHERE` clause in the panel's ES|QL query. **Discover** then uses that same context. {{kib}} drops a filter when ES|QL cannot express it. The **Explore in Discover** panel action applies the same translation.

    On an {{esql}} **Bar**, **Line**, **Area**, or **Heat map**, drag to select a range. That range opens the drilldown. A click updates the {{esql}} query.

On a visualization that uses a data view, select the value.

::::{tip}
You can [open a visualization panel in Discover](../visualize/manage-panels.md#explore-the-underlying-documents) without setting up a drilldown.
::::

For a computed value, including an {{esql}} result, refer to [How a drilldown uses the selected value](drilldowns.md#drilldowns-requirements).

## Create the drilldown [_create_the_discover_drilldown]

This example creates a Discover drilldown on the **[Logs] Bytes distribution** panel. Follow it with the sample data, or use your own dashboard and data.

1. Add the [**Sample web logs**](/manage-data/ingest/sample-data.md) data. This also adds the **[Logs] Web Traffic** dashboard.
2. Open that dashboard and select **Edit**.
3. Hover over the **[Logs] Bytes distribution** panel, open the {icon}`boxes_vertical` panel menu, then select {icon}`plus_in_circle` **Create drilldown**.
4. Select **Open in Discover**. In **Name**, enter `View bytes distribution in Discover`. **Open in new tab** is already on. Select **Create drilldown**.
5. Save the dashboard.
6. Drag across the bars to select a range of `bytes` values, then select **View bytes distribution in Discover**.

   :::{image} /explore-analyze/images/kibana-dashboard_discoverDrilldown.png
   :alt: Drilldown on bar vertical stacked chart that navigates to Discover
   :screenshot:
   :::

**Discover** opens in a new tab and shows the documents for the `bytes` range you selected. The dashboard time range, filters, and query stay in place.

## Next steps [create-discover-drilldown-next-steps]

* [Manage drilldowns](manage-drilldowns.md)

## Related pages [create-discover-drilldown-related-pages]

* [Drilldowns](drilldowns.md)
* [Add drilldowns to an {{esql}} visualization](../visualize/esorql.md#esql-viz-drilldowns)
