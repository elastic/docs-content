---
navigation_title: "Compare Cloud Hosted and Serverless"
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-differences.html
applies_to:
  serverless:
  ess:
---

# Compare Elastic Cloud Hosted and Serverless [elasticsearch-differences]

This guide compares Elastic Cloud Hosted deployments with Elastic Cloud Serverless projects, highlighting key features and capabilities across different project types. Use this information to understand what's available in each deployment option or to plan migrations between platforms.

## Architectural differences

Elastic Cloud Serverless takes a fundamentally different approach to running the Elastic Stack compared to Elastic Cloud Hosted:

| **Aspect** | Elastic Cloud Hosted | Elastic Cloud Serverless |
|--------|----------------------|--------------------------|
| **Management model** | Self-service infrastructure | Fully managed service |
| **Project organization** | Single deployments with multiple capabilities | Separate projects for Elasticsearch, Observability, and Security |
| **Scaling** | Manual or automated with configuration | Fully automated |
| **Infrastructure decisions** | User manages capacity | Automatically managed by Elastic |
| **Pricing model** | Based on provisioned resources | Based on actual usage |
| **Cloud providers** | AWS, GCP, Azure | AWS, Azure (in preview) |
| **Upgrades** | User-controlled timing | Automatically performed by Elastic |
| **User management** | Elastic Cloud-managed and native Kibana users | Elastic Cloud-managed users only |
| **Backups** | User-managed with Snapshot & Restore | Automatically backed up by Elastic |
| **Solutions** | Full Elastic Stack per deployment | Single solution per project |

In Serverless, Elastic automatically manages:
* Cluster scaling and optimization
* Node management and allocation
* Shard distribution and replication
* Resource utilization and monitoring
* High availability and disaster recovery strategies

## Compare features [elasticsearch-differences-serverless-infrastructure-management]

$$$elasticsearch-differences-serverless-feature-categories$$$
$$$elasticsearch-differences-serverless-features-replaced$$$
$$$elasticsearch-differences-serverless-feature-planned$$$

### Core platform capabilities

These fundamental platform capabilities apply to both deployment models:

