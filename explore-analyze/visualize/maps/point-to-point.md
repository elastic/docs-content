---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/point-to-point.html
description: Visualize connections between geographic locations with point-to-point layers. Display origin-destination relationships and directional flows on maps.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Point-to-point layers [point-to-point]

Point-to-point layers visualize origin-destination relationships by drawing lines between source and destination locations. Line thickness and color intensity represent connection volume or frequency, with thicker, darker lines showing higher traffic and thinner, lighter lines showing lower traffic.

Point-to-point layers work well for network traffic visualization, flight routes, migration patterns, and delivery logistics.

Point to point uses an {{es}} [terms aggregation](elasticsearch://reference/aggregations/search-aggregations-bucket-terms-aggregation.md) to group your documents by destination. Then, a nested [GeoTile grid aggregation](elasticsearch://reference/aggregations/search-aggregations-bucket-geotilegrid-aggregation.md) groups sources for each destination into grids. A line connects each source grid centroid to each destination.

Point-to-point layers are used in several common use cases:

* Source-destination maps for network traffic
* Origin-destination maps for flight data
* Origin-destination flows for import/export/migration
* Origin-destination for pick-up/drop-off data

:::{image} /explore-analyze/images/kibana-point_to_point.png
:alt: point to point
:::

