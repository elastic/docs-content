---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps-getting-started.html
description: Step-by-step tutorial for building Maps to compare metrics by country or region. Create multi-layer maps with styled data, labels, and dashboard integration.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Build a map to compare metrics by country or region [maps-getting-started]

In this tutorial, you'll learn the fundamentals of creating maps in {{kib}} by building a multi-layer visualization that compares web traffic metrics across countries. You'll explore how to add layers, style data with colors and labels, and embed maps in dashboards. By the end, you'll understand the core workflows for building effective geographic visualizations.

You will learn to:

* Create a map with multiple layers and data sources
* Use symbols, colors, and labels to style data values
* Embed a map in a dashboard
* Search across panels in your dashboard

When you complete this tutorial, you’ll have a map that looks like this:

:::{image} /explore-analyze/images/kibana-sample_data_web_logs.png
:alt: sample data web logs
:screenshot:
:::


## Prerequisites [_prerequisites_2]

* If you don’t already have {{kib}}, set it up with [our free trial](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs).
* This tutorial requires the [web logs sample data set](/explore-analyze/index.md#gs-get-data-into-kibana). The sample data includes a [Logs] Total Requests and Bytes map, which you’ll re-create in this tutorial.
* You must have the correct privileges for creating a map. If you don’t have sufficient privileges to create or save maps, a read-only icon appears in the toolbar. For more information, refer to [Granting access to {{kib}}](elasticsearch://reference/elasticsearch/roles.md).


## Step 1. Create a map [maps-create]

1. Go to **Dashboards**.
2. Click **Create dashboard**.
3. Set the time range to **Last 7 days**.
4. Click the **Create new Maps** icon ![app gis icon](/explore-analyze/images/kibana-app_gis_icon.png "").


## Step 2. Add a choropleth layer [maps-add-choropleth-layer]

The first layer you’ll add is a choropleth layer to shade world countries by web log traffic. Darker shades will symbolize countries with more web log traffic, and lighter shades will symbolize countries with less traffic.

1. Click **Add layer**, and then click **Choropleth**.
2. From the **EMS boundaries** dropdown menu, select **World Countries**.
3. In **Statistics source**, set:

    * **Data view** to **kibana_sample_data_logs**
    * **Join field** to **geo.dest**

4. Click **Add and continue**.
5. In **Layer settings**, set:

    * **Name** to `Total Requests by Destination`
    * **Opacity** to 50%

6. Add a Tooltip field:

    * **ISO 3166-1 alpha-2 code** is added by default.
    * Click **+ Add** to open the field select.
    * Select **name** and click **Add**.

7. In **Layer style**:

    * Set **Fill color > As number** to the grey color ramp.
    * Set **Border color** to white.
    * Under **Label**, change **By value** to **Fixed**.

8. Click **Keep changes**.

   Your map now looks like this:

   :::{image} /explore-analyze/images/kibana-gs_add_cloropeth_layer.png
   :alt: Map showing the Total Requests by Destination layer
   :screenshot:
   :::



## Step 3. Add layers for the Elasticsearch data [maps-add-elasticsearch-layer]

To avoid overwhelming the user with too much data at once, you’ll add two layers for the Elasticsearch data. The first layer will display individual documents when users zoom in on the map. The second layer will display aggregated data when users zoom the map out.


### Add a layer for individual documents [_add_a_layer_for_individual_documents]

This layer displays web log documents as points. The layer is only visible when users zoom in.

1. Click **Add layer**, and then click **Documents**.
2. Set **Data view** to **kibana_sample_data_logs**.
3. Click **Add and continue**.
4. In **Layer settings**, set:

    * **Name** to `Actual Requests`
    * **Visibility** to the range [9, 24]
    * **Opacity** to 100%

5. Add a tooltip field and select **agent**, **bytes**, **clientip**, **host**, **machine.os**, **request**, **response**, and **timestamp**.
6. In **Scaling**, enable **Limit results to 10,000.**
7. In **Layer style**, set **Fill color** to **#2200FF**.
8. Click **Keep changes**.

   Your map will look like this from zoom level 9 to 24:

   :::{image} /explore-analyze/images/kibana-gs_add_es_document_layer.png
   :alt: Map showing what zoom level looks like a level 9
   :screenshot:
   :::



### Add a layer for aggregated data [_add_a_layer_for_aggregated_data]

You’ll create a layer for [aggregated data](../../query-filter/aggregations.md) and make it visible only when the map is zoomed out. Darker colors will symbolize grids with more web log traffic, and lighter colors will symbolize grids with less traffic. Larger circles will symbolize grids with more total bytes transferred, and smaller circles will symbolize grids with less bytes transferred.

1. Click **Add layer**, and select **Clusters**.
2. Set **Data view** to **kibana_sample_data_logs**.
3. Click **Add and continue**.
4. In **Layer settings**, set:

    * **Name** to `Total Requests and Bytes`
    * **Visibility** to the range [0, 9]
    * **Opacity** to 100%

5. In **Metrics**:

    * Set **Aggregation** to **Count**.
    * Click **Add metric**.
    * Set **Aggregation** to **Sum** with **Field** set to **bytes**.

6. In **Layer style**, change **Symbol size**:

    * Set **By value** to **sum bytes**.
    * Set the min size to 7 and the max size to 25 px.

7. Click **Keep changes** button.

   Your map will look like this between zoom levels 0 and 9:

   :::{image} /explore-analyze/images/kibana-sample_data_web_logs.png
   :alt: Map showing what zoom level 3 looks like
   :screenshot:
   :::



## Step 4. Save the map [maps-save]

Now that your map is complete, save it and return to the dashboard.

1. In the toolbar, click **Save and return**.


## Step 5. Explore your data from the dashboard [maps-embedding]

View your geospatial data alongside a heat map and pie chart, and then filter the data. When you apply a filter in one panel, it is applied to all panels on the dashboard.

1. Click **Add from library** to open a list of panels that you can add to the dashboard.
2. Add **[Logs] Unique Destination Heatmap** and **[Logs] Bytes distribution** to the dashboard.

   :::{image} /explore-analyze/images/kibana-gs_dashboard_with_map.png
   :alt: Map in a dashboard with 2 other panels
   :screenshot:
   :::

3. To filter for documents with unusually high byte values, click and drag in the **Bytes distribution** chart.
4. Remove the filter by clicking **x** next to its name in the filter bar.
5. Set a filter from the map:

    1. Open a tooltip by clicking anywhere in the United States vector.
    2. To show only documents where **geo.src** is **US**, click the filter icon ![filter icon](/explore-analyze/images/kibana-gs-filter-icon.png "kibana-gs-filter-icon =4%x4%")in the row for **ISO 3066-1 alpha-2**.

       :::{image} /explore-analyze/images/kibana-gs_tooltip_filter.png
       :alt: Tooltip on map
       :screenshot:
       :::

       Your filtered map should look similar to this:

       :::{image} /explore-analyze/images/kibana-gs_map_filtered.png
       :alt: Map showing filtered data
       :screenshot:
       :::

### Filter pill actions

:::{include} ../../_snippets/global-filters.md
:::

## What’s next? [_whats_next_6]

* Check out [additional types of layers](vector-layer.md) that you can add to your map.
* Learn more ways [customize your map](maps-vector-style-properties.md).
* Learn more about [vector tooltips](vector-tooltip.md).