| **Feature**  | Elastic Cloud Hosted | Serverless projects| Notes  |
|----------|----------------------|--------------------|--------|
| **Audit logging** | ✅ | **Planned** | [View roadmap](https://www.elastic.co/cloud/serverless/roadmap) |
| **Authentication realms** | ✅ | ✅ | Through Elastic Cloud only in Serverless |
| **BYO-Key for Encryption at Rest** | ✅ | **Planned** | [View roadmap](https://www.elastic.co/cloud/serverless/roadmap) |
| **Cloud provider support** | AWS, GCP, Azure | AWS, Azure (in preview), GCP (planned) | Azure: [Preview details](https://www.elastic.co/blog/elastic-cloud-serverless-microsoft-azure-tech-preview) |
| **Cluster scaling** | Manual with autoscaling option | Managed | Automatic scaling eliminates capacity planning - [Learn more](https://www.elastic.co/blog/elastic-serverless-architecture) |
| **Custom plugins and bundles** | ✅ | ❌ | Not supported in Serverless |
| **Custom roles** | ✅ | ✅ | Fully supported in both |
| **Deployment health monitoring** | AutoOps or monitoring cluster | Managed by Elastic | No monitoring cluster required in Serverless |
| **Deployment model** | Single deployments with multiple solutions | Separate projects for specific use cases | Fundamental architectural difference - [Learn more](https://www.elastic.co/blog/elastic-serverless-architecture) |
| **Deployment monitoring** | AutoOps or monitoring cluster | Managed | Monitoring is handled by Elastic |
| **Hardware configuration** | Limited control | Managed | Hardware choices are managed by Elastic |
| **High availability** | ✅ | ✅ | Automatic resilience |
| **Network security** | Public IP traffic filtering, private connectivity (VPCs, PrivateLink) | **Planned** |  [View roadmap](https://www.elastic.co/cloud/serverless/roadmap) |
| **Node management** | User-controlled | Managed | No node configuration access by design |
| **Snapshot/restore** | ✅ | **Planned** | User-initiated snapshots are planned - [View roadmap](https://www.elastic.co/cloud/serverless/roadmap) |


### Elasticsearch

| **Feature** | Elastic Cloud Hosted | Serverless Elasticsearch projects | Serverless notes |
|---------|----------------------|-----------------------------------|------------------|
| **Behavioral analytics** | UI and APIs | ❌ | Not supported in Serverless |
| **Clone index API** | ✅ | **Planned** | [View roadmap](https://www.elastic.co/cloud/serverless/roadmap) |
| **Cross-cluster replication** | ✅ | **Planned** | Planned as cross-project replication - [View roadmap](https://www.elastic.co/cloud/serverless/roadmap) |
| **Cross-cluster search** | ✅ | **Planned** | Planned as cross-project search - [View roadmap](https://www.elastic.co/cloud/serverless/roadmap) |
| **Data lifecycle management** | ILM and data stream lifecycle | Data stream lifecycle only | No data tiers in Serverless |
| **Elastic connectors (for search)** | Self-managed or hosted (discontinued in 9.0) | Self-managed only | Managed connectors not available |
| **Elasticsearch for Apache Hadoop** | ✅ | ❌ | Not supported in Serverless |
| **Enterprise Search (App Search & Workplace Search)** | ✅ (discontinued in 9.0) | ❌ | Not available in Serverless |
| **Kibana Alerts** | ✅ | ✅ | |
| **Reindexing from remote** | ✅ | **Planned** | [View roadmap](https://www.elastic.co/cloud/serverless/roadmap) |
| **Repository management** | ✅ | Managed | Automatically managed by Elastic |
| **Scripted metric aggregations** | ✅ | ❌ | Not supported in Serverless |
| **Search applications** | UI and APIs | Maintenance mode (beta), API only | UI not available in Serverless |
| **Shard management** | User-configurable | Managed by Elastic | No manual shard allocation in Serverless |
| **Watcher** | ✅ | ❌ | Use Kibana Alerts instead |
| **Web crawler** | Self-managed or hosted (discontinued in 9.0) | Self-managed only | Managed crawler not available |

### Observability

| **Feature** | Elastic Cloud Hosted | Serverless Observability projects | Serverless notes |
|---------|----------------------|-----------------------------------|------------------|
| **Agent policies** | ✅ | ✅ | |
| **APM Agent Central Configuration** | ✅ | ❌ | Not currently available |
| **APM integration** | ✅ | Limited | Limited to distributed tracing and infrastructure monitoring capabilities |
| **APM Tail-based sampling** | ✅ | ❌ | Consider OpenTelemetry alternative |
| **Android agent/SDK instrumentation** | ✅ | ❌ | Not currently available |
| **Custom ingest pipelines** | ✅ | Limited | Some advanced processors not available |
| **Custom roles for Kibana Spaces** | ✅ | **Planned** | [View roadmap](https://www.elastic.co/cloud/serverless/roadmap) |
| **Data stream lifecycle** | ✅ | ✅ | Primary lifecycle management method in Serverless |
| **Fleet server** | Self-hosted or hosted | ✅ | Fully managed by Elastic |
| **Index lifecycle management** | ✅ | ❌ | Use data stream lifecycle instead |
| **iOS agent/SDK instrumentation** | ✅ | ❌ | Not currently available |
| **Kibana Alerts** | ✅ | ✅ | |
| **Logs management** | ✅ | ✅ | |
| **Metrics monitoring** | ✅ | ✅ | |
| **Real User Monitoring (RUM)** | ✅ | **Planned** | [View roadmap](https://www.elastic.co/cloud/serverless/roadmap) |
| **Universal Profiling** | ✅ | ❌ | Not currently available |
| **Uptime monitoring** | ✅ | ✅ | |
| **Watcher** | ✅ | ❌ | Use Kibana Alerts instead |

### Security

| **Feature** | Elastic Cloud Hosted | Serverless Security projects | Serverless notes |
|---------|---------------------|------------------------------|------------------|
| **API keys** | ✅ | ✅ | |
| **Defend for Containers integration** | ✅ (being deprecated in 9.0) | ❌ | Not supported in Serverless architecture |
| **Endpoint security** | ✅ | ✅ | |
| **Field and document level security** | ✅ | ✅ | |
| **Kibana Alerts** | ✅ | ✅ | |
| **Kibana navigation** | Standard layout | Different layout | UI differences in Security projects |
| **LogsDB** | Optional | ✅ | Enabled by default, cannot be disabled |
| **Observability Logs UI** | ✅ | ❌ | Not available in Security projects |
| **Role-based access control** | ✅ | Limited | Core RBAC functionality supported - [Learn more](https://www.elastic.co/guide/en/serverless/current/security-rbac.html) |
| **SIEM capabilities** | ✅ | ✅ | Core functionality supported |
| **Watcher** | ✅ | ❌ | Use Kibana Alerts instead |

## Elasticsearch index sizing guidelines [elasticsearch-differences-serverless-index-size]

To ensure optimal performance in Serverless Elasticsearch projects, follow these sizing recommendations:

| **Use case** | Maximum index size | Project configuration |
| --- | --- | --- |
| **Vector search** | 150GB | Vector optimized |
| **General search (non data-stream)** | 300GB | General purpose |
| **Other uses (non data-stream)** | 600GB | General purpose |

For large datasets that exceed the recommended maximum size, consider splitting your data across smaller indices and using an alias to search them collectively.

These recommendations do not apply to indices using better binary quantization (BBQ). Refer to [vector quantization](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) for more information.

## Available {{es}} APIs [elasticsearch-differences-serverless-apis-availability]

Because Elastic Cloud Serverless manages infrastructure automatically, certain Elasticsearch APIs are not available:

Infrastructure operations
:   * All `_nodes/*` operations
* All `_cluster/*` operations
* Most `_cat/*` operations, except for index-related operations such as `/_cat/indices` and `/_cat/aliases`

Storage and backup
:   * All `_snapshot/*` operations
* Repository management operations

Index management
:   * `indices/close` operations
* `indices/open` operations
* Recovery and stats operations
* Force merge operations

When attempting to use an unavailable API, you'll receive this error:

```json
{
 "error": {
   "root_cause": [
     {
       "type": "api_not_available_exception",
       "reason": "Request for uri [/<API_ENDPOINT>] with method [<METHOD>] exists but is not available when running in serverless mode"
     }
   ],
   "status": 410
 }
}
```

::::{tip}
Refer to the [{{es-serverless}} API reference](https://www.elastic.co/docs/api/doc/elasticsearch-serverless) for a complete list of available APIs.
::::

## Available {{es}} settings [elasticsearch-differences-serverless-settings-availability]

In Elastic Cloud Serverless Elasticsearch projects, you can only configure [index-level settings](elasticsearch://reference/elasticsearch/index-settings/index.md). Cluster-level settings and node-level settings are fully managed by Elastic.

Available settings
:   **Index-level settings**: Settings that control how documents are processed, stored, and searched are available to end users. These include:

    * Analysis configuration
    * Mapping parameters
    * Search/query settings
    * Indexing settings such as `refresh_interval`

Managed settings
:   **Infrastructure-related settings**: Settings that affect cluster resources or data distribution are not available to end users. These include:

    * Node configurations
    * Cluster topology
    * Shard allocation
    * Resource management

## Learn more

- [Elastic Cloud Serverless roadmap](https://www.elastic.co/cloud/serverless/roadmap): See upcoming features and development plans
- [Elasticsearch Serverless API reference](https://www.elastic.co/docs/api/doc/elasticsearch-serverless): Check out the complete list of available APIs in Elastic Cloud Serverless
- [Project settings](/deploy-manage/deploy/elastic-cloud/project-settings.md): Configure project settings in Elastic Cloud Serverless
- [Serverless regions](/deploy-manage/deploy/elastic-cloud/regions.md): Choose the right region for your Elastic Cloud Serverless project
- [Elastic Cloud pricing](https://www.elastic.co/pricing/): Understand pricing for Elastic Cloud Hosted and Serverless projects
  - [Serverless project billing](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md): Understand billing dimensions for Serverless projects
  - [Elastic Cloud Hosted billing](/deploy-manage/cloud-organization/billing/cloud-hosted-deployment-billing-dimensions.md): Understand billing dimensions for Elastic Cloud Hosted deployments