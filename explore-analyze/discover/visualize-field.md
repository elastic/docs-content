---
navigation_title: Visualize a field
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: Turn a field from the Discover fields list into a Lens visualization in one step, refine it, and save it for a dashboard or the Visualize library.
---

# Visualize a field from Discover

When a field in the Discover fields list looks interesting, you can open it in **Lens** to see how its values break down, without building a chart from scratch. **Lens** is the default visualization editor in {{kib}}.

## Before you begin

- Open **Discover** in classic mode and select a data view. If **Discover** opens in {{esql}} mode, refer to [Switch to Discover's classic mode](switch-esql-mode.md#revert-to-classic-mode).
- Pick a field that can be [aggregated](../query-filter/aggregations.md).

## Visualize a field

1. In the list of fields, find an aggregatable field. For example, with the sample data, you can look for `day_of_week`.

   ![Top values for the day_of_week field](/explore-analyze/images/kibana-discover-day-of-week.png "title =60%")

2. In the popup, select **Visualize**.

   {{kib}} creates a **Lens** visualization best suited for this field. For geo point fields (![Geo point field icon](/explore-analyze/images/kibana-geoip-icon.png "kibana-geoip-icon =4%x4%")), your data appears on a map instead.

   ![Map containing documents](/explore-analyze/images/kibana-discover-maps.png "")

3. Optional: In **Lens**, from the **Available fields** list, drag more fields onto the workspace to refine the visualization. In this example, adding the `manufacturer.keyword` field automatically adds a breakdown of the top values to the visualization.

   ![Visualization that opens from Discover based on your data](/explore-analyze/images/kibana-discover-from-visualize.png "")

4. To add the visualization to a dashboard or keep it in the Visualize library for later use, save it.

**Result:** You have a visualization of the field that you can refine in **Lens**, add to a dashboard, or reopen from the Visualize library.

## Related pages

- [Use Discover in classic mode](use-classic-mode.md)
- [Lens](../visualize/lens.md)
