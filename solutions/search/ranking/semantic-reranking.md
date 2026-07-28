---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/semantic-reranking.html
applies_to:
  stack: ga 9.0
  serverless:
products:
  - id: elasticsearch
---

# Semantic reranking [semantic-reranking]


::::{tip}
This overview focuses more on the high-level concepts and use cases for semantic re-ranking. For full implementation details on how to set up and use semantic re-ranking in {{es}}, see the [reference documentation]({{es-apis}}operation/operation-search#operation-search-body-application-json-retriever) in the Search API docs.

::::


Re-rankers improve the relevance of results from earlier-stage retrieval mechanisms. *Semantic* re-rankers use machine learning models to reorder search results based on their semantic similarity to a query.

Semantic re-ranking requires relatively large and complex machine learning models and operates in real-time in response to queries. This technique makes sense on a small *top-k* result set, as one of the final steps in a pipeline. This is a powerful technique for improving search relevance that works equally well with keyword, semantic, or hybrid retrieval algorithms.

The next sections provide more details on the benefits, use cases, and model types used for semantic re-ranking. The final sections include a practical, high-level overview of how to implement [semantic re-ranking in {{es}}](#semantic-reranking-in-es) and links to the full reference documentation.


## Use cases [semantic-reranking-use-cases]

Semantic re-ranking enables a variety of use cases:

* **Lexical (BM25) retrieval results re-ranking**

    * Out-of-the-box semantic search by adding a simple API call to any lexical/BM25 retrieval pipeline.
    * Adds semantic search capabilities on top of existing indices without reindexing, perfect for quick improvements.
    * Ideal for environments with complex existing indices.

* **Semantic retrieval results re-ranking**

    * Improves results from semantic retrievers using ELSER sparse vector embeddings or dense vector embeddings by using more powerful models.
    * Adds a refinement layer on top of hybrid retrieval with [reciprocal rank fusion (RRF)](elasticsearch://reference/elasticsearch/rest-apis/reciprocal-rank-fusion.md) or linear combination using the [linear retriever](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/retrievers/linear-retriever)

* **General applications**

    * Provides explicit control over document relevance in retrieval-augmented generation (RAG) use cases or other scenarios involving language model (LLM) inputs.


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

{{es}} provides two ways to add semantic re-ranking to your search pipeline:
-  Using the [`text_similarity_reranker` retriever](#use-the-text_similarity_reranker-retriever)
-  Using the {{esql}} [`RERANK` command](#use-the-esql-rerank-command)

Both use the same underlying inference endpoints and re-ranking models.

### Step 1: Configure a re-ranking model

Both approaches require an inference endpoint configured for the `rerank` task. You have the following options:

1. Use the preconfigured `.jina-reranker-v3` endpoint, powered by the [Elastic Inference Service (EIS)](/explore-analyze/elastic-inference/eis.md). This is the recommended option. Learn more about [Jina reranker models](/explore-analyze/machine-learning/nlp/ml-nlp-jina.md#jina-rerankers).
2. Use the Elastic Rerank cross-encoder model through a preconfigured `.rerank-v1-elasticsearch` endpoint or create a custom one using the [{{infer}} API’s {{es}} service]({{es-apis}}operation/operation-inference-put-elasticsearch).
3. Use the [Jina AI Rerank {{infer}} endpoint]({{es-apis}}operation/operation-inference-put-jinaai) to create a `rerank` endpoint.
4. Use the [Cohere Rerank {{infer}} endpoint]({{es-apis}}operation/operation-inference-put-cohere) to create a `rerank` endpoint.
5. Use the [Google Vertex AI inference endpoint]({{es-apis}}operation/operation-inference-put-googlevertexai) to create a `rerank` endpoint.
6. Upload a model to {{es}} from Hugging Face with [Eland](eland://reference/machine-learning.md#ml-nlp-pytorch). You’ll need to use the `text_similarity` NLP task type when loading the model using Eland. Then set up an [{{es}} service inference endpoint]({{es-apis}}operation/operation-inference-put-elasticsearch) with the `rerank` endpoint type.

    Refer to [the Elastic NLP model reference](../../../explore-analyze/machine-learning/nlp/ml-nlp-model-ref.md#ml-nlp-model-ref-text-similarity) for a list of third party text similarity models supported by {{es}} for semantic re-ranking.

### Step 2: Choose an implementation approach

You can perform semantic re-ranking using either retrievers or {{esql}}.

#### Use the `text_similarity_reranker` retriever

Use the [retriever syntax](../retrievers-overview.md) to compose multi-stage retrieval pipelines declaratively within a single `_search` call. This is a good fit when you want to combine re-ranking with other retriever stages like [RRF](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md#rrf-retriever), [linear](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md#linear-retriever), or [pinned](elasticsearch://reference/elasticsearch/rest-apis/retrievers.md#pinned-retriever).

You can use a preconfigured rerank endpoint (such as `.jina-reranker-v3` or `.rerank-v1-elasticsearch`) or create a custom one using the [{{es}} Inference API]({{es-apis}}operation/operation-inference-put). Then define a `text_similarity_reranker` retriever in your search request.

::::{dropdown} Example: Retriever-based semantic reranking
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
::::

For full reference documentation, refer to the [`text_similarity_reranker` retriever](elasticsearch://reference/elasticsearch/rest-apis/retrievers/text-similarity-reranker-retriever.md).

#### Use the {{esql}} `RERANK` command

Use the {{esql}} [`RERANK` command](elasticsearch://reference/query-languages/esql/commands/rerank.md) to add re-ranking as a step in a piped query. This is a good fit when you want to combine re-ranking with other [{{esql}}](elasticsearch://reference/query-languages/esql.md) capabilities like transformations, aggregations, or text generation with `COMPLETION`.

::::{dropdown} Example: ES|QL-based semantic reranking
```esql
FROM books
| WHERE title : "search query"
| SORT _score DESC
| LIMIT 100
| RERANK "search query" ON title
```
::::

For full reference documentation, refer to the [`RERANK` command](elasticsearch://reference/query-languages/esql/commands/rerank.md).

#### When to use which

| | Retrievers | ES\|QL |
|---|---|---|
| **Syntax** | Declarative JSON (retriever tree) | Piped query language |
| **Composability** | Nest with other retrievers (RRF, linear, pinned, diversify) | Pipe with other commands (FORK, FUSE, COMPLETION, STATS) |
| **Multi-field reranking** | Single field only | Multiple fields supported |
| **Best for** | Multi-stage retrieval pipelines in the `_search` API | End-to-end search queries that include transformations or generation |
| **Client support** | All {{es}} clients | All {{es}} clients |

### Handling long documents

A limitation of many cross-encoder models is that they do not perform well when used on corpora with long documents.
This is because many models truncate input to the length of their token window, which can potentially cut off the most relevant part of the document before it is sent to the reranker. The preconfigured `.rerank-v1-elasticsearch` endpoint truncates in this manner.

The `chunk_rescorer` in the `text_similarity_reranker` retriever allows explicit control over how much content is sent to the reranker. This addresses the long document problem and also allows control of inference costs by sending fewer tokens into the reranker.

::::{warning}
Reranking on scored chunks is an expert feature that can negatively impact relevance if used with models that don’t perform truncation.
::::

::::{dropdown} Example search request with semantic reranker using chunk rescoring
The following example shows the semantic reranker using the `chunk_rescorer` to control chunk sizes using default settings.

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
      "chunk_rescorer": {},
      "rank_window_size": 100,
      "min_score": 0.5
    }
  }
}
```
::::

## Learn more [semantic-reranking-learn-more]

* Read the [`text_similarity_reranker` retriever reference](elasticsearch://reference/elasticsearch/rest-apis/retrievers/text-similarity-reranker-retriever.md) for syntax and implementation details
* Read the [ES|QL `RERANK` command reference](elasticsearch://reference/query-languages/esql/commands/rerank.md) for the piped query approach
* Learn more about the [retrievers](../retrievers-overview.md) abstraction
* Learn more about choosing a [query interface](../querying-for-search.md) for your search use case
* Learn more about the Elastic [Inference APIs]({{es-apis}}group/endpoint-inference)
* Check out our [Python notebook](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/integrations/cohere/cohere-elasticsearch.ipynb) for using Cohere with {{es}}
