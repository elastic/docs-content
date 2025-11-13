---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/token-graphs.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Token graphs [token-graphs]

When a [tokenizer](anatomy-of-an-analyzer.md#analyzer-anatomy-tokenizer) converts a text into a stream of tokens, it also records the following:

* The `position` of each token in the stream
* The `positionLength`, the number of positions that a token spans

Using these, you can create a [directed acyclic graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph), called a *token graph*, for a stream. In a token graph, each position represents a node. Each token represents an edge or arc, pointing to the next position.

:::{image} /manage-data/images/elasticsearch-reference-token-graph-qbf-ex.svg
:alt: token graph qbf ex
:::

## Synonyms [token-graphs-synonyms]

Some [token filters](anatomy-of-an-analyzer.md#analyzer-anatomy-token-filters) can add new tokens, like synonyms, to an existing token stream. These synonyms often span the same positions as existing tokens.

In the following graph, `quick` and its synonym `fast` both have a position of `0`. They span the same positions.

:::{image} /manage-data/images/elasticsearch-reference-token-graph-qbf-synonym-ex.svg
:alt: token graph qbf synonym ex
:::


## Multi-position tokens [token-graphs-multi-position-tokens]

Some token filters can add tokens that span multiple positions. These can include tokens for multi-word synonyms, such as using "atm" as a synonym for "automatic teller machine".

However, only some token filters, known as *graph token filters*, accurately record the `positionLength` for multi-position tokens. These filters include:

* [`synonym_graph`](elasticsearch://reference/text-analysis/analysis-synonym-graph-tokenfilter.md)
* [`word_delimiter_graph`](elasticsearch://reference/text-analysis/analysis-word-delimiter-graph-tokenfilter.md)

Some tokenizers, such as the [`nori_tokenizer`](elasticsearch://reference/elasticsearch-plugins/analysis-nori-tokenizer.md), also accurately decompose compound tokens into multi-position tokens.

In the following graph, `domain name system` and its synonym, `dns`, both have a position of `0`. However, `dns` has a `positionLength` of `3`. Other tokens in the graph have a default `positionLength` of `1`.

:::{image} /manage-data/images/elasticsearch-reference-token-graph-dns-synonym-ex.svg
:alt: token graph dns synonym ex
:::

### Using token graphs for search [token-graphs-token-graphs-search]

[Indexing](index-search-analysis.md) ignores the `positionLength` attribute and does not support token graphs containing multi-position tokens.

However, queries, such as the [`match`](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md) or [`match_phrase`](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query-phrase.md) query, can use these graphs to generate multiple sub-queries from a single query string.

:::::{dropdown} Example
A user runs a search for the following phrase using the `match_phrase` query:

`domain name system is fragile`

During [search analysis](index-search-analysis.md), `dns`, a synonym for `domain name system`, is added to the query string’s token stream. The `dns` token has a `positionLength` of `3`.

:::{image} /manage-data/images/elasticsearch-reference-token-graph-dns-synonym-ex.svg
:alt: token graph dns synonym ex
:::

The `match_phrase` query uses this graph to generate sub-queries for the following phrases:

```text
dns is fragile
domain name system is fragile
```

This means the query matches documents containing either `dns is fragile` *or* `domain name system is fragile`.

:::::



### Invalid token graphs [token-graphs-invalid-token-graphs]

The following token filters can add tokens that span multiple positions but only record a default `positionLength` of `1`:

* [`synonym`](elasticsearch://reference/text-analysis/analysis-synonym-tokenfilter.md)
* [`word_delimiter`](elasticsearch://reference/text-analysis/analysis-word-delimiter-tokenfilter.md)

This means these filters will produce invalid token graphs for streams containing such tokens.

In the following graph, `dns` is a multi-position synonym for `domain name system`. However, `dns` has the default `positionLength` value of `1`, resulting in an invalid graph.

:::{image} /manage-data/images/elasticsearch-reference-token-graph-dns-invalid-ex.svg
:alt: token graph dns invalid ex
:::

Avoid using invalid token graphs for search. Invalid graphs can cause unexpected search results.



