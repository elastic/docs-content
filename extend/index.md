---
description: Extend the Elastic Platform by creating integrations for data ingestion
  or building custom applications with REST APIs. Learn how to contribute to Elastic
  documentation and ecosystem.
---

# Extend and contribute 

You can extend and build on the Elastic Platform in several ways. Whether you need to get data into Elasticsearch, add new functionality, edit the documentation, or build a custom application, here is an overview of the primary development paths to help you choose the right one for your project.

There are two main approaches to extending Elastic: creating standardized Integrations for data ingestion or building custom solutions by developing directly against our REST APIs.

## Path 1: Create an Elastic Integration

If your primary goal is to bring a new data source into the Elastic Stack in a standardized, reusable way, building an Elastic Integration is the best path. Integrations are pre-packaged assets that make it simple for users to collect and process data from a specific service or platform.

This approach is ideal for shipping data, logs, metrics, and traces. By building an integration, you contribute to the ever-growing ecosystem that both you and the community can benefit from.

* Integrations are built on a consistent framework, providing users with a turnkey experience, including dashboards, visualizations, and alerts.  
* **`elastic-package`** is a command-line tool that is your primary interface for creating, testing, and packaging your integration. It scaffolds the entire project structure, letting you focus on the logic for data collection.  
* Your integration will run on the Elastic Agent, our single, unified agent for data shipping.

**When to choose this path**

* You want to ingest data from a new data source, like a database, API, or log file.  
* You want to provide a standardized, out-of-the-box experience for other users.  
* You need to process and structure data according to the Elastic Common Schema (ECS).

**Ready to start?** Head over to the [Create an Integration](integrations://extend/index.md) guide.

## Path 2: Develop against the REST APIs

For complete control and custom development, you can interact directly with Elastic's REST APIs. This path is perfect for building custom applications, automating complex workflows, and integrating Elastic into your existing infrastructure in a bespoke way. For example, you can programmatically manage your cluster, run complex queries, manage security settings, and interact with Kibana.

* The APIs provide direct access to the core capabilities of Elasticsearch and Kibana. If you can do it in the UI, you can automate it with the API.  
* Elastic provides and supports official [clients](/reference/elasticsearch-clients/index.md) for popular languages like Java, Go, .NET, PHP, Python, Ruby, and JavaScript. These clients simplify interacting with the API, handling requests, and processing responses.
* The APIs are secured using role-based access control (RBAC). You can create API keys or use bearer tokens with fine-grained permissions to ensure your interactions are safe.

### Elastic APIs at a glance

* Use the Elasticsearch APIs to:

  * Create, read, update, and delete documents.  
  * Perform everything from simple keyword searches to complex analytical aggregations.  
  * Monitor cluster health, manage nodes, and configure settings.  
  * Manage users, roles, and API keys.  

* Use the Kibana APIs to programmatically control the Kibana front-end and its objects:

  * Create and manage dashboards, visualizations, and saved searches.  
  * Automate the organization of content within Kibana.  
  * Create and manage rules for detecting conditions within your data.

**When to choose this path**

* You are building a custom application that uses Elasticsearch as its backend.  
* You need to automate administrative tasks, such as creating users or managing index lifecycle policies.  
* You are integrating Elastic's search and analytics capabilities into another platform.

Ready to get started? Explore the [Elastic API Reference]({{apis}}).

## Contributing to Elastic documentation

You can contribute to the Elastic documentation in several ways. Refer to [Contribute to Elastic documentation](./../contribute-docs/index.md) for an overview.
