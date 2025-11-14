---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-search.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-reference-semantic-search.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Semantic search [semantic-search]

:::{note}
This page focuses on the semantic search workflows available in {{es}}. For detailed information about lower-level vector search implementations, refer to [vector search](vector.md).
:::

{{es}} provides various semantic search capabilities using [natural language processing (NLP)](/explore-analyze/machine-learning/nlp.md) and [vector search](vector.md).

To understand the infrastructure that powers semantic search and other NLP tasks, including managed services and inference endpoints, see the [Elastic Inference overview](../../explore-analyze/elastic-inference.md) page.

Learn more about use cases for AI-powered search in the [overview](ai-search/ai-search.md) page.

## Overview of semantic search workflows [semantic-search-workflows-overview]

You have several options for using NLP models for semantic search in the {{stack}}:

* [Option 1](#_semantic_text_workflow): Use the `semantic_text` workflow (recommended)
* [Option 2](#_infer_api_workflow): Use the {{infer}} API workflow
* [Option 3](#_model_deployment_workflow): Deploy models directly in {{es}}

This diagram summarizes the relative complexity of each workflow:

:::{image} /solutions/images/elasticsearch-reference-semantic-options.svg
:alt: Overview of semantic search workflows in {{es}}
:::

## Choose a semantic search workflow [using-nlp-models]

### Option 1: `semantic_text` [_semantic_text_workflow]

The simplest way to use NLP models in the {{stack}} is through the [`semantic_text` workflow](semantic-search/semantic-search-semantic-text.md). We recommend using this approach because it abstracts away a lot of manual work. All you need to do is create an index mapping to start ingesting, embedding, and querying data. There is no need to define model-related settings and parameters, or to create {{infer}} ingest pipelines. For guidance on the available query types for `semantic_text`, see [Querying `semantic_text` fields](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md#querying-semantic-text-fields).

To learn more about supported services, refer to [](/explore-analyze/elastic-inference/inference-api.md) and the [{{infer}} API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) documentation. For an end-to-end tutorial, refer to [Semantic search with `semantic_text`](semantic-search/semantic-search-semantic-text.md).

### Option 2: Inference API [_infer_api_workflow]

The {{infer}} API workflow is more complex but offers greater control over the {{infer}} endpoint configuration. You need to create an {{infer}} endpoint, provide various model-related settings and parameters, and define an index mapping. Optionally you can also set up an {{infer}} ingest pipeline for automatic embedding during data ingestion, or alternatively, you can manually call the {{infer}} API.

For an end-to-end tutorial, refer to [Semantic search with the {{infer}} API](semantic-search/semantic-search-inference.md).

### Option 3: Manual model deployment [_model_deployment_workflow]

You can also deploy NLP in {{es}} manually, without using an {{infer}} endpoint. This is the most complex and labor intensive workflow for performing semantic search in the {{stack}}. You need to select an NLP model from the [list of supported dense and sparse vector models](../../explore-analyze/machine-learning/nlp/ml-nlp-model-ref.md#ml-nlp-model-ref-text-embedding), deploy it using the Eland client, create an index mapping, and set up a suitable ingest pipeline to start ingesting and querying data.

For an end-to-end tutorial, refer to [Semantic search with a model deployed in {{es}}](vector/dense-versus-sparse-ingest-pipelines.md).

::::{tip}
Refer to [vector queries and field types](vector.md#vector-queries-and-field-types) for a quick reference overview.
::::

## Learn more [semantic-search-read-more]

### Interactive examples

- The [`elasticsearch-labs`](https://github.com/elastic/elasticsearch-labs) repo contains a number of interactive semantic search examples in the form of executable Python notebooks, using the {{es}} Python client
- [Semantic search with ELSER using the model deployment workflow](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/03-ELSER.ipynb)
- [Semantic search with `semantic_text`](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/09-semantic-text.ipynb)

### Blogs

- [{{es}} new semantic_text mapping: Simplifying semantic search](https://www.elastic.co/search-labs/blog/semantic-search-simplified-semantic-text)
- [GA information for `semantic_text`](https://www.elastic.co/search-labs/blog/semantic-text-ga)
- [Introducing ELSER: Elastic's AI model for semantic search](https://www.elastic.co/blog/may-2023-launch-sparse-encoder-ai-model)
- [How to get the best of lexical and AI-powered search with Elastic's vector database](https://www.elastic.co/blog/lexical-ai-powered-search-elastic-vector-database)
- Information retrieval blog series:
    - [Part 1: Steps to improve search relevance](https://www.elastic.co/blog/improving-information-retrieval-elastic-stack-search-relevance)
    - [Part 2: Benchmarking passage retrieval](https://www.elastic.co/blog/improving-information-retrieval-elastic-stack-benchmarking-passage-retrieval)
    - [Part 3: Introducing Elastic Learned Sparse Encoder, our new retrieval model](https://www.elastic.co/blog/may-2023-launch-information-retrieval-elasticsearch-ai-model)
    - [Part 4: Hybrid retrieval](https://www.elastic.co/blog/improving-information-retrieval-elastic-stack-hybrid)