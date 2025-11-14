---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/show-field-statistics.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Examine field distributions and value ranges with Discover's Field statistics view. Identify data quality issues, understand cardinality, and create visualizations from field data.
---

# View field statistics in Discover [show-field-statistics]

Field statistics view in Discover shows distribution patterns, cardinality, and value ranges for fields in your data. Use this view to assess data quality, understand field usage, identify outliers, and create quick visualizations from field distributions. Statistics vary by field type. Numeric fields show ranges and distributions, while geo fields display coordinate maps.

Field statistics help you answer questions like:
* What's the distribution of values across a field?
* Are there unexpected patterns or outliers in the data?
* Is the field format appropriate for its cardinality?
* What does latency look like when one of the containers is down on a specific day?

**Prerequisites:**

* You need a {{data-source}} with data to explore
* Field statistics aren't available when Discover is in {{esql}} mode
* This example uses [sample web logs data](../index.md#gs-get-data-into-kibana), or you can use your own data

1. Go to **Discover**.
2. Expand the {{data-source}} dropdown, and select **{{kib}} Sample Data Logs**.
3. If you don't see any results, expand the time range, for example, to **Last 7 days**.
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

