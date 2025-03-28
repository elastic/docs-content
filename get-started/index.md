---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-what-is-es.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/index.html
---
# Get started

## Overview

[{{es}}](https://github.com/elastic/elasticsearch) is a distributed search and analytics engine, scalable data store, and vector database built on Apache Lucene. It’s optimized for speed and relevance on production-scale workloads. Use {{es}} to search, index, store, and analyze data of all shapes and sizes in near real time. [{{kib}}](https://github.com/elastic/kibana) is the graphical user interface for {{es}}. It’s a powerful tool for visualizing and analyzing your data, and for managing and monitoring the Elastic Stack. 

{{es}} is the heart of the [Elastic Stack](the-stack.md). Combined with {{kib}}, it powers these Elastic solutions and use cases:

* **[Observability](/solutions/observability.md)**: Resolve problems with open, flexible, and unified observability powered by advanced machine learning and analytics.
* **[Security](/solutions/security.md)**: Detect, investigate, and respond to threats with AI-driven security analytics to protect your organization at scale.
* **[Search](/solutions/search.md)**: Build powerful search and RAG applications using Elasticsearch's vector database, AI toolkit, and advanced retrieval capabilities.

:::{tip}
Refer to our [customer success stories](https://www.elastic.co/customers/success-stories) for concrete examples of how Elastic is used in real-world scenarios.
:::

## Step 1: Choose your deployment type

Elasticsearch provides multiple deployment options:

1. **Elastic Cloud**: Fully managed Elasticsearch service, hassle-free with automatic updates. Ideal for those seeking scalability and ease of use. [Learn more about Elastic Cloud](../deploy-manage/deploy/elastic-cloud.md).  
   **Get started**: [Sign up here](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
2. **Serverless**: A deployment option designed for flexibility and efficiency, allowing you to scale resources automatically without worrying about infrastructure. Perfect for unpredictable workloads. [Learn more about Elasticsearch Serverless](../deploy-manage/deploy/elastic-cloud/serverless.md).  
   **Get started**: [Sign up here](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
3. **Self-Managed**: Deploy Elasticsearch on-premise or on your infrastructure. Ideal for those who prefer complete control. [Learn about self-managed deployment](https://www.elastic.co/downloads/elasticsearch).  
   **Get started**: [Download Elasticsearch here](../deploy-manage/deploy/self-managed/local-development-installation-quickstart.md).

## Step 2: Explore the solutions

Elasticsearch supports diverse use cases. Select a solution and follow its dedicated getting-started guide:

1. **Search**: Create seamless search experiences for apps, websites, or workplaces. [Get started with Search](../solutions/search/get-started.md).
2. **Observability**: Monitor logs, metrics, and traces to gain insight into your systems. [Get started with Observability](../solutions/observability/get-started.md).
3. **Security**: Detect and respond to threats with real-time analytics. [Get started with Security](../solutions/security/get-started.md).

## Next steps

For learn more about our products and solutions, see:

- [{{es}} and {{kib}}](introduction.md), the core components of the {{stack}}.
  - [The stack](/get-started/the-stack.md) to understand the relationship between core and optional components of an Elastic deployment.
- [The out-of-the-box solutions and use cases](/solutions/index.md) that Elastic supports.
- [Deploying Elastic](./deployment-options.md) for your use case.
- [Versioning and availability](./versioning-availability.md) in Elastic deployments.

