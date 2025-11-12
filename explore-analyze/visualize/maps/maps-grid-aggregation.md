---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps-grid-aggregation.html
description: Visualize data with grid aggregations in Maps using geohash, geotile, or geohex grids. Group documents into geographic buckets for density analysis.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Clusters [maps-grid-aggregation]

Clusters use [Geotile grid aggregation](elasticsearch://reference/aggregations/search-aggregations-bucket-geotilegrid-aggregation.md) or [Geohex grid aggregation](elasticsearch://reference/aggregations/search-aggregations-bucket-geohexgrid-aggregation.md) to group your documents into grids. You can calculate metrics for each gridded cell.

Symbolize cluster metrics as:

**Clusters**
:   Uses [Geotile grid aggregation](elasticsearch://reference/aggregations/search-aggregations-bucket-geotilegrid-aggregation.md) to group your documents into grids. Creates a [vector layer](vector-layer.md) with a cluster symbol for each gridded cell. The cluster location is the weighted centroid for all documents in the gridded cell.

**Grids**
:   Uses [Geotile grid aggregation](elasticsearch://reference/aggregations/search-aggregations-bucket-geotilegrid-aggregation.md) to group your documents into grids. Creates a [vector layer](vector-layer.md) with a bounding box polygon for each gridded cell.

**Heat map**
:   Uses [Geotile grid aggregation](elasticsearch://reference/aggregations/search-aggregations-bucket-geotilegrid-aggregation.md) to group your documents into grids. Creates a [heat map layer](heatmap-layer.md) that clusters the weighted centroids for each gridded cell.

**Hexbins**
:   Uses [Geohex grid aggregation](elasticsearch://reference/aggregations/search-aggregations-bucket-geohexgrid-aggregation.md) to group your documents into H3 hexagon grids. Creates a [vector layer](vector-layer.md) with a hexagon polygon for each gridded cell.

To enable a clusters layer:

1. Click **Add layer**, then select the **Clusters** or **Heat map** layer.

To enable a blended layer that dynamically shows clusters or documents:

1. Click **Add layer**, then select the **Documents** layer.
2. Configure **Data view** and the **Geospatial field**.
3. In **Scaling**, select **Show clusters when results exceed 10000**.

