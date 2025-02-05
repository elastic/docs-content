---
applies:
  hosted: all
  ece: all
  eck: all
  stack: all
---
# Security event audit logging

% What needs to be done: Write from scratch
% GitHub issue: https://github.com/elastic/docs-projects/issues/350
% Scope notes: Landing page about audit logs in Kibana and Elasticsearch, explaining how they can be enabled and configured, and also linking to the page about correlating information. We can create a doc to explain how to enable audit logging in both Elasticsearch and Kibana, and considering also ECE and orchestrated deployments. Kibana audit events list should be moved to reference content.

% consider organizing the architecture in a better way, separating configuration pages from visualizing pages if needed...

::::{important}
Audit logs are only available on certain [subscription levels](https://www.elastic.co/subscriptions).
::::

Audit logging is a powerful feature that helps you monitor and track security-related events within the {{stack}}. By enabling audit logs, you can gain visibility into authentication attempts, authorization decisions, and other system activity.

Audit logging also provides forensic evidence in the event of an attack.

Use the {{kib}} audit logs in conjunction with {{es}} audit logging to get a holistic view of all security related events. {{kib}} defers to the {{es}} security model for authentication, data index authorization, and features that are driven by cluster-wide privileges.

This section provides a comprehensive guide to configure and use audit logging in {{es}} and {{kib}} across all supported deployment types, including self-managed clusters, Elastic Cloud Hosted, Elastic Cloud Enterprise (ECE), and Elastic Cloud on Kubernetes (ECK).

In this section you will learn how to:

* [Enable {{es}} audit logs](./enabling-audit-logs.md#enable-audit-logging-elasticsearch).

* [Enable {{kib}} audit logs](./enabling-audit-logs.md#enable-audit-logging-kibana).

* [Enable audit logs on orchestrated deployments](./enabling-audit-logs.md#enable-audit-logging-orchestrated).

* [Configure audit logging](./enabling-audit-logs.md#audit-logging-configuration) to control the events that should be logged. 

* [Correlate {{kib}} and {{es}} audit events](./correlating-kibana-elasticsearch-audit-logs.md) to gain a complete view of security-related activities.

By following these guidelines, you can effectively audit system behavior, enhance security monitoring, and meet compliance requirements.