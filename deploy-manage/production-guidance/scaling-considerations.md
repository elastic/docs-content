---
navigation_title: Scaling considerations
applies_to:
  deployment:
    eck: all
    ess: all
    ece: all
    self: all
---

# {{es}} scaling considerations

Knowing when and how to scale your deployment is critical, especially when unexpected workloads hits. Adding more nodes or adjusting resources is not always the best solution—scaling should be based on real workload patterns and informed decision-making.

In orchestrated or managed deployments, [Autoscaling](/deploy-manage/autoscaling.md) can automatically adjust cluster resources based on demand, reducing operational overhead. However, in self-managed environments, scaling is a manual process, requiring careful planning to adapt to workload changes and ensure the cluster remains performant and resilient.

Refer to [Sizing {{es}}: Scaling up and out](https://www.elastic.co/blog/found-sizing-elasticsearch) to identify which questions to ask yourself when determining which cluster size is the best fit for your {{es}} use case.

## Monitoring and scaling decisions

To make informed scaling decisions, [cluster monitoring](/deploy-manage/monitor.md) is essential. Metrics such as CPU usage, memory pressure, disk I/O, query response times, and shard distribution provide insights into when scaling may be necessary.

## Performance optimizations and scaling

Scaling isn’t just about adding more nodes—it also involves [optimizing the cluster configuration for better performance](./production-guidance/optimize-performance.md). Adjustments such as shard and index tuning, query optimizations, caching strategies, and efficient resource allocation can improve performance without requiring additional hardware. These optimizations directly influence scaling strategies, as a well-tuned cluster can handle more workload with fewer resources.

## Scaling and fault tolerance

When adding zones for fault tolerance or high availability, it might seem like you’re also scaling up. While additional zones might improve the performance, they should not be relied upon for additional capacity.

In {{ech}} and {{ece}}, the concept of zones is intended for:
* High Availability (2 zones)
* Fault Tolerance (3 zones)

Neither will work if the cluster relies on the resources from those zones to be operational.

The recommendation is to scale up the resources within a single zone until the cluster can take the full load (add some buffer to be prepared for a peak of requests), then scale out by adding additional zones depending on your requirements: 2 zones for High Availability, 3 zones for Fault Tolerance.

::::{note}
This is a general recommendation, but you are free to design your cluster in a way that best supports your high availability (HA) requirements. Just ensure you fully understand the implications of your choices and plan accordingly.
::::

## How to scale

Refer to the following documents depending on your deployment type:

* [](/deploy-manage/autoscaling.md): Autoscaling is available for {{ech}}, {{ece}} and {{eck}} deployments. Autoscaling on ECK requires an enterprise license.
* [Configure {{ech}} deployments](/deploy-manage/deploy/elastic-cloud/configure.md): You can change your deployment resources or even the [hardware profile](/deploy-manage/deploy/elastic-cloud/ec-change-hardware-profile.md) of your instances.
* [Resize an ECE deployment](/deploy-manage/deploy/cloud-enterprise/resize-deployment.md)
* [Configure ECK deployments](/deploy-manage/deploy/cloud-on-k8s/configure-deployments.md): Change the amount of instances of any component, or [customize compute resources](/deploy-manage/deploy/cloud-on-k8s/manage-compute-resources.md).
* In self-managed deployments, scaling up or down requires manually [adding](/deploy-manage/deploy/self-managed/installing-elasticsearch.md) or [removing](/deploy-manage/uninstall.md) instances from your deployment.


