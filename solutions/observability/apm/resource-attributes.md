---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-open-telemetry-resource-attributes.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-agents-opentelemetry-resource-attributes.html
applies_to:
  stack:
  serverless:
---

# Resource attributes [apm-open-telemetry-resource-attributes]

A resource attribute is a key-value pair containing information about the entity producing telemetry. Resource attributes are mapped to Elastic Common Schema (ECS) fields like `service.*`, `cloud.*`, `process.*`, and so on. These fields describe the service and the environment that the service runs in.

The examples set the Elastic (ECS) `service.environment` field for the resource that's producing trace events. Elastic maps the OpenTelemetry `deployment.environment` field to the ECS `service.environment` field on ingestion.

## Setting resource attributes

You can set resource attributes through the environment variables or by editing the configuration of the resource processor of the Collector.

### OpenTelemetry configuration

Use the `OTEL_RESOURCE_ATTRIBUTES` environment variable to pass resource attributes at process invocation. For example:

```bash
export OTEL_RESOURCE_ATTRIBUTES=deployment.environment=production
```

### Resource processor

Use the [resource processor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourceprocessor) to set or apply changes to resource attributes.

```yaml
...
processors:
  resource:
    attributes:
    - key: deployment.environment
      action: insert
      value: production
...
```

## OTel resource attribute to ECS field mapping

The following table summarizes the mapping between OpenTelemetry resource attributes and Elastic Common Schema (ECS) fields.

| OTel Attribute                          | ECS Field                               |
|-----------------------------------------|-----------------------------------------|
| `http.method`                           | `http.method`                           |
| `http.url`, `http.target`, `http.path`  | `url.original`                          |
| `http.host`                             | `host.hostname`                         |
| `http.scheme`                           | `url.scheme`                            |
| `http.status_code`                      | `http.response.status_code`             |
| `http.user_agent`                       | `user_agent.original`                   |
| `net.peer.name`, `net.peer.ip`          | `source.domain`, `source.ip`            |
| `net.peer.port`                         | `source.port`                           |
| `net.host.name`                         | `host.hostname`                         |
| `net.host.port`                         | `host.port`                             |
| `db.system`                             | `span.db.type`                          |
| `db.name`, `db.instance`                | `span.db.instance`                      |
| `db.statement`                          | `span.db.statement`                     |
| `rpc.system`                            | `rpc.system`                            |
| `rpc.service`                           | `rpc.service`                           |
| `rpc.method`                            | `rpc.method`                            |
| `messaging.system`                      | `span.messaging.system`                 |
| `messaging.destination`                 | `span.messaging.destination.name`       |
| `messaging.operation`                   | `span.messaging.operation`              |
| `service.name`                          | `service.name`                          |
| `service.version`                       | `service.version`                       |
| `service.instance.id`                   | `service.instance.id`                   |
| `exception.type`                        | `error.type`                            |
| `exception.message`                     | `error.message`                         |
| `exception.stacktrace`                  | `error.stacktrace`                      |
| `data_stream.dataset`                   | `data_stream.dataset`                   |
| `data_stream.namespace`                 | `data_stream.namespace`                 |


### Handling of unmapped attributes

When an attribute doesn't have a direct ECS field mapping, the system stores it under the `labels` namespace and replaces dots with underscores in the attribute key to comply with field name limitations.

For example, if an OpenTelemetry resource contains:

```json
{
  "service.name": "user-service",
  "deployment.environment": "production",
  "otel.library.name": "my-lib",
  "custom.attribute.with.dots": "value"
}
```

Elastic APM stores the following:

```json
{
  "service.name": "user-service",
  "service.environment": "production",
  "labels": {
    "otel_library_name": "my-lib",
    "custom_attribute_with_dots": "value"
  }
}
```

### Conditional attribute translation

Some OpenTelemetry attributes are conditionally converted based on their value type.

The following table shows how OpenTelemetry resource attributes are converted.

# Conditionally Converted Attributes in `traces.go`

This document lists the conditionally converted attributes in the `traces.go` file. It details the source OpenTelemetry (OTel) attributes, their corresponding Elastic Common Schema (ECS) fields, and the transformation or conversion applied.
# Conditionally Converted Attributes in `traces.go`

This document lists the conditionally converted attributes in the `traces.go` file. It details the source OpenTelemetry (OTel) attributes, their corresponding Elastic Common Schema (ECS) fields, and the transformation or conversion applied.

