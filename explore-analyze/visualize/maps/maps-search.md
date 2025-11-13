---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps-search.html
description: Search and filter map data with queries and time ranges. Control data visibility across layers using global or layer-specific search parameters.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Search geographic data [maps-search]

Global search and time filters in Maps narrow data across all {{es}}-backed layers simultaneously. You can use KQL queries for field-based searches, combine multiple filters, and set time ranges to focus on specific data subsets.

This guide covers global search behavior, layer-specific search options, and strategies for controlling which layers respond to search criteria.

This image shows an example of global search and global time narrowing results.

:::{image} /explore-analyze/images/kibana-global_search_bar.png
:alt: global search and global time narrowing results
:screenshot:
:::

Only layers requesting data from {{es}} are narrowed by global search and global time. To add a layer that requests data from {{es}} to your map, click **Add layer**, then select one of the following:

* Documents
* Choropleth
* Clusters and grid
* Heat map
* Point to point
* Top hits per entity
* Tracks


## Narrow layers by global search [maps-narrow-layer-by-global-search]

Layers that request data from {{es}} are narrowed when you submit a search. Layers narrowed by semi-structured search and filters contain the filter icon ![filter icon](/explore-analyze/images/kibana-filter_icon.png "") next to the layer name in the legend.

To prevent the global search from applying to a layer, configure the following:

* In **Filtering**, clear the **Apply global search to layer data** checkbox to turn off global search for the layer source.
* In **Term joins**, clear the **Apply global search to join** checkbox to turn off global search for the [term join](terms-join.md).


## Narrow layers by global time [maps-narrow-layer-by-global-time]

Layers that request data from {{es}} using a [data view](../../find-and-organize/data-views.md) with a configured time field are narrowed by the [global time](../../query-filter/filtering.md). These layers contain the clock icon ![clock icon](/explore-analyze/images/kibana-clock_icon.png "") next to the layer name in the legend.

Use the time slider to quickly select time slices within the global time range:

1. Click ![timeslider icon](/explore-analyze/images/kibana-timeslider_toggle_icon.png "") to open the time slider.
2. Click previous and next buttons to advance the time slice backward or forward.
3. Click play to animate your spatial temporal data.

To prevent the global time filter from applying to a layer, configure the following:

* In **Filtering**, clear the **Apply global time to layer data** checkbox to turn off the global time for the layer source.
* In **Term joins**, clear the **Apply global time to join** checkbox to turn off the global time for the [term join](terms-join.md).


## Refresh layer data [maps-refresh-layer]

Layers that request data from {{es}} re-fetch data when [automatic refresh](../../query-filter/filtering.md) fires and when you click **Refresh**.

To prevent refreshing layer data, configure the following:

* In **Filtering**, clear the **Apply global refresh to layer data** checkbox to turn off refresh for the layer source.




