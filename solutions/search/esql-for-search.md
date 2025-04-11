---
applies_to:
  stack: preview
  serverless: preview
---

% ℹ️ 8.x version of this doc lives in elasticsearch repo
% https://github.com/elastic/elasticsearch/blob/8.x/docs/reference/esql/esql-for-search.asciidoc

# {{esql}} for search [esql-for-search]

This page provides an overview of how to use {{esql}} for search use cases.

::::{tip}
Prefer to get started with a hands-on tutorial? Check out [Search and filter with {{esql}}](esql-search-tutorial.md).
::::


## Overview

The following table summarizes the key search features available in [{{esql}}](/explore-analyze/query-filter/languages/esql.md) and when they were introduced.

| Feature | Available since | Description |
|---------|----------------|-------------|
| [Full text search functions](elasticsearch://reference/query-languages/esql/functions-operators/search-functions.md) | 8.17 | Perform basic text searches with `MATCH` function or match operator (`:`) |
| [Query string function](#esql-for-search-query-string) | 8.17 | Execute complex queries with `QSTR` using Query String syntax |
| [Relevance scoring](#esql-for-search-scoring) | 8.18/9.0 | Calculate and sort by relevance with `METADATA _score` |
| Enhanced match options | 8.18/9.0 | Configure text searches with additional parameters for the `MATCH` function |
| [Kibana Query Language](#esql-for-search-kql) | 8.18/9.0 | Use Kibana Query Language with the `KQL` function |
| [Semantic search](#esql-for-search-semantic) | 8.18/9.0 | Perform semantic searches on `semantic_text` field types |
| [Hybrid search](#esql-for-search-hybrid) | 8.18/9.0 | Combine lexical and semantic search approaches with custom weights |

## Filtering vs. searching [esql-filtering-vs-searching]

{{esql}} can be used for both simple filtering and relevance-based searching:

* **Filtering** removes non-matching documents without calculating relevance scores
* **Searching** both filters documents and ranks them by how well they match the query

Note that filtering is faster than searching, because it doesn't require score calculations.

### Relevance scoring [esql-for-search-scoring]

To get the most relevant results first, you need to use `METADATA _score` and sort by score. For example:

```esql
FROM books METADATA _score
| WHERE match(title, "Shakespeare") OR match(plot, "Shakespeare")
| SORT _score DESC
```

### How `_score` works [esql-for-search-how-scoring-works]

When working with relevance scoring in {{esql}}:

* If you don't include `METADATA _score` in your query, this only performs filtering operations with no relevance calculation.
* When you include `METADATA _score`, any search function included in `WHERE` conditions contribute to the relevance score. This means that every occurrence of `MATCH`, `QSTR` and `KQL` will affect the score.
* Filtering operations that are not search functions, like range conditions and exact matches, don't affect the score.
* Including `METADATA _score` doesn't automatically sort your results by relevance. You must explicitly use `SORT _score DESC` or `SORT _score ASC` to order your results by relevance.

## Full text search [esql-for-search-full-text]

### `MATCH` function and operator [esql-for-search-match-function-operator]

{{esql}} offers two syntax options for `match`, which replicate the functionality of [match](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md) queries in Query DSL.

Use the compact operator syntax (`:`) for simple text matching with default parameters.

```esql
FROM logs | WHERE message: "connection error"
```

Use the `match()` function syntax when you need to pass additional parameters:

```esql
FROM products | WHERE match(name, "laptop", { "boost": 2.0 })
```

These full-text functions address several key limitations that existed for text filtering in {{esql}}:

* They work directly on multivalued fields, returning results when any value in a multivalued field matches the query
* They leverage analyzers, ensuring the query is analyzed with the same process as the indexed data (enabling case-insensitive matching, ASCII folding, stopword removal, and synonym support)
* They are highly performant, using Lucene index structures rather than pattern matching or regular expressions to locate terms in your data

Refer to this blog for more context: [Introducing full text filtering in {{esql}}](https://www.elastic.co/search-labs/blog/filtering-in-esql-full-text-search-match-qstr).

::::{tip}
See [Match field parameters](elasticsearch://reference/query-languages/esql/functions-operators/search-functions.md#esql-match) for more advanced options using match.
::::

::::{important}
These queries match documents but don't automatically sort by relevance. To get the most relevant results first, you need to use `METADATA _score` and sort by score. See [Relevance scoring](#esql-for-search-scoring) for more information.
::::

### Query string (`QSTR`) function [esql-for-search-query-string]

The [`qstr` function](elasticsearch://reference/query-languages/esql/functions-operators/search-functions.md#esql-qstr) provides the same functionality as the Query DSL's `query_string` query. This is for advanced use cases, such as wildcard searches, searches across multiple fields, and more.

```esql
FROM articles METADATA _score
| WHERE QSTR("(new york city) OR (big apple)")
| SORT _score DESC
| LIMIT 10
```

For complete details, refer to the [Query DSL `query_string` docs](elasticsearch://reference/query-languages/query-dsl/query-dsl-query-string-query.md).

### `KQL` function [esql-for-search-kql]

Use the [KQL function](elasticsearch://reference/query-languages/esql/functions-operators/search-functions.md#esql-kql) to use the [Kibana Query Language](/explore-analyze/query-filter/languages/kql.md) in your {{esql}} queries:

```esql
FROM logs*
| WHERE KQL("http.request.method:GET AND agent.type:filebeat")
```

The `kql` function is useful when transitioning queries from Kibana's Discover, Dashboard, or other interfaces that use KQL. This will allow you to gradually migrate queries to {{esql}} without needing to rewrite them all at once.

## Semantic search [esql-for-search-semantic]

You can perform semantic searches over [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field types using the same match syntax as full-text search.

This example uses the match operator `:`:

```esql
FROM articles METADATA _score
| WHERE semantic_content: "What are the impacts of climate change on agriculture?"
| SORT _score DESC
```

This example uses the match function:

```esql
FROM articles METADATA _score
| WHERE match(semantic_content, "What are the impacts of climate change on agriculture?")
| SORT _score DESC
```

## Hybrid search [esql-for-search-hybrid]

[Hybrid search](/solutions/search/hybrid-search.md) combines lexical and semantic search with custom weights:

```esql
FROM books METADATA _score
| WHERE match(semantic_title, "fantasy adventure", { "boost": 0.75 }) 
    OR match(title, "fantasy adventure", { "boost": 0.25 })
| SORT _score DESC
```

## Limitations [esql-for-search-limitations]

Refer to [{{esql}} limitations](elasticsearch://reference/query-languages/esql/limitations.md#esql-limitations-full-text-search) for a list of known limitations.

## Next steps [esql-for-search-next-steps]

### Tutorials and how-to guides [esql-for-search-tutorials]

- [Search and filter with {{esql}}](esql-search-tutorial.md): Hands-on tutorial for getting started with search tools in {esql}
- [Semantic search with semantic_text](semantic-search/semantic-search-semantic-text.md): Learn how to use the `semantic_text` field type

### Technical reference [esql-for-search-reference]

- [Search functions](elasticsearch://reference/query-languages/esql/functions-operators/search-functions.md): Complete reference for all search functions
- [Limitations](elasticsearch://reference/query-languages/esql/limitations.md#esql-limitations-full-text-search): Current limitations for search in {{esql}}

### Background concepts [esql-for-search-concepts]

- [Analysis](/manage-data/data-store/text-analysis.md): Learn how text is processed for full-text search
- [Semantic search](semantic-search.md): Get an overview of semantic search in Elasticsearch
- [Query vs filter context](elasticsearch://reference/query-languages/query-dsl/query-filter-context.md): Understand the difference between query and filter contexts in Elasticsearch

### Related blog posts [esql-for-search-blogs]

% TODO* https://www.elastic.co/blog/esql-you-know-for-search-scoring-semantic-search[{{esql}}, you know for Search]: Introducing scoring and semantic search
- [Introducing full text filtering in {{esql}}](https://www.elastic.co/search-labs/blog/filtering-in-esql-full-text-search-match-qstr): Overview of {{esql}}'s text filtering capabilities