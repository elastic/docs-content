---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/conf-map-ui.html
  - https://www.elastic.co/guide/en/serverless/current/security-conf-map-ui.html
---

# Configure network map data


Depending on your {{kib}} setup, to display and interact with data on the **Network** page’s map you might need to:

* [Create {{kib}} data views](/solutions/security/explore/configure-network-map-data.md#kibana-index-pattern)
* [Add geographical IP data to events](/solutions/security/explore/configure-network-map-data.md#geoip-data)
* [Map your internal network](/solutions/security/explore/configure-network-map-data.md#private-network)

::::{note}
To see source and destination connections lines on the map, you must configure `source.geo` and `destination.geo` ECS fields for your indices.
::::



## Permissions required [prereq-perms]

To view the map in {{stack}}, you need a role with at least `Read` [privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md#adding_kibana_privileges) for the `Maps` feature. In serverless, you need the appropriate [predefined user role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles) or a [custom role](/deploy-manage/users-roles/cloud-organization/user-roles.md) with at least `Read` privileges for the `Maps` feature.


## Create {{kib}} data views [kibana-index-pattern]

To display map data, you must define a {{kib}} [data view](/explore-analyze/find-and-organize/data-views.md) that includes one or more of the indices specified in the `securitysolution:defaultIndex` field. To view those indices, find **Stack Management** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Advanced Settings** → **`securitysolution:defaultIndex`**.

For example, to display data that is stored in indices matching the index pattern `servers-europe-*` on the map, you must use a {{kib}} data view whose index pattern matches `servers-europe-*`, such as `servers-*`.


## Add geoIP data [geoip-data]

When the ECS [source.geo.location and destination.geo.location](https://www.elastic.co/guide/en/ecs/current/ecs-geo.html) fields are mapped, network data is displayed on the map.

If you use Beats, configure a geoIP processor to add data to the relevant fields:

1. Define an ingest node pipeline that uses one or more `geoIP` processors to add location information to events. For example, use the Console in {{kib}} to create the following pipeline:

    ```console
    PUT _ingest/pipeline/geoip-info
    {
      "description": "Add geoip info",
      "processors": [
        {
          "geoip": {
            "field": "client.ip",
            "target_field": "client.geo",
            "ignore_missing": true
          }
        },
        {
          "geoip": {
            "field": "source.ip",
            "target_field": "source.geo",
            "ignore_missing": true
          }
        },
        {
          "geoip": {
            "field": "destination.ip",
            "target_field": "destination.geo",
            "ignore_missing": true
          }
        },
        {
          "geoip": {
            "field": "server.ip",
            "target_field": "server.geo",
            "ignore_missing": true
          }
        },
        {
          "geoip": {
            "field": "host.ip",
            "target_field": "host.geo",
            "ignore_missing": true
          }
        }
      ]
    }
    ```

    In this example, the pipeline ID is `geoip-info`. `field` specifies the field that contains the IP address to use for the geographical lookup, and `target_field` is the field that will hold the geographical information. `"ignore_missing": true` configures the pipeline to continue processing when it encounters an event that doesn’t have the specified field.

    ::::{tip}
    An example ingest pipeline that uses the GeoLite2-ASN.mmdb database to add autonomous system number (ASN) fields can be found [here](https://github.com/elastic/examples/blob/master/Security%20Analytics/SIEM-examples/Packetbeat/geoip-info.json).
    ::::

2. In your Beats configuration files, add the pipeline to the `output.elasticsearch` tag:

    ```yaml
      output.elasticsearch:
        hosts: ["localhost:9200"]
        pipeline: geoip-info <1>
    ```

    1. The value of this field must be the same as the ingest pipeline name in step 1 (`geoip-info` in this example).



## Map your internal network [private-network]

If you want to add your network’s internal IP addresses to the map, define geo location fields under the `processors` tag in the Beats configuration files on your hosts:

```yaml
  processors:
   - add_host_metadata:
   - add_cloud_metadata: ~
   - add_fields:
       when.network.source.ip: <private/IP address> <1>
       fields:
         source.geo.location:
           lat: <latitude coordinate>
           lon: <longitude coordinate>
       target: ''
   - add_fields:
       when.network.destination.ip: <private/IP address>
       fields:
         destination.geo.location:
           lat: <latitude coordinate>
           lon: <longitude coordinate>
       target: ''
```

1. For the IP address, you can use either `private` or CIDR notation.


::::{tip}
You can also enrich your data with other [host fields](https://www.elastic.co/guide/en/beats/packetbeat/current/add-host-metadata.html).
::::
