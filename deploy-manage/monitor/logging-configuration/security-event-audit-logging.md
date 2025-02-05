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

::::{important}
Audit logs are only available on certain [subscription levels](https://www.elastic.co/subscriptions).
::::

Audit logging is a powerful feature that helps you monitor and track security-related events within the {{stack}}. By enabling audit logs, you can gain visibility into authentication attempts, authorization decisions, and other system activity.

This section provides a comprehensive guide to configuring and using audit logging in Elasticsearch and Kibana across all supported deployment types, including self-managed clusters, Elastic Cloud, Elastic Cloud Enterprise (ECE), and Elastic Cloud on Kubernetes (ECK).

In this section you will learn how to:

* Enable {{es}} audit logs for all supported deployment types.

* Enable {{kib}} audit logs to track authentication, API access, and administrative actions.

* Configure {{es}} audit logging framework by using [include/exclude filters](elasticsearch-audit-events.md), [ignore policies](logfile-audit-events-ignore-policies.md), and [search queries auditing](auditing-search-queries.md).

* Correlating {{kib}} and {{es}} audit events to gain a complete view of security-related activities.

By following these guidelines, you can effectively audit system behavior, enhance security monitoring, and meet compliance requirements.

Use the {{kib}} audit logs in conjunction with {{es}} audit logging to get a holistic view of all security related events. {{kib}} defers to the {{es}} security model for authentication, data index authorization, and features that are driven by cluster-wide privileges.