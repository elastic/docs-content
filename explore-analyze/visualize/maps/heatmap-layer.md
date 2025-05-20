---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/heatmap-layer.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Heat map layer [heatmap-layer]

Heat map layers cluster point data to show locations with higher densities.

:::{image} /explore-analyze/images/kibana-heatmap_layer.png
:alt: heatmap layer
:screenshot:
:::

To add a heat map layer to your map, click **Add layer**, then select **Heat map**. The index must contain at least one field mapped as [geo_point](elasticsearch://reference/elasticsearch/mapping-reference/geo-point.md) or [geo_shape](elasticsearch://reference/elasticsearch/mapping-reference/geo-shape.md).

::::{note}
Only count, sum, unique count metric aggregations are available with the grid aggregation source and heat map layers. Average, min, and max are turned off because the heat map will blend nearby values. Blending two average values would make the cluster more prominent, even though it just might literally mean that these nearby areas are average.
::::


