---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Query DSL

## What's Query DSL? [search-analyze-query-dsl]

**Query DSL** is a full-featured JSON-style query language that enables complex searching, filtering, and aggregations. It is the original and most powerful query language for {{es}} today.

The [`_search` endpoint](../../../solutions/search/querying-for-search.md) accepts queries written in Query DSL syntax.


### Search and filter with Query DSL [search-analyze-query-dsl-search-filter]

Query DSL supports a wide range of search techniques, including the following:

* [**Full-text search**](/solutions/search/full-text.md): Search text that has been analyzed and indexed to support phrase or proximity queries, fuzzy matches, and more.
* [**Keyword search**](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md): Search for exact matches using `keyword` fields.
* [**Semantic search**](/solutions/search/semantic-search/semantic-search-semantic-text.md): Search `semantic_text` fields using dense or sparse vector search on embeddings generated in your {{es}} cluster.
* [**Vector search**](/solutions/search/vector/knn.md): Search for similar dense vectors using the kNN algorithm for embeddings generated outside of {{es}}.
* [**Geospatial search**](elasticsearch://reference/query-languages/query-dsl/geo-queries.md): Search for locations and calculate spatial relationships using geospatial queries.

You can also filter data using Query DSL. Filters enable you to include or exclude documents by retrieving documents that match specific field-level criteria. A query that uses the `filter` parameter indicates [filter context](#filter-context).

### Analyze with Query DSL [search-analyze-data-query-dsl]

[Aggregations](../aggregations.md) are the primary tool for analyzing {{es}} data using Query DSL. Aggregations enable you to build complex summaries of your data and gain insight into key metrics, patterns, and trends.

Because aggregations leverage the same data structures used for search, they are also very fast. This enables you to analyze and visualize your data in real time. You can search documents, filter results, and perform analytics at the same time, on the same data, in a single request. That means aggregations are calculated in the context of the search query.

The following aggregation types are available:

* [Metric](elasticsearch://reference/aggregations/metrics.md): Calculate metrics, such as a sum or average, from field values.
* [Bucket](elasticsearch://reference/aggregations/bucket.md): Group documents into buckets based on field values, ranges, or other criteria.
* [Pipeline](elasticsearch://reference/aggregations/pipeline.md): Run aggregations on the results of other aggregations.

Run aggregations by specifying the [search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search)'s `aggs` parameter. Learn more in [Run an aggregation](/explore-analyze/query-filter/aggregations.md#run-an-agg).


## How does it work? [query-dsl]

Think of the Query DSL as an AST (Abstract Syntax Tree) of queries, consisting of two types of clauses:

**Leaf query clauses**: Leaf query clauses look for a particular value in a particular field, such as the [`match`](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md), [`term`](elasticsearch://reference/query-languages/query-dsl/query-dsl-term-query.md) or [`range`](elasticsearch://reference/query-languages/query-dsl/query-dsl-range-query.md) queries. These queries can be used by themselves.

**Compound query clauses**: Compound query clauses wrap other leaf **or** compound queries and are used to combine multiple queries in a logical fashion (such as the [`bool`](elasticsearch://reference/query-languages/query-dsl/query-dsl-bool-query.md) or [`dis_max`](elasticsearch://reference/query-languages/query-dsl/query-dsl-dis-max-query.md) query), or to alter their behavior (such as the [`constant_score`](elasticsearch://reference/query-languages/query-dsl/query-dsl-constant-score-query.md) query).

Query clauses behave differently depending on whether they are used in [query context or filter context](#query-filter-context).

$$$query-dsl-allow-expensive-queries$$$

**Allow expensive queries**: Certain types of queries will generally execute slowly due to the way they are implemented, which can affect the stability of the cluster. Those queries can be categorized as follows:

 - Queries that need to do linear scans to identify matches:

    - [`script` queries](elasticsearch://reference/query-languages/query-dsl/query-dsl-script-query.md)
    - queries on [numeric](elasticsearch://reference/elasticsearch/mapping-reference/number.md), [date](elasticsearch://reference/elasticsearch/mapping-reference/date.md), [boolean](elasticsearch://reference/elasticsearch/mapping-reference/boolean.md), [ip](elasticsearch://reference/elasticsearch/mapping-reference/ip.md), [geo_point](elasticsearch://reference/elasticsearch/mapping-reference/geo-point.md) or [keyword](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md) fields that are not indexed but have [doc values](elasticsearch://reference/elasticsearch/mapping-reference/doc-values.md) enabled

 - Queries that have a high up-front cost:

    - [`fuzzy` queries](elasticsearch://reference/query-languages/query-dsl/query-dsl-fuzzy-query.md) (except on [`wildcard`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#wildcard-field-type) fields)
    - [`regexp` queries](elasticsearch://reference/query-languages/query-dsl/query-dsl-regexp-query.md) (except on [`wildcard`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#wildcard-field-type) fields)
    - [`prefix` queries](elasticsearch://reference/query-languages/query-dsl/query-dsl-prefix-query.md)  (except on [`wildcard`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#wildcard-field-type) fields or those without [`index_prefixes`](elasticsearch://reference/elasticsearch/mapping-reference/index-prefixes.md))
    - [`wildcard` queries](elasticsearch://reference/query-languages/query-dsl/query-dsl-wildcard-query.md) (except on [`wildcard`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md#wildcard-field-type) fields)
    - [`range` queries](elasticsearch://reference/query-languages/query-dsl/query-dsl-range-query.md) on [`text`](elasticsearch://reference/elasticsearch/mapping-reference/text.md) and [`keyword`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md) fields

 - [Joining queries](elasticsearch://reference/query-languages/query-dsl/joining-queries.md)
 - Queries that may have a high per-document cost:

    - [`script_score` queries](elasticsearch://reference/query-languages/query-dsl/query-dsl-script-score-query.md)
    - [`percolate` queries](elasticsearch://reference/query-languages/query-dsl/query-dsl-percolate-query.md)


The execution of such queries can be prevented by setting the value of the `search.allow_expensive_queries` setting to `false` (defaults to `true`).

## Query and filter context [query-filter-context]

### Relevance scores [relevance-scores]

By default, Elasticsearch sorts matching search results by **relevance score**, which measures how well each document matches a query.

The relevance score is a positive floating point number, returned in the `_score` metadata field of the [search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) API. The higher the `_score`, the more relevant the document. While each query type can calculate relevance scores differently, score calculation also depends on whether the query clause is run in a **query** or **filter** context.


### Query context [query-context]

In the query context, a query clause answers the question *How well does this document match this query clause?* Besides deciding whether or not the document matches, the query clause also calculates a relevance score in the `_score` metadata field.

Query context is in effect whenever a query clause is passed to a `query` parameter, such as the `query` parameter in the [search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#request-body-search-query) API.


### Filter context [filter-context]

A filter answers the binary question “Does this document match this query clause?”. The answer is simply "yes" or "no". Filtering has several benefits:

1. **Simple binary logic**: In a filter context, a query clause determines document matches based on a yes/no criterion, without score calculation.
2. **Performance**: Because they don’t compute relevance scores, filters execute faster than queries.
3. **Caching**: {{es}} automatically caches frequently used filters, speeding up subsequent search performance.
4. **Resource efficiency**: Filters consume less CPU resources compared to full-text queries.
5. **Query combination**: Filters can be combined with scored queries to refine result sets efficiently.

Filters are particularly effective for querying structured data and implementing "must have" criteria in complex searches.

Structured data refers to information that is highly organized and formatted in a predefined manner. In the context of Elasticsearch, this typically includes:

* Numeric fields (integers, floating-point numbers)
* Dates and timestamps
* Boolean values
* Keyword fields (exact match strings)
* Geo-points and geo-shapes

Unlike full-text fields, structured data has a consistent, predictable format, making it ideal for precise filtering operations.

Common filter applications include:

* Date range checks: for example is the `timestamp` field between 2015 and 2016
* Specific field value checks: for example is the `status` field equal to "published" or is the `author` field equal to "John Doe"

Filter context applies when a query clause is passed to a `filter` parameter, such as:

* `filter` or `must_not` parameters in [`bool`](elasticsearch://reference/query-languages/query-dsl/query-dsl-bool-query.md)  queries
* `filter` parameter in [`constant_score`](elasticsearch://reference/query-languages/query-dsl/query-dsl-constant-score-query.md) queries
* [`filter`](elasticsearch://reference/aggregations/search-aggregations-bucket-filter-aggregation.md) aggregations

Filters optimize query performance and efficiency, especially for structured data queries and when combined with full-text searches.


### Example of query and filter contexts [query-filter-context-ex]

Below is an example of query clauses being used in query and filter context in the `search` API. This query will match documents where all of the following conditions are met:

* The `title` field contains the word `search`.
* The `content` field contains the word `elasticsearch`.
* The `status` field contains the exact word `published`.
* The `publish_date` field contains a date from 1 Jan 2015 onwards.

```console
GET /_search
{
  "query": { <1>
    "bool": { <2>
      "must": [
        { "match": { "title":   "Search"        }},
        { "match": { "content": "Elasticsearch" }}
      ],
      "filter": [ <3>
        { "term":  { "status": "published" }},
        { "range": { "publish_date": { "gte": "2015-01-01" }}}
      ]
    }
  }
}
```

1. The `query` parameter indicates query context.
2. The `bool` and two `match` clauses are used in query context, which means that they are used to score how well each document matches.
3. The `filter` parameter indicates filter context. Its `term` and `range` clauses are used in filter context. They will filter out documents which do not match, but they will not affect the score for matching documents.


::::{warning}
Scores calculated for queries in query context are represented as single precision floating point numbers; they have only 24 bits for significand’s precision. Score calculations that exceed the significand’s precision will be converted to floats with loss of precision.
::::


::::{tip}
Use query clauses in query context for conditions which should affect the score of matching documents (i.e. how well does the document match), and use all other query clauses in filter context.
::::
