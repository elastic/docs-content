---
navigation_title: How Streams works
description: Learn how a stream works. Sources receive data, pipelines process it, routers decide where it goes, and destinations store it, before it reaches Elasticsearch.
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

# How Streams works

Data enters Streams at a source and lands in a destination. On the way, a pipeline can shape it and a router can branch it. A stream is any path from a source to a destination. The same model applies to logs, metrics, and traces, and to JSON documents sent with the {{es}} bulk API.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

| Component | What it is | Where it runs |
| --- | --- | --- |
| Source | The endpoint your shippers send to. Accepts OpenTelemetry Protocol (OTLP), Prometheus Remote Write, or {{es}} bulk requests, with its own API keys. | Your project's ingest host, managed by Elastic |
| Pipeline | A sequence of processors that change records or drop them. | Elastic-managed OpenTelemetry Collectors |
| Router | A list of routing rules with conditions that decide which destination a record goes to, and whether it's moved or copied. | Elastic-managed OpenTelemetry Collectors |
| Destination | Where data lands and the credentials used to write it. | {{es}}, in the project you're in or in a remote Elastic Cloud deployment, or an Amazon S3 bucket you own |

Everything between the source and the destination runs before the data reaches {{es}}. That's the point of the model. You can drop, reshape, and route records before they're indexed, and you can send them somewhere other than {{es}}.

## Sources [streams-how-sources]

A source is how data enters Streams. Create a source for each kind of traffic you want to manage separately, choose its type and which signals it accepts, and point your shippers at it. A source is one of three types. An **OTLP endpoint** source accepts logs, metrics, and traces, a **Prometheus Remote Write** source accepts metrics, and a **Managed _bulk** source accepts JSON documents sent with the {{es}} bulk API. OpenTelemetry Collectors, Prometheus, and applications that build bulk requests keep sending in the format they use today. The processing and routing that you'd otherwise configure in each shipper, you configure once in Streams.

Each source has its own API keys, which allow writing to that source and nothing else, and its own endpoint URLs that carry the source ID. Different shippers writing to the same source share everything downstream of it, so use separate sources for data that needs to be kept apart.

## Pipelines and processors [streams-how-pipelines]

A pipeline is an ordered list of processors. Each processor does one thing to every record that passes through it, such as adding or renaming fields, setting a field's value, dropping records that match a condition, or running statements in the OpenTelemetry Transformation Language (OTTL). Conditions are OTTL expressions over the record and its resource and scope attributes.

A Streams pipeline isn't an {{es}} ingest pipeline. It runs outside the cluster, before data reaches any destination, and applies to every destination downstream of it. An ingest pipeline runs in {{es}} at index time. The two can be used together. Refer to [How a Streams pipeline differs from an ingest pipeline](../process-data.md#streams-process-vs-ingest).

## Routers and routing rules [streams-how-routers]

A router holds an ordered list of rules. Each rule has an optional condition and a target, which is the destination or pipeline it's connected to on the Streams Map. Records are checked against the rules from top to bottom, and the first match decides where a record goes. A rule either moves matching records to its target, taking them off the main path, or copies them, so the same record continues to the next rule as well. A rule without a condition catches everything that hasn't matched yet. Records that match nothing are dropped, and the routing panel warns you when that can happen.

Copy rules are how you store the same data in two places, for example the complete record in S3 and a filtered subset in {{es}}.

## Destinations [streams-how-destinations]

A destination is where data lands and the credentials used to write it.

* A **Local Elasticsearch** destination writes to the project you're working in, with an API key that Streams creates and scopes to the destination's write patterns. Its index mode decides which data stream each record is written to, so one destination node on the Streams Map can stand for many data streams.
* A **Remote Elasticsearch** destination writes to another Elastic Cloud deployment, with an endpoint and API key that you provide.
* An **Amazon S3** destination writes newline-delimited JSON objects to a bucket you own, with an access key pair that you provide.

Whatever a destination can't store is dropped, and a failing destination doesn't stop the rest of the stream. Refer to [Destinations](../destinations.md).

## The Streams Map [streams-how-map]

The Streams Map is where you build streams. Every source, pipeline, router, and destination is a node, and the connections between them show where data goes. You add a pipeline or a router on a connection, on the path the data takes. Changes to connections and routers run only after you select **Save changes**, and changes to processors only after you select **Save and apply** in the **Processing** panel. The **Sources** and **Destinations** tabs next to the Map list the same sources and destinations as tables. Refer to [Work with the Streams Map](../streams-map.md).

## What Elastic runs for you [streams-how-elastic-runs]

Streams is a managed Elastic Cloud service. The buffer that absorbs bursts and the OpenTelemetry Collectors that run your pipelines and routers are deployed, patched, and scaled by Elastic as part of {{serverless-full}}. They sit outside {{es}}, so processing and routing finish before data reaches your project, and none of that work uses the compute that indexes and serves your searches.

When you change a pipeline or a router on the Streams Map and save, the collectors pick up the change. There's nothing to restart or redeploy, and your shippers keep pointing at the same source throughout.

## Where your existing data streams fit [streams-how-existing-data-streams]

An {{es}} destination writes to data streams, and those data streams are what you manage as classic streams after the data arrives. Nothing is migrated between the two. Refer to [Streams Map and classic streams compared](../index.md#streams-map-and-classic).

Integrations, {{agent}} policies, and your project's existing managed OTLP and bulk endpoints don't appear on the Map. Refer to [Streams limitations](../limitations.md#streams-limitations-sources).

## Next steps [streams-how-next]

* [Build your first stream](build-your-first-stream.md): Create a source, connect it to an {{es}} destination, send data, and add a processor.
* [Streams limitations](../limitations.md): Check what Streams doesn't support before you send production data.
* [Streams glossary](../glossary.md): Look up source, pipeline, router, destination, and the other terms used on this page.
