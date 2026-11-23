---
navigation_title: View field statistics
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/show-field-statistics.html
applies_to:
  stack: ga
  serverless: ga
type: how-to
products:
  - id: kibana
description: View a summary of every field in Discover, including the most common values, numeric ranges, and the number of documents that contain each field.
---

# View field statistics in Discover [show-field-statistics]

If you don't know yet what your data looks like, the **Field statistics** view in **Discover** shows each field's most common values, ranges, and how many documents contain it. That helps you spot data problems and decide what to chart before you build visualizations.

## Before you begin

- Make sure **Discover** is in classic mode. {{esql}} mode doesn't support this functionality. To switch, refer to [Switch to Discover's classic mode](switch-esql-mode.md#revert-to-classic-mode).
- **Discover** must have a [data view](../find-and-organize/data-views.md) selected and a time range that contains data.
- The **Field statistics** view is on by default. If it's missing from **Discover**, check whether the **Show field statistics** [advanced setting](kibana://reference/advanced-settings.md) is turned on.
- This example uses the [web logs sample data](/manage-data/ingest/sample-data.md). To follow along, add it, or use your own data.

## View the statistics of your fields

1. Go to **Discover**.
2. Expand the data view menu, and select **Kibana Sample Data Logs**.
3. If you don't see any results, expand the time range, for example, to **Last 7 days**.
4. Select **Field statistics** (or **View as** → **Field statistics**, depending on your version).
   The table summarizes, for each field, how many documents in the sample contain it for the selected time period, the number of distinct values, and the distribution.

   :::{image} /explore-analyze/images/kibana-field-statistics-view.png
   :alt: Field statistics view in Discover with the View as menu open.
   :screenshot:
   :::

5. Expand the `machine.ram` field.
   For numeric fields, **Discover** provides the document statistics, minimum, median, and maximum values, a list of top values, and a distribution chart. Use this chart to get a better idea of how the values in the data are clustered.

   :::{image} /explore-analyze/images/kibana-field-statistics-numeric.png
   :alt: Field statistics for the machine.ram numeric field.
   :screenshot:
   :::

6. Expand the `geo.coordinates` field.

   For geo fields, **Discover** provides the document statistics, examples, and a map of the coordinates.

   :::{image} /explore-analyze/images/kibana-field-statistics-geo.png
   :alt: Field statistics for a geo field.
   :screenshot:
   :::

7. Optional: Expand fields of other types, such as keyword or date fields, to see the statistics that **Discover** provides for them.
8. Optional: To explore the field data in Lens or Maps, select **Explore in Lens** ![the icon to create a visualization of the data in Lens](/explore-analyze/images/kibana-visualization-icon.png "") or **Explore in Maps** ![the Maps icon to explore the data in a map](/explore-analyze/images/kibana-map-icon.png "") in the **Actions** column. These actions appear only if your role gives you access to visualizations and to maps, and **Explore in Maps** is available for geo fields only.

**Result:** **Discover** shows a row of statistics for each field in your data view, and you can expand a field to see its values in detail.

## Next steps

- To check a single field's top values from the fields list, refer to [Explore fields in Discover](explore-fields.md).
- To chart a field, refer to [Visualize a field from Discover](visualize-field.md).

## Related pages

- [How to query in Discover's classic mode](use-classic-mode.md)

