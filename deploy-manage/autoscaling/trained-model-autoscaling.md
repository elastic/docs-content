---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/general-ml-nlp-auto-scale.html
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-auto-scale.html
applies_to:
  deployment:
    ess:
    eck:
    ece:
  serverless:
products:
  - id: cloud-serverless
  - id: machine-learning
---

# Trained model autoscaling

You can enable autoscaling for each of your trained model deployments. Autoscaling allows {{es}} to automatically adjust the resources the model deployment can use based on the workload demand.

There are two ways to enable autoscaling:

* through APIs by enabling adaptive allocations
* in {{kib}} by enabling adaptive resources

For {{serverless-short}} projects, trained model autoscaling is always enabled and cannot be turned off. 

::::{important}
To fully leverage model autoscaling in {{ech}}, {{ece}}, and {{eck}}, it is highly recommended to enable [{{es}} deployment autoscaling](../../deploy-manage/autoscaling.md).
::::

Trained model autoscaling is available for {{serverless-short}}, {{ech}}, {{ece}}, and {{eck}} deployments. In {{serverless-short}} projects, processing power is managed differently across Search, Observability, and Security projects, which impacts their costs and resource limits.

:::{admonition} Trained model auto-scaling for self-managed deployments
The available resources of self-managed deployments are static, so trained model autoscaling is not applicable. However, available resources are still segmented based on the settings described in this section.
:::

{{serverless-full}} Security and Observability projects are only charged for data ingestion and retention. They are not charged for processing power (VCU usage), which is used for more complex operations, like running advanced search models. For example, in Search projects, models such as ELSER require significant processing power to provide more accurate search results.

## Cooldown periods [cooldown-periods]

Trained model deployments remain active for 24 hours after the last inference request. After that, they scale down to zero. When scaled up again, they stay active for 5 minutes before they can scale down. These cooldown periods prevent unnecessary scaling and ensure models are available when needed.

::::{important}
During these cooldown periods, you will continue to be billed for the active resources.
::::

For {{ech}}, {{eck}} and {{ece}} deployments, you can change the length of this period with the `xpack.ml.trained_models.adaptive_allocations.scale_to_zero_time` cluster setting (minimum 1 minute). For {{serverless-short}} projects, this period is fixed and cannot be changed.

## Enabling autoscaling through APIs - adaptive allocations [enabling-autoscaling-through-apis-adaptive-allocations]

$$$nlp-model-adaptive-resources$$$

