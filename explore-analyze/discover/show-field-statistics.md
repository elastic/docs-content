---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/show-field-statistics.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Explore field statistics in Discover to view distributions, top values, and data quality metrics. Analyze numeric ranges, geographic coordinates, and field cardinality.
---

# View field statistics [show-field-statistics]

The **Field statistics** view in **Discover** provides statistical summaries and visualizations of your data fields. View distributions, top values, minimum and maximum ranges, and cardinality to quickly understand your data quality and patterns. Use field statistics to identify data issues, understand field characteristics, and discover insights before building visualizations.

:::{note}
Field statistics are only available when **Discover** is in default mode, not in {{esql}} mode.
:::

This example explores the fields in the [sample web logs data](../index.md#gs-get-data-into-kibana), or you can use your own data.

1. Go to **Discover**.
2. Expand the {{data-source}} dropdown, and select **Kibana Sample Data Logs**.
3. If you don’t see any results, expand the time range, for example, to **Last 7 days**.
4. Click **Field statistics**.
   The table summarizes how many documents in the sample contain each field for the selected time period the number of distinct values, and the distribution.

   :::{image} /explore-analyze/images/kibana-field-statistics-view.png
   :alt: Field statistics view in Discover showing a summary of document data.
   :screenshot:
   :::

5. Expand the `hour_of_day` field.
   For numeric fields, **Discover** provides the document statistics, minimum, median, and maximum values, a list of top values, and a distribution chart. Use this chart to get a better idea of how the values in the data are clustered.

   :::{image} /explore-analyze/images/kibana-field-statistics-numeric.png
   :alt: Field statistics for a numeric field.
   :screenshot:
   :::

6. Expand the `geo.coordinates` field.

   For geo fields, **Discover** provides the document statistics, examples, and a map of the coordinates.

   :::{image} /explore-analyze/images/kibana-field-statistics-geo.png
   :alt: Field statistics for a geo field.
   :screenshot:
   :::

7. Explore additional field types to see the statistics that **Discover** provides.
8. To create a Lens visualization of the field data, click ![the magnifying glass icon to create a visualization of the data in Lens](/explore-analyze/images/kibana-visualization-icon.png "") or ![the Maps icon to explore the data in a map](/explore-analyze/images/kibana-map-icon.png "") in the **Actions** column.

