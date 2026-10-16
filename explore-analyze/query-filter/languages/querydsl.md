---
navigation_title: Query DSL
description: Learn how Query DSL runs full-text, semantic, and filtered searches and aggregations in Elasticsearch, and how query context and filter context differ.
meta_title: Query DSL - Elasticsearch
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/query-filter-context.html
applies_to:
  serverless: ga
  stack: ga
products:
  - id: elasticsearch
  - id: kibana
type: overview
---

# Query DSL overview

## What's Query DSL? [search-analyze-query-dsl]

**Query DSL** is a full-featured JSON-style query language that enables complex searching, filtering, and aggregations. It is the original query language for {{es}}.

The [`_search` endpoint]({{es-apis}}operation/operation-search) accepts queries written in Query DSL syntax.

In {{kib}}, you can send Query DSL requests from [Console](/explore-analyze/query-filter/tools/console.md). In Discover, you can also write a filter as Query DSL: select **Add filter**, then **Edit as Query DSL**.

To look up a specific query type and its parameters, refer to the [Query DSL reference](elasticsearch://reference/query-languages/querydsl.md).

Query DSL is one of several query languages in {{es}}. To compare it with {{esql}} and retrievers, refer to [Build your search queries](/solutions/search/querying-for-search.md). For all query languages, refer to [Query languages](/explore-analyze/query-filter/languages.md).


### Search and filter with Query DSL [search-analyze-query-dsl-search-filter]

Query DSL supports a wide range of search techniques, including the following:

* [**Full-text search**](/solutions/search/full-text.md): Search text that {{es}} analyzes and indexes, with support for phrase or proximity queries, fuzzy matches, and more.
* [**Keyword search**](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md): Search for exact matches using `keyword` fields.
* [**Semantic search**](/solutions/search/semantic-search/semantic-search-semantic-text.md): Search `semantic_text` fields using dense or sparse vector search on embeddings generated in your {{es}} cluster.
* [**Vector search**](/solutions/search/vector/knn.md): Search for similar dense vectors using the kNN algorithm for embeddings generated outside of {{es}}.
* [**Geospatial search**](elasticsearch://reference/query-languages/query-dsl/geo-queries.md): Search for locations and calculate spatial relationships using geospatial queries.

You can also filter data using Query DSL. Filters enable you to include or exclude documents by retrieving documents that match specific field-level criteria. A query that uses the `filter` parameter indicates [filter context](#filter-context).

### Analyze with Query DSL [search-analyze-data-query-dsl]

[Aggregations](../aggregations.md) are the primary tool for analyzing {{es}} data using Query DSL. Aggregations enable you to build complex summaries of your data and gain insight into key metrics, patterns, and trends.

Because aggregations use the same data structures as search, they are also fast. This enables you to analyze and visualize your data in real time. You can search documents, filter results, and perform analytics at the same time, on the same data, in a single request. That means {{es}} calculates aggregations in the context of the search query.

The following aggregation types are available:

* [Metric](elasticsearch://reference/aggregations/metrics.md): Calculate metrics, such as a sum or average, from field values.
* [Bucket](elasticsearch://reference/aggregations/bucket.md): Group documents into buckets based on field values, ranges, or other criteria.
* [Pipeline](elasticsearch://reference/aggregations/pipeline.md): Run aggregations on the results of other aggregations.

Run aggregations by specifying the [search API]({{es-apis}}operation/operation-search)'s `aggs` parameter. Learn more in [Run an aggregation](/explore-analyze/query-filter/aggregations.md#run-an-agg).


## How does it work? [query-dsl]

Think of the Query DSL as an AST (Abstract Syntax Tree) of queries, consisting of two types of clauses:

**Leaf query clauses**: Leaf query clauses look for a particular value in a particular field, such as the [`match`](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md), [`term`](elasticsearch://reference/query-languages/query-dsl/query-dsl-term-query.md) or [`range`](elasticsearch://reference/query-languages/query-dsl/query-dsl-range-query.md) queries. You can use these queries by themselves.

**Compound query clauses**: Compound query clauses wrap other leaf **or** compound queries to combine multiple queries logically (such as the [`bool`](elasticsearch://reference/query-languages/query-dsl/query-dsl-bool-query.md) or [`dis_max`](elasticsearch://reference/query-languages/query-dsl/query-dsl-dis-max-query.md) query) or to alter their behavior (such as the [`constant_score`](elasticsearch://reference/query-languages/query-dsl/query-dsl-constant-score-query.md) query).

Query clauses behave differently depending on whether you use them in [query context or filter context](#query-filter-context).

## Query and filter context [query-filter-context]

### Relevance scores [relevance-scores]

By default, {{es}} sorts matching search results by **relevance score**, which measures how well each document matches a query.

The relevance score is a positive floating point number, returned in the `_score` metadata field of the [search]({{es-apis}}operation/operation-search) API. The higher the `_score`, the more relevant the document. While each query type can calculate relevance scores differently, score calculation also depends on whether you use the query clause in a **query** or **filter** context.


### Query context [query-context]

In the query context, a query clause answers the question *How well does this document match this query clause?* Besides deciding whether the document matches, the query clause also calculates a relevance score in the `_score` metadata field.

Query context is in effect whenever you pass a query clause to a `query` parameter, such as the `query` parameter in the [search]({{es-apis}}operation/operation-search#request-body-search-query) API.


### Filter context [filter-context]

A query clause in filter context is called a filter. A filter answers the binary question “Does this document match this query clause?” with "yes" or "no". Filtering has several benefits:

1. **Binary logic**: In a filter context, a query clause determines document matches based on a yes/no criterion, without score calculation.
2. **Performance**: Because filters don’t compute relevance scores, they run faster than query clauses in query context.
3. **Caching**: {{es}} automatically caches frequently used filters, speeding up subsequent search performance.
4. **Resource efficiency**: Filters consume less CPU resources compared to full-text queries.
5. **Query combination**: You can combine filters with scored queries to refine result sets efficiently.

Filters are particularly effective for querying structured data and implementing "must have" criteria in complex searches.

Structured data refers to information that is highly organized and formatted in a predefined manner. In the context of {{es}}, this typically includes:

* Numeric fields (integers, floating-point numbers)
* Dates and timestamps
* Boolean values
* Keyword fields (exact match strings)
* Geo-points and geo-shapes

Unlike full-text fields, structured data has a consistent, predictable format, making it ideal for precise filtering operations.

Common filter applications include:

* Date range checks: for example is the `timestamp` field between 2015 and 2016
* Specific field value checks: for example is the `status` field equal to "published" or is the `author` field equal to "John Doe"

Filter context applies when you pass a query clause to a `filter` parameter, such as:

* `filter` or `must_not` parameters in [`bool`](elasticsearch://reference/query-languages/query-dsl/query-dsl-bool-query.md)  queries
* `filter` parameter in [`constant_score`](elasticsearch://reference/query-languages/query-dsl/query-dsl-constant-score-query.md) queries
* [`filter`](elasticsearch://reference/aggregations/search-aggregations-bucket-filter-aggregation.md) aggregations

Filters optimize query performance and efficiency, especially for structured data queries and when combined with full-text searches.


### Example of query and filter contexts [query-filter-context-ex]

The following example shows query clauses in query context and filter context in the `search` API. The query matches documents where all the following conditions are met:

* The `title` field contains the word `search`.
* The `content` field contains the word `elasticsearch`.
* The `status` field contains the exact word `published`.
* The `publish_date` field contains a date from 1 Jan 2015 onwards.

To run this request, you need the `read` [index privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) on the target indices.

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
2. The `bool` and two `match` clauses run in query context, so they score how well each document matches.
3. The `filter` parameter indicates filter context. Its `term` and `range` clauses run in filter context. They filter out documents that don’t match, but they don’t affect the score for matching documents.

Use query clauses in query context for conditions that should affect the score of matching documents (that is, how well the document matches), and use all other query clauses in filter context.

::::{warning}
Scores calculated for queries in query context are single precision floating point numbers, which have only 24 bits for significand’s precision. Score calculations that exceed the significand’s precision lose precision when converted to floats.
::::

## Limit expensive queries

$$$query-dsl-allow-expensive-queries$$$

Some query types are resource-intensive, which can slow searches and affect cluster stability. Examples are `script` queries, joining queries, and queries on [runtime fields](/manage-data/data-store/mapping/runtime-fields.md).

{{es}} runs these queries by default. Whether you can block them depends on your deployment:

* {applies_to}`serverless: ga` You can't block these queries. The `search.allow_expensive_queries` setting isn't configurable.
* {applies_to}`stack: ga` To block these queries, set `search.allow_expensive_queries` to `false` with the [cluster update settings API]({{es-apis}}operation/operation-cluster-put-settings).

For the full list of queries and the details of blocking them, refer to [Limit expensive queries](elasticsearch://reference/query-languages/querydsl.md#query-dsl-allow-expensive-queries) in the Query DSL reference.

To browse every query type, refer to the [Query DSL reference](elasticsearch://reference/query-languages/querydsl.md). To run and test searches, refer to [Build your search queries](/solutions/search/querying-for-search.md).
