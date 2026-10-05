---
applies_to:
  serverless:
  stack:
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

Activity logging gives you visibility into what's happening in your Elastic environment. Use it to track security events, monitor query performance, and identify slow operations.

## Audit logging

Audit logging tracks security-related events such as authentication attempts, authorization decisions, and configuration changes.

* [](./stack-audit-logging.md): Enable and configure audit logging for {{es}} and {{kib}} deployments.
* [](./cloud-audit-trail.md): Audit organization-level actions in {{fedramp-mod}} environments, such as deployment management, API key usage, and sign-in activity.

## Query and performance logging

* [](./logging-configuration/query-logs.md): Log every search, {{esql}}, SQL, or EQL query for analysis and debugging.
* [](./logging-configuration/slow-logs.md): Identify slow queries and indexing operations.
