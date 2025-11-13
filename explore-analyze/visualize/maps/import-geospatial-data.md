---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/import-geospatial-data.html
description: Import geospatial data into Elasticsearch as geo_point or geo_shape. Upload GeoJSON files, shapefiles, or use coordinate pairs for map visualization.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Import geospatial data [import-geospatial-data]

Before visualizing geospatial data in Maps, you must index it in {{es}} as geo_point or geo_shape fields. The import method depends on your data format: you can upload GeoJSON files or shapefiles directly through the Maps interface, use the {{data-viz}} for delimited files with coordinate pairs, or programmatically index data using {{es}} APIs or {{product.logstash}}.

This guide covers import options for different geospatial data formats, required permissions, and best practices for indexing location data.


## Security privileges [import-geospatial-privileges]

The {{stack-security-features}} provide roles and privileges that control which users can upload files. You can manage your roles, privileges, and spaces in **{{stack-manage-app}}** in {{kib}}. For more information, see [Security privileges](elasticsearch://reference/elasticsearch/security-privileges.md), [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md), and [{{kib}} role management](../../../deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).

To upload GeoJSON files, shapefiles, and draw features in {{kib}} with **Maps**, you must have:

* The `all` {{kib}} privilege for **Maps**
* The `all` {{kib}} privilege for **{{ipm-app}}**
* The `create` and `create_index` index privileges for destination indices
* To use the index in **Maps**, you must also have the `read` and `view_index_metadata` index privileges for destination indices

To upload delimited files (such as CSV, TSV, or JSON files) from the **Upload file** integration, you must also have:

* The `all` {{kib}} privilege for **Discover**
* The `manage_pipeline` or `manage_ingest_pipelines` cluster privilege
* The `manage` index privilege for destination indices


## Upload delimited files with latitude and longitude columns [_upload_delimited_files_with_latitude_and_longitude_columns]

You can upload a file and import it into an {{es}} index with latitude and longitude columns combined into a `geo_point` field.

1. Go to the **Integrations** page and select **Upload file**.
2. Select a file in one of the supported file formats.
3. Click **Import**.
4. Select the **Advanced** tab.
5. Set **Index name**.
6. If a combined `geo_point` field is not created automatically, click **Add combined field**, then click **Add geo point field**.
7. Fill out the form and click **Add**.
8. Click **Import**.


## Upload a GeoJSON file [_upload_a_geojson_file]

**Upload file** indexes GeoJSON features in {{es}}, creating a document for each feature.

::::{note}
GeoJSON feature coordinates must be in EPSG:4326 coordinate reference system..
::::


1. [Create a new map](maps-getting-started.md#maps-create).
2. Click **Add layer**.
3. Select **Upload file**.
4. Use the file chooser to select a GeoJSON file with the extension `.json` or `.geojson`.
5. Click **Import file**.


## Upload a shapefile [_upload_a_shapefile]

**Upload file** indexes shapefile features in {{es}}, creating a document for each feature.

1. [Create a new map](maps-getting-started.md#maps-create).
2. Click **Add layer**.
3. Select **Upload file**.
4. Use the file chooser to select the `.shp` file from your shapefile folder.
5. Use the `.dbf` file chooser to select the `.dbf` file from your shapefile folder.
6. Use the `.prj` file chooser to select the `.prj` file from your shapefile folder.
7. Use the `.shx` file chooser to select the `.shx` file from your shapefile folder.
8. Click **Import file**.


## Draw features in a map [_draw_features_in_a_map]

Upload features into {{es}} by drawing lines, polygons, circles, bounding boxes, and points in a map.

To create a new index for drawing:

1. [Create a map](maps-getting-started.md#maps-create).
2. Click **Add layer**.
3. Select **Create index**.
4. Set **Index name**.
5. Click **Create index**.

To open an existing index for drawing:

1. [Create a map](maps-getting-started.md#maps-create).
2. Click **Add layer**.
3. Select **Documents**.
4. Select the data view that points to your index. A [data view](../../find-and-organize/data-views.md) can point to one or more indices. For feature editing, the data view must point to a single index.
5. Click **Add and close**.
6. In the legend, click the layer name and select **Edit features**.

When feature editing is open, a feature editing toolbox is displayed on the left side of the map.

:::{image} /explore-analyze/images/kibana-drawing_layer.png
:alt: drawing layer
:screenshot:
:::

To draw features:

1. Click on the line, polygon, circle, bounding box, or point icon.
2. Move the mouse cursor over the map and follow the on screen instructions to draw a feature.

    When a feature is complete, the feature is added to the index as a new document.

3. Repeat to draw additional features.
4. When you are finished adding features, go to the legend, and click **Exit** under the layer name.


## Upload data with IP addresses [_upload_data_with_ip_addresses]

The GeoIP processor adds information about the geographical location of IP addresses. See [GeoIP processor](elasticsearch://reference/enrich-processor/geoip-processor.md) for details. For private IP addresses, see [Enriching data with GeoIPs from internal, private IP addresses](https://www.elastic.co/blog/enriching-elasticsearch-data-geo-ips-internal-private-ip-addresses).


## Upload data with GDAL [_upload_data_with_gdal]

[GDAL](https://www.gdal.org/) (Geospatial Data Abstraction Library) contains command line tools that can convert geospatial data between 75 different geospatial file formats and index that geospatial data into {{es}}. See [Ingest geospatial data into Elasticsearch with GDAL](https://www.elastic.co/blog/how-to-ingest-geospatial-data-into-elasticsearch-with-gdal) for details.
