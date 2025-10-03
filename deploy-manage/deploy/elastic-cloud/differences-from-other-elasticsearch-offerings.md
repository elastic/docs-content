---
navigation_title: Compare Cloud Hosted and Serverless
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-differences.html
applies_to:
  serverless:
  deployment:
    ess:
products:
  - id: cloud-serverless
---

# Compare {{ech}} and Serverless [elasticsearch-differences]

This guide compares {{ech}} deployments with {{serverless-full}} projects, highlighting key features and capabilities across different project types. Use this information to understand what's available in each deployment option or to plan migrations between platforms.

:::{note}
The following information reflects our strategic goals, plans and objectives and includes estimated release dates, anticipated features and functions, and proposed descriptions for commercial features. All details are for information only and are subject to change in our discretion. Information might be updated, added, or removed from this document as features or products become available, canceled, or postponed.
:::

## Architectural differences

{{serverless-full}} takes a fundamentally different approach to running the {{stack}} compared to {{ech}}:

| **Functionality** | {{ech}} | {{serverless-full}} |
|--------|----------------------|--------------------------|
| **Management model** | Self-service infrastructure | Fully managed service |
| **Project organization** | Single deployments with multiple capabilities | Separate projects for Elasticsearch, Observability, and Security |
| **Scaling** | Manual or automated with configuration | Fully automated |
| **Infrastructure decisions** | User manages capacity | Automatically managed by Elastic |
| **Pricing model** | Based on provisioned resources | Based on usage |
| **Cloud providers** | AWS, Azure, GCP  | AWS, Azure, GCP |
| **Upgrades** | User-controlled timing | Automatically performed by Elastic |
| **User management** | Elastic Cloud-managed and deployment-local users | Elastic Cloud-managed users only. Serverless users are managed at the organization level with SAML authentication support. |
| **Backups** | User-managed with Snapshot & Restore | Automatically backed up by Elastic |
| **Solutions** | Full {{stack}} per deployment | Single solution per project |
| **Cross-origin resource sharing (CORS)** | Supported | Not available. Browser-based applications must route requests through a backend proxy server. |

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

This table compares the core platform capabilities between {{ech}} deployments and Serverless projects:

