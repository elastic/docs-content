---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Downsample data"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/downsampling-manual.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/downsampling-ilm.html
products:
  - id: elasticsearch
---

# Downsample time series data [running-downsampling]

To downsample a time series data stream (TSDS), you can use index lifecycle management (ILM) or a data stream lifecycle. (You can also use the [downsample API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-downsample) with an individual time series index, but most users don't need to use the API.)

Before you begin, review the [](downsampling-concepts.md).

:::{important}
Downsampling requires **read-only** data.
:::

In most cases, you can choose the data stream lifecycle option. If you're using [data tiers](/manage-data/lifecycle/data-tiers.md) in {{stack}}, choose the index lifecycle option.

::::{tab-set}


:::{tab-item} Data stream lifecycle

## Downsample with a data stream lifecycle
```{applies_to}
stack: ga
serverless: ga
```

To downsample a time series via a [data stream lifecycle](/manage-data/lifecycle/data-stream.md), add a [downsampling](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-data-lifecycle) section to the data stream lifecycle (for existing data streams) or the index template (for new data streams).

* Set `fixed_interval` to your preferred level of granularity. The original time series data will be aggregated at this interval.
* Set `after` to the minimum time to wait after an index rollover, before running downsampling.

```console
PUT _data_stream/my-data-stream/_lifecycle
{
  "data_retention": "7d",
  "downsampling": [
     {
       "after": "1m",
       "fixed_interval": "10m"
      },
      {
        "after": "1d",
        "fixed_interval": "1h"
      }
   ]
}
```

The downsampling action runs after the [index time series end time](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time) has passed. 
:::

:::{tab-item} Index lifecycle
    
## Downsampling with index lifecycle management
```{applies_to}
stack: ga
serverless: unavailable
```

To downsample time series data as part of index lifecycle management (ILM), include  [downsample actions](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md) in your ILM policy. You can configure multiple downsampling actions across different phases to progressively reduce data granularity over time.

This example shows a policy with rollover and two downsampling actions: one in the hot phase for initial aggregation at 5-minute intervals, and another in the warm phase for further aggregation at 1-hour intervals:

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
  	        "fixed_interval": "5m"
  	      }
        }
      },
      "warm": {
        "actions": {
          "downsample": {
            "fixed_interval": "1h"
          }
        }
      }
    }
  }
}
```
Set `fixed_interval` to your preferred level of granularity. The original time series data will be aggregated at this interval. The downsample action runs after the index is rolled over and the [index time series end time](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time) has passed. 


:::
::::

## Practical tips

Downsampling requires reading and indexing the contents of a backing index. The following guidelines can help you get the most out of it.

### Choosing the downsampling interval

When choosing the downsampling interval, you need to consider the original sampling rate of your measurements. Ideally, you would like an interval that would reduce your number of documents by a significant amount. For example, if a sensor sends data every 10 seconds downsampling to 1 minute would reduce the number of documents by 83%, compared to downsampling to 5 minutes by 96%.

The same applied when downsampling already downsampled data. 

### Downsampling with Index Lifecycle Management

The following tips apply to data streams downsampled by index lifecycle management (ILM).

#### Reducing index size

When configuring an ILM policy with downsampling, it is necessary to define the [rollover action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md) in the  `hot` phase. The rollover action consists of the conditions that would trigger a rollover hence it determines the size of an index and its shards. The size of an index can influence the impact that downsampling has on a cluster's performance. 

The downsampling operation runs over a whole index, so in certain cases downsampling can increase the load on a cluster. One of the ways to reduce that load is to reduce the size of the index; this way you can have smaller downsampling tasks that get better distributed. You can achieve that either by reducing the number of primary shards or by using setting [`max_primary_shard_docs`](https://www.elastic.co/docs/reference/elasticsearch/index-lifecycle-actions/ilm-rollover#ilm-rollover-options) to reduce the number of docs in a single shard. Using a lower value than the default of 200 million is expected to help smoothen load spikes due to downsampling.

#### Phases and tiers

When using ILM, you can define at most one downsampling round in the following phases:

- `hot` phase: it will execute the downsampling after the [index time series end time](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time) has passed
- `warm` phase: it will execute the downsampling `min_age` time after the rollover (respecting the [index time series end time](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time))
- `cold` phase: it will execute the downsampling `min_age` time after the rollover (respecting the [index time series end time](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time))

The phases do not require the respective tiers to exist. However, when a cluster has tiers, ILM automatically migrates the data processed in the phase to the respective tier. This can be disabled by adding the [migrate action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md#ilm-migrate-options) with `enabled: false`.

The migrate action is implicitly enabled, so unless explicitly disabled, the downsampling data will have to move to the respective tier; the downsampling operation occurs at the same tier as the source index and then the downsampled data gets migrated, this implementation choice allows downsampling to leverage the better resources from the "hotter" tier and move less data to the next tier.

## Additional resources

* [](downsampling-concepts.md)
* [](time-series-data-stream-tsds.md)
* [](set-up-tsds.md)

% :::{tab-item} Downsample API

% ## Downsampling with the API

% Make a [downsample API] request:

% ```console
% POST /my-time-series-index/_downsample/my-downsampled-time-series-index
% {
%    "fixed_interval": "1d"
% }
% ```

% Set `fixed_interval` to your preferred level of granularity. The original time series data will be aggregated at this interval.

% :::
