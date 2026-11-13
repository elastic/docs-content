---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps-getting-started.html
description: Use Maps in Kibana to build a map of web traffic by country, with layers that change by zoom level, and filter it from a dashboard.
type: tutorial
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Build a map to compare metrics by country or region [maps-getting-started]

If you want to learn **Maps** by building something, this tutorial takes you from an empty map to a dashboard that shows web traffic by country and by location. Along the way, you see how layers stack, how a choropleth matches your data to country shapes, and how zoom levels decide which layer is visible.

By the end of this tutorial, you can:

* Combine reference boundaries and {{es}} data in one map with multiple layers
* Style features with colors, symbols, and labels that depend on data values
* Embed a map in a dashboard
* Filter the map and the other dashboard panels together

When you finish, you have a map like this one:

:::{image} /explore-analyze/images/kibana-sample_data_web_logs.png
:alt: A map of North America with shaded countries and circles that show the number of web requests per area. The Layers panel lists the Total Requests and Bytes, Actual Requests, and Total Requests by Destination layers, and the basemap.
:screenshot:
:::


## Prerequisites [_prerequisites_2]

You don’t need experience with **Maps**, but you should know how to open and edit a dashboard.

* If you don’t already have {{kib}}, set it up with [our free trial](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs).
* This tutorial requires the [web logs sample data set](/explore-analyze/index.md#gs-get-data-into-kibana). The sample data includes a **[Logs] Total Requests and Bytes** map, which you’ll re-create in this tutorial.
* You must have the correct privileges for creating a map. If you don’t have sufficient privileges to create or save maps, a **Read only** badge appears. For more information, refer to [Granting access to {{kib}}](elasticsearch://reference/elasticsearch/roles.md).


## Step 1. Create a map on a dashboard [maps-create]

You build the map on a dashboard, so you can return to the dashboard when you save the map. A map is a stack of layers. The **Basemap** layer draws the background, and every layer you add draws your data on top of it.

1. Open the **Dashboards** page and select **Create dashboard**.
2. Set the time range to **Last 7 days**.

    The map and the other panels show only data from this time range. If a panel looks empty later, widen the range.

3. Add a map panel:

    * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` Select **Add**. In the **Add to dashboard** flyout, select **Maps** in the **Other visualizations** group.
    * {applies_to}`stack: ga 9.2-9.4` Select **Add** → **New panel**, then select **Maps** in the **Visualizations** group.
    * {applies_to}`stack: ga 9.0-9.1` Select **Add panel**, then select **Maps** in the **Visualizations** group.

    The map editor opens. Its **Layers** panel lists the **Basemap** layer and has an **Add layer** button.


## Step 2. Shade countries by traffic with a choropleth layer [maps-add-choropleth-layer]

A choropleth layer shades areas by a value. Here, a country gets a darker shade the more web log requests it receives. {{kib}} gets the country shapes from the Elastic Maps Service (EMS), then matches each shape to the web logs by country code. This match is called a join.

1. Select **Add layer**, then select **Choropleth**.

    The **Add layer** panel offers more layer types. This tutorial uses **Choropleth**, **Documents**, and **Clusters**. To learn about the others, refer to [Vector layer](vector-layer.md), [Heat map layer](heatmap-layer.md), and [Tile layer](tile-layer.md).

2. Choose the country shapes. Keep **Boundaries source** set to **Administrative boundaries from the Elastic Maps Service**, then select **World Countries** in **EMS boundaries**.

    The **Join field** in this section is **ISO 3166-1 alpha-2 code**, the two-letter country code, such as `US`. Leave it as it is.

3. Choose the data to count. In **Statistics source**, set:

    * **Data view** to **Kibana Sample Data Logs**
    * **Join field** to **geo.dest**

    {{kib}} counts the web log documents for each value of `geo.dest`, the country code of the request’s destination. Each country gets the count for its own code.

4. Select **Add and continue**.

    {{kib}} adds the layer and opens its settings.

5. In **Layer settings**, set:

    * **Name** to `Total Requests by Destination`
    * **Opacity** to 50%

    The name identifies the layer in the layer list, the legend, and tooltips. A lower opacity lets the basemap show through the shaded countries.

6. Choose what the tooltip shows. When you select a country on the map, its tooltip lists the tooltip fields. **ISO 3166-1 alpha-2 code** is already there. To also show the country name:

    1. Select {icon}`plus` **Add** to open the field list.
    2. Select **name**, then select **Add**.

    The `name` field holds the country name from the EMS boundaries, for example `United States of America`. Without it, the tooltip shows only the country code and the request count.

7. In **Layer style**:

    * Set **Fill color** to **As number**, then select the gray color ramp. The fill color depends on the request count, so with this ramp, countries with more requests are darker.
    * Set **Border color** to white. White borders separate neighboring countries.
    * Under **Label**, change **By value** to **Fixed**. By default, the layer labels each country with its request count. A fixed label with no text removes these labels, so the basemap’s country names stay readable.

    To learn more about styling options, refer to [Vector style](vector-style.md).

8. Select **Keep changes**.

   Your map now shows the countries shaded by traffic:

   :::{image} /explore-analyze/images/kibana-gs_add_cloropeth_layer.png
   :alt: A map of Europe and Asia with countries shaded in gray. The legend shows the count of web log documents per country, from fewer than 78 to 538 or more.
   :screenshot:
   :::



## Step 3. Add layers for the Elasticsearch data [maps-add-elasticsearch-layer]

Drawing every web request at every zoom level would overwhelm the map. Instead, you add two layers for the {{es}} data. One shows individual requests when you zoom in. The other shows clusters of requests when you zoom out. Zoom levels run from 0, the whole world, to 24, individual streets.


### Add a layer for individual documents [_add_a_layer_for_individual_documents]

This layer displays each web log document as a point. It’s visible only when you zoom in.

1. Select **Add layer**, then select **Documents**.
2. Set **Data view** to **Kibana Sample Data Logs**.

    **Geospatial field** is already set to **geo.coordinates**. This field stores the location of each request, and {{kib}} uses it to place each document on the map. If your data view has more than one geospatial field, this is where you choose which one to plot.

3. Select **Add and continue**.
4. In **Layer settings**, set:

    * **Name** to `Actual Requests`
    * **Visibility** to the range [9, 24]
    * **Opacity** to 100%

    **Visibility** limits the layer to zoom levels 9 through 24. The points appear only when you zoom in close.

5. Add the tooltip fields to show when you select a point: **agent**, **bytes**, **clientip**, **host**, **machine.os**, **request**, **response**, and **timestamp**.
6. In **Scaling**, select **Limit results to 10,000**.

    {{kib}} draws at most 10,000 documents for the visible map area, which keeps the map fast. To compare this option with the others, refer to [Vector layer](vector-layer.md).

7. In **Layer style**, set **Fill color** to **#2200FF**.
8. Select **Keep changes**.

   From zoom level 9 to 24, your map shows individual requests:

   :::{image} /explore-analyze/images/kibana-gs_add_es_document_layer.png
   :alt: A map zoomed in on the east coast of the United States. Blue points mark individual requests, and a tooltip lists the fields of one request.
   :screenshot:
   :::



### Add a layer for aggregated data [_add_a_layer_for_aggregated_data]

A clusters layer groups nearby documents into grid cells and draws one circle for each cell. Because it uses an [aggregation](../../query-filter/aggregations.md), the layer stays fast even for very large data sets. You make it visible only when the map is zoomed out. Darker circles mark cells with more web log requests, and larger circles mark cells with more bytes transferred.

1. Select **Add layer**, then select **Clusters**.
2. Set **Data view** to **Kibana Sample Data Logs**.

    **Geospatial field** is again **geo.coordinates**. It decides which grid cell each document falls into.

3. Select **Add and continue**.
4. In **Layer settings**, set:

    * **Name** to `Total Requests and Bytes`
    * **Visibility** to the range [0, 9]
    * **Opacity** to 100%

    With the **Actual Requests** layer, this range means that one of the two layers is visible at every zoom level: clusters from 0 to 9, and individual requests from 9 to 24.

5. In **Metrics**:

    * Keep **Aggregation** set to **Count**.
    * Select **Add metric**.
    * Set **Aggregation** to **Sum** with **Field** set to **bytes**.

    Each cluster now reports two values: the number of requests and the total bytes. The count sets the circle’s color, and you use the sum for its size in the next step.

6. In **Layer style**, change **Symbol size**:

    * Set **By value** to **sum bytes**.
    * Set the min size to 7 and the max size to 25 px.

7. Select **Keep changes**.

   Between zoom levels 0 and 9, your map shows clusters over the shaded countries:

   :::{image} /explore-analyze/images/kibana-sample_data_web_logs.png
   :alt: A map of North America at zoom level 4 with circles that show the number of web requests per grid cell, over countries shaded by traffic. A tooltip shows the count and the sum of bytes for one circle.
   :screenshot:
   :::



## Step 4. Save the map and return to the dashboard [maps-save]

Now that your map is complete, save it and return to the dashboard.

1. Select **Save and return**.

    The map editor closes, and the map appears as a panel on your dashboard.


## Step 5. Explore your data from the dashboard [maps-embedding]

Put the map next to charts of the same web logs, then filter them together. A filter you set in one panel applies to every panel on the dashboard, so you can look at the same slice of data from different angles.

1. Open the list of panels that you can add from the library:

    * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` Select **Add** → **From library**.
    * {applies_to}`stack: ga 9.0-9.1` Select **Add from library**.

2. Select **[Logs] Unique Destination Heatmap** and **[Logs] Bytes distribution** to add them to the dashboard, then close the list.

   :::{image} /explore-analyze/images/kibana-gs_dashboard_with_map.png
   :alt: A dashboard with the map in the top half and the Bytes distribution chart and the Unique Destination Heatmap in the bottom half.
   :screenshot:
   :::

3. To filter for documents with unusually high byte values, select and drag across the high values in the **Bytes distribution** chart. The map and the heat map update.
4. To remove the filter, select the {icon}`cross` next to its name in the filter bar. All panels show the full data again.
5. Set a filter from the map:

    1. Select anywhere on the United States to open a tooltip.

       The tooltip has one page for each feature under your pointer. If it shows more than one page, use the arrows or the layer list to open the **Total Requests by Destination** page.

    2. To keep only the requests whose destination is the United States, select the {icon}`filter` **Filter on property** button in the row for **ISO 3166-1 alpha-2 code**.

       {{kib}} adds the filter `geo.dest: US`, because `geo.dest` is the field you joined in step 2.

       :::{image} /explore-analyze/images/kibana-gs_tooltip_filter.png
       :alt: The tooltip of the Total Requests by Destination layer for the United States, with the Filter on property button next to the country code.
       :screenshot:
       :::

       Your filtered dashboard should look similar to this:

       :::{image} /explore-analyze/images/kibana-gs_map_filtered.png
       :alt: The dashboard with the geo.dest US filter applied. The map and the heat map show only requests to the United States.
       :screenshot:
       :::

    The tooltip also has a **Filter by geometry** link, which filters by the country’s shape instead. Refer to [Create a filter from a map](maps-create-filter-from-map.md).

### Filter pill actions

:::{include} ../../_snippets/global-filters.md
:::

## What’s next? [_whats_next_6]

* Check out [additional types of layers](vector-layer.md) that you can add to your map.
* Learn how [terms joins](terms-join.md) match your data to boundaries.
* Learn more ways to [customize your map](maps-vector-style-properties.md).
* Learn more about [vector tooltips](vector-tooltip.md).
