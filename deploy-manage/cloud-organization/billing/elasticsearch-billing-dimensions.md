---
navigation_title: Elasticsearch
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-billing.html
applies_to:
  serverless: all
products:
  - id: cloud-serverless
---

# {{es}} billing dimensions [elasticsearch-billing]

{{es}} is priced based on consumption of the underlying infrastructure that supports your use case, with the performance characteristics you need. Measurements are in Virtual Compute Units (VCUs). Each VCU represents a fraction of RAM, CPU, and local disk for caching.

The number of VCUs you need is determined by:

* Volume and ingestion rate of your data
* Data retention requirements
* Search query volume
* Search Power setting
* Machine learning usage

For detailed {{es-serverless}} project rates, see the [{{es-serverless}} pricing page](https://www.elastic.co/pricing/serverless-search).


## VCU types: Search, Indexing, and ML [elasticsearch-billing-information-about-the-vcu-types-search-ingest-and-ml]

{{es}} uses three VCU types:

* **Indexing:** The VCUs used to index incoming documents.
* **Search:** The VCUs used to return search results, with the latency and queries per second (QPS) you require.
* **Machine learning:** The VCUs used to perform inference, NLP tasks, and other ML activities.


## Data storage and billing [elasticsearch-billing-information-about-the-search-ai-lake-dimension-gb]

{{es-serverless}} projects store data in the [Search AI Lake](../../deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-ai-lake-settings). You are charged per GB of stored data at rest. Note that if you perform operations at ingest such as vectorization or enrichment, the size of your stored data will differ from the size of the original source data.


## Managing {{es}} costs [elasticsearch-billing-managing-elasticsearch-costs]

You can control costs using the following strategies:

* **Search Power setting:** [Search Power](../../deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) controls the speed of searches against your data. With Search Power, you can improve search performance by adding more resources for querying, or you can reduce provisioned resources to cut costs.
* **Search boost window**: By limiting the number of days of [time series data](../../../solutions/search/ingest-for-search.md#elasticsearch-ingest-time-series-data) that are available for caching, you can reduce the number of search VCUs required.
* **Machine learning trained model autoscaling:** Configure your trained model deployment to allow it to scale down to zero allocations when there are no active inference requests:

    * When starting or updating a trained model deployment, [Enable adaptive resources](../../autoscaling/trained-model-autoscaling.md#enabling-autoscaling-in-kibana-adaptive-resources) and set the VCU usage level to **Low**.
    * When using the inference API for {{es}} or ELSER, [enable `adaptive_allocations`](../../autoscaling/trained-model-autoscaling.md#enabling-autoscaling-through-apis-adaptive-allocations).
 
* **Indexing Strategies:** Consider your indexing strategies and how they might impact overall VCU usage and costs:
  
    * To ensure optimal performance and cost-effectiveness for your project, it’s important to consider how you structure your data.
        * Consolidate small indices for better efficiency. We recommend avoiding a design where your project contains hundreds of very small indices, specifically those under 1GB each.
    * Why is this important?
         * Every index in Elasticsearch has a certain amount of resource overhead. This is because Elasticsearch needs to maintain metadata for each index to keep it running smoothly. When you have a very large number of small indices, the combined               overhead from all of them can consume more CPU resources than if the same data were stored in fewer, larger indices. This can lead to higher resource consumption and hence higher costs and potentially impact the overall performance of your project.

    * Recommended Approach
        * If your use case naturally generates many small, separate streams of data, we advise implementing a process to consolidate them into fewer, larger indices. This practice leads to more efficient resource utilization. By grouping your data               into larger indices, you can ensure a more performant and cost-efficient experience with Elasticsearch Serverless.
