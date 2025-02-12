---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/show-field-statistics.html
---

# View field statistics [show-field-statistics]

Explore the fields in your data with the **Field statistics** view in **Discover** and answer such questions as:

* What does the latency look like when one of the containers is down on a Sunday?
* Is the field type and format in the data view appropriate for the data and its cardinality?

This example explores the fields in the [sample web logs data](../index.md#gs-get-data-into-kibana), or you can use your own data.

1. Go to **Discover**.
2. Expand the {{data-source}} dropdown, and select **Kibana Sample Data Logs**.
3. If you don’t see any results, expand the time range, for example, to **Last 7 days**.
4. Click **Field statistics**.
   The table summarizes how many documents in the sample contain each field for the selected time period the number of distinct values, and the distribution.

   :::{image} ../../images/kibana-field-statistics-view.png
   :alt: Field statistics view in Discover showing a summary of document data.
   :class: screenshot
   :::

5. Expand the `hour_of_day` field.
   For numeric fields, **Discover** provides the document statistics, minimum, median, and maximum values, a list of top values, and a distribution chart. Use this chart to get a better idea of how the values in the data are clustered.

   :::{image} ../../images/kibana-field-statistics-numeric.png
   :alt: Field statistics for a numeric field.
   :class: screenshot
   :::

6. Expand the `geo.coordinates` field.

   For geo fields, **Discover** provides the document statistics, examples, and a map of the coordinates.

   :::{image} ../../images/kibana-field-statistics-geo.png
   :alt: Field statistics for a geo field.
   :class: screenshot
   :::

7. Explore additional field types to see the statistics that **Discover** provides.
8. To create a visualization of the field data, click ![Click the magnifying glass icon to create a visualization of the data in Lens](../../images/kibana-visualization-icon.png "") or ![Click the Maps icon to explore the data in a map](../../images/kibana-map-icon.png "") in the **Actions** column.

