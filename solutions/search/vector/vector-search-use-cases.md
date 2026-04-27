---
navigation_title: Use cases
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

:::{tip}
New to vector search? Start with this [vector search quick start](../get-started/semantic-search.md).

To understand core vector search concepts in {{es}}, including embeddings, field types, retrieval methods, and available workflows, refer to [Vector search in {{es}}](../vector.md#vectors-and-embeddings).
:::

Sometimes [full-text search](../full-text.md) alone isn't enough. {{ml-cap}} techniques help you find data based on intent and contextual meaning, not just keywords. Vector search is the foundation for these capabilities in {{es}}.

This page introduces common vector search use cases and provides guidance on how to implement them in {{es}}.

## RAG and question answering on your own data

:::{image} /solutions/images/elasticsearch-reference-rag-schema.svg
:alt: Components of a simple RAG system using {{es}}
:::

Use vector search to retrieve relevant pieces of your data and provide them to a language model. This helps generate answers that are grounded in your own content instead of relying on general knowledge. Use this when you want to build:

- Question answering over your own documents (PDFs, wikis, tickets)
- Internal or customer-facing knowledge assistants
- Chatbots that use your data instead of general knowledge
- Customer support over FAQs or ticket history  
- Internal knowledge search (Confluence, SharePoint, Notion)  

::::::{stepper}
:::::{step} Learn about RAG in {{es}}

To understand how retrieval-augmented generation works, refer to [RAG](../rag.md).

:::::

:::::{step} Choose a search strategy

To build a RAG application, you first need a search system that can retrieve relevant content from your data.

To set up retrieval, you can use full-text, semantic, or hybrid search. Refer to [Search approaches](../search-approaches.md) to choose the option that best fits your use case.



:::::

:::::{step} Generate answers with an LLM

Take the top retrieved results and pass them as context to a language model. This allows the model to generate answers grounded in your data.

You can implement this step using your preferred LLM provider or orchestration framework (for example, LangChain or LlamaIndex). Refer to [Core search options](../rag.md#core-search-options) to learn about the available approaches for integrating retrieval and generation, including {{esql}} `COMPLETION`, Agent Builder, and custom implementations.

:::::
::::::

## Search semantically over documents and knowledge bases

Use vector search to retrieve documents based on meaning rather than exact keyword matches. This helps users find relevant information even when queries are phrased differently from the original content.

Use this when you want to build:

- Search over documents such as PDFs, wikis, or knowledge bases  
- FAQ or help center search  
- Internal knowledge search (Confluence, SharePoint, Notion)  
- Search experiences where users use natural language queries  
- Multilingual or synonym-heavy content search  

::::::{stepper}
:::::{step} Learn about semantic search

To understand how semantic search works in {{es}}, refer to [Semantic search](../semantic-search.md).

:::::

:::::{step} Choose an implementation approach

To implement semantic search, you can choose between the following approaches depending on your level of control and complexity:

- **[Semantic search with `semantic_text`](../semantic-search/semantic-search-semantic-text.md)**  
  Use this for the simplest setup. {{es}} handles chunking, embedding generation, and indexing automatically. Suitable for most standard text search use cases.

- **[Hybrid search with `semantic_text`](../hybrid-semantic-text.md)**  
  Use this when you want to combine semantic understanding with keyword matching. This is recommended for most production use cases where both exact matches and meaning matter.

- **[Semantic search with the {{infer}} API](../semantic-search/semantic-search-inference.md)**  
  Use this when you need more control over how embeddings are generated, such as choosing models or customizing your pipeline.

:::::
::::::

## Discovery and recommendations (similar items)

## Multimodal search (image, audio, video)

## Duplicate detection, fraud, and anomaly detection

## Enterprise and legal search across large corpora

## Long-term memory for LLMs

