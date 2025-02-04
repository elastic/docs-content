# Trained model autoscaling [general-ml-nlp-auto-scale]

This content applies to: [![Elasticsearch](../../../images/serverless-es-badge.svg "")](../../../solutions/search.md) [![Observability](../../../images/serverless-obs-badge.svg "")](../../../solutions/observability.md) [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md)

You can enable autoscaling for each of your trained model deployments. Autoscaling allows {{es}} to automatically adjust the resources the model deployment can use based on the workload demand.

There are two ways to enable autoscaling:

* through APIs by enabling adaptive allocations
* in Kibana by enabling adaptive resources

Trained model autoscaling is available for both serverless and Cloud deployments. In serverless deployments, processing power is managed differently across Search, Observability, and Security projects, which impacts their costs and resource limits.

Security and Observability projects are only charged for data ingestion and retention. They are not charged for processing power (VCU usage), which is used for more complex operations, like running advanced search models. For example, in Search projects, models such as ELSER require significant processing power to provide more accurate search results.


## Enabling autoscaling through APIs - adaptive allocations [enabling-autoscaling-through-apis-adaptive-allocations]

Model allocations are independent units of work for NLP tasks. If you set a static number of allocations, they remain constant even when not all the available resources are fully used or when the load on the model requires more resources. Instead of setting the number of allocations manually, you can enable adaptive allocations to set the number of allocations based on the load on the process. This can help you to manage performance and cost more easily. (Refer to the [pricing calculator](https://cloud.elastic.co/pricing) to learn more about the possible costs.)

When adaptive allocations are enabled, the number of allocations of the model is set automatically based on the current load. When the load is high, additional model allocations are automatically created as needed. When the load is low, a model allocation is automatically removed. You can explicitly set the minimum and maximum number of allocations; autoscaling will occur within these limits.

::::{note}
If you set the minimum number of allocations to 1, you will be charged even if the system is not using those resources.

::::


You can enable adaptive allocations by using:

* the create inference endpoint API for [ELSER](../../../solutions/search/inference-api/elser-inference-integration.md), [E5 and models uploaded through Eland](../../../solutions/search/inference-api/elasticsearch-inference-integration.md) that are used as inference services.
* the [start trained model deployment](https://www.elastic.co/guide/en/elasticsearch/reference/current/start-trained-model-deployment.html) or [update trained model deployment](https://www.elastic.co/guide/en/elasticsearch/reference/current/update-trained-model-deployment.html) APIs for trained models that are deployed on machine learning nodes.

If the new allocations fit on the current machine learning nodes, they are immediately started. If more resource capacity is needed for creating new model allocations, then your machine learning node will be scaled up if machine learning autoscaling is enabled to provide enough resources for the new allocation. The number of model allocations can be scaled down to 0. They cannot be scaled up to more than 32 allocations, unless you explicitly set the maximum number of allocations to more. Adaptive allocations must be set up independently for each deployment and [inference endpoint](https://www.elastic.co/guide/en/elasticsearch/reference/current/put-inference-api.html).

When you create inference endpoints on Serverless using Kibana, adaptive allocations are automatically turned on, and there is no option to disable them.


### Optimizing for typical use cases [optimizing-for-typical-use-cases]

You can optimize your model deployment for typical use cases, such as search and ingest. When you optimize for ingest, the throughput will be higher, which increases the number of inference requests that can be performed in parallel. When you optimize for search, the latency will be lower during search processes.

* If you want to optimize for ingest, set the number of threads to `1` (`"threads_per_allocation": 1`).
* If you want to optimize for search, set the number of threads to greater than `1`. Increasing the number of threads will make the search processes more performant.


## Enabling autoscaling in {{kib}} - adaptive resources [enabling-autoscaling-in-kibana-adaptive-resources]

You can enable adaptive resources for your models when starting or updating the model deployment. Adaptive resources make it possible for {{es}} to scale up or down the available resources based on the load on the process. This can help you to manage performance and cost more easily. When adaptive resources are enabled, the number of VCUs that the model deployment uses is set automatically based on the current load. When the load is high, the number of VCUs that the process can use is automatically increased. When the load is low, the number of VCUs that the process can use is automatically decreased.

You can choose from three levels of resource usage for your trained model deployment; autoscaling will occur within the selected level’s range.

Refer to the tables in the auto-scaling-matrix section to find out the settings for the level you selected.

:::{image} ../../../images/serverless-ml-nlp-deployment.png
:alt: ML model deployment with adaptive resources enabled.
:::

Search projects are given access to more processing resources, while Security and Observability projects have lower limits. This difference is reflected in the UI configuration: Search projects have higher resource limits compared to Security and Observability projects to accommodate their more complex operations.

On Serverless, adaptive allocations are automatically enabled for all project types. However, the "Adaptive resources" control is not displayed in Kibana for Observability and Security projects.


## Model deployment resource matrix [model-deployment-resource-matrix]

The used resources for trained model deployments depend on three factors:

* your cluster environment (Serverless, Cloud, or on-premises)
* the use case you optimize the model deployment for (ingest or search)
* whether model autoscaling is enabled with adaptive allocations/resources to have dynamic resources, or disabled for static resources

The following tables show you the number of allocations, threads, and VCUs available on Serverless when adaptive resources are enabled or disabled.


### Deployments on serverless optimized for ingest [deployments-on-serverless-optimized-for-ingest]

In case of ingest-optimized deployments, we maximize the number of model allocations.


#### Adaptive resources enabled [adaptive-resources-enabled]

| Level | Allocations | Threads | VCUs |
| --- | --- | --- | --- |
| Low | 0 to 2 dynamically | 1 | 0 to 16 dynamically |
| Medium | 1 to 32 dynamically | 1 | 8 to 256 dynamically |
| High | 1 to 512 for Search<br> 1 to 128 for Security and Observability<br> | 1 | 8 to 4096 for Search<br> 8 to 1024 for Security and Observability<br> |


#### Adaptive resources disabled (Search only) [adaptive-resources-disabled-search-only]

| Level | Allocations | Threads | VCUs |
| --- | --- | --- | --- |
| Low | Exactly 2 | 1 | 16 |
| Medium | Exactly 32 | 1 | 256 |
| High | 512 for Search<br> No static allocations for Security and Observability<br> | 1 | 4096 for Search<br> No static allocations for Security and Observability<br> |


### Deployments on serverless optimized for Search [deployments-on-serverless-optimized-for-search]


#### Adaptive resources enabled [adaptive-resources-enabled-for-search]

| Level | Allocations | Threads | VCUs |
| --- | --- | --- | --- |
| Low | 0 to 1 dynamically | Always 2 | 0 to 16 dynamically |
| Medium | 1 to 2 (if threads=16), dynamically | Maximum (for example, 16) | 8 to 256 dynamically |
| High | 1 to 32 (if threads=16), dynamically<br> 1 to 128 for Security and Observability<br> | Maximum (for example, 16) | 8 to 4096 for Search<br> 8 to 1024 for Security and Observability<br> |


#### Adaptive resources disabled [adaptive-resources-disabled-for-search]

| Level | Allocations | Threads | VCUs |
| --- | --- | --- | --- |
| Low | 1 statically | Always 2 | 16 |
| Medium | 2 statically (if threads=16) | Maximum (for example, 16) | 256 |
| High | 32 statically (if threads=16) for Search<br> No static allocations for Security and Observability<br> | Maximum (for example, 16) | 4096 for Search<br> No static allocations for Security and Observability<br> |

