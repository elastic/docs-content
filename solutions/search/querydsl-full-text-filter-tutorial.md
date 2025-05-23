---
navigation_title: Search and filter with Query DSL
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-filter-tutorial.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
---

# Tutorial: Full-text search and filtering with Query DSL [full-text-filter-tutorial]

:::{tip}
This tutorial presents examples in Query DSL syntax. Refer to [the {{esql}} version](esql-search-tutorial.md) for the equivalent examples in {{esql}} syntax.
:::

This is a hands-on introduction to the basics of [full-text search](full-text.md) with {{es}}, also known as *lexical search*, using the [`_search` API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) and [Query DSL](../../explore-analyze/query-filter/languages/querydsl.md). You’ll also learn how to filter data, to narrow down search results based on exact criteria.

In this scenario, we’re implementing a search function for a cooking blog. The blog contains recipes with various attributes including textual content, categorical data, and numerical ratings.

The goal is to create search queries that enable users to:

* Find recipes based on ingredients they want to use or avoid
* Discover dishes suitable for their dietary needs
* Find highly-rated recipes in specific categories
* Find recent recipes from their favorite authors

To achieve these goals we’ll use different Elasticsearch queries to perform full-text search, apply filters, and combine multiple search criteria.


## Requirements [full-text-filter-tutorial-requirements]

You’ll need a running {{es}} cluster, together with {{kib}} to use the Dev Tools API Console. Refer to [choose your deployment type](/deploy-manage/deploy.md#choosing-your-deployment-type) for deployment options.

Want to get started quickly? Run the following command in your terminal to set up a [single-node local cluster in Docker](get-started.md):

```sh
curl -fsSL https://elastic.co/start-local | sh
```


## Step 1: Create an index [full-text-filter-tutorial-create-index]

Create the `cooking_blog` index to get started:

```console
PUT /cooking_blog
```

Now define the mappings for the index:

```console
PUT /cooking_blog/_mapping
{
  "properties": {
    "title": {
      "type": "text",
      "analyzer": "standard", <1>
      "fields": { <2>
        "keyword": {
          "type": "keyword",
          "ignore_above": 256 <3>
        }
      }
    },
    "description": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword"
        }
      }
    },
    "author": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword"
        }
      }
    },
    "date": {
      "type": "date",
      "format": "yyyy-MM-dd"
    },
    "category": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword"
        }
      }
    },
    "tags": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword"
        }
      }
    },
    "rating": {
      "type": "float"
    }
  }
}
```

1. The `standard` analyzer is used by default for `text` fields if an `analyzer` isn’t specified. It’s included here for demonstration purposes.
2. [Multi-fields](elasticsearch://reference/elasticsearch/mapping-reference/multi-fields.md) are used here to index `text` fields as both `text` and `keyword` [data types](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md). This enables both full-text search and exact matching/filtering on the same field. Note that if you used [dynamic mapping](../../manage-data/data-store/mapping/dynamic-field-mapping.md), these multi-fields would be created automatically.
3. The [`ignore_above` parameter](elasticsearch://reference/elasticsearch/mapping-reference/ignore-above.md) prevents indexing values longer than 256 characters in the `keyword` field. Again this is the default value, but it’s included here for demonstration purposes. It helps to save disk space and avoid potential issues with Lucene’s term byte-length limit.


::::{tip}
Full-text search is powered by [text analysis](full-text/text-analysis-during-search.md). Text analysis normalizes and standardizes text data so it can be efficiently stored in an inverted index and searched in near real-time. Analysis happens at both [index and search time](../../manage-data/data-store/text-analysis/index-search-analysis.md). This tutorial won’t cover analysis in detail, but it’s important to understand how text is processed to create effective search queries.

::::



## Step 2: Add sample blog posts to your index [full-text-filter-tutorial-index-data]

Now you’ll need to index some example blog posts using the [Bulk API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings). Note that `text` fields are analyzed and multi-fields are generated at index time.

```console
POST /cooking_blog/_bulk?refresh=wait_for
{"index":{"_id":"1"}}
{"title":"Perfect Pancakes: A Fluffy Breakfast Delight","description":"Learn the secrets to making the fluffiest pancakes, so amazing you won't believe your tastebuds. This recipe uses buttermilk and a special folding technique to create light, airy pancakes that are perfect for lazy Sunday mornings.","author":"Maria Rodriguez","date":"2023-05-01","category":"Breakfast","tags":["pancakes","breakfast","easy recipes"],"rating":4.8}
{"index":{"_id":"2"}}
{"title":"Spicy Thai Green Curry: A Vegetarian Adventure","description":"Dive into the flavors of Thailand with this vibrant green curry. Packed with vegetables and aromatic herbs, this dish is both healthy and satisfying. Don't worry about the heat - you can easily adjust the spice level to your liking.","author":"Liam Chen","date":"2023-05-05","category":"Main Course","tags":["thai","vegetarian","curry","spicy"],"rating":4.6}
{"index":{"_id":"3"}}
{"title":"Classic Beef Stroganoff: A Creamy Comfort Food","description":"Indulge in this rich and creamy beef stroganoff. Tender strips of beef in a savory mushroom sauce, served over a bed of egg noodles. It's the ultimate comfort food for chilly evenings.","author":"Emma Watson","date":"2023-05-10","category":"Main Course","tags":["beef","pasta","comfort food"],"rating":4.7}
{"index":{"_id":"4"}}
{"title":"Vegan Chocolate Avocado Mousse","description":"Discover the magic of avocado in this rich, vegan chocolate mousse. Creamy, indulgent, and secretly healthy, it's the perfect guilt-free dessert for chocolate lovers.","author":"Alex Green","date":"2023-05-15","category":"Dessert","tags":["vegan","chocolate","avocado","healthy dessert"],"rating":4.5}
{"index":{"_id":"5"}}
{"title":"Crispy Oven-Fried Chicken","description":"Get that perfect crunch without the deep fryer! This oven-fried chicken recipe delivers crispy, juicy results every time. A healthier take on the classic comfort food.","author":"Maria Rodriguez","date":"2023-05-20","category":"Main Course","tags":["chicken","oven-fried","healthy"],"rating":4.9}
```


## Step 3: Perform basic full-text searches [full-text-filter-tutorial-match-query]

Full-text search involves executing text-based queries across one or more document fields. These queries calculate a relevance score for each matching document, based on how closely the document’s content aligns with the search terms. {{es}} offers various query types, each with its own method for matching text and [relevance scoring](../../explore-analyze/query-filter/languages/querydsl.md#relevance-scores).


### `match` query [_match_query]

The [`match`](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md) query is the standard query for full-text, or "lexical", search. The query text will be analyzed according to the analyzer configuration specified on each field (or at query time).

First, search the `description` field for "fluffy pancakes":

```console
GET /cooking_blog/_search
{
  "query": {
    "match": {
      "description": {
        "query": "fluffy pancakes" <1>
      }
    }
  }
}
```

1. By default, the `match` query uses `OR` logic between the resulting tokens. This means it will match documents that contain either "fluffy" or "pancakes", or both, in the description field.


At search time, {{es}} defaults to the analyzer defined in the field mapping. In this example, we’re using the `standard` analyzer. Using a different analyzer at search time is an [advanced use case](../../manage-data/data-store/text-analysis/index-search-analysis.md#different-analyzers).

::::{dropdown} Example response
```console-result
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": { <1>
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.8378843, <2>
    "hits": [
      {
        "_index": "cooking_blog",
        "_id": "1",
        "_score": 1.8378843, <3>
        "_source": {
          "title": "Perfect Pancakes: A Fluffy Breakfast Delight", <4>
          "description": "Learn the secrets to making the fluffiest pancakes, so amazing you won't believe your tastebuds. This recipe uses buttermilk and a special folding technique to create light, airy pancakes that are perfect for lazy Sunday mornings.", <5>
          "author": "Maria Rodriguez",
          "date": "2023-05-01",
          "category": "Breakfast",
          "tags": [
            "pancakes",
            "breakfast",
            "easy recipes"
          ],
          "rating": 4.8
        }
      }
    ]
  }
}
```

1. The `hits` object contains the total number of matching documents and their relation to the total.
2. `max_score` is the highest relevance score among all matching documents. In this example, we only have one matching document.
3. `_score` is the relevance score for a specific document, indicating how well it matches the query. Higher scores indicate better matches. In this example the `max_score` is the same as the `_score`, as there is only one matching document.
4. The title contains both "Fluffy" and "Pancakes", matching our search terms exactly.
5. The description includes "fluffiest" and "pancakes", further contributing to the document’s relevance due to the analysis process.


::::



### Require all terms in a match query [_require_all_terms_in_a_match_query]

Specify the `and` operator to require both terms in the `description` field. This stricter search returns *zero hits* on our sample data, as no document contains both "fluffy" and "pancakes" in the description.

```console
GET /cooking_blog/_search
{
  "query": {
    "match": {
      "description": {
        "query": "fluffy pancakes",
        "operator": "and"
      }
    }
  }
}
```

::::{dropdown} Example response
```console-result
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
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

::::



### Specify a minimum number of terms to match [_specify_a_minimum_number_of_terms_to_match]

Use the [`minimum_should_match`](elasticsearch://reference/query-languages/query-dsl/query-dsl-minimum-should-match.md) parameter to specify the minimum number of terms a document should have to be included in the search results.

Search the title field to match at least 2 of the 3 terms: "fluffy", "pancakes", or "breakfast". This is useful for improving relevance while allowing some flexibility.

```console
GET /cooking_blog/_search
{
  "query": {
    "match": {
      "title": {
        "query": "fluffy pancakes breakfast",
        "minimum_should_match": 2
      }
    }
  }
}
```


## Step 4: Search across multiple fields at once [full-text-filter-tutorial-multi-match]

When users enter a search query, they often don’t know (or care) whether their search terms appear in a specific field. A [`multi_match`](elasticsearch://reference/query-languages/query-dsl/query-dsl-multi-match-query.md) query allows searching across multiple fields simultaneously.

Let’s start with a basic `multi_match` query:

```console
GET /cooking_blog/_search
{
  "query": {
    "multi_match": {
      "query": "vegetarian curry",
      "fields": ["title", "description", "tags"]
    }
  }
}
```

This query searches for "vegetarian curry" across the title, description, and tags fields. Each field is treated with equal importance.

However, in many cases, matches in certain fields (like the title) might be more relevant than others. We can adjust the importance of each field using field boosting:

```console
GET /cooking_blog/_search
{
  "query": {
    "multi_match": {
      "query": "vegetarian curry",
      "fields": ["title^3", "description^2", "tags"] <1>
    }
  }
}
```

1. The `^` syntax applies a boost to specific fields:* `title^3`: The title field is 3 times more important than an unboosted field
* `description^2`: The description is 2 times more important
* `tags`: No boost applied (equivalent to `^1`)

    These boosts help tune relevance, prioritizing matches in the title over the description, and matches in the description over tags.




Learn more about fields and per-field boosting in the [`multi_match` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-multi-match-query.md) reference.

::::{dropdown} Example response
```console-result
{
  "took": 0,
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
    "max_score": 7.546015,
    "hits": [
      {
        "_index": "cooking_blog",
        "_id": "2",
        "_score": 7.546015,
        "_source": {
          "title": "Spicy Thai Green Curry: A Vegetarian Adventure", <1>
          "description": "Dive into the flavors of Thailand with this vibrant green curry. Packed with vegetables and aromatic herbs, this dish is both healthy and satisfying. Don't worry about the heat - you can easily adjust the spice level to your liking.", <2>
          "author": "Liam Chen",
          "date": "2023-05-05",
          "category": "Main Course",
          "tags": [
            "thai",
            "vegetarian",
            "curry",
            "spicy"
          ], <3>
          "rating": 4.6
        }
      }
    ]
  }
}
```

1. The title contains "Vegetarian" and "Curry", which matches our search terms. The title field has the highest boost (^3), contributing significantly to this document’s relevance score.
2. The description contains "curry" and related terms like "vegetables", further increasing the document’s relevance.
3. The tags include both "vegetarian" and "curry", providing an exact match for our search terms, albeit with no boost.


This result demonstrates how the `multi_match` query with field boosts helps users find relevant recipes across multiple fields. Even though the exact phrase "vegetarian curry" doesn’t appear in any single field, the combination of matches across fields produces a highly relevant result.

::::


::::{tip}
The `multi_match` query is often recommended over a single `match` query for most text search use cases, as it provides more flexibility and better matches user expectations.

::::



## Step 5: Filter and find exact matches [full-text-filter-tutorial-filtering]

[Filtering](../../explore-analyze/query-filter/languages/querydsl.md#filter-context) allows you to narrow down your search results based on exact criteria. Unlike full-text searches, filters are binary (yes/no) and do not affect the relevance score. Filters execute faster than queries because excluded results don’t need to be scored.

This [`bool`](elasticsearch://reference/query-languages/query-dsl/query-dsl-bool-query.md) query will return only blog posts in the "Breakfast" category.

```console
GET /cooking_blog/_search
{
  "query": {
    "bool": {
      "filter": [
        { "term": { "category.keyword": "Breakfast" } }  <1>
      ]
    }
  }
}
```

1. Note the use of `category.keyword` here. This refers to the [`keyword`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md) multi-field of the `category` field, ensuring an exact, case-sensitive match.


::::{tip}
The `.keyword` suffix accesses the unanalyzed version of a field, enabling exact, case-sensitive matching. This works in two scenarios:

1. **When using dynamic mapping for text fields**. Elasticsearch automatically creates a `.keyword` sub-field.
2. **When text fields are explicitly mapped with a `.keyword` sub-field**. For example, we explicitly mapped the `category` field in [Step 1](#full-text-filter-tutorial-create-index) of this tutorial.

::::



### Search for posts within a date range [full-text-filter-tutorial-range-query]

Often users want to find content published within a specific time frame. A [`range`](elasticsearch://reference/query-languages/query-dsl/query-dsl-range-query.md) query finds documents that fall within numeric or date ranges.

```console
GET /cooking_blog/_search
{
  "query": {
    "range": {
      "date": {
        "gte": "2023-05-01", <1>
        "lte": "2023-05-31" <2>
      }
    }
  }
}
```

1. Greater than or equal to May 1, 2023.
2. Less than or equal to May 31, 2023.



### Find exact matches [full-text-filter-tutorial-term-query]

Sometimes users want to search for exact terms to eliminate ambiguity in their search results. A [`term`](elasticsearch://reference/query-languages/query-dsl/query-dsl-term-query.md) query searches for an exact term in a field without analyzing it. Exact, case-sensitive matches on specific terms are often referred to as "keyword" searches.

Here you’ll search for the author "Maria Rodriguez" in the `author.keyword` field.

```console
GET /cooking_blog/_search
{
  "query": {
    "term": {
      "author.keyword": "Maria Rodriguez" <1>
    }
  }
}
```

1. The `term` query has zero flexibility. For example, here the queries `maria` or `maria rodriguez` would have zero hits, due to case sensitivity.


::::{tip}
Avoid using the `term` query for [`text` fields](elasticsearch://reference/elasticsearch/mapping-reference/text.md) because they are transformed by the analysis process.

::::



## Step 6: Combine multiple search criteria [full-text-filter-tutorial-complex-bool]

A [`bool`](elasticsearch://reference/query-languages/query-dsl/query-dsl-bool-query.md) query allows you to combine multiple query clauses to create sophisticated searches. In this tutorial scenario it’s useful for when users have complex requirements for finding recipes.

Let’s create a query that addresses the following user needs:

* Must be a vegetarian recipe
* Should contain "curry" or "spicy" in the title or description
* Should be a main course
* Must not be a dessert
* Must have a rating of at least 4.5
* Should prefer recipes published in the last month

```console
GET /cooking_blog/_search
{
  "query": {
    "bool": {
      "must": [
        { "term": { "tags": "vegetarian" } },
        {
          "range": {
            "rating": {
              "gte": 4.5
            }
          }
        }
      ],
      "should": [
        {
          "term": {
            "category": "Main Course"
          }
        },
        {
          "multi_match": {
            "query": "curry spicy",
            "fields": [
              "title^2",
              "description"
            ]
          }
        },
        {
          "range": {
            "date": {
              "gte": "now-1M/d"
            }
          }
        }
      ],
      "must_not": [ <1>
        {
          "term": {
            "category.keyword": "Dessert"
          }
        }
      ]
    }
  }
}
```

1. The `must_not` clause excludes documents that match the specified criteria. This is a powerful tool for filtering out unwanted results.


::::{dropdown} Example response
```console-result
{
  "took": 1,
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
    "max_score": 7.444513,
    "hits": [
      {
        "_index": "cooking_blog",
        "_id": "2",
        "_score": 7.444513,
        "_source": {
          "title": "Spicy Thai Green Curry: A Vegetarian Adventure", <1>
          "description": "Dive into the flavors of Thailand with this vibrant green curry. Packed with vegetables and aromatic herbs, this dish is both healthy and satisfying. Don't worry about the heat - you can easily adjust the spice level to your liking.", <2>
          "author": "Liam Chen",
          "date": "2023-05-05",
          "category": "Main Course", <3>
          "tags": [ <4>
            "thai",
            "vegetarian", <5>
            "curry",
            "spicy"
          ],
          "rating": 4.6 <6>
        }
      }
    ]
  }
}
```

1. The title contains "Spicy" and "Curry", matching our should condition. With the default [best_fields](elasticsearch://reference/query-languages/query-dsl/query-dsl-multi-match-query.md#type-best-fields) behavior, this field contributes most to the relevance score.
2. While the description also contains matching terms, only the best matching field’s score is used by default.
3. The recipe was published within the last month, satisfying our recency preference.
4. The "Main Course" category satisfies another `should` condition.
5. The "vegetarian" tag satisfies a `must` condition, while "curry" and "spicy" tags align with our `should` preferences.
6. The rating of 4.6 meets our minimum rating requirement of 4.5.


::::



## Learn more [full-text-filter-tutorial-learn-more]

This tutorial introduced the basics of full-text search and filtering in {{es}}. Building a real-world search experience requires understanding many more advanced concepts and techniques. Here are some resources once you’re ready to dive deeper:

* [Full-text search](full-text.md): Learn about the core components of full-text search in {{es}}.
* [Elasticsearch basics — Search and analyze data](../../explore-analyze/query-filter.md): Understand all your options for searching and analyzing data in {{es}}.
* [Text analysis](full-text/text-analysis-during-search.md): Understand how text is processed for full-text search.
* [Search your data](../search.md): Learn about more advanced search techniques using the `_search` API, including semantic search.