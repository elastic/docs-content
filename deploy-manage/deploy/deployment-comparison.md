
# Deployment comparison reference

This reference provides detailed comparisons of features and capabilities across Elastic's deployment options: self-managed deployments, Elastic Cloud Hosted, and Serverless. For a high-level overview of deployment types and guidance on choosing between them, see the [overview](../deploy.md).

## Security features

| Feature/capability | Self-managed | Elastic Cloud Hosted | Serverless |
|-------------------|-------------|--------------------------------|-------------------------|
| Custom security configurations | Yes | Limited | No |
| Authentication realms and custom roles | Yes | Yes | No |
| Audit logging | Yes | Yes | No |

## Management features

| Feature/capability | Self-managed | Elastic Cloud Hosted | Serverless |
|-------------------|-------------|--------------------------------|-------------------------|
| Full control over configuration | Yes | Limited | No |
| Infrastructure flexibility | Yes | No | No |
| Autoscaling | No | Yes | Yes |
| Data tiers management | No | Yes | No |
| Snapshot management | No | Yes | No |
| High availability and disaster recovery | Yes | Yes | Yes |
| Multi-cloud support | No | Yes | Yes |
| Shard management and replicas | Yes | Yes | No |

## Monitoring features

| Feature/capability | Self-managed | Elastic Cloud Hosted | Serverless |
|-------------------|-------------|--------------------------------|-------------------------|
| Watcher | Yes | Yes | No |

## Data lifecycle features

| Feature/capability | Self-managed | Elastic Cloud Hosted | Serverless |
|-------------------|-------------|--------------------------------|-------------------------|
| Index lifecycle management (ILM) | Yes | Yes | No (uses data streams) |
| Data tiers management | No | Yes | No |
| Snapshot management | No | Yes | No |

## Integration features

| Feature/capability | Self-managed | Elastic Cloud Hosted | Serverless |
|-------------------|-------------|--------------------------------|-------------------------|
| Custom plugins | Yes | No | No |
| Self-managed connectors | Yes | No | Limited |
| Elasticsearch-Hadoop integration | Yes | Yes | No |
| Cross cluster search (CCS) | Yes | Yes | No |
| Cross cluster replication | Yes | Yes | Yes |

## Development and testing features

| Feature/capability | Self-managed | Elastic Cloud Hosted | Serverless |
|-------------------|-------------|--------------------------------|-------------------------|
| Advanced testing and development | Yes | No | No |
| Java (JVM) customization | Yes | No | No |

