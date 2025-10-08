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

## Best practices

This section provides some best practices for downsampling.

### Choose an optimal downsampling interval

When choosing the downsampling interval, make sure to consider the original sampling rate of your measurements. Use an interval that reduces the number of documents by a significant percentage. For example, if a sensor sends data every 10 seconds, downsampling to 1 minute would reduce the number of documents by 83%. Downsampling to 5 minutes instead would reduce the number by 96%.

The same applies when downsampling already downsampled data. 

### Downsampling with Index Lifecycle Management

The following tips apply to data streams downsampled by index lifecycle management (ILM).

### Configure phases and tiers for downsampling

When using [index lifecycle management](/manage-data/lifecycle/index-lifecycle-management.md) (ILM), you can define at most one downsampling round in each of the following phases:

- `hot` phase: Runs after the [index time series end time](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time) passes
- `warm` phase: Runs after the `min_age` time (following the rollover and  respecting the [index time series end time](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time))
- `cold` phase: Runs after the `min_age` time (following the rollover and respecting the [index time series end time](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time)

Phases don't require matching tiers. If a matching tier exists for the phase, ILM automatically migrates the data to the respective tier. To prevent this, add a [migrate action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md#ilm-migrate-options) and specify `enabled: false`.

If you leave the default migrate action enabled, downsampling runs on the hotter tier, which typically has more resources. The smaller, downsampled data is then migrated to the next tier.

### Reduce the index size

When configuring an ILM policy with downsampling, define the [rollover action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md) in the `hot` phase to control index size. Using smaller indices helps to minimize the impact of downsampling on a cluster's performance. 

Because the downsampling operation processes an entire index at once, it can increase the load on the cluster. Smaller indices improve task distribution. To reduce the index size, limit the number of primary shards or use  [`max_primary_shard_docs`](https://www.elastic.co/docs/reference/elasticsearch/index-lifecycle-actions/ilm-rollover#ilm-rollover-options) to cap documents per shard. Specify a lower value than the default of 200 million, to help prevent load spikes due to downsampling.

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
