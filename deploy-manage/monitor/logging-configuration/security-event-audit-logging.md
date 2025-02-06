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

Audit logging also provides forensic evidence in the event of an attack, and can be enabled independently for {{es}} and {{kib}}.

Use the {{kib}} audit logs in conjunction with {{es}} audit logging to get a holistic view of all security related events. {{kib}} defers to the {{es}} security model for authentication, data index authorization, and features that are driven by cluster-wide privileges.

This section provides a comprehensive guide to [enable](./enabling-audit-logs.md) and [configure](./enabling-audit-logs.md#audit-logging-configuration) audit logging in {{es}} and {{kib}} across all supported deployment types, including self-managed clusters, Elastic Cloud Hosted, Elastic Cloud Enterprise (ECE), and Elastic Cloud on Kubernetes (ECK).

By following these guidelines, you can effectively audit system behavior, enhance security monitoring, and meet compliance requirements.

## Optimizing audit logging for effective security monitoring [audit-logging-recommendations]

When auditing security events, a single client request might generate multiple audit events across multiple cluster nodes, potentially leading to a high volume of log data. To maintain clarity and ensure logs remain actionable, {{es}} and {{kib}} provide configuration mechanisms to control what events are logged and which can be ignored.

To make audit logs useful and manageable to your use case, we recommend:
  * Spending some time **analyzing what gets logged** to ensure relevant events are captured.
  * **Measuring the performance impact** of audit logging on your environment, as I/O activity can be significant depending on your use case. Refer to [](./logfile-audit-events-ignore-policies.md) for more details.
  * **Tuning the audit logging configuration** by using include/exclude filters, ignore policies, and query auditing options, to reduce unnecessary noise. Refer to [](./enabling-audit-logs.md#audit-logging-configuration) for more information.
  * **Balancing verbosity with security requirements**, to ensure relevant events are captured without excessive log volume.

## Correlating audit events

This section explains the main fields that help correlate events and understand their relationships more effectively.  

### `request.id` attribute in {{es}} audit events

When a request generates multiple audit events across multiple nodes, you can use the `request.id` attribute to correlate the associated events.

This identifier allows you to trace the flow of a request across the {{es}} cluster and reconstruct the full context of an operation.

Refer to [](./elasticsearch-audit-events.md) for a complete reference of event types and attributes.

### `trace.id` field in {{kib}} audit events

In {{kib}}, the [trace.id](https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html#field-trace-id) field allows to correlate multiple events that originate from the same request.

Additionally, this field helps correlate also events from one request with the backend calls that create {{es}} audit events. When {{kib}} sends requests to {{es}}, the `trace.id` value is propagated and stored in the `opaque_id` attribute of {{es}} audit logs, allowing cross-component correlation.

For an example of correlating {{es}} and {{kib}} audit logs, refer to [](./correlating-kibana-elasticsearch-audit-logs.md)