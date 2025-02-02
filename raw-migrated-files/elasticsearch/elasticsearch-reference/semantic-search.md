# Semantic search [semantic-search]

Semantic search is a search method that helps you find data based on the intent and contextual meaning of a search query, instead of a match on query terms (lexical search).

{{es}} provides various semantic search capabilities using [natural language processing (NLP)](../../../explore-analyze/machine-learning/nlp.md) and vector search. Using an NLP model enables you to extract text embeddings out of text. Embeddings are vectors that provide a numeric representation of a text. Pieces of content with similar meaning have similar representations.

:::{image} ../../../images/elasticsearch-reference-semantic-options.svg
:alt: Overview of semantic search workflows in {es}
:::

You have several options for using NLP models in the {{stack}}:

* use the `semantic_text` workflow (recommended)
* use the {{infer}} API workflow
* deploy models directly in {es}

Refer to [this section](../../../solutions/search/semantic-search.md#using-nlp-models) to choose your workflow.

You can also store your own embeddings in {{es}} as vectors. Refer to [this section](../../../solutions/search/semantic-search.md#using-query) for guidance on which query type to use for semantic search.

At query time, {{es}} can use the same NLP model to convert a query into embeddings, enabling you to find documents with similar text embeddings.


## Choose a semantic search workflow [using-nlp-models]


### `semantic_text` workflow [_semantic_text_workflow]

The simplest way to use NLP models in the {{stack}} is through the [`semantic_text` workflow](../../../solutions/search/semantic-search/semantic-search-semantic-text.md). We recommend using this approach because it abstracts away a lot of manual work. All you need to do is create an {{infer}} endpoint and an index mapping to start ingesting, embedding, and querying data. There is no need to define model-related settings and parameters, or to create {{infer}} ingest pipelines. Refer to the [Create an {{infer}} endpoint API](https://www.elastic.co/guide/en/elasticsearch/reference/current/put-inference-api.html) documentation for a list of supported services.

The [Semantic search with `semantic_text`](../../../solutions/search/semantic-search/semantic-search-semantic-text.md) tutorial shows you the process end-to-end.


### {{infer}} API workflow [_infer_api_workflow]

The [{{infer}} API workflow](../../../solutions/search/inference-api.md) is more complex but offers greater control over the {{infer}} endpoint configuration. You need to create an {{infer}} endpoint, provide various model-related settings and parameters, define an index mapping, and set up an {{infer}} ingest pipeline with the appropriate settings.

The [Semantic search with the {{infer}} API](../../../solutions/search/inference-api.md) tutorial shows you the process end-to-end.


### Model deployment workflow [_model_deployment_workflow]

You can also deploy NLP in {{es}} manually, without using an {{infer}} endpoint. This is the most complex and labor intensive workflow for performing semantic search in the {{stack}}. You need to select an NLP model from the [list of supported dense and sparse vector models](../../../explore-analyze/machine-learning/nlp/ml-nlp-model-ref.md#ml-nlp-model-ref-text-embedding), deploy it using the Eland client, create an index mapping, and set up a suitable ingest pipeline to start ingesting and querying data.

The [Semantic search with a model deployed in {{es}}](../../../solutions/search/semantic-search/semantic-search-deployed-nlp-model.md) tutorial shows you the process end-to-end.


## Using the right query [using-query]

Crafting the right query is crucial for semantic search. Which query you use and which field you target in your queries depends on your chosen workflow. If you’re using the `semantic_text` workflow it’s quite simple. If not, it depends on which type of embeddings you’re working with.

| Field type to query | Query to use | Notes |
| --- | --- | --- |
| [`semantic_text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-text.html) | [`semantic`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-semantic-query.html) | The `semantic_text` field handles generating embeddings for you at index time and query time. |
| [`sparse_vector`](https://www.elastic.co/guide/en/elasticsearch/reference/current/sparse-vector.html) | [`sparse_vector`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-sparse-vector-query.html) | The `sparse_vector` query can generate query embeddings for you, but you can also provide your own. You must provide embeddings at index time. |
| [`dense_vector`](https://www.elastic.co/guide/en/elasticsearch/reference/current/dense-vector.html) | [`knn`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-knn-query.html) | The `knn` query can generate query embeddings for you, but you can also provide your own. You must provide embeddings at index time. |

If you want {{es}} to generate embeddings at both index and query time, use the `semantic_text` field and the `semantic` query. If you want to bring your own embeddings, use the `sparse_vector` or `dense_vector` field type and the associated query depending on the NLP model you used to generate the embeddings.

::::{important}
For the easiest way to perform semantic search in the {{stack}}, refer to the [`semantic_text`](../../../solutions/search/semantic-search/semantic-search-semantic-text.md) end-to-end tutorial.
::::



## Read more [semantic-search-read-more]

* Tutorials:

    * [Semantic search with `semantic_text`](../../../solutions/search/semantic-search/semantic-search-semantic-text.md)
    * [Semantic search with the {{infer}} API](../../../solutions/search/inference-api.md)
    * [Semantic search with ELSER](../../../solutions/search/vector/sparse-vector-elser.md) using the model deployment workflow
    * [Semantic search with a model deployed in {{es}}](../../../solutions/search/semantic-search/semantic-search-deployed-nlp-model.md)
    * [Semantic search with the msmarco-MiniLM-L-12-v3 sentence-transformer model](../../../explore-analyze/machine-learning/nlp/ml-nlp-text-emb-vector-search-example.md)

* Interactive examples:

    * The [`elasticsearch-labs`](https://github.com/elastic/elasticsearch-labs) repo contains a number of interactive semantic search examples in the form of executable Python notebooks, using the {{es}} Python client
    * [Semantic search with ELSER using the model deployment workflow](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/03-ELSER.ipynb)
    * [Semantic search with `semantic_text`](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/09-semantic-text.ipynb)

* Blogs:

    * [{{es}} new semantic_text mapping: Simplifying semantic search](https://www.elastic.co/search-labs/blog/semantic-search-simplified-semantic-text)
    * [Introducing Elastic Learned Sparse Encoder: Elastic’s AI model for semantic search](https://www.elastic.co/blog/may-2023-launch-sparse-encoder-ai-model)
    * [How to get the best of lexical and AI-powered search with Elastic’s vector database](https://www.elastic.co/blog/lexical-ai-powered-search-elastic-vector-database)
    * Information retrieval blog series:

        * [Part 1: Steps to improve search relevance](https://www.elastic.co/blog/improving-information-retrieval-elastic-stack-search-relevance)
        * [Part 2: Benchmarking passage retrieval](https://www.elastic.co/blog/improving-information-retrieval-elastic-stack-benchmarking-passage-retrieval)
        * [Part 3: Introducing Elastic Learned Sparse Encoder, our new retrieval model](https://www.elastic.co/blog/may-2023-launch-information-retrieval-elasticsearch-ai-model)
        * [Part 4: Hybrid retrieval](https://www.elastic.co/blog/improving-information-retrieval-elastic-stack-hybrid)









