---
mapped_pages:
  - https://www.elastic.co/guide/en/reference-architectures/current/reference-architectures-overview.html
  - https://www.elastic.co/guide/en/reference-architectures/current/index.html
applies_to:
  deployment:
    self: all
    ess: all
    ece: all
    eck: all
products:
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: cloud-hosted
---

# Reference architectures [reference-architectures-overview]

{{es}} reference architectures are blueprints for deploying {{es}} clusters tailored to different use cases. Whether you’re handling logs or metrics these reference architectures focus on scalability, reliability, and cost efficiency. Use these guidelines to deploy {{es}} for your use case.

These architectures are designed by architects and engineers to provide standardized, proven solutions that help you to follow best practices when deploying {{es}}.

::::{tip}
These architectures are specific to deploying Elastic on {{ech}}, {{eck}}, {{ece}}, or deploying a self-managed instance. If you are using {{serverless-full}}, your {{es}} clusters are autoscaled and fully managed by Elastic. To learn about all of the deployment options, refer to the [Deploy and manage overview](/deploy-manage/index.md).
::::


These reference architectures are recommendations and should be adapted to fit your specific environment and needs. Each solution can vary based on the unique requirements and conditions of your deployment. In these architectures we discuss about how to deploy cluster components. For information about designing ingest architectures to feed content into your cluster, refer to [Ingest architectures](../manage-data/ingest/ingest-reference-architectures.md).

## Architectures [reference-architectures-time-series]

| Architecture | When to use |
| --- | --- |
| [*Hot/Frozen - High Availability*](/deploy-manage/reference-architectures/hotfrozen-high-availability.md)<br>A high availability architecture that is cost optimized for large time-series datasets. | * Have a requirement for cost effective long term data storage (many months or years).<br>* Provide insights and alerts using logs, metrics, traces, or various event types to ensure optimal performance and quick issue resolution for applications.<br>* Apply Machine Learning and Search AI to assist in dealing with the large amount of data.<br>* Deploy an architecture model that allows for maximum flexibility between storage cost and performance.<br> |
| [*GenAI search - High Availability*](/deploy-manage/reference-architectures/genai-search-high-availability.md)<br>A high availability architecture that is performance-optimized for low-latency information retrieval using lexical, temporal, geospatial, and/or vector/semantic search, or a hybrid combination of each. | * Lexical, vector/semantic, temporal, geospatial, hybrid, and multi-modal search (text, audio, image, video).<br>* Generative AI applications such as assistants, agents, and agentic workflows using Retrieval Augmented Generation (RAG) and/or Model Context Protocol (MCP).<br>* Integrating with foundation models (Azure OpenAI, Anthropic, Amazon Bedrock, etc.) and re-ranking techniques for optimal relevance.<br>* Applications requiring low-latency time series analytics and natural language processing.<br>* Integration with common development frameworks for Large Language Models, including LlamaIndex, LangChain, and LangSmith.<br> |
| Additional architectures are on the way.<br>Stay tuned for updates. |  |



