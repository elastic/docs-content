---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Run downsampling"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/downsampling-manual.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/downsampling-ilm.html
products:
  - id: elasticsearch
---

# Run downsampling on time series data [running-downsampling]

:::{admonition} Page status
🟢 Ready for review
:::

% TODO consider retitling (cf. overview)

To downsample a time series data stream backing index, you can use the `downsample API`, index lifecycle management (ILM), or a data stream lifecycle.

:::{note}
Downsampling runs on the data stream backing index, not the data stream itself.
:::

## Prerequisites

Before you start, make sure your index is a candidate for downsampling:

* The index must be **read-only**. You can roll over a write index and make it read-only.
* The index must have at least one metric field.

For more details about the downsampling process, refer to [](downsampling-concepts.md).

::::{tab-set}
:::{tab-item} Downsample API

## Downsampling with the API

Make a [downsample API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-downsample) request:

```console
POST /my-time-series-index/_downsample/my-downsampled-time-series-index
{
    "fixed_interval": "1d"
}
```

Set `fixed_interval` to your preferred level of granularity. The original time series data will be aggregated at this interval.

:::

:::{tab-item} Index lifecycle
    
## Downsampling with index lifecycle management

To downsample time series data as part of index lifecycle management (ILM), include a [downsample action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md) in your ILM policy:

```console
PUT _ilm/policy/my_policy
{
"policy": {
    "phases": {
    "warm": {
        "actions": {
        "downsample" : {
            "fixed_interval": "1h"
        }
        }
    }
    }
}
}
```
Set `fixed_interval` to your preferred level of granularity. The original time series data will be aggregated at this interval.

% TODO consider restoring removed tutorial-esque content

In this example, an ILM policy is configured for the `hot` phase. The downsample action runs after the index is rolled over and the [index time series end time](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time) has passed. 

```console
PUT _ilm/policy/datastream_policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover" : {
            "max_age": "5m"
          },
          "downsample": {
  	        "fixed_interval": "1h"
  	      }
        }
      }
    }
  }
}
```


:::

:::{tab-item} Data stream lifecycle

## Downsampling with data stream lifecycle management

To downsample time series data as part of data lifecycle management, create an index template that includes a `lifecycle` section with a [downsampling](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-data-lifecycle) object. 

* Set `fixed_interval` to your preferred level of granularity. The original time series data will be aggregated at this interval.
* Set `after` to the minimum time to wait after an index rollover, before running downsampling.

```console
PUT _index_template/datastream_template
{
  "index_patterns": [
    "datastream*"
  ],
  "data_stream": {},
  "template": {
    "lifecycle": {
      "downsampling": [
        {
          "after": "1m",
          "fixed_interval": "1h"
        }
      ]
    },
    "settings": {
      "index": {
        "mode": "time_series"
      }
    },
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date"
        },
        [...]
      }
    }
  }
}
```


For more details about index templates for time series data streams, refer to [](set-up-tsds.md).

:::

::::

## Additional resources

* [](downsampling-concepts.md)
* [](time-series-data-stream-tsds.md)
