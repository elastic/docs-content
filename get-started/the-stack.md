---
navigation_title: Solutions
mapped_pages:
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/stack-components.html
  - https://www.elastic.co/guide/en/kibana/current/introduction.html
  - https://www.elastic.co/guide/en/kibana/current/index.html
  - https://www.elastic.co/guide/en/elastic-stack/current/installing-elastic-stack.html
  - https://www.elastic.co/guide/en/elastic-stack/current/overview.html
products:
  - id: elastic-stack
  - id: kibana
---

# Solutions and the Search AI platform

Let's take a closer look at each of our three solutions, their use cases and core concepts so you can decide which product best suits your business needs. 

- Use [{{es}}](/solutions/search.md) if you want to build powerful, scalable searches to quickly search, analyze, and visualize large amounts of data for real-time insights. 

- Use [Elastic {{observability}}](/solutions/observability.md) if you want to monitor the health and performance of your IT environments and applications or send telemetry data. 

- Use [{{elastic-sec}}](/solutions/security.md) if you want to leverage search and analytics to monitor data, detect anomalous activity, and protect against cyber threats in real time.

You can also check out our [customer success stories](https://www.elastic.co/customers/success-stories) to learn how various organizations are utilizing our products for their specific business needs.    

## Search AI platform overview

Elastic's Search AI platform is built around the {{stack}}, a group of open source products and components designed for ingesting, storing, searching, analyzing, and visualizing data.

Continue reading to learn how these components work together. 

### Ingest data from a wide variety of sources

**Ingestion** is the process of collecting data from your sources and sending it to {{es}}. The Elastic platform is engineered for flexibility, designed to ingest data from a wide variety of sources. 

#### Elasticsearch

When building custom search experiences or indexing general data, you have several direct and flexible ingestion options:

* **Native APIs and language clients:** Index any JSON document directly using the {{es}} REST API or the official clients for languages like Python, Java, Go, and more.  
* **Web crawler:** Ingest content from public or private websites to make them searchable.  
* **Enterprise connectors:** Use pre-built connectors to sync data from external content sources like SharePoint, Confluence, Jira, and databases like MongoDB or PostgreSQL into {{es}}.

#### Elastic Observability

For full-stack observability, ingest logs, metrics, traces, and profiles using these OpenTelemetry-native methods:

* **{{edot}}:** Use Elastic's supported OpenTelemetry SDKs for custom application instrumentation and the Collector for vendor-neutral infrastructure telemetry.  
* **{{agent}}:** A single agent to collect infrastructure logs and metrics from hosts, containers, and cloud services using pre-built integrations.  
* **APM Agents:** Provide streamlined, out-of-the-box auto-instrumentation of your applications to capture detailed traces and performance metrics.  
* **{{ls}} and {{beats}}:** Leverage these battle-tested tools for advanced log processing pipelines (Logstash) and lightweight data shipping (Beats).

#### Elastic Security

**{{agent}}** is the core ingestion method for security data. As a single, unified agent, it's purpose-built to collect the rich data needed for modern threat detection and response, including:

* **Endpoint Security:** Collects detailed event data for threat prevention, detection (EDR), and response directly from your endpoints.  
* **System & Audit Logs:** Gathers security-relevant logs and audit trails from hosts across your environment.  
* **Network Activity:** Captures network data to help detect intrusions and suspicious behavior.

Fleets of Elastic Agents are managed centrally, simplifying deployment and policy enforcement across thousands of hosts.

### Store your data

{{es}} is the heart of the Elastic Stack, functioning as the central place to store and search your data. It stores data as **JSON documents**, which are structured data objects. These documents are organized into **indices**, which you can think of as collections of similar documents.

Elasticsearch is built to be a resilient and scalable distributed system. It runs as a **cluster** of one or more servers, called **nodes**. When you add data to an index, it's divided into pieces called **shards**, which are spread across the various nodes in the cluster. This architecture allows Elasticsearch to handle large volumes of data and ensures that your data remains available even if a node fails.

Learn more in [The {{es}} data store](/manage-data/data-store.md)

### Visualize and query your data

While {{es}} stores your data, **Kibana** is the user interface where you can explore, visualize, and manage it. It provides a window into your data, allowing you to quickly gain insights and understand trends.

With Kibana, you can:

* Use **Discover** to interactively search and filter your raw data.  
* Build custom **visualizations** like charts, graphs, and metrics with tools like **Lens**, which offers a drag-and-drop experience.  
* Assemble your visualizations into interactive **dashboards** to get a comprehensive overview of your information.  
* Analyze geospatial data using the powerful **Maps** application.

At the same time, Kibana works as the user interface of all Elastic solutions, like Elastic Security and Elastic Observability, providing ways of configuring Elastic to suit your needs and offering interactive guidance.

A **query** is a question you ask about your data, and Elastic provides several powerful languages to do so. You can query data directly through the API or through the user interface in Kibana.

* **Kibana Query Language (KQL)** is the text-based language used in the **Discover** search bar, perfect for interactive filtering and exploration.  
* **Elasticsearch Query Language (ES|QL)** is a powerful, modern query language that uses a familiar pipe-based syntax to transform and aggregate your data at search time.  
* **Event Query Language (EQL)** is a specialized language designed to query sequences of events, which is particularly useful for security analytics and threat hunting.

Learn more in [Explore and analyze data with Kibana](/explore-analyze/index.md) 
