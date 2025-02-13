---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/static-scoring-signals.html
applies:
  stack:
  serverless:
---

# Incorporating static relevance signals into the score [static-scoring-signals]

Many domains have static signals that are known to be correlated with relevance. For instance [PageRank](https://en.wikipedia.org/wiki/PageRank) and url length are two commonly used features for web search in order to tune the score of web pages independently of the query.

There are two main queries that allow combining static score contributions with textual relevance, eg. as computed with BM25:

* [`script_score` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-script-score-query.html)
* [`rank_feature` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-rank-feature-query.html)

For instance imagine that you have a `pagerank` field that you wish to combine with the BM25 score so that the final score is equal to `score = bm25_score + pagerank / (10 + pagerank)`.

With the [`script_score` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-script-score-query.html) the query would look like this:

```console
GET index/_search
{
  "query": {
    "script_score": {
      "query": {
        "match": { "body": "elasticsearch" }
      },
      "script": {
        "source": "_score * saturation(doc['pagerank'].value, 10)" <1>
      }
    }
  }
}
```

1. `pagerank` must be mapped as a [Numeric](https://www.elastic.co/guide/en/elasticsearch/reference/current/number.html)


while with the [`rank_feature` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-rank-feature-query.html) it would look like below:

```console
GET _search
{
  "query": {
    "bool": {
      "must": {
        "match": { "body": "elasticsearch" }
      },
      "should": {
        "rank_feature": {
          "field": "pagerank", <1>
          "saturation": {
            "pivot": 10
          }
        }
      }
    }
  }
}
```

1. `pagerank` must be mapped as a [`rank_feature`](https://www.elastic.co/guide/en/elasticsearch/reference/current/rank-feature.html) field


While both options would return similar scores, there are trade-offs: [script_score](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-script-score-query.html) provides a lot of flexibility, enabling you to combine the text relevance score with static signals as you prefer. On the other hand, the [`rank_feature` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/rank-feature.html) only exposes a couple ways to incorporate static signals into the score. However, it relies on the [`rank_feature`](https://www.elastic.co/guide/en/elasticsearch/reference/current/rank-feature.html) and [`rank_features`](https://www.elastic.co/guide/en/elasticsearch/reference/current/rank-features.html) fields, which index values in a special way that allows the [`rank_feature` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-rank-feature-query.html) to skip over non-competitive documents and get the top matches of a query faster.

