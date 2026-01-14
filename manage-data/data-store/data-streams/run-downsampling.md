---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Configuration"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/downsampling-manual.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/downsampling-ilm.html
products:
  - id: elasticsearch
---

# Configuring a time series data stream for downsampling [running-downsampling]

To downsample a time series data stream (TSDS), you can use index lifecycle management (ILM) or a data stream lifecycle. (You can also use the [downsample API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-downsample) with an individual time series index, but most users don't need to use the API.)

Before you begin, review [](downsampling-concepts.md).

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

To downsample a time series using a [data stream lifecycle](/manage-data/lifecycle/data-stream.md), add a [downsampling](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-data-lifecycle) section to the data stream lifecycle (for existing data streams) or the index template (for new data streams).

* Set `fixed_interval` to your preferred level of granularity. The original time series data will be aggregated at this interval.
* Set `after` to the minimum time to wait after an index rollover, before running downsampling.
* (Optional) Set `downsampling_method` to your preferred [downsampling method](/manage-data/data-store/data-streams/downsampling-concepts.md#downsampling-methods) (`last_value` or `aggregate`), or leave it unspecified to use the default method (`aggregate`). {applies_to}`stack: preview 9.3` {applies_to}`serverless: ga`

```console
PUT _data_stream/my-data-stream/_lifecycle
{
  "data_retention": "7d",
  "downsampling_method": "aggregate",
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
  	        "fixed_interval": "5m",
  	        "sampling_method": "aggregate"
  	      }
        }
      },
      "warm": {
        "actions": {
          "downsample": {
            "fixed_interval": "1h",
  	        "sampling_method": "aggregate"
          }
        }
      }
    }
  }
}
```
Set `fixed_interval` to your preferred level of granularity. The original time series data will be aggregated at this interval. The downsample action runs after the index is rolled over and the [index time series end time](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time) has passed.
(Optional) Set `sampling_method` to your preferred [downsampling method](/manage-data/data-store/data-streams/downsampling-concepts.md#downsampling-methods) (`last_value` or `aggregate`), or leave it unspecified to use the default method (`aggregate`). {applies_to}`stack: preview 9.3` {applies_to}`serverless: ga`

:::
::::

## Best practices

This section provides some best practices for downsampling.

### Choose an optimal downsampling interval

When choosing the downsampling interval, make sure to consider the original sampling rate of your measurements. Use an interval that reduces the number of documents by a significant percentage. For example, if a sensor sends data every 10 seconds, downsampling to 1 minute would reduce the number of documents by 83%. Downsampling to 5 minutes instead would reduce the number by 96%.

The same applies when downsampling already downsampled data. 

### Understand downsampling phases (ILM only)

When using [index lifecycle management](/manage-data/lifecycle/index-lifecycle-management.md) (ILM), you can define at most one downsampling round in each of the following phases:

- `hot` phase: Runs after the [index time series end time](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time) passes
- `warm` phase: Runs after the `min_age` time (starting the count after the rollover and  respecting the [index time series end time](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time))
- `cold` phase: Runs after the `min_age` time (starting the count after the rollover and respecting the [index time series end time](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time)

Phases don't require matching tiers. If a matching tier exists for the phase, ILM automatically migrates the data to the respective tier. To prevent this, add a [migrate action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-migrate.md#ilm-migrate-options) and specify `enabled: false`.

If you leave the default migrate action enabled, downsampling runs on the tier of the source index, which typically has more resources. The smaller, downsampled data is then migrated to the next tier.

### Reduce the index size

Because the downsampling operation processes an entire index at once, it can increase the load on the cluster. Smaller indices improve task distribution which helps to minimize the impact of downsampling on a cluster's performance.

To reduce the index size:

- limit the number of primary shards, or
- (ILM only) use  [`max_primary_shard_docs`](https://www.elastic.co/docs/reference/elasticsearch/index-lifecycle-actions/ilm-rollover#ilm-rollover-options) in the [rollover action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md) of the `hot` phase to cap documents per shard. Specify a lower value than the default of 200 million, to help prevent load spikes due to downsampling.


## Additional resources

* [](downsampling-concepts.md)
* [](time-series-data-stream-tsds.md)
* [](set-up-tsds.md)


