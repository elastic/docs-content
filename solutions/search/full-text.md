---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-search.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
---

# Full-text search [full-text-search]

::::{tip}
Would you prefer to start with a hands-on example? Refer to our [full-text search tutorial](elasticsearch://reference/query-languages/query-dsl/full-text-filter-tutorial.md).
::::

Full-text search, also known as lexical search, is a technique for fast, efficient searching through text fields in documents. Documents and search queries are transformed to enable returning [relevant](https://www.elastic.co/what-is/search-relevance) results instead of simply exact term matches. Fields of type [`text`](elasticsearch://reference/elasticsearch/mapping-reference/text.md#text-field-type) are analyzed and indexed for full-text search.

Built on decades of information retrieval research, full-text search delivers reliable results that scale predictably as your data grows. Because it runs efficiently on CPUs, {{es}}'s full-text search requires minimal computational resources compared to GPU-intensive vector operations.

You can combine full-text search with [semantic search using vectors](semantic-search.md) to build modern hybrid search applications. While vector search may require additional GPU resources, the full-text component remains cost-effective by leveraging existing CPU infrastructure.

## Getting started [full-text-search-getting-started]


For a high-level overview of how full-text search works, refer to [How full-text search works](full-text/how-full-text-works.md).

For a hands-on introduction to full-text search, refer to the [full-text search tutorial](elasticsearch://reference/query-languages/query-dsl/full-text-filter-tutorial.md).


## Learn more [full-text-search-learn-more]

Here are some resources to help you learn more about full-text search with {{es}}.

**Core concepts**

Learn about the core components of full-text search:

* [Text fields](elasticsearch://reference/elasticsearch/mapping-reference/text.md)
* [Text analysis](full-text/text-analysis-during-search.md)
    * [Tokenizers](elasticsearch://reference/text-analysis/tokenizer-reference.md)
    * [Analyzers](elasticsearch://reference/text-analysis/analyzer-reference.md)


**{{es}} query languages**

Learn how to build full-text search queries using {{es}}'s query languages:

* [Full-text queries using Query DSL](elasticsearch://reference/query-languages/query-dsl/full-text-queries.md)
* [Full-text search functions in {{esql}}](elasticsearch://reference/query-languages/esql/functions-operators/search-functions.md)

**Advanced topics**

For a technical deep dive into {{es}}'s BM25 implementation read this blog post: [The BM25 Algorithm and its Variables](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables).

To learn how to optimize the relevance of your search results, refer to [Search relevance optimizations](full-text/search-relevance.md).

