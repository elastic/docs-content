---
navigation_title: Limitations
description: What Streams can't do yet when it ingests, processes, and routes data before Elasticsearch, from delivery and monitoring to sources and destinations.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
  stack: unavailable
products:
  - id: kibana
  - id: cloud-serverless
---

# Streams limitations

Ingesting, processing, and routing data before it reaches {{es}}, with sources, pipelines, routers, and destinations on the Streams Map, is new, and some capabilities are incomplete. This page lists what to expect, so you can decide what to send through a stream and what to keep on your existing path. The limitations are grouped into [availability](#streams-limitations-availability), [data handling](#streams-limitations-data), [monitoring](#streams-limitations-monitoring), [sources](#streams-limitations-sources), [processing](#streams-limitations-processing), [routing](#streams-limitations-routing), [destinations](#streams-limitations-destinations), and [operations and access control](#streams-limitations-operations).

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

For how the building blocks fit together, refer to [How Streams works](get-started/how-streams-work.md). For problems with a stream you've already built, refer to [Troubleshoot Streams](troubleshooting.md).

## Availability [streams-limitations-availability]

The preview is limited in where it runs and in what you can rely on:

* Ingesting, processing, and routing data before it reaches {{es}} is available only on {{serverless-full}} {{es}}, Observability, and Security projects, and Elastic enables it per project. It isn't available on {{es}} Vector DB projects. On {{ech}}, self-managed deployments, {{ece}}, and {{eck}}, Streams works only on data after it reaches {{es}}, as classic streams. Refer to [Availability](index.md#streams-availability).
* Features and the API can change without notice, including in ways that aren't backward compatible.
* Classic streams aren't migrated into the new model. They keep working as before, continue to process data inside {{es}}, and don't appear on the Streams Map.

## Data handling [streams-limitations-data]

These limitations affect whether, and how many times, a record reaches its destination:

* Delivery is best effort. If an Elastic-managed collector restarts while data is buffered, that data is lost. If a destination rejects data, for example because of a wrong index name or an invalid credential, those records are dropped after the retry window, and the drop isn't reported in the UI. For data you rely on, consider keeping your current ingest path in place and sending a copy to a source.
* Duplicates are possible. When Streams retries a failed write, records that were already stored can be stored again. Metrics written to time series data streams are deduplicated by {{es}}. Logs and traces aren't, unless the documents carry their own `_id`.
* A source acknowledges data as soon as it's accepted, before processing and delivery finish. A shipper isn't told when its data is dropped later.
* Changes you save apply to live data immediately. There's no way to test a processor or a routing rule against sample data, no draft mode, and no version history.
* Processing is stateless and per record. Multi-line assembly, for example of stack traces, has to happen in the shipper.

## Monitoring [streams-limitations-monitoring]

The Streams Map tells you whether data flows, but not much more:

* Statistics are limited to throughput in records per second and, on pipeline and destination nodes, an average duration. Error rates, the number of dropped records, and the reasons records were dropped aren't shown.
* There's no end-to-end latency figure for a stream.
* Among destinations, only Local Elasticsearch nodes show statistics. Router nodes, Remote Elasticsearch destinations, and Amazon S3 destinations show no state and no statistics. A source that isn't connected to any destination accepts records and drops them; its node shows **Live**, and nothing on the Map tells you the records went nowhere.
* The indices listed for a Local Elasticsearch destination are the ones that match its write patterns, not the ones the stream has written to.
* There's no alerting on stream health.

For what the Map does show and how to read it, refer to [Monitor streams](monitor-streams.md).

## Sources [streams-limitations-sources]

These limitations affect what a source can receive, and from which shippers:

* Source types are **OTLP endpoint**, **Prometheus Remote Write**, and **Managed _bulk**. There's no syslog, TCP, Fluent Forward, generic HTTP, Kinesis Firehose, or Kafka source.
* Sources don't pull data. Sources that poll S3 buckets, HTTP APIs, or other systems aren't available.
* A source accepts only the signals selected when it's created, and its type and name can't be changed afterwards.
* OTLP is accepted over HTTP only. OTLP over gRPC isn't supported.
* A Prometheus Remote Write source accepts Remote Write 1.0 only. Remote Write 2.0 isn't supported.
* A Managed _bulk source carries documents only and accepts only `create` actions, and only for index names that start with `logs-`, `metrics-`, or `traces-`. Other actions and index names are rejected.
* A Managed _bulk source answers bulk requests only. Logstash, Beats, and standalone {{agent}} check the server with a `GET` request before sending, so they can't connect to it. Fleet-managed {{agent}} can't send to any source. OpenTelemetry Collectors, including {{agent}} in OpenTelemetry mode, and Prometheus can.
* Your project's existing managed OTLP and bulk endpoints, the ones that integrations and {{agent}} policies use, don't appear on the Streams Map, and the data they receive can't be processed or routed with Streams.

For what each source type accepts, refer to [Sources](sources.md).

## Processing [streams-limitations-processing]

These limitations affect what a pipeline can do to a record:

* The processors are **Add fields**, **Filter**, **Rename fields**, **Set**, and **Transform**. The list in the **Processing** panel comes from the Streams backend, so it can change without a {{kib}} release.
* There are no dedicated parsing processors, such as Grok, Dissect, JSON, key-value, CSV, or date parsing, and no enrichment processors, such as GeoIP or lookups. For parsing, write OTTL statements in a [Transform](processors/transform.md) processor, for example with `ParseJSON` or `ExtractPatterns`.
* Processor conditions and Transform statements are written in OpenTelemetry Transformation Language (OTTL) in a free-text field, with no autocompletion. You need to know OTTL syntax and the OTLP data model to write them.
* {{es}} ingest pipelines and integration pipelines can't run inside a Streams pipeline. They still run in {{es}} when the data is indexed, after Streams.

For what the processors do, refer to [Process data](process-data.md).

## Routing [streams-limitations-routing]

These limitations affect what a router can do with a record:

* Each routing rule sends to one target.
* Rules can't be named. On the Streams Map, each rule is labeled by its position, `rule-0`, `rule-1`, and so on, and the label changes when you reorder the rules.
* Records that match no rule are dropped. The number of unmatched records isn't shown.
* There's no discard destination. To drop data on purpose, filter it out with a [Filter](processors/filter.md) processor or leave it unmatched.
* Routing rules can be viewed only on the Map, router by router. There's no list of all routing rules in the project.

For how routing works, refer to [Route data](route-data.md).

## Destinations [streams-limitations-destinations]

These limitations affect where data can go and what you can change after creating a destination:

* Destination types are **Local Elasticsearch**, **Remote Elasticsearch**, and **External storage**, which writes to Amazon S3. Other object stores, such as Azure Blob Storage and Google Cloud Storage, aren't available.
* Destinations can't be edited after you create them. To change anything about a destination, create a new one, reconnect the routing rules, and delete the old one.
* In **Auto** index mode, a destination writes only to data streams matching `logs-*-*`, `metrics-*-*`, and `traces-*-*`. Custom write patterns can narrow this, but the signal prefix is fixed. Index names can't be built from field values.
* In **Fixed index per signal** mode, a signal you leave blank, and data of a signal the destination doesn't accept, is dropped.
* A **Remote Elasticsearch** destination doesn't accept documents from a Managed _bulk source. Documents routed to one are dropped.
* Remote Elasticsearch destinations must be Elastic Cloud deployments, {{ech}} or {{serverless-short}}, on 9.5 or later, reachable at their public `https://` endpoint. Self-managed clusters, deployments behind traffic filters or private link, and versions before 9.5 aren't supported, and sending to them fails or drops data.
* Amazon S3 destinations write newline-delimited JSON only. Parquet isn't available.
* Remote Elasticsearch and Amazon S3 destinations don't list what they've written, and Streams doesn't report a rejected credential. Check for the data on the remote side.
* A failing destination doesn't block the stream and doesn't retry indefinitely. Its records are dropped after the retry window and aren't recovered when the destination comes back.
* The index details that a Local Elasticsearch destination opens are read-only. To change retention, mappings, or ingest pipelines, select **Manage in Stack Management** or use classic streams.

For what each destination type accepts and how it's set up, refer to [Destinations](destinations.md), [Remote Elasticsearch destination](destinations/remote-elasticsearch.md), and [Amazon S3 destination](destinations/s3.md).

## Operations and access control [streams-limitations-operations]

These limitations affect how you operate Streams and who can change it:

* A project has one Streams configuration, shared by all {{kib}} spaces. Separate configurations per space or team aren't available.
* Creating sources and Local Elasticsearch destinations requires the **Admin** role, because Streams creates their API keys as you. The **Streams V2** feature privilege on its own isn't enough. Refer to [Privileges and API keys](security.md#streams-security-view-edit).
* There's no public API for sources, pipelines, routers, and destinations, and no export or import of the configuration. The Streams APIs that exist manage classic streams.
* There's no published guidance on throughput per source or on the cost of processors.
