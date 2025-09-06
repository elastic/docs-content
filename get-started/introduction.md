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

Elastic offers three major search-powered solutions: {{es}}, {{observability}}, and {{elastic-sec}}— all built on {{es}}. Whether you're building a search experience, monitoring your infrastructure, or securing your environment, this topic helps you understand what each Elastic solution offers—and how to choose the right one for your business needs.

Refer to the following table for a quick reference of which solution you may need based on your needs. 

| Your need | Recommended solution | Best for |
|-----------|-------------------|----------|
| Build powerful, scalable searches to quickly search, analyze, and visualize large amounts of data for real-time insights  | [{{es}}](/solutions/search.md) | Developers, architects, data engineers |
| Observe and monitor system health and performance or send telemetry data | [Elastic {{observability}}](/solutions/observability.md) | DevOps, SREs, IT operations |
| Monitor data for anomalous activity, detect, prevent, and respond to security incidents | [{{elastic-sec}}](/solutions/security.md) | SOC teams, security analysts, IT security admins |

:::{tip}
Check out our [customer success stories](https://www.elastic.co/customers/success-stories) to learn how various organizations are utilizing our products for their specific business needs.
:::

## Elasticsearch

### Overview [search-overview]

{{es}} is an open-source, distributed search and analytics engine built on Apache Lucene, used for high-performance full-text search, log analytics, business analytics, and operational intelligence. It stores data in JSON documents, provides REST APIs for easy interaction, and functions as a NoSQL database that enables fast searches, analytics, and AI-driven applications. Built on Apache Lucene, {{es}} is the core of the Search AI platform. 

### Use cases [search-use-cases]
Use {{es}} for a wide range of business needs:  

* **Full-text search:** Quickly find specific words or phrases within large volumes of text-based data, such as documents, articles, or product descriptions. Documents and search queries are transformed to enable returning relevant results instead of simply exact term matches. 
* **Semantic search:** Go beyond keyword matching to understand the user's intent. This helps your search engine to recognize what users mean, not just what they type, by understanding synonyms and related concepts.
* **Hybrid search:** Get the best of both worlds by combining traditional keyword search with modern, meaning-based vector search. This ensures your users get the most accurate and relevant results every time.
* **Vector database:** Search for data based on its meaning and context, not just keywords. This allows you to find similar items, like pictures that have the same style or songs with a similar vibe, by understanding the underlying concepts.
* **Retrieval augmented generation (RAG):** Connect your generative AI applications (like chatbots) to your own private data. This allows your AI to provide more accurate, up-to-date, and relevant answers based on your proprietary information.
* **Geospatial search:** Build location-aware features into your applications. This allows you to do things like find all available services within a certain radius, calculate the distance between two points, or identify which delivery routes are most efficient.

### Core concepts [search-concepts]
Familiarize yourself with the following {{es}} concepts. 

* **Index:** A collection of documents with similar characteristics that are uniquely identified by a name or an alias. The name is used to target the index in search queries and other operations.
 **Field:** The smallest individual unit of data within a document. It represents a specific property or attribute of the data you're indexing (for example, title, author, date, summary, etc.). Fields are critical for indexing, as they determine how data is analyzed and stored to enable efficient searching.
* **Document:** Any structured data encoded in JSON. {{es}} organizes and stores data into documents. 
* **Shard:** A self-contained Lucene index that contains a subset of the documents in the index. Shards allow {{es}} to horizontally scale by splitting an index's data into smaller, manageable partitions, thus improving performance. Each document in an index belongs to one primary shard.
* **Replica:** A copy of a primary shard. Replicas maintain redundant copies of your data across the nodes in your cluster. This protects against hardware failure and increases capacity to serve read requests like searching or retrieving a document.
* **Node:** A single running instance of the {{es}} server. 
* **Cluster:** A collection of one or more nodes that holds all of your data and provides  indexing and search capabilities across all nodes. Elasticsearch clusters feature primary and replica shards to provide failover in the case of a node going down. When a primary shard goes down, the replica takes its place.
* **Mapping:** The process that defines how a document and the fields it contains are stored and indexed.

## Elastic {{observability}} 

### Overview [observability-overview]

Elastic {{observability}} provides unified observability across applications and infrastructure. It brings together logs, metrics, application traces, user experience data, and more into a single, integrated platform. This consolidation allows for powerful, cross-referenced analysis, enabling teams to move from detecting issues to understanding their root causes with speed and efficiency. By leveraging the search and analytics capabilities of {{es}}, it offers a holistic view of system behavior.

Available as a fully-managed {{serverless-short}} project or a self-managed deployment, Elastic {{observability}} embraces open standards like OpenTelemetry for flexible data collection, and offers scalable, cost-efficient data retention with tiered storage.

### Use cases [observability-use-cases]

Apply Elastic {{observability}} to a wide range of scenarios to improve operational awareness and system reliability:

* **Log Monitoring and Analytics:** Centralize and analyze petabytes of log data from any source. This enables quick searching, ad-hoc queries with ES|QL, and visualization with prebuilt dashboards to diagnose issues.
* **Application Performance Monitoring (APM):** Gain code-level visibility into application performance. By collecting and analyzing traces with native OTel support, teams can identify bottlenecks, track errors, and optimize the end-user experience.
* **Infrastructure Monitoring:** Monitor metrics from servers, virtual machines, containers, and serverless environments with over 400 out-of-the-box integrations, including OpenTelemetry. This provides deep insights into resource utilization and overall system health.
* **Digital Experience Monitoring:**
  * **Real User Monitoring (RUM):** Capture and analyze data on how real users are interacting with web applications to improve perceived performance.
  * **Synthetic Monitoring:** Proactively simulate user journeys and API calls to test application availability and functionality.
  * **Uptime Monitoring:** Continuously check the status of services and applications to ensure they are available.
* **Universal Profiling:** Gain visibility into system performance and identify expensive lines of code without application instrumentation, helping to increase CPU efficiency and reduce cloud spend.
* **LLM Observability:** Gain deep insights into the performance, usage, and costs of Large Language Model (LLM) prompts and responses.
* **Incident Response and Management:** Facilitate the investigation of operational incidents by correlating data from multiple sources, which accelerates root cause analysis and resolution.

### Core concepts [observability-concepts]

## {{elastic-sec}} 

### Overview 

{{elastic-sec}} is a unified security solution that integrates SIEM (Security Information and Event Management), endpoint security, and cloud security into a single platform so you can detect, prevent, and respond to cyber threats across your entire environment in near real time. Elastic Security leverages {{es}} powerful platform for its searching and analytic capabilities, and {{kib}} for its visualization features. By combining prevention, detection, and response capabilities, {{elastic-sec}} helps your organization reduce the risk of successful attacks. 

Install {{elastic-sec}} on one of our Elastic-managed Cloud deployments or on your own self-managed infrastructure.  

### Use cases 

Use {{elastic-sec}} for a wide variety of security needs to ensure your systems are protected from the latest threats.

* **SIEM:** {{elastic-sec}} acts as a modern SIEM that provides a centralized platform for ingesting, analyzing, and managing security data from various sources. 
* **Third-party integration support:** Ingest data from a variety of tools and data sources so you can centralize your security data.
* **Threat detection and analytics:** Identify unknown threats by enabling prebuilt or custom detection rules, automatically detect anomalous activity with built-in machine learning jobs, or proactively search for threats using our powerful threat hunting and interactive visualization tools. 
* **Automatic migration:** Migrate SIEM rules from other platforms to Elastic Security. 
* **Endpoint protection and threat prevention:** Automatically stop cybersecurity attacks—such as malware and ransomware—before damage and loss can occur.
* **AI-powered features:** Elastic Security leverages generative AI to help enhance threat detection, assist with incident response, and day-to-day security operations. For example, the AI Assistant  can summarize alerts, identify relevant information, suggest investigation steps, and even generate complex queries from natural language input.
* **Custom dashboards and visualizations:** Create custom dashboards and visualizations to gain insights into security events.
* **Cloud Security:** Elastic Security provides the following cloud features:
  * **Cloud Security Posture Management (CSPM) and Kubernetes Security Posture Management (KSPM):** Check cloud service configurations against security benchmarks to identify and resolve misconfigurations that could be exploited.
  * **Cloud Workload Protection:** Get visibility and runtime protection for cloud workloads.
  * **Vulnerability Management:** Uncover vulnerabilities within your cloud infrastructure.

 ### Core concepts



Let's take a more comprehensive look at the various use cases for 
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
