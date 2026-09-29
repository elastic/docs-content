---
navigation_title: Ingest logs
description: Send logs to Elastic with Elastic Agent in OTel mode, Elastic Agent integrations, or another shipper, with the recommended path for each deployment type and log source.
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Ingest logs [logs-ingest]

For a new setup, collect logs with {{agent}} in OTel mode and send them over the OpenTelemetry Protocol (OTLP). Use {{agent}} integrations instead when a prebuilt integration exists for the source and you want its parsing and dashboards, or when you already manage agents with {{fleet}}. Everything else on this page follows from that choice: the endpoint you send to, the schema your logs are stored in, and where parsing happens.

## Choose a collection path [logs-ingest-recommended]

| Your log source | Collect with | Because |
|---|---|---|
| Any log source, when you're setting up new collection | [{{agent}} in OTel mode](#logs-ingest-otel) | One collector for logs, metrics, and traces in OpenTelemetry-native form, and the path Elastic recommends for new deployments. You parse in Streams or in the Collector. |
| A service or platform that has an Elastic integration, when you want its prebuilt content or already run {{fleet}} | {{fleet}}-managed {{agent}} with the [integration](#logs-ingest-integrations) | The integration parses the logs, maps the fields, and installs dashboards. Elastic doesn't ship centrally managed ingest pipelines for OpenTelemetry-native logs, so an integration is the shortest path to structured data for that source. |
| Your own application | Structured logging at the source, then either path above | Logs arrive with fields and trace IDs, so nothing needs parsing. Refer to [Application logs](#logs-ingest-application). |

To check whether a source has an integration, browse the [{{integrations}} catalog](https://www.elastic.co/docs/reference/integrations). Some sources have two tiles, one for {{product.ecs}} (ECS) and one marked **(OpenTelemetry)**. [ECS and OpenTelemetry integration tiles](#logs-ingest-integrations-otel) explains how to pick.

A few cases still work better with classic Elastic components, such as web real user monitoring and centrally managed log processing. Refer to [Know when to keep using classic Elastic components](/solutions/observability/get-started/opentelemetry/start-with-otel.md#start-with-otel-when-classic). {{filebeat}}, {{ls}}, and the REST APIs are covered in [Other ways to collect logs](#logs-ingest-other).

## Ingest with OpenTelemetry (recommended) [logs-ingest-otel]

{{agent}} in OTel mode runs as an OpenTelemetry Collector: it reads log files with the `filelog` receiver, adds host metadata, and exports OpenTelemetry-native logs. It's the distribution Elastic supports, and it's what the quickstarts in [Get started with logs](/solutions/observability/logs/get-started.md) install. You don't need it to send OpenTelemetry logs: any Collector or SDK that speaks OTLP, including the upstream OpenTelemetry Collector, can send to the same endpoints.

- To collect a specific log file rather than the platform defaults, follow [Send any log file using OTel Collector](/solutions/observability/logs/stream-any-log-file-using-edot-collector.md).
- To parse JSON, multiline, or custom formats in the Collector, refer to [Configure logs collection](elastic-agent://reference/edot-collector/config/configure-logs-collection.md).
- To send logs from your application code without a Collector, use an [EDOT SDK](opentelemetry://reference/edot-sdks/index.md).

### Endpoint by deployment type [logs-ingest-endpoints]

Where OpenTelemetry logs go depends on your deployment type. Integrations aren't affected: they use the {{fleet}} output.

:::::{applies-switch}

::::{applies-item} { serverless:, ess: }
Send logs to the {{motlp}}. For application logs, point an EDOT SDK or any OTLP-compatible exporter directly at the endpoint, with no {{agent}} required. For host, container, and {{k8s}} logs, run {{agent}} in OTel mode on the host or cluster and configure its OTLP exporter to send to the endpoint. For the endpoint URL, authentication, and limitations, refer to [{{motlp}}](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md).

The {{ech}} quickstarts currently write to {{es}} directly with the `elasticsearch` exporter. That works, but for a new setup on {{ech}}, send to the {{motlp}} instead. Refer to [Send OTLP data to the {{motlp}}](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md).
::::

::::{applies-item} { self:, ece:, eck: }
The {{motlp}} isn't available. Run {{agent}} in OTel mode as a gateway: it exposes an OTLP endpoint that your edge collectors and EDOT SDKs send to, and it writes to {{es}} with the `elasticsearch` exporter. Use the OTLP exporter at the edge and the `elasticsearch` exporter only on the gateway. Refer to [{{agent}} deployment modes](elastic-agent://reference/edot-collector/modes.md).
::::

:::::

## Ingest with {{agent}} integrations [logs-ingest-integrations]

An integration is a package of inputs, ingest pipelines, field mappings, and dashboards for one source. You add it to an {{agent}} policy in {{fleet}}, the {{kib}} app that manages agents, and every agent on that policy starts collecting. Logs land in a `logs-<dataset>-<namespace>` data stream in ECS and are sent to the output configured in {{fleet}}, which is {{es}} by default. Integrations don't use the OpenTelemetry endpoints described earlier on this page.

If you already collect logs with integrations, keep doing so. Nothing forces you to move them to OpenTelemetry.

To collect host logs this way, follow [Get started with system logs](/solutions/observability/logs/get-started-with-system-logs.md), which scans the host and installs the integrations it finds. To add a specific integration, refer to [Manage {{agent}} integrations](/reference/fleet/manage-integrations.md). To install {{agent}} itself, refer to [Install {{fleet}}-managed {{agent}}](/reference/fleet/install-fleet-managed-elastic-agent.md).

To send a log file that no integration covers with a standalone {{agent}} you configure by hand, follow [Send any log file using {{agent}}](/solutions/observability/logs/stream-any-log-file.md).

### ECS and OpenTelemetry integration tiles [logs-ingest-integrations-otel]
```{applies_to}
stack: preview 9.2+
serverless: preview
```

Some services have two tiles in the {{kib}} {{integrations}} UI, for example **Nginx** and **Nginx (OpenTelemetry)**. The **(OpenTelemetry)** tile is an OpenTelemetry input package: a {{fleet}}-managed {{agent}} runs the matching OTel Collector receiver and stores the data with OpenTelemetry semantic conventions. The other tile is the ECS integration.

Select the OpenTelemetry tile when you standardize on the OpenTelemetry schema and want {{fleet}} to manage the agents. Select the ECS tile when you need the integration's ECS dashboards and alerts. Refer to [Collect OpenTelemetry data with {{agent}} integrations](/reference/fleet/otel-integrations.md).

## How the path decides your log schema [logs-ingest-schema]

Elastic doesn't convert logs between schemas at ingest, so the collection path fixes the field names you query, the dashboards that work, and how you parse:

| Path | Stored as | Data streams |
|---|---|---|
| {{agent}} in OTel mode, EDOT SDKs, any OTLP client | OpenTelemetry-native, with attributes under `attributes.*` and `resource.attributes.*` | `logs-*.otel-*` |
| {{agent}} integrations, {{filebeat}}, ECS loggers | ECS, for example `host.name` and `log.level` | `logs-<dataset>-<namespace>` |

Prefer one schema across your sources. Mixing them works, but every query and dashboard then has two sets of field names. For how the two are stored and which ECS-style queries work on OpenTelemetry data, refer to [OpenTelemetry data streams compared to classic {{product.apm}} and ECS-based integrations](opentelemetry://reference/compatibility/data-streams.md).

{applies_to}`serverless: preview` {applies_to}`stack: preview 9.4+` If you want Streams to partition new logs into child streams with inherited processing and retention, send them to the `logs.otel` or `logs.ecs` wired stream endpoint instead of a regular data stream. Don't reroute data streams that already exist. Refer to [Ingest new data with wired streams](/solutions/observability/streams/get-data-in.md#get-data-in-wired).

{applies_to}`stack: preview 9.2-9.3` In these versions, `logs` is the only wired stream endpoint. Use it in place of `logs.otel` or `logs.ecs`.

## Application logs [logs-ingest-application]

The best application log is one that arrives already structured. In order of preference:

[ECS formatted application logs](/solutions/observability/logs/ecs-formatted-application-logs.md)
:   Instrument with an EDOT SDK, or add an ECS logging library to your logger, so logs arrive as structured JSON with trace IDs. No parsing needed, and the same ingest configuration works for every service.

[Plaintext application logs](/solutions/observability/logs/plaintext-application-logs.md)
:   Collect existing text logs with {{agent}} or {{filebeat}} without changing the application, then parse them. Refer to [Process logs](/solutions/observability/logs/process.md) for where to do that.

[APM agent log sending](/solutions/observability/logs/apm-agent-log-sending.md)
:   The Java APM agent can send logs directly without a separate shipper. It's experimental and not resilient to outages, so use it for evaluation rather than production.

For the full comparison, refer to [Send application log data](/solutions/observability/logs/stream-application-logs.md). If your logs don't carry a service name, add one so they correlate with traces and appear in the Applications UI. Refer to [Add a service name to logs](/solutions/observability/logs/add-service-name-to-logs.md).

## Other ways to collect logs [logs-ingest-other]

These tools remain supported. Use one when its constraint applies:

[{{filebeat}}](beats://reference/filebeat/index.md)
:   A lightweight shipper for log files. Use it when you can't run {{agent}} on the host, or when you already run {{beats}} and don't want to migrate yet. It writes ECS. To move to {{agent}} later, refer to [Migrate from {{beats}} to {{agent}}](/reference/fleet/migrate-from-beats-to-elastic-agent.md).

[{{ls}}](logstash://reference/index.md)
:   A data processing pipeline. Use it when you need to enrich, transform, or fan out logs before they reach {{es}}, or to add processing to data that {{agent}} collects. Refer to [Using {{ls}} with Elastic integrations](logstash://reference/using-logstash-with-elastic-integrations.md).

[{{es}} REST APIs](elasticsearch://reference/elasticsearch/rest-apis/index.md)
:   Send documents straight from your own code or scripts with the bulk API. Use it for custom pipelines where a shipper doesn't fit. You own batching, retries, and backpressure.

## Related pages [logs-ingest-related]

- [Process logs](/solutions/observability/logs/process.md)
- [Manage logs storage](/solutions/observability/logs/manage-storage.md)
- [Migrate logs to Elastic](/solutions/observability/logs/migrate.md)
- [Start using OpenTelemetry with Elastic](/solutions/observability/get-started/opentelemetry/start-with-otel.md)
- [Ingest: Bring your data to Elastic](/manage-data/ingest.md)
