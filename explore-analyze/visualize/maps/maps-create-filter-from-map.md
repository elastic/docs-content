---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps-create-filter-from-map.html
description: Create filters from Maps by drawing shapes or selecting features. Focus analysis on specific geographic regions with interactive spatial filtering.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Create filters from a map [maps-create-filter-from-map]

Create filters from your map to focus in on just the data you want. **Maps** provides three ways to create filters:

* [Filter dashboard by map bounds](#maps-map-extent-filter)
* [Spatial filters](#maps-spatial-filters)
* [Phrase filters](#maps-phrase-filter)


## Filter dashboard by map bounds [maps-map-extent-filter]

To filter your dashboard by your map bounds as you pan and zoom your map:

1. Go to **Dashboards**.
2. Select your dashboard from the list or click **Create dashboard**.
3. If your dashboard does not have a map, add a map panel.
4. Click the gear icon ![gear icon](/explore-analyze/images/kibana-gear_icon.png "") to open the map panel menu.
5. Select **More** to view all panel options.
6. Select **Filter dashboard by map bounds**.
7. Select the checkbox for your map panel.


## Spatial filters [maps-spatial-filters]

A spatial filter narrows search results to documents that either intersect with, are within, or do not intersect with the specified geometry.

Spatial filters have the following properties:

* **Geometry label** enables you to provide a meaningful name for your spatial filter.
* **Spatial relation** determines the [spatial relation operator](elasticsearch://reference/query-languages/query-dsl/query-dsl-geo-shape-query.md#geo-shape-spatial-relations) to use at search time.
* **Action** specifies whether to apply the filter to the current view or to a drilldown action.

::::{note}
[Drilldowns](../../dashboards/drilldowns.md) are available only if the map is a panel in a [dashboard](../../dashboards.md), and not within the Maps application.
::::


You can create spatial filters in two ways:

* Click the tool icon ![tool icon](/explore-analyze/images/kibana-tools_icon.png ""), and then draw a shape, bounding box, or distance on the map to define the spatial filter.
* Click **Filter by geometry** in a [locked tooltip](vector-tooltip.md#maps-vector-tooltip-locking), and then use the feature’s geometry for the spatial filter.

:::{image} /explore-analyze/images/kibana-create_spatial_filter.png
:alt: create spatial filter
:screenshot:
:::


## Phrase filters [maps-phrase-filter]

A phrase filter narrows search results to documents that contain the specified text. You can create a phrase filter by clicking the plus icon ![gs plus icon](/explore-analyze/images/kibana-gs_plus_icon.png "") in a [locked tooltip](vector-tooltip.md#maps-vector-tooltip-locking). If the map is a dashboard panel with drilldowns, you can apply a phrase filter to a drilldown by selecting the drilldown action.

