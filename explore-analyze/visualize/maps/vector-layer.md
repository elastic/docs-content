---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/vector-layer.html
---

# Vector layer [vector-layer]

Vector layers display points, lines, and polygons.

:::{image} ../../../images/kibana-vector_layer.png
:alt: vector layer
:class: screenshot
:::

To add a vector layer to your map, click **Add layer**, then select one of the following:

**Choropleth**
:   Shaded areas to compare statistics across boundaries.

**Clusters**
:   Geospatial data grouped in grids with metrics for each gridded cell. The index must contain at least one field mapped as [geo_point](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html) or [geo_shape](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-shape.html).

**Create index**
:   Draw shapes on the map and index in Elasticsearch.

**Documents**
:   Points, lines, and polyons from Elasticsearch. The index must contain at least one field mapped as [geo_point](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html) or [geo_shape](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-shape.html).

    Results are limited to the `index.max_result_window` index setting, which defaults to 10000. Select the appropriate **Scaling** option for your use case.

    * **Limit results to 10,000** The layer displays features from the first `index.max_result_window` documents. Results exceeding `index.max_result_window` are not displayed.
    * **Show clusters when results exceed 10,000** When results exceed `index.max_result_window`, the layer uses [GeoTile grid aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-geotilegrid-aggregation.html) to group your documents into clusters and displays metrics for each cluster. When results are less then `index.max_result_window`, the layer displays features from individual documents.
    * **Use vector tiles.** Vector tiles partition your map into tiles. Each tile request is limited to the `index.max_result_window` index setting. When a tile exceeds `index.max_result_window`, results exceeding `index.max_result_window` are not contained in the tile and a dashed rectangle outlining the bounding box containing all geo values within the tile is displayed.


**EMS Boundaries**
:   Administrative boundaries from [Elastic Maps Service](https://www.elastic.co/elastic-maps-service).

**ML Anomalies**
:   Points and lines associated with anomalies. The {{anomaly-job}} must use a `lat_long` function. Go to [Detecting anomalous locations in geographic data](../../machine-learning/anomaly-detection/geographic-anomalies.md) for an example.

**Point to point**
:   Aggregated data paths between the source and destination. The index must contain at least 2 fields mapped as [geo_point](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html), source and destination.

**Top hits per entity**
:   The layer displays the [most relevant documents per entity](maps-top-hits-aggregation.md). The index must contain at least one field mapped as [geo_point](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html) or [geo_shape](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-shape.html).

**Tracks**
:   Create lines from points. The index must contain at least one field mapped as [geo_point](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html).

**Upload Geojson**
:   Index GeoJSON data in Elasticsearch.




