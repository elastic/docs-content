---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-what-is-es.html
---

# Get started [elasticsearch-intro-what-is-es]

[{{es}}](https://github.com/elastic/elasticsearch/) is a distributed search and analytics engine, scalable data store, and vector database built on Apache Lucene. It’s optimized for speed and relevance on production-scale workloads. Use {{es}} to search, index, store, and analyze data of all shapes and sizes in near real time.

{{es}} is the heart of the [Elastic Stack](the-stack.md). Combined with [{{kib}}](https://www.elastic.co/kibana), it powers the following Elastic solutions:

* [Observability](https://www.elastic.co/observability)
* [Search](https://www.elastic.co/enterprise-search)
* [Security](https://www.elastic.co/security)

::::{tip}
{{es}} has a lot of features. Explore the full list on the [product webpage](https://www.elastic.co/elasticsearch/features).

::::


::::{admonition} What is the Elastic Stack?
:name: elasticsearch-intro-elastic-stack

{{es}} is the core component of the Elastic Stack, a suite of products for collecting, storing, searching, and visualizing data. [Learn more about the Elastic Stack](the-stack.md).

::::



## Use cases [elasticsearch-intro-use-cases]

{{es}} is used for a wide and growing range of use cases. Here are a few examples:

**Observability**

* **Logs, metrics, and traces**: Collect, store, and analyze logs, metrics, and traces from applications, systems, and services.
* **Application performance monitoring (APM)**: Monitor and analyze the performance of business-critical software applications.
* **Real user monitoring (RUM)**: Monitor, quantify, and analyze user interactions with web applications.
* **OpenTelemetry**: Reuse your existing instrumentation to send telemetry data to the Elastic Stack using the OpenTelemetry standard.

**Search**

* **Full-text search**: Build a fast, relevant full-text search solution using inverted indexes, tokenization, and text analysis.
* **Vector database**: Store and search vectorized data, and create vector embeddings with built-in and third-party natural language processing (NLP) models.
* **Semantic search**: Understand the intent and contextual meaning behind search queries using tools like synonyms, dense vector embeddings, and learned sparse query-document expansion.
* **Hybrid search**: Combine full-text search with vector search using state-of-the-art ranking algorithms.
* **Build search experiences**: Add hybrid search capabilities to apps or websites, or build enterprise search engines over your organization’s internal data sources.
* **Retrieval augmented generation (RAG)**: Use {{es}} as a retrieval engine to supplement generative AI models with more relevant, up-to-date, or proprietary data for a range of use cases.
* **Geospatial search**: Search for locations and calculate spatial relationships using geospatial queries.

**Security**

* **Security information and event management (SIEM)**: Collect, store, and analyze security data from applications, systems, and services.
* **Endpoint security**: Monitor and analyze endpoint security data.
* **Threat hunting**: Search and analyze data to detect and respond to security threats.

This is just a sample of search, observability, and security use cases enabled by {{es}}. Refer to Elastic [customer success stories](https://www.elastic.co/customers/success-stories) for concrete examples across a range of industries.
