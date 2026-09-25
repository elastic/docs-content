---
navigation_title: Searches
description: Diagnose and fix common Elasticsearch search problems including missing results, unexpected ordering, slow queries, and relevance issues.
type: troubleshooting
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/troubleshooting-searches.html
  - https://www.elastic.co/guide/en/serverless/current/devtools-dev-tools-troubleshooting.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Troubleshoot searches [troubleshooting-searches]

When you query your data, {{es}} might return an error, no search results, or results in an unexpected order. This guide describes how to troubleshoot searches.


## Ensure the data stream, index, or alias exists [troubleshooting-searches-exists]

{{es}} returns an `index_not_found_exception` when the data stream, index or alias you try to query does not exist. This can happen when you misspell the name or when the data has been indexed to a different data stream or index.

Use the [exists API]({{es-apis}}operation/operation-indices-exists) to check whether a data stream, index, or alias exists:

```console
HEAD my-data-stream
```

Use the [data stream stats API]({{es-apis}}operation/operation-indices-data-streams-stats-1) to list all data streams:

```console
GET /_data_stream/_stats?human=true
```

Use the [get index API]({{es-apis}}operation/operation-indices-get) to list all indices and their aliases:

```console
GET _all?filter_path=*.aliases
```

Instead of an error, it is possible to retrieve partial search results if some of the indices you’re querying are unavailable. Set `ignore_unavailable` to `true`:

```console
GET /my-alias/_search?ignore_unavailable=true
```


## Ensure the data stream or index contains data [troubleshooting-searches-data]

When a search request returns no hits, the data stream or index may contain no data. This can happen when there is a data ingestion issue. For example, the data may have been indexed to a data stream or index with another name.

Use the [count API]({{es-apis}}operation/operation-count) to retrieve the number of documents in a data stream or index. Check that `count` in the response is not 0.

```console
GET /my-index-000001/_count
```

::::{note}
When getting no search results in {{kib}}, check that you have selected the correct data view and a valid time range. Also, ensure the data view has been configured with the correct time field.
::::



## Check that the field exists and its capabilities [troubleshooting-searches-field-exists-caps]

Querying a field that does not exist will not return any results. Use the [field capabilities API]({{es-apis}}operation/operation-field-caps) to check whether a field exists:

```console
GET /my-index-000001/_field_caps?fields=my-field
```

If the field does not exist, check the data ingestion process. The field may have a different name.

If the field exists, the request will return the field’s type and whether it is searchable and aggregatable.

```console-response
{
  "indices": [
    "my-index-000001"
  ],
  "fields": {
    "my-field": {
      "keyword": {
        "type": "keyword",         <1>
        "metadata_field": false,
        "searchable": true,        <2>
        "aggregatable": true       <3>
      }
    }
  }
}
```

1. The field is of type `keyword` in this index.
2. The field is searchable in this index.
3. The field is aggregatable in this index.



## Check the field’s mappings [troubleshooting-searches-mappings]

A field’s capabilities are determined by its [mapping](../../manage-data/data-store/mapping.md). To retrieve the mapping, use the [get mapping API](../../manage-data/data-store/mapping.md):

```console
GET /my-index-000001/_mappings
```

If you query a `text` field, pay attention to the analyzer that may have been configured. You can use the [analyze API]({{es-apis}}operation/operation-indices-analyze) to check how a field’s analyzer processes values and query terms:

```console
GET /my-index-000001/_analyze
{
  "field" : "my-field",
  "text" : "this is a test"
}
```

