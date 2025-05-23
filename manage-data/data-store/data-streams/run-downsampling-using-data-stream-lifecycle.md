---
navigation_title: Run downsampling using data stream lifecycle
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/downsampling-dsl.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---



# Run downsampling using data stream lifecycle [downsampling-dsl]


This is a simplified example that allows you to see quickly how [downsampling](./downsampling-time-series-data-stream.md) works as part of a datastream lifecycle to reduce the storage size of a sampled set of metrics. The example uses typical Kubernetes cluster monitoring data. To test out downsampling with data stream lifecycle, follow these steps:

1. Check the [prerequisites](#downsampling-dsl-prereqs).
2. [Create an index template with data stream lifecycle](#downsampling-dsl-create-index-template).
3. [Ingest time series data](#downsampling-dsl-ingest-data).
4. [View current state of data stream](#downsampling-dsl-view-data-stream-state).
5. [Roll over the data stream](#downsampling-dsl-rollover).
6. [View downsampling results](#downsampling-dsl-view-results).


## Prerequisites [downsampling-dsl-prereqs]

Refer to [time series data stream prerequisites](./set-up-tsds.md#tsds-prereqs).


## Create an index template with data stream lifecycle [downsampling-dsl-create-index-template]

This creates an index template for a basic data stream. The available parameters for an index template are described in detail in [Set up a time series data stream](set-up-data-stream.md).

For simplicity, in the time series mapping all `time_series_metric` parameters are set to type `gauge`, but the `counter` metric type may also be used. The `time_series_metric` values determine the kind of statistical representations that are used during downsampling.

The index template includes a set of static [time series dimensions](time-series-data-stream-tsds.md#time-series-dimension): `host`, `namespace`, `node`, and `pod`. The time series dimensions are not changed by the downsampling process.

To enable downsampling, this template includes a `lifecycle` section with [downsampling](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-data-lifecycle) object. `fixed_interval` parameter sets downsampling interval at which you want to aggregate the original time series data. `after` parameter specifies how much time after index was rolled over should pass before downsampling is performed.

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
        "kubernetes": {
          "properties": {
            "container": {
              "properties": {
                "cpu": {
                  "properties": {
                    "usage": {
                      "properties": {
                        "core": {
                          "properties": {
                            "ns": {
                              "type": "long"
                            }
                          }
                        },
                        "limit": {
                          "properties": {
                            "pct": {
                              "type": "float"
                            }
                          }
                        },
                        "nanocores": {
                          "type": "long",
                          "time_series_metric": "gauge"
                        },
                        "node": {
                          "properties": {
                            "pct": {
                              "type": "float"
                            }
                          }
                        }
                      }
                    }
                  }
                },
                "memory": {
                  "properties": {
                    "available": {
                      "properties": {
                        "bytes": {
                          "type": "long",
                          "time_series_metric": "gauge"
                        }
                      }
                    },
                    "majorpagefaults": {
                      "type": "long"
                    },
                    "pagefaults": {
                      "type": "long",
                      "time_series_metric": "gauge"
                    },
                    "rss": {
                      "properties": {
                        "bytes": {
                          "type": "long",
                          "time_series_metric": "gauge"
                        }
                      }
                    },
                    "usage": {
                      "properties": {
                        "bytes": {
                          "type": "long",
                          "time_series_metric": "gauge"
                        },
                        "limit": {
                          "properties": {
                            "pct": {
                              "type": "float"
                            }
                          }
                        },
                        "node": {
                          "properties": {
                            "pct": {
                              "type": "float"
                            }
                          }
                        }
                      }
                    },
                    "workingset": {
                      "properties": {
                        "bytes": {
                          "type": "long",
                          "time_series_metric": "gauge"
                        }
                      }
                    }
                  }
                },
                "name": {
                  "type": "keyword"
                },
                "start_time": {
                  "type": "date"
                }
              }
            },
            "host": {
              "type": "keyword",
              "time_series_dimension": true
            },
            "namespace": {
              "type": "keyword",
              "time_series_dimension": true
            },
            "node": {
              "type": "keyword",
              "time_series_dimension": true
            },
            "pod": {
              "type": "keyword",
              "time_series_dimension": true
            }
          }
        }
      }
    }
  }
}
```


## Ingest time series data [downsampling-dsl-ingest-data]

Use a bulk API request to automatically create your TSDS and index a set of ten documents.

**Important:** Before running this bulk request you need to update the timestamps to within three to five hours after your current time. That is, search `2022-06-21T15` and replace with your present date, and adjust the hour to your current time plus three hours.

```console
PUT /datastream/_bulk?refresh
{"create": {}}
{"@timestamp":"2022-06-21T15:49:00Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":91153,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":463314616},"usage":{"bytes":307007078,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":585236},"rss":{"bytes":102728},"pagefaults":120901,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
{"create": {}}
{"@timestamp":"2022-06-21T15:45:50Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":124501,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":982546514},"usage":{"bytes":360035574,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":1339884},"rss":{"bytes":381174},"pagefaults":178473,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
{"create": {}}
{"@timestamp":"2022-06-21T15:44:50Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":38907,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":862723768},"usage":{"bytes":379572388,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":431227},"rss":{"bytes":386580},"pagefaults":233166,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
{"create": {}}
{"@timestamp":"2022-06-21T15:44:40Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":86706,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":567160996},"usage":{"bytes":103266017,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":1724908},"rss":{"bytes":105431},"pagefaults":233166,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
{"create": {}}
{"@timestamp":"2022-06-21T15:44:00Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":150069,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":639054643},"usage":{"bytes":265142477,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":1786511},"rss":{"bytes":189235},"pagefaults":138172,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
{"create": {}}
{"@timestamp":"2022-06-21T15:42:40Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":82260,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":854735585},"usage":{"bytes":309798052,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":924058},"rss":{"bytes":110838},"pagefaults":259073,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
{"create": {}}
{"@timestamp":"2022-06-21T15:42:10Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":153404,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":279586406},"usage":{"bytes":214904955,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":1047265},"rss":{"bytes":91914},"pagefaults":302252,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
{"create": {}}
{"@timestamp":"2022-06-21T15:40:20Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":125613,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":822782853},"usage":{"bytes":100475044,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":2109932},"rss":{"bytes":278446},"pagefaults":74843,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
{"create": {}}
{"@timestamp":"2022-06-21T15:40:10Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":100046,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":567160996},"usage":{"bytes":362826547,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":1986724},"rss":{"bytes":402801},"pagefaults":296495,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
{"create": {}}
{"@timestamp":"2022-06-21T15:38:30Z","kubernetes":{"host":"gke-apps-0","node":"gke-apps-0-0","pod":"gke-apps-0-0-0","container":{"cpu":{"usage":{"nanocores":40018,"core":{"ns":12828317850},"node":{"pct":2.77905e-05},"limit":{"pct":2.77905e-05}}},"memory":{"available":{"bytes":1062428344},"usage":{"bytes":265142477,"node":{"pct":0.01770037710617187},"limit":{"pct":9.923134671484496e-05}},"workingset":{"bytes":2294743},"rss":{"bytes":340623},"pagefaults":224530,"majorpagefaults":0},"start_time":"2021-03-30T07:59:06Z","name":"container-name-44"},"namespace":"namespace26"}}
```


## View current state of data stream [downsampling-dsl-view-data-stream-state]

Now that you’ve created and added documents to the data stream, check to confirm the current state of the new index.

```console
GET _data_stream
```

If the data stream lifecycle policy has not yet been applied, your results will be like the following. Note the original `index_name`: `.ds-datastream-2024.04.29-000001`.

```console-result
{
  "data_streams": [
    {
      "name": "datastream",
      "timestamp_field": {
        "name": "@timestamp"
      },
      "indices": [
        {
          "index_name": ".ds-datastream-2024.04.29-000001",
          "index_uuid": "vUMNtCyXQhGdlo1BD-cGRw",
          "managed_by": "Data stream lifecycle"
        }
      ],
      "generation": 1,
      "status": "GREEN",
      "template": "datastream_template",
      "lifecycle": {
        "enabled": true,
        "downsampling": [
          {
            "after": "1m",
            "fixed_interval": "1h"
          }
        ]
      },
      "next_generation_managed_by": "Data stream lifecycle",
      "hidden": false,
      "system": false,
      "allow_custom_routing": false,
      "replicated": false,
      "rollover_on_write": false,
      "time_series": {
        "temporal_ranges": [
          {
            "start": "2024-04-29T15:55:46.000Z",
            "end": "2024-04-29T18:25:46.000Z"
          }
        ]
      }
    }
  ]
}
```

Next, run a search query:

```console
GET datastream/_search
```

The query returns your ten newly added documents.

```console-result
{
  "took": 23,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10,
      "relation": "eq"
    },
...
```


## Roll over the data stream [downsampling-dsl-rollover]

Data stream lifecycle will automatically roll over data stream and perform downsampling. This step is only needed in order to see downsampling results in scope of this tutorial.

Roll over the data stream using the [rollover API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover):

```console
POST /datastream/_rollover/
```


## View downsampling results [downsampling-dsl-view-results]

By default, data stream lifecycle actions are executed every five minutes. Downsampling takes place after the index is rolled over and the [index time series end time](elasticsearch://reference/elasticsearch/index-settings/time-series.md#index-time-series-end-time) has lapsed as the source index is still expected to receive major writes until then. Index is now rolled over after previous step but its time series range end is likely still in the future. Once index time series range is in the past, re-run the `GET _data_stream` request.

```console
GET _data_stream
```

After the data stream lifecycle action was executed, original `.ds-datastream-2024.04.29-000001` index is replaced with a new, downsampled index, in this case `downsample-1h-.ds-datastream-2024.04.29-000001`.

```console-result
{
  "data_streams": [
    {
      "name": "datastream",
      "timestamp_field": {
        "name": "@timestamp"
      },
      "indices": [
        {
          "index_name": "downsample-1h-.ds-datastream-2024.04.29-000001",
          "index_uuid": "VqXuShP4T8ODAOnWFcqitg",
          "managed_by": "Data stream lifecycle"
        },
        {
          "index_name": ".ds-datastream-2024.04.29-000002",
          "index_uuid": "8gCeSdjUSWG-o-PeEAJ0jA",
          "managed_by": "Data stream lifecycle"
        }
      ],
...
```

Run a search query on the datastream (note that when querying downsampled indices there are [a few nuances to be aware of](./downsampling-time-series-data-stream.md#querying-downsampled-indices-notes)).

```console
GET datastream/_search
```

The new downsampled index contains just one document that includes the `min`, `max`, `sum`, and `value_count` statistics based off of the original sampled metrics.

```console-result
{
  "took": 26,
  "timed_out": false,
  "_shards": {
    "total": 2,
    "successful": 2,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "downsample-1h-.ds-datastream-2024.04.29-000001",
        "_id": "0eL0wMf38sl_s5JnAAABjyrMjoA",
        "_score": 1,
        "_source": {
          "@timestamp": "2024-04-29T17:00:00.000Z",
          "_doc_count": 10,
          "kubernetes": {
            "container": {
              "cpu": {
                "usage": {
                  "core": {
                    "ns": 12828317850
                  },
                  "limit": {
                    "pct": 0.0000277905
                  },
                  "nanocores": {
                    "min": 38907,
                    "max": 153404,
                    "sum": 992677,
                    "value_count": 10
                  },
                  "node": {
                    "pct": 0.0000277905
                  }
                }
              },
              "memory": {
                "available": {
                  "bytes": {
                    "min": 279586406,
                    "max": 1062428344,
                    "sum": 7101494721,
                    "value_count": 10
                  }
                },
                "majorpagefaults": 0,
                "pagefaults": {
                  "min": 74843,
                  "max": 302252,
                  "sum": 2061071,
                  "value_count": 10
                },
                "rss": {
                  "bytes": {
                    "min": 91914,
                    "max": 402801,
                    "sum": 2389770,
                    "value_count": 10
                  }
                },
                "usage": {
                  "bytes": {
                    "min": 100475044,
                    "max": 379572388,
                    "sum": 2668170609,
                    "value_count": 10
                  },
                  "limit": {
                    "pct": 0.00009923134
                  },
                  "node": {
                    "pct": 0.017700378
                  }
                },
                "workingset": {
                  "bytes": {
                    "min": 431227,
                    "max": 2294743,
                    "sum": 14230488,
                    "value_count": 10
                  }
                }
              },
              "name": "container-name-44",
              "start_time": "2021-03-30T07:59:06.000Z"
            },
            "host": "gke-apps-0",
            "namespace": "namespace26",
            "node": "gke-apps-0-0",
            "pod": "gke-apps-0-0-0"
          }
        }
      }
    ]
  }
}
```

Use the [data stream stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-data-streams-stats-1) to get statistics for the data stream, including the storage size.

```console
GET /_data_stream/datastream/_stats?human=true
```

```console-result
{
  "_shards": {
    "total": 4,
    "successful": 4,
    "failed": 0
  },
  "data_stream_count": 1,
  "backing_indices": 2,
  "total_store_size": "37.3kb",
  "total_store_size_bytes": 38230,
  "data_streams": [
    {
      "data_stream": "datastream",
      "backing_indices": 2,
      "store_size": "37.3kb",
      "store_size_bytes": 38230,
      "maximum_timestamp": 1714410000000
    }
  ]
}
```

This example demonstrates how downsampling works as part of a data stream lifecycle to reduce the storage size of metrics data as it becomes less current and less frequently queried.
