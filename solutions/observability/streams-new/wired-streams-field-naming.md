---
applies_to:
  serverless: preview
  stack: preview 9.2+
description: Learn how wired streams normalize field names across the logs.otel and logs.ecs endpoints.
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Wired streams field naming [streams-field-naming]

When data is ingested into a wired stream, field names are normalized depending on which endpoint you use. Understanding how fields are mapped helps you write accurate queries and processing rules.

## Field naming by endpoint [streams-field-naming-by-endpoint]

::::{applies-switch}

:::{applies-item} { serverless: preview, stack: preview 9.4+ }

Field naming depends on the endpoint you use.

### `logs.ecs` endpoint

Data ingested into the `logs.ecs` endpoint is stored in the original ECS field names without being transformed. The fields remain as shown in the "ECS field" column in the [field naming table](#streams-field-naming-table).

### `logs.otel` endpoint

Data ingested into the `logs.otel` endpoint is stored and processed in a normalized OpenTelemetry (OTel)–compatible format. This format aligns ECS fields with OTel semantic conventions so all data is consistently structured and OTTL-expressible.

When data is ingested into a wired stream, it's automatically translated into this normalized format:

- Standard ECS documents are converted to OTel fields (`message → body.text`, `log.level → severity_text`, `host.name → resource.attributes.host.name`, and so on).
- Custom fields are stored under `attributes.*`.

To preserve backward-compatible querying, Streams creates aliases that mirror existing `logs-*.otel-*` data streams behavior. This allows queries to use either ECS or OTel field names interchangeably.

Refer to the [field naming table](#streams-field-naming-table) for ECS fields and corresponding OTel fields.

:::

:::{applies-item} stack: preview 9.2-9.3

Data ingested into the `/logs` endpoint is stored and processed in a normalized OpenTelemetry (OTel)–compatible format. This format aligns ECS fields with OTel semantic conventions so all data is consistently structured and OTTL-expressible.

Data ingested into a wired stream is automatically translated into this normalized format:

- Streams converts standard ECS documents to OTel fields (`message → body.text`, `log.level → severity_text`, `host.name → resource.attributes.host.name`, and so on).
- Streams stores custom fields under `attributes.*`.

To preserve backward-compatible querying, Streams creates aliases that mirror existing `logs-*.otel-*` data streams behavior. This allows queries to use either ECS or OTel field names interchangeably.

Refer to the [field naming table](#streams-field-naming-table) for ECS fields and corresponding OTel fields.

:::

::::

## Field naming table [streams-field-naming-table]

The following table lists ECS fields and their corresponding OTel fields.

| ECS field | OTel field |
|------------|-------------------------|
| `message` | `body.text` |
| `log.level` | `severity_text` |
| `span.id` | `span_id` |
| `trace.id` | `trace_id` |
| `host.name` | `resource.attributes.host.name` |
| `host.ip` | `resource.attributes.host.ip` |
| `custom_field` | `attributes.custom_field` |
