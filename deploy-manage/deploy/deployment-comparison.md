
# Detailed deployment comparison

This reference provides detailed comparisons of features and capabilities across Elastic's deployment options: [fully self-managed clusters](/deploy-manage/deploy/self-managed.md), [{{ece}}](/deploy-manage/deploy/cloud-enterprise.md) (ECE), [{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md) (ECK), [{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md) (ECH), and [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md). For a high-level overview of deployment types and guidance on choosing between them, refer to the [Deploy and manage overview](../deploy.md).

For more details about feature availability in {{serverless-short}}, refer to [](elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-feature-categories).

## Security

| Feature/capability | Fully self-managed, ECE, ECK | ECH | {{serverless-short}} |
|-------------------|-------------|--------------------------------|-------------------------|
| [Security configurations](/deploy-manage/security.md) | Full control | Limited control | Limited control |
| [Authentication realms](/deploy-manage/users-roles.md) | Available | Available | Available, through {{ecloud}} only |
| [Custom roles](/deploy-manage/users-roles.md) | Available | Available | Available |
| [Audit logging](/deploy-manage/security/logging-configuration/security-event-audit-logging.md) | Available | Available | No |

## Infrastructure and cluster management

| Feature/capability | Fully self-managed | ECE | ECK | ECH | {{serverless-short}} |
|--------------------|--------------------|---------|---------|-----------------|-------------------------|
| Hosting | Any infrastructure | Any infrastructure | Any infrastructure | {{ecloud}} through AWS, Azure, or GCP | {{ecloud}} through AWS, Azure, or GCP |
| Hardware configuration | Full control | Full control | Full control | Limited control | Managed by Elastic |
| [Autoscaling](/deploy-manage/autoscaling.md) | No |  Available | Available | Available | Automatic |
| [Data tier](/manage-data/lifecycle/data-tiers.md) management | Through [ILM policies](/manage-data/lifecycle/index-lifecycle-management.md) | Through [ILM policies](/manage-data/lifecycle/index-lifecycle-management.md) | Through [ILM policies](/manage-data/lifecycle/index-lifecycle-management.md) | Available | No data tiers |
| [Snapshot management](/deploy-manage/tools/snapshot-and-restore.md) | Custom | Custom | Available | Available | Managed by Elastic |
| [High availability and disaster recovery](/deploy-manage/production-guidance/availability-and-resilience.md) | Available | Available | Available | Available | Managed by Elastic |
| [Shard management and replicas](/deploy-manage/distributed-architecture/clusters-nodes-shards.md) | Available | Available | Available | Available | Managed by Elastic |

## Monitoring

| Feature/capability | Fully self-managed, ECE, ECK | ECH | {{serverless-short}} |
|-------------------|-------------------------------|---------|----------------------|
| [Deployment health monitoring](/deploy-manage/monitor.md) | AutoOps or monitoring cluster | AutoOps or monitoring cluster | Managed by Elastic |
| [Alerting](/explore-analyze/alerts-cases.md) | Watcher or {{kib}} alerts | Watcher or {{kib}} alerts | Alerts ([why?](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-features-replaced)) |

## Data lifecycle

| Feature/capability | Fully self-managed, ECE, ECK | ECH | {{serverless-short}} |
|-------------------|-------------------------------|---------|----------------------|
| [Data lifecycle management](/manage-data/lifecycle.md) | ILM, data tiers, data stream lifecycle | ILM, data tiers, data stream lifecycle | Data stream lifecycle ([why?](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-features-replaced)) |
| [Snapshot management](/deploy-manage/tools/snapshot-and-restore.md) | Custom | Available | Managed by Elastic |

## Integrations and extensions

| Feature/capability | Fully self-managed, ECE, ECK | ECH | {{serverless-short}} |
|-------------------|-------------------------------|---------|----------------------|
| Custom plugins and bundles | Available | Available | No |
| [Self-managed connectors](elasticsearch://reference/search-connectors/self-managed-connectors.md) | Available | Limited | Limited |
| [{{es}}-Hadoop integration](elasticsearch-hadoop://reference/elasticsearch-hadoop.md) | Available | Available | No |
| [Cross cluster search (CCS)](/solutions/search/cross-cluster-search.md) | Available | Available | [Planned](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-feature-planned) |
| [Cross cluster replication](/deploy-manage/tools/cross-cluster-replication.md) | Available | Available | [Planned](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-feature-planned) |

## Development and testing features

| Feature/capability | Fully self-managed, ECE, ECK | ECH | {{serverless-short}} |
|-------------------|-------------------------------|---------|----------------------|
| Advanced testing and development | Available | No | No |
| Java (JVM) customization | Available | No | No |

