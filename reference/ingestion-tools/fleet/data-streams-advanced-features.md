---
navigation_title: "Advanced data stream features"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/data-streams-advanced-features.html
---

# Enabling and disabling advanced indexing features for {{fleet}}-managed data streams [data-streams-advanced-features]


{{fleet}} provides support for several advanced features around its data streams, including:

* [Time series data streams (TSDS)](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md)
* [Synthetic `_source`](elasticsearch://docs/reference/elasticsearch/mapping-reference/mapping-source-field.md#synthetic-source)

These features can be enabled and disabled for {{fleet}}-managed data streams by using the index template API and a few key settings. Note that in versions 8.17.0 and later, Synthetic `_source` requires an Enterprise license.

::::{note}
If you are already making use of `@custom` component templates for ingest or retention customization (as shown for example in [Tutorial: Customize data retention policies](/reference/ingestion-tools/fleet/data-streams-ilm-tutorial.md)), exercise care to ensure you don’t overwrite your customizations when making these requests.
::::


We recommended using [{{kib}} Dev Tools](/explore-analyze/query-filter/tools.md) to run the following requests. Replace `<NAME>` with the name of a given integration data stream. For example specifying `metrics-nginx.stubstatus` results in making a PUT request to `_component_template/metrics-nginx.stubstatus@custom`. Use the index management interface to explore what integration data streams are available to you.

Once you’ve executed a given request below, you also need to execute a data stream rollover to ensure any incoming data is ingested with your new settings immediately. For example:

```sh
POST metrics-nginx.stubstatus-default/_rollover
```

Refer to the following steps to enable or disable advanced data stream features:

* [Disable synthetic `_source`](#data-streams-advanced-synthetic-disable)


## Enable TSDS [data-streams-advanced-tsds-enable]

::::{note}
TSDS uses synthetic `_source`, so if you want to trial both features you need to enable only TSDS.
::::


Due to restrictions in the {{es}} API, TSDS must be enabled at the **index template** level. So, you’ll need to make some sequential requests to enable or disable TSDS.

1. Send a GET request to retrieve the index template:

    ```json
    GET _index_template/<NAME>
    ```

2. Use the JSON payload returned from the GET request to populate a PUT request, for example:

    ```json
    PUT _index_template/<NAME>
    {
      # You can copy & paste this directly from the GET request above
      "index_patterns": [
        "<index pattern from GET request>"
      ],

      # Make sure this is added
      "template": {
        "settings": {
          "index": {
            "mode": "time_series"
          }
        }
      },

      # You can copy & paste this directly from the GET request above
      "composed_of": [
        "<NAME>@package",
        "<NAME>@custom",
        ".fleet_globals-1",
        ".fleet_agent_id_verification-1"
      ],

      # You can copy & paste this directly from the GET request above
      "priority": 200,

      # Make sure this is added
      "data_stream": {
        "allow_custom_routing": false
      }
    }
    ```



## Disable TSDS [data-streams-advanced-tsds-disable]

To disable TSDS, follow the same procedure as to [enable TSDS](#data-streams-advanced-tsds-enable), but specify `null` for `index.mode` instead of `time_series`. Follow the steps below or you can copy the [NGINX example](#data-streams-advanced-tsds-disable-nginx-example).

1. Send a GET request to retrieve the index template:

    ```json
    GET _index_template/<NAME>
    ```

2. Use the JSON payload returned from the GET request to populate a PUT request, for example:

    ```json
    PUT _index_template/<NAME>
    {
      # You can copy/paste this directly from the GET request above
      "index_patterns": [
        "<index pattern from GET request>"
      ],

      # Make sure this is added
      "template": {
        "settings": {
          "index": {
            "mode": null
          }
        }
      },

      # You can copy/paste this directly from the GET request above
      "composed_of": [
        "<NAME>@package",
        "<NAME>@custom",
        ".fleet_globals-1",
        ".fleet_agent_id_verification-1"
      ],

      # You can copy/paste this directly from the GET request above
      "priority": 200,

      # Make sure this is added
      "data_stream": {
        "allow_custom_routing": false
      }
    }
    ```

    For example, the following payload disables TSDS on `nginx.stubstatus`:

    $$$data-streams-advanced-tsds-disable-nginx-example$$$

    ```json
    {
      "index_patterns": [
          "metrics-nginx.stubstatus-*"
      ],

      "template": {
        "settings": {
          "index": {
            "mode": null
          }
        }
      },

      "composed_of": [
        "metrics-nginx.stubstatus@package",
        "metrics-nginx.stubstatus@custom",
        ".fleet_globals-1",
        ".fleet_agent_id_verification-1"
      ],

      "priority": 200,

      "data_stream": {
        "allow_custom_routing": false
      }
    }
    ```



## Enable synthetic `_source` [data-streams-advanced-synthetic-enable]

```json
PUT _component_template/<NAME>@custom
{
  "settings": {
    "index": {
      "mapping": {
        "source": {
          "mode": "synthetic"
        }
      }
    }
  }
}
```


## Disable synthetic `_source` [data-streams-advanced-synthetic-disable]

```json
PUT _component_template/<NAME>@custom
{
  "settings": {
    "index": {
      "mapping": {
        "source": {"mode": "stored"}
      }
    }
  }
}
```

