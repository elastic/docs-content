---
navigation_title: Get started
description: Get started with Streams on Elastic Cloud Serverless. Learn how sources, pipelines, routers, and destinations fit together, then build your first stream.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Get started with Streams

Use Streams to create managed data pipelines that process and route your data before it reaches {{es}}. Your shippers send data to a source, pipelines and routers process and route it in OpenTelemetry Collectors that Elastic operates, and destinations store it in {{es}}, in another Elastic Cloud deployment, or in an Amazon S3 bucket you own. You build and manage the whole path on the Streams Map.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

Choose where to start:

* [How Streams works](how-streams-work.md): Learn the four building blocks of a stream, where each one runs, and how they appear on the Streams Map. Start here if you want to understand the model before you use the UI.
* [Build your first stream](build-your-first-stream.md): Create a source, connect it to an {{es}} destination, send test records with `curl`, and add a processor. Start here if you'd rather learn by doing.

Before you send data you rely on, read [Streams limitations](../limitations.md).

After you build your first stream, continue with [Sources](../sources.md), [Destinations](../destinations.md), [Process data](../process-data.md), and [Route data](../route-data.md) for the details of each building block.
