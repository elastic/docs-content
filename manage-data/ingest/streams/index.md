---
navigation_title: Streams
description: Manage how data gets into Elastic. Ingest, process, and route data before it reaches Elasticsearch, or manage existing data streams as classic streams.
applies_to:
  serverless:
    elasticsearch: preview
    observability: ga
    security: ga
  stack: preview =9.1, ga 9.2+
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: elastic-stack
---

# Streams

Streams is the part of {{kib}} where you manage how data gets into Elastic and what happens to it on the way. To open it, find **Streams** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

Streams has two sets of capabilities. They differ in when they act on your data:

* {applies_to}`serverless: preview` **Before data reaches {{es}}.** Keep your shippers as they are and point them at a source. Streams processes and routes the data on infrastructure that Elastic manages, then delivers it to {{es}}, to an Amazon S3 bucket you own, or to both. You build the whole path on the Streams Map.
* **After data reaches {{es}}.** You manage existing data streams in {{es}}. You parse and process their data with ingest pipelines, set retention, and check data quality. These are classic streams.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

## Streams Map: Ingest, process, and route data before it reaches {{es}} [streams-map-before-elasticsearch]

```{applies_to}
serverless:
  elasticsearch: preview
  observability: preview
  security: preview
```

A stream is the path that data follows into Elastic, from a source to a destination. It's made of four kinds of building blocks:

* A **source** is the endpoint your shippers send to. It accepts OpenTelemetry Protocol (OTLP), Prometheus Remote Write, or {{es}} bulk requests, so OpenTelemetry Collectors, Prometheus, and applications that send bulk requests keep sending in the format they use today.
* A **pipeline** is a list of processors that change each record or drop it.
* A **router** decides which destination a record goes to, and whether it's moved there or copied.
* A **destination** is where the data is stored. It can be {{es}}, in this project or in another Elastic Cloud deployment, or an Amazon S3 bucket you own.

You build and edit streams on the **Streams Map**, where each building block is a node and the connections between them show where data goes. Pipelines and routers run in OpenTelemetry Collectors that Elastic operates, so there's nothing for you to install or scale, and the data is already processed by the time it reaches a destination.

Processing and routing data before it reaches {{es}} lets you:

* Drop or reshape data before it's indexed, so you store only what you need.
* Keep the complete record in storage you control, such as Amazon S3, and index only a subset in {{es}}.
* Configure processing and routing once, in Streams, instead of in each shipper.
* See every source, pipeline, router, and destination in one place, and change them there.

To begin, go to [Get started](get-started/index.md). Read [How Streams works](get-started/how-streams-work.md) to learn the model, then follow [Build your first stream](get-started/build-your-first-stream.md) to try it. Before you send production data, read the [limitations](limitations.md).

## Classic streams: Manage data streams in {{es}} [streams-classic]

```{applies_to}
serverless:
  observability: ga
  security: ga
stack: preview =9.1, ga 9.2+
```

Classic streams work on data after it reaches {{es}}. A classic stream is an existing data stream that you manage from Streams. You add processing that runs as an {{es}} ingest pipeline, set retention, and check data quality.

For the full documentation, refer to [Streams](/solutions/observability/streams/streams.md).

## Streams Map and classic streams compared [streams-map-and-classic]

Use this table to decide which side of Streams a task belongs to:

:::{table}
:widths: 3-5-4

| Aspect | Before data reaches {{es}} (Streams Map) {applies_to}`serverless: { elasticsearch: preview, observability: preview, security: preview }` | After data reaches {{es}} (classic streams) |
| --- | --- | --- |
| What you work with | Sources, pipelines (lists of processors), routers, and destinations | Classic streams |
| Processing runs in | OpenTelemetry Collectors that Elastic manages | {{es}} ingest pipelines, as data is indexed |
| Can send data to | {{es}}, another Elastic Cloud deployment, or Amazon S3 | The data stream it's attached to |
| Where you work in Streams | The **Map**, **Sources**, and **Destinations** tabs | The **Classic Streams** tab, and each stream's own page with its **Processing**, **Data lifecycle**, **Schema**, and **Data quality** tabs |
:::

You can use both. An {{es}} destination writes to ordinary data streams, and an ingest pipeline attached to a data stream still runs when the data arrives. From a destination, you can open each data stream it can write to and view its overview and retention.

Nothing is migrated between the two. Classic streams keep working as before and don't appear on the Map. To open a classic stream, select the **Classic Streams** tab, which lists everything the Streams list showed before. The tab appears only when the project has at least one classic stream or [wired stream](/solutions/observability/streams/get-data-in.md#get-data-in-wired).

## Availability [streams-availability]

Where each side of Streams is available depends on your deployment type:

| Deployment | Before data reaches {{es}} (Streams Map) | After data reaches {{es}} (classic streams) |
| --- | --- | --- |
| {{serverless-full}}, Observability and Security projects | Private technical preview | Available |
| {{serverless-full}}, {{es}} projects | Private technical preview | Not available |
| {{serverless-full}}, {{es}} Vector DB projects | Not available | Not available |
| {{ech}} | Not available | Available |
| Self-managed, {{ece}}, {{eck}} | Not available | Available |

## Learn more [streams-learn-more]

These pages cover ingesting, processing, and routing data before it reaches {{es}}, with sources, pipelines, routers, and destinations on the Streams Map:

* [Get started](get-started/index.md): Learn the model with [How Streams works](get-started/how-streams-work.md), then [build your first stream](get-started/build-your-first-stream.md).
* [Streams Map](streams-map.md): Read and edit the Map, and move around it.
* [Sources](sources.md): Create [OTLP](sources/otlp.md), [Prometheus Remote Write](sources/prometheus-remote-write.md), and [{{es}} bulk](sources/elasticsearch-bulk.md) sources, point your shippers at them, and manage them on the **Sources** tab.
* [Destinations](destinations.md): Write to [{{es}} in this project](destinations/elasticsearch.md), a [remote {{ech}} deployment or {{serverless-short}} project](destinations/remote-elasticsearch.md), or [Amazon S3](destinations/s3.md), and manage destinations on the **Destinations** tab.
* [Process data](process-data.md): Add a pipeline and configure its processors.
* [Route data](route-data.md): Send records to different destinations by condition, or copy them.
* [Monitor streams](monitor-streams.md): Read the states and statistics on the Map.
* [Privileges and API keys](security.md): Learn who can edit streams, and how sources and destinations authenticate.
* [Troubleshooting](troubleshooting.md): Resolve the most common errors.
* [Limitations](limitations.md): Check what Streams doesn't support before you send production data.
* [Glossary](glossary.md): Look up the terms used in these pages.

For managing data streams after data reaches {{es}}, refer to [Classic streams](/solutions/observability/streams/streams.md).
