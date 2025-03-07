---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/scripts-and-search-speed.html
---

# Scripts, caching, and search speed [scripts-and-search-speed]

{{es}} performs a number of optimizations to make using scripts as fast as possible. One important optimization is a script cache. The compiled script is placed in a cache so that requests that reference the script do not incur a compilation penalty.

Cache sizing is important. Your script cache should be large enough to hold all of the scripts that users need to be accessed concurrently.

If you see a large number of script cache evictions and a rising number of compilations in [node stats](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats), your cache might be too small.

All scripts are cached by default so that they only need to be recompiled when updates occur. By default, scripts do not have a time-based expiration. You can change this behavior by using the `script.cache.expire` setting. Use the `script.cache.max_size` setting to configure the size of the cache.

::::{note}
The size of scripts is limited to 65,535 bytes. Set the value of `script.max_size_in_bytes` to increase that soft limit. If your scripts are really large, then consider using a [native script engine](modules-scripting-engine.md).
::::



## Improving search speed [_improving_search_speed]

Scripts are incredibly useful, but can’t use {{es}}'s index structures or related optimizations. This relationship can sometimes result in slower search speeds.

If you often use scripts to transform indexed data, you can make search faster by transforming data during ingest instead. However, that often means slower index speeds. Let’s look at a practical example to illustrate how you can increase search speed.

When running searches, it’s common to sort results by the sum of two values. For example, consider an index named `my_test_scores` that contains test score data. This index includes two fields of type `long`:

* `math_score`
* `verbal_score`

You can run a query with a script that adds these values together. There’s nothing wrong with this approach, but the query will be slower because the script valuation occurs as part of the request. The following request returns documents where `grad_year` equals `2099`, and sorts by the results by the valuation of the script.

```console
GET /my_test_scores/_search
{
  "query": {
    "term": {
      "grad_year": "2099"
    }
  },
  "sort": [
    {
      "_script": {
        "type": "number",
        "script": {
          "source": "doc['math_score'].value + doc['verbal_score'].value"
        },
        "order": "desc"
      }
    }
  ]
}
```
%  TEST[s/^/PUT my_test_scores\n/]

If you’re searching a small index, then including the script as part of your search query can be a good solution. If you want to make search faster, you can perform this calculation during ingest and index the sum to a field instead.

First, we’ll add a new field to the index named `total_score`, which will contain sum of the `math_score` and `verbal_score` field values.

```console
PUT /my_test_scores/_mapping
{
  "properties": {
    "total_score": {
      "type": "long"
    }
  }
}
```
%  TEST[continued]

Next, use an [ingest pipeline](../../manage-data/ingest/transform-enrich/ingest-pipelines.md) containing the [script processor](elasticsearch://reference/ingestion-tools/enrich-processor/script-processor.md) to calculate the sum of `math_score` and `verbal_score` and index it in the `total_score` field.

```console
PUT _ingest/pipeline/my_test_scores_pipeline
{
  "description": "Calculates the total test score",
  "processors": [
    {
      "script": {
        "source": "ctx.total_score = (ctx.math_score + ctx.verbal_score)"
      }
    }
  ]
}
```
%  TEST[continued]

To update existing data, use this pipeline to [reindex](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) any documents from `my_test_scores` to a new index named `my_test_scores_2`.

```console
POST /_reindex
{
  "source": {
    "index": "my_test_scores"
  },
  "dest": {
    "index": "my_test_scores_2",
    "pipeline": "my_test_scores_pipeline"
  }
}
```
%  TEST[continued]

Continue using the pipeline to index any new documents to `my_test_scores_2`.

```console
POST /my_test_scores_2/_doc/?pipeline=my_test_scores_pipeline
{
  "student": "kimchy",
  "grad_year": "2099",
  "math_score": 1200,
  "verbal_score": 800
}
```
%  TEST[continued]

These changes slow the index process, but allow for faster searches. Instead of using a script, you can sort searches made on `my_test_scores_2` using the `total_score` field. The response is near real-time! Though this process slows ingest time, it greatly increases queries at search time.

```console
GET /my_test_scores_2/_search
{
  "query": {
    "term": {
      "grad_year": "2099"
    }
  },
  "sort": [
    {
      "total_score": {
        "order": "desc"
      }
    }
  ]
}
```
%  TEST[continued]