To change the mapping of an existing field, refer to [Changing the mapping of a field](../../manage-data/data-store/mapping.md#updating-field-mappings).


## Check the field’s values [troubleshooting-check-field-values]

Use the [`exists` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-exists-query.md) to check whether there are documents that return a value for a field. Check that `count` in the response is not 0.

```console
GET /my-index-000001/_count
{
  "query": {
    "exists": {
      "field": "my-field"
    }
  }
}
```

If the field is aggregatable, you can use [aggregations](../../explore-analyze/query-filter/aggregations.md) to check the field’s values. For `keyword` fields, you can use a [terms aggregation](elasticsearch://reference/aggregations/search-aggregations-bucket-terms-aggregation.md) to retrieve the field’s most common values:

```console
GET /my-index-000001/_search?filter_path=aggregations
{
  "size": 0,
  "aggs": {
    "top_values": {
      "terms": {
        "field": "my-field",
        "size": 10
      }
    }
  }
}
```

For numeric fields, you can use the [stats aggregation](elasticsearch://reference/aggregations/search-aggregations-metrics-stats-aggregation.md) to get an idea of the field’s value distribution:

```console
GET my-index-000001/_search?filter_path=aggregations
{
  "aggs": {
    "my-num-field-stats": {
      "stats": {
        "field": "my-num-field"
      }
    }
  }
}
```

If the field does not return any values, check the data ingestion process. The field may have a different name.


## Check the latest value [troubleshooting-searches-latest-data]

For time-series data, confirm there is non-filtered data within the attempted time range. For example, if you are trying to query the latest data for the `@timestamp` field, run the following to see if the max `@timestamp` falls within the attempted range:

```console
GET my-index-000001/_search?sort=@timestamp:desc&size=1
```


## Validate, explain, and profile queries [troubleshooting-searches-validate-explain-profile]

When a query returns unexpected results, {{es}} offers several tools to investigate why.

The [validate API]({{es-apis}}operation/operation-indices-validate-query) enables you to validate a query. Use the `rewrite` parameter to return the Lucene query an {{es}} query is rewritten into:

```console
GET /my-index-000001/_validate/query?rewrite=true
{
  "query": {
    "match": {
      "user.id": {
        "query": "kimchy",
        "fuzziness": "auto"
      }
    }
  }
}
```

Use the [explain API]({{es-apis}}operation/operation-explain) to find out why a specific document matches or doesn’t match a query. For deeper relevance debugging, refer to [Troubleshoot relevance quality](#troubleshooting-relevance-quality).

```console
GET /my-index-000001/_explain/0
{
  "query" : {
    "match" : { "message" : "elasticsearch" }
  }
}
```

The [profile API](elasticsearch://reference/elasticsearch/rest-apis/search-profile.md) provides detailed timing information about a search request. For a visual representation of the results, use the [Search Profiler](../../explore-analyze/query-filter/tools/search-profiler.md) in {{kib}}.

::::{note}
To troubleshoot queries in {{kib}}, select **Inspect** in the toolbar. Next, select **Request**. You can now copy the query {{kib}} sent to {{es}} for further analysis in Console.
::::



## Check index settings [troubleshooting-searches-settings]

[Index settings](elasticsearch://reference/elasticsearch/index-settings/index.md) can influence search results. For example, the `index.query.default_field` setting, which determines the field that is queried when a query specifies no explicit field. Use the [get index settings API]({{es-apis}}operation/operation-indices-get-settings) to retrieve the settings for an index:

```console
GET /my-index-000001/_settings
```

You can update dynamic index settings with the [update index settings API]({{es-apis}}operation/operation-indices-put-settings). [Changing dynamic index settings for a data stream](../../manage-data/data-store/data-streams/modify-data-stream.md#change-dynamic-index-setting-for-a-data-stream) requires changing the index template used by the data stream.

For static settings, you need to create a new index with the correct settings. Next, you can reindex the data into that index. For data streams, refer to [Change a static index setting for a data stream](../../manage-data/data-store/data-streams/modify-data-stream.md#change-static-index-setting-for-a-data-stream).


## Find slow queries [troubleshooting-slow-searches]
```{applies_to}
stack:
```

Start with [slow logs](/deploy-manage/monitor/logging-configuration/slow-logs.md), which pinpoint the search requests that take too long to run. Once you've identified a slow request, determine where it comes from. How you do this depends on your version.

{applies_to}`stack: preview 9.4` Use [query logging](/deploy-manage/monitor/logging-configuration/query-logs.md) to determine the query source. A single configuration captures end-to-end request duration across all query types, including Query DSL, {{esql}}, EQL, and SQL.

If you can't use query logging, enable [audit logging](/deploy-manage/security/logging-configuration/enabling-audit-logs.md) instead to determine the query source. Add the following settings to the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) configuration file to trace queries. The resulting logging is verbose, so disable these settings when not troubleshooting.

```yaml
xpack.security.audit.enabled: true
xpack.security.audit.logfile.events.include: _all
xpack.security.audit.logfile.events.emit_request_body: true
```

Refer to [Advanced tuning: finding and fixing slow Elasticsearch queries](https://www.elastic.co/blog/advanced-tuning-finding-and-fixing-slow-elasticsearch-queries) for more information.

For {{esql}}-specific slow query diagnosis and prevention, refer to [Optimize {{esql}} query performance](elasticsearch://reference/query-languages/esql/esql-query-performance.md).

## Troubleshoot relevance quality [troubleshooting-relevance-quality]

Use this section when your search returns results but they're in the wrong order, irrelevant, or missing expected matches. These symptoms point to a relevance problem rather than a technical error.

### Diagnose scoring with the Explain API [troubleshooting-relevance-explain]

When a document ranks unexpectedly high or low, use the [Explain API]({{es-apis}}operation/operation-explain) to see exactly how {{es}} calculated its score. Replace `2` with the `_id` of the document you want to inspect:

```console
GET /my-index-000001/_explain/2
{
  "query": {
    "match": {
      "title": "search relevance"
    }
  }
}
```

The response shows whether the document matched and breaks the score down by term and field:

```console-result
{
  "_index": "my-index-000001",
  "_id": "2",
  "matched": true, <1>
  "explanation": {
    "value": 2.1845279,
    "description": "sum of:",
    "details": [
      {
        "value": 1.0922639,
        "description": "weight(title:search in 1) [PerFieldSimilarity], result of:",
        "details": [
          {
            "value": 1.0922639,
            "description": "score(freq=1.0), computed as boost * idf * tf from:",
            "details": [
              { "value": 2.2,       "description": "boost" }, <2>
              { "value": 1.2039728, "description": "idf, computed as log(1 + (N - n + 0.5) / (n + 0.5))" }, <3>
              { "value": 0.4123711, "description": "tf, computed as freq / (freq + k1 * (1 - b + b * dl / avgdl))" } <3>
            ]
          }
        ]
      },
      {
        "value": 1.0922639,
        "description": "weight(title:relevance in 1) [PerFieldSimilarity], result of: ..."
      }
    ]
  }
}
```
1. Confirms the document matched the query.
2. A high `boost` value (here `2.2`) means the field mapping or query applied a field boost — verify this is intentional.
3. Each entry in `details` shows one term's contribution. `boost`, `idf` (how rare the term is), and `tf` (how often it appears) multiply together to produce the term score.

When a document does not match at all:

```console
GET /my-index-000001/_explain/4
{
  "query": {
    "match": {
      "title": "search relevance"
    }
  }
}
```

```console-result
{
  "_index": "my-index-000001",
  "_id": "4",
  "matched": false,
  "explanation": {
    "value": 0.0,
    "description": "No matching clauses",
    "details": [
      { "value": 0.0, "description": "no match on optional clause (title:search)" },
      { "value": 0.0, "description": "no match on optional clause (title:relevance)" }
    ]
  }
}
```

`"matched": false` with `"No matching clauses"` means the tokens in the query did not appear in the indexed field. This is usually a token mismatch — see [Fix token mismatches between index and query](#troubleshooting-relevance-tokens).

For a visual representation, use the [Search Profiler](../../explore-analyze/query-filter/tools/search-profiler.md) in {{kib}}.

### Fix token mismatches between index and query [troubleshooting-relevance-tokens]

When a query fails to match an expected document, the index and query might be tokenizing text differently. Use the [Analyze API]({{es-apis}}operation/operation-indices-analyze) to inspect what tokens {{es}} produces for a given field and text.

First, check how the indexed field tokenizes the text:

```console
GET /my-index-000001/_analyze
{
  "field": "title",
  "text": "Getting started with Elasticsearch"
}
```

```console-result
{
  "tokens": [
    { "token": "getting",       "position": 0 },
    { "token": "start",         "position": 1 },
    { "token": "with",          "position": 2 },
    { "token": "elasticsearch", "position": 3 }
  ]
}
```

Then run the same text through the analyzer your query uses. If your `title` field uses the `english` analyzer but the query runs with `standard` (the default for `match`), the tokens differ:

```console
GET /my-index-000001/_analyze
{
  "analyzer": "standard",
  "text": "Getting started with Elasticsearch"
}
```

```console-result
{
  "tokens": [
    { "token": "getting",       "position": 0 },
    { "token": "started",       "position": 1 },
    { "token": "with",          "position": 2 },
    { "token": "elasticsearch", "position": 3 }
  ]
}
```

The index produced `"start"` (stemmed by the English analyzer) but the query produces `"started"`. These tokens don't match, so the document won't appear in results. To fix this, set `search_analyzer` on the field to match the index analyzer, or explicitly pass `analyzer` in the query.

Refer to [Test an analyzer](../../manage-data/data-store/text-analysis/test-an-analyzer.md) for a detailed walkthrough.

### Fix synonyms not applying [troubleshooting-relevance-synonyms]

Synonyms only expand queries when the synonym filter is part of the **search analyzer**, not the index analyzer. If synonyms aren't matching, check:

1. Use the Analyze API with your index's search analyzer to confirm the synonym expansion is happening:

   ```console
   GET /my-index-000001/_analyze
   {
     "analyzer": "my_search_analyzer",
     "text": "car"
   }
   ```

   If synonyms are working, the response includes extra tokens with `"type": "SYNONYM"`:

   ```console-result
   {
     "tokens": [
       { "token": "car",        "position": 0, "type": "<ALPHANUM>" },
       { "token": "automobile", "position": 0, "type": "SYNONYM" },
       { "token": "vehicle",    "position": 0, "type": "SYNONYM" }
     ]
   }
   ```

   If you only see the original token and no `SYNONYM` entries, the synonym filter is not part of the search analyzer chain.

2. If you updated the synonym set, confirm whether you need to reload or reindex:
   - Synonym sets managed via the [Synonyms API]({{es-apis}}group/endpoint-synonyms) can be reloaded without reindexing. Call `POST /<index>/_reload_search_analyzers` to apply the update.
   - Custom synonym files configured as index-time analyzers require a full reindex to take effect on already-indexed documents. If the file is configured as a search-time analyzer with `updateable: true`, you can reload it without reindexing using the same reload API.

Refer to [Search with synonyms](../../solutions/search/full-text/search-with-synonyms.md) for setup and reload guidance.

### Fix boosting not working as expected [troubleshooting-relevance-boosting]

If boosted fields or documents aren't ranking as expected, use the Explain API to confirm the boost applies. Common causes:

- **Field boosts in `multi_match`**: verify the `^` syntax is correct and the field exists in the mapping.
- **`function_score`**: check that the filter on each function matches the documents you expect.
- **`script_score`**: confirm the script returns the value you intend. Log the script output with a test query.

Run your query with `"explain": true` in the request body to see per-result score breakdowns inline:

```console
GET /my-index-000001/_search
{
  "explain": true,
  "query": {
    "multi_match": {
      "query": "search relevance",
      "fields": ["title^3", "body"]
    }
  }
}
```

Each result in the response includes an `_explanation` block showing how the boost affected the score:

```console-result
{
  "hits": {
    "hits": [
      {
        "_id": "2",
        "_score": 6.553584,
        "_explanation": {
          "value": 6.553584,
          "description": "max of:",
          "details": [
            {
              "value": 6.553584,
              "description": "sum of:",
              "details": [
                {
                  "value": 3.276792,
                  "description": "weight(title:search in 1) [PerFieldSimilarity], result of:",
                  "details": [
                    {
                      "value": 3.276792,
                      "description": "score(freq=1.0), computed as boost * idf * tf from:",
                      "details": [
                        { "value": 6.6000004, "description": "boost" },
                        { "value": 1.2039728, "description": "idf" },
                        { "value": 0.4123711, "description": "tf" }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      }
    ]
  }
}
```

The `boost` value here is `6.6` (the BM25 default `2.2` multiplied by the `^3` field boost). If you don't see the boost you configured reflected in this value, verify the field name in the `fields` array matches the mapping exactly.

### Fix the wrong fields being searched [troubleshooting-relevance-fields]

When a `multi_match` query returns irrelevant results, the field list might be too broad or misconfigured. Check:

- The `fields` array in your `multi_match`: remove low-signal fields or add explicit boosts to prioritize the right ones.
- Whether `copy_to` is pulling unrelated content into a combined field. Use the [Get mapping API]({{es-apis}}operation/operation-indices-get-mapping) to inspect which fields copy into your target field.
- The `type` parameter: `best_fields` ranks by the single best matching field, while `most_fields` sums scores across fields. Switch between them to see which fits your use case.

### Fix poor semantic search results [troubleshooting-relevance-semantic]

If semantic search returns results that are off-topic or miss obvious matches, the most common cause is an embedding model mismatch: documents and queries were embedded by different models or at different times.

Check the following:

- Confirm the same inference endpoint handles both indexing and querying.
- If you changed the model or endpoint, reindex the affected documents so their embeddings match the current model.
- Use the `_explain` API to verify that the vector similarity scores are non-zero for documents you expect to match.
- If embeddings are missing or zero-length, the inference pipeline might have failed silently during indexing.
