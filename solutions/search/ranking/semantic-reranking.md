---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-reranking.html
applies_to:
  stack:
  serverless:
---

# Semantic reranking [semantic-reranking]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


::::{tip}
This overview focuses more on the high-level concepts and use cases for semantic re-ranking. For full implementation details on how to set up and use semantic re-ranking in {{es}}, see the [reference documentation](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-retriever) in the Search API docs.

::::


Re-rankers improve the relevance of results from earlier-stage retrieval mechanisms. *Semantic* re-rankers use machine learning models to reorder search results based on their semantic similarity to a query.

Semantic re-ranking requires relatively large and complex machine learning models and operates in real-time in response to queries. This technique makes sense on a small *top-k* result set, as one the of the final steps in a pipeline. This is a powerful technique for improving search relevance that works equally well with keyword, semantic, or hybrid retrieval algorithms.

The next sections provide more details on the benefits, use cases, and model types used for semantic re-ranking. The final sections include a practical, high-level overview of how to implement [semantic re-ranking in {{es}}](#semantic-reranking-in-es) and links to the full reference documentation.


## Use cases [semantic-reranking-use-cases]

Semantic re-ranking enables a variety of use cases:

* **Lexical (BM25) retrieval results re-ranking**

    * Out-of-the-box semantic search by adding a simple API call to any lexical/BM25 retrieval pipeline.
    * Adds semantic search capabilities on top of existing indices without reindexing, perfect for quick improvements.
    * Ideal for environments with complex existing indices.

* **Semantic retrieval results re-ranking**

    * Improves results from semantic retrievers using ELSER sparse vector embeddings or dense vector embeddings by using more powerful models.
    * Adds a refinement layer on top of hybrid retrieval with [reciprocal rank fusion (RRF)](elasticsearch://reference/elasticsearch/rest-apis/reciprocal-rank-fusion.md).

* **General applications**

    * Supports automatic and transparent chunking, eliminating the need for pre-chunking at index time.
    * Provides explicit control over document relevance in retrieval-augmented generation (RAG) uses cases or other scenarios involving language model (LLM) inputs.


Now that we’ve outlined the value of semantic re-ranking, we’ll explore the specific models that power this process and how they differ.


## Cross-encoder and bi-encoder models [semantic-reranking-models]

At a high level, two model types are used for semantic re-ranking: cross-encoders and bi-encoders.

::::{note}
In this version, {{es}} **only supports cross-encoders** for semantic re-ranking.
::::


* A **cross-encoder model** can be thought of as a more powerful, all-in-one solution, because it generates query-aware document representations. It takes the query and document texts as a single, concatenated input.
* A **bi-encoder model** takes as input either document or query text. Documents and query embeddings are computed separately, so they aren’t aware of each other.

    * To compute a ranking score, an external operation is required. This typically involves computing dot-product or cosine similarity between the query and document embeddings.


In brief, cross-encoders provide high accuracy but are more resource-intensive. Bi-encoders are faster and more cost-effective but less precise.

In future versions, {{es}} will also support bi-encoders. If you’re interested in a more detailed analysis of the practical differences between cross-encoders and bi-encoders, untoggle the next section.

::::{dropdown} Comparisons between cross-encoder and bi-encoder
The following is a non-exhaustive list of considerations when choosing between cross-encoders and bi-encoders for semantic re-ranking:

* Because a cross-encoder model simultaneously processes both query and document texts, it can better infer their relevance, making it more effective as a reranker than a bi-encoder.
* Cross-encoder models are generally larger and more computationally intensive, resulting in higher latencies and increased computational costs.
* There are significantly fewer open-source cross-encoders, while bi-encoders offer a wide variety of sizes, languages, and other trade-offs.
* The effectiveness of cross-encoders can also improve the relevance of semantic retrievers. For example, their ability to take word order into account can improve on dense or sparse embedding retrieval.
* When trained in tandem with specific retrievers (like lexical/BM25), cross-encoders can “correct” typical errors made by those retrievers.
* Cross-encoders output scores that are consistent across queries. This enables you to maintain high relevance in result sets, by setting a minimum score threshold for all queries. For example, this is important when using results in a RAG workflow or if you’re otherwise feeding results to LLMs. Note that similarity scores from bi-encoders/embedding similarities are *query-dependent*, meaning you cannot set universal cut-offs.
* Bi-encoders rerank using embeddings. You can improve your re-ranking latency by creating embeddings at ingest-time. These embeddings can be stored for re-ranking without being indexed for retrieval, reducing your memory footprint.

::::



## Semantic re-ranking in {{es}} [semantic-reranking-in-es]

In {{es}}, semantic re-rankers are implemented using the {{es}} [Inference API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference) and a [retriever](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-retriever).

To use semantic re-ranking in {{es}}, you need to:

1. **Select and configure a re-ranking model**. You have the following options:

    1. Use the [Elastic Rerank](../../../explore-analyze/elastic-inference/inference-api/elasticsearch-inference-integration.md#inference-example-elastic-reranker) cross-encoder model via the inference API’s {{es}} service.
    2. Use the [Cohere Rerank inference endpoint](../../../explore-analyze/elastic-inference/inference-api/cohere-inference-integration.md) to create a `rerank` endpoint.
    3. Use the [Google Vertex AI inference endpoint](../../../explore-analyze/elastic-inference/inference-api/google-vertex-ai-inference-integration.md) to create a `rerank` endpoint.
    4. Upload a model to {{es}} from Hugging Face with [Eland](eland://reference/machine-learning.md#ml-nlp-pytorch). You’ll need to use the `text_similarity` NLP task type when loading the model using Eland. Then set up an [{{es}} service inference endpoint](../../../explore-analyze/elastic-inference/inference-api/elasticsearch-inference-integration.md#inference-example-eland) with the `rerank` endpoint type.

        Refer to [the Elastic NLP model reference](../../../explore-analyze/machine-learning/nlp/ml-nlp-model-ref.md#ml-nlp-model-ref-text-similarity) for a list of third party text similarity models supported by {{es}} for semantic re-ranking.

2. **Create a `rerank` endpoint using the [{{es}} Inference API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put)**. The Inference API creates an inference endpoint and configures your chosen machine learning model to perform the re-ranking task.
3. **Define a `text_similarity_reranker` retriever in your search request**. The retriever syntax makes it simple to configure both the retrieval and re-ranking of search results in a single API call.

::::{dropdown} Example search request with semantic reranker
The following example shows a search request that uses a semantic reranker to reorder the top-k documents based on their semantic similarity to the query.

```console
POST _search
{
  "retriever": {
    "text_similarity_reranker": {
      "retriever": {
        "standard": {
          "query": {
            "match": {
              "text": "How often does the moon hide the sun?"
            }
          }
        }
      },
      "field": "text",
      "inference_id": "elastic-rerank",
      "inference_text": "How often does the moon hide the sun?",
      "rank_window_size": 100,
      "min_score": 0.5
    }
  }
}
```
%  TEST[skip:TBD]

::::



## Learn more [semantic-reranking-learn-more]

* Read the [retriever reference documentation](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search#operation-search-body-application-json-retriever) for syntax and implementation details
* Learn more about the [retrievers](../querying-for-search.md) abstraction
* Learn more about the Elastic [Inference APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference)
* Check out our [Python notebook](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/integrations/cohere/cohere-elasticsearch.ipynb) for using Cohere with {{es}}

