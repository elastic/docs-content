---
navigation_title: Scaling considerations
applies_to:
  deployment:
    eck: all
    ess: all
    ece: all
    self: all
products:
  - id: elasticsearch
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
---

# {{es}} scaling considerations

Knowing when and how to scale your deployment is critical, especially when unexpected workloads hit. Adding more nodes or adjusting resources is not always the best solution. Instead, scaling should be based on real workload patterns and informed decision-making.

In orchestrated or managed deployments, [Autoscaling](/deploy-manage/autoscaling.md) can automatically adjust cluster resources based on demand, reducing operational overhead. However, if you choose not to use it, or in self-managed environments, scaling becomes a manual process that requires careful planning to adapt to workload changes and ensure the cluster remains performant and resilient.

::::{note}
In **{{serverless-full}}** projects, Elastic manages all scaling and performance tuning automatically. You don't need to configure nodes, resources, or autoscaling parameters.
::::

Refer to [Sizing {{es}}: Scaling up and out](https://www.elastic.co/blog/found-sizing-elasticsearch) to identify which questions to ask yourself when determining which cluster size is the best fit for your {{es}} use case.

## Monitoring and scaling decisions

To make informed scaling decisions, [cluster monitoring](/deploy-manage/monitor.md) is essential. Metrics such as CPU usage, memory pressure, disk I/O, query response times, and shard distribution provide insights into when scaling may be necessary.

## Performance optimizations and scaling

Scaling isn’t just about adding more nodes—it also involves [optimizing the cluster configuration for better performance](./optimize-performance.md). Adjustments such as shard and index tuning, query optimizations, caching strategies, and efficient resource allocation can improve performance without requiring additional hardware. These optimizations directly influence scaling strategies, because a well-tuned cluster can handle more workload with fewer resources.

## Scaling and fault tolerance

When adding zones for fault tolerance or high availability (HA), it might seem like you’re also scaling up. While additional zones might improve the performance, they should not be relied upon for additional capacity.

In {{ech}} and {{ece}}, the concept of zones is intended for:
* High availability (two zones)
* Fault tolerance (three zones)

Neither will work if the cluster relies on the resources from those zones to be operational.

For true HA at the zone level, the recommended approach is to **first scale up** resources within a single zone until the cluster can take the full load (add some buffer to be prepared for a peak of requests), **then scale out** by adding additional zones depending on your requirements: two zones for high availability, three zones for fault tolerance.

Although the previous is the general recommendation, you should design your cluster to best support your HA requirements. Just make sure you fully understand the implications of your choices and plan accordingly.

## How to scale

Scaling {{es}} depends on how you deploy it. Refer to the appropriate guides below based on your deployment type.

### Orchestrated deployments

These platforms offer built-in autoscaling and flexible resource management:

* [Autoscaling](/deploy-manage/autoscaling.md): Available in {{ech}}, {{ece}}, and {{eck}}.  

  ::::{note}
  An enterprise license is required for ECK autoscaling.
  ::::

* [Configure {{ech}} deployments](/deploy-manage/deploy/elastic-cloud/configure.md): Change instance sizes, increase capacity, or [select a different hardware profile](/deploy-manage/deploy/elastic-cloud/ec-change-hardware-profile.md).

* [Resize an ECE deployment](/deploy-manage/deploy/cloud-enterprise/resize-deployment.md): Adjust deployment size or topology in the {{ece}} console.

* [Configure ECK deployments](/deploy-manage/deploy/cloud-on-k8s/configure-deployments.md): Change the number of {{es}} nodes, [customize compute resources](/deploy-manage/deploy/cloud-on-k8s/manage-compute-resources.md), or configure `nodeSets` to adjust the cluster architecture and topology.

### Self-managed deployments

In self-managed environments, scaling requires manual intervention:

* [Add {{es}} nodes](/deploy-manage/deploy/self-managed/installing-elasticsearch.md)
* [Uninstall {{es}} nodes](/deploy-manage/uninstall.md)
