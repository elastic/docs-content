---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-search-your-data-the-search-api.html
applies_to:
  stack:
  serverless:
products:
  - id: cloud-serverless
---
# The `_search` API [search-your-data]

::::{tip}
This page is focused on the `_search` API using Query DSL syntax. Refer to [](querying-for-search.md) for an overview of alternative Elastic query syntaxes for search use cases.
::::

A *search* consists of one or more queries that are combined and sent to {{es}}. Documents that match a search’s queries are returned in the *hits*, or *search results*, of the response.

A search may also contain additional information used to better process its queries. For example, a search may be limited to a specific index or only return a specific number of results.

You can use the [search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) to search and [aggregate](../../explore-analyze/query-filter/aggregations.md) data stored in {{es}} data streams or indices. The API’s `query` request body parameter accepts queries written in [Query DSL](../../explore-analyze/query-filter/languages/querydsl.md).


## Run a search [run-an-es-search]

The following request searches `my-index-000001` using a [`match`](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md) query. This query matches documents with a `user.id` value of `kimchy`.

```console
GET /my-index-000001/_search
{
  "query": {
    "match": {
      "user.id": "kimchy"
    }
  }
}
```

The API response returns the top 10 documents matching the query in the `hits.hits` property.

```console-result
{
  "took": 5,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.3862942,
    "hits": [
      {
        "_index": "my-index-000001",
        "_id": "kxWFcnMByiguvud1Z8vC",
        "_score": 1.3862942,
        "_source": {
          "@timestamp": "2099-11-15T14:12:12",
          "http": {
            "request": {
              "method": "get"
            },
            "response": {
              "bytes": 1070000,
              "status_code": 200
            },
            "version": "1.1"
          },
          "message": "GET /search HTTP/1.1 200 1070000",
          "source": {
            "ip": "127.0.0.1"
          },
          "user": {
            "id": "kimchy"
          }
        }
      }
    ]
  }
}
```


## Common search options [common-search-options]

You can use the following options to customize your searches.

**Query DSL**<br> [Query DSL](../../explore-analyze/query-filter/languages/querydsl.md) supports a variety of query types you can mix and match to get the results you want. Query types include:

* [Boolean](elasticsearch://reference/query-languages/query-dsl/query-dsl-bool-query.md) and other [compound queries](elasticsearch://reference/query-languages/query-dsl/compound-queries.md), which let you combine queries and match results based on multiple criteria
* [Term-level queries](elasticsearch://reference/query-languages/query-dsl/term-level-queries.md) for filtering and finding exact matches
* [Full text queries](elasticsearch://reference/query-languages/query-dsl/full-text-queries.md), which are commonly used in search engines
* [Geo](elasticsearch://reference/query-languages/query-dsl/geo-queries.md) and [spatial queries](elasticsearch://reference/query-languages/query-dsl/shape-queries.md)

**Aggregations**<br> You can use [search aggregations](../../explore-analyze/query-filter/aggregations.md) to get statistics and other analytics for your search results. Aggregations help you answer questions like:

* What’s the average response time for my servers?
* What are the top IP addresses hit by users on my network?
* What is the total transaction revenue by customer?

**Search multiple data streams and indices**<br> You can use comma-separated values and grep-like index patterns to search several data streams and indices in the same request. You can even boost search results from specific indices. See [Search multiple data streams and indices using a query](elasticsearch://reference/elasticsearch/rest-apis/search-multiple-data-streams-indices.md).

**Paginate search results**<br> By default, searches return only the top 10 matching hits. To retrieve more or fewer documents, see [Paginate search results](elasticsearch://reference/elasticsearch/rest-apis/paginate-search-results.md).

**Retrieve selected fields**<br> The search response’s `hits.hits` property includes the full document [`_source`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md) for each hit. To retrieve only a subset of the `_source` or other fields, see [Retrieve selected fields](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md).

**Sort search results**<br> By default, search hits are sorted by `_score`, a [relevance score](../../explore-analyze/query-filter/languages/querydsl.md#relevance-scores) that measures how well each document matches the query. To customize the calculation of these scores, use the [`script_score`](elasticsearch://reference/query-languages/query-dsl/query-dsl-script-score-query.md) query. To sort search hits by other field values, see [Sort search results](elasticsearch://reference/elasticsearch/rest-apis/sort-search-results.md).

**Run an async search**<br> {{es}} searches are designed to run on large volumes of data quickly, often returning results in milliseconds. For this reason, searches are *synchronous* by default. The search request waits for complete results before returning a response.

However, complete results can take longer for searches across large data sets or [multiple clusters](cross-cluster-search.md).

To avoid long waits, you can run an *asynchronous*, or *async*, search instead. An [async search](async-search-api.md) lets you retrieve partial results for a long-running search now and get complete results later.


## Define fields that exist only in a query [run-search-runtime-fields]

Instead of indexing your data and then searching it, you can define [runtime fields](../../manage-data/data-store/mapping/define-runtime-fields-in-search-request.md) that only exist as part of your search query. You specify a `runtime_mappings` section in your search request to define the runtime field, which can optionally include a Painless script.

For example, the following query defines a runtime field called `day_of_week`. The included script calculates the day of the week based on the value of the `@timestamp` field, and uses `emit` to return the calculated value.

The query also includes a [terms aggregation](elasticsearch://reference/aggregations/search-aggregations-bucket-terms-aggregation.md) that operates on `day_of_week`.

```console
GET /my-index-000001/_search
{
  "runtime_mappings": {
    "day_of_week": {
      "type": "keyword",
      "script": {
        "source":
        """emit(doc['@timestamp'].value.dayOfWeekEnum
        .getDisplayName(TextStyle.FULL, Locale.ENGLISH))"""
      }
    }
  },
  "aggs": {
    "day_of_week": {
      "terms": {
        "field": "day_of_week"
      }
    }
  }
}
```

The response includes an aggregation based on the `day_of_week` runtime field. Under `buckets` is a `key` with a value of `Sunday`. The query dynamically calculated this value based on the script defined in the `day_of_week` runtime field without ever indexing the field.

```console-result
{
  ...
  ***
  "aggregations" : {
    "day_of_week" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : "Sunday",
          "doc_count" : 5
        }
      ]
    }
  }
}
```


## Search timeout [search-timeout]

By default, search requests don’t time out. The request waits for complete results from each shard before returning a response.

While [async search](async-search-api.md) is designed for long-running searches, you can also use the `timeout` parameter to specify a duration you’d like to wait on each shard to complete. Each shard collects hits within the specified time period. If collection isn’t finished when the period ends, {{es}} uses only the hits accumulated up to that point. The overall latency of a search request depends on the number of shards needed for the search and the number of concurrent shard requests.

```console
GET /my-index-000001/_search
{
  "timeout": "2s",
  "query": {
    "match": {
      "user.id": "kimchy"
    }
  }
}
```

To set a cluster-wide default timeout for all search requests, configure `search.default_search_timeout` using the [cluster settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). This global timeout duration is used if no `timeout` argument is passed in the request. If the global search timeout expires before the search request finishes, the request is cancelled using [task cancellation](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-tasks). The `search.default_search_timeout` setting defaults to `-1` (no timeout).


## Search cancellation [global-search-cancellation]

You can cancel a search request using the [task management API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-tasks). {{es}} also automatically cancels a search request when your client’s HTTP connection closes. We recommend you set up your client to close HTTP connections when a search request is aborted or times out.


## Track total hits [track-total-hits]

Generally the total hit count can’t be computed accurately without visiting all matches, which is costly for queries that match lots of documents. The `track_total_hits` parameter allows you to control how the total number of hits should be tracked. Given that it is often enough to have a lower bound of the number of hits, such as "there are at least 10000 hits", the default is set to `10,000`. This means that requests will count the total hit accurately up to `10,000` hits. It is a good trade off to speed up searches if you don’t need the accurate number of hits after a certain threshold.

When set to `true` the search response will always track the number of hits that match the query accurately (e.g. `total.relation` will always be equal to `"eq"` when `track_total_hits` is set to true). Otherwise the `"total.relation"` returned in the `"total"` object in the search response determines how the `"total.value"` should be interpreted. A value of `"gte"` means that the `"total.value"` is a lower bound of the total hits that match the query and a value of `"eq"` indicates that `"total.value"` is the accurate count.

```console
GET my-index-000001/_search
{
  "track_total_hits": true,
  "query": {
    "match" : {
      "user.id" : "elkbee"
    }
  }
}
```

... returns:

```console-result
{
  "_shards": ...
  "timed_out": false,
  "took": 100,
  "hits": {
    "max_score": 1.0,
    "total" : {
      "value": 2048,    <1>
      "relation": "eq"  <2>
    },
    "hits": ...
  }
}
```

1. The total number of hits that match the query.
2. The count is accurate (e.g. `"eq"` means equals).


It is also possible to set `track_total_hits` to an integer. For instance the following query will accurately track the total hit count that match the query up to 100 documents:

```console
GET my-index-000001/_search
{
  "track_total_hits": 100,
  "query": {
    "match": {
      "user.id": "elkbee"
    }
  }
}
```

The `hits.total.relation` in the response will indicate if the value returned in `hits.total.value` is accurate (`"eq"`) or a lower bound of the total (`"gte"`).

For instance the following response:

```console-result
{
  "_shards": ...
  "timed_out": false,
  "took": 30,
  "hits": {
    "max_score": 1.0,
    "total": {
      "value": 42,         <1>
      "relation": "eq"     <2>
    },
    "hits": ...
  }
}
```

1. 42 documents match the query
2. and the count is accurate (`"eq"`)


... indicates that the number of hits returned in the `total` is accurate.

If the total number of hits that match the query is greater than the value set in `track_total_hits`, the total hits in the response will indicate that the returned value is a lower bound:

```console-result
{
  "_shards": ...
  "hits": {
    "max_score": 1.0,
    "total": {
      "value": 100,         <1>
      "relation": "gte"     <2>
    },
    "hits": ...
  }
}
```

1. There are at least 100 documents that match the query
2. This is a lower bound (`"gte"`).


If you don’t need to track the total number of hits at all you can improve query times by setting this option to `false`:

```console
GET my-index-000001/_search
{
  "track_total_hits": false,
  "query": {
    "match": {
      "user.id": "elkbee"
    }
  }
}
```

... returns:

```console-result
{
  "_shards": ...
  "timed_out": false,
  "took": 10,
  "hits": {             <1>
    "max_score": 1.0,
    "hits": ...
  }
}
```

1. The total number of hits is unknown.


Finally you can force an accurate count by setting `"track_total_hits"` to `true` in the request.

::::{tip}
The `track_total_hits` parameter allows you to trade hit count accuracy for performance. In general the lower the value of `track_total_hits` the faster the query will be, with `false` returning the fastest results. Setting `track_total_hits` to true will cause {{es}} to return exact hit counts, which could hurt query performance because it disables the [Max WAND](https://www.elastic.co/blog/faster-retrieval-of-top-hits-in-elasticsearch-with-block-max-wand) optimization.

::::



## Quickly check for matching docs [quickly-check-for-matching-docs]

If you only want to know if there are any documents matching a specific query, you can set the `size` to `0` to indicate that we are not interested in the search results. You can also set `terminate_after` to `1` to indicate that the query execution can be terminated whenever the first matching document was found (per shard).

```console
GET /_search?q=user.id:elkbee&size=0&terminate_after=1
```

::::{note}
`terminate_after` is always applied **after** the [`post_filter`](elasticsearch://reference/elasticsearch/rest-apis/filter-search-results.md#post-filter) and stops the query as well as the aggregation executions when enough hits have been collected on the shard. Though the doc count on aggregations may not reflect the `hits.total` in the response since aggregations are applied **before** the post filtering.
::::


The response will not contain any hits as the `size` was set to `0`. The `hits.total` will be either equal to `0`, indicating that there were no matching documents, or greater than `0` meaning that there were at least as many documents matching the query when it was early terminated. Also if the query was terminated early, the `terminated_early` flag will be set to `true` in the response. Some queries are able to retrieve the hits count directly from the index statistics, which is much faster as it does not require executing the query. In those situations, no documents are collected, the returned `total.hits` will be higher than `terminate_after`, and `terminated_early` will be set to `false`.

```console-result
{
  "took": 3,
  "timed_out": false,
  "terminated_early": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped" : 0,
    "failed": 0
  },
  "hits": {
    "total" : {
        "value": 1,
        "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
```

The `took` time in the response contains the milliseconds that this request took for processing, beginning quickly after the node received the query, up until all search related work is done and before the above JSON is returned to the client. This means it includes the time spent waiting in thread pools, executing a distributed search across the whole cluster and gathering all the results.

`_shards.failed` indicates how many shards did not successfully return results for the search request. `_shards.failures` is returned only when shard failures occur and contains an array of objects with details such as the index name, shard number, node ID, and the reason for the failure.

```console-result
"_shards": {
  "total": 5,
  "successful": 1,
  "skipped": 0,
  "failed": 4,
  "failures": [
    {
      "shard": 0,
      "index": "<index_name>",
      "node": "<node_id>",
      "reason": {
        "type": "node_not_connected_exception",
        "reason": "[<node_name>][<ip>:<port>] Node not connected"
      }
    },
    {
      "shard": 1,
      "index": "<index_name>",
      "node": null,
      "reason": {
        "type": "no_shard_available_action_exception",
        "index_uuid": "<index_uuid>",
        "shard": "1",
        "index": "<index_name>"
      }
    }
  ]
}
```

Shard failures are deduplicated by `index` and `exception`. If the same exception occurs multiple times on the same index, it is reported only once in `_shards.failures`, even if multiple shards failed. As a result, the number of entries in `_shards.failures` can be lower than the value in `_shards.failed`.
