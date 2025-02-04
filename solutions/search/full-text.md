---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-search.html
---

# Full-text search [full-text-search]

::::{admonition} Hands-on introduction to full-text search
:class: tip

Would you prefer to jump straight into a hands-on tutorial? Refer to our quick start [full-text search tutorial](get-started.md).

::::

Full-text search, also known as lexical search, is a technique for fast, efficient searching through text fields in documents. Documents and search queries are transformed to enable returning [relevant](https://www.elastic.co/what-is/search-relevance) results instead of simply exact term matches. Fields of type [`text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html#text-field-type) are analyzed and indexed for full-text search.

Built on decades of information retrieval research, full-text search delivers reliable results that scale predictably as your data grows. Because it runs efficiently on CPUs, {{es}}'s full-text search requires minimal computational resources compared to GPU-intensive vector operations.

You can combine full-text search with [semantic search using vectors](semantic-search.md) to build modern hybrid search applications. While vector search may require additional GPU resources, the full-text component remains cost-effective by leveraging existing CPU infrastructure.


## How full-text search works [full-text-search-how-it-works]

The following diagram illustrates the components of full-text search.

:::{image} ../../images/elasticsearch-reference-full-text-search-overview.svg
:alt: Components of full-text search from analysis to relevance scoring
:::

At a high level, full-text search involves the following:

* [**Text analysis**](../../manage-data/data-store/text-analysis.md): Analysis consists of a pipeline of sequential transformations. Text is transformed into a format optimized for searching using techniques such as stemming, lowercasing, and stop word elimination. {{es}} contains a number of built-in [analyzers](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html) and tokenizers, including options to analyze specific language text. You can also create custom analyzers.

    ::::{tip}
    Refer to [Test an analyzer](../../manage-data/data-store/text-analysis/test-an-analyzer.md) to learn how to test an analyzer and inspect the tokens and metadata it generates.

    ::::

* **Inverted index creation**: After analysis is complete, {{es}} builds an inverted index from the resulting tokens. An inverted index is a data structure that maps each token to the documents that contain it. It’s made up of two key components:

    * **Dictionary**: A sorted list of all unique terms in the collection of documents in your index.
    * **Posting list**: For each term, a list of document IDs where the term appears, along with optional metadata like term frequency and position.

* **Relevance scoring**: Results are ranked by how relevant they are to the given query. The relevance score of each document is represented by a positive floating-point number called the `_score`. The higher the `_score`, the more relevant the document.

    The default [similarity algorithm](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-similarity.html) {{es}} uses for calculating relevance scores is [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25), a variation of the [TF-IDF algorithm](https://en.wikipedia.org/wiki/Tf–idf). BM25 calculates relevance scores based on term frequency, document frequency, and document length. Refer to this [technical blog post](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables) for a deep dive into BM25.

* **Full-text search query**: Query text is analyzed [the same way as the indexed text](../../manage-data/data-store/text-analysis/index-search-analysis.md), and the resulting tokens are used to search the inverted index.

    Query DSL supports a number of [full-text queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html).

    As of 8.17, {{esql}} also supports [full-text search](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-functions-operators.html#esql-search-functions) functions.



## Getting started [full-text-search-getting-started]

For a hands-on introduction to full-text search, refer to the [full-text search tutorial](get-started.md).


## Learn more [full-text-search-learn-more]

Here are some resources to help you learn more about full-text search with {{es}}.

**Core concepts**

Learn about the core components of full-text search:

* [Text fields](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html)
* [Text analysis](full-text/text-analysis-during-search.md)
    * [Tokenizers](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.html)
    * [Analyzers](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html)


**{{es}} query languages**

Learn how to build full-text search queries using {{es}}'s query languages:

* [Full-text queries using Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html)
* [Full-text search functions in {{esql}}](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-functions-operators.html#esql-search-functions)

**Advanced topics**

For a technical deep dive into {{es}}'s BM25 implementation read this blog post: [The BM25 Algorithm and its Variables](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables).

To learn how to optimize the relevance of your search results, refer to [Search relevance optimizations](examples.md).

