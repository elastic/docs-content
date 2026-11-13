---
navigation_title: Data routing
description: How the Elastic Cloud Managed OTLP Endpoint routes telemetry to data streams, and how to override the default routing with data stream attributes or the elasticsearch.index attribute.
applies_to:
  serverless:
    observability: ga
    security: ga
  deployment:
    ech: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Data routing with the Managed OTLP Endpoint

By default, the {{motlp}} routes each signal to a data stream based on its type and its `service.name` attribute. If no routing attributes are set, telemetry is routed to the generic data streams: `logs-generic.otel-default`, `metrics-generic.otel-default`, and `traces-generic.otel-default`.

You can override the default routing by setting routing attributes in your OTLP payload, as described in the following sections.

:::{note}
Any client that holds the API key can use these attributes to write to any data stream with a `logs-`, `metrics-`, or `traces-` prefix. For details on the key's write scope, refer to [Authentication](authentication-delivery-and-failure-handling.md#authentication).
:::

## Routing telemetry to dedicated datasets or namespace [routing-telemetry-to-dedicated-datasets-or-namespace]

You can route signals to dedicated datasets by setting the `data_stream.dataset` attribute on the record. This attribute is used to route the signal to the corresponding dataset.

For example, if you want to route the {{edot-cf}} logs to custom datasets, you can add the following attributes to the log records:

```yaml
processors:
  transform:
    log_statements:
      - set(log.attributes["data_stream.dataset"], "aws.cloudtrail") where log.attributes["aws.cloudtrail.event_id"] != nil
```

You can also set the `OTEL_RESOURCE_ATTRIBUTES` environment variable to set the `data_stream.dataset` attribute for all logs. For example:

```bash
export OTEL_RESOURCE_ATTRIBUTES="data_stream.dataset=app.orders"
```

The `data_stream.namespace` attribute is also honored for all signals: logs, metrics, and traces.

## Routing telemetry to a specific index [routing-telemetry-to-a-specific-index]

To route a signal to a specific index instead of using data stream routing, set the `elasticsearch.index` attribute on the record, scope, or resource. When this attribute is present, it takes precedence over the `data_stream.dataset` and `data_stream.namespace` attributes, and it is removed from the final document. For the full routing rules, refer to [Document routing](elastic-agent://reference/edot-collector/components/elasticsearchexporter.md#document-routing) in the {{es}} exporter reference.

For example, to route specific log records to a dedicated index, you can add the attribute in a transform processor:

```yaml
processors:
  transform:
    log_statements:
      - set(log.attributes["elasticsearch.index"], "logs-audit-default") where log.attributes["event.domain"] == "audit"
```

The target index name must start with the `logs-`, `metrics-`, or `traces-` prefix. As with data stream routing, data routed to other prefixes is silently dropped and doesn't appear in {{es}}.

:::{warning}
When you route data with `elasticsearch.index`, the {{motlp}} writes it to a data stream with that name, so the target must match an index template with a data stream definition, and you are responsible for that template and its mappings. The built-in OpenTelemetry index templates that Elastic provides only cover the default data stream naming scheme, such as `logs-*.otel-*`. If another matching template exists, such as the built-in `logs-*-*` template, data is indexed with that template's mappings. If no template matches, documents fail indexing asynchronously and are silently dropped. Refer to [Indexing errors and the failure store](authentication-delivery-and-failure-handling.md#failure-store) for more information.
:::

## Troubleshooting unexpected routing [troubleshooting-unexpected-routing]

Any `data_stream.dataset`, `data_stream.namespace`, or `elasticsearch.index` attribute present in an OTLP payload overrides the default routing for that signal. This applies whether the attribute is set intentionally or by a collector, SDK, or integration.

If data is landing in an unexpected data stream, inspect a sample document from that data stream for the field `resource.attributes.data_stream.dataset`. If the field is present and matches the unexpected data stream name, the attribute was set in the payload, not by the pipeline. The `elasticsearch.index` attribute is removed from the final document, so check your collector and SDK configuration for it instead.

To restore default routing, remove the `data_stream.dataset`, `data_stream.namespace`, and `elasticsearch.index` attributes from your OTLP payload configuration. Once removed, the {{motlp}} falls back to routing based on `service.name`.
