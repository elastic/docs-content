---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps-top-hits-aggregation.html
description: Display most recent or highest-ranked documents in Maps with top hits aggregation. Show latest GPS positions and track entity movements over time.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Display the most relevant documents per entity [maps-top-hits-aggregation]

Use **Top hits per entity** to display the most relevant documents per entity, for example, the most recent GPS tracks per flight route. To get this data, {{es}} first groups your data using a [terms aggregation](elasticsearch://reference/aggregations/search-aggregations-bucket-terms-aggregation.md), then accumulates the most relevant documents based on sort order for each entry using a [top hits metric aggregation](elasticsearch://reference/aggregations/search-aggregations-metrics-top-hits-aggregation.md).

To enable top hits:

1. Click **Add layer**, then select the **Top hits per entity** layer.
2. Configure **Data view** and **Geospatial field**.
3. Set **Entity** to the field that identifies entities in your documents. This field will be used in the terms aggregation to group your documents into entity buckets.
4. Set **Documents per entity** to configure the maximum number of documents accumulated per entity. This setting is limited to the `index.max_inner_result_window` index setting, which defaults to 100.

:::{image} /explore-analyze/images/kibana-top_hits.png
:alt: top hits
:screenshot:
:::

