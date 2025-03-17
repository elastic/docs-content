
# Detailed deployment comparison

This reference provides detailed comparisons of features and capabilities across Elastic's deployment options: self-managed deployments, Elastic Cloud Hosted, and Serverless. For a high-level overview of deployment types and guidance on choosing between them, see the [overview](../deploy.md).

For more details about feature availability in Serverless, check [](elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-feature-categories).

## Security

| Feature/capability | Self-managed | Elastic Cloud Hosted | Serverless |
|-------------------|-------------|--------------------------------|-------------------------|
| [Security configurations](/deploy-manage/security.md) | Full control | Limited control | Limited control |
| [Authentication realms](/deploy-manage/users-roles.md) | Available | Available | Available, through Elastic Cloud only |
| [Custom roles](/deploy-manage/users-roles.md) | Available | Available | Available |
| [Audit logging](/deploy-manage/security/logging-configuration/security-event-audit-logging.md) | Available | Available | No |

## Infrastructure and cluster management

| Feature/capability | Self-managed | Elastic Cloud Hosted | Serverless |
|-------------------|-------------|--------------------------------|-------------------------|
| Hosting | Any infrastructure | Elastic Cloud through AWS, Azure, or GCP | Elastic Cloud through AWS or Azure |
| Hardware configuration | Full control | Limited control | Managed by Elastic |
| Autoscaling | No | Available | Automatic |
| Data tiers management | Through ILM policies | Available | No data tiers |
| Snapshot management | Custom | Available | Managed by Elastic |
| High availability and disaster recovery | Available | Available | Managed by Elastic |
| Shard management and replicas | Available | Available | Managed by Elastic |

## Monitoring

| Feature/capability | Self-managed | Elastic Cloud Hosted | Serverless |
|-------------------|-------------|--------------------------------|-------------------------|
| [Deployment health monitoring](/deploy-manage/monitor.md) | Monitoring cluster | AutoOps or monitoring cluster | Managed by Elastic |
| [Alerting](/explore-analyze/alerts-cases.md) | Watcher or Kibana alerts | Watcher or Kibana alerts | Alerts ([why?](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-features-replaced)) |

## Data lifecycle

| Feature/capability | Self-managed | Elastic Cloud Hosted | Serverless |
|-------------------|-------------|--------------------------------|-------------------------|
| [Data lifecycle management](/manage-data/lifecycle.md) | ILM, data tiers, data stream lifecycle | ILM, data tiers, data stream lifecycle | Data stream lifecycle ([why?](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-features-replaced)) |
| [Snapshot management](/deploy-manage/tools/snapshot-and-restore.md) | Custom | Available | Managed by Elastic |

## Integrations and extensions

| Feature/capability | Self-managed | Elastic Cloud Hosted | Serverless |
|-------------------|-------------|--------------------------------|-------------------------|
| Custom plugins and bundles | Available | Available | No |
| Self-managed connectors | Available | Limited | Limited |
| Elasticsearch-Hadoop integration | Available | Available | No |
| Cross cluster search (CCS) | Available | Available | [Planned](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-feature-planned) |
| Cross cluster replication | Available | Available | [Planned](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-serverless-feature-planned) |

## Development and testing features

| Feature/capability | Self-managed | Elastic Cloud Hosted | Serverless |
|-------------------|-------------|--------------------------------|-------------------------|
| Advanced testing and development | Available | No | No |
| Java (JVM) customization | Available | No | No |

