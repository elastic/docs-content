---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_retrieval_augmented_generation.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
---

# RAG [_retrieval_augmented_generation]

::::{admonition} 🍿 Prefer a video introduction?
Check out [this short video](https://www.youtube.com/watch?v=OS4ZefUPAks) from the Elastic Snackable Series.
::::

Retrieval Augmented Generation (RAG) is a technique for improving language model responses by grounding the model with additional, verifiable sources of information. It works by first retrieving relevant context from an external datastore, which is then added to the model’s context window.

RAG is a form of [in-context learning](https://arxiv.org/abs/2301.00234), where the model learns from information provided at inference time. Compared to fine-tuning or continuous pre-training, RAG can be implemented more quickly and cheaply, and offers several advantages.

:::{image} /solutions/images/elasticsearch-reference-rag-venn-diagram.svg
:alt: RAG sits at the intersection of information retrieval and generative AI
:width: 600px
:::

RAG sits at the intersection of [information retrieval](https://www.elastic.co/what-is/information-retrieval) and generative AI. {{es}} is an excellent tool for implementing RAG, because it offers various retrieval capabilities, such as full-text search, vector search, and hybrid search, as well as other tools like filtering, aggregations, and security features.


## Advantages of RAG [rag-elasticsearch-advantages]

Implementing RAG with {{es}} has several advantages:

* **Improved context:** Enables grounding the language model with additional, up-to-date, and/or private data.
* **Reduced hallucination:** Helps minimize factual errors by enabling models to cite authoritative sources.
* **Cost efficiency:** Requires less maintenance compared to fine-tuning or continuously pre-training models.
* **Built-in security:** Controls data access by leveraging {{es}}'s [user authorization](../../deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md) features, such as role-based access control and field/document-level security.
* **Simplified response parsing:** Eliminates the need for custom parsing logic by letting the language model handle parsing {{es}} responses and formatting the retrieved context.
* **Flexible implementation:** Works with basic [full-text search](full-text.md), and can be gradually updated to add more advanced and computationally intensive [semantic search](semantic-search.md) capabilities.


## RAG system overview [rag-elasticsearch-components]

The following diagram illustrates a simple RAG system using {{es}}.

:::{image} /solutions/images/elasticsearch-reference-rag-schema.svg
:alt: Components of a simple RAG system using Elasticsearch
:::

The workflow is as follows:

1. The user submits a query.
2. Elasticsearch retrieves relevant documents using full-text search, vector search, or hybrid search.
3. The language model processes the context and generates a response, using custom instructions. Examples of custom instructions include "Cite a source" or "Provide a concise summary of the `content` field in markdown format."
4. The model returns the final response to the user.

::::{tip}
A more advanced setup might include query rewriting between steps 1 and 2. This intermediate step could use one or more additional language models with different instructions to reformulate queries for more specific and detailed responses.
::::

## Building RAG applications [rag-elasticsearch-getting-started]

You can build RAG applications with {{es}} by retrieving relevant context from your indices and passing it to a language model. The basic approach works across all deployment types, solutions, and project types:

1. Use {{es}} search capabilities (full-text, vector, semantic, or hybrid search) to retrieve relevant documents
2. Pass the retrieved content as context to your language model
3. The language model generates a response grounded in your data

### Core search options

**{{esql}} `COMPLETION` command:** Use the [`COMPLETION`](elasticsearch://reference/query-languages/esql/commands/completion.md) command to send prompts and context directly to language models within your {{esql}} queries.

**Agent Builder:** Create AI agents that can search your {{es}} indices, use tools, and maintain conversational context. Agent Builder provides a complete framework for building stateful RAG applications. Learn more in the [Agent Builder documentation](/solutions/elasticsearch-solution-project/elastic-agent-builder.md).

**Custom implementation:** Retrieve documents using any {{es}} [search approach](/solutions/search/search-approaches.md) (Query DSL, {{esql}}, or retrievers), then integrate with your choice of language model provider in your applications code using their APIs or SDKs.

### {{es}} solution UI tools

If you're using the {{es}} solution or serverless project type, these additional tools provide enable RAG workflows:

**Playground:** Build, test, and deploy RAG interfaces with a UI that automatically selects retrieval methods and provides full control over queries and model instructions. Download Python code to integrate with your applications. Learn more in the [Playground documentation](/solutions/elasticsearch-solution-project/playground.md).


## Learn more [rag-elasticsearch-learn-more]

Learn more about building RAG systems using {{es}} in these blog posts:

* [Beyond RAG Basics: Advanced strategies for AI applications](https://www.elastic.co/blog/beyond-rag-basics)
* [Building a RAG system with Gemma, Hugging Face, and Elasticsearch](https://www.elastic.co/search-labs/blog/building-a-rag-system-with-gemma-hugging-face-elasticsearch)
* [Building an agentic RAG tool with Elasticsearch and Langchain](https://www.elastic.co/search-labs/blog/rag-agent-tool-elasticsearch-langchain)

