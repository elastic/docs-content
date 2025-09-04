---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-what-is-es.html
products:
  - id: elasticsearch
applies_to:
  stack:
  serverless:
---
# Solutions and use cases [introduction]

Let's take a closer look at each of our three solutions, their use cases and core concepts so you can decide which product best suits your business needs.

- Use [{{es}}](/solutions/search.md) if you want to build powerful, scalable searches to quickly search, analyze, and visualize large amounts of data for real-time insights. 

- Use [Elastic {{observability}}](/solutions/observability.md) if you want to monitor the health and performance of your IT environments and applications or send telemetry data. 

- Use [{{elastic-sec}}](/solutions/security.md) if you want to leverage search and analytics to monitor data, detect anomalous activity, and protect against cyber threats in real time.

You can also check out our [customer success stories](https://www.elastic.co/customers/success-stories) to learn how various organizations are utilizing our products for their specific business needs.
<!--TBD: Call out how solutions map to Serverless project types? -->
<!-- Content moved from the-stack.md
## Get data into Elasticsearch

When building custom search experiences or indexing general data, you have several direct and flexible ingestion options:

* **Native APIs and language clients:** Index any JSON document directly using the {{es}} REST API or the official clients for languages like Python, Java, Go, and more.  
* **Web crawler:** Ingest content from public or private websites to make them searchable.  
* **Enterprise connectors:** Use pre-built connectors to sync data from external content sources like SharePoint, Confluence, Jira, and databases like MongoDB or PostgreSQL into {{es}}.

## Get data into Elastic Observability

For full-stack observability, ingest logs, metrics, traces, and profiles using these OpenTelemetry-native methods:

* **{{edot}}:** Use Elastic's supported OpenTelemetry SDKs for custom application instrumentation and the Collector for vendor-neutral infrastructure telemetry.  
* **{{agent}}:** A single agent to collect infrastructure logs and metrics from hosts, containers, and cloud services using pre-built integrations.  
* **APM Agents:** Provide streamlined, out-of-the-box auto-instrumentation of your applications to capture detailed traces and performance metrics.  
* **{{ls}} and {{beats}}:** Leverage these battle-tested tools for advanced log processing pipelines (Logstash) and lightweight data shipping (Beats).

## Get data into Elastic Security

**{{agent}}** is the core ingestion method for security data. As a single, unified agent, it's purpose-built to collect the rich data needed for modern threat detection and response, including:

* **Endpoint Security:** Collects detailed event data for threat prevention, detection (EDR), and response directly from your endpoints.  
* **System & Audit Logs:** Gathers security-relevant logs and audit trails from hosts across your environment.  
* **Network Activity:** Captures network data to help detect intrusions and suspicious behavior.

Fleets of Elastic Agents are managed centrally, simplifying deployment and policy enforcement across thousands of hosts.
-->
<!-- Existing content from introduction.md
# Use cases [introduction]

The {{stack}} is used for a wide and growing range of use cases. Here are a few examples:

## Elasticsearch

- **Full-text search**: Build a fast, relevant full-text search solution using inverted indexes, tokenization, and text analysis.
- **Vector database**: Store and search vectorized data, and create vector embeddings with built-in and third-party natural language processing (NLP) models.
- **Semantic search**: Understand the intent and contextual meaning behind search queries using tools like synonyms, dense vector embeddings, and learned sparse query-document expansion.
- **Hybrid search**: Combine full-text search with vector search using state-of-the-art ranking algorithms.
- **Build search experiences**: Add hybrid search capabilities to apps or websites, or build enterprise search engines over your organization’s internal data sources.
- **Retrieval augmented generation (RAG)**: Use {{ecloud}} as a retrieval engine to supplement generative AI models with more relevant, up-to-date, or proprietary data for a range of use cases.
- **Geospatial search**: Search for locations and calculate spatial relationships using geospatial queries.

[**Get started with {{es}} →**](../solutions/search/get-started.md)

## Observability

- **Logs, metrics, and traces**: Collect, store, and analyze logs, metrics, and traces from applications, systems, and services.
- **Application performance monitoring (APM)**: Monitor and analyze the performance of business-critical software applications.
- **Real user monitoring (RUM)**: Monitor, quantify, and analyze user interactions with web applications.
- **OpenTelemetry**: Reuse your existing instrumentation to send telemetry data to the Elastic Stack using the OpenTelemetry standard.

[**Get started with {{observability}} →**](../solutions/observability/get-started.md)

## Security

- **Security information and event management (SIEM)**: Collect, store, and analyze security data from applications, systems, and services.
- **Endpoint security**: Monitor and analyze endpoint security data.
- **Threat hunting**: Search and analyze data to detect and respond to security threats.

[**Get started with {{elastic-sec}} →**](../solutions/security/get-started.md)

This is just a sample of search, observability, and security use cases enabled by {{ecloud}}. Refer to Elastic [customer success stories](https://www.elastic.co/customers/success-stories) for concrete examples across a range of industries.
-->
% TODO: cleanup these links, consolidate with Explore and analyze
$$$what-is-kib$$$
$$$what-is-es$$$
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
