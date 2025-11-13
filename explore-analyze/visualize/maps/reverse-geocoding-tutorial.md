---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/reverse-geocoding-tutorial.html
description: Step-by-step tutorial for converting coordinates to human-readable location names with reverse geocoding. Enrich geospatial data with place names and addresses.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Map custom regions with reverse geocoding [reverse-geocoding-tutorial]

In this tutorial, you'll learn how to map custom geographic regions when your data contains coordinates but not region identifiers. You'll explore uploading custom region boundaries, using {{es}} enrich processors for reverse geocoding, and visualizing metrics by region. By the end, you'll understand how to assign region identifiers to data based on geographic location.

Reverse geocoding converts coordinates into region identifiers by determining which region boundary contains each point. This tutorial demonstrates the technique using US Census Bureau Combined Statistical Areas, but it applies to any custom regional boundaries.

In this tutorial, you’ll use reverse geocoding to visualize United States Census Bureau Combined Statistical Area (CSA) regions by web traffic.

You’ll learn to:

* Upload custom regions.
* Reverse geocode with the {{es}} [enrich processor](elasticsearch://reference/enrich-processor/enrich-processor.md).
* Create a map and visualize CSA regions by web traffic.

When you complete this tutorial, you’ll have a map that looks like this:

:::{image} /explore-analyze/images/kibana-csa_regions_by_web_traffic.png
:alt: Map showing custom regions
:screenshot:
:::


## Step 1: Index web traffic data [_step_1_index_web_traffic_data]

GeoIP is a common way of transforming an IP address to a longitude and latitude. GeoIP is roughly accurate on the city level globally and neighborhood level in selected countries. It’s not as good as an actual GPS location from your phone, but it’s much more precise than just a country, state, or province.

You’ll use the [web logs sample data set](../../index.md#gs-get-data-into-kibana) that comes with Kibana for this tutorial. Web logs sample data set has longitude and latitude. If your web log data does not contain longitude and latitude, use [GeoIP processor](elasticsearch://reference/enrich-processor/geoip-processor.md) to transform an IP address into a [geo_point](elasticsearch://reference/elasticsearch/mapping-reference/geo-point.md) field.


## Step 2: Index Combined Statistical Area (CSA) regions [_step_2_index_combined_statistical_area_csa_regions]

GeoIP level of detail is very useful for driving decision-making. For example, say you want to spin up a marketing campaign based on the locations of your users or show executive stakeholders which metro areas are experiencing an uptick of traffic.

That kind of scale in the United States is often captured with what the Census Bureau calls the Combined Statistical Area (CSA). CSA is roughly equivalent with how people intuitively think of which urban area they live in. It does not necessarily coincide with state or city boundaries.

CSAs generally share the same telecom providers and ad networks. New fast food franchises expand to a CSA rather than a particular city or municipality. Basically, people in the same CSA shop in the same IKEA.

To get the CSA boundary data:

1. Go to the [Census Bureau’s website](https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html) and download the `cb_2018_us_csa_500k.zip` file.
2. Uncompress the zip file.
3. In Kibana, go to **Maps**.
4. Click **Create map**.
5. Click **Add layer**.
6. Click **Upload file**.
7. Use the file chooser to select the `.shp` file from the CSA shapefile folder.
8. Use the `.dbf` file chooser to select the `.dbf` file from the CSA shapefile folder.
9. Use the `.prj` file chooser to select the `.prj` file from the CSA shapefile folder.
10. Use the `.shx` file chooser to select the `.shx` file from the CSA shapefile folder.
11. Set index name to **csa** and click **Import file**.
12. When importing is complete, click **Add as document layer**.
13. Add Tooltip fields:

    1. Click **+ Add** to open the field select.
    2. Select **NAME**, **GEOID**, and **AFFGEOID**.
    3. Click **Add**.

14. Click **Keep changes**.

Looking at the map, you get a sense of what constitutes a metro area in the eyes of the Census Bureau.

:::{image} /explore-analyze/images/kibana-csa_regions.png
:alt: Map showing metro area
:screenshot:
:::


## Step 3: Reverse geocoding [_step_3_reverse_geocoding]

To visualize CSA regions by web log traffic, the web log traffic must contain a CSA region identifier. You’ll use {{es}} [enrich processor](elasticsearch://reference/enrich-processor/enrich-processor.md) to add CSA region identifiers to the web logs sample data set. You can skip this step if your source data already contains region identifiers.

1. Go to **Developer tools** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In **Console**, create a [geo_match enrichment policy](../../../manage-data/ingest/transform-enrich/example-enrich-data-based-on-geolocation.md):

    ```js
    PUT /_enrich/policy/csa_lookup
    {
      "geo_match": {
        "indices": "csa",
        "match_field": "geometry",
        "enrich_fields": [ "GEOID", "NAME"]
      }
    }
    ```

3. To initialize the policy, run:

    ```js
    POST /_enrich/policy/csa_lookup/_execute
    ```

4. To create a ingest pipeline, run:

    ```js
    PUT _ingest/pipeline/lonlat-to-csa
    {
      "description": "Reverse geocode longitude-latitude to combined statistical area",
      "processors": [
        {
          "enrich": {
            "field": "geo.coordinates",
            "policy_name": "csa_lookup",
            "target_field": "csa",
            "ignore_missing": true,
            "ignore_failure": true,
            "description": "Lookup the csa identifier"
          }
        },
        {
          "remove": {
            "field": "csa.geometry",
            "ignore_missing": true,
            "ignore_failure": true,
            "description": "Remove the shape field"
          }
        }
      ]
    }
    ```

5. To update your existing data, run:

    ```js
    POST kibana_sample_data_logs/_update_by_query?pipeline=lonlat-to-csa
    ```

6. To run the pipeline on new documents at ingest, run:

    ```js
    PUT kibana_sample_data_logs/_settings
    {
      "index": {
        "default_pipeline": "lonlat-to-csa"
      }
    }
    ```

7. Go to **Discover**.
8. Set the data view to **Kibana Sample Data Logs**.
9. Open the [time filter](../../query-filter/filtering.md), and set the time range to the last 30 days.
10. Scan through the list of **Available fields** until you find the `csa.GEOID` field. You can also search for the field by name.
11. Click ![Add icon](/explore-analyze/images/kibana-add-icon.png "") to toggle the field into the document table.
12. Find the *csa.NAME* field and add it to your document table.

Your web log data now contains `csa.GEOID` and `csa.NAME` fields from the matching **csa** region. Web log traffic not contained in a CSA region does not have values for `csa.GEOID` and `csa.NAME` fields.

:::{image} /explore-analyze/images/kibana-discover_enriched_web_log.png
:alt: View of data in Discover
:screenshot:
:::


## Step 4: Visualize Combined Statistical Area (CSA) regions by web traffic [_step_4_visualize_combined_statistical_area_csa_regions_by_web_traffic]

Now that our web traffic contains CSA region identifiers, you’ll visualize CSA regions by web traffic.

1. Go to **Maps**.
2. Click **Create map**.
3. Click **Add layer**.
4. Click **Choropleth**.
5. For **Boundaries source**:

    1. Select **Points, lines, and polygons from Elasticsearch**.
    2. Set **Data view** to **csa**.
    3. Set **Join field** to **GEOID**.

6. For **Statistics source**:

    1. Set **Data view** to **Kibana Sample Data Logs**.
    2. Set **Join field** to **csa.GEOID.keyword**.

7. Click **Add and continue**.
8. Scroll to **Layer Style** and Set **Label** to **Fixed**.
9. Click **Keep changes**.
10. **Save** the map.

    1. Give the map a title.
    2. Under **Add to dashboard**, select **None**.
    3. Click **Save and add to library**.


:::{image} /explore-analyze/images/kibana-csa_regions_by_web_traffic.png
:alt: Final map showing custom regions
:screenshot:
:::

Congratulations! You have completed the tutorial and have the recipe for visualizing custom regions. You can now try replicating this same analysis with your own data.

