---
mapped_pages:
  - https://www.elastic.co/guide/en/reference-architectures/current/reference-architectures-overview.html
---

# Reference architectures [reference-architectures-overview]

Elasticsearch reference architectures are blueprints for deploying Elasticsearch clusters tailored to different use cases. Whether you’re handling logs or metrics these reference architectures focus on scalability, reliability, and cost efficiency. Use these guidelines to deploy Elasticsearch for your use case.

These architectures are designed by architects and engineers to provide standardized, proven solutions that help you to follow best practices when deploying {{es}}.

::::{tip}
These architectures are specific to running your deployment on-premises or on cloud. If you are using Elastic serverless your {{es}} clusters are autoscaled and fully managed by Elastic. For all the deployment options, refer to [Run Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-deploy.html).
::::


These reference architectures are recommendations and should be adapted to fit your specific environment and needs. Each solution can vary based on the unique requirements and conditions of your deployment. In these architectures we discuss about how to deploy cluster components. For information about designing ingest architectures to feed content into your cluster, refer to [Ingest architectures](https://www.elastic.co/guide/en/ingest/current/use-case-arch.html)


## Architectures [reference-architectures-time-series-2]

|     |     |
| --- | --- |
| **Architecture** | **When to use** |
| [*Hot/Frozen - High Availability*](https://www.elastic.co/guide/en/reference-architectures/current/hot-frozen-architecture.html)<br>A high availability architecture that is cost optimized for large time-series datasets. | * Have a requirement for cost effective long term data storage (many months or years).<br>* Provide insights and alerts using logs, metrics, traces, or various event types to ensure optimal performance and quick issue resolution for applications.<br>* Apply Machine Learning and Search AI to assist in dealing with the large amount of data.<br>* Deploy an architecture model that allows for maximum flexibility between storage cost and performance.<br> |
| Additional architectures are on the way.<br>Stay tuned for updates. |  |

