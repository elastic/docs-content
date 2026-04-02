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
# AI-powered search

Natural language understanding and information retrieval go hand in hand in modern search systems. Sometimes [full-text search](../full-text.md) alone isn't enough. Machine learning techniques are powerful tools for helping users find data based on intent and contextual meaning.

Depending on your team's technical expertise and requirements, you can choose from two main paths to implement AI-powered search in Elasticsearch. You can use managed workflows that abstract away much of the complexity, or you can work directly with the underlying vector search technology.

## Use cases

AI-powered search enables a wide range of applications:
- Natural language search
- Retrieval Augmented Generation (RAG)
- Question answering systems
- Content recommendation engines
- Information retrieval from large datasets
- Product discovery in e-commerce
- Workplace document search
- Similar item matching

## Overview

AI-powered search in Elasticsearch is built on vector search technology, which uses machine learning models to capture meaning in content. These vector representations come in two forms: dense vectors that capture overall meaning, and sparse vectors that focus on key terms and their relationships.

:::{tip}
New to AI-powered search? Start with the `semantic_text` workflow, which provides an easy-to-use abstraction over these capabilities with sensible defaults. Learn more [in this hands-on tutorial](../semantic-search/semantic-search-semantic-text.md).
:::

## Implementation paths

Elasticsearch uses vector search as the foundation for AI-powered search capabilities. You can work with this technology in two ways:

1. [**Semantic search**](../semantic-search.md) provides managed workflows that use vector search under the hood:
   - The `semantic_text` field type offers the simplest path with automatic embedding generation and model management
   - Additional implementation options available for more complex needs

2. [**Vector search**](../vector.md) gives you direct access to the underlying technology:
   - Manual configuration of dense or sparse vectors
   - Flexibility to bring your own embeddings
   - Direct implementation of vector similarity matching

Once you've implemented either approach, you can combine it with full-text search to create [hybrid search](../hybrid-search.md) solutions that leverage both meaning-based and keyword-based matching.