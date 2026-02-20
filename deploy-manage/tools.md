---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/high-availability.html
applies_to:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---



# Backup, high availability, and resilience tools [high-availability]

Elastic provides comprehensive tools to safeguard data, ensure continuous availability, and maintain resilience. These tools are designed to support disaster recovery strategies, enabling businesses to protect critical information and minimize downtime, and maintain high availability in case of unexpected failures. In this section, you'll learn about these tools and how to implement them in your environment.

For strategies to design resilient clusters, see **[Availability and resilience](production-guidance/availability-and-resilience.md)**.

::::{note} 
The snapshot and restore and cross-cluster replication features are currently not available for {{serverless-full}} projects. These features will be introduced in the future. For more information, refer to [](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-feature-categories).
::::

## Snapshot and restore

Snapshots in {{es}} are point-in-time backups that include your cluster's data, settings, and overall state. They capture all the information necessary to restore your cluster to a specific moment in time, making them essential for protecting data, recovering from unexpected issues, and transferring data between clusters. Snapshots are a reliable way to ensure the safety of your data and maintain the continuity of your operations.

You can perform the following tasks to manage snapshots and snapshot repositories:

- **[Register a repository](tools/snapshot-and-restore/manage-snapshot-repositories.md):** Configure storage repositories (for example, S3, Azure, Google Cloud) to store snapshots. The way that you register repositories differs depending on your deployment method:
  - **[{{ech}}](tools/snapshot-and-restore/elastic-cloud-hosted.md):** Deployments come with a preconfigured S3 repository for automatic backups, simplifying the setup process. You can also register external repositories, such as Azure, and Google Cloud, for more flexibility.
  - **[{{ece}}](tools/snapshot-and-restore/cloud-enterprise.md):** Repository configuration is managed through the {{ece}} user interface and automatically linked to deployments.
  - **[{{eck}}](tools/snapshot-and-restore/cloud-on-k8s.md) and [self-managed](tools/snapshot-and-restore/self-managed.md) deployments:** Repositories must be configured manually.

- **[Create snapshots](tools/snapshot-and-restore/create-snapshots.md):** Manually or automatically create backups of your cluster.
- **[Restore a snapshot](tools/snapshot-and-restore/restore-snapshot.md):** Recover indices, data streams, or the entire cluster to revert to a previous state. You can choose to restore specific parts of a snapshot, such as a single index, or perform a full restore.

To reduce storage costs for infrequently accessed data while maintaining access, you can also create **[searchable snapshots](tools/snapshot-and-restore/searchable-snapshots.md)**.

::::{note}
Snapshot configurations vary across {{ech}}, {{ece}} (ECE), {{eck}} (ECK), and self-managed deployments.
::::

## Cross-cluster replication (CCR)

**[Cross-cluster replication (CCR)](tools/cross-cluster-replication.md)** is a feature in {{es}} that allows you to replicate data in real time from a leader cluster to one or more follower clusters. This replication ensures that data is synchronized across clusters, providing continuity, redundancy, and enhanced data accessibility. 

CCR provides a way to automatically synchronize indices from a leader cluster to a follower cluster. This cluster could be in a different data center or even a different continent from the leader cluster. If the primary cluster fails, the secondary cluster can take over.

::::{note}
CCR relies on **[remote clusters](remote-clusters.md)** functionality to establish and manage connections between the leader and the follower clusters.
::::

You can perform the following tasks to manage cross-cluster replication:

- **[Set up CCR](tools/cross-cluster-replication/set-up-cross-cluster-replication.md):** Configure leader and follower clusters for data replication.
- **[Manage CCR](tools/cross-cluster-replication/manage-cross-cluster-replication.md):** Monitor and manage replicated indices.
- **[Automate replication](tools/cross-cluster-replication/manage-auto-follow-patterns.md):** Use auto-follow patterns to automatically replicate newly created indices.
- **Set up failover clusters:** Configure **[uni-directional](tools/cross-cluster-replication/uni-directional-disaster-recovery.md)** or **[bi-directional](tools/cross-cluster-replication/bi-directional-disaster-recovery.md)** CCR for redundancy and disaster recovery.
- **[Review cluster upgrade considerations when using CCR](upgrade.md):** If you're using CCR, then you might need to upgrade your clusters in a specific order to prevent errors. Review the considerations and recommended procedures for performing upgrades on CCR leaders and followers.