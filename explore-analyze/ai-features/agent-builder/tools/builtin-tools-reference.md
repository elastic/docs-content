---
navigation_title: "Built-in tools reference"
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless:
---

# Elastic Agent Builder built-in tools reference

This page lists all built-in tools available in {{agent-builder}} and their availability. Unless otherwise specified, all built-in tools are available within all types of deployments. These tools are available to all [custom agents](/explore-analyze/ai-features/agent-builder/agent-builder-agents.md#create-a-new-agent-in-the-gui).

Built-in tools provide core capabilities for working with {{es}} data. You can't modify or delete them. In the tools overview, the UI organizes built-in tools using labels (called `tags` in the API) such as `observability`, `security`, `apm`, and `alerts` to help you filter and find related tools. To learn more, refer to [find all available tools](/explore-analyze/ai-features/agent-builder/tools.md#find-available-tools).

:::{tip}
For an overview of how tools work in {{agent-builder}}, refer to the [Tools overview](../tools.md).
:::

## Tool naming conventions

Tool naming conventions help organize and identify tools by their source. Built-in tools use consistent prefixes such as `platform.core`, `observability`, and `security`. This convention:

- Prevents naming conflicts between system and custom tools
- Makes it easy to identify tool sources
- Provides a consistent pattern for tool identification

## Platform core tools

Platform Core tools provide fundamental capabilities for interacting with {{es}} data, executing queries, and working with indices. They are relevant to many use cases.

`platform.core.execute_esql` {applies_to}`stack: ga 9.2+`
:   Executes an [{{esql}}](elasticsearch://reference/query-languages/esql.md) query and returns the results in a tabular format.

`platform.core.generate_esql` {applies_to}`stack: ga 9.2+`
:   Generates an [{{esql}}](elasticsearch://reference/query-languages/esql.md) query from a natural language query.

`platform.core.get_document_by_id` {applies_to}`stack: ga 9.2+`
:   Retrieves the full content of an {{es}} document based on its ID and index name.

`platform.core.get_index_mapping` {applies_to}`stack: ga 9.2+`
:   Retrieves mappings for the specified index or indices.

`platform.core.index_explorer` {applies_to}`stack: ga 9.2+`
:   Lists relevant indices and corresponding mappings based on a natural language query.

`platform.core.list_indices` {applies_to}`stack: ga 9.2+`
:   Lists the indices, aliases, and data streams in the {{es}} cluster the current user has access to.

`platform.core.search` {applies_to}`stack: ga 9.2+`
:   Searches and analyzes data within your {{es}} cluster using full-text relevance searches or structured analytical queries.

`platform.core.product_documentation` {applies_to}`stack: ga 9.3+`
:   Searches and retrieves documentation about Elastic products ({{kib}}, Elasticsearch, Elastic Security, Elastic Observability).

`platform.core.integration_knowledge` {applies_to}`stack: ga 9.3+`
:   Searches and retrieves knowledge from [{{fleet}}](/reference/fleet/index.md)-installed integrations, including information on how to configure and use integrations for data ingestion.

`platform.core.create_visualization` {applies_to}`stack: ga 9.3+`
:   Creates a [Lens](/explore-analyze/visualize/lens.md) visualization based on specifications.

`platform.core.cases` {applies_to}`stack: ga 9.3+`
:   Searches and retrieves [cases](/explore-analyze/alerts-cases/cases.md) for tracking and managing issues.

`platform.core.get_workflow_execution_status` {applies_to}`stack: ga 9.3+`
:   Retrieves the execution status of a workflow.

### Attachment tools
```{applies_to}
stack: ga 9.3+
```

% TODO are these available in 9.3?

The following tools manage file attachments in conversations:

`platform.core.attachment_read`
:   Reads the content of a file attachment.

`platform.core.attachment_update`
:   Updates the content of a file attachment.

`platform.core.attachment_add`
:   Adds a new file attachment to the conversation.

`platform.core.attachment_list`
:   Lists all file attachments in the conversation.

`platform.core.attachment_diff`
:   Shows the differences between versions of a file attachment.

## Dashboard tools
```{applies_to}
stack: ga 9.3+
```

Dashboard tools enable agents to create and manage [Dashboards](/explore-analyze/dashboards.md).

`dashboard.create_dashboard`
:   Creates a dashboard with specified title, description, panels, and markdown summary.

`dashboard.update_dashboard`
:   Updates an existing dashboard with new panels or modifications.

## Observability tools
```{applies_to}
stack: ga 9.3+
```

% TODO mention that the built-in Observability agent is assigned these tools

Observability tools provide specialized capabilities for monitoring applications, infrastructure, and logs.

`observability.get_alerts`
:   Retrieves Observability [alerts](/solutions/observability/incident-management/alerting.md) within a specified time range, supporting filtering by status (active/recovered) and KQL queries.

`observability.get_services`
:   Retrieves information about services being monitored in [APM](/solutions/observability/apm/index.md).

`observability.get_hosts`
:   Retrieves information about hosts being monitored in infrastructure monitoring.

`observability.get_data_sources`
:   Retrieves available Observability data sources and their configuration.

`observability.get_trace_metrics`
:   Retrieves metrics and statistics for distributed traces.

`observability.get_downstream_dependencies`
:   Identifies downstream dependencies (other services, databases, external APIs) for a specific service to understand service topology and blast radius.

`observability.get_log_categories`
:   Retrieves categorized log patterns to identify common log message types.

`observability.get_log_change_points`
:   Detects statistically significant changes in log patterns and volumes.

`observability.get_metric_change_points`
:   Detects statistically significant changes in metrics across groups (for example, by service, host, or custom fields), identifying spikes, dips, step changes, and trend changes.

`observability.get_correlated_logs`
:   Finds logs that are correlated with a specific event or time period.

`observability.run_log_rate_analysis`
:   Analyzes log ingestion rates to identify anomalies and trends.

`observability.get_anomaly_detection_jobs`
:   Retrieves {{ml-app}} [{{anomaly-jobs}}](/explore-analyze/machine-learning/anomaly-detection.md) and their top anomaly records for investigating outliers and abnormal behavior.

## Security tools
```{applies_to}
stack: ga 9.3+
```

% TODO mention that the built-in Security agent is assigned these tools

Security tools provide specialized capabilities for security monitoring, threat detection, and incident response.

`security.alerts`
:   Searches and analyzes security alerts using full-text or structured queries for finding, counting, aggregating, or summarizing alerts.

`security.entity_risk_score`
:   Retrieves [risk scores for entities](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md) (users, hosts, and services) to identify high-risk entities in the environment.

`security.attack_discovery_search`
:   Returns any related [attack discoveries](/solutions/security/ai/attack-discovery.md) from the last week, given one or more alert IDs.

`security.security_labs_search`
:   Searches [Elastic Security Labs](https://www.elastic.co/security-labs) research and threat intelligence content.

## Related pages

- [Tools in {{agent-builder}}](../tools.md)
- [Custom ES|QL tools](esql-tools.md)
- [Custom index search tools](index-search-tools.md)