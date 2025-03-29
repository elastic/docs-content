---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-what-is-es.html
---

# {{es}} and {{kib}} [introduction]

## What is {{es}}?

[{{es}}](https://github.com/elastic/elasticsearch) is a distributed search and analytics engine, scalable data store, and vector database built on Apache Lucene. It’s optimized for speed and relevance on production-scale workloads. Use {{es}} to search, index, store, and analyze data of all shapes and sizes in near real time.

You can deploy {{es}} as a standalone service to build custom search and analytics solutions or deploy it together with other Elastic products, using various [deployment options](./deployment-options.md).

Explore the full list of [{{es}} features](https://www.elastic.co/elasticsearch/features) on the product webpage.

To learn more about the internals of the data store, refer to [](/manage-data/data-store.md).

::::{tip}
Want to get started quickly with the {{es}} API? Check out our hands-on [quick start tutorials](/solutions/search/api-quickstarts.md) and [Python notebooks](https://github.com/elastic/elasticsearch-labs/tree/main/notebooks#readme).
::::

## What is {{kib}}?

[{{kib}}](https://github.com/elastic/kibana) is the graphical user interface for {{es}}. It’s a powerful tool for visualizing and analyzing your data, and for managing and monitoring the Elastic Stack.

Together, {{es}} and {{kib}} form the core of the [Elastic Stack](the-stack.md).

They power all Elastic solutions and use cases:

- [Observability](/solutions/observability.md)
- [Security](/solutions/security.md)
- [Search](/solutions/search.md)

## Use cases

The {{stack}} is used for a wide and growing range of use cases. Here are a few examples:

**Observability**

- **Logs, metrics, and traces**: Collect, store, and analyze logs, metrics, and traces from applications, systems, and services.
- **Application performance monitoring (APM)**: Monitor and analyze the performance of business-critical software applications.
- **Real user monitoring (RUM)**: Monitor, quantify, and analyze user interactions with web applications.
- **OpenTelemetry**: Reuse your existing instrumentation to send telemetry data to the Elastic Stack using the OpenTelemetry standard.

**Security**

- **Security information and event management (SIEM)**: Collect, store, and analyze security data from applications, systems, and services.
- **Endpoint security**: Monitor and analyze endpoint security data.
- **Threat hunting**: Search and analyze data to detect and respond to security threats.

**Search**

- **Full-text search**: Build a fast, relevant full-text search solution using inverted indexes, tokenization, and text analysis.
- **Vector database**: Store and search vectorized data, and create vector embeddings with built-in and third-party natural language processing (NLP) models.
- **Semantic search**: Understand the intent and contextual meaning behind search queries using tools like synonyms, dense vector embeddings, and learned sparse query-document expansion.
- **Hybrid search**: Combine full-text search with vector search using state-of-the-art ranking algorithms.
- **Build search experiences**: Add hybrid search capabilities to apps or websites, or build enterprise search engines over your organization’s internal data sources.
- **Retrieval augmented generation (RAG)**: Use {{ecloud}} as a retrieval engine to supplement generative AI models with more relevant, up-to-date, or proprietary data for a range of use cases.
- **Geospatial search**: Search for locations and calculate spatial relationships using geospatial queries.

This is just a sample of search, observability, and security use cases enabled by {{ecloud}}. Refer to Elastic [customer success stories](https://www.elastic.co/customers/success-stories) for concrete examples across a range of industries.

% TODO: cleanup these links, consolidate with Explore and analyze

$$$visualize-and-analyze$$$
$$$extend-your-use-case$$$
$$$_manage_your_data$$$
$$$_alert_and_take_action$$$
$$$organize-and-secure$$$
$$$organize-in-spaces$$$
$$$_organize_your_content_with_tags$$$
$$$intro-kibana-Security$$$
$$$_log_in$$$
$$$extend-your-use-case$$$
$$$try-kibana$$$
$$$_view_all_kib_has_to_offer$$$
$$$_audit_access$$$
$$$_secure_access$$$
