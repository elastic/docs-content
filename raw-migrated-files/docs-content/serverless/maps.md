# {{maps-app}} [maps]

This content applies to: [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md)

In **{{project-settings}} → {{maps-app}}** you can:

* Build maps with multiple layers and indices.
* Animate spatial temporal data.
* Upload GeoJSON files and shapefiles.
* Embed your map in dashboards.
* Focus on only the data that’s important to you.


## Build maps with multiple layers and indices [maps-build-maps-with-multiple-layers-and-indices]

Use multiple layers and indices to show all your data in a single map. Show how data sits relative to physical features like weather patterns, human-made features like international borders, and business-specific features like sales regions. Plot individual documents or use aggregations to plot any data set, no matter how large.

:::{image} ../../../images/serverless-sample_data_ecommerce_map.png
:alt: A world map with country and revenue layers
:class: screenshot
:::

Go to **{{project-settings}} → {{maps-app}}** and click **Add layer**. To learn about specific types of layers, check out [Heat map layer](../../../explore-analyze/visualize/maps/heatmap-layer.md), [Tile layer](../../../explore-analyze/visualize/maps/tile-layer.md), and [Vector layer](../../../explore-analyze/visualize/maps/vector-layer.md).


## Animate spatial temporal data [maps-animate-spatial-temporal-data]

Data comes to life with animation. Hard to detect patterns in static data pop out with movement. Use time slider to animate your data and gain deeper insights.

This animated map uses the time slider to show Portland buses over a period of 15 minutes. The routes come alive as the bus locations update with time.

:::{image} ../../../images/serverless-timeslider_map.gif
:alt: An animated city map of Portland with changing bus locations
:class: screenshot
:::

To create this type of map, check out [Track, visualize, and alert assets in real time](../../../explore-analyze/visualize/maps/asset-tracking-tutorial.md).


## Upload GeoJSON files and shapefiles [maps-upload-geojson-files-and-shapefiles]

Use **{{maps-app}}** to drag and drop your GeoJSON and shapefile data and then use them as layers in your map. Check out [Import geospatial data](../../../explore-analyze/visualize/maps/import-geospatial-data.md).


## Embed your map in dashboards [maps-embed-your-map-in-dashboards]

Viewing data from different angles provides better insights. Dimensions that are obscured in one visualization might be illuminated in another. Add your map to a [Dashboard](../../../explore-analyze/dashboards.md) and view your geospatial data alongside bar charts, pie charts, tag clouds, and more.

This choropleth map shows the density of non-emergency service requests in San Diego by council district. The map is embedded in a dashboard, so users can better understand when services are requested and gain insight into the top requested services.

:::{image} ../../../images/serverless-embed_dashboard_map.jpeg
:alt: A dashboard with a map
:class: screenshot
:::

For a detailed example, check out [Build a map to compare metrics by country or region](../../../explore-analyze/visualize/maps/maps-getting-started.md).


## Focus on only the data that’s important to you [maps-focus-on-only-the-data-thats-important-to-you]

Search across the layers in your map to focus on just the data you want. Combine free text search with field-based search using the {{kib}} Query Language (KQL) Set the time filter to restrict layers by time. Draw a polygon on the map or use the shape from features to create spatial filters. Filter individual layers to compares facets.

Check out [Search geographic data](../../../explore-analyze/visualize/maps/maps-search.md).
