---
navigation_title: Troubleshoot
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps-troubleshooting.html
description: Troubleshooting guide for Maps issues including Elasticsearch request inspection, polygon display problems, and layer configuration errors.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---



# Troubleshoot Maps [maps-troubleshooting]

When Maps displays unexpected results or encounters errors, inspecting {{product.elasticsearch}} requests and understanding common configuration issues helps identify root causes. The Maps inspector shows both vector tile and search API requests, revealing how layers query data and why certain features might not display.

This guide covers inspecting {{product.elasticsearch}} requests, troubleshooting missing or incorrect polygon displays, and resolving common layer configuration problems.


## Inspect Elasticsearch requests [_inspect_elasticsearch_requests]

Maps uses the [{{product.elasticsearch}} vector tile search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search-mvt) and the [{{product.elasticsearch}} search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) to get documents and aggregation results from {{product.elasticsearch}}. Use **Vector tiles** inspector to view {{product.elasticsearch}} vector tile search API requests. Use **Requests** inspector to view {{product.elasticsearch}} search API requests.

:::{image} /explore-analyze/images/kibana-vector_tile_inspector.png
:alt: vector tile inspector
:screenshot:
:::

:::{image} /explore-analyze/images/kibana-requests_inspector.png
:alt: requests inspector
:screenshot:
:::


## Solutions to common problems [_solutions_to_common_problems]


### Data view not listed when adding layer [_data_view_not_listed_when_adding_layer]

* Verify your geospatial data is correctly mapped as [geo_point](elasticsearch://reference/elasticsearch/mapping-reference/geo-point.md) or [geo_shape](elasticsearch://reference/elasticsearch/mapping-reference/geo-shape.md).

    * Run `GET myIndexName/_field_caps?fields=myGeoFieldName` in [Console](../../query-filter/tools/console.md), replacing `myIndexName` and `myGeoFieldName` with your index and geospatial field name.
    * Ensure response specifies `type` as `geo_point` or `geo_shape`.

* Verify your geospatial data is correctly mapped in your [data view](../../find-and-organize/data-views.md#managing-fields).

    * Open your data view in [Stack Management](../../../deploy-manage/index.md).
    * Ensure your geospatial field type is `geo_point` or `geo_shape`.
    * Ensure your geospatial field is searchable and aggregatable.
    * If your geospatial field type does not match your Elasticsearch mapping, click the **Refresh** button to refresh the field list from Elasticsearch.

* Data views with thousands of fields can exceed the default maximum payload size. Increase [`server.maxPayload`](kibana://reference/configuration-reference/general-settings.md) for large data views.


### Features are not displayed [_features_are_not_displayed]

* Use Inspector to view {{product.elasticsearch}} responses. Ensure the response is not empty.
* Ensure geometry uses the correct latitude and longitude ordering.

    * Geo-points expressed as strings are ordered as `"latitude,longitude"`. Geo-points expressed as arrays are ordered as the reverse: `[longitude, latitude]`.
    * Geo-shapes expressed as geojson provide coordinates as `[longitude, latitude]`.

* Ensure fill color and border color are distinguishable from map tiles. It’s hard to see white features on a white background.


### Elastic Maps Service basemaps are not displayed [_elastic_maps_service_basemaps_are_not_displayed]

**Maps** uses tile and vector data from Elastic Maps Service by default. See [Connect to Elastic Maps Service](maps-connect-to-ems.md) for more info.


### Custom tiles are not displayed [_custom_tiles_are_not_displayed]

* When using a custom tile service, ensure your tile server has configured [Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) so tile requests from your {{product.kibana}} domain have permission to access your tile server domain.
* Ensure custom vector and tile services have the required coordinate system. Vector data must use EPSG:4326 and tiles must use EPSG:3857.

