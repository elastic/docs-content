---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-what-is-es.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/index.html
products:
  - id: elasticsearch
  - id: elastic-stack
---
# Get started

## Overview [what-is-es]

[{{es}}](https://github.com/elastic/elasticsearch) is a distributed search and analytics engine, scalable data store, and vector database built on Apache Lucene. It’s optimized for speed and relevance on production-scale workloads. Use {{es}} to search, index, store, and analyze data of all shapes and sizes in near real time. [{{kib}}](https://github.com/elastic/kibana) is the graphical user interface for {{es}}. It’s a powerful tool for visualizing and analyzing your data, and for managing and monitoring the Elastic Stack.

{{es}} is the heart of the [Elastic Stack](the-stack.md). Combined with {{kib}}, it powers these Elastic solutions and use cases:

* **[Elasticsearch](/solutions/search.md)**: Build powerful search and RAG applications using Elasticsearch's vector database, AI toolkit, and advanced retrieval capabilities.
* **[Observability](/solutions/observability.md)**: Resolve problems with open, flexible, and unified observability powered by advanced machine learning and analytics.
* **[Security](/solutions/security.md)**: Detect, investigate, and respond to threats with AI-driven security analytics to protect your organization at scale.

:::{tip}
Refer to our [customer success stories](https://www.elastic.co/customers/success-stories) for concrete examples of how Elastic is used in real-world scenarios.
:::

## Choose your deployment type

:::{include} /deploy-manage/_snippets/deployment-options-overview.md
:::

## Explore the solutions

Elasticsearch supports diverse use cases. Select a solution and follow its dedicated getting-started guide:

|     |     |
| :---: | --- |
| ![elasticsearch](images/64x64_Color_elasticsearch-logo-color-64px.png "elasticsearch =50%") | **Elasticsearch**<br> Create seamless search experiences for apps, websites, or workplaces.<br><br>[**Get started →**](../solutions/search/get-started.md)<br> |
| ![observability](images/64x64_Color_observability-logo-color-64px.png "observability =50%") | **Observability**<br> Monitor logs, metrics, and traces to gain insight into your systems.<br><br>[**Get started →**](../solutions/observability/get-started.md)<br> |
| ![security](images/64x64_Color_security-logo-color-64px.png "security =50%") | **Security**<br> Monitor logs, metrics, and traces to gain insight into your systems.<br><br>[**Get started →**](../solutions/security/get-started.md)<br> |

## Next steps

To learn more about our products and solutions, check out:

- [{{es}} and {{kib}}](introduction.md), the core components of the {{stack}}.
  - [The stack](/get-started/the-stack.md) to understand the relationship between core and optional components of an Elastic deployment.
- [The out-of-the-box solutions and use cases](/solutions/index.md) that Elastic supports.
- [Deploying Elastic](./deployment-options.md) for your use case.
- [Versioning and availability](./versioning-availability.md) in Elastic deployments.

