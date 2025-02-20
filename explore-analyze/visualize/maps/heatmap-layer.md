---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/heatmap-layer.html
---

# Heat map layer [heatmap-layer]

Heat map layers cluster point data to show locations with higher densities.

:::{image} ../../../images/kibana-heatmap_layer.png
:alt: heatmap layer
:class: screenshot
:::

To add a heat map layer to your map, click **Add layer**, then select **Heat map**. The index must contain at least one field mapped as [geo_point](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/geo-point.md) or [geo_shape](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/geo-shape.md).

::::{note}
Only count, sum, unique count metric aggregations are available with the grid aggregation source and heat map layers. Average, min, and max are turned off because the heat map will blend nearby values. Blending two average values would make the cluster more prominent, even though it just might literally mean that these nearby areas are average.
::::


