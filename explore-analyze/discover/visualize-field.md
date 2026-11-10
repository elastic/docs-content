---
navigation_title: Visualize a field
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: Open a field from the Discover fields list in Lens to see how its values break down, then refine the chart and save it for a dashboard or the Visualize library.
---

# Visualize a field from Discover

When a field in the fields list looks interesting, you can open it in **Lens** to see how its values break down, without building a chart from scratch. **Lens** is the default visualization editor in {{kib}}.

## Before you begin

- Make sure **Discover** is in classic mode. {{esql}} mode doesn't support this functionality. To switch, refer to [Switch to Discover's classic mode](switch-esql-mode.md#revert-to-classic-mode).
- **Discover** must have a [data view](../find-and-organize/data-views.md) selected, and a search must have run on a time range that contains data, so the fields list appears.
- This example uses the [ecommerce sample data](/manage-data/ingest/sample-data.md). To follow along, add it and select its data view.

## Visualize a field

1. In the fields list in the sidebar, find a field that can be [aggregated](../query-filter/aggregations.md), for example `day_of_week` in the ecommerce sample data. Select the field name to open its details.

   :::{image} /explore-analyze/images/kibana-discover-day-of-week.png
   :alt: Top values for the day_of_week field in the sample ecommerce data
   :screenshot:
   :width: 60%
   :::

2. In the field details, select **Visualize**.

   {{kib}} creates a **Lens** visualization best suited for this field. For geo point fields (![Geo point field icon](/explore-analyze/images/kibana-geoip-icon.png "")), your data appears on a map instead.

   :::{image} /explore-analyze/images/kibana-discover-maps.png
   :alt: Map showing the documents of a geo point field
   :screenshot:
   :::

3. Optional: In **Lens**, from the **Available fields** list, drag more fields onto the chart to refine the visualization. In this example, adding the `manufacturer.keyword` field automatically adds a breakdown of the top values to the visualization.

   :::{image} /explore-analyze/images/kibana-discover-from-visualize.png
   :alt: Lens visualization of day_of_week with a breakdown by manufacturer.keyword
   :screenshot:
   :::

4. To keep the visualization, select **Save**. In the save dialog, you can add the visualization to a dashboard, save it to the Visualize library, or both.

**Result:** You have a visualization of the field that you can refine in **Lens**, add to a dashboard, or reopen from the Visualize library.

## Next steps

- To check a field's values before you chart it, refer to [Explore fields in Discover](explore-fields.md).

## Related pages

- [How to query in Discover's classic mode](use-classic-mode.md)
- [Lens visualizations](../visualize/lens.md)
