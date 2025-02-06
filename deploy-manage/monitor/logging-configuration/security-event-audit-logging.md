---
applies:
  hosted: all
  ece: all
  eck: all
  stack: all
---
# Security event audit logging

::::{important}
Audit logs are only available on certain [subscription levels](https://www.elastic.co/subscriptions).
::::

Audit logging is a powerful feature that helps you monitor and track security-related events within the {{stack}}. By enabling audit logs, you can gain visibility into authentication attempts, authorization decisions, and other system activity.

Audit logging also provides forensic evidence in the event of an attack, and can be enabled independently for {{es}} and {{kib}}.

Use the {{kib}} audit logs in conjunction with {{es}} audit logging to get a holistic view of all security related events. {{kib}} defers to the {{es}} security model for authentication, data index authorization, and features that are driven by cluster-wide privileges.

This section provides a comprehensive guide to [enable](./enabling-audit-logs.md) and [configure](./enabling-audit-logs.md#audit-logging-configuration) audit logging in {{es}} and {{kib}} across all supported deployment types, including self-managed clusters, Elastic Cloud Hosted, Elastic Cloud Enterprise (ECE), and Elastic Cloud on Kubernetes (ECK).

By following these guidelines, you can effectively audit system behavior, enhance security monitoring, and meet compliance requirements.

## Optimizing audit logging for effective security monitoring [audit-logging-recommendations]

When auditing security events, a single client request might generate multiple audit events across multiple cluster nodes, potentially leading to a high volume of log data and *I/O operations*. To maintain clarity and ensure logs remain actionable, {{es}} and {{kib}} provide configuration mechanisms to control what events are logged and which can be ignored.

Refer to [](./enabling-audit-logs.md#audit-logging-configuration) for more details.

Balancing verbosity, performance, and security requirements is essential to capture relevant events without generating excessive log volume.

## Correlating audit events

This section explains the main fields that help correlate events and understand their relationships more effectively.  

### `request.id` attribute in {{es}} audit events

When a request generates multiple audit events across multiple nodes, you can use the `request.id` attribute to correlate the associated events.

This identifier allows you to trace the flow of a request across the {{es}} cluster and reconstruct the full context of an operation.

Refer to [](./elasticsearch-audit-events.md) for a complete reference of event types and attributes.

### `trace.id` field in {{kib}} audit events

In {{kib}}, the [trace.id](https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html#field-trace-id) field allows to correlate multiple events that originate from the same request.

Additionally, this field helps correlate events from one request with the backend calls that create {{es}} audit events. When {{kib}} sends requests to {{es}}, the `trace.id` value is propagated and stored in the `opaque_id` attribute of {{es}} audit logs, allowing cross-component correlation.

For an example of correlating {{es}} and {{kib}} audit logs, refer to [](./correlating-kibana-elasticsearch-audit-logs.md).

Refer to [{{kib}} audit events](https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html#xpack-security-ecs-audit-logging) for a complete description of {{kib}} auditing events.
