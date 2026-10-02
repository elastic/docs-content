---
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
  serverless: unavailable
products:
  - id: elasticsearch
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---
# Security event audit logging

::::{important}
Audit logs are only available on certain [subscription levels](https://www.elastic.co/subscriptions).
::::

:::{include} /deploy-manage/security/_snippets/audit-logging.md
:::

:::{tip}
In {{fedramp-mod}} environments, you can also audit organization-level actions such as deployment management, API key usage, and sign-in activity. Refer to [](/deploy-manage/monitor/log-delivery/cloud-audit-trail.md).
:::

Use the {{kib}} audit logs in conjunction with {{es}} audit logging to get a holistic view of all security related events. {{kib}} defers to the {{es}} security model for authentication, data index authorization, and features that are driven by cluster-wide privileges.

In this section, you'll learn how to:

* [](./enabling-audit-logs.md): Activate {{es}} or {{kib}} audit logs for all supported deployment types.

* [](./configuring-audit-logs.md): Filter and control what security events get logged in the audit log output.

* [Audit {{es}} search queries](./auditing-search-queries.md): Audit and log search request bodies.

* [Correlate audit events](./correlating-kibana-elasticsearch-audit-logs.md): Explore audit logs and understand how events from the same request are correlated.

By following these guidelines, you can effectively audit system activity, enhance security monitoring, and meet compliance requirements.

For a complete description of audit event details and format, refer to:

* [{{es}} audit events](elasticsearch://reference/elasticsearch/elasticsearch-audit-events.md)
* [{{kib}} audit events](kibana://reference/kibana-audit-events.md)