| OTel Attribute                                      | ECS Field                                 | Comment                                                                                                                                                                                                                                                |
|----------------------------------------------------|-------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `http.scheme`, `http.host`, `http.target`, `http.url`, `http.path`, `http.query` | `event.Url`                               | Constructs the URL by combining the scheme, host, and target attributes. Uses `http.url` if provided.                                                                                                           |
| `http.status_code`, `http.response.status_code`    | `http.Response.StatusCode`               | Converts the status code directly into the ECS field.                                                                                                                                                                                                 |
| `http.method`, `http.request.method`               | `http.Request.Method`                    | Maps the HTTP method to the ECS field.                                                                                                                                                                                                                 |
| `net.peer.ip`, `net.peer.port`, `net.peer.name`    | `event.Source`                            | Sets the source IP, port, and domain. Uses `net.peer.name` as the domain and `net.peer.ip` as the IP address.                                                                                                   |
| `net.host.name`, `net.host.port`, `server.address`, `server.port` | `event.Destination`                       | Sets the destination IP, port, and domain. Uses `net.host.name` or `server.address` as the domain.                                                                                                             |
| `messaging.system`, `messaging.destination`, `messaging.destination.name` | `event.Transaction.Message.QueueName`    | Populates the message queue name based on these attributes.                                                                                                                                                                                           |
| `db.system`, `db.name`, `db.statement`, `db.user`  | `event.Span.Db`                           | Converts database-related attributes into the ECS database field. For example, `db.statement` is assigned directly to `Db.Statement`.                                                                           |
| `rpc.system`, `rpc.service`, `rpc.method`          | `event.Service.Target`                    | Maps RPC attributes, such as the system and service, to the ECS service target fields.                                                                                                                         |
| `telemetry.sdk.elastic_export_timestamp`           | Adjusts `event.Timestamp`                 | Adjusts the timestamp of spans and transactions based on the provided export timestamp.                                                                                                                         |
| `sampler.type`, `sampler.param`                    | `Transaction.RepresentativeCount` or `Span.RepresentativeCount` | Uses the sampling type and parameter to calculate the representative count. For probabilistic sampling, the count is calculated as `1 / probability`.                                                           |
| `data_stream.dataset`, `data_stream.namespace`     | `event.DataStream.Dataset`, `event.DataStream.Namespace` | Sanitizes the dataset and namespace values by replacing disallowed characters and truncating them to the maximum length.                                                                                         |
| `exception.type`, `exception.message`, `exception.stacktrace`, `exception.escaped` | `Error.Exception`                         | Maps exception attributes to the ECS error exception fields (type, message, and stacktrace).                                                                                                                   |
| `elastic.profiler_stack_trace_ids`                 | `Transaction.ProfilerStackTraceIds`       | Converts the profiler stack trace IDs to a list.                                                                                                                                                                                                      |
| `http.user_agent`, `user_agent.original`           | `UserAgent.Original`                      | Maps the user agent string directly to the ECS field.                                                                                                                                                                                                 |
| `network.connection.type`, `network.connection.subtype`, `network.carrier.*` | `Network.Connection`, `Network.Carrier`   | Maps the network connection type, subtype, and carrier details to the ECS fields.                                                                                                                                                                     |
| `span.kind`                                        | `Transaction.Type` or `Span.Type`         | Determines the transaction or span type based on the span's kind. For example, `SpanKindConsumer` results in a transaction type of `messaging`.                                                                 |
| `peer.service`                                     | `Destination.Service.Name`                | Maps the peer service name to the destination service name.                                                                                                                                                                                            |
| `message_bus.destination`, `messaging.temp_destination` | `Destination.Service.Resource`            | Appends the message bus destination or queue name to the service resource.                                                                                                                                                                             |
| `elastic.is_child`, `is_child`                     | `Span.ChildIds`                           | Determines if a span link is a child span and populates the `ChildIds` field accordingly.                                                                                                                                                              |

Consider the following resource attributes:

```json
{
  "http.status_code": 200,
  "feature.enabled": true,
  "http.request_headers": ["accept:json", "auth:token"]
}
```

The previous resource attributes are stored by Elastic APM as follows:

```json
{
  "http.response.status_code": 200,
  "labels": {
    "feature_enabled": true,
    "http_request_headers.0": "accept:json",
    "http_request_headers.1": "auth:token"
  }
}
```