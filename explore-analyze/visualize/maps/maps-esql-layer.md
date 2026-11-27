---
navigation_title: "ES|QL layer"
description: Create a map layer from an ES|QL query to plot points, shapes, and grids, narrow it by map area, time, and search, and tie grid detail to the zoom level.
type: how-to
applies_to:
  serverless: preview
  stack: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Create a map layer from an {{esql}} query [maps-esql-layer]

If you want to map the result of a calculation, such as the number of requests per area, an {{esql}} layer draws each row that your query returns as a point, line, or polygon. The layer can narrow the query to the visible map area, the time range, and your search. The query then covers only the data you're looking at.

## Before you begin

To follow these steps, you need data that your query can turn into a location, such as an index with a `geo_point` or `geo_shape` field. The examples use the **Kibana Sample Data Logs** data set and its `geo.coordinates` field. If you haven't installed it yet, refer to [Sample data](/manage-data/ingest/sample-data.md).

## Add an {{esql}} layer [maps-esql-layer-add]

1. Go to **Maps**, then open a map or select **Create map**.
2. Select **Add layer**, then select **ES|QL**.
3. Enter a query that returns the data to plot. If your data has a geospatial field, {{kib}} starts you with a query that keeps that field.

   For example, this query plots each request as a point, with its client IP address and the bytes transferred:

   ```esql
   FROM kibana_sample_data_logs
   | KEEP geo.coordinates, clientip, bytes
   | LIMIT 10000
   ```

4. Run the query. The map previews the layer. If the editor shows an error, refer to [](#maps-esql-layer-query) for what the query must return.
5. Check the options that narrow the layer to the visible map area, the time range, and your search. They appear with the query editor. Refer to [](#maps-esql-layer-narrow).
6. Select **Add and continue**.
7. In **Layer settings**, enter a **Name** for the layer, and adjust **Layer style** if you want.
8. Select **Keep changes**.

The map draws one feature for each row that the query returns. To see how many rows came back, hover over the layer's icon in the layer list.

{applies_to}`stack: preview 9.2+` To see the other columns of a row, hover over or select its feature on the map.

## Write a query the map can draw [maps-esql-layer-query]

The map draws each row of the result as a feature. The result needs one column that holds the location.

* The query must return exactly one column of type `geo_point` or `geo_shape`. If it returns none or more than one, the editor shows an error. Use `KEEP` or `DROP` to narrow the columns.
* {applies_to}`stack: preview 9.2+` The tooltip of a feature lists the other columns of its row.
* When a query returns six or more columns, the editor suggests `KEEP` or `DROP` to narrow them, because fewer columns make the map faster.
* A query without a [`LIMIT`](elasticsearch://reference/query-languages/esql/commands/limit.md) command returns up to 1,000 rows. The query that {{kib}} starts you with ends with `limit 10000`, and you can raise it up to the [result set size limit](elasticsearch://reference/query-languages/esql/limitations.md) of your cluster. When the results reach the limit, the tooltip on the layer's icon says that the results are limited to the first rows.

If your locations are stored as text instead of in a geospatial field, the query can convert them with [`TO_GEOPOINT`](elasticsearch://reference/query-languages/esql/functions-operators/type-conversion-functions/to_geopoint.md) or [`TO_GEOSHAPE`](elasticsearch://reference/query-languages/esql/functions-operators/type-conversion-functions/to_geoshape.md). Both functions read the well-known text (WKT) format, such as `POINT (-73.98 40.75)`, which lists the longitude first. With `ROW`, you can also mark a place that isn't in any index:

```esql
ROW location = TO_GEOPOINT("POINT (2.2945 48.8584)"), name = "Eiffel Tower"
```

When the query doesn't read a geospatial field from an index, {{kib}} turns off the option that limits the layer to the visible map area. The layer then loads every row, wherever you look on the map.

## Narrow the layer by map area, time, and search [maps-esql-layer-narrow]

An {{esql}} layer can ask only for the data that matters to the current view. The following options appear with the query editor, both when you add the layer and when you edit it later. All three are on by default when your data has the fields they need.

These options apply as filters on the documents before your query runs, so a `STATS` command aggregates only the narrowed documents.

**Dynamically filter for data in the visible map area**
:   Limits the query to the documents inside the visible map area. **Filter by** lists the geospatial fields of your data. Select the one that the filter uses.

**Apply global search to ES|QL statement**
:   Applies the filters and the query that narrow the whole map. Refer to [Search geographic data](maps-search.md).

**Apply global time range to ES|QL statement**
:   Applies the time range of the map. **Filter by** lists the time fields of your data. Select the one that the range uses.

To apply the time range at a specific point in the query instead, use the `?_tstart` and `?_tend` parameters and turn off **Apply global time range to ES|QL statement**. The layer still runs the query again when the time range changes. Refer to [Custom time parameters](/explore-analyze/query-filter/languages/esql-kibana.md#_custom_time_parameters).

When the map refreshes automatically or you select **Refresh**, the layer runs the query again. To stop that for one layer, turn off **Re-fetch layer data on refresh** in the layer settings.

## Color areas with shapes from another index [maps-esql-layer-join]

If your documents hold a region code instead of a shape, such as a country code, the query can add the shape of each region from another index. The map then colors each region by a value that the query calculates, like the map in [Build a map to compare metrics by country or region](maps-getting-started.md).

The shapes must come from a [lookup index](elasticsearch://reference/query-languages/esql/esql-lookup-join.md), which is an index that uses the `lookup` index mode. The [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/commands/lookup-join.md) command adds the columns of the matching document to each row. For example, with a `world_countries` lookup index that holds a two-letter `iso2` code and a `geometry` shape for each country, this query counts requests per destination country:

```esql
FROM kibana_sample_data_logs
| STATS count = COUNT(*) BY geo.dest
| RENAME geo.dest AS iso2
| LOOKUP JOIN world_countries ON iso2
| KEEP geometry, iso2, count
```

`RENAME` gives the country code the name of the matching field in the lookup index. To shade the countries, set **Fill color** to **By value** and select `count` in the layer style.

The option that limits the layer to the visible map area filters the documents by the field selected in **Filter by**, not by the shapes that the join adds. To count all documents wherever you look on the map, turn off **Dynamically filter for data in the visible map area**.

## Make grids follow the zoom level [maps-esql-layer-zoom-precision]
```{applies_to}
serverless: preview
stack: preview 9.7+
```

If a layer groups documents into grid cells, you can let the map pick the cell size from the zoom level. The cells then stay readable as you zoom in and out.

The cell size of a grid comes from the `precision` argument of the [`ST_GEOTILE`](elasticsearch://reference/query-languages/esql/functions-operators/spatial-functions/st_geotile.md), [`ST_GEOHEX`](elasticsearch://reference/query-languages/esql/functions-operators/spatial-functions/st_geohex.md), and [`ST_GEOHASH`](elasticsearch://reference/query-languages/esql/functions-operators/spatial-functions/st_geohash.md) functions. Instead of a fixed number, pass the matching parameter, and {{kib}} fills in a value for the current zoom level:

* `?_geotile_precision` for `ST_GEOTILE`
* `?_geohex_precision` for `ST_GEOHEX`
* `?_geohash_precision` for `ST_GEOHASH`

For example, this query counts requests per tile and draws each tile as a polygon:

```esql
FROM kibana_sample_data_logs
| STATS count = COUNT(*), sumOfBytes = SUM(bytes)
    BY geotile = ST_GEOTILE(geo.coordinates, ?_geotile_precision)
| EVAL tile = TO_GEOSHAPE(geotile)
| KEEP tile, count, sumOfBytes
```

To draw a circle for each cell instead, like a [Clusters](maps-grid-aggregation.md) layer, return the center of the documents in each cell with [`ST_CENTROID_AGG`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions/st_centroid_agg.md):

```esql
FROM kibana_sample_data_logs
| STATS count = COUNT(*), centroid = ST_CENTROID_AGG(geo.coordinates)
    BY geotile = ST_GEOTILE(geo.coordinates, ?_geotile_precision)
| KEEP centroid, count
```

To size the circles by the number of requests, set **Symbol size** to **By value** and select `count` in the layer style.

When you zoom far enough to change the value, the layer runs the query again with the new precision. When you write the `precision` argument, autocomplete suggests the matching parameter, and hovering over the parameter shows a description.

To make the cells smaller or larger at every zoom level, move the **Resolution** slider toward **high** for finer detail or toward **low** for coarser detail. The slider appears with the other layer options, both when you add the layer and when you edit it later, but only when the query uses one of the three parameters.

These parameters work only in Maps layers, not in a [Vega visualization](/explore-analyze/visualize/custom-visualizations-with-vega.md).

## When to use another layer type [maps-esql-layer-limits]

An {{esql}} layer loads the rows of one query, so some map features work differently than on layers that you configure without a query:

* The **Fit to data** layer action isn't available for an {{esql}} layer. To find its features, pan and zoom the map.
* The layer loads all its rows at once, up to the query limit, instead of loading the map in tiles. When your data has more documents than the limit, aggregate them in the query with `STATS`, or use a [Documents layer with vector tiles](vector-layer.md).
* When you style features **By value**, the color and size ranges come from the rows that the layer returned, not from the whole index. As you pan or zoom, the ranges can change with the rows.

## Next steps

To change how the features that your query returns look, refer to [Vector styling](vector-style.md).

## Related pages

* [Clusters](maps-grid-aggregation.md): Group documents into grids without writing a query.
* [Use {{esql}} in {{kib}}](/explore-analyze/query-filter/languages/esql-kibana.md): Get help from the editor as you write queries.
* {applies_to}`stack: preview 9.6+` [Approximate results on a dashboard](../maps.md#maps-esql-fast-mode): Get faster, estimated results for a `STATS` query when the map is on a dashboard.
* {applies_to}`serverless: ga` {applies_to}`stack: unavailable` [Search across linked projects](../maps.md#maps-cps): Choose which projects the map queries, and change them for one layer with `SET project_routing`.