Model allocations are independent units of work for NLP tasks. If you set the numbers of threads and allocations for a model manually, they remain constant even when not all the available resources are fully used or when the load on the model requires more resources. Instead of setting the number of allocations manually, you can enable adaptive allocations to set the number of allocations based on the load on the process. This can help you to manage performance and cost more easily. (Refer to the [pricing calculator](https://cloud.elastic.co/pricing) to learn more about the possible costs.)

When adaptive allocations are enabled, the number of allocations of the model is set automatically based on the current load. When the load is high, a new model allocation is automatically created. When the load is low, a model allocation is automatically removed. You can explicitly set the minimum and maximum number of allocations; autoscaling will occur within these limits.

::::{note}
If you set the minimum number of allocations to 1, you will be charged even if the system is not using those resources.

::::

You can enable adaptive allocations by using:

* the create inference endpoint API for [ELSER](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put-elser), [E5 and models uploaded through Eland](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put-elasticsearch) that are used as inference services.
* the [start trained model deployment](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-start-trained-model-deployment) or [update trained model deployment](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-update-trained-model-deployment) APIs for trained models that are deployed on {{ml}} nodes.

If the new allocations fit on the current {{ml}} nodes, they are immediately started. If more resource capacity is needed for creating new model allocations, then your {{ml}} node will be scaled up if {{ml}} autoscaling is enabled to provide enough resources for the new allocation. The number of model allocations can be scaled down to 0. They cannot be scaled up to more than 32 allocations, unless you explicitly set the maximum number of allocations to more. Adaptive allocations must be set up independently for each deployment and [{{infer}} endpoint](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference).

### Optimizing for typical use cases [optimizing-for-typical-use-cases]

You can optimize your model deployment for typical use cases, such as search and ingest. When you optimize for ingest, the throughput will be higher, which increases the number of {{infer}} requests that can be performed in parallel. When you optimize for search, the latency will be lower during search processes.

* If you want to optimize for ingest, set the number of threads to `1` (`"threads_per_allocation": 1`).
* If you want to optimize for search, set the number of threads to greater than `1`. Increasing the number of threads will make the search processes more performant.

## Enabling autoscaling in {{kib}} - adaptive resources [enabling-autoscaling-in-kibana-adaptive-resources]

You can enable adaptive resources for your models when starting or updating the model deployment. Adaptive resources make it possible for {{es}} to scale up or down the available resources based on the load on the process. This can help you to manage performance and cost more easily. When adaptive resources are enabled, the number of vCPUs that the model deployment uses is set automatically based on the current load. When the load is high, the number of vCPUs that the process can use is automatically increased. When the load is low, the number of vCPUs that the process can use is automatically decreased.

You can choose from three levels of resource usage for your trained model deployment; autoscaling will occur within the selected level’s range.

Refer to the tables in the [Model deployment resource matrix](#model-deployment-resource-matrix) section to find out the settings for the level you selected.

The image below shows the process of starting a trained model on an {{ech}} deployment. In {{serverless-short}} projects, the **Adaptive resources** toggle is not available when starting trained model deployments, as adaptive allocations are always enabled and cannot be disabled.

:::{image} /deploy-manage/images/ml-nlp-deployment-id-elser.png
:alt: ELSER deployment with adaptive resources enabled.
:screenshot:
:width: 500px
:::

In {{serverless-full}}, Search projects are given access to more processing resources, while Security and Observability projects have lower limits. This difference is reflected in the UI configuration: Search projects have higher resource limits compared to Security and Observability projects to accommodate their more complex operations.

## Model deployment resource matrix [model-deployment-resource-matrix]

The used resources for trained model deployments depend on three factors:

* your cluster environment ({{serverless-short}}, Cloud (ECE, ECK, ECH), or self-managed)
* the use case you optimize the model deployment for (ingest or search)
* whether model autoscaling is enabled with adaptive allocations/resources to have dynamic resources, or disabled for static resources

::::{note}
On {{serverless-short}}, VCUs for {{ml}} are based on the amount of vCPU and memory consumed. For {{ml}}, `1` VCU equals `0.125` of vCPU and `1GB` of memory, where vCPUs are measured by allocations multiplied by threads, and where memory is the amount consumed by trained models or {{ml}} jobs.
As a math formula, `VCUs = 8 * allocations * threads`, or `1` VCU for every `1GB` of memory consumed, whichever is greater.
::::

If you use a self-managed cluster or ECK, vCPUs level ranges are derived from the `total_ml_processors` and `max_single_ml_node_processors` values. Use the [get {{ml}} info API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-info) to check these values.

The following tables show you the number of allocations, threads, and vCPUs available in ECE and ECH when adaptive resources are enabled or disabled.

### Ingest optimized

In case of ingest-optimized deployments, we maximize the number of model allocations.

#### Adaptive resources enabled

::::{applies-switch}

:::{applies-item} { "ess":, "ece": }

| Level | Allocations | Threads | vCPUs |
| --- | --- | --- | --- |
| Low | 0 to 2 if available, dynamically | 1 | 0 to 2 if available, dynamically |
| Medium | 1 to 32 dynamically | 1 | 1 to the smaller of 32 or the limit set in the Cloud console, dynamically |
| High | 1 to limit set in the Cloud console *, dynamically | 1 | 1 to limit set in the Cloud console, dynamically |

\* The Cloud console doesn’t directly set an allocations limit; it only sets a vCPU limit. This vCPU limit indirectly determines the number of allocations, calculated as the vCPU limit divided by the number of threads.

:::

:::{applies-item} serverless:

| Level | Allocations | Threads | VCUs |
| --- | --- | --- | --- |
| Low | 0 to 2 dynamically | 1 | 0 to 16 dynamically |
| Medium | 0 to 32 dynamically | 1 | 8 to 256 dynamically |
| High | 0 to 512 for Search<br> 1 to 128 for Security and Observability<br> | 1 | 8 to 4096 for Search<br> 8 to 1024 for Security and Observability<br> |

:::

::::

#### Adaptive resources disabled

::::{applies-switch}

:::{applies-item} { "ess":, "ece": }

| Level | Allocations | Threads | vCPUs |
| --- | --- | --- | --- |
| Low | 2 if available, otherwise 1, statically | 1 | 2 if available |
| Medium | the smaller of 32 or the limit set in the Cloud console, statically | 1 | 32 if available |
| High | Maximum available set in the  Cloud console *, statically | 1 | Maximum available set in the Cloud console, statically |

\* The Cloud console doesn’t directly set an allocations limit; it only sets a vCPU limit. This vCPU limit indirectly determines the number of allocations, calculated as the vCPU limit divided by the number of threads.

:::

::::

### Search optimized

In case of search-optimized deployments, we maximize the number of threads. The maximum number of threads that can be claimed depends on the hardware your architecture has.

#### Adaptive resources enabled

::::{applies-switch}

:::{applies-item} { "ess":, "ece": }

| Level | Allocations | Threads | vCPUs |
| --- | --- | --- | --- |
| Low | 1 | 2 | 2 |
| Medium | 1 to 2 (if threads=16) dynamically | maximum that the hardware allows (for example, 16) | 1 to 32 dynamically |
| High | 1 to limit set in the Cloud console *, dynamically | maximum that the hardware allows (for example, 16) | 1 to limit set in the Cloud console, dynamically |

\* The Cloud console doesn’t directly set an allocations limit; it only sets a vCPU limit. This vCPU limit indirectly determines the number of allocations, calculated as the vCPU limit divided by the number of threads.

:::

:::{applies-item} serverless:

| Level | Allocations | Threads | VCUs |
| --- | --- | --- | --- |
| Low | 0 to 1 dynamically | 2 | 0 to 16 dynamically |
| Medium | 0 to 2 dynamically for Search and Observatibility<br> 1 to 2 dynamically for Security | 4 | 0 to 256 dynamically for Search and Observatibility<br> 8 to 256 dynamically for Security |
| High | 0 to 32 dynamically for Search and Observatibility<br> 1 to 128 dynamically for Security<br> | 8 | 0 to 4096 dynamically for Search<br> 0 to 1024 dynamically for Observability<br>8 to 1014 dynamically for Security |

:::

::::

#### Adaptive resources disabled

::::{applies-switch}

:::{applies-item} { "ess":, "ece": }

| Level | Allocations | Threads | vCPUs |
| --- | --- | --- | --- |
| Low | 1 if available, statically | 2 | 2 if available |
| Medium | 2 (if threads=16) statically | maximum that the hardware allows (for example, 16) | 32 if available |
| High | Maximum available set in the Cloud console *, statically | maximum that the hardware allows (for example, 16) | Maximum available set in the Cloud console, statically |

\* The Cloud console doesn’t directly set an allocations limit; it only sets a vCPU limit. This vCPU limit indirectly determines the number of allocations, calculated as the vCPU limit divided by the number of threads.

:::

::::
