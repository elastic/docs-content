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

Elastic offers three major search-powered solutions: {{es}}, Elastic {{observability}}, and {{elastic-sec}}—all built on an open source, extensible platform.
Whether you're building a search experience, monitoring your infrastructure, or securing your environment, this topic helps you understand what each Elastic solution offers—and how to choose the right one for your business needs.

| Your need | Recommended solution | Best for |
|-----------|-------------------|----------|
| Build powerful, scalable searches to quickly search, analyze, and visualize large amounts of data for real-time insights  | [{{es}}](#search-overview) | Developers, architects, data engineers |
| Observe and monitor system health and performance, or send telemetry data | [Elastic {{observability}}](#observability-overview) | DevOps, SREs, IT operations |
| Monitor data for anomalous activity, detect, prevent, and respond to security incidents | [{{elastic-sec}}](#security-overview) | SOC teams, security analysts, IT security admins |

:::{tip}
Check out our [customer success stories](https://www.elastic.co/customers/success-stories) to learn how various organizations utilize our products for their specific business needs.
:::

Each of our solutions is available as a fully managed {{serverless-short}} project or a self-managed deployment. Refer to [deployment options](../get-started/deployment-options.md) to learn about these options. 

## {{es}} [search-overview]

{{es}} combines the core {{es}} data store, search engine, and vector database technologies with specialized user interfaces and tools, giving you the building blocks to create, deploy, and run your own search applications.

<!--
### {{es}} use cases [search-use-cases]
-->
For an overview of search use cases, including full-text, geospatial, semantic, and vector search, as well as retrieval augmented generation (RAG), go to [](/solutions/search.md).
To try out some simple search use cases, go to [](/solutions/search/get-started/quickstarts.md).
<!--
### {{es}} core concepts [search-concepts]
-->
For an introduction to core {{es}} concepts such as indices, documents, and mappings, refer to [](/manage-data/data-store.md).
To dive more deeply into the building blocks of {{es}} clusters, including nodes, shards, primaries, and replicas, refer to [](/deploy-manage/distributed-architecture.md).

<!--
The following concepts are not unique to this solution.
 ::::{dropdown} Concepts

The following concepts relate to core {{es}} features and thus apply to all solutions:

* **Index:** A collection of related documents that are uniquely identified by a name or an alias. The name is used to target the index in search queries and other operations.
* **Document:** Any structured data encoded in JSON. {{es}} organizes and stores data into documents.
* **Field:** The smallest individual unit of data within a document. It represents a specific property or attribute of the data you're indexing (for example, title, author, date, or summary). Fields are critical for indexing, as they determine how data is analyzed and stored to enable efficient searching.
* **Mapping:** The process that defines how a document and its fields are stored and indexed.
* **Client:** Software or an application that facilitates communication and interaction with an {{es}} cluster. It enables applications written in various programming languages to send requests to {{es}}, process its response, and push data into the cluster.
* **Primary shard:** A self-contained Lucene index that contains some or all of an index's data. Shards allow {{es}} to scale horizontally by splitting an index's data into smaller, manageable partitions, improving performance. Each document in an index belongs to one primary shard.
* **Replica:** A copy of a primary shard. Replicas maintain redundant copies of your data across the nodes in your cluster. This protects against hardware failure and increases capacity to serve read requests like searching or retrieving a document.
* **Node:** A single running instance of the {{es}} server. 
* **Cluster:** A collection of one or more nodes that holds all your data and provides indexing and search capabilities across all nodes. {{es}} clusters feature primary and replica shards to provide failover in the case of a node going down. When a primary shard goes down, the replica takes its place.
  :::{note}
  If you're using an {{es-serverless}} project, you don't have to worry about shards, nodes, or clusters. Elastic manages these for you.
  :::
 ::::
-->

## Elastic {{observability}} 

### {{observability}} overview [observability-overview]

Elastic {{observability}} provides unified observability across applications and infrastructure. It combines logs, metrics, application traces, user experience data, and more into a single, integrated platform. This consolidation allows for powerful, cross-referenced analysis, enabling teams to move from detecting issues to understanding their root causes with speed and efficiency. By leveraging the search and analytics capabilities of {{es}}, it offers a holistic view of system behavior.

Elastic {{observability}} embraces open standards like OpenTelemetry for flexible data collection, and offers scalable, cost-efficient data retention with tiered storage.

### {{observability}} use cases [observability-use-cases]

Apply {{observability}} to various scenarios to improve operational awareness and system reliability. 
:::{dropdown} Use cases
* **Log monitoring and analytics:** Centralize and analyze petabytes of log data from any source. This enables quick searching, ad-hoc queries with ES|QL, and visualization with prebuilt dashboards to diagnose issues.
* **Application Performance Monitoring (APM):** Gain code-level visibility into application performance. By collecting and analyzing traces with native OTel support, teams can identify bottlenecks, track errors, and optimize the end-user experience.
* **Infrastructure monitoring:** Monitor metrics from servers, virtual machines, containers, and serverless environments with over 400 out-of-the-box integrations, including OpenTelemetry. This provides deep insights into resource utilization and overall system health.
* **AI-powered log analysis with Streams**: Ingest raw logs in any format directly to a single endpoint without the need for complex agent management or manual parsing pipelines. Streams leverages AI to automatically parse, structure, and analyze log data on the fly.
* **Digital experience monitoring:**
  * **Real User Monitoring (RUM):** Capture and analyze data on how real users interact with web applications to improve perceived performance.
  * **Synthetic monitoring:** Proactively simulate user journeys and API calls to test application availability and functionality.
  * **Uptime monitoring:** Continuously check the status of services and applications to ensure they are available.
* **Universal Profiling:** Gain visibility into system performance and identify expensive lines of code without application instrumentation, helping to increase CPU efficiency and reduce cloud spend.
* **LLM Observability:** Gain deep insights into the performance, usage, and costs of Large Language Model (LLM) prompts and responses.
* **Incident response and management:** Investigate operational incidents by correlating data from multiple sources, which accelerates root cause analysis and resolution.
:::

### {{observability}} core concepts [observability-concepts]
At the heart of Elastic {{observability}} are several key components that enable its capabilities. 

:::{dropdown} Concepts
* The three pillars of {{observability}} are: 
  * [**Logs:**](/solutions/observability/logs.md) Timestamped records of events that provide detailed, contextual information.
  * [**Metrics:**](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) Numerical measurements of system performance and health over time.
  * [**Traces:**](/solutions/observability/apm/traces.md) Representations of end-to-end journeys of requests as they travel through distributed systems.
* [**OpenTelemetry:**](/solutions/observability/apm/use-opentelemetry-with-apm.md) {{Observability}} offers first-class, production-grade support for OpenTelemetry. This allows organizations to use vendor-neutral instrumentation and stream native OTel data without proprietary agents, leveraging the Elastic Distribution of OpenTelemetry (EDOT).
* [**AIOps and AI Assistant:**](/solutions/observability/observability-ai-assistant.md) Leverages predictive analytics and an LLM-powered AI Assistant to reduce the time required to detect, investigate, and resolve incidents. This includes zero-config anomaly detection, pattern analysis, and the ability to surface correlations and root causes.
* **[Alerting](/solutions/observability/incident-management/alerting.md) and [Cases](/solutions/observability/incident-management/cases.md):** Allows you to create  rules to detect complex conditions and perform actions. Cases allows teams to stay aware of potential issues and track investigation details, assign tasks, and collaborate on resolutions.
* [**Service Level Objectives (SLOs):**](/solutions/observability/incident-management/service-level-objectives-slos.md) A framework for defining and monitoring the reliability of a service. Elastic {{observability}} allows for creating and tracking SLOs to ensure that performance targets are being met.
:::

## {{elastic-sec}}

### Security overview [security-overview]

{{elastic-sec}} is a unified security solution that unifies SIEM (Security Information and Event Management), XDR, (Extended Detection and Response), endpoint security, and cloud security into a single platform so you can detect, prevent, and respond to cyber threats across your entire environment in near real time. {{elastic-sec}} leverages {{es}}'s powerful search and analytics capabilities, and {{kib}}'s visualization and collaboration features. By combining prevention, detection, and response capabilities, {{elastic-sec}} helps your organization reduce its security risk. 

Install {{elastic-sec}} on one of our {{ecloud}} deployments or your own self-managed infrastructure.  

### Security use cases [security-use-cases]

Use {{elastic-sec}} to protect your systems from security threats.

:::{dropdown} Use cases
* **SIEM:** {{elastic-sec}}'s modern SIEM provides a centralized platform for ingesting, analyzing, and managing security data from various sources. 
* **Third-party integration support:** Ingest data from a various tools and data sources so you can centralize your security data.
* **Threat detection and analytics:** Identify unknown threats by enabling prebuilt or custom detection rules, automatically detect anomalous activity with built-in machine learning jobs, or proactively search for threats using our powerful threat hunting and interactive visualization tools. 
* **Automatic migration:** Migrate SIEM rules from other platforms to {{elastic-sec}}. 
* **Endpoint protection and threat prevention:** Automatically stop cybersecurity attacks—such as malware and ransomware—before damage and loss can occur.
* **AI-powered features:** Leverage generative AI to help enhance threat detection, assist with incident response, and improve day-to-day security operations. For example, use AI Assistant to summarize alerts, identify relevant information, suggest investigation steps, and generate complex queries from natural language input.
* **Custom dashboards and visualizations:** Create custom dashboards and visualizations to gain insights into security events.
* **Cloud Security:** {{elastic-sec}} provides the following cloud features:
  * **Cloud Security Posture Management (CSPM) and Kubernetes Security Posture Management (KSPM):** Check cloud service configurations against security benchmarks to identify and resolve misconfigurations that can be exploited.
  * **Cloud Workload Protection:** Get visibility and runtime protection for cloud workloads.
  * **Vulnerability Management:** Uncover vulnerabilities within your cloud infrastructure.
:::

### Security core concepts [security-concepts]

Before diving into setup and configuration, familiarize yourself with the foundational terms and core concepts that power {{elastic-sec}}. 

:::{dropdown} Concepts 

* [**{{agent}}:**](/reference/fleet/index.md#elastic-agent) A single, unified way to collect logs, metrics, and other types of data from a host. {{agent}} can also protect hosts from security threats, query data from operating systems, and forward data from remote services or hardware. 
* [**{{elastic-defend}}:**](/solutions/security/configure-elastic-defend/install-elastic-defend.md) {{elastic-sec}}'s Endpoint Detection and Response (EDR) tool that protects endpoints from malicious activity. {{elastic-defend}} uses a combination of techniques like machine learning, behavioral analysis, and prebuilt rules to detect, prevent, and respond to threats in real-time.
* [**{{elastic-endpoint}}:**](/solutions/security/manage-elastic-defend/elastic-endpoint-self-protection-features.md) The security component, enabled by {{agent}}, that performs {{elastic-defend}}'s threat monitoring and prevention capabilities. 
* [**Detection engine:**](/solutions/security/detect-and-alert.md) The framework that detects threats by using rules to search for suspicious events in your data, and generates alerts when events meet a rule's criteria.
* [**Detection rules:**](/solutions/security/detect-and-alert/about-detection-rules.md) Sets of conditions that identify potential threats and malicious activities. Rules analyze various data sources, including logs and network traffic, to detect anomalies, suspicious behaviors, or known attack patterns. {{elastic-sec}} ships out-of-the-box prebuilt rules, and you can create your own custom rules. 
* [**Alerts:**](/solutions/security/detect-and-alert/manage-detection-alerts.md) Notifications that are generated when rule conditions are met. Alerts include a wide range of information about potential threats, including host, user, network, and other contextual data to assist your investigation.  
* [**Machine learning and anomaly detection:**](/solutions/security/advanced-entity-analytics/anomaly-detection.md) Anomaly detection jobs identify anomalous events or patterns in your data. Use these with machine learning detection rules to generate alerts when behavior deviates from normal activity.
* [**Entity analytics:**](/solutions/security/advanced-entity-analytics/overview.md) A threat detection feature that combines the power of Elastic’s detection engine and machine learning capabilities to identify unusual behavior for hosts, users, and services. 
* [**Cases:**](/solutions/security/investigate/cases.md) A tool that allows you to collect and share information about security issues. Opening a case lets you track key investigation details and collect alerts in a central location. You can also send cases to external systems.
* [**Timeline:**](/solutions/security/investigate/timeline.md) A threat hunting tool that allows you to investigate security events so you can gather and analyze data related to alerts or suspicious activity. You can add events to Timeline from various sources, build custom queries, and import/export a Timeline to collaborate and share. 
* [**Security posture management:**](/solutions/security/cloud.md) Includes native cloud security features, such as Cloud Security Posture Management (CSPM) and Cloud Native Vulnerability Management (CNVM), that help you evaluate your cloud infrastructure's configuration against security best practices and identify vulnerabilities. You can use Elastic's native tools or ingest third-party cloud security data and incorporate it into {{elastic-sec}}'s workflows.
* [**AI Assistant:**](/solutions/security/ai/ai-assistant.md) A generative AI-powered tool that helps with tasks like alert investigation, incident response, and query generation. It utilizes natural language processing and knowledge retrieval to provide context-aware assistance, summarize threats, suggest next steps, and automate workflows. Use AI Assistant to better understand and respond to security incidents.
:::

<!--TBD: Call out how solutions map to Serverless project types? -->
<!-- Content moved from the-stack.md
## Get data into Elasticsearch

When building custom search experiences or indexing general data, you have several direct and flexible ingestion options:

* **Native APIs and language clients:** Index any JSON document directly using the {{es}} REST API or the official clients for languages like Python, Java, Go, and more.  
* **Web crawler:** Ingest content from public or private websites to make it searchable.  
* **Enterprise connectors:** Use pre-built connectors to sync data from external content sources like SharePoint, Confluence, Jira, and databases like MongoDB or PostgreSQL into {{es}}.

## Get data into Elastic Observability

For full-stack observability, ingest logs, metrics, traces, and profiles using these OpenTelemetry-native methods:

* **{{edot}}:** Use Elastic's OpenTelemetry SDKs for custom application instrumentation and the Collector for vendor-neutral infrastructure telemetry.  
* **{{agent}}:** Collects infrastructure logs and metrics from hosts, containers, and cloud services using pre-built integrations.  
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
