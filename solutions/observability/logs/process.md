---
navigation_title: Process logs
description: Choose where to parse logs, at the source, in Streams, in an ingest pipeline, in Logstash, or in the OpenTelemetry Collector, test the result, and route logs into the right data streams.
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Process logs [logs-process]

A log line you can only full-text search is a log line you can't aggregate, chart, or alert on by field. Processing extracts fields such as `log.level`, `host.ip`, and `@timestamp` from the message, tests the result against representative events, and routes logs into the data streams whose retention and processing match them.

The question isn't whether to process. It's where. This page takes a position for each situation and links to the page that shows you how.

## Where to parse [logs-parse-where]

Work down this table and stop at the first row that matches:

| Situation | Parse | Why |
|---|---|---|
| You own the application that writes the logs | At the source, with an {{edot}} (EDOT) SDK or an {{product.ecs}} (ECS) logging library | Logs arrive structured, with trace IDs for correlation, and nothing downstream needs to know the format. Refer to [ECS formatted application logs](/solutions/observability/logs/ecs-formatted-application-logs.md). |
| The logs come from an Elastic integration | Nowhere. The integration already does it | Integrations ship the ingest pipeline and mappings for their source. Refer to [Ingest with {{agent}} integrations](/solutions/observability/logs/ingest.md#logs-ingest-integrations). |
| A new setup, or custom or third-party logs that are already flowing into Elastic | In [Streams](#logs-parse-streams) | A {{kib}} UI that previews the result on real data before you save and keeps failed documents so you can fix the rule. Its processing rules are stored as Streamlang, so you can version them. |
| An existing setup with ingest pipelines that work | Keep the [ingest pipelines](#logs-parse-pipelines) | Nothing forces you to migrate. Ingest pipelines expose every processor and run in {{es}}, so they work for any shipper. Streams builds on them. |
| Streams lacks the processor you need, or you need {{product.painless}} scripting | In an [ingest pipeline](#logs-parse-pipelines) | Same reason: the full processor set. |
| Complex normalization across many sources, or enrichment from external systems before indexing | In {{ls}} filters | {{ls}} runs before {{es}} and can join, enrich, and fan out. OpenTelemetry and {{agent}} don't replace it for this. Refer to [{{ls}}](logstash://reference/index.md). |
| OpenTelemetry-native logs where you want structure before they leave the host | In {{agent}} in OTel mode, the OTel Collector | The `filelog` receiver operators and the transform processor parse JSON, multiline, and custom formats at the edge. Refer to [Configure logs collection](elastic-agent://reference/edot-collector/config/configure-logs-collection.md). |

Whatever you choose, keep the original message. Every option here leaves the raw line in place by default, and you'll want it when a parsing rule is wrong.

## Parse in Streams [logs-parse-streams]
```{applies_to}
serverless: ga
stack: preview =9.1, ga 9.2+
```

Streams is the recommended place to parse logs that aren't already structured. Open **Streams** from the navigation menu, or select **Parse content in Streams** from a log's details in **Discover** to open the right stream directly. On the **Processing** tab, add processors, add conditions so a processor runs only on matching documents, and check the data preview before you save. Documents that fail after you save go to the failure store rather than being dropped.

{applies_to}`stack: preview 9.3+` {applies_to}`serverless: preview` Streams can also suggest a complete pipeline from sample documents for you to refine.

Streams doesn't support every ingest processor, and it can't process array fields. When you reach one of those limits, use an ingest pipeline for that step instead. Refer to [Known limitations](/solutions/observability/streams/parse-and-process.md#streams-known-limitations).

For the walkthrough, refer to [Process your documents with Streams](/solutions/observability/streams/parse-and-process.md).

{applies_to}`stack: ga 9.2+` For the YAML format behind the UI, refer to [Streamlang](/solutions/observability/streams/streamlang.md).

## Parse with an ingest pipeline [logs-parse-pipelines]

An ingest pipeline is a list of processors that {{es}} runs on each document before indexing it. Use dissect for fixed-layout messages and grok when the layout varies. Test it with the simulate API before you attach it to a data stream through the index template.

For an end-to-end example that extracts `@timestamp`, `log.level`, and `host.ip`, then routes by severity, follow [Parse and route logs using ingest pipelines](/solutions/observability/logs/parse-route-logs.md). For the full processor set, refer to [Ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md).

## Route logs to data streams [logs-parse-route]

Routing splits one incoming stream of logs into several data streams so each can have its own retention, processing, and mappings. Split by structure and lifecycle, not by every distinct value: firewall logs and application logs deserve separate streams because they look different and are kept for different lengths of time. Two web servers with identical logs don't.

Two mechanisms, chosen by how the logs arrive:

[Partition a wired stream](/solutions/observability/streams/organize-your-data.md) {applies_to}`serverless: preview` {applies_to}`stack: preview 9.2+`
:   For logs sent to a wired stream endpoint such as `logs.otel` or `logs.ecs`. Define conditions on the **Partitioning** tab and Streams creates child streams that inherit the parent's processing and lifecycle. Aim for tens of partitions, not hundreds. Each one is a data stream with its own cost.

[Add a reroute processor](/solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-reroute-log-data-to-specific-data-streams)
:   For existing data streams. The processor changes the target dataset or namespace based on a field. Pick a field with a small, fixed set of values, such as severity, so you don't create a data stream per unique value.

## Related pages [logs-process-related]

- [Ingest logs](/solutions/observability/logs/ingest.md)
- [Manage logs storage](/solutions/observability/logs/manage-storage.md)
- [Filter and aggregate logs](/solutions/observability/logs/filter-aggregate-logs.md): what parsed fields let you do next.
