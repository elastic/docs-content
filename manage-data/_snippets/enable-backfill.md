{{es}} can create missing backing indices when you add data that precedes existing time ranges.
To enable this feature, update the cluster settings:

```console
PUT _cluster/settings
{
  "persistent": { <1>
    "data_stream.past_tsdb_index_creation_enabled": true,
    "data_streams.past_tsdb_index_interval": "2d" <1>
  }
}
```

1. These settings are persistent and apply to all data streams in the cluster.
2. By default, each past backing index covers one day of data. Refer to [`data_streams.past_tsdb_index_interval`](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#time-series-data-stream).
