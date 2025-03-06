---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-auto-scale.html
---

# Trained model autoscaling [ml-nlp-auto-scale]

You can enable autoscaling for each of your trained model deployments. Autoscaling allows {{es}} to automatically adjust the resources the model deployment can use based on the workload demand.

There are two ways to enable autoscaling:

* through APIs by enabling adaptive allocations
* in {{kib}} by enabling adaptive resources

::::{important}
To fully leverage model autoscaling, it is highly recommended to enable [{{es}} deployment autoscaling](../../../deploy-manage/autoscaling.md).
::::

## Enabling autoscaling through APIs - adaptive allocations [nlp-model-adaptive-allocations]

Model allocations are independent units of work for NLP tasks. If you set the numbers of threads and allocations for a model manually, they remain constant even when not all the available resources are fully used or when the load on the model requires more resources. Instead of setting the number of allocations manually, you can enable adaptive allocations to set the number of allocations based on the load on the process. This can help you to manage performance and cost more easily. (Refer to the [pricing calculator](https://cloud.elastic.co/pricing) to learn more about the possible costs.)

When adaptive allocations are enabled, the number of allocations of the model is set automatically based on the current load. When the load is high, a new model allocation is automatically created. When the load is low, a model allocation is automatically removed. You can explicitely set the minimum and maximum number of allocations; autoscaling will occur within these limits.

You can enable adaptive allocations by using:

* the create inference endpoint API for [ELSER](../../elastic-inference/inference-api/elser-inference-integration.md), [E5 and models uploaded through Eland](../../elastic-inference/inference-api/elasticsearch-inference-integration.md) that are used as {{infer}} services.
* the [start trained model deployment](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-start-trained-model-deployment) or [update trained model deployment](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-update-trained-model-deployment) APIs for trained models that are deployed on {{ml}} nodes.

If the new allocations fit on the current {{ml}} nodes, they are immediately started. If more resource capacity is needed for creating new model allocations, then your {{ml}} node will be scaled up if {{ml}} autoscaling is enabled to provide enough resources for the new allocation. The number of model allocations can be scaled down to 0. They cannot be scaled up to more than 32 allocations, unless you explicitly set the maximum number of allocations to more. Adaptive allocations must be set up independently for each deployment and [{{infer}} endpoint](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference).

### Optimizing for typical use cases [optimize-use-case]

You can optimize your model deployment for typical use cases, such as search and ingest. When you optimize for ingest, the throughput will be higher, which increases the number of {{infer}} requests that can be performed in parallel. When you optimize for search, the latency will be lower during search processes.

* If you want to optimize for ingest, set the number of threads to `1` (`"threads_per_allocation": 1`).
* If you want to optimize for search, set the number of threads to greater than `1`. Increasing the number of threads will make the search processes more performant.

## Enabling autoscaling in {{kib}} - adaptive resources [nlp-model-adaptive-resources]

You can enable adaptive resources for your models when starting or updating the model deployment. Adaptive resources make it possible for {{es}} to scale up or down the available resources based on the load on the process. This can help you to manage performance and cost more easily. When adaptive resources are enabled, the number of vCPUs that the model deployment uses is set automatically based on the current load. When the load is high, the number of vCPUs that the process can use is automatically increased. When the load is low, the number of vCPUs that the process can use is automatically decreased.

You can choose from three levels of resource usage for your trained model deployment; autoscaling will occur within the selected level’s range.

Refer to the tables in the [Model deployment resource matrix](#auto-scaling-matrix) section to find out the setings for the level you selected.

:::{image} ../../../images/machine-learning-ml-nlp-deployment-id-elser-v2.png
:alt: ELSER deployment with adaptive resources enabled.
:class: screenshot
:::

## Model deployment resource matrix [auto-scaling-matrix]

The used resources for trained model deployments depend on three factors:

* your cluster environment (Serverless, Cloud, or on-premises)
* the use case you optimize the model deployment for (ingest or search)
* whether model autoscaling is enabled with adaptive allocations/resources to have dynamic resources, or disabled for static resources

If you use {{es}} on-premises, vCPUs level ranges are derived from the `total_ml_processors` and `max_single_ml_node_processors` values. Use the [get {{ml}} info API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-info) to check these values. The following tables show you the number of allocations, threads, and vCPUs available in Cloud when adaptive resources are enabled or disabled.

::::{note}
On Serverless, adaptive allocations are automatically enabled for all project types. However, the "Adaptive resources" control is not displayed in {{kib}} for Observability and Security projects.
::::

### Deployments in Cloud optimized for ingest [_deployments_in_cloud_optimized_for_ingest]

In case of ingest-optimized deployments, we maximize the number of model allocations.

#### Adaptive resources enabled [_adaptive_resources_enabled]

| Level | Allocations | Threads | vCPUs |
| --- | --- | --- | --- |
| Low | 0 to 2 if available, dynamically | 1 | 0 to 2 if available, dynamically |
| Medium | 1 to 32 dynamically | 1 | 1 to the smaller of 32 or the limit set in the Cloud console, dynamically |
| High | 1 to limit set in the Cloud console *, dynamically | 1 | 1 to limit set in the Cloud console, dynamically |

* The Cloud console doesn’t directly set an allocations limit; it only sets a vCPU limit. This vCPU limit indirectly determines the number of allocations, calculated as the vCPU limit divided by the number of threads.

#### Adaptive resources disabled [_adaptive_resources_disabled]

| Level | Allocations | Threads | vCPUs |
| --- | --- | --- | --- |
| Low | 2 if available, otherwise 1, statically | 1 | 2 if available |
| Medium | the smaller of 32 or the limit set in the Cloud console, statically | 1 | 32 if available |
| High | Maximum available set in the  Cloud console *, statically | 1 | Maximum available set in the Cloud console, statically |

* The Cloud console doesn’t directly set an allocations limit; it only sets a vCPU limit. This vCPU limit indirectly determines the number of allocations, calculated as the vCPU limit divided by the number of threads.

### Deployments in Cloud optimized for search [_deployments_in_cloud_optimized_for_search]

In case of search-optimized deployments, we maximize the number of threads. The maximum number of threads that can be claimed depends on the hardware your architecture has.

#### Adaptive resources enabled [_adaptive_resources_enabled_2]

| Level | Allocations | Threads | vCPUs |
| --- | --- | --- | --- |
| Low | 1 | 2 | 2 |
| Medium | 1 to 2 (if threads=16) dynamically | maximum that the hardware allows (for example, 16) | 1 to 32 dynamically |
| High | 1 to limit set in the Cloud console *, dynamically | maximum that the hardware allows (for example, 16) | 1 to limit set in the Cloud console, dynamically |

* The Cloud console doesn’t directly set an allocations limit; it only sets a vCPU limit. This vCPU limit indirectly determines the number of allocations, calculated as the vCPU limit divided by the number of threads.

#### Adaptive resources disabled [_adaptive_resources_disabled_2]

| Level | Allocations | Threads | vCPUs |
| --- | --- | --- | --- |
| Low | 1 if available, statically | 2 | 2 if available |
| Medium | 2 (if threads=16) statically | maximum that the hardware allows (for example, 16) | 32 if available |
| High | Maximum available set in the Cloud console *, statically | maximum that the hardware allows (for example, 16) | Maximum available set in the Cloud console, statically |

\* The Cloud console doesn’t directly set an allocations limit; it only sets a vCPU limit. This vCPU limit indirectly determines the number of allocations, calculated as the vCPU limit divided by the number of threads.
