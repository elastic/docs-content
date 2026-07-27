---
navigation_title: Use cases
description: Explore vector search use cases in Elasticsearch, including RAG, recommendations, image search, and hybrid retrieval.
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
# Vector search use cases

Sometimes [full-text search](../full-text.md) alone is not enough. Machine learning helps you find data by meaning, not only by matching keywords. Vector search is how Elasticsearch supports these workloads.

This page describes common vector search use cases and how to implement them.

:::{tip}
New to vector search? You might want to start with the [managed `semantic_text` workflow](../get-started/semantic-search.md).
:::

## How to implement retrieval [how-to-implement-retrieval]

Choose a search strategy based on the following:

- **Embeddings**: For meaning-based text search, start with [managed workflows](../semantic-search.md) such as [`semantic_text`](../semantic-search/semantic-search-semantic-text.md). When you need full control over models, embeddings, or non-text vectors, configure [vector search](../vector.md) directly. To understand the differences and choose the right approach, refer to [Semantic search and vector search](../vector.md#semantic-search-vs-vector-search).
- **Query interface**: Send requests with the [Search API and Query DSL](../the-search-api.md) or [{{esql}} for search](../esql-for-search.md). Use the same approach at index time and at search time.
- **Combine strategies**: To rank keyword and vector results together, use [Hybrid search](../hybrid-search.md) or [retrievers](../retrievers-overview.md) in a single Search API request.

## RAG and question answering on your own data

Use Elasticsearch to find relevant passages in your documents, wikis, tickets, or knowledge bases, then pass those passages to a language model. The model can answer using your data instead of only its training data. This fits internal assistants, support bots, and tools that must cite sources.

::::::{stepper}
:::::{step} Learn how RAG works in Elasticsearch

Read how retrieval, chunking, and orchestration fit together.

- [RAG](../rag.md)

:::::

:::::{step} Set up search for your documents

Split long documents into smaller chunks so each search result is a useful passage. Refer to [How to implement retrieval](#how-to-implement-retrieval) to choose your embedding approach, query interface, and search strategy.

:::::

:::::{step} Generate answers with an LLM

Send the top search hits and their text fields to your model or orchestration layer.

- [Core search options in RAG](../rag.md#core-search-options)

:::::
::::::

## Discovery and recommendations

Find related products, articles, videos, or other items when keywords alone do not match well. Examples include "similar products," "you might also like," and matching users or players in an app.

::::::{stepper}
:::::{step} Store embeddings for each item

Each item needs a vector from the same model so similarity scores are comparable. Refer to [How to implement retrieval](#how-to-implement-retrieval) for your embedding approach.

:::::

:::::{step} Search for similar items

Use the vector of the current item (or a user profile vector) as the search input. Run a k-nearest neighbor (kNN) query to get the closest matches. On large catalogs, adjust `k` and `num_candidates` to balance speed and quality. Refer to [How to implement retrieval](#how-to-implement-retrieval) for your query interface and search strategy.

- [kNN search](knn.md)

:::::

:::::{step} Limit results with filters

A **filter** is a rule on structured fields in your index, such as "in stock," "region = EU," or "category = shoes." It narrows which documents kNN considers. Without filters, similarity search might return items the user cannot buy or see.

Add a `filter` clause to your kNN request so only matching documents are returned. This is important for catalogs where most items are out of scope for a given user.

- [Filtered kNN search](knn.md#knn-search-filter-example)

:::::

:::::{step} Improve the result order

The closest vectors are not always the best final ranking. You can boost by popularity or recency, or rescore the top results. Refer to [How to implement retrieval](#how-to-implement-retrieval) for how to combine search strategies.

- [Semantic reranking](../ranking/semantic-reranking.md)

:::::
::::::

## Multimodal search

Search images, audio, video, or text when your content uses more than one type. For example, search with text to find images, or search with an image to find similar images.

The following steps use the [Inference API](../semantic-search/semantic-search-inference.md) to embed multimodal content. Refer to [How to implement retrieval](#how-to-implement-retrieval) for other embedding approaches.

::::::{stepper}
:::::{step} Create an inference endpoint

Create an endpoint with a model that supports your media types (text, images, audio, or video). Use the `embedding` task type for multimodal models. Use the same endpoint ID when you ingest documents and when you run a search.

- [Create an inference endpoint](../semantic-search/semantic-search-inference.md#infer-text-embedding-task)

:::::

:::::{step} Add an index mapping and ingest pipeline

Define a `dense_vector` field for embeddings and any other fields you need for filters (category, license, date). In the same tutorial, add an ingest pipeline with an inference processor that calls your endpoint, then load your documents so each one is embedded at index time.

- [Create the index mapping](../semantic-search/semantic-search-inference.md#infer-service-mappings)

:::::

:::::{step} Run kNN search

Use kNN with a `query_vector_builder` so Elasticsearch embeds the user's query with the same model, then returns the closest vectors. Add a filter on structured fields when you need to limit results by category or other rules. Refer to [How to implement retrieval](#how-to-implement-retrieval) for your query interface and search strategy.

- [Semantic search with the Inference API](../semantic-search/semantic-search-inference.md#infer-semantic-search)

:::::
::::::

## Duplicate detection, fraud, and anomaly detection

Compare documents, accounts, or events to find near-duplicates, suspicious matches, or unusual patterns that exact matching would miss. Examples include duplicate articles, fraudulent transactions, and operational outliers.

::::::{stepper}
:::::{step} Clean records before embedding

Use an [ingest pipeline](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md) to normalize the fields you embed before they are indexed. The goal is to avoid separate vectors for content that only differs in formatting.

:::::

:::::{step} Store one vector per record you compare

Index one embedding per document, account snapshot, or time window you want to compare. Refer to [How to implement retrieval](#how-to-implement-retrieval) for your embedding approach.

:::::

:::::{step} Find neighbors and apply thresholds

Run kNN for each new or suspect record. In your application, use the similarity score to decide what to do: mark pairs above a threshold as duplicates, block submissions close to a known fraud example, or raise an alert when neighbors look unusual. Refer to [How to implement retrieval](#how-to-implement-retrieval) for your query interface and search strategy.

- [kNN search](knn.md)

:::::

:::::{step} Act on matches in your pipeline

Run scheduled checks on new data, write matches to a review index, or combine vector results with aggregations (for example, count duplicates per URL). For time-series patterns that are not vector-based, you can also use [anomaly detection in Elasticsearch](/explore-analyze/machine-learning/anomaly-detection.md).

:::::
::::::

## Long-term memory for LLMs

Store facts, chat turns, or summaries so an assistant can load relevant past context without sending the full chat history every time.

::::::{stepper}
:::::{step} Design the memory index

Store a user or session ID, a timestamp, and optional expiry fields. Decide whether each stored item is a full message, a short fact, or a summary so search returns the right level of detail.

- [Index basics](../get-started/index-basics.md)

:::::

:::::{step} Index new memories with embeddings

Use the same embedding setup at index time and at search time. Refer to [How to implement retrieval](#how-to-implement-retrieval) for your embedding approach.

:::::

:::::{step} Retrieve memories for each new message

Restrict search to the current user or session, then run semantic or kNN search on the new message. Pass the top hits to your application with the user's latest input. Refer to [How to implement retrieval](#how-to-implement-retrieval) for your query interface and search strategy.

:::::

:::::{step} Remove or merge old memories

Delete or roll up outdated entries in your app, or use [index lifecycle management](../../../manage-data/lifecycle/index-lifecycle-management.md) so the index stays accurate and does not grow without limit.

:::::
::::::
