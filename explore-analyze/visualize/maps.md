---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps.html
  - https://www.elastic.co/guide/en/serverless/current/maps.html
  - https://www.elastic.co/guide/en/kibana/current/maps-visualizations.html
description: Create geospatial visualizations in Kibana Maps with multi-layer mapping, animations, and GeoJSON uploads. Visualize location data with custom styling and dashboard embedding.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
---

# Maps [maps]

Maps visualizes geospatial data from {{es}} indices, uploaded files, or external sources. You can combine multiple data layers, animate temporal changes, apply custom styling based on data values, and embed maps in dashboards alongside other visualizations.

Maps supports various data sources including {{es}} documents with geo fields, GeoJSON files, shapefiles, tile services, and web mapping services. Use Maps to display location data, analyze spatial patterns, track assets in real time, or create choropleth visualizations.

## Build maps with multiple layers and indices [_build_maps_with_multiple_layers_and_indices]

Use multiple layers and indices to show all your data in a single map. Show how data sits relative to physical features like weather patterns, human-made features like international borders, and business-specific features like sales regions. Plot individual documents or use aggregations to plot any data set, no matter how large.

:::{image} /explore-analyze/images/kibana-sample_data_ecommerce.png
:alt: sample data ecommerce
:screenshot:
:::

To learn about specific types of layers, check out [Heat map layer](../../explore-analyze/visualize/maps/heatmap-layer.md), [Tile layer](../../explore-analyze/visualize/maps/tile-layer.md), and [Vector layer](../../explore-analyze/visualize/maps/vector-layer.md).


## Animate spatial temporal data [_animate_spatial_temporal_data]

Data comes to life with animation. Hard to detect patterns in static data pop out with movement. Use time slider to animate your data and gain deeper insights.

This animated map uses the time slider to show Portland buses over a period of 15 minutes. The routes come alive as the bus locations update with time.

:::{image} /explore-analyze/images/kibana-timeslider.gif
:alt: timeslider
:screenshot:
:::

To create this type of map, check out [Track, visualize, and alert assets in real time](../../explore-analyze/visualize/maps/asset-tracking-tutorial.md).

## Upload GeoJSON files and shapefiles [_upload_geojson_files_and_shapefiles]

Use **Maps** to drag and drop your GeoJSON and shapefile data into Elasticsearch, and then use them as layers in your map.


## Embed your map in dashboards [_embed_your_map_in_dashboards]

Viewing data from different angles provides better insights. Dimensions that are obscured in one visualization might be illuminated in another. Add your map to a [Dashboard](../../explore-analyze/dashboards.md) and view your geospatial data alongside bar charts, pie charts, tag clouds, and more.

This choropleth map shows the density of non-emergency service requests in San Diego by council district. The map is embedded in a dashboard, so users can better understand when services are requested and gain insight into the top requested services.

:::{image} /explore-analyze/images/kibana-embed_in_dashboard.jpeg
:alt: embed in dashboard
:screenshot:
:::


## Symbolize features using data values [_symbolize_features_using_data_values]

Customize each layer to highlight meaningful dimensions in your data. For example, use dark colors to symbolize areas with more web log traffic, and lighter colors to symbolize areas with less traffic.


## Focus on only the data that’s important to you [_focus_on_only_the_data_thats_important_to_you]

Search across the layers in your map to focus on just the data you want. Combine free text search with field-based search using the [{{kib}} Query Language](../../explore-analyze/query-filter/languages/kql.md). Set the time filter to restrict layers by time. Draw a polygon on the map or use the shape from features to create spatial filters. Filter individual layers to compares facets.

Check out [Search geographic data](../../explore-analyze/visualize/maps/maps-search.md).