| **Feature**  | {{ech}} | Serverless projects| Notes  |
|----------|----------------------|--------------------|--------|
| **Audit logging** | ✅ | **Planned** | Anticipated in a future release |
| **Authentication realms** | ✅ | ✅ | Managed at organization level in Serverless; deployment level in Hosted |
| **BYO-Key for encryption at rest** | ✅ | **Planned** | Anticipated in a future release; data in Serverless is stored on cloud-provider encrypted object storage |
| **Cloud provider support** | - AWS <br>- GCP <br>- Azure | - AWS <br>- Azure <br>- GCP | - [{{ech}} regions](cloud://reference/cloud-hosted/regions.md)<br>- [Serverless regions](/deploy-manage/deploy/elastic-cloud/regions.md) |
| **Cluster scaling** | Manual with autoscaling option | Managed | Automatic scaling eliminates capacity planning - [Learn more](https://www.elastic.co/blog/elastic-serverless-architecture) |
| **Custom plugins and bundles** | ✅ | ❌ | Not available in Serverless |
| **Custom roles** | ✅ | ✅ |  |
| **Deployment health monitoring** | AutoOps or monitoring cluster | Managed by Elastic | - No monitoring cluster required <br>- Automatically handled by Elastic |
| **Deployment model** | Single deployments with multiple solutions | Separate projects for specific use cases | Fundamental architectural difference - [Learn more](https://www.elastic.co/blog/elastic-serverless-architecture) |
| **Deployment monitoring** | AutoOps or monitoring cluster | Managed | Monitoring is handled by Elastic |
| **Email service** | ✅ | ✅ | Preconfigured email connector available - [Learn more about limits and usage](/deploy-manage/deploy/elastic-cloud/tools-apis.md#elastic-cloud-email-service) |
| **Hardware configuration** | Limited control | Managed | Hardware choices are managed by Elastic |
| **High availability** | ✅ | ✅ | Automatic resilience |
| **Network security** | IP filtering, private connectivity (VPCs, PrivateLink) | IP filtering | Private connectivity options anticipated in a future release |
| **Node management** | User-controlled | Managed | No node configuration access by design |
| **Snapshot/restore** | ✅ | **Planned** | User-initiated snapshots are anticipated in a future release |

:::{note}
The [{{serverless-full}} roadmap](https://www.elastic.co/cloud/serverless/roadmap) primarily focuses on platform capabilities rather than project-specific features. Use the following project-specific tables for information about features for each project type.
:::

### Elasticsearch

This table compares Elasticsearch capabilities between {{ech}} deployments and Serverless projects:

| **Feature** | {{ech}} | Serverless Elasticsearch projects | Serverless notes |
|---------|----------------------|-----------------------------------|------------------|
| [**AI Assistant**](/solutions/observability/observability-ai-assistant.md) | ✅ | ✅ | |
| **Behavioral analytics** | ❌ (deprecated in 9.0) | ❌ | Not available in Serverless |
| [**Clone index API**](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-clone) | ✅ | **Planned** | Anticipated in a future release |
| [**Bulk indexing**](/deploy-manage/production-guidance/optimize-performance/indexing-speed.md#_use_bulk_requests) |  ✅ | ✅ | The maximum bulk request response time in {{serverless-short}} is 200ms |
| [**Cross-cluster replication**](/deploy-manage/tools/cross-cluster-replication.md) | ✅ | **Planned** | Anticipated in a future release |
| [**Cross-cluster search**](/solutions/search/cross-cluster-search.md) | ✅ | **Planned** | Anticipated in a future release |
| **Data lifecycle management** | - [ILM](/manage-data/lifecycle/index-lifecycle-management.md) <br>- [Data stream lifecycle](/manage-data/lifecycle/data-stream.md) | [Data stream lifecycle](/manage-data/lifecycle/data-stream.md) only | - No data tiers in Serverless <br>- Optimized for common lifecycle management needs |
| **Elastic connectors (for search)** | ❌ (Managed connectors discontinued with Enterprise Search in 9.0) | Self-managed only | - Managed connectors not available <br>- Use [**self-managed connectors**](elasticsearch://reference/search-connectors/self-managed-connectors.md) |
| [**Elasticsearch for Apache Hadoop**](https://www.elastic.co/elasticsearch/hadoop) | ✅ | ❌ | Not available in Serverless |
| **Enterprise Search (App Search & Workplace Search)** | ❌ (discontinued in 9.0) | ❌ | Not available in Serverless |
| [**Kibana Alerts**](/deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md) | ✅ | ✅ | |
| [**Reindexing from remote**](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) | ✅ | **Planned** | Anticipated in a future release |
| **Repository management** | ✅ | Managed | Automatically managed by Elastic |
| [**Scripted metric aggregations**](elasticsearch://reference/aggregations/search-aggregations-metrics-scripted-metric-aggregation.md) | ✅ | ❌ | Not available in Serverless<br>The alternative for this in Serverless is [ES|QL](elasticsearch://reference/query-languages/esql.md) |
| [**`join` fields**](elasticsearch://reference/elasticsearch/mapping-reference/parent-join.md) | ✅ | ❌ | Not available in Serverless<br>The alternative for this in Serverless is the ES\|QL [`LOOKUP JOIN`](elasticsearch://reference/query-languages/esql/commands/lookup-join.md) command |
| [**Search applications**](/solutions/search/search-applications.md) | - UI and APIs <br>- Maintenance mode (beta) | - API-only <br>- Maintenance mode (beta) | UI not available in Serverless |
| **Shard management** | User-configurable | Managed by Elastic | No manual shard allocation in Serverless |
| [**Watcher**](/explore-analyze/alerts-cases/watcher.md) | ✅ | ❌ | Use **Kibana Alerts** instead, which provides rich integrations across use cases |
| **Web crawler** | ❌ (Managed Elastic Crawler discontinued with Enterprise Search in 9.0) | Self-managed only | Use [**self-managed crawler**](https://github.com/elastic/crawler) |

### Observability

This table compares Observability capabilities between {{ech}} deployments and Observability Complete Serverless projects. For more information on Observability Logs Essentials Serverless projects, refer to [Observability feature tiers](../../../solutions/observability/observability-serverless-feature-tiers.md).

| **Feature** | {{ech}} | Serverless Observability Complete projects | Serverless notes |
|---------|----------------------|-----------------------------------|------------------|
| [**AI Assistant**](/solutions/observability/observability-ai-assistant.md) | ✅ | ✅ | |
| **APM integration** | ✅ | ✅ | Use **Managed Intake Service** (supports Elastic APM and OTLP protocols) <br> Refer to [Managed OTLP endpoint](opentelemetry://reference/motlp.md) for OTLP data ingestion |
| [**APM Agent Central Configuration**](/solutions/observability/apm/apm-server/apm-agent-central-configuration.md) | ✅ | ❌ | Not available in Serverless |
| [**APM Tail-based sampling**](/solutions/observability/apm/transaction-sampling.md#apm-tail-based-sampling) | ✅ | ❌ | - Not available in Serverless <br>- Consider **OpenTelemetry** tail sampling processor as an alternative |
| [**Android agent/SDK instrumentation**](apm-agent-android://reference/edot-android/index.md) | ✅ | ✅ | |
| [**AWS Firehose integration**](/solutions/observability/cloud/monitor-amazon-web-services-aws-with-amazon-data-firehose.md) | ✅ | ✅ | |
| [**Custom roles for Kibana Spaces**](/deploy-manage/manage-spaces.md#spaces-control-user-access) | ✅ | ✅ | |
| [**Data stream lifecycle**](/manage-data/lifecycle/data-stream.md) | ✅ | ✅ | Primary lifecycle management method in Serverless |
| [**EDOT Cloud Forwarder**](opentelemetry://reference/edot-cloud-forwarder/index.md) | ❌ | ✅ | |
| **[Elastic Serverless Forwarder](elastic-serverless-forwarder://reference/index.md)** | ✅ | ❌ | |
| **[Elastic Synthetics Private Locations](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-add)** | ✅ | ✅ | |
| **[Fleet Agent policies](/reference/fleet/agent-policy.md)** | ✅ | ✅ | |
| **[Fleet server](/reference/fleet/fleet-server.md)** | - Self-hosted <br>- Hosted | ✅ | Fully managed by Elastic |
| [**Index lifecycle management**](/manage-data/lifecycle/index-lifecycle-management.md) | ✅ | ❌ | Use [**Data stream lifecycle**](/manage-data/lifecycle/data-stream.md) instead |
| **[iOS agent/SDK instrumentation](apm-agent-ios://reference/edot-ios/index.md)** | ✅ | ✅ | |
| **[Kibana Alerts](/deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md)** | ✅ | ✅ | |
| **[LogsDB index mode](/manage-data/data-store/data-streams/logs-data-stream.md)** | ✅ | ✅ | - Reduces storage footprint <br> - Enabled by default <br>- Cannot be disabled |
| **[Logs management](/solutions/observability/logs.md)** | ✅ | ✅ | |
| **[Metrics monitoring](/solutions/observability/apm/metrics.md)** | ✅ | ✅ | |
| **[Observability SLO](/solutions/observability/incident-management/service-level-objectives-slos.md)** | ✅ | ✅ | |
| [**Real User Monitoring (RUM)**](/solutions/observability/applications/user-experience.md) | ✅ | **Planned** | Anticipated in a future release |
| **[Universal Profiling](/solutions/observability/infra-and-hosts/get-started-with-universal-profiling.md)** | ✅ | ❌ | Not available in Serverless |
| **Uptime monitoring** | ❌ | ❌ | - Deprecated in all deployment types <br>- Use [**Synthetics app**](/solutions/observability/synthetics/index.md) instead |

### Security

This table compares Security capabilities between {{ech}} deployments and Serverless projects:

| **Feature** | {{ech}} | Serverless Security projects | Serverless notes |
|---------|---------------------|------------------------------|------------------|
| **[Advanced Entity Analytics](/solutions/security/advanced-entity-analytics.md)** | ✅ | ✅ | |
| **[AI Assistant](/solutions/security/ai/ai-assistant.md)** | ✅ | ✅ | |
| **[API keys](/deploy-manage/api-keys.md)** | ✅ | ✅ | |
| **[Cloud Security](/solutions/security/cloud.md)** | ✅ | ✅ | |
| [**Defend for Containers integration**](https://www.elastic.co/guide/en/security/8.18/d4c-overview.html) | ✅ (deprecated in 9.0) | ❌ | Not available in Serverless |
| **[Endpoint security](/solutions/security/configure-elastic-defend.md)** | ✅ | ✅ | |
| **[Kibana Alerts](/deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md)** | ✅ | ✅ | |
| **Kibana navigation** | Standard layout | Different layout | UI differences in Security projects |
| **[LogsDB](/manage-data/data-store/data-streams/logs-data-stream.md)** | Optional | ✅ | - Enabled by default <br>- Cannot be disabled |
| **[Native realm authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md)** | ✅ | ❌ | Only API key-based authentication is supported at the project level. User authentication, including SAML SSO, is managed at the [organization level](/deploy-manage/users-roles/cloud-organization.md). |
| **Role-based access control** | ✅ | Limited | Core RBAC functionality supported |
| **SIEM capabilities** | ✅ | ✅ | Core functionality supported |

## Elasticsearch index sizing guidelines [elasticsearch-differences-serverless-index-size]

To ensure optimal performance in Serverless Elasticsearch projects, follow these sizing recommendations:

| **Use case** | Maximum index size | Project configuration |
| --- | --- | --- |
| **Vector search** | 150GB | Vector optimized |
| **General search (non data-stream)** | 300GB | General purpose |
| **Other uses (non data-stream)** | 600GB | General purpose |

If you expect that you will have large datasets that exceed the recommended maximum size, consider creating multiple smaller indices that you can query using an [alias](/manage-data/data-store/aliases.md), or configuring [data stream lifecycle](/manage-data/lifecycle/data-stream.md) to prevent data streams from growing larger than the maximum size. You should design your indexing and data lifecycle strategy with the size and growth of your data in mind.

These recommendations do not apply to indices using better binary quantization (BBQ). Refer to [vector quantization](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) for more information.

## Available {{es}} APIs [elasticsearch-differences-serverless-apis-availability]

In {{serverless-full}}, access is limited to a subset of {{es}} APIs, as Elastic manages the underlying infrastructure. These restrictions help maintain cluster stability, availability, and data integrity, ensuring reliable operation of Serverless projects.

The following {{es}} APIs are not available in {{serverless-full}}:


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

In {{serverless-full}} projects, configuration available to users is limited to certain [index-level settings](elasticsearch://reference/elasticsearch/index-settings/index.md), while Elastic manages cluster-level and node-level settings to maintain stability, availability, performance, and data integrity. These restrictions help ensure the reliability of Serverless projects.

Available settings
:   **Index-level settings**: Settings that control how documents are processed, stored, and searched are available to end users. These include:

    * Analysis configuration
    * Mapping parameters
    * Search/query settings
    * Indexing settings such as `refresh_interval`

  Some settings might have different default values or value constraints in {{serverless-short}}. This information is documented in the [settings reference](elasticsearch://reference/elasticsearch/index-settings/index.md).

Managed settings
:   **Infrastructure-related settings**: Settings that affect cluster resources or data distribution are not available to end users. These include:

    * Node configurations
    * Cluster topology
    * Shard allocation
    * Resource management

When attempting to use an unavailable index setting, you'll receive this error:

```json
{
    "error": {
        "root_cause": [
            {
                "type": "illegal_argument_exception",
                "reason": "Settings [xyz] are not available when running in serverless mode"
            }
        ],
        "type": "illegal_argument_exception",
        "reason": "Settings [xyz] are not available when running in serverless mode"
    },
    "status": 400
}
```

## Learn more

- [{{serverless-full}} roadmap](https://www.elastic.co/cloud/serverless/roadmap): See upcoming features and development plans for the Serverless platform
- [Elasticsearch Serverless API reference](https://www.elastic.co/docs/api/doc/elasticsearch-serverless): Check out the complete list of available APIs in {{serverless-full}}
- [Project settings](/deploy-manage/deploy/elastic-cloud/project-settings.md): Configure project settings in {{serverless-full}}
- [Serverless regions](/deploy-manage/deploy/elastic-cloud/regions.md): Choose the right region for your {{serverless-full}} project
- [{{ecloud}} pricing](https://www.elastic.co/pricing/): Understand pricing for {{ech}} and Serverless projects
  - [Serverless project billing](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md): Understand billing dimensions for Serverless projects
  - [{{ech}} billing](/deploy-manage/cloud-organization/billing/cloud-hosted-deployment-billing-dimensions.md): Understand billing dimensions for {{ech}} deployments
