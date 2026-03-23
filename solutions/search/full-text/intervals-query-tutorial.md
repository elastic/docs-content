---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Use the intervals query [intervals-query-tutorial]

The [intervals query](elasticsearch://reference/query-languages/query-dsl/query-dsl-intervals-query.md) returns documents based on the **order and proximity** of matching terms. Unlike the [`match_phrase` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query-phrase.md), it lets you define flexible rules about how terms appear relative to each other — allowing gaps, enforcing ordering, and combining multiple term sequences.

Use this tutorial to learn how to:

* Index sample data and run a basic intervals query
* Perform ordered proximity searches using `all_of` with `any_of`
* Narrow results further using the `prefix` rule

::::{tip}
The code examples use [Console](../../../explore-analyze/query-filter/tools/console.md) syntax.
You can [convert examples into other programming languages](../../../explore-analyze/query-filter/tools/console.md#import-export-console-requests) in the Console UI.
::::

## Requirements [intervals-query-tutorial-requirements]

You can follow these steps with any {{es}} deployment.
Refer to [Choosing your deployment type](../../../deploy-manage/deploy.md) for deployment options.

## Create an index [intervals-query-tutorial-create-index]

Create a `products` index:

```console
PUT /products
```

## Add sample documents [intervals-query-tutorial-index-data]

Index several product descriptions to use as sample data:

```console
POST /products/_bulk?refresh=wait_for
{"index":{"_id":"1"}}
{"description":"fast full text search for developers"}
{"index":{"_id":"2"}}
{"description":"full text search with machine learning"}
{"index":{"_id":"3"}}
{"description":"machine learning performance optimization"}
{"index":{"_id":"4"}}
{"description":"developer tools for fast search"}
{"index":{"_id":"5"}}
{"description":"high performance machine learning platform"}
```

The [`standard` analyzer](elasticsearch://reference/text-analysis/analyzer-reference/standard-analyzer.md) is used by default for `text` fields.
It lowercases and tokenizes the text, so each word becomes a searchable term at a specific position.
For example, document 1 produces the tokens `fast`(0), `full`(1), `text`(2), `search`(3), `for`(4), `developers`(5).

To learn more about how text is analyzed and indexed, refer to [Text analysis during search](text-analysis-during-search.md).

## Basic ordered proximity search [intervals-query-tutorial-basic-example]

Find products where `full text` appears immediately before `search`:

```console
GET /products/_search
{
  "query": {
    "intervals": {
      "description": {
        "all_of": {
          "ordered": true, <1>
          "intervals": [
            {
              "match": {
                "query": "full text",
                "max_gaps": 0, <2>
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

1. `ordered: true` on `all_of` enforces that `full text` must appear before `search`.
2. `max_gaps: 0` on the inner `match` requires `full` and `text` to be adjacent with no words in between.

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
          "description": "fast full text search for developers"
        }
      },
      {
        "_id": "2",
        "_score": 0.5,
        "_source": {
          "description": "full text search with machine learning"
        }
      }
    ]
  }
}
```
::::

Documents 1 and 2 match because both contain `full text search` in that exact order with no gaps.
Documents 3, 4, and 5 don't contain `full text` followed immediately by `search`.

## Combining multiple intervals rules [intervals-query-tutorial-any-of-example]

Find products that describe `machine learning` near either `search` or `performance`, in any order and within two positions:

```console
GET /products/_search
{
  "query": {
    "intervals": {
      "description": {
        "all_of": {
          "ordered": false, <1>
          "max_gaps": 2, <2>
          "intervals": [
            {
              "match": {
                "query": "machine learning"
              }
            },
            {
              "any_of": { <3>
                "intervals": [
                  { "match": { "query": "search" } },
                  { "match": { "query": "performance" } }
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

1. `ordered: false` allows `machine learning` and the other term to appear in either order.
2. `max_gaps: 2` limits the number of unmatched positions between the two intervals to two.
3. `any_of` matches whichever alternative appears in the text.

::::{dropdown} Example response
```console-result
{
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "hits": [
      {
        "_id": "2",
        "_score": 0.5,
        "_source": {
          "description": "full text search with machine learning"
        }
      },
      {
        "_id": "3",
        "_score": 0.5,
        "_source": {
          "description": "machine learning performance optimization"
        }
      },
      {
        "_id": "5",
        "_score": 0.5,
        "_source": {
          "description": "high performance machine learning platform"
        }
      }
    ]
  }
}
```
::::

Document 2 matches because `search` and `machine learning` are within two positions of each other (`with` is the only word between them).
Documents 3 and 5 match because `performance` immediately precedes `machine learning` in both.
Documents 1 and 4 don't contain `machine learning`.

## Advanced use case: Searching for terms by prefix [intervals-query-tutorial-prefix-example]

The `prefix` rule matches any term that starts with a given set of characters, letting you broaden an interval without enumerating every possible form.
Use it when the exact term varies but the leading characters are consistent.

Find products that mention something starting with `fast` near `search`:

```console
GET /products/_search
{
  "query": {
    "intervals": {
      "description": {
        "all_of": {
          "ordered": false,
          "max_gaps": 2,
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

1. The `prefix` rule expands to match any term beginning with `fast`, such as `fast`, `faster`, or `fastest`.

::::{warning}
The `prefix` rule can expand to match many terms depending on your data. To avoid errors caused by exceeding the `indices.query.bool.max_clause_count` [search setting](/reference/elasticsearch/configuration-reference/search-settings.md), use the [`index-prefixes`](/reference/elasticsearch/mapping-reference/index-prefixes.md) option in your field mapping, or keep prefix patterns specific enough to limit expansion.
::::

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
          "description": "fast full text search for developers"
        }
      },
      {
        "_id": "4",
        "_score": 0.5,
        "_source": {
          "description": "developer tools for fast search"
        }
      }
    ]
  }
}
```
::::

Documents 1 and 4 match because both contain a term starting with `fast` within two positions of `search`.

## Clean up [intervals-query-tutorial-cleanup]

Delete the `products` index when you're done:

```console
DELETE /products
```

## Next steps [intervals-query-tutorial-next-steps]

* Refer to the full [intervals query reference](elasticsearch://reference/query-languages/query-dsl/query-dsl-intervals-query.md) for all available rules and parameters, including `filter`, `fuzzy`, `wildcard`, and `regexp` rules.
* Learn how [text analysis](../../../manage-data/data-store/text-analysis.md) affects how terms are stored and matched.
* Explore [full-text queries](elasticsearch://reference/query-languages/query-dsl/full-text-queries.md) for other proximity and matching options.
* Use the [`match_phrase` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query-phrase.md) for strict phrase matching without gaps.
