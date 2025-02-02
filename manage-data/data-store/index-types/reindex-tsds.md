---
navigation_title: "Reindex a TSDS"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tsds-reindex.html
---



# Reindex a TSDS [tsds-reindex]



## Introduction [tsds-reindex-intro] 

With reindexing, you can copy documents from an old [time-series data stream (TSDS)](time-series-data-stream-tsds.md) to a new one. Data streams support reindexing in general, with a few [restrictions](use-data-stream.md#reindex-with-a-data-stream). Still, time-series data streams introduce additional challenges due to tight control on the accepted timestamp range for each backing index they contain. Direct use of the reindex API would likely error out due to attempting to insert documents with timestamps that are outside the current acceptance window.

To avoid these limitations, use the process that is outlined below:

1. Create an index template for the destination data stream that will contain the re-indexed data.
2. Update the template to

    1. Set `index.time_series.start_time` and `index.time_series.end_time` index settings to match the lowest and highest `@timestamp` values in the old data stream.
    2. Set the `index.number_of_shards` index setting to the sum of all primary shards of all backing indices of the old data stream.
    3. Set `index.number_of_replicas` to zero and unset the `index.lifecycle.name` index setting.

3. Run the reindex operation to completion.
4. Revert the overriden index settings in the destination index template.
5. Invoke the `rollover` api to create a new backing index that can receive new documents.

::::{note} 
This process only applies to time-series data streams without [downsampling](downsampling-time-series-data-stream.md) configuration. Data streams with downsampling can only be re-indexed by re-indexing their backing indexes individually and adding them to an empty destination data stream.
::::


In what follows, we elaborate on each step of the process with examples.


## Create a TSDS template to accept old documents [tsds-reindex-create-template] 

Consider a TSDS with the following template:

```console
POST /_component_template/source_template
{
  "template": {
    "settings": {
      "index": {
        "number_of_replicas": 2,
        "number_of_shards": 2,
        "mode": "time_series",
        "routing_path": [ "metricset" ]
      }
    },
    "mappings": {
      "properties": {
        "@timestamp": { "type": "date" },
        "metricset": {
          "type": "keyword",
          "time_series_dimension": true
        },
        "k8s": {
          "properties": {
            "tx": { "type": "long" },
            "rx": { "type": "long" }
          }
        }
      }
    }
  }
}

POST /_index_template/1
{
  "index_patterns": [
    "k8s*"
  ],
  "composed_of": [
    "source_template"
  ],
  "data_stream": {}
}
```

A possible output of `/k8s/_settings` looks like:

```console-result
{
  ".ds-k8s-2023.09.01-000002": {
    "settings": {
      "index": {
        "mode": "time_series",
        "routing": {
          "allocation": {
            "include": {
              "_tier_preference": "data_hot"
            }
          }
        },
        "hidden": "true",
        "number_of_shards": "2",
        "time_series": {
          "end_time": "2023-09-01T14:00:00.000Z",
          "start_time": "2023-09-01T10:00:00.000Z"
        },
        "provided_name": ".ds-k9s-2023.09.01-000002",
        "creation_date": "1694439857608",
        "number_of_replicas": "2",
        "routing_path": [
          "metricset"
        ],
        ...
      }
    }
  },
  ".ds-k8s-2023.09.01-000001": {
    "settings": {
      "index": {
        "mode": "time_series",
        "routing": {
          "allocation": {
            "include": {
              "_tier_preference": "data_hot"
            }
          }
        },
        "hidden": "true",
        "number_of_shards": "2",
        "time_series": {
          "end_time": "2023-09-01T10:00:00.000Z",
          "start_time": "2023-09-01T06:00:00.000Z"
        },
        "provided_name": ".ds-k9s-2023.09.01-000001",
        "creation_date": "1694439837126",
        "number_of_replicas": "2",
        "routing_path": [
          "metricset"
        ],
        ...
      }
    }
  }
}
```

To reindex this TSDS, do not to re-use its index template in the destination data stream, to avoid impacting its functionality. Instead, clone the template of the source TSDS and apply the following modifications:

* Set `index.time_series.start_time` and `index.time_series.end_time` index settings explicitly. Their values should be based on the lowest and highest `@timestamp` values in the data stream to reindex. This way, the initial backing index can load all data that is contained in the source data stream.
* Set `index.number_of_shards` index setting to the sum of all primary shards of all backing indices of the source data stream. This helps maintain the same level of search parallelism, as each shard is processed in a separate thread (or more).
* Unset the `index.lifecycle.name` index setting, if any. This prevents ILM from modifying the destination data stream during reindexing.
* (Optional) Set `index.number_of_replicas` to zero. This helps speed up the reindex operation. Since the data gets copied, there is limited risk of data loss due to lack of replicas.

Using the example above as source TSDS, the template for the destination TSDS would be:

```console
POST /_component_template/destination_template
{
  "template": {
    "settings": {
      "index": {
        "number_of_replicas": 0,
        "number_of_shards": 4,
        "mode": "time_series",
        "routing_path": [ "metricset" ],
        "time_series": {
          "end_time": "2023-09-01T14:00:00.000Z",
          "start_time": "2023-09-01T06:00:00.000Z"
        }
      }
    },
    "mappings": {
      "properties": {
        "@timestamp": { "type": "date" },
        "metricset": {
          "type": "keyword",
          "time_series_dimension": true
        },
        "k8s": {
          "properties": {
            "tx": { "type": "long" },
            "rx": { "type": "long" }
          }
        }
      }
    }
  }
}

POST /_index_template/2
{
  "index_patterns": [
    "k9s*"
  ],
  "composed_of": [
    "destination_template"
  ],
  "data_stream": {}
}
```


## Reindex [tsds-reindex-op] 

Invoke the reindex api, for instance:

```console
POST /_reindex
{
  "source": {
    "index": "k8s"
  },
  "dest": {
    "index": "k9s",
    "op_type": "create"
  }
}
```


## Restore the destination index template [tsds-reindex-restore] 

Once the reindexing operation completes, restore the index template for the destination TSDS as follows:

* Remove the overrides for `index.time_series.start_time` and `index.time_series.end_time`.
* Restore the values of `index.number_of_shards`, `index.number_of_replicas`  and  `index.lifecycle.name` as applicable.

Using the previous example, the destination template is modified as follows:

```console
POST /_component_template/destination_template
{
  "template": {
    "settings": {
      "index": {
        "number_of_replicas": 2,
        "number_of_shards": 2,
        "mode": "time_series",
        "routing_path": [ "metricset" ]
      }
    },
    "mappings": {
      "properties": {
        "@timestamp": { "type": "date" },
        "metricset": {
          "type": "keyword",
          "time_series_dimension": true
        },
        "k8s": {
          "properties": {
            "tx": { "type": "long" },
            "rx": { "type": "long" }
          }
        }
      }
    }
  }
}
```

Next, Invoke the `rollover` api on the destination data stream without any conditions set.

```console
POST /k9s/_rollover/
```

This creates a new backing index with the updated index settings. The destination data stream is now ready to accept new documents.

Note that the initial backing index can still accept documents within the range of timestamps derived from the source data stream. If this is not desired, mark it as [read-only](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-blocks.html#index-blocks-read-only) explicitly.

