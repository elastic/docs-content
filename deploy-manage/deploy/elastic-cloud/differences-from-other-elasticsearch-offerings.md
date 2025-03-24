---
navigation_title: "Compare Cloud Hosted and Serverless"
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-differences.html
applies_to:
  serverless:
---

# Compare Elastic Cloud Hosted and Serverless [elasticsearch-differences]

This guide compares Elastic Cloud Hosted deployments with Elastic Cloud Serverless projects, highlighting key features and capabilities across different project types. Use this information to understand what's available in each deployment option or to plan migrations between platforms.

## Compare features [elasticsearch-differences-serverless-infrastructure-management]

### Core platform capabilities

These fundamental platform capabilities apply to both deployment models:

| Feature  | Elastic Cloud Hosted | Serverless projects| Notes  |
|----------|----------------------|--------------------|--------|
| Deployment model           | Single deployments with multiple solutions | Separate projects for specific use cases | Fundamental architectural difference                                                   |
| Cloud provider support     | AWS, GCP, Azure                            | AWS, Azure (in preview)              | Azure: [Preview details](https://www.elastic.co/blog/elastic-cloud-serverless-microsoft-azure-tech-preview) |
| Hardware configuration     | Limited control                            | Managed                              | Hardware choices are managed by Elastic                                                |
| Cluster scaling            | Manual with autoscaling option             | Managed                              | Automatic scaling eliminates capacity planning                                         |
| Node management            | User-controlled                            | Managed                              | No node configuration access by design                                                 |
| High availability          | ✅                                         | ✅                                   | Automatic resilience                                                                   |
| Deployment monitoring      | AutoOps or monitoring cluster              | Managed                              | Monitoring is handled by Elastic                                                       |
| Snapshot/restore           | ✅                                         | **WIP**                                  | User-initiated snapshots are planned                                                   |
| Authentication realms      | ✅                                         | ✅                                   | Through Elastic Cloud only in Serverless                                               |
| Custom roles               | ✅                                         | ✅                                   | Fully supported in both                                                                  |
| Audit logging              | ✅                                         | **WIP**                                  | Feature in roadmap                                                                     |
| Traffic filtering and VPCs | ✅                                         | **WIP**                                  | Planned feature in roadmap                                                             |
| Custom plugins and bundles | ✅                                         | ❌                                  | Not supported in Serverless                                                            |

### Elasticsearch

| Feature                         | Elastic Cloud Hosted              | Serverless Elasticsearch projects | Serverless notes                             |
|---------------------------------|-----------------------------------|-----------------------------------|----------------------------------------------|
| Data lifecycle management       | ILM and data stream lifecycle     | Data stream lifecycle only        | No data tiers in Serverless                  |
| Watcher                         | ✅                                | ❌                                | Use Kibana Alerts instead                    |
| Kibana Alerts                   | ✅                                | ✅                                |                                              |
| Reindexing from remote          | ✅                                | **WIP**                               | Planned feature in roadmap                   |
| Clone index API                 | ✅                                | **WIP**                               | Planned feature in roadmap                   |
| Cross-cluster search            | ✅                                | **WIP**                               | Planned as cross-project search              |
| Cross-cluster replication       | ✅                                | **WIP**                               | Planned as cross-project replication         |
| Repository management           | ✅                                | Managed                           | Automatically managed by Elastic             |
| Elasticsearch for Apache Hadoop | ✅                                | ❌                                | Not supported in Serverless     |
| Scripted metric aggregations    | ✅                                | ❌                                | Not supported in Serverless     |
| Enterprise Search (App Search & Workplace Search) | EOL in 9.0 | ❌ | Not available in Serverless |
| Web crawler                     | Self-managed or hosted            | Self-managed only                 | Managed crawler not available                |
| Elastic connectors (for search)               | Self-managed or hosted            | Self-managed only                 | Managed connectors not available             |
| Behavioral analytics| UI and APIs            |  ❌                | Not supported in Serverless     |
| Search applications             | UI and APIs | Maintenance mode (beta), API only | UI not available in Serverless     |

### Observability

| Feature                           | Elastic Cloud Hosted              | Serverless Observability projects | Serverless notes                             |
|-----------------------------------|-----------------------------------|-----------------------------------|----------------------------------------------|
| APM integration                   | ✅                                | Limited                           | See APM limitations below                    |
| Logs management                   | ✅                                | ✅                                |                                              |
| Metrics monitoring                | ✅                                | ✅                                |                                              |
| Uptime monitoring                 | ✅                                | ✅                                |                                              |
| Universal Profiling               | ✅                                | ❌                                | Not currently available                      |
| Real User Monitoring (RUM)        | ✅                                | **WIP**                               | Planned feature in roadmap                   |
| iOS agent/SDK instrumentation     | ✅                                | ❌                                | Not currently available                      |
| Android agent/SDK instrumentation | ✅                                | ❌                                | Not currently available                      |
| APM Tail-based sampling           | ✅                                | ❌                                | Consider OpenTelemetry alternative           |
| APM Agent Central Configuration   | ✅                                | ❌                                | Not currently available                      |
| Custom roles for Kibana Spaces    | ✅                                | **WIP**                               | Planned feature in roadmap                   |
| Fleet server                      | Self-hosted or hosted             | ✅                                | Fully managed by Elastic                     |
| Agent policies                    | ✅                                | ✅                                |                                              |
| Custom ingest pipelines           | ✅                                | Limited                           | Some advanced processors not available       |
| Watcher                           | ✅                                | ❌                                | Use Kibana Alerts instead                    |
| Kibana Alerts                     | ✅                                | ✅                                |                                              |
| Index lifecycle management        | ✅                                | ❌                                | Use data stream lifecycle instead            |
| Data stream lifecycle             | ✅                                | ✅                                |                                              |

### Security

| Feature                                | Elastic Cloud Hosted              | Serverless Security projects      | Serverless notes                             |
|----------------------------------------|-----------------------------------|-----------------------------------|----------------------------------------------|
| SIEM capabilities                      | ✅                                | ✅                                | Core functionality supported                 |
| Endpoint security                      | ✅                                | ✅                                |                                              |
| Field and document level security      | ✅                                | ✅                                |                                              |
| API keys                               | ✅                                | ✅                                |                                              |
| Role-based access control              | ✅                                | Limited                           | Core RBAC supported with some limitations    |
| Watcher                                | ✅                                | ❌                                | Use Kibana Alerts instead                    |
| Kibana Alerts                          | ✅                                | ✅                                |                                              |
| LogsDB                                 | Optional                         | ✅                                | Enabled by default, cannot be disabled       |
| Observability Logs UI                  | ✅                                | ❌                                | Not available in Security projects           |
| Defend for Containers integration      | ✅                                | ❌                                | Not supported in Serverless architecture     |
| Kibana navigation                      | Standard layout                   | Different layout                  | UI differences in Security projects          |

## Architectural differences

Elastic Cloud Serverless takes a fundamentally different approach to running the Elastic Stack compared to Elastic Cloud Hosted:

| Aspect | Elastic Cloud Hosted | Elastic Cloud Serverless |
|--------|----------------------|--------------------------|
| Management model | Self-service infrastructure | Fully managed service |
| Project organization | Single deployments with multiple capabilities | Separate projects for Elasticsearch, Observability, and Security |
| Scaling | Manual or automated with configuration | Fully automated |
| Infrastructure decisions | User manages capacity | Automatically managed by Elastic |
| Pricing model | Based on provisioned resources | Based on actual usage |
| Cloud providers | AWS, GCP, Azure | AWS, Azure (in preview) |

In Serverless, Elastic automatically manages:
* Cluster scaling and optimization
* Node management and allocation
* Shard distribution and replication
* Resource utilization and monitoring

## Elasticsearch index sizing guidelines [elasticsearch-differences-serverless-index-size]

To ensure optimal performance in Serverless Elasticsearch projects, follow these sizing recommendations:

| Use case | Maximum index size | Project configuration |
| --- | --- | --- |
| Vector search | 150GB | Vector optimized |
| General search (non data-stream) | 300GB | General purpose |
| Other uses (non data-stream) | 600GB | General purpose |

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