---
navigation_title: "Search using LTR"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/learning-to-rank-search-usage.html
applies_to:
  stack:
  serverless:
---



# Search using LTR [learning-to-rank-search-usage]


::::{note}
This feature was introduced in version 8.12.0 and is only available to certain subscription levels. For more information, see {{subscriptions}}.
::::



## Learning To Rank as a rescorer [learning-to-rank-rescorer]

Once your LTR model is trained and deployed in {{es}}, it can be used as a [rescorer](elasticsearch://reference/elasticsearch/rest-apis/filter-search-results.md#rescore) in the [search API](../querying-for-search.md):

```console
GET my-index/_search
{
  "query": { <1>
    "multi_match": {
      "fields": ["title", "content"],
      "query": "the quick brown fox"
    }
  },
  "rescore": {
    "learning_to_rank": {
      "model_id": "ltr-model", <2>
      "params": { <3>
        "query_text": "the quick brown fox"
      }
    },
    "window_size": 100 <4>
  }
}
```

1. First pass query providing documents to be rescored.
2. The unique identifier of the trained model uploaded to {{es}}.
3. Named parameters to be passed to the query templates used for feature.
4. The number of documents that should be examined by the rescorer on each shard.
%  TEST[skip:TBD]


### Known limitations [learning-to-rank-rescorer-limitations]


#### Rescore window size [learning-to-rank-rescorer-limitations-window-size]

Scores returned by LTR models are usually not comparable with the scores issued by the first pass query and can be lower than the non-rescored score. This can cause the non-rescored result document to be ranked higher than the rescored document. To prevent this, the `window_size` parameter is mandatory for LTR rescorers and should be greater than or equal to `from + size`.


#### Pagination [learning-to-rank-rescorer-limitations-pagination]

When exposing pagination to users, `window_size` should remain constant as each page is progressed by passing different `from` values. Changing the `window_size` can alter the top hits causing results to confusingly shift as the user steps through pages.


#### Negative scores [learning-to-rank-rescorer-limitations-negative-scores]

Depending on how your model is trained, it’s possible that the model will return negative scores for documents. While negative scores are not allowed from first-stage retrieval and ranking, it is possible to use them in the LTR rescorer.

