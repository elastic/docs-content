---
navigation_title: Correlate audit events
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html
applies:
  hosted: all
  ece: all
  eck: all
  stack: all
  serverless: unavailable
---

# Correlating audit events [xpack-security-ecs-audit-correlation]

When audit logs are enabled, a single request to {{kib}} or {{es}} generates multiple audit events in the logs.

Audit events from {{kib}} can also be correlated with backend calls that produce {{es}} audit events, allowing for a more comprehensive view of user actions.

This section explains the key fields that help correlate these events, with examples to illustrate their relationships.

## `request.id` attribute in {{es}} audit events

When an {{es}} request generates multiple audit events across multiple nodes, you can use the `request.id` attribute to correlate the associated events.

This identifier allows you to trace the flow of a request across the {{es}} cluster and reconstruct the full context of an operation.

Refer to [linkTBD]() asciidocalypse://elasticsearch/docs/reference/elasticsearch/elasticsearch-audit-events for a complete reference of event types and attributes.

## `trace.id` field in {{kib}} audit events

In {{kib}}, the [trace.id](https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html#field-trace-id) field allows to correlate multiple events that originate from the same request.

Additionally, this field helps correlate events from one request with the backend calls that create {{es}} audit events. When {{kib}} sends requests to {{es}}, the `trace.id` value is propagated and stored in the `opaque_id` attribute of {{es}} audit logs, allowing cross-component correlation.

Refer to [{{kib}} audit events](https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html#xpack-security-ecs-audit-logging) for a complete description of {{kib}} auditing events.

## Examples

This section shows practical examples of correlating audit logs.

::::{note}
The examples below are simplified. Many fields have been omitted and values have been shortened for clarity.
::::

### Example 1: correlating multiple {{kib}} audit events [_example_1_correlating_multiple_kib_audit_events]

When "thom" creates a new alerting rule, five audit events are written:

```json
{"event":{"action":"http_request","category":["web"],"outcome":"unknown"},"http":{"request":{"method":"post"}},"url":{"domain":"localhost","path":"/api/alerting/rule","port":5601,"scheme":"https"},"user":{"name":"thom","roles":["superuser"]},"kibana":{"space_id":"default","session_id":"3dHCZRB..."},"@timestamp":"2022-01-25T13:05:34.449-05:00","message":"User is requesting [/api/alerting/rule] endpoint","trace":{"id":"e300e06..."}}
{"event":{"action":"space_get","category":["database"],"type":["access"],"outcome":"success"},"kibana":{"space_id":"default","session_id":"3dHCZRB...","saved_object":{"type":"space","id":"default"}},"user":{"name":"thom","roles":["superuser"]},"@timestamp":"2022-01-25T13:05:34.454-05:00","message":"User has accessed space [id=default]","trace":{"id":"e300e06..."}}
{"event":{"action":"connector_get","category":["database"],"type":["access"],"outcome":"success"},"kibana":{"space_id":"default","session_id":"3dHCZRB...","saved_object":{"type":"action","id":"5e3b1ae..."}},"user":{"name":"thom","roles":["superuser"]},"@timestamp":"2022-01-25T13:05:34.948-05:00","message":"User has accessed connector [id=5e3b1ae...]","trace":{"id":"e300e06..."}}
{"event":{"action":"connector_get","category":["database"],"type":["access"],"outcome":"success"},"kibana":{"space_id":"default","session_id":"3dHCZRB...","saved_object":{"type":"action","id":"5e3b1ae..."}},"user":{"name":"thom","roles":["superuser"]},"@timestamp":"2022-01-25T13:05:34.956-05:00","message":"User has accessed connector [id=5e3b1ae...]","trace":{"id":"e300e06..."}}
{"event":{"action":"rule_create","category":["database"],"type":["creation"],"outcome":"unknown"},"kibana":{"space_id":"default","session_id":"3dHCZRB...","saved_object":{"type":"alert","id":"64517c3..."}},"user":{"name":"thom","roles":["superuser"]},"@timestamp":"2022-01-25T13:05:34.956-05:00","message":"User is creating rule [id=64517c3...]","trace":{"id":"e300e06..."}}
```

All of these audit events can be correlated together by the same `trace.id` value `"e300e06..."`. The first event is the HTTP API call, the next audit events are checks to validate the space and the connectors, and the last audit event is the actual rule creation.


### Example 2: correlating a {{kib}} audit event with {{es}} audit events [_example_2_correlating_a_kib_audit_event_with_es_audit_events]

When "thom" logs in, a "user_login" {{kib}} audit event is written:

```json
{"event":{"action":"user_login","category":["authentication"],"outcome":"success"},"kibana":{"session_id":"ab93zdA..."},"user":{"name":"thom","roles":["superuser"]},"@timestamp":"2022-01-25T09:40:39.267-05:00","message":"User [thom] has logged in using basic provider [name=basic]","trace":{"id":"818cbf3..."}}
```

The `trace.id` value `"818cbf3..."` in the {{kib}} audit event can be correlated with the `opaque_id` value in these six {{es}} audit events:

```json
{"type":"audit", "timestamp":"2022-01-25T09:40:38,604-0500", "event.action":"access_granted", "user.name":"thom", "user.roles":["superuser"], "request.id":"YCx8wxs...", "action":"cluster:admin/xpack/security/user/authenticate", "request.name":"AuthenticateRequest", "opaque_id":"818cbf3..."}
{"type":"audit", "timestamp":"2022-01-25T09:40:38,613-0500", "event.action":"access_granted", "user.name":"kibana_system", "user.roles":["kibana_system"], "request.id":"Ksx73Ad...", "action":"indices:data/write/index", "request.name":"IndexRequest", "indices":[".kibana_security_session_1"], "opaque_id":"818cbf3..."}
{"type":"audit", "timestamp":"2022-01-25T09:40:38,613-0500", "event.action":"access_granted", "user.name":"kibana_system", "user.roles":["kibana_system"], "request.id":"Ksx73Ad...", "action":"indices:data/write/bulk", "request.name":"BulkRequest", "opaque_id":"818cbf3..."}
{"type":"audit", "timestamp":"2022-01-25T09:40:38,613-0500", "event.action":"access_granted", "user.name":"kibana_system", "user.roles":["kibana_system"], "request.id":"Ksx73Ad...", "action":"indices:data/write/bulk[s]", "request.name":"BulkShardRequest", "indices":[".kibana_security_session_1"], "opaque_id":"818cbf3..."}
{"type":"audit", "timestamp":"2022-01-25T09:40:38,613-0500", "event.action":"access_granted", "user.name":"kibana_system", "user.roles":["kibana_system"], "request.id":"Ksx73Ad...", "action":"indices:data/write/index:op_type/create", "request.name":"BulkItemRequest", "indices":[".kibana_security_session_1"], "opaque_id":"818cbf3..."}
{"type":"audit", "timestamp":"2022-01-25T09:40:38,613-0500", "event.action":"access_granted", "user.name":"kibana_system", "user.roles":["kibana_system"], "request.id":"Ksx73Ad...", "action":"indices:data/write/bulk[s][p]", "request.name":"BulkShardRequest", "indices":[".kibana_security_session_1"], "opaque_id":"818cbf3..."}
```

The {{es}} audit events show that "thom" authenticated, then subsequently "kibana_system" created a session for that user.
