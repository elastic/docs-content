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
These architectures are specific to deploying Elastic on {{ech}}, {{eck}}, {{ece}}, or deploying a self-managed instance. If you are using {{serverless-full}}, your {{es}} clusters are autoscaled and fully managed by Elastic. To learn about all of the deployment options, refer to the [Deploy and manage overview](/deploy-manage/index.md).
::::


These reference architectures are recommendations and should be adapted to fit your specific environment and needs. Each solution can vary based on the unique requirements and conditions of your deployment. In these architectures we discuss about how to deploy cluster components. For information about designing ingest architectures to feed content into your cluster, refer to [Ingest architectures](../manage-data/ingest/ingest-reference-architectures/use-case-arch.md)

## Architectures [reference-architectures-time-series] 

|     |     |
| --- | --- |
| **Architecture** | **When to use** |
| [*Hot/Frozen - High Availability*](/deploy-manage/reference-architectures/hotfrozen-high-availability.md)<br>A high availability architecture that is cost optimized for large time-series datasets. | * Have a requirement for cost effective long term data storage (many months or years).<br>* Provide insights and alerts using logs, metrics, traces, or various event types to ensure optimal performance and quick issue resolution for applications.<br>* Apply Machine Learning and Search AI to assist in dealing with the large amount of data.<br>* Deploy an architecture model that allows for maximum flexibility between storage cost and performance.<br> |
| Additional architectures are on the way.<br>Stay tuned for updates. |  |



