---
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---
# How full-text search works [full-text-search-how-it-works]

The following diagram illustrates the components of full-text search.

:::{image} /solutions/images/elasticsearch-reference-full-text-search-overview.svg
:alt: Components of full-text search from analysis to relevance scoring
:width: 550px
:::

At a high level, full-text search involves the following:

* [**Text analysis**](../../../manage-data/data-store/text-analysis.md): Analysis consists of a pipeline of sequential transformations. Text is transformed into a format optimized for searching using techniques such as stemming, lowercasing, and stop word elimination. {{es}} contains a number of built-in [analyzers](elasticsearch://reference/text-analysis/analyzer-reference.md) and tokenizers, including options to analyze specific language text. You can also create custom analyzers.
::::{tip}
Refer to [Test an analyzer](../../../manage-data/data-store/text-analysis/test-an-analyzer.md) to learn how to test an analyzer and inspect the tokens and metadata it generates.
::::

* **Inverted index creation**: After analysis is complete, {{es}} builds an inverted index from the resulting tokens. An inverted index is a data structure that maps each token to the documents that contain it. It’s made up of two key components:

    * **Dictionary**: A sorted list of all unique terms in the collection of documents in your index.
    * **Posting list**: For each term, a list of document IDs where the term appears, along with optional metadata like term frequency and position.

* **Relevance scoring**: Results are ranked by how relevant they are to the given query. The relevance score of each document is represented by a positive floating-point number called the `_score`. The higher the `_score`, the more relevant the document.

    The default [similarity algorithm](elasticsearch://reference/elasticsearch/index-settings/similarity.md) {{es}} uses for calculating relevance scores is [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25), a variation of the [TF-IDF algorithm](https://en.wikipedia.org/wiki/Tf–idf). BM25 calculates relevance scores based on term frequency, document frequency, and document length. Refer to this [technical blog post](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables) for a deep dive into BM25.

* **Full-text search query**: Query text is analyzed [the same way as the indexed text](../../../manage-data/data-store/text-analysis/index-search-analysis.md), and the resulting tokens are used to search the inverted index.

    Query DSL supports a number of [full-text queries](elasticsearch://reference/query-languages/query-dsl/full-text-queries.md).

    As of 8.17, {{esql}} also supports [full-text search](elasticsearch://reference/query-languages/esql/functions-operators/search-functions.md) functions.
