---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/asset-tracking-tutorial.html
description: Step-by-step tutorial for tracking real-time asset locations with Maps. Visualize transit data, create alerts for geofences, and monitor vehicle movements.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Track, visualize, and alert on assets in real time [asset-tracking-tutorial]

Are you interested in asset tracking? Good news! Visualizing and analyzing data that moves is easy with **Maps**. You can track the location of an IoT device and monitor a package or vehicle in transit.

In this tutorial, you’ll look at live urban transit data from the city of Portland, Oregon. You’ll watch the city buses, tram, and trains, use the data to visualize congestion, and notify a dispatch team when a vehicle enters a construction zone.

You’ll learn to:

* Use {{agent}} to ingest the [TriMet REST API](https://developer.trimet.org/ws_docs/) into {{es}}.
* Create a map with layers that visualize asset tracks and last-known locations.
* Use symbols and colors to style data values and show which direction an asset is heading.
* Set up tracking containment alerts to monitor moving vehicles.
* Display those alerts on a map.

When you complete this tutorial, you’ll have a map that looks like this:

:::{image} /explore-analyze/images/kibana-construction_zones.png
:alt: construction zones
:screenshot:
:::


## Prerequisites [_prerequisites_3]

* If you don’t already have {{kib}}, sign up for [a free Elastic Cloud trial](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs) and create a hosted deployment. When creating it, download the deployment credentials.
* Obtain an API key for [TriMet web services](https://developer.trimet.org/) at [https://developer.trimet.org/appid/registration/](https://developer.trimet.org/appid/registration/).
* [Fleet](/reference/fleet/index.md) is enabled on your cluster, and one or more [{{agent}}s](/reference/fleet/install-elastic-agents.md) is enrolled.


## Part 1: Ingest the Portland public transport data [_part_1_ingest_the_portland_public_transport_data]

To get to the fun of visualizing and alerting on Portland public transport vehicles, you must first add the **Custom API** integration to an Elastic Agent policy to get the TriMet Portland data into {{es}}.


### Step 1: Set up an Elasticsearch index [_step_1_set_up_an_elasticsearch_index]

1. In Kibana, go to **Developer tools** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In **Console**, create the `tri_met_tracks` index lifecyle policy. This policy will keep the events in the hot data phase for 7 days. The data then moves to the warm phase. After 365 days in the warm phase, the data is deleted.

   ::::{dropdown} ILM policy definition
   ```js
   PUT _ilm/policy/tri_met_tracks
   {
    "policy": {
      "phases": {
        "hot": {
          "min_age": "0ms",
          "actions": {
            "rollover": {
              "max_primary_shard_size": "50gb",
              "max_age": "7d"
            },
            "set_priority": {
              "priority": 100
            }
          }
        },
        "warm": {
          "min_age": "0d",
          "actions": {
            "set_priority": {
              "priority": 50
            }
          }
        },
        "delete": {
          "min_age": "365d",
          "actions": {
            "delete": {
              "delete_searchable_snapshot": true
            }
          }
        }
      }
    }
   }
   ```

   ::::

3. In **Console**, add the `tri_met_tracks_for_elastic_agent` ingest pipeline.

   ::::{dropdown} Ingest policy definition
   ```js
   PUT _ingest/pipeline/tri_met_tracks_for_elastic_agent
   {
    "processors": [
      {
        "set": {
          "field": "trimet.inCongestion",
          "value": "false",
          "if": "ctx?.trimet?.inCongestion == null"
        }
      },
      {
        "convert": {
          "field": "trimet.bearing",
          "type": "float"
        }
      },
      {
        "convert": {
          "field": "trimet.inCongestion",
          "type": "boolean"
        }
      },
      {
        "script": {
          "source": """
            double lat=Math.round(ctx['trimet']['latitude']*1e6)/1e6;
            double lon=Math.round(ctx['trimet']['longitude']*1e6)/1e6;
            ctx['trimet']['location'] = lat + "," + lon
            """,
          "description": "Generate the geometry rounding to six decimals"
        }
      },
      {
        "script": {
          "source": """ctx['_id'] = ctx['trimet']['vehicleID'] + "_" + ctx['trimet']['time']""",
          "description": "Generate documentID"
        }
      },
      {
        "remove": {
          "field": [
            "message",
            "input",
            "agent",
            "ecs",
            "host",
            "event",
            "trimet.longitude",
            "trimet.latitude"
          ]
        }
      }
    ]
   }
   ```

   ::::

4. In **Console**, create the component and index template, which is configured to use datastreams and the previous ILM policy and ingest pipeline:

   ::::{dropdown} Index component template
   ```js
   PUT _component_template/logs-httpjson.trimet@package
   {
    "template": {
      "settings": {
        "index": {
          "lifecycle": {
            "name": "tri_met_tracks"
          },
          "codec": "best_compression",
          "default_pipeline": "tri_met_tracks_for_elastic_agent"
        }
      },
      "mappings": {
        "_routing": {
          "required": false
        },
        "numeric_detection": false,
        "dynamic_date_formats": [
          "strict_date_optional_time",
          "yyyy/MM/dd HH:mm:ss Z||yyyy/MM/dd Z"
        ],
        "dynamic": true,
        "_source": {
          "excludes": [],
          "includes": [],
          "enabled": true
        },
        "dynamic_templates": [],
        "date_detection": true,
        "properties": {
          "input": {
            "properties": {
              "type": {
                "ignore_above": 1024,
                "type": "keyword"
              }
            }
          },
          "@timestamp": {
            "ignore_malformed": false,
            "type": "date"
          },
          "ecs": {
            "properties": {
              "version": {
                "ignore_above": 1024,
                "type": "keyword"
              }
            }
          },
          "data_stream": {
            "properties": {
              "namespace": {
                "type": "constant_keyword"
              },
              "type": {
                "type": "constant_keyword"
              },
              "dataset": {
                "type": "constant_keyword"
              }
            }
          },
          "event": {
            "properties": {
              "created": {
                "type": "date"
              },
              "module": {
                "type": "constant_keyword",
                "value": "httpjson"
              },
              "dataset": {
                "type": "constant_keyword",
                "value": "httpjson.trimet"
              }
            }
          },
          "message": {
            "type": "match_only_text"
          },
          "tags": {
            "ignore_above": 1024,
            "type": "keyword"
          },
          "trimet": {
            "type": "object",
            "properties": {
              "expires": {
                "type": "date"
              },
              "signMessage": {
                "type": "text"
              },
              "serviceDate": {
                "type": "date"
              },
              "loadPercentage": {
                "type": "float"
              },
              "nextStopSeq": {
                "type": "integer"
              },
              "source": {
                "type": "keyword"
              },
              "type": {
                "type": "keyword"
              },
              "blockID": {
                "type": "integer"
              },
              "signMessageLong": {
                "type": "text"
              },
              "lastLocID": {
                "type": "keyword"
              },
              "nextLocID": {
                "type": "keyword"
              },
              "locationInScheduleDay": {
                "type": "integer"
              },
              "newTrip": {
                "type": "boolean"
              },
              "direction": {
                "type": "integer"
              },
              "inCongestion": {
                "type": "boolean"
              },
              "routeNumber": {
                "type": "integer"
              },
              "bearing": {
                "type": "integer"
              },
              "garage": {
                "type": "keyword"
              },
              "tripID": {
                "type": "keyword"
              },
              "delay": {
                "type": "integer"
              },
              "extraBlockID": {
                "type": "keyword"
              },
              "messageCode": {
                "type": "integer"
              },
              "lastStopSeq": {
                "type": "integer"
              },
              "location": {
                "type": "geo_point"
              },
              "time": {
                "index": true,
                "ignore_malformed": false,
                "store": false,
                "type": "date",
                "doc_values": true
              },
              "vehicleID": {
                "type": "keyword"
              },
              "offRoute": {
                "type": "boolean"
              }
            }
          }
        }
      }
    }
   }
   ```

   ::::


   ::::{dropdown} Index template
   ```js
   PUT _index_template/logs-httpjson.trimet
   {
    "index_patterns": [
      "logs-httpjson.trimet-*"
    ],
    "composed_of": [
      "logs-httpjson.trimet@package",
      ".fleet_globals-1",
      ".fleet_agent_id_verification-1"
    ],
    "priority": 200,
    "data_stream": {
      "hidden": false,
      "allow_custom_routing": false
    }
   }
   ```

   ::::



### Step 2: Configure {{agent}} [_step_2_configure_agent]

:::::::{tab-set}

::::::{tab-item} Existing agent policy
If you already have an agent policy, get its identifier from the `View policy` action fly out

:::{image} /explore-analyze/images/kibana-agent-policy-id.png
:alt: agent policy id
:screenshot:
:::

:::{image} /explore-analyze/images/kibana-policy_id.png
:alt: policy id
:screenshot:
:::
::::::

::::::{tab-item} Create a new agent policy
If you don’t have yet an agent policy ready:

1. Still in the **Console**, create an agent policy for this data source

    ```js
    POST kbn:/api/fleet/agent_policies?sys_monitoring=true
    {
     "name": "trimet",
     "description": "Policy to gather TriMet data",
     "namespace": "default",
     "monitoring_enabled": ["logs", "metrics"],
     "inactivity_timeout": 1209600,
     "is_protected": false
    }
    ```

2. Note the `item.id` value of the request result, it will be used later when registering your integration
3. Enroll a new {{agent}} into this new policy using any of the methods provided by the UI (linux, Mac, Windows, etc.)
::::::

:::::::
Execute the following request from the **Console** to install a new Custom API integration. Put the corresponding values for the `policy_id` and `tri_met_app_id`.

::::{dropdown} Create a new Custom API integration
```js
POST kbn:/api/fleet/package_policies
{
 "policy_id": "<policy_id>", <1>
 "package": {
   "name": "httpjson",
   "version": "1.18.0"
 },
 "name": "httpjson-trimet",
 "description": "TriMet data upload",
 "namespace": "default",
 "inputs": {
   "generic-httpjson": {
     "enabled": true,
     "streams": {
       "httpjson.generic": {
         "enabled": true,
         "vars": {
           "data_stream.dataset": "httpjson.trimet",
           "request_url": "https://developer.trimet.org/ws/v2/vehicles?appID=<tri_met_app_id>", <2>
           "request_interval": "1m", <3>
           "request_method": "GET",
           "response_split": "target: body.resultSet.vehicle",
           "request_redirect_headers_ban_list": [],
           "oauth_scopes": [],
           "processors": "- decode_json_fields:\n    fields: [\"message\"]\n    target: \"trimet\"\n",
           "tags": [
             "trimet"
             ]
         }
       }
     }
   }
 }
}
```

1. Agent policy identifier
2. TriMet application identifier
3. Retrieve vehicle positions every minute


::::


This request will configure the integration to make requests to the TriMet REST API every minute, splitting the API response into one message per vehicle into the `httpjson.trimet` data stream, and encoding the vehicle’s data into the `trimet` field. The rest of the data management will be handled by the ingest policy defined in the first step.


### Step 3: Create a data view for the tri_met_tracks {{es}} index [_step_3_create_a_data_view_for_the_tri_met_tracks_es_index]

In **Console** execute this request to create a new {{kib}} Data View called TriMet Positions:

```js
POST kbn:/api/data_views/data_view
{
 "data_view": {
    "title": "logs-httpjson.trimet-*",
    "name": "TriMet Positions",
    "timeFieldName": "trimet.time"
 }
}
```

{{kib}} shows the fields in your data view.

:::{image} /explore-analyze/images/kibana-data_view.png
:alt: data view
:screenshot:
:::

::::{tip}
You may want to tweak this Data View to adjust the field names and number or date formatting to your personal preferences. These settings are honored by the Maps application in the tooltips and other UI elements. Check [Format data fields](../../find-and-organize/data-views.md#managing-fields) for more details.
::::



### Step 4: Explore the Portland TriMet data [_step_4_explore_the_portland_trimet_data]

1. Go to **Discover**.
2. Set the data view to **TriMet Positions**.
3. Open the [time filter](../../query-filter/filtering.md), and set the time range to the last 15 minutes.
4. Expand a document and explore some of the fields that you will use later in this tutorial: `trimet.bearing`, `trimet.inCongestion`, `trimet.location`, and `trimet.vehicleID`.

:::{image} /explore-analyze/images/kibana-discover.png
:alt: discover
:screenshot:
:::


## Part 2: Build an operational map [_part_2_build_an_operational_map]

It’s hard to get an overview of Portland vehicles by looking at individual events. Let’s create a map to show the routes and current location for each vehicle, along with the direction they are heading.


### Step 1: Create your map [_step_1_create_your_map]

Create your map and set the theme for the default layer to dark mode.

1. Go to **Maps**.
2. Click **Create map**.
3. In the **Layers** list, click **Road map**, and then click **Edit layer settings**.
4. Open the **Tile service** dropdown, and select **Road map - dark**.
5. Click **Keep changes**.


### Step 2. Add a tracks layer [_step_2_add_a_tracks_layer]

Add a layer to show the vehicle routes for the last 15 minutes.

1. Click **Add layer**.
2. Click **Tracks**.
3. Select the **TriMet Positions** data view.
4. Define the tracks:

    1. Set **Entity** to `trimet.vehicleID`.
    2. Set **Sort** to `trimet.time`.

5. Click **Add and continue**.
6. In Layer settings:

    1. Set **Name** to **Tracks**.
    2. Set **Opacity** to 80%.

7. Scroll to **Layer Style**, and set **Border color** to pink.
8. Click **Keep changes**.
9. In the **Layers** list, click **Tracks**, and then click **Fit to data**.

At this point, you have a map with lines that represent the routes of the TriMet vehicles as they move around the city.

:::{image} /explore-analyze/images/kibana-tracks_layer.png
:alt: tracks layer
:screenshot:
:::


### Step 3. Indicate the direction of the vehicle tracks [_step_3_indicate_the_direction_of_the_vehicle_tracks]

Add a layer that uses attributes in the data to set the style and orientation of the vehicles. You’ll see the direction vehicles are headed and what traffic is like.

1. Click **Add layer**, and then select **Top Hits per entity**.
2. Select the **TriMet Positions** data view.
3. To display the most recent location per vehicle:

    1. Set **Entity** to `trimet.vehicleID`.
    2. Set **Documents per entity** to 1.
    3. Set **Sort field** to `trimet.time`.
    4. Set **Sort order** to **descending**.

4. Click **Add and continue**.
5. Change the name to **Latest positions**.
6. Scroll to **Layer Style**.

    1. Set **Symbol type** to **icon**.
    2. Set **Icon** to **Arrow**.
    3. Set the **Fill color**:

        1. Select **By value** styling, and set the field to `trimet.inCongestion`.
        2. Use a **Custom color palette**.
        3. Set the **Other** color to a dark grey.
        4. Add a green class for `false`, meaning the vehicle is not in traffic.
        5. Add a red class for `true`, meaning the vehicle is in congestion.

    4. Set **Border width** to 0.
    5. Change **Symbol orientation** to use **By value** and the `trimet.bearing` field.

       :::{image} /explore-analyze/images/kibana-top_hits_layer_style.png
       :alt: top hits layer style
       :screenshot:
       :::

7. Click **Keep changes**.
8. Open the [time filter](../../query-filter/filtering.md), and set **Refresh every** to 10 seconds, and click **Start**.

Your map should automatically refresh every 10 seconds to show the latest vehicle positions and tracks.

:::{image} /explore-analyze/images/kibana-tracks_and_top_hits.png
:alt: tracks and top hits
:screenshot:
:::


## Part 3: Setup geo-fencing alerts [_part_3_setup_geo_fencing_alerts]

Let’s make TriMet Portland data actionable and alert when vehicles enter construction zones.


### Step 1. Add a construction zone [_step_1_add_a_construction_zone]

Add a layer for construction zones, which you will draw on the map. The construction zones will be used as your geofence boundary or threshold that serves as the basis for triggering alerts.

1. Click **Add layer**.
2. Click **Create index**.
3. Set **Index name** to `trimet_construction_zones`.
4. Click **Create index**.
5. Draw 2 or 3 construction zones on your map:

    1. In the toolbar on left side of the map, select the bounding box icon ![bounding box icon](/explore-analyze/images/kibana-bounding_box_icon.png "").
    2. To draw a construction zone, click a start point on the map and drag.
    3. Click an endpoint to finish.

6. When you finish drawing the construction zones, click **Exit** under the layer name in the legend.
7. In **Layer settings**, set **Name** to **Construction zones**.
8. Scroll to **Layer Style**, and set **Fill color** to yellow.
9. Click **Keep changes**.
10. **Save** the map.

    1. Give the map a title.
    2. Under **Add to dashboard**, select **None**.
    3. Click **Save and add to library**.


The map now represents an operational view of live public transport traffic.  You’ll see the direction that the vehicles are traveling, and whether they are near or have entered a construction zone.

Your map is now complete for now, congratulations!

:::{image} /explore-analyze/images/kibana-construction_zones.png
:alt: construction zones
:screenshot:
:::


### Step 2. Configure an alert [_step_2_configure_an_alert]

Create a new alert by defining a rule and a connector. The rule includes the conditions that will trigger the alert, and the connector defines what action takes place once the alert is triggered. In this case, each alert will insert a new document into an {{es}} index.

::::{note}
For this example, you will set the rule to check every minute. However, when running in production this value may need to be adjusted to a higher check interval to avoid performance issues. Refer to [Alerting production considerations](../../../deploy-manage/production-guidance/kibana-alerting-production-considerations.md) for more information.
::::


1. In the {{kib}} **Console** create a new index and Data view

   ::::{dropdown} Create an index and Data View for the alerts
   ```js
   # Create the alerts index
   PUT trimet_alerts
   {
    "settings": {
      "number_of_replicas": 1,
      "number_of_shards": 1
    },
    "mappings": {
      "properties": {
        "vehicleId": {"type": "keyword"},
        "documentId": {"type": "text"},
        "vehicleTime": {"type": "date"},
        "detectionTime": {"type": "date"},
        "location": {"type": "geo_point"},
        "boundaryId": {"type": "keyword"},
        "message": {"type": "text"}
      }
    }
   }


   # Create the alerts index data view
   POST kbn:/api/data_views/data_view
   {
    "data_view": {
       "title": "trimet_alerts",
       "name": "TriMet Alerts",
       "timeFieldName": "detectionTime"
    }
   }
   ```

   ::::

2. Open **{{stack-manage-app}}**, and then click **{{rules-ui}}**.
3. Click **Create rule**.
4. Name the rule **TriMet Alerts**.
5. Select the **Tracking containment** rule type.
6. In the **Entities** block

    1. Select the **TriMet Positions** Data View
    2. Select `trimet.time` as the **time field**
    3. Select `trimet.location` as the **location field**
    4. Select `trimet.vehicleID` as the **entity field**

7. In the **Boundaries** block

    1. Select the **trimet_construction_zones** Data View
    2. Select `coordinates` as the **location field**
    3. Leave the **Display name** and **Filter** empty

8. Select the rule to check every minute
9. Set **Check every** to **1 minute**.
10. Notify **Only on status change**.

    :::{image} /explore-analyze/images/kibana-rule_configuration.png
    :alt: rule configuration
    :screenshot:
    :::

11. Under **Actions**, select the **Index** connector type.
12. Add a new conector named **TriMet Alerts**

    1. Select the `trimet_alerts` index
    2. Define time field for each document with the `detectionTime` field

13. Leave the **Action frequency** with the default option: **On status changes**
14. Leave the **Run when** selector with the default option: **Tracking containment met**
15. Use the following template to create new index documents:

    ```js
    {
     "vehicleId": "{{context.entityId}}",
     "vehicleTime": "{{context.entityDateTime}}",
     "documentId": "{{context.entityDocumentId}}",
     "detectionTime": "{{context.detectionDateTime}}",
     "location": "{{context.entityLocation}}",
     "boundaryId": "{{context.containingBoundaryId}}"
    }
    ```

    :::{image} /explore-analyze/images/kibana-alert_connector.png
    :alt: alert connector
    :screenshot:
    :::

16. Click **Save**.

The **TriMet Alerts connector** is added to the **{{connectors-ui}}** page. For more information on common connectors, refer to the [Slack](kibana://reference/connectors-kibana/slack-action-type.md) and [Email](kibana://reference/connectors-kibana/email-action-type.md) connectors.


### Step 3. View alerts in real time [_step_3_view_alerts_in_real_time]

With the alert configured and running, in a few minutes your `trimet_alerts` index should start getting data. You can add this data to the operational map easily:

* Open your operational map
* Click **Add layer**
* Click **Documents**
* Select the **TriMet Alerts** Data View
* Change the **Symbol type** to **Icon** and select the **Bus** icon
* Change the color to pink
* Enable the **Label** option with the `vehicleId` field
* Add the `vehicleId`, `boundaryId`, `detectionTime`, and `vehicleTime` fields to the tooltip configuration to allow viewing alert details on the map.

  :::{image} /explore-analyze/images/kibana-vehicle_alerts.png
  :alt: vehicle alerts
  :screenshot:
  :::


Congratulations! You have completed the tutorial and have the recipe for tracking assets. You can now try replicating this same analysis with your own data.
