# Semantic search [elasticsearch-reference-semantic-search]

Semantic search is a search method that helps you find data based on the intent and contextual meaning of a search query, instead of a match on query terms (lexical search).

Elasticsearch provides various semantic search capabilities using natural language processing (NLP) and vector search. Using an NLP model enables you to extract text embeddings out of text. Embeddings are vectors that provide a numeric representation of a text. Pieces of content with similar meaning have similar representations.

There are three main workflows for implementing semantic search with {{es}}, arranged in order of increasing complexity:

* [The `semantic text` workflow](../../../solutions/search/semantic-search.md#elasticsearch-reference-semantic-search-semantic-text)
* [Inference API workflow](../../../solutions/search/semantic-search.md#elasticsearch-reference-semantic-search-inference-api)
* [Model deployment workflow](../../../solutions/search/semantic-search.md#elasticsearch-reference-semantic-search-model-deployment)

:::{image} ../../../images/serverless-semantic-options.svg
:alt: Overview of semantic search workflows in {es}
:::

::::{note}
Semantic search is available on all Elastic deployment types: self-managed clusters, Elastic Cloud Hosted deployments, and {{es-serverless}} projects. The links on this page will take you to the [{{es}} core documentation](../../../solutions/search/semantic-search.md).

::::



## Semantic search with `semantic text` [elasticsearch-reference-semantic-search-semantic-text]

The `semantic_text` field simplifies semantic search by providing inference at ingestion time with sensible default values, eliminating the need for complex configurations.

Learn how to implement semantic search with `semantic text` in the [Elasticsearch docs →](../../../solutions/search/semantic-search/semantic-search-semantic-text.md).


## Semantic search with the inference API [elasticsearch-reference-semantic-search-inference-api]

The inference API workflow enables you to perform semantic search using models from a variety of services, such as Cohere, OpenAI, HuggingFace, Azure AI Studio, and more.

Learn how to implement semantic search with the inference API in the [Elasticsearch docs →](../../../solutions/search/inference-api.md).


## Semantic search with the model deployment workflow [elasticsearch-reference-semantic-search-model-deployment]

The model deployment workflow enables you to deploy custom NLP models in Elasticsearch, giving you full control over text embedding generation and vector search. While this workflow offers advanced flexibility, it requires expertise in NLP and machine learning.

Learn how to implement semantic search with the model deployment workflow in the [Elasticsearch docs →](../../../solutions/search/semantic-search/semantic-search-deployed-nlp-model.md).

