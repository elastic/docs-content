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

| Feature | Description | Availability |
|---|---|---|
| [](./stack-audit-logging.md) | Enable and configure audit logging for {{es}} and {{kib}} deployments. | {applies_to}`stack: ga` |
| [](./cloud-audit-trail.md) | Audit organization-level actions such as deployment management, API key usage, and sign-in activity. | {applies_to}`ech: ga` {{fedramp-mod}} only |

## Query and performance logging

| Feature | Description | Availability |
|---|---|---|
| [](./logging-configuration/query-logs.md) | Log every search, {{esql}}, SQL, or EQL query for analysis and debugging. | {applies_to}`stack: ga` |
| [](./logging-configuration/slow-logs.md) | Identify slow queries and indexing operations. | {applies_to}`stack: ga` |
