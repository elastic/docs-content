---
navigation_title: "Built-in tools"
description: "Reference of all built-in tools available in Elastic Agent Builder."
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

<!-- Note: This file contains commented-out tool sections for features on main that are not yet available in released versions. -->

# {{agent-builder}} built-in tools reference

This page lists all built-in tools available in {{agent-builder}}. Built-in tools enable core operations for working with {{es}} data across platform, observability, and security use cases out-of-the-box.

Built-in tools are read-only: you can't modify or delete them. To check which tools are available in your Elastic deployment, refer to [Manage tools](/explore-analyze/ai-features/agent-builder/tools.md#manage-tools).

:::{tip}
For an overview of how tools work in {{agent-builder}}, refer to the [Tools overview](../tools.md).
:::

## Availability

Built-in platform core tools are available across all deployments, while observability and security tools are available in their respective serverless projects (or solution views). Tools use consistent prefixes (`platform.core`, `observability`, `security`) that reflect this scoping.

## Agents and tools

[Built-in agents](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md) are pre-configured with relevant tools. For example, the Observability agent includes all observability tools by default. You can assign any available built-in tools to [custom agents](/explore-analyze/ai-features/agent-builder/custom-agents.md#create-a-new-agent) you create.

## Platform core tools
```{applies_to}
stack: preview =9.2, ga 9.3
serverless:
  elasticsearch: ga
  observability: ga
  security: ga
```

Platform core tools provide fundamental capabilities for interacting with {{es}} data, executing queries, and working with indices. They are relevant to many use cases.

:::{note}
All [built-in agents](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md) are assigned these tools by default.
:::

`platform.core.execute_esql`
:   Executes an [{{esql}}](elasticsearch://reference/query-languages/esql.md) query and returns the results in a tabular format.

`platform.core.generate_esql`
:   Generates an [{{esql}}](elasticsearch://reference/query-languages/esql.md) query from a natural language query.

`platform.core.get_document_by_id`
:   Retrieves the full content of an {{es}} document based on its ID and index name.

`platform.core.get_index_mapping`
:   Retrieves mappings for the specified index or indices.

`platform.core.index_explorer`
:   Lists relevant indices and corresponding mappings based on a natural language query.

`platform.core.list_indices`
:   Lists the indices, aliases, and data streams in the {{es}} cluster the current user has access to.

`platform.core.search`
:   Searches and analyzes data within your {{es}} cluster using full-text relevance searches or structured analytical queries.

$$$agent-builder-product-documentation-tool$$$ `platform.core.product_documentation` {applies_to}`stack: ga 9.3+`
:   Searches and retrieves documentation about Elastic products. To use this tool, search for **GenAI Settings** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) and install **Elastic documentation** from the **Documentation** section. This takes a few minutes.

`platform.core.integration_knowledge` {applies_to}`stack: ga 9.3+`
:   Searches and retrieves knowledge from [{{fleet}}](/reference/fleet/index.md)-installed integrations, including information on how to configure and use integrations for data ingestion.

<!-- `platform.core.create_visualization` {applies_to}`stack: ga 9.4+`
:   Creates a [Lens](/explore-analyze/visualize/lens.md) visualization based on specifications. -->

`platform.core.cases` {applies_to}`stack: ga 9.3+`
:   Searches and retrieves [cases](/explore-analyze/alerts-cases/cases.md) for tracking and managing issues.

`platform.core.get_workflow_execution_status` {applies_to}`stack: ga 9.3+`
:   Retrieves the execution status of a workflow.

<!--
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
-->

<!-- 
## Dashboard tools
```{applies_to}
stack: ga 9.4+
```

Dashboard tools enable agents to create and manage [Dashboards](/explore-analyze/dashboards.md).

`dashboard.create_dashboard`
:   Creates a dashboard with specified title, description, panels, and markdown summary.

`dashboard.update_dashboard`
:   Updates an existing dashboard with new panels or modifications. 
-->

## Observability tools
```{applies_to}
stack: ga 9.3+
serverless:
  observability: ga
```

Observability tools provide specialized capabilities for monitoring applications, infrastructure, and logs.

:::{note}
The [built-in Observability agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#observability-agent) is assigned these tools by default.
:::

`observability.get_alerts`
:   Retrieves Observability [alerts](/solutions/observability/incident-management/alerting.md) within a specified time range, supporting filtering by status (active/recovered) and KQL queries.

`observability.get_services`
:   Retrieves information about services being monitored in [APM](/solutions/observability/apm/index.md).

`observability.get_hosts`
:   Retrieves information about hosts being monitored in infrastructure monitoring.

`observability.get_index_info`
:   Retrieves information about Observability indices and their fields. Supports operations for getting an overview of available data sources, listing fields that contain actual data, and retrieving distinct values or ranges for specific fields.

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
serverless: 
  security: ga
```

Security tools provide specialized capabilities for security monitoring, threat detection, and incident response.

:::{note}
The [built-in Threat Hunting Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#threat-hunting-agent) is assigned these tools by default.
:::

`security.alerts`
:   Searches and analyzes security alerts using full-text or structured queries for finding, counting, aggregating, or summarizing alerts.

<!-- `security.entity_risk_score`
:   Retrieves [risk scores for entities](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md) (users, hosts, and services) to identify high-risk entities in the environment. -->

<!-- `security.attack_discovery_search`
:   Returns any related [attack discoveries](/solutions/security/ai/attack-discovery.md) from the last week, given one or more alert IDs.-->

$$$agent-builder-security-labs-search-tool$$$ `security.security_labs_search`
:   Searches [Elastic Security Labs](https://www.elastic.co/security-labs) research and threat intelligence content. To use this tool, search for **GenAI Settings** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) and install **Security labs** from the **Documentation** section. This takes a few minutes.

:::{tip}
You can also manage tools programmatically. To learn more, refer to [Tools API](../tools.md#tools-api).
:::

## Related pages

- [Tools in {{agent-builder}}](../tools.md)
- [Custom ES|QL tools](esql-tools.md)
- [Custom index search tools](index-search-tools.md)

