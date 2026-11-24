---
navigation_title: "ES|QL layer"
description: Create a map layer from an ES|QL query to plot points, shapes, and grids, narrow it by map area, time, and search, and tie grid detail to the zoom level.
type: how-to
applies_to:
  stack: beta
  serverless: beta
products:
  - id: kibana
  - id: cloud-serverless
---

# Create a map layer from an {{esql}} query [maps-esql-layer]

If you want to map the result of a calculation, such as the number of requests per area, an {{esql}} layer draws each row that your query returns as a point, line, or polygon. The layer can narrow the query to the visible map area, the time range, and your search, so the query covers only the data you're looking at.

## Before you begin

To follow these steps, you need data that your query can turn into a location, such as an index with a `geo_point` or `geo_shape` field. The examples use the **Kibana Sample Data Logs** data set and its `geo.coordinates` field. If you haven't installed it yet, refer to [Sample data](/manage-data/ingest/sample-data.md).

## Add an {{esql}} layer [maps-esql-layer-add]

1. Go to **Maps**, then open a map or select **Create map**.
2. Select **Add layer**, then select **ES|QL**.
3. Write a query that returns the data to plot, and run it. If your data has a geospatial field, {{kib}} starts you with a query that keeps that field. To see what the query can return, refer to [](#maps-esql-layer-query).

   For example, this query plots each request as a point and adds the client IP address and the bytes transferred to its tooltip:

   ```esql
   FROM kibana_sample_data_logs
   | KEEP geo.coordinates, clientip, bytes
   | LIMIT 10000
   ```

4. Select **Add and continue**.
5. In **Layer settings**, name the layer and adjust **Layer style**, then select **Keep changes**.

The map draws one feature for each row that the query returns. To see how many rows came back, hover over the layer's icon in the layer list. To see the other columns of a row, hover over or select its feature on the map.

## Write a query the map can draw [maps-esql-layer-query]

The map draws each row of the result as a feature, so the result needs one column that holds a location.

* The query must return exactly one column of type `geo_point` or `geo_shape`. If it returns none or more than one, the editor shows an error. Use `KEEP` or `DROP` to narrow the columns.
* The tooltip of a feature lists the other columns of its row.
* When a query returns six or more columns, the editor suggests `KEEP` or `DROP` to narrow them, because fewer columns make the map faster.
* A query returns up to 1,000 rows by default. A [`LIMIT`](elasticsearch://reference/query-languages/esql/commands/limit.md) command can raise that to 10,000. When the results reach the limit, the tooltip on the layer's icon says that the results are limited to the first rows.

## Narrow the layer by map area, time, and search [maps-esql-layer-narrow]

By default, an {{esql}} layer asks only for the data that matters to the current view. These options apply as filters on the documents before your query runs, so a `STATS` command aggregates only the narrowed documents.

**Dynamically filter for data in the visible map area**
:   Limits the query to the documents inside the visible map area. Use **Filter by** to select the geospatial field that the filter uses.

**Apply global search to ES|QL statement**
:   Applies the filters and the query that narrow the whole map. Refer to [Search geographic data](maps-search.md).

**Apply global time range to ES|QL statement**
:   Applies the time range of the map. Use **Filter by** to select the time field that the range uses.

To control where the time range applies inside the query, use the `?_tstart` and `?_tend` parameters instead. Refer to [Custom time parameters](/explore-analyze/query-filter/languages/esql-kibana.md#_custom_time_parameters).

When the map refreshes automatically or you select **Refresh**, the layer runs the query again. To stop that for one layer, turn off **Re-fetch layer data on refresh** in the layer settings.

## Make grids follow the zoom level [maps-esql-layer-zoom-precision]
```{applies_to}
serverless: beta
stack: beta 9.7+
```

If a layer groups documents into grid cells, you can let the map pick the cell size from the zoom level. The cells then stay readable as you zoom in and out.

The cell size of a grid comes from the `precision` argument of the [`ST_GEOTILE`](elasticsearch://reference/query-languages/esql/functions-operators/spatial-functions/st_geotile.md), [`ST_GEOHEX`](elasticsearch://reference/query-languages/esql/functions-operators/spatial-functions/st_geohex.md), and [`ST_GEOHASH`](elasticsearch://reference/query-languages/esql/functions-operators/spatial-functions/st_geohash.md) functions. Instead of a fixed number, pass the matching parameter, and Maps fills in a value for the current zoom level:

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

When you zoom far enough to change the value, the layer runs the query again with the new precision. When you write the `precision` argument, autocomplete suggests the matching parameter, and hovering over the parameter shows a description.

To make the cells smaller or larger at every zoom level, move the **Resolution** slider toward **high** for finer detail or toward **low** for coarser detail. The slider appears only when the query uses one of the three parameters.

Only Maps fills in these parameters. A query that uses them doesn't work in a Vega visualization.

## Related pages

* [Clusters](maps-grid-aggregation.md): Group documents into grids without writing a query.
* [Vector style](vector-style.md): Change the colors and sizes of the features that your query returns.
* [Use {{esql}} in {{kib}}](/explore-analyze/query-filter/languages/esql-kibana.md): Get help from the editor as you write queries.
