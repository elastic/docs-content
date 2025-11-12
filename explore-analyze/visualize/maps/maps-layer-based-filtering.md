---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps-layer-based-filtering.html
description: Apply filters to individual layers in Maps without affecting other layers. Create focused visualizations with layer-specific data filters and queries.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Filter a single layer [maps-layer-based-filtering]

You can apply a search request to individual layers by setting `Filters` in the layer details panel. Click the **Add filter** button to add a filter to a layer.

::::{note}
Layer filters are not applied to the right side of **term joins**. You can apply a search request to the right side of **term joins** by setting the **where** clause in the join definition. For example, suppose you have a layer with a term join where the left side is roads and the right side is traffic volume measurements. A layer filter of `roadType is "highway"` is applied to the roads index, but not to the traffic volume measurements index.
::::


:::{image} /explore-analyze/images/kibana-layer_search.png
:alt: layer search
:screenshot:
:::

