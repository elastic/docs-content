---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-what-is-es.html
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/index.html
products:
  - id: elasticsearch
  - id: elastic-stack
  - id: observability
  - id: security
applies_to:
  serverless:
  stack:
description: Learn what Elastic is, understand the platform and solutions it provides,
  and discover how Elastic can help solve your business challenges.
---

# What is Elastic? [what-is-elastic]

Elastic is a company that provides an open source search, analytics, and AI platform, along with out-of-the-box solutions for observability and security. The Elastic platform combines the power of search and generative AI to deliver near real-time search and analysis capabilities that help organizations reduce time to value and make data-driven decisions.

:::{image} /get-started/images/elastic-platform.png
:alt: The Elastic platform
:::

## The Elastic platform

At its core, Elastic provides a distributed, RESTful search and analytics engine built on Apache Lucene. The platform is designed to handle large volumes of data—whether structured or unstructured, text or numerical, geospatial or time-series—and make it searchable and analyzable in near real-time.

The platform is built on open source principles, giving you the flexibility to:
- Deploy on your own infrastructure or in the cloud
- Customize and extend functionality to meet your specific needs
- Avoid vendor lock-in with open APIs and standards

## Core solutions

Elastic offers three primary solutions built on the platform, each designed to address specific business needs:

### Elasticsearch

{{es}} is the distributed search and analytics engine at the heart of the Elastic platform. It enables you to:
- Build powerful, scalable search experiences for applications and websites
- Perform complex analytics on large datasets
- Store and query structured and unstructured data
- Integrate with generative AI to enhance search relevance and user experience

Whether you're building a product catalog search, implementing site search, creating a recommendation engine, or developing custom analytics applications, {{es}} provides the foundation for fast, relevant search and analysis.

[Learn more about {{es}}](/solutions/search.md)

### Elastic Observability

Elastic {{observability}} helps you monitor, troubleshoot, and optimize your applications and infrastructure. It provides:
- **Application Performance Monitoring (APM)**: Track application performance, identify bottlenecks, and understand user experience
- **Log analytics**: Centralize, search, and analyze logs from across your infrastructure
- **Infrastructure monitoring**: Monitor servers, containers, and cloud services
- **Synthetic monitoring**: Proactively test and monitor your applications from around the world
- **Uptime monitoring**: Track the availability and response times of your services

With Elastic {{observability}}, you can gain visibility into your entire technology stack, from applications to infrastructure, helping you maintain system health and performance.

[Learn more about Elastic {{observability}}](/solutions/observability.md)

### Elastic Security

{{elastic-sec}} provides security information and event management (SIEM), endpoint security, and cloud security capabilities. It helps you:
- **Detect threats**: Identify security incidents and anomalous activity across your environment
- **Investigate incidents**: Use powerful search and analytics to investigate security events
- **Prevent attacks**: Protect endpoints and cloud workloads from threats
- **Respond quickly**: Automate response actions and streamline security workflows
- **Comply with regulations**: Meet compliance requirements with built-in reporting and audit capabilities

{{elastic-sec}} enables security teams to protect their organizations by providing comprehensive visibility into security events and the tools needed to detect, investigate, and respond to threats.

[Learn more about {{elastic-sec}}](/solutions/security.md)

## The Elastic Stack

The {{stack}} is a collection of open source products that work together to help you take data from any source, in any format, and search, analyze, and visualize it. The core components include:

- **{{es}}**: The distributed search and analytics engine
- **{{kib}}**: The visualization and management interface
- **{{beats}}**: Lightweight data shippers for sending operational data
- **{{ls}}**: A data processing pipeline for transforming and enriching data
- **{{agent}}**: A unified agent for collecting observability and security data

These components are designed to work together seamlessly, with synchronized releases to simplify installation and upgrades.

[Learn more about the {{stack}}](/get-started/the-stack.md)

## Key capabilities

### Search and relevance

Elastic provides powerful search capabilities that go beyond simple keyword matching:
- **Full-text search**: Search across large volumes of text with relevance ranking
- **Fuzzy matching**: Find results even with typos or variations
- **Geospatial search**: Search and filter by geographic location
- **AI-powered search**: Enhance search relevance with machine learning and generative AI
- **Multi-language support**: Search across content in multiple languages

### Analytics and insights

Transform raw data into actionable insights:
- **Real-time analytics**: Analyze data as it arrives
- **Aggregations**: Perform complex calculations and statistical analysis
- **Time-series analysis**: Track metrics and trends over time
- **Machine learning**: Detect anomalies and predict future trends
- **Data visualization**: Create dashboards and visualizations to understand your data

### Scalability and performance

Built to handle growth:
- **Horizontal scaling**: Add nodes to scale out as your data grows
- **Distributed architecture**: Automatically distribute data and queries across nodes
- **High availability**: Built-in replication and failover capabilities
- **Performance optimization**: Tune for your specific use case and workload

### Security and compliance

Protect your data and meet compliance requirements:
- **Authentication and authorization**: Control who can access your data
- **Encryption**: Encrypt data at rest and in transit
- **Audit logging**: Track all access and changes to your data
- **Compliance features**: Built-in capabilities to meet regulatory requirements

## Deployment options

Elastic offers flexible deployment options to meet your operational needs:

- **{{serverless-full}}**: Fully managed, serverless deployments that automatically scale with your needs
- **{{ech}}**: Managed service on Elastic Cloud with full control over configuration
- **Self-managed**: Deploy and manage Elastic on your own infrastructure

[Learn more about deployment options](/get-started/deployment-options.md)

## Use cases

Organizations use Elastic for a wide variety of use cases:

- **Enterprise search**: Build search experiences for internal knowledge bases, documentation, and content
- **E-commerce**: Power product search, recommendations, and personalization
- **Application monitoring**: Monitor application performance and troubleshoot issues
- **Security operations**: Detect and respond to security threats
- **Log management**: Centralize and analyze logs from across your infrastructure
- **Business intelligence**: Analyze business data and create dashboards
- **Content discovery**: Help users discover relevant content in applications
- **Fraud detection**: Identify fraudulent activity in real-time

## Getting started

Ready to get started with Elastic? Here are some recommended next steps:

1. **[Explore solutions](/solutions/index.md)**: Learn more about Elasticsearch, Observability, and Security solutions
2. **[Understand the Stack](/get-started/the-stack.md)**: Learn how Elastic components work together
3. **[Choose a deployment option](/get-started/deployment-options.md)**: Select the deployment approach that fits your needs
4. **[Try Elastic](https://www.elastic.co/cloud/elasticsearch-service/signup)**: Sign up for a free trial to explore Elastic Cloud

Whether you're building search experiences, monitoring your infrastructure, or securing your environment, Elastic provides the platform and solutions to help you succeed.


