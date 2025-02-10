---
mapped_pages:
  - https://www.elastic.co/guide/en/reference-architectures/current/reference-architectures-overview.html
applies:
  stack: all
  hosted: all
  ece: all
  eck: all
---

# Reference architectures [reference-architectures-overview]

Elasticsearch reference architectures are blueprints for deploying Elasticsearch clusters tailored to different use cases. Whether you’re handling logs or metrics these reference architectures focus on scalability, reliability, and cost efficiency. Use these guidelines to deploy Elasticsearch for your use case.

These architectures are designed by architects and engineers to provide standardized, proven solutions that help you to follow best practices when deploying {{es}}.

::::{tip} 
These architectures are specific to running your deployment on-premises or on cloud. If you are using Elastic serverless your {{es}} clusters are autoscaled and fully managed by Elastic. For all the deployment options, refer to [Run Elasticsearch](deploy.md).
::::


These reference architectures are recommendations and should be adapted to fit your specific environment and needs. Each solution can vary based on the unique requirements and conditions of your deployment. In these architectures we discuss about how to deploy cluster components. For information about designing ingest architectures to feed content into your cluster, refer to [Ingest architectures](../manage-data/ingest/ingest-reference-architectures/use-case-arch.md)


## Architectures [reference-architectures-time-series] 

|     |     |
| --- | --- |
| **Architecture** | **When to use** |
| [*Hot/Frozen - High Availability*](reference-architectures/hotfrozen-high-availability.md)<br>A high availability architecture that is cost optimized for large time-series datasets. | <ul><li> Have a requirement for cost effective long term data storage (many months or years).</li><li> Provide insights and alerts using logs, metrics, traces, or various event types to ensure optimal performance and quick issue resolution for applications.</li><li> Apply Machine Learning and Search AI to assist in dealing with the large amount of data.</li><li> Deploy an architecture model that allows for maximum flexibility between storage cost and performance.</li></ul> |
| Additional architectures are on the way.<br>Stay tuned for updates. |  |

