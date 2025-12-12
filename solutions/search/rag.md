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



## Getting started [rag-elasticsearch-getting-started]

Start building RAG applications quickly with Playground, which seamlessly integrates {{es}} with language model providers. The Playground UI enables you to build, test, and deploy RAG interfaces on top of your {{es}} indices.

Playground automatically selects the best retrieval methods for your data, while providing full control over the final {{es}} queries and language model instructions. You can also download the underlying Python code to integrate with your existing applications.

::::{note}
Playground is available as part of the {{es}} solution and serverless project type. Learn more in the [Playground documentation](/solutions/elasticsearch-solution-project/playground.md) and try the [interactive lab](https://www.elastic.co/demo-gallery/ai-playground) for hands-on experience.
::::


## Learn more [rag-elasticsearch-learn-more]

Learn more about building RAG systems using {{es}} in these blog posts:

* [Beyond RAG Basics: Advanced strategies for AI applications](https://www.elastic.co/blog/beyond-rag-basics)
* [Building a RAG system with Gemma, Hugging Face, and Elasticsearch](https://www.elastic.co/search-labs/blog/building-a-rag-system-with-gemma-hugging-face-elasticsearch)
* [Building an agentic RAG tool with Elasticsearch and Langchain](https://www.elastic.co/search-labs/blog/rag-agent-tool-elasticsearch-langchain)

