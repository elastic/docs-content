---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-deploy-model.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Deploy the model in your cluster [ml-nlp-deploy-model]

After you import the model and vocabulary, you can use {{kib}} to view and manage their deployment across your cluster under **{{ml-app}}** > **Model Management**. Alternatively, you can use the [start trained model deployment API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-start-trained-model-deployment).

You can deploy a model multiple times by assigning a unique deployment ID when starting the deployment.

You can optimize your deplyoment for typical use cases, such as search and ingest. When you optimize for ingest, the throughput will be higher, which increases the number of {{infer}} requests that can be performed in parallel. When you optimize for search, the latency will be lower during search processes. When you have dedicated deployments for different purposes, you ensure that the search speed remains unaffected by ingest workloads, and vice versa. Having separate deployments for search and ingest mitigates performance issues resulting from interactions between the two, which can be hard to diagnose.

:::{image} /explore-analyze/images/ml-nlp-deployment-id-elser.png
:alt: Model deployment on the Trained Models UI.
:screenshot:
:::

Each deployment will be fine-tuned automatically based on its specific purpose you choose.

::::{note}
Since eland uses APIs to deploy the models, you cannot see the models in {{kib}} until the saved objects are synchronized. You can follow the prompts in {{kib}}, wait for automatic synchronization, or use the [sync {{ml}} saved objects API]({{kib-apis}}group/endpoint-ml).
::::

You can define the resource usage level of the NLP model during model deployment. The resource usage levels behave differently depending on [adaptive resources](../../../deploy-manage/autoscaling/trained-model-autoscaling.md#enabling-autoscaling-through-apis-adaptive-allocations) being enabled or disabled. When adaptive resources are disabled but {{ml}} autoscaling is enabled, vCPU usage of Cloud deployments derived from the Cloud console and functions as follows:

* Low: This level limits resources to two vCPUs, which may be suitable for development, testing, and demos depending on your parameters. It is not recommended for production use
* Medium: This level limits resources to 32 vCPUs, which may be suitable for development, testing, and demos depending on your parameters. It is not recommended for production use.
* High: This level may use the maximum number of vCPUs available for this deployment from the Cloud console. If the maximum is 2 vCPUs or fewer, this level is equivalent to the medium or low level.

For the resource levels when adaptive resources are enabled, refer to [Trained model autoscaling](../../../deploy-manage/autoscaling/trained-model-autoscaling.md).

## Request queues and search priority [infer-request-queues]

Each allocation of a model deployment has a dedicated queue to buffer {{infer}} requests. The size of this queue is determined by the `queue_capacity` parameter in the [start trained model deployment API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-start-trained-model-deployment). When the queue reaches its maximum capacity, new requests are declined until some of the queued requests are processed, creating available capacity once again. When multiple ingest pipelines reference the same deployment, the queue can fill up, resulting in rejected requests. Consider using dedicated deployments to prevent this situation.

{{infer-cap}} requests originating from search, such as the [`text_expansion` query](elasticsearch://reference/query-languages/query-dsl/query-dsl-text-expansion-query.md), have a higher priority compared to non-search requests. The {{infer}} ingest processor generates normal priority requests. If both a search query and an ingest processor use the same deployment, the search requests with higher priority skip ahead in the queue for processing before the lower priority ingest requests. This prioritization accelerates search responses while potentially slowing down ingest where response time is less critical.
