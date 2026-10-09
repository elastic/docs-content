---
navigation_title: Search relevance
meta_title: Troubleshoot search relevance in Elasticsearch
description: Diagnose and fix common Elasticsearch search relevance problems including unexpected scoring, token mismatches, synonyms not applying, and poor semantic search results.
type: troubleshooting
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Troubleshoot search relevance [troubleshooting-search-relevance]

Use this page when your search returns results but they're in the wrong order, irrelevant, or missing expected matches. These symptoms point to a relevance problem rather than a technical error.

## Diagnose scoring with the explain API [troubleshooting-relevance-explain]

Use the [explain API]({{es-apis}}operation/operation-explain) to see exactly how {{es}} calculated a document's score, or to find out why a document didn't match. For a visual representation, use the [Search Profiler](../../explore-analyze/query-filter/tools/search-profiler.md) in {{kib}}.

### Find out why a document ranks unexpectedly high or low [troubleshooting-relevance-explain-ranking]

When a document ranks higher or lower than you expect, run the explain API against it. Replace `2` with the `_id` of the document you want to inspect:

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
2. The `boost` value (here `2.2`) is the effective boost passed to the BM25 scorer. For an unmodified field, this equals `1.0 × (1 + k1) = 2.2` by default. A higher value, for example `6.6` for a `^3` field boost, indicates a user-specified boost was applied.
3. Each entry in `details` shows one term's contribution. `boost`, `idf` (how rare the term is), and `tf` (how often it appears) multiply together to produce the term score.

### Find out why a document doesn't match [troubleshooting-relevance-explain-no-match]

When a document you expect in the results is missing, run the explain API against it. Replace `4` with the `_id` of the document you want to inspect:

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

`"matched": false` with `"No matching clauses"` means the tokens in the query did not appear in the indexed field. This is usually a token mismatch. Refer to [Fix token mismatches between index and query](#troubleshooting-relevance-tokens).

## Fix token mismatches between index and query [troubleshooting-relevance-tokens]

When a query fails to match an expected document, the index and query might be tokenizing text differently. Use the [analyze API]({{es-apis}}operation/operation-indices-analyze) to inspect what tokens {{es}} produces for a given field and text.

In the following examples, the `title` field uses the `english` analyzer. First, check how the indexed field tokenizes the text:

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
    { "token": "get",           "position": 0 },
    { "token": "start",         "position": 1 },
    { "token": "elasticsearch", "position": 3 }
  ]
}
```

The `english` analyzer removes the stop word `with` and stems `getting` to `get` and `started` to `start`. Removing `with` leaves a gap, so `elasticsearch` keeps position `3`.

Then run the same text through the analyzer your query uses. By default, a `match` query uses the analyzer defined on the field, so the tokens only differ if the field has a different `search_analyzer` or the query overrides the analyzer. For example, if your `title` field uses the `english` analyzer but the query sets `"analyzer": "standard"`, the tokens differ:

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

The index contains the stemmed tokens `get` and `start`, but the query produces `getting` and `started`. These tokens don't match, so the document won't appear in results.

To reproduce this with a search, run a `match` query that overrides the field's analyzer. The query term `started` is analyzed as `started`, which doesn't match the indexed token `start`:

```console
GET /my-index-000001/_search
{
  "query": {
    "match": {
      "title": {
        "query": "started",
        "analyzer": "standard"
      }
    }
  }
}
```

```console-result
{
  "hits": {
    "total": {
      "value": 0,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  }
}
```

Without the `analyzer` override, the same query uses the field's `english` analyzer, analyzes `started` as `start`, and matches the document.

To fix this, remove the `analyzer` override from the query so it uses the field's analyzer, or change the field's `search_analyzer` to match its index analyzer.

Refer to [Test an analyzer](../../manage-data/data-store/text-analysis/test-an-analyzer.md) for a detailed walkthrough.

## Fix synonyms not applying [troubleshooting-relevance-synonyms]

Synonyms are usually applied at search time, which is the recommended approach because you can update synonym sets without reindexing. Synonym sets managed through the synonyms API or {{kib}} work only in search analyzers. Index-time synonyms are also supported with the `synonym` filter (not `synonym_graph`), but changing them requires a reindex. {{serverless-short}} supports only synonym sets managed through the synonyms API or {{kib}}, not index-time or file-based synonyms. If synonyms aren't matching, check:

1. Use the analyze API with the analyzer that applies your synonyms, usually your index's search analyzer, to confirm the synonym expansion is happening:

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

   If you only see the original token and no `SYNONYM` entries, the synonym filter is not part of that analyzer's chain.

2. If you updated the synonym set, confirm whether you need to reload or reindex:
   - Synonym sets managed through the [synonyms API]({{es-apis}}group/endpoint-synonyms) reload automatically when you update the set. You don't need to reload manually or reindex, as long as the synonym filter sets `"updateable": true`.
   - {applies_to}`serverless: unavailable` Custom synonym files configured as index-time analyzers require a full reindex to take effect on already-indexed documents. If the file is configured as a search-time analyzer with `"updateable": true`, you can reload it without reindexing by calling the [reload search analyzers API]({{es-apis}}operation/operation-indices-reload-search-analyzers) after you update the file on every node.

Refer to [Search with synonyms](../../solutions/search/full-text/search-with-synonyms.md) for setup and reload guidance.

## Fix boosting not working as expected [troubleshooting-relevance-boosting]

If boosted fields or documents aren't ranking as expected, use the explain API to confirm the boost applies. Common causes:

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

## Fix the wrong fields being searched [troubleshooting-relevance-fields]

When a `multi_match` query returns irrelevant results, the field list might be too broad or misconfigured. Check:

- The `fields` array in your `multi_match`: remove low-signal fields or add explicit boosts to prioritize the right ones.
- Whether `copy_to` is pulling unrelated content into a combined field. Use the [get mapping API]({{es-apis}}operation/operation-indices-get-mapping) to inspect which fields copy into your target field.
- The `type` parameter: `best_fields` ranks by the single best matching field, while `most_fields` sums scores across fields. Switch between them to see which fits your use case.

## Fix poor semantic search results [troubleshooting-relevance-semantic]

If semantic search returns results that are off-topic or miss obvious matches, the most common cause is an embedding model mismatch: documents and queries were embedded by incompatible models or at different times.

Check the following:

- Verify that the indexing and query-time embeddings come from compatible models. The `inference_id` parameter sets the endpoint used at index time, and `search_inference_id`, if set, sets the endpoint used at query time. The two endpoints can differ, but they must produce compatible embeddings. Refer to the [`semantic_text` field type reference](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-reference.md) for details.
- If you changed the model or endpoint, reindex the affected documents so their embeddings match the current model.
- Use the `_explain` API to verify that the vector similarity scores are non-zero for documents you expect to match.
- If embeddings are missing or zero-length, the inference pipeline might have failed silently during indexing.
