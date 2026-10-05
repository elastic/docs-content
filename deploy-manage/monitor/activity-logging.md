---
applies_to:
  stack: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: cloud-serverless
  - id: elastic-stack
---
# Activity logging

Activity logging records actions taken by users and systems in your Elastic environment, such as authentication events, search queries, and configuration changes. Use these logs for security auditing, compliance, debugging, and performance investigation.

:::{admonition} Looking for application and component logging? 
You can enable {{es}} and {{kib}} logging features to gain insight into {{stack}} operations and diagnose issues. To configure these logs, refer to [](/deploy-manage/monitor/logging-configuration.md).
:::

## Audit logging

Audit logging tracks security-related events such as authentication attempts, authorization decisions, and configuration changes. 

Stack audit logging records security events inside your cluster. Cloud audit trail records organization-level actions around your deployments. On FedRAMP environments, use both for full coverage.

| Feature | Description | Availability |
|---|---|---|
| [](./stack-audit-logging.md) | Enable and configure audit logging for {{es}} and {{kib}} deployments. | {applies_to}`stack: ga` |
| [](./cloud-audit-trail.md) | Audit organization-level actions such as sign-in activity, deployment management, user and role changes, and API key usage. | {applies_to}`ech: ga` {{fedramp-mod}} only |

## Query and performance logging

Query and performance logging helps you understand how queries perform and identify operations that need optimization. Use these logs to debug slow queries, audit search activity, and analyze indexing performance.

For search operations, query logging is the recommended approach because it captures end-to-end request duration across all query types with a single configuration. Slow logs measure shard-level execution time and are the only option for indexing operations.

| Feature | Description | Availability |
|---|---|---|
| [](./logging-configuration/query-logs.md) | Log every search, {{esql}}, SQL, or EQL query for analysis and debugging. | {applies_to}`stack: preview 9.4` |
| [](./logging-configuration/slow-logs.md) | Identify slow queries and indexing operations. | {applies_to}`stack: ga` |

If query logging is not available in your {{stack}} version, [audit logging](./stack-audit-logging/enabling-audit-logs.md) can also capture query sources.

:::{tip}
Activity logs record events for later analysis. For real-time visibility into running queries, use [Query activity](./query-activity.md). For real-time cluster health and performance monitoring, refer to the [monitoring tools](/deploy-manage/monitor.md) available for your deployment type.
:::