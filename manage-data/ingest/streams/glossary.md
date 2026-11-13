---
navigation_title: Glossary
description: Definitions of the terms used in Streams, including source, pipeline, processor, router, routing rule, destination, record, location, write pattern, and stream.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Streams glossary

These terms appear throughout the Streams documentation. For how they fit together, refer to [How Streams works](get-started/how-streams-work.md).

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

**Auto index mode**
:   The default index mode of a Local or Remote {{es}} destination. The data stream that each record is written to is derived from the record's own metadata, within the destination's write patterns. To learn more, refer to [Local Elasticsearch destination](destinations/elasticsearch.md).

**Catch-all rule**
:   A routing rule without a condition. It receives every record that no rule above it matched. In the routing panel, the rule a new router starts with is labeled **Default**; on the Streams Map, a rule with no condition is labeled **Otherwise**, or **All data** when it's the only rule in the router. To learn more, refer to [Route data](route-data.md).

**Classic stream**
:   An existing {{es}} data stream that you manage in Streams: processing that runs as an {{es}} ingest pipeline, retention, schema, and data quality. Classic streams work on data after it reaches {{es}}. To learn more, refer to [Streams](/solutions/observability/streams/streams.md).

**Condition**
:   A boolean expression in the OpenTelemetry Transformation Language (OTTL) that a routing rule or a processor evaluates against each record. To learn more, refer to [Fields and conditions](fields-and-conditions.md#streams-fields-conditions).

**Connection**
:   A line between two nodes on the Streams Map, along which data flows. Hover over a connection to add processing or routing on it. To learn more, refer to [Work with the Streams Map](streams-map.md).

**Context**
:   In OTTL, the part of the data model that a condition or statement is written against, such as **Resource**, **Scope**, **Log**, or **Span**. The Filter and Transform processors ask for it per block. Other processors use locations instead, so you don't have to choose one. To learn more, refer to [Fields and conditions](fields-and-conditions.md#streams-fields-locations).

**Copy rule**
:   A routing rule that sends matching records to its destination and also lets them continue to the rules below it, so the same record can reach more than one destination. Selected with **Create a copy of the data** in the routing panel. To learn more, refer to [Route data](route-data.md).

**Destination**
:   Where data lands at the end of a stream, together with the credentials used to write it. A destination is one connection, and an {{es}} destination can write to many data streams and indices. Destination types are Local Elasticsearch, Remote Elasticsearch, and External storage (Amazon S3). To learn more, refer to [Destinations](destinations.md).

**Fixed index mode**
:   An index mode of an {{es}} destination in which every record of a signal is written to one index that you name. The UI calls it **Fixed index per signal**. To learn more, refer to [Local Elasticsearch destination](destinations/elasticsearch.md).

**Location**
:   The part of a record that a processor reads or writes: **Body**, **Resource**, **Scope**, **Attributes**, **Metadata**, **Record**, or, for documents from a Managed _bulk source, **Document**. Locations mean the same thing for logs, metrics, and traces, so you don't have to pick an OTTL context. To learn more, refer to [Fields and conditions](fields-and-conditions.md#streams-fields-locations).

**Move rule**
:   The default kind of routing rule. It sends matching records to its destination and takes them off the path, so no rule below it sees them. The first matching move rule wins. Selected with **Route data exclusively** in the routing panel. To learn more, refer to [Route data](route-data.md).

**Node**
:   A source, pipeline, router, or destination on the Streams Map. Select a node to open its panel. To learn more, refer to [Work with the Streams Map](streams-map.md).

**OTLP**
:   The OpenTelemetry Protocol, the format that OpenTelemetry SDKs, collectors, and agents use to send logs, metrics, and traces. An OTLP endpoint source accepts it over HTTP. To learn more, refer to [OTLP source](sources/otlp.md).

**OTTL**
:   The OpenTelemetry Transformation Language, the language of processor statements and routing rule conditions in Streams. It runs in the OpenTelemetry Collector's `transform` and `filter` processors. To learn more, refer to the [OTTL documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/pkg/ottl).

**Pipeline**
:   An ordered list of processors that run on every record passing through it. A pipeline decides how data changes, never where it goes. A Streams pipeline runs in Elastic-managed OpenTelemetry Collectors and is not an {{es}} ingest pipeline. To learn more, refer to [Process data](process-data.md).

**Processor**
:   One step inside a pipeline, such as **Add fields**, **Filter**, or **Transform**. The meaning matches the OpenTelemetry Collector's use of the word. To learn more, refer to [Process data](process-data.md).

**Record**
:   A single unit of data as it moves through a stream: a log record, a span, a metric data point, or a document sent to a Managed _bulk source. Processors and routing rules act on one record at a time.

**Router**
:   An ordered list of routing rules, checked from top to bottom for each record. A router decides where data goes, never how it changes. To learn more, refer to [Route data](route-data.md).

**Routing rule**
:   One entry in a router: an optional condition plus the destination or pipeline that matching records go to, and whether they're moved or copied. Shown as **Rule 1**, **Rule 2**, and so on in the routing panel, and as `rule-0`, `rule-1`, and so on on the Map. To learn more, refer to [Route data](route-data.md).

**Shipper**
:   Software that collects data and sends it to a source, such as an OpenTelemetry Collector, {{agent}} in OpenTelemetry mode, or Prometheus. Where a page says *sender* instead, it means anything that makes the request, which also covers an OpenTelemetry SDK inside your application or a test tool. To learn more, refer to [Sources](sources.md).

**Signal**
:   The kind of data a record is: logs, metrics, traces, or documents. Documents are the JSON documents sent to a Managed _bulk source, and that source type carries nothing else. Sources accept only the signals you select for them, and destinations can treat each signal differently.

**Source**
:   The entry point for data into Streams: an endpoint of a given type, with its own API key, that your shippers send to. Source types are OTLP endpoint, Prometheus Remote Write, and Managed _bulk. To learn more, refer to [Sources](sources.md).

**Stream**
:   Any path from a source to a destination on the Streams Map. A stream isn't something you create or name directly. You build one by connecting a source to a destination, directly or through pipelines and routers. To learn more, refer to [Build your first stream](get-started/build-your-first-stream.md).

**Streams Map**
:   The graph in Streams where every source, pipeline, router, and destination is a node and you build streams by connecting them. The **Sources** and **Destinations** tabs show the same objects as tables. To learn more, refer to [Work with the Streams Map](streams-map.md).

**Write pattern**
:   An index pattern, such as `logs-*-*`, that limits what a Local Elasticsearch destination's API key is allowed to write to. Write patterns constrain permissions, not routing. To learn more, refer to [Local Elasticsearch destination](destinations/elasticsearch.md).
