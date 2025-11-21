---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/indexing-geojson-data-tutorial.html
description: Step-by-step tutorial for importing and indexing GeoJSON files into Elasticsearch. Build multi-layer maps displaying flight paths and geographic points.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Tutorial: Index GeoJSON data [indexing-geojson-data-tutorial]

In this tutorial, you'll learn how to import and index GeoJSON files into {{product.elasticsearch}} for visualization in Maps. You'll explore uploading vector data files, indexing them as geo_shape fields, and building multi-layer maps that combine different geographic features. By the end, you'll understand the workflow for working with custom GeoJSON data.

The tutorial creates a map showing airport locations, flight paths, and lightning detection zones, but these techniques apply to any GeoJSON vector data.

You'll learn to:

* Import GeoJSON files into Kibana
* Index the files in {{product.elasticsearch}}
* Display the data in a multi-layer map


## Before you begin [_before_you_begin]

This tutorial requires you to download the following GeoJSON sample data files. These files are good examples of the types of vector data that you can upload to Kibana and index in Elasticsearch for display in  Maps.

* [Logan International Airport](https://raw.githubusercontent.com/elastic/examples/master/Maps/Getting%20Started%20Examples/geojson_upload_and_styling/logan_international_airport.geojson)
* [Bangor International Airport](https://raw.githubusercontent.com/elastic/examples/master/Maps/Getting%20Started%20Examples/geojson_upload_and_styling/bangor_international_airport.geojson)
* [Lightning detected](https://raw.githubusercontent.com/elastic/examples/master/Maps/Getting%20Started%20Examples/geojson_upload_and_styling/lightning_detected.geojson)
* [Original flight path](https://raw.githubusercontent.com/elastic/examples/master/Maps/Getting%20Started%20Examples/geojson_upload_and_styling/original_flight_path.geojson)
* [Modified flight path](https://raw.githubusercontent.com/elastic/examples/master/Maps/Getting%20Started%20Examples/geojson_upload_and_styling/modified_flight_path.geojson)

The data represents two real airports, two fictitious flight routes, and fictitious lightning reports. You don’t need to use all of these files. Feel free to work with as many files as you’d like, or use valid GeoJSON files of your own.


## Create and set up a map [_create_and_set_up_a_map]

1. [Create a new map](maps-getting-started.md#maps-create).
2. Zoom in on the New England area in the northeast United States.

   You’re adding flight paths to this area, and this sets up the map for a good view of the data.

   :::{image} /explore-analyze/images/kibana-fu_gs_new_england_map.png
   :alt: fu gs new england map
   :screenshot:
   :::



## Upload and index GeoJSON files [upload-and-index-geojson-file]

For each GeoJSON file you downloaded, complete the following steps:

1. Click **Add layer**.
2. From the list of layer types, click **Upload file**.
3. Using the File Picker, upload the GeoJSON file.

    Depending on the geometry type of your features, this will auto-populate **Index type** with either [geo_point](elasticsearch://reference/elasticsearch/mapping-reference/geo-point.md) or [geo_shape](elasticsearch://reference/elasticsearch/mapping-reference/geo-shape.md) and **Index name** with `<file name>`.

4. Click **Import file**.

    You’ll see activity as the GeoJSON Upload utility creates a new index and data view for the data set. When the process is complete, you should receive messages that the creation of the new index and data view were successful.

5. Click **Add layer**.
6. In **Layer settings**, adjust settings and [properties](maps-vector-style-properties.md) as needed.
7. Click **Keep changes**.
8. Once you’ve added all of the sample files, [save your map](maps-getting-started.md#maps-save).

   At this point, you could consider the map complete, but there are a few additions and tweaks that you can make to tell a better story with your data.

   :::{image} /explore-analyze/images/kibana-fu_gs_flight_paths.png
   :alt: fu gs flight paths
   :screenshot:
   :::



## Add a heatmap aggregation layer [_add_a_heatmap_aggregation_layer]

Looking at the `Lightning detected` layer, it’s clear where lightning has struck. What’s less clear, is if there have been more lightning strikes in some areas than others, in other words, where the lightning hot spots are. An advantage of having indexed [geo_point](elasticsearch://reference/elasticsearch/mapping-reference/geo-point.md) data for the lightning strikes is that you can perform aggregations on the data.

1. Click **Add layer**.
2. From the list of layer types, click **Heat map**.

    Because you indexed `lightning_detected.geojson` using the index name and pattern `lightning_detected`, that data is available as a [geo_point](elasticsearch://reference/elasticsearch/mapping-reference/geo-point.md) aggregation.

3. Select `lightning_detected`.
4. Click **Add layer** to add the heat map layer "Lightning intensity".

    The remaining default settings are good, but there are a couple of settings that you might want to change.

5. Play around with the **Layer Style** > **Color range** setting.

    Again the default looks good, but feel free to choose a different color range.

6. When you’re finished modifying settings, click **Keep changes**.

   With your new lightning heat map layer, your map should look like this:

   :::{image} /explore-analyze/images/kibana-fu_gs_lightning_intensity.png
   :alt: fu gs lightning intensity
   :screenshot:
   :::



## Organize the layers [_organize_the_layers]

Consider ways you might improve the appearance of the final map. Small changes in how and when layers are shown can help tell a better story with your data. Here are a few final tweaks you might make:

* Update layer names
* Adjust styles for each layer
* Adjust the layer order
* Decide which layers to show at different zoom levels

When you’ve finished, again be sure to [save your work ](maps-getting-started.md#maps-save).

Your final map might look like this:

:::{image} /explore-analyze/images/kibana-fu_gs_final_map.png
:alt: fu gs final map
:screenshot:
:::

