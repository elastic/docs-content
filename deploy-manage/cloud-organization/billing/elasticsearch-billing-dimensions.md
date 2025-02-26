---
navigation_title: "Elasticsearch"
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-billing.html
applies_to:
  serverless: all
---

# Elasticsearch billing dimensions [elasticsearch-billing]

Elasticsearch is priced based on consumption of the underlying infrastructure that supports your use case, with the performance characteristics you need. Measurements are in Virtual Compute Units (VCUs). Each VCU represents a fraction of RAM, CPU, and local disk for caching.

The number of VCUs you need is determined by:

* Volume and ingestion rate of your data
* Data retention requirements
* Search query volume
* Search Power setting
* Machine learning usage

For detailed {{es-serverless}} project rates, see the [{{es-serverless}} pricing page](https://www.elastic.co/pricing/serverless-search).


## VCU types: Search, Indexing, and ML [elasticsearch-billing-information-about-the-vcu-types-search-ingest-and-ml]

Elasticsearch uses three VCU types:

* **Indexing:** The VCUs used to index incoming documents.
* **Search:** The VCUs used to return search results, with the latency and queries per second (QPS) you require.
* **Machine learning:** The VCUs used to perform inference, NLP tasks, and other ML activities.


## Data storage and billing [elasticsearch-billing-information-about-the-search-ai-lake-dimension-gb]

{{es-serverless}} projects store data in the [Search AI Lake](../../deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-ai-lake-settings). You are charged per GB of stored data at rest. Note that if you perform operations at ingest such as vectorization or enrichment, the size of your stored data will differ from the size of the original source data.


## Managing {{es}} costs [elasticsearch-billing-managing-elasticsearch-costs]

You can control costs using the following strategies:

* **Search Power setting:** [Search Power](../../deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) controls the speed of searches against your data. With Search Power, you can improve search performance by adding more resources for querying, or you can reduce provisioned resources to cut costs.
* **Time series data retention:** By limiting the number of days of [time series data](../../../solutions/search/ingest-for-search.md#elasticsearch-ingest-time-series-data) that are available for caching, you can reduce the number of search VCUs required.
* **Machine learning trained model autoscaling:** Configure your trained model deployment to allow it to scale down to zero allocations when there are no active inference requests:

    * When starting or updating a trained model deployment, [Enable adaptive resources](../../autoscaling/trained-model-autoscaling.md#enabling-autoscaling-in-kibana-adaptive-resources) and set the VCU usage level to **Low**.
    * When using the inference API for Elasticsearch or ELSER, [enable `adaptive_allocations`](../../autoscaling/trained-model-autoscaling.md#enabling-autoscaling-through-apis-adaptive-allocations).
