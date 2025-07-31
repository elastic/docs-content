---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/8.18/esql-for-search.html
applies_to:
  stack: preview 9.0, ga 9.1
  serverless: ga
products:
  - id: elasticsearch
---

% ℹ️ 8.x version of this doc lives in elasticsearch repo
% https://github.com/elastic/elasticsearch/blob/8.x/docs/reference/esql/esql-for-search.asciidoc

# {{esql}} for search [esql-for-search]

This page provides an overview of how to use {{esql}} for search use cases.

::::{tip}
For a hands-on tutorial check out [Search and filter with {{esql}}](esql-search-tutorial.md).
::::

## {{esql}} search quick reference

The following table summarizes the key search features available in [{{esql}}](/explore-analyze/query-filter/languages/esql.md) and when they were introduced, organized chronologically by release.

| Feature | Description | Available since |
|---------|-------------|----------------|
| [Match function/operator](#match-function-and-operator) | Perform basic text searches with `MATCH` function or match operator (`:`) | 8.17 |
| [Query string function](#query-string-qstr-function) | Execute complex queries with `QSTR` using Query String syntax | 8.17 |
| [Relevance scoring](#esql-for-search-scoring) | Calculate and sort by relevance with `METADATA _score` | 8.18/9.0 |
| [Semantic search](#semantic-search) | Perform semantic searches on `semantic_text` field types | 8.18/9.0 |
| [Hybrid search](#hybrid-search) | Combine lexical and semantic search approaches with custom weights | 8.18/9.0 |
| [Kibana Query Language](#kql-function) | Use Kibana Query Language with the `KQL` function | 8.18/9.0 |
| [Match phrase function](#match_phrase-function) | Perform phrase matching with `MATCH_PHRASE` function | 8.19/9.1 |

## How search works in {{esql}}

{{esql}} provides two distinct approaches for finding documents: filtering and searching. Understanding the difference is crucial for building effective queries and choosing the right approach for your use case.

**Filtering** removes documents that don't meet your criteria. It's a binary yes/no decision - documents either match your conditions or they don't. Filtering is faster because it doesn't calculate relevance scores and leverages efficient index structures for exact matches, ranges, and boolean logic.

**Searching** both filters documents and ranks them by relevance. It calculates a score for each matching document based on how well the content matches your query, allowing you to sort results from most relevant to least relevant. Search functions use advanced text analysis including stemming, synonyms, and fuzzy matching.

**When to choose filtering:**
- Exact category matches (`category.keyword == "Electronics"`)
- Date ranges (`date >= "2023-01-01"`)
- Numerical comparisons (`price < 100`)
- Any scenario where you want all matching results without ranking

**When to choose searching:**
- Text queries where some results are more relevant than others
- Finding documents similar to a search phrase
- Any scenario where you want the "best" matches first
- You want to use [analyzers](elasticsearch://reference/elasticsearch/mapping-reference/analyzer.md) or [synonyms](/solutions/search/full-text/search-with-synonyms.md) 

{{esql}}'s search functions address several key limitations that existed for text filtering: they work directly on multivalued fields, leverage analyzers for proper text analysis, and use optimized Lucene index structures for better performance.

### Relevance scoring [esql-for-search-scoring]

To get relevance-ranked results, you must explicitly request scoring with `METADATA _score` and sort by the score. Without this, even search functions like `MATCH` will only filter documents without ranking them.

**Without `METADATA _score`**: All operations are filtering-only, even `MATCH`, `QSTR`, and `KQL` functions. Documents either match or don't match - no ranking occurs.

**With `METADATA _score`**: [Search functions](elasticsearch://reference/query-languages/esql/functions-operators/search-functions.md) contribute to relevance scores, while filtering operations (range conditions, exact matches) don't affect scoring. You must explicitly use `SORT _score DESC` to see the most relevant results first.

This gives you full control over when to use fast filtering versus slower but more powerful relevance-based searching.

## Search functions

The following functions provide text-based search capabilities in {{esql}} with different levels of precision and control.

### `MATCH` function and operator

{{esql}} offers two syntax options for match, which replicate the functionality of [match](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md) queries in Query DSL.

- Use the compact [operator syntax (:)](elasticsearch://reference/query-languages/esql/functions-operators/operators.md#esql-match-operator) for simple text matching with default parameters.
- Use the [MATCH function syntax](elasticsearch://reference/query-languages/esql/functions-operators/search-functions.md#esql-match) for more control over the query, such as specifying analyzers, fuzziness, and other parameters.

Refer to the [tutorial](esql-search-tutorial.md#step-3-basic-search-operations) for examples of both syntaxes.

### `MATCH_PHRASE` function

Use the [`MATCH_PHRASE` function](elasticsearch://reference/query-languages/esql/functions-operators/search-functions.md#esql-match_phrase) to perform a `match_phrase` query on the specified field. This is equivalent to using the [match_phrase query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query-phrase.md) in Query DSL.

For exact phrase matching rather than individual word matching, use `MATCH_PHRASE`.

### Query string (`QSTR`) function

The [`qstr` function](elasticsearch://reference/query-languages/esql/functions-operators/search-functions.md#esql-qstr) provides the same functionality as the Query DSL's `query_string` query. This enables advanced search patterns with wildcards, boolean logic, and multi-field searches.

For complete details, refer to the [Query DSL `query_string` docs](elasticsearch://reference/query-languages/query-dsl/query-dsl-query-string-query.md).

### `KQL` function

Use the [KQL function](elasticsearch://reference/query-languages/esql/functions-operators/search-functions.md#esql-kql) to use the [Kibana Query Language](/explore-analyze/query-filter/languages/kql.md) in your {{esql}} queries.

For migrating queries from other Kibana interfaces, the `KQL` function preserves existing query syntax and allows gradual migration to {{esql}} without rewriting existing Kibana queries.

## Advanced search capabilities

### Semantic search

[Semantic search](/solutions/search/semantic-search.md) leverages machine learning models to understand the meaning of text, enabling more accurate and context-aware search results.

In {{esql}}, you can perform semantic searches on [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field types using the same match syntax as full-text search.

Refer to [semantic search with semantic_text](/solutions/search/semantic-search/semantic-search-semantic-text.md) for an example or follow the [tutorial](esql-search-tutorial.md#step-5-semantic-search-and-hybrid-search).

### Hybrid search

[Hybrid search](/solutions/search/hybrid-search.md) combines lexical and semantic search with custom weights to leverage both exact keyword matching and semantic understanding.

Refer to [hybrid search with semantic_text](hybrid-semantic-text.md) for an example or follow the [tutorial](esql-search-tutorial.md#step-5-semantic-search-and-hybrid-search).

## Next steps [esql-for-search-next-steps]

### Tutorials and how-to guides [esql-for-search-tutorials]

- [Search and filter with {{esql}}](esql-search-tutorial.md): Hands-on tutorial for getting started with search tools in {{esql}}, with concrete examples of the functionalities described in this page

### Technical reference [esql-for-search-reference]

- [Search functions](elasticsearch://reference/query-languages/esql/functions-operators/search-functions.md): Complete reference for all search functions
- [Limitations](elasticsearch://reference/query-languages/esql/limitations.md#esql-limitations-full-text-search): Current limitations for search functions in {{esql}}

### Related blog posts [esql-for-search-blogs]

- [{{esql}}, you know for Search](https://www.elastic.co/search-labs/blog/esql-introducing-scoring-semantic-search): Introducing scoring and semantic search
- [Introducing full text filtering in {{esql}}](https://www.elastic.co/search-labs/blog/filtering-in-esql-full-text-search-match-qstr): Overview of {{esql}}'s text filtering capabilities
