---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-configuring-aggregation.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Aggregating data for faster performance [ml-configuring-aggregation]

When you aggregate data, {{es}} automatically distributes the calculations across your cluster. Then you can feed this aggregated data into the {{ml-features}} instead of raw results. It reduces the volume of data that must be analyzed.

## Requirements [aggs-requs-dfeeds]

There are a number of requirements for using aggregations in {{dfeeds}}.

### Aggregations [aggs-aggs]

* Your aggregation must include a `date_histogram` aggregation or a top level `composite` aggregation, which in turn must contain a `max` aggregation on the time field. It ensures that the aggregated data is a time series and the timestamp of each bucket is the time of the last record in the bucket.
* The `time_zone` parameter in the date histogram aggregation must be set to `UTC`, which is the default value.
* The name of the aggregation and the name of the field that it operates on need to match. For example, if you use a `max` aggregation on a time field called `responsetime`, the name of the aggregation must also be `responsetime`.
* For `composite` aggregation support, there must be exactly one `date_histogram` value source. That value source must not be sorted in descending order. Additional `composite` aggregation value sources are allowed, such as `terms`.
* The `size` parameter of the non-composite aggregations must match the cardinality of your data. A greater value of the `size` parameter increases the memory requirement of the aggregation.
* If you set the `summary_count_field_name` property to a non-null value, the {{anomaly-job}} expects to receive aggregated input. The property must be set to the name of the field that contains the count of raw data points that have been aggregated. It applies to all detectors in the job.
* The influencers or the partition fields must be included in the aggregation of your {{dfeed}}, otherwise they are not included in the job analysis. For more information on influencers, refer to [Influencers](ml-ad-run-jobs.md#ml-ad-influencers).

### Intervals [aggs-interval]

* The bucket span of your {{anomaly-job}} must be divisible by the value of the `calendar_interval` or `fixed_interval` in your aggregation (with no remainder).
* If you specify a `frequency` for your {{dfeed}}, it must be divisible by the `calendar_interval` or the `fixed_interval`.
* {{anomaly-jobs-cap}} cannot use `date_histogram` or `composite` aggregations with an interval measured in months because the length of the month is not fixed; they can use weeks or smaller units.

## Limitations [aggs-limits-dfeeds]

* If your [{{dfeed}} uses aggregations with nested `terms` aggs](#aggs-dfeeds) and model plot is not enabled for the {{anomaly-job}}, neither the **Single Metric Viewer** nor the **Anomaly Explorer** can plot and display an anomaly chart. In these cases, an explanatory message is shown instead of the chart.
* Your {{dfeed}} can contain multiple aggregations, but only the ones with names that match values in the job configuration are fed to the job.
* Using [scripted metric](elasticsearch://reference/aggregations/search-aggregations-metrics-scripted-metric-aggregation.md) aggregations is not supported in {{dfeeds}}.

## Recommendations [aggs-recommendations-dfeeds]

* When your detectors use [metric](/reference/machine-learning/ml-metric-functions.md) or [sum](/reference/machine-learning/ml-sum-functions.md) analytical functions, it’s recommended to set the `date_histogram` or `composite` aggregation interval to a tenth of the bucket span. This creates finer, more granular time buckets, which are ideal for this type of analysis.
* When your detectors use [count](/reference/machine-learning/ml-count-functions.md) or [rare](/reference/machine-learning/ml-rare-functions.md) functions, set the interval to the same value as the bucket span.
* If you have multiple influencers or partition fields or if your field cardinality is more than 1000, use [composite aggregations](elasticsearch://reference/aggregations/search-aggregations-bucket-composite-aggregation.md).

    To determine the cardinality of your data, you can run searches such as:

    ```js
    GET .../_search
    {
      "aggs": {
        "service_cardinality": {
          "cardinality": {
            "field": "service"
          }
        }
      }
    }
    ```

## Including aggregations in {{anomaly-jobs}} [aggs-using-date-histogram]

When you create or update an {{anomaly-job}}, you can include aggregated fields in the analysis configuration. In the {{dfeed}} configuration object, you can define the aggregations.

```console
PUT _ml/anomaly_detectors/kibana-sample-data-flights
{
  "analysis_config": {
    "bucket_span": "60m",
    "detectors": [{
      "function": "mean",
      "field_name": "responsetime",  <1>
      "by_field_name": "airline"  <1>
    }],
    "summary_count_field_name": "doc_count" <2>
  },
  "data_description": {
    "time_field":"time"  <1>
  },
  "datafeed_config":{
    "indices": ["kibana-sample-data-flights"],
    "aggregations": {
      "buckets": {
        "date_histogram": {
          "field": "time",
          "fixed_interval": "360s",
          "time_zone": "UTC"
        },
        "aggregations": {
          "time": {  <3>
            "max": {"field": "time"}
          },
          "airline": {  <4>
            "terms": {
             "field": "airline",
              "size": 100
            },
            "aggregations": {
              "responsetime": {  <5>
                "avg": {
                  "field": "responsetime"
                }
              }
            }
          }
        }
      }
    }
  }
}
```

1. The `airline`, `responsetime`, and `time` fields are aggregations. Only the aggregated fields defined in the `analysis_config` object are analyzed by the {{anomaly-job}}.
2. The `summary_count_field_name` property is set to the `doc_count` field that is an aggregated field and contains the count of the aggregated data points.
3. The aggregations have names that match the fields that they operate on. The `max` aggregation is named `time` and its field also needs to be `time`.
4. The `term` aggregation is named `airline` and its field is also named `airline`.
5. The `avg` aggregation is named `responsetime` and its field is also named `responsetime`.

Use the following format to define a `date_histogram` aggregation to bucket by time in your {{dfeed}}:

```js
"aggregations": {
  ["bucketing_aggregation": {
    "bucket_agg": {
      ...
    },
    "aggregations": {
      "data_histogram_aggregation": {
        "date_histogram": {
          "field": "time",
        },
        "aggregations": {
          "timestamp": {
            "max": {
              "field": "time"
            }
          },
          [,"<first_term>": {
            "terms":{...
            }
            [,"aggregations" : {
              [<sub_aggregation>]+
            } ]
          }]
        }
      }
    }
  }
}
```

## Composite aggregations [aggs-using-composite]

Composite aggregations are optimized for queries that are either `match_all` or `range` filters. Use composite aggregations in your {{dfeeds}} for these cases. Other types of queries may cause the `composite` aggregation to be inefficient.

The following is an example of a job with a {{dfeed}} that uses a `composite` aggregation to bucket the metrics based on time and terms:

```console
PUT _ml/anomaly_detectors/kibana-sample-data-flights-composite
{
  "analysis_config": {
    "bucket_span": "60m",
    "detectors": [{
      "function": "mean",
      "field_name": "responsetime",
      "by_field_name": "airline"
    }],
    "summary_count_field_name": "doc_count"
  },
  "data_description": {
    "time_field":"time"
  },
  "datafeed_config":{
    "indices": ["kibana-sample-data-flights"],
    "aggregations": {
      "buckets": {
        "composite": {
          "size": 1000,  <1>
          "sources": [
            {
              "time_bucket": {  <2>
                "date_histogram": {
                  "field": "time",
                  "fixed_interval": "360s",
                  "time_zone": "UTC"
                }
              }
            },
            {
              "airline": {  <3>
                "terms": {
                  "field": "airline"
                }
              }
            }
          ]
        },
        "aggregations": {
          "time": {  <4>
            "max": {
              "field": "time"
            }
          },
          "responsetime": { <5>
            "avg": {
              "field": "responsetime"
            }
          }
        }
      }
    }
  }
}
```

1. The number of resources to use when aggregating the data. A larger `size` means a faster {{dfeed}} but more cluster resources are used when searching.
2. The required `date_histogram` composite aggregation source. Make sure it is named differently than your desired time field.
3. Instead of using a regular `term` aggregation, adding a composite aggregation `term` source with the name `airline` works. Note its name is the same as the field.
4. The required `max` aggregation whose name is the time field in the job analysis config.
5. The `avg` aggregation is named `responsetime` and its field is also named `responsetime`.

Use the following format to define a composite aggregation in your {{dfeed}}:

```js
"aggregations": {
  "composite_agg": {
    "sources": [
      {
        "date_histogram_agg": {
          "field": "time",
          ...settings...
        }
      },
      ...other valid sources...
      ],
      ...composite agg settings...,
      "aggregations": {
        "timestamp": {
            "max": {
              "field": "time"
            }
          },
          ...other aggregations...
          [
            [,"aggregations" : {
              [<sub_aggregation>]+
            } ]
          }]
      }
   }
}
```

## Nested aggregations [aggs-dfeeds]

You can also use complex nested aggregations in {{dfeeds}}.

The next example uses the [`derivative` pipeline aggregation](elasticsearch://reference/aggregations/search-aggregations-pipeline-derivative-aggregation.md) to find the first order derivative of the counter `system.network.out.bytes` for each value of the field `beat.name`.

::::{note}
`derivative` or other pipeline aggregations may not work within `composite` aggregations. See [composite aggregations and pipeline aggregations](elasticsearch://reference/aggregations/search-aggregations-bucket-composite-aggregation.md#search-aggregations-bucket-composite-aggregation-pipeline-aggregations).
::::

```js
"aggregations": {
  "beat.name": {
    "terms": {
      "field": "beat.name"
    },
    "aggregations": {
      "buckets": {
        "date_histogram": {
          "field": "@timestamp",
          "fixed_interval": "5m"
        },
        "aggregations": {
          "@timestamp": {
            "max": {
              "field": "@timestamp"
            }
          },
          "bytes_out_average": {
            "avg": {
              "field": "system.network.out.bytes"
            }
          },
          "bytes_out_derivative": {
            "derivative": {
              "buckets_path": "bytes_out_average"
            }
          }
        }
      }
    }
  }
}
```

## Single bucket aggregations [aggs-single-dfeeds]

You can also use single bucket aggregations in {{dfeeds}}. The following example shows two `filter` aggregations, each gathering the number of unique entries for the `error` field.

```js
{
  "job_id":"servers-unique-errors",
  "indices": ["logs-*"],
  "aggregations": {
    "buckets": {
      "date_histogram": {
        "field": "time",
        "interval": "360s",
        "time_zone": "UTC"
      },
      "aggregations": {
        "time": {
          "max": {"field": "time"}
        }
        "server1": {
          "filter": {"term": {"source": "server-name-1"}},
          "aggregations": {
            "server1_error_count": {
              "value_count": {
                "field": "error"
              }
            }
          }
        },
        "server2": {
          "filter": {"term": {"source": "server-name-2"}},
          "aggregations": {
            "server2_error_count": {
              "value_count": {
                "field": "error"
              }
            }
          }
        }
      }
    }
  }
}
```

## Using `aggregate_metric_double` field type in {{dfeeds}} [aggs-amd-dfeeds]

::::{note}
It is not currently possible to use `aggregate_metric_double` type fields in {{dfeeds}} without aggregations.
::::

You can use fields with the [`aggregate_metric_double`](elasticsearch://reference/elasticsearch/mapping-reference/aggregate-metric-double.md) field type in a {{dfeed}} with aggregations. It is required to retrieve the `value_count` of the `aggregate_metric_double` filed in an aggregation and then use it as the `summary_count_field_name` to provide the correct count that represents the aggregation value.

In the following example, `presum` is an `aggregate_metric_double` type field that has all the possible metrics: `[ min, max, sum, value_count ]`. To use an `avg` aggregation on this field, you need to perform a `value_count` aggregation on `presum` and then set the field that contains the aggregated values `my_count` as the `summary_count_field_name`:

```js
{
  "analysis_config": {
    "bucket_span": "1h",
    "detectors": [
      {
        "function": "avg",
        "field_name": "my_avg"
      }
    ],
    "summary_count_field_name": "my_count" <1>
  },
  "data_description": {
    "time_field": "timestamp"
  },
  "datafeed_config": {
    "indices": [
      "my_index"
    ],
    "datafeed_id": "datafeed-id",
    "aggregations": {
      "buckets": {
        "date_histogram": {
          "field": "time",
          "fixed_interval": "360s",
          "time_zone": "UTC"
        },
        "aggregations": {
            "timestamp": {
                "max": {"field": "timestamp"}
            },
            "my_avg": {  <2>
                "avg": {
                    "field": "presum"
                }
             },
             "my_count": { <3>
                 "value_count": {
                     "field": "presum"
                 }
             }
          }
        }
     }
  }
}
```

1. The field `my_count` is set as the `summary_count_field_name`. This field contains aggregated values from the `presum` `aggregate_metric_double` type field (refer to footnote 3).
2. The `avg` aggregation to use on the `presum` `aggregate_metric_double` type field.
3. The `value_count` aggregation on the `presum` `aggregate_metric_double` type field. This aggregated field must be set as the `summary_count_field_name` (refer to footnote 1) to make it possible to use the `aggregate_metric_double` type field in another aggregation.
