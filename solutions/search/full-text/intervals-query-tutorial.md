---
navigation_title: "Intervals query"
description: "Learn how to use the Elasticsearch intervals query for proximity and order-sensitive full-text searches."
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Search by term proximity and order with the intervals query [intervals-query-tutorial]

The [intervals query](elasticsearch://reference/query-languages/query-dsl/query-dsl-intervals-query.md) finds documents based on the **order and proximity** of matching terms.
Unlike the [`match_phrase` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query-phrase.md), it lets you define flexible rules about how terms relate to each other — allowing gaps between terms, enforcing ordering, and combining multiple term patterns.

By the end of this tutorial, you can:

* Run a basic ordered proximity search using `all_of` with `match`
* Combine `all_of` and `any_of` rules for flexible matching
* Use the `prefix` rule to match term variants by their leading characters
* Apply a `filter` rule to exclude unwanted terms from proximity matches

::::{tip}
The code examples use [Console](../../../explore-analyze/query-filter/tools/console.md) syntax.
You can [convert examples into other programming languages](../../../explore-analyze/query-filter/tools/console.md#import-export-console-requests) in the Console UI.
::::

## Before you begin [intervals-query-tutorial-prereqs]

You can follow these steps with any {{es}} deployment.
Refer to [Choosing your deployment type](../../../deploy-manage/deploy.md) for deployment options.

## Step 1: Create an index and add sample data [intervals-query-tutorial-setup]

Create a `books` index and add several sample documents:

```console
PUT /books
```

```console
POST /books/_bulk?refresh=wait_for
{"index":{"_id":"1"}}
{"title":"Elasticsearch in Action","synopsis":"A practical guide to full text search with Elasticsearch. Covers queries, filters, and performance tuning."}
{"index":{"_id":"2"}}
{"title":"Search Fundamentals","synopsis":"Learn the basics of full text search including tokenization, analyzers, and relevance scoring."}
{"index":{"_id":"3"}}
{"title":"Faster Elasticsearch","synopsis":"Tips for fast and efficient search at scale. Covers caching, faster queries, and cluster optimization."}
{"index":{"_id":"4"}}
{"title":"Machine Learning for Search","synopsis":"Apply machine learning to improve search relevance. Covers learning to rank and query classification."}
{"index":{"_id":"5"}}
{"title":"Advanced Text Processing","synopsis":"Deep dive into text analysis and search pipelines. Full coverage of custom analyzers and token filters."}
```

The [`standard` analyzer](elasticsearch://reference/text-analysis/analyzer-reference/standard-analyzer.md) is used by default for `text` fields.
It lowercases and tokenizes the text, so each word becomes a searchable term at a specific position.

To learn more, refer to [Text analysis](../../../manage-data/data-store/text-analysis.md).

## Step 2: Run a basic ordered proximity search [intervals-query-tutorial-basic-example]

Use `all_of` with `ordered: true` to find books where `full text` appears immediately before `search`, with no gaps allowed:

```console
GET /books/_search
{
  "query": {
    "intervals": {
      "synopsis": {
        "all_of": {
          "ordered": true, <1>
          "max_gaps": 0, <2>
          "intervals": [
            {
              "match": {
                "query": "full text",
                "max_gaps": 0,
                "ordered": true
              }
            },
            {
              "match": {
                "query": "search"
              }
            }
          ]
        }
      }
    }
  }
}
```

1. `ordered: true` requires the first interval (`full text`) to appear before the second (`search`).
2. `max_gaps: 0` on `all_of` requires both intervals to be adjacent — no words between `text` and `search`.

::::{dropdown} Example response
```console-result
{
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "hits": [
      {
        "_id": "1",
        "_score": 0.5,
        "_source": {
          "title": "Elasticsearch in Action",
          "synopsis": "A practical guide to full text search with Elasticsearch. Covers queries, filters, and performance tuning."
        }
      },
      {
        "_id": "2",
        "_score": 0.5,
        "_source": {
          "title": "Search Fundamentals",
          "synopsis": "Learn the basics of full text search including tokenization, analyzers, and relevance scoring."
        }
      }
    ]
  }
}
```
::::

Documents 1 and 2 match because both contain `full text search` as three contiguous, ordered terms.
The other documents don't contain the phrase `full text search`.

## Step 3: Combine rules with `any_of` [intervals-query-tutorial-any-of-example]

Use `any_of` inside `all_of` to match alternative terms.
This query finds books where `search` appears within two positions of either `machine learning` or `text`, in any order:

```console
GET /books/_search
{
  "query": {
    "intervals": {
      "synopsis": {
        "all_of": {
          "ordered": false, <1>
          "max_gaps": 2, <2>
          "intervals": [
            {
              "match": {
                "query": "search"
              }
            },
            {
              "any_of": { <3>
                "intervals": [
                  { "match": { "query": "machine learning" } },
                  { "match": { "query": "text" } }
                ]
              }
            }
          ]
        }
      }
    }
  }
}
```

1. `ordered: false` allows the intervals to appear in any order.
2. `max_gaps: 2` allows up to two unmatched positions between the intervals.
3. `any_of` matches either `machine learning` or `text`.

::::{dropdown} Example response
```console-result
{
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "hits": [
      {
        "_id": "1",
        "_score": 0.5,
        "_source": {
          "title": "Elasticsearch in Action",
          "synopsis": "A practical guide to full text search with Elasticsearch. Covers queries, filters, and performance tuning."
        }
      },
      {
        "_id": "2",
        "_score": 0.5,
        "_source": {
          "title": "Search Fundamentals",
          "synopsis": "Learn the basics of full text search including tokenization, analyzers, and relevance scoring."
        }
      },
      {
        "_id": "4",
        "_score": 0.5,
        "_source": {
          "title": "Machine Learning for Search",
          "synopsis": "Apply machine learning to improve search relevance. Covers learning to rank and query classification."
        }
      },
      {
        "_id": "5",
        "_score": 0.5,
        "_source": {
          "title": "Advanced Text Processing",
          "synopsis": "Deep dive into text analysis and search pipelines. Full coverage of custom analyzers and token filters."
        }
      }
    ]
  }
}
```
::::

Documents 1 and 2 match because `text` appears immediately before `search` (zero gaps).
Document 4 matches because `search` appears two positions after `machine learning` (`to` and `improve` are the intervening tokens).
Document 5 matches because `text` and `search` are two positions apart (`analysis` and `and` are between them).
Document 3 doesn't match because its synopsis contains neither `text` nor `machine learning` near `search`.

## Step 4: Match term variants with `prefix` [intervals-query-tutorial-prefix-example]

The `prefix` rule matches any term that starts with a given set of characters, so you can match term variants without listing every form.

Find books where any term starting with `fast` appears within three positions of `search`:

```console
GET /books/_search
{
  "query": {
    "intervals": {
      "synopsis": {
        "all_of": {
          "ordered": false,
          "max_gaps": 3,
          "intervals": [
            {
              "prefix": { <1>
                "prefix": "fast"
              }
            },
            {
              "match": {
                "query": "search"
              }
            }
          ]
        }
      }
    }
  }
}
```

1. The `prefix` rule matches any indexed term beginning with `fast`, including `fast`, `faster`, and `fastest`.

::::{warning}
The `prefix` rule can expand to match many terms depending on your data.
To avoid errors from exceeding the `indices.query.bool.max_clause_count` [search setting](/reference/elasticsearch/configuration-reference/search-settings.md), use the [`index-prefixes`](/reference/elasticsearch/mapping-reference/index-prefixes.md) mapping option or keep prefix patterns specific enough to limit expansion.
::::

::::{dropdown} Example response
```console-result
{
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "hits": [
      {
        "_id": "3",
        "_score": 0.5,
        "_source": {
          "title": "Faster Elasticsearch",
          "synopsis": "Tips for fast and efficient search at scale. Covers caching, faster queries, and cluster optimization."
        }
      }
    ]
  }
}
```
::::

Document 3 matches because `fast` appears two positions before `search` (`and efficient` are the intervening tokens).
A regular `match` for `fast` would also find this document, but the `prefix` rule additionally catches variants like `faster` in the same document — ensuring the query works even if the data uses different word forms.

## Step 5: Exclude terms with a filter [intervals-query-tutorial-filter-example]

Use the `filter` rule to exclude unwanted terms from a proximity match.
This query finds books where `search` appears near `text`, but only when `analysis` does not appear between them:

```console
GET /books/_search
{
  "query": {
    "intervals": {
      "synopsis": {
        "match": {
          "query": "text search",
          "max_gaps": 5,
          "ordered": false,
          "filter": { <1>
            "not_containing": {
              "match": {
                "query": "analysis"
              }
            }
          }
        }
      }
    }
  }
}
```

1. The `not_containing` filter excludes intervals where `analysis` appears between `text` and `search`.

::::{dropdown} Example response
```console-result
{
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "hits": [
      {
        "_id": "1",
        "_score": 0.5,
        "_source": {
          "title": "Elasticsearch in Action",
          "synopsis": "A practical guide to full text search with Elasticsearch. Covers queries, filters, and performance tuning."
        }
      },
      {
        "_id": "2",
        "_score": 0.5,
        "_source": {
          "title": "Search Fundamentals",
          "synopsis": "Learn the basics of full text search including tokenization, analyzers, and relevance scoring."
        }
      }
    ]
  }
}
```
::::

Documents 1 and 2 match because both contain `text` near `search` without `analysis` between them.
Document 5 also contains `text` near `search` (and matched in [Step 3](#intervals-query-tutorial-any-of-example)), but `analysis` appears between them (the tokens `text`, `analysis`, `and`, `search` are contiguous), so the filter excludes it.

## Clean up [intervals-query-tutorial-cleanup]

Delete the `books` index:

```console
DELETE /books
```

## Summary [intervals-query-tutorial-summary]

In this tutorial, you learned how to:

* Search for ordered, contiguous phrases with `all_of` and `max_gaps`
* Match alternative terms using `any_of`
* Broaden interval matching to term variants using the `prefix` rule
* Exclude unwanted terms from proximity matches using a `filter` rule

## Next steps [intervals-query-tutorial-next-steps]

* Refer to the full [intervals query reference](elasticsearch://reference/query-languages/query-dsl/query-dsl-intervals-query.md) for all available rules and parameters, including `fuzzy`, `wildcard`, `regexp`, and `range` rules.
* Learn how [text analysis](../../../manage-data/data-store/text-analysis.md) affects how terms are stored and matched.
* Explore [full-text queries](elasticsearch://reference/query-languages/query-dsl/full-text-queries.md) for other matching options.
* Use the [`match_phrase` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query-phrase.md) for strict phrase matching without gaps.
