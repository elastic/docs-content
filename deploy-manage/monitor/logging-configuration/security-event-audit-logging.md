---
applies:
  hosted: all
  ece: all
  eck: all
  stack: all
  serverless: unavailable
---
# Security event audit logging

::::{important}
Audit logs are only available on certain [subscription levels](https://www.elastic.co/subscriptions).
::::

Audit logging is a powerful feature that helps you monitor and track security-related events within the {{stack}}. By enabling audit logs, you can gain visibility into authentication attempts, authorization decisions, and other system activity.

Audit logging also provides forensic evidence in the event of an attack, and can be enabled independently for {{es}} and {{kib}}.

In this section, you'll learn how to:

1. [](./enabling-audit-logs.md): Activate {{es}} or {{kib}} audit logs for all supported deployment types, including self-managed clusters, {{ech}}, {{ece}} (ECE), and {{eck}} (ECK).

2. [](./configuring-audit-logs.md): Filter and control what security events get logged in the audit log output.

3. Optionally, [audit {{es}} search queries](./auditing-search-queries.md): Audit and log search request bodies. 

4. [Correlate audit events](./correlating-kibana-elasticsearch-audit-logs.md): Explore audit logs and understand how events from the same request are correlated.

By following these guidelines, you can effectively audit system activity, enhance security monitoring, and meet compliance requirements.
