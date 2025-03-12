# Tutorial: Full-text search and filtering in Elasticsearch

This is a hands-on introduction to the basics of [full-text search](full-text.md) with Elasticsearch, also known as *lexical search*, and how to filter search results based on exact criteria.

In this scenario, we're implementing a search function for a cooking blog. The blog contains recipes with various attributes including textual content, categorical data, and numerical ratings.

:::{note}
This tutorial presents examples in two different query languages:
- **Query DSL**: The traditional JSON-based query language using the [`_search` API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)
- **ESQL (Elasticsearch Query Language)**: The newer SQL-like piped query language using the [`_query` API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-esql)

Each example is presented in both languages using tabs, allowing you to compare approaches and choose the syntax that works best for you.

For a comprehensive overview of the different query languages available in Elasticsearch, see [](../../explore-analyze/query-filter/languages/querying-for-search.md).
:::

## Requirements [full-text-filter-tutorial-requirements]

You’ll need a running {{es}} cluster, together with {{kib}} to use the Dev Tools API Console. Run the following command in your terminal to set up a [single-node local cluster in Docker](get-started.md):

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

## Step 3: Perform basic full-text searches

Full-text search involves executing text-based queries across one or more document fields. These queries calculate a relevance score for each matching document, based on how closely the document's content aligns with the search terms. Elasticsearch offers various query types, each with its own method for matching text and [relevance scoring](../../explore-analyze/query-filter/languages/querydsl.md#relevance-scores).

::::{tab-set}
:::{tab-item} Query DSL
### Basic match query

The [`match`](elasticsearch://reference/query-languages/query-dsl-match-query.md) query is the standard query for full-text, or "lexical", search. The query text will be analyzed according to the analyzer configuration specified on each field (or at query time).

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
:::

:::{tab-item} ES|QL
### Basic match query

In ESQL, the `MATCH` function provides similar full-text search capabilities. Here's how to search the `description` field for "fluffy pancakes":

```esql
POST /_query?format=txt
{
  "query": """
    FROM cooking_blog
    | WHERE description:"fluffy pancakes"
    | LIMIT 1000
  """
}
```

By default, like the Query DSL `match` query, the ESQL `MATCH` function uses `OR` logic between terms. This means it will match documents that contain either "fluffy" or "pancakes", or both, in the description field.

:::{tip}
You can see exactly which fields to include in the response using the `KEEP` command:

```esql
POST /_query?format=txt
{
  "query": """
    FROM cooking_blog
    | WHERE description:"fluffy pancakes"
    | KEEP title, description, rating
    | LIMIT 1000
  """
}
```
:::
:::
::::

### Require all terms in a match query

Sometimes you need to require that all search terms appear in the matching documents. Here's how to do that with both query languages:

::::{tab-set}
:::{tab-item} Query DSL
Specify the `and` operator to require both terms in the `description` field:

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

This stricter search returns *zero hits* on our sample data, as no document contains both "fluffy" and "pancakes" in the description.
:::

:::{tab-item} ES|QL
In ESQL, you can use the `operator` parameter to specify the `AND` operator:

```esql
POST /_query?format=txt
{
  "query": """
    FROM cooking_blog
    | WHERE MATCH(description, "fluffy pancakes", {"operator": "AND"})
    | LIMIT 1000
  """
}
```

This stricter search returns *zero hits* on our sample data, as no document contains both "fluffy" and "pancakes" in the description.
:::
::::

### Specify a minimum number of terms to match

Sometimes requiring all terms is too strict, but the default OR behavior is too lenient. You can specify a minimum number of terms that must match:

::::{tab-set}
:::{tab-item} Query DSL
Use the [`minimum_should_match`](elasticsearch://reference/query-languages/query-dsl-minimum-should-match.md) parameter to specify the minimum number of terms a document should have to be included in the search results:

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

This query searches the title field to match at least 2 of the 3 terms: "fluffy", "pancakes", or "breakfast".
:::

:::{tab-item} ES|QL
In ESQL, you can use the `minimum_should_match` parameter in a similar way:

```esql
POST /_query?format=txt
{
  "query": """
    FROM cooking_blog
    | WHERE MATCH(title, "fluffy pancakes breakfast", {"minimum_should_match": 2})
    | LIMIT 1000
  """
}
```

This query searches the title field to match at least 2 of the 3 terms: "fluffy", "pancakes", or "breakfast".
:::
::::

## Step 4: Search across multiple fields at once

When users enter a search query, they often don't know (or care) whether their search terms appear in a specific field. Both Query DSL and ESQL provide ways to search across multiple fields simultaneously:

::::{tab-set}
:::{tab-item} Query DSL
A [`multi_match`](elasticsearch://reference/query-languages/query-dsl-multi-match-query.md) query allows searching across multiple fields simultaneously:

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
      "fields": ["title^3", "description^2", "tags"]
    }
  }
}
```

The `^` syntax applies a boost to specific fields:
* `title^3`: The title field is 3 times more important than an unboosted field
* `description^2`: The description is 2 times more important
* `tags`: No boost applied (equivalent to `^1`)
:::

:::{tab-item} ES|QL
In ESQL, you can use multiple `MATCH` functions combined with OR operators to search across different fields:

```esql
POST /_query?format=txt
{
  "query": """
    FROM cooking_blog
    | WHERE title:"vegetarian curry" OR description:"vegetarian curry" OR tags:"vegetarian curry"
    | LIMIT 1000
  """
}
```

For field boosting in ESQL, we can use a more complex approach that makes use of the query's relevance scores:

```esql
POST /_query?format=txt
{
  "query": """
    FROM cooking_blog metadata _score
    | WHERE title:"vegetarian curry" 
        OR description:"vegetarian curry" 
        OR tags:"vegetarian curry"
    | KEEP title, description, tags, _score
    | SORT _score DESC
    | LIMIT 1000
  """
}
```

:::
::::

## Step 5: Filter and find exact matches

Filtering allows you to narrow down your search results based on exact criteria. Unlike full-text searches, filters are binary (yes/no) and do not affect the relevance score. Filters execute faster than queries because excluded results don't need to be scored.

::::{tab-set}
:::{tab-item} Query DSL
This [`bool`](elasticsearch://reference/query-languages/query-dsl-bool-query.md) query will return only blog posts in the "Breakfast" category:

```console
GET /cooking_blog/_search
{
  "query": {
    "bool": {
      "filter": [
        { "term": { "category.keyword": "Breakfast" } }
      ]
    }
  }
}
```

Note the use of `category.keyword` here. This refers to the [`keyword`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md) multi-field of the `category` field, ensuring an exact, case-sensitive match.
:::

:::{tab-item} ES|QL
In ESQL, you can use the `WHERE` clause with a direct field comparison for exact matches:

```esql
POST /_query?format=txt
{
  "query": """
    FROM cooking_blog
    | WHERE category.keyword == "Breakfast"
    | KEEP title, author, rating, tags
    | SORT rating DESC
    | LIMIT 1000
  """
}
```

Just like in Query DSL, we use the `.keyword` field to ensure an exact, case-sensitive match.
:::
::::

### Search for posts within a date range

Often users want to find content published within a specific time frame:

::::{tab-set}
:::{tab-item} Query DSL
A [`range`](elasticsearch://reference/query-languages/query-dsl-range-query.md) query finds documents that fall within numeric or date ranges:

```console
GET /cooking_blog/_search
{
  "query": {
    "range": {
      "date": {
        "gte": "2023-05-01",
        "lte": "2023-05-31"
      }
    }
  }
}
```
:::

:::{tab-item} ES|QL
In ESQL, you can use comparison operators in the `WHERE` clause for date ranges:

```esql
POST /_query?format=txt
{
  "query": """
    FROM cooking_blog
    | WHERE date >= "2023-05-01" AND date <= "2023-05-31"
    | KEEP title, author, rating, tags
    | LIMIT 1000
  """
}
```
:::
::::

### Find exact matches

Sometimes users want to search for exact terms to eliminate ambiguity in their search results:

::::{tab-set}
:::{tab-item} Query DSL
A [`term`](elasticsearch://reference/query-languages/query-dsl-term-query.md) query searches for an exact term in a field without analyzing it:

```console
GET /cooking_blog/_search
{
  "query": {
    "term": {
      "author.keyword": "Maria Rodriguez"
    }
  }
}
```

The `term` query has zero flexibility. For example, here the queries `maria` or `maria rodriguez` would have zero hits, due to case sensitivity.
:::

:::{tab-item} ES|QL
In ESQL, exact matching can be done using the equality operator on keyword fields:

```esql
POST /_query?format=txt
{
  "query": """
    FROM cooking_blog
    | WHERE category.keyword == "Breakfast"
    | KEEP title, author, rating, tags
    | LIMIT 1000
  """
}
```

Like the `term` query in Query DSL, this has zero flexibility and is case-sensitive.
:::
::::

## Step 6: Combine multiple search criteria

Complex searches often require combining multiple search criteria:

::::{tab-set}
:::{tab-item} Query DSL
A [`bool`](elasticsearch://reference/query-languages/query-dsl-bool-query.md) query allows you to combine multiple query clauses:

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
      "must_not": [
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

The `must_not` clause excludes documents that match the specified criteria. This is a powerful tool for filtering out unwanted results.
:::

:::{tab-item} ES|QL
In ESQL, you can combine multiple criteria using logical operators (AND, OR, NOT):

```console
POST /_query?format=txt
{
  "query": """
    FROM cooking_blog metadata _score
    | WHERE rating >= 4.5
      AND NOT category.keyword == "Dessert"
      AND (title:"curry spicy" OR description:"curry spicy")
    | SORT _score DESC
    | KEEP title, author, rating, tags, description
    | LIMIT 1000
  """
}
```

For more complex relevance scoring with combined criteria, you can use the `EVAL` command to calculate custom scores:

```console
GET /_query/esql
{
  "query": "
    FROM cooking_blog
    | WHERE tags == \"vegetarian\" AND rating >= 4.5
    | EVAL title_score = SCORE(MATCH(title, \"curry spicy\")) * 2
    | EVAL desc_score = SCORE(MATCH(description, \"curry spicy\"))
    | EVAL combined_score = title_score + desc_score
    | EVAL category_boost = IF(category == \"Main Course\", 1.0, 0.0)
    | EVAL date_boost = IF(date >= \"now-1M/d\", 0.5, 0.0)
    | EVAL final_score = combined_score + category_boost + date_boost
    | WHERE NOT category.keyword == \"Dessert\"
    | WHERE final_score > 0
    | SORT final_score DESC
  "
}
```

This ESQL query achieves the same goals as the complex bool query but with a more explicit scoring mechanism:
1. Requires "vegetarian" tag and rating >= 4.5
2. Computes separate scores for title and description matches
3. Adds boosts for Main Course category and recent dates
4. Excludes Desserts
5. Sorts by the final combined score
:::
::::

## Learn more

This tutorial introduced the basics of full-text search and filtering in Elasticsearch using both Query DSL and ESQL. Building a real-world search experience requires understanding many more advanced concepts and techniques. Here are some resources once you're ready to dive deeper:

* [Full-text search](full-text.md): Learn about the core components of full-text search in Elasticsearch.
* [Elasticsearch basics — Search and analyze data](../../explore-analyze/query-filter.md): Understand all your options for searching and analyzing data in Elasticsearch.
* [Text analysis](full-text/text-analysis-during-search.md): Understand how text is processed for full-text search.
* [Search your data](../search.md): Learn about more advanced search techniques using the `_search` API, including semantic search.
* [Elasticsearch SQL & ESQL](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql.html): Learn more about the ESQL query language.