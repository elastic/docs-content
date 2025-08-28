---
navigation_title: Elasticsearch
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-billing.html
applies_to:
  serverless:
    elasticsearch: ga
products:
  - id: cloud-serverless
description: The cost of {{es-serverless}} projects is affected by the type and number of virtual compute units used.
---

# {{es}} billing dimensions [elasticsearch-billing]

{{es-serverless}} projects are priced based on consumption of the underlying infrastructure that supports your use case with the performance characteristics you need.
Measurements are in virtual compute units (VCUs).
Each VCU represents a fraction of RAM, CPU, and local disk for caching.

The number of VCUs you need is determined by:

* Volume and ingestion rate of your data
* Data retention requirements
* Search query volume
* Search Power setting
* Machine learning usage

The number of VCUs is also affected by your choice of configuration:

* The general purpose configuration is suitable for all standard search and vector workloads. It is performant and less expensive than the vector optimized configuration for most use cases.
* The optimized for vectors configuration provides great performance on vector search for uncompressed vectors with high dimensionality. However, it uses approximately four times more VCUs than the general purpose configuration.

For detailed {{es-serverless}} project rates, refer to the [{{es-serverless}} pricing page](https://www.elastic.co/pricing/serverless-search).

## VCU types: search, indexing, and ML [elasticsearch-billing-information-about-the-vcu-types-search-ingest-and-ml]

{{es-serverless}} uses three VCU types:

* **Indexing:** The VCUs used to index incoming documents. Indexing VCUs account for compute resources consumed for ingestion. This is based on ingestion rate and amount of data ingested at any given time. Transforms and ingest pipelines also contribute to ingest VCU consumption.
* **Search:** The VCUs used to return search results with the latency and queries per second (QPS) you require. Search VCUs are calculated as a factor of the compute resources needed to run search queries, search throughput, and latency. Search VCUs are not charged per search request. Instead, they are a factor of the compute resources that scale up and down based on amount of searchable data, search load (QPS), and performance (latency and availability).
* **Machine learning:** The VCUs used to perform inference, NLP tasks, and other ML activities. ML VCUs are a factor of the models deployed and number of ML operations such as inference for search and ingest. ML VCUs are typically consumed for generating embeddings during ingestion and during semantic search or reranking.
* **Tokens:** The Elastic Managed LLM is charged per 1 million input and output tokens. The LLM powers all AI Search features such as Playground and AI Assistant for Search and is enabled by default.

## Data storage and billing [elasticsearch-billing-information-about-the-search-ai-lake-dimension-gb]

{{es-serverless}} projects store data in the [Search AI Lake](/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-ai-lake-settings). You are charged per GB of stored data at rest. Note that if you perform operations at ingest such as vectorization or enrichment, the size of your stored data will differ from the size of the original source data.

## Managing {{es}} costs [elasticsearch-billing-managing-elasticsearch-costs]

You can control costs using the following strategies:

* **Search Power setting:** [Search Power](/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) controls the speed of searches against your data. With Search Power, you can improve search performance by adding more resources for querying or you can reduce provisioned resources to cut costs.
* **Search boost window**: By limiting the number of days of [time series data](/solutions/search/ingest-for-search.md#elasticsearch-ingest-time-series-data) that are available for caching, you can reduce the number of search VCUs required.
* **Machine learning trained model autoscaling:** [Trained model autoscaling](/deploy-manage/autoscaling/trained-model-autoscaling.md) is always enabled and cannot be disabled, ensuring efficient resource usage, reduced costs, and optimal performance without manual configuration.

  Trained model deployments automatically scale down to zero allocations after 24 hours without any inference requests. When they scale up again, they remain active for 5 minutes before they can scale down. During these cooldown periods, you will continue to be billed for the active resources.
* **Indexing strategies:** Consider your indexing strategies and how they might impact overall VCU usage and costs:
  
  * To ensure optimal performance and cost-effectiveness for your project, it's important to consider how you structure your data. Consolidate small indices for better efficiency. In general, avoid a design where your project contains hundreds of very small indices, specifically those under 1GB each.
  * Why is this important? Every index in {{es}} has a certain amount of resource overhead. This is because {{es}} needs to maintain metadata for each index to keep it running smoothly. When you have a very large number of small indices, the combined overhead from all of them can consume more CPU resources than if the same data were stored in fewer, larger indices. This can lead to higher resource consumption and hence higher costs and potentially impact the overall performance of your project.
  * If your use case naturally generates many small, separate streams of data, the recommended approach is to implement a process to consolidate them into fewer, larger indices. This practice leads to more efficient resource utilization. By grouping your data into larger indices, you can ensure a more performant and cost-efficient experience with {{es-serverless}}.
