---
navigation_title: Resilience in Serverless
applies_to:
  serverless:
products:
  - id: cloud-serverless
---

# Resilience in {{serverless-full}} [resilience-in-serverless]

In {{serverless-full}}, Elastic manages all infrastructure resilience automatically. Unlike {{ech}} or self-managed deployments, there are no nodes to configure, no replica counts to tune, and no availability zone settings to manage. Resilience is built into the platform at the infrastructure level.

## Data durability [resilience-serverless-data-durability]

{{serverless-short}} uses a stateless storage architecture in which indexed data is written to cloud-provider object storage rather than stored as local replicas on cluster nodes. This provides extreme data durability:

* Object storage is replicated across multiple physical locations within a region by the underlying cloud provider, independently of compute node health.
* Data durability does not depend on in-cluster shard replication. A node failure has no impact on data that has already been written — the data exists independently of the compute layer.
* The {{es}} storage engine is continuously updated, so {{serverless-short}} users always benefit from the latest search performance and capabilities. In the extremely rare event that an {{es}} software error affects the quality of stored data, the service is able to roll back any resulting corruption with a one-hour Recovery Point Objective (RPO).

When a client receives a successful write response from {{es}}, the data has been durably persisted to the relevant cloud service provider's regionally-resilient object storage — [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/DataDurability.html), [Google Cloud Storage](https://cloud.google.com/storage/docs/consistency), or [Azure Blob Storage](https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy). For detailed information on the durability and recoverability guarantees of these stores, refer to their respective documentation. From the perspective of {{es}}, the Recovery Point Objective (RPO) for data loss in events such as node failures or even an availability zone outage is zero.

To learn more about the stateless architecture underpinning {{serverless-short}}, refer to [Elastic's serverless architecture](https://www.elastic.co/search-labs/blog/stateless-your-new-state-of-find-with-elasticsearch).

The stateless architecture introduces a higher baseline write latency compared to {{ech}}, as writes are batched before being committed to object storage. Refer to [Compare {{ech}} and Serverless](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md) for details on write performance characteristics.

## High availability [resilience-serverless-high-availability]

{{serverless-short}} automatically distributes compute resources across multiple availability zones within a region. No configuration is required:

* Query and indexing traffic is served from multiple zones simultaneously.
* If a zone becomes unavailable, traffic is automatically shifted to the remaining zones with no action required from you.

Elastic maintains a service level agreement (SLA) for {{serverless-short}} project availability. Refer to the [Elastic Cloud Serverless Service Level Agreement](https://www.elastic.co/agreements/sla-elastic-cloud-serverless) for details.

## Data recovery [resilience-serverless-data-recovery]

{{serverless-short}} does not currently offer a self-service recovery workflow for data loss resulting from user-initiated operations, such as accidental index deletion or bulk document removal. If you experience this type of data loss, [contact Elastic Support](/troubleshoot/index.md#contact-us) to discuss your options.

::::{note}
Self-service data recovery is planned for a future release.
::::

## Regional scope [resilience-serverless-regional-scope]

All resilience in {{serverless-short}} is regional. Projects run in a single cloud region, and there is no built-in support for multi-region architectures:

* Cross-region replication is not available.
* There is no automatic failover to an alternative region if the region itself becomes unavailable.

If your requirements include multi-region resilience, you can deploy separate projects in different regions and manage data routing or synchronization at the application level. Refer to [available Serverless regions](/deploy-manage/deploy/elastic-cloud/regions.md) for the supported options.
