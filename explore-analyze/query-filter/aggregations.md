---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html
---

# Aggregations [search-aggregations]

An aggregation summarizes your data as metrics, statistics, or other analytics. Aggregations help you answer questions like:

* What’s the average load time for my website?
* Who are my most valuable customers based on transaction volume?
* What would be considered a large file on my network?
* How many products are in each product category?

{{es}} organizes aggregations into three categories:

* [Metric](elasticsearch://reference/data-analysis/aggregations/metrics.md) aggregations that calculate metrics, such as a sum or average, from field values.
* [Bucket](elasticsearch://reference/data-analysis/aggregations/bucket.md) aggregations that group documents into buckets, also called bins, based on field values, ranges, or other criteria.
* [Pipeline](elasticsearch://reference/data-analysis/aggregations/pipeline.md) aggregations that take input from other aggregations instead of documents or fields.

## Run an aggregation [run-an-agg]

You can run aggregations as part of a [search](../../solutions/search/querying-for-search.md) by specifying the [search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)'s `aggs` parameter. The following search runs a [terms aggregation](elasticsearch://reference/data-analysis/aggregations/search-aggregations-bucket-terms-aggregation.md) on `my-field`:

```console
GET /my-index-000001/_search
{
  "aggs": {
    "my-agg-name": {
      "terms": {
        "field": "my-field"
      }
    }
  }
}
```
%  TEST[setup:my_index]
%  TEST[s/my-field/http.request.method/]

Aggregation results are in the response’s `aggregations` object:

```console-result
{
  "took": 78,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 5,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [...]
  },
  "aggregations": {
    "my-agg-name": {                           <1>
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": []
    }
  }
}
```

1. Results for the `my-agg-name` aggregation.
%  TESTRESPONSE[s/"took": 78/"took": "$body.took"/]
%  TESTRESPONSE[s/...$/"took": "$body.took", "timed_out": false, "_shards": "$body._shards", /]
%  TESTRESPONSE[s/"hits": [...]/"hits": "$body.hits.hits"/]
%  TESTRESPONSE[s/"buckets": []/"buckets":[{"key":"get","doc_count":5}]/]

## Change an aggregation’s scope [change-agg-scope]

Use the `query` parameter to limit the documents on which an aggregation runs:

```console
GET /my-index-000001/_search
{
  "query": {
    "range": {
      "@timestamp": {
        "gte": "now-1d/d",
        "lt": "now/d"
      }
    }
  },
  "aggs": {
    "my-agg-name": {
      "terms": {
        "field": "my-field"
      }
    }
  }
}
```
%  TEST[setup:my_index]
%  TEST[s/my-field/http.request.method/]

## Return only aggregation results [return-only-agg-results]

By default, searches containing an aggregation return both search hits and aggregation results. To return only aggregation results, set `size` to `0`:

```console
GET /my-index-000001/_search
{
  "size": 0,
  "aggs": {
    "my-agg-name": {
      "terms": {
        "field": "my-field"
      }
    }
  }
}
```
%  TEST[setup:my_index]
%  TEST[s/my-field/http.request.method/]

## Run multiple aggregations [run-multiple-aggs]

You can specify multiple aggregations in the same request:

```console
GET /my-index-000001/_search
{
  "aggs": {
    "my-first-agg-name": {
      "terms": {
        "field": "my-field"
      }
    },
    "my-second-agg-name": {
      "avg": {
        "field": "my-other-field"
      }
    }
  }
}
```
%  TEST[setup:my_index]
%  TEST[s/my-field/http.request.method/]
%  TEST[s/my-other-field/http.response.bytes/]

## Run sub-aggregations [run-sub-aggs]

Bucket aggregations support bucket or metric sub-aggregations. For example, a terms aggregation with an [avg](elasticsearch://reference/data-analysis/aggregations/search-aggregations-metrics-avg-aggregation.md) sub-aggregation calculates an average value for each bucket of documents. There is no level or depth limit for nesting sub-aggregations.

```console
GET /my-index-000001/_search
{
  "aggs": {
    "my-agg-name": {
      "terms": {
        "field": "my-field"
      },
      "aggs": {
        "my-sub-agg-name": {
          "avg": {
            "field": "my-other-field"
          }
        }
      }
    }
  }
}
```
%  TEST[setup:my_index]
%  TEST[s/_search/_search?size=0/]
%  TEST[s/my-field/http.request.method/]
%  TEST[s/my-other-field/http.response.bytes/]

The response nests sub-aggregation results under their parent aggregation:

```console-result
{
  ...
  "aggregations": {
    "my-agg-name": {                           <1>
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "foo",
          "doc_count": 5,
          "my-sub-agg-name": {                 <2>
            "value": 75.0
          }
        }
      ]
    }
  }
}
```

1. Results for the parent aggregation, `my-agg-name`.
2. Results for `my-agg-name`'s sub-aggregation, `my-sub-agg-name`.
%  TESTRESPONSE[s/.../"took": "$body.took", "timed_out": false, "_shards": "$body._shards", "hits": "$body.hits",/]
%  TESTRESPONSE[s/"key": "foo"/"key": "get"/]
%  TESTRESPONSE[s/"value": 75.0/"value": $body.aggregations.my-agg-name.buckets.0.my-sub-agg-name.value/]

## Add custom metadata [add-metadata-to-an-agg]

Use the `meta` object to associate custom metadata with an aggregation:

```console
GET /my-index-000001/_search
{
  "aggs": {
    "my-agg-name": {
      "terms": {
        "field": "my-field"
      },
      "meta": {
        "my-metadata-field": "foo"
      }
    }
  }
}
```
%  TEST[setup:my_index]
%  TEST[s/_search/_search?size=0/]

The response returns the `meta` object in place:

```console-result
{
  ...
  "aggregations": {
    "my-agg-name": {
      "meta": {
        "my-metadata-field": "foo"
      },
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": []
    }
  }
}
```
%  TESTRESPONSE[s/.../"took": "$body.took", "timed_out": false, "_shards": "$body._shards", "hits": "$body.hits",/]

## Return the aggregation type [return-agg-type]

By default, aggregation results include the aggregation’s name but not its type. To return the aggregation type, use the `typed_keys` query parameter.

```console
GET /my-index-000001/_search?typed_keys
{
  "aggs": {
    "my-agg-name": {
      "histogram": {
        "field": "my-field",
        "interval": 1000
      }
    }
  }
}
```
%  TEST[setup:my_index]
%  TEST[s/typed_keys/typed_keys&size=0/]
%  TEST[s/my-field/http.response.bytes/]

The response returns the aggregation type as a prefix to the aggregation’s name.

::::{important}
Some aggregations return a different aggregation type from the type in the request. For example, the terms, [significant terms](elasticsearch://reference/data-analysis/aggregations/search-aggregations-bucket-significantterms-aggregation.md), and [percentiles](elasticsearch://reference/data-analysis/aggregations/search-aggregations-metrics-percentile-aggregation.md) aggregations return different aggregations types depending on the data type of the aggregated field.
::::

```console-result
{
  ...
  "aggregations": {
    "histogram#my-agg-name": {                 <1>
      "buckets": []
    }
  }
}
```

1. The aggregation type, `histogram`, followed by a `#` separator and the aggregation’s name, `my-agg-name`.
%  TESTRESPONSE[s/.../"took": "$body.took", "timed_out": false, "_shards": "$body._shards", "hits": "$body.hits",/]
%  TESTRESPONSE[s/"buckets": []/"buckets":[{"key":1070000.0,"doc_count":5}]/]

## Use scripts in an aggregation [use-scripts-in-an-agg]

When a field doesn’t exactly match the aggregation you need, you should aggregate on a [runtime field](../../manage-data/data-store/mapping/runtime-fields.md):

```console
GET /my-index-000001/_search?size=0
{
  "runtime_mappings": {
    "message.length": {
      "type": "long",
      "script": "emit(doc['message.keyword'].value.length())"
    }
  },
  "aggs": {
    "message_length": {
      "histogram": {
        "interval": 10,
        "field": "message.length"
      }
    }
  }
}
```
%  TEST[setup:my_index]

Scripts calculate field values dynamically, which adds a little overhead to the aggregation. In addition to the time spent calculating, some aggregations like [`terms`](elasticsearch://reference/data-analysis/aggregations/search-aggregations-bucket-terms-aggregation.md) and [`filters`](elasticsearch://reference/data-analysis/aggregations/search-aggregations-bucket-filters-aggregation.md) can’t use some of their optimizations with runtime fields. In total, performance costs for using a runtime field varies from aggregation to aggregation.

## Aggregation caches [agg-caches]

For faster responses, {{es}} caches the results of frequently run aggregations in the [shard request cache](elasticsearch://reference/elasticsearch/configuration-reference/shard-request-cache-settings.md). To get cached results, use the same [`preference` string](elasticsearch://reference/elasticsearch/rest-apis/search-shard-routing.md#shard-and-node-preference) for each search. If you don’t need search hits, [set `size` to `0`](#return-only-agg-results) to avoid filling the cache.

{{es}} routes searches with the same preference string to the same shards. If the shards' data doesn’t change between searches, the shards return cached aggregation results.

## Limits for `long` values [limits-for-long-values]

When running aggregations, {{es}} uses [`double`](elasticsearch://reference/elasticsearch/mapping-reference/number.md) values to hold and represent numeric data. As a result, aggregations on [`long`](elasticsearch://reference/elasticsearch/mapping-reference/number.md) numbers greater than `253` are approximate.
