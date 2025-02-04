---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/geospatial-analysis.html
---

# Geospatial analysis [geospatial-analysis]

Did you know that {{es}} has geospatial capabilities? [{{es}} and geo](https://www.elastic.co/blog/geo-location-and-search) go way back, to 2010. A lot has happened since then and today {{es}} provides robust geospatial capabilities with speed, all with a stack that scales automatically.

Not sure where to get started with {{es}} and geo? Then, you have come to the right place.


## Geospatial mapping [geospatial-mapping]

{{es}} supports two types of geo data: [geo_point](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html) fields which support lat/lon pairs, and [geo_shape](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-shape.html) fields, which support points, lines, circles, polygons, multi-polygons, and so on. Use [explicit mapping](../manage-data/data-store/mapping/explicit-mapping.md) to index geo data fields.

Have an index with lat/lon pairs but no geo_point mapping? Use [runtime fields](../manage-data/data-store/mapping/map-runtime-field.md) to make a geo_point field without reindexing.


## Ingest [geospatial-ingest]

Data is often messy and incomplete. [Ingest pipelines](../manage-data/ingest/transform-enrich/ingest-pipelines.md) lets you clean, transform, and augment your data before indexing.

* Use [CSV](https://www.elastic.co/guide/en/elasticsearch/reference/current/csv-processor.html) together with [explicit mapping](../manage-data/data-store/mapping/explicit-mapping.md) to index CSV files with geo data. Kibana’s [Import CSV](visualize/maps/import-geospatial-data.md) feature can help with this.
* Use [GeoIP](https://www.elastic.co/guide/en/elasticsearch/reference/current/geoip-processor.html) to add geographical location of an IPv4 or IPv6 address.
* Use [geo-grid processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest-geo-grid-processor.html) to convert grid tiles or hexagonal cell ids to bounding boxes or polygons which describe their shape.
* Use [geo_match enrich policy](../manage-data/ingest/transform-enrich/example-enrich-data-based-on-geolocation.md) for reverse geocoding. For example, use [reverse geocoding](visualize/maps/reverse-geocoding-tutorial.md) to visualize metropolitan areas by web traffic.


## Query [geospatial-query]

[Geo queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-queries.html) answer location-driven questions. Find documents that intersect with, are within, are contained by, or do not intersect your query geometry. Combine geospatial queries with full text search queries for unparalleled searching experience. For example, "Show me all subscribers that live within 5 miles of our new gym location, that joined in the last year and have running mentioned in their profile".


## ES|QL [esql-query]

[ES|QL](query-filter/languages/esql.md) has support for [Geospatial Search](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-functions-operators.html#esql-spatial-functions) functions, enabling efficient index searching for documents that intersect with, are within, are contained by, or are disjoint from a query geometry. In addition, the `ST_DISTANCE` function calculates the distance between two points.

* [`ST_INTERSECTS`](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-functions-operators.html#esql-st_intersects)
* [`ST_DISJOINT`](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-functions-operators.html#esql-st_disjoint)
* [`ST_CONTAINS`](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-functions-operators.html#esql-st_contains)
* [`ST_WITHIN`](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-functions-operators.html#esql-st_within)
* [`ST_DISTANCE`](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-functions-operators.html#esql-st_distance)


## Aggregate [geospatial-aggregate]

[Aggregations](aggregations.md) summarizes your data as metrics, statistics, or other analytics. Use [bucket aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket.html) to group documents into buckets, also called bins, based on field values, ranges, or other criteria. Then, use [metric aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics.html) to calculate metrics, such as a sum or average, from field values in each bucket. Compare metrics across buckets to gain insights from your data.

Geospatial bucket aggregations:

* [Geo-distance aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-geodistance-aggregation.html) evaluates the distance of each geo_point location from an origin point and determines the buckets it belongs to based on the ranges (a document belongs to a bucket if the distance between the document and the origin falls within the distance range of the bucket).
* [Geohash grid aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-geohashgrid-aggregation.html) groups geo_point and geo_shape values into buckets that represent a grid.
* [Geohex grid aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-geohexgrid-aggregation.html) groups geo_point and geo_shape values into buckets that represent an H3 hexagonal cell.
* [Geotile grid aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-geotilegrid-aggregation.html) groups geo_point and geo_shape values into buckets that represent a grid. Each cell corresponds to a [map tile](https://en.wikipedia.org/wiki/Tiled_web_map) as used by many online map sites.

Geospatial metric aggregations:

* [Geo-bounds aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-geobounds-aggregation.html) computes the geographic bounding box containing all values for a Geopoint or Geoshape field.
* [Geo-centroid aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-geocentroid-aggregation.html) computes the weighted centroid from all coordinate values for geo fields.
* [Geo-line aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-geo-line.html) aggregates all geo_point values within a bucket into a LineString ordered by the chosen sort field. Use geo_line aggregation to create [vehicle tracks](visualize/maps/asset-tracking-tutorial.md).

Combine aggregations to perform complex geospatial analysis. For example, to calculate the most recent GPS tracks per flight, use a [terms aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html) to group documents into buckets per aircraft. Then use geo-line aggregation to compute a track for each aircraft. In another example, use geotile grid aggregation to group documents into a grid. Then use geo-centroid aggregation to find the weighted centroid of each grid cell.


## Integrate [geospatial-integrate]

Use [vector tile search API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-vector-tile-api.html) to consume {{es}} geo data within existing GIS infrastructure.


## Visualize [geospatial-visualize]

Visualize geo data with [Kibana](visualize/maps.md). Add your map to a [dashboard](dashboards.md) to view your data from all angles.

This dashboard shows the effects of the [Cumbre Vieja eruption](https://www.elastic.co/blog/understanding-evolution-volcano-eruption-elastic-maps/).

![Kibana dashboard showing Cumbre Vieja eruption from Aug 31 2021 to Dec 14 2021](../images/elasticsearch-reference-cumbre_vieja_eruption_dashboard.png "")


## Machine learning [geospatial-ml]

Put machine learning to work for you and find the data that should stand out with anomaly detections. Find credit card transactions that occur in an unusual locations or a web request that has an unusual source location. [Location-based anomaly detections](machine-learning/anomaly-detection/geographic-anomalies.md) make it easy to find and explore and compare anomalies with their typical locations.


## Alerting [geospatial-alerting]

Let your location data drive insights and action with [geographic alerts](alerts/kibana/geo-alerting.md). Commonly referred to as geo-fencing, track moving objects as they enter or exit a boundary to receive notifications through common business systems (email, Slack, Teams, PagerDuty, and more).

Interested in learning more? Follow [step-by-step instructions](visualize/maps/asset-tracking-tutorial.md) for setting up tracking containment alerts to monitor moving vehicles.

