---
navigation_title: Remote Elasticsearch
description: Write data from a stream to another Elastic Cloud deployment or Serverless project on 9.5 or later, using an endpoint and API key that you supply.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Remote Elasticsearch destination

A **Remote Elasticsearch** destination writes data from a stream to an {{ech}} deployment or {{serverless-short}} project other than the one you're working in. Use it to keep a copy of data in another region or another team's deployment, to send data from a {{serverless-short}} project to an {{ech}} deployment, or to move a stream between projects without touching the shippers. Unlike a [Local Elasticsearch destination](elasticsearch.md), you supply the credentials, and Streams uses them as they are.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

## Before you begin [streams-remote-es-prereqs]

To create a Remote Elasticsearch destination, you need:

* The **Admin** role. Refer to [Privileges and API keys](../security.md#streams-security-view-edit).
* A remote deployment that Streams can write to:
  * An Elastic Cloud deployment, either {{ech}} or a {{serverless-short}} project, running 9.5 or later. Self-managed clusters aren't supported, and sending to a version before 9.5 fails or drops data.
  * Reachable at its public `https://` endpoint. Deployments behind traffic filters or private link aren't reachable from Streams.
* An API key created on the remote deployment, in its encoded form, with write access to the target data streams. Give it the least privilege the destination needs, which is the `write` and `auto_configure` index privileges on the data streams you intend to write to.

## Create the destination [streams-remote-es-create]

You create the destination on the Streams Map, and it exists as soon as you save the dialog:

1. Find **Streams** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Map** tab.
1. Select **Destination** in the toolbar at the bottom of the Map.
1. Under **Where will this destination's data live?**, select **Remote Elasticsearch**.
1. Under **Connection**, enter the remote deployment's **Endpoint** as an `https://` URL without credentials, a query, or a fragment, for example `https://my-cluster.es.us-central1.gcp.elastic.cloud:443`, and paste the encoded **API key**.
1. Under **Index mode**, choose how records are placed on the remote deployment:
   * **Auto (default)**: each record is written to the data stream its `data_stream.*` fields name, or to the default data stream for its signal.
   * **Fixed index per signal**: under **Fixed index naming**, choose **One index for all signals** and enter one index name, or choose **Name signals individually** and enter a name for each of **Logs**, **Metrics**, and **Traces**. Leave a signal blank to not send it to this destination. Names are used as you type them, with no signal prefix added. They must be lowercase, can't start with a `.`, and can't be built from field values.
1. Enter a **Destination name** and, optionally, a **Description**. The name must be unique among your destinations and can't be changed later.
1. Select **Create destination**.

The destination appears on the Map with the host of its endpoint under its name. Connect a source, pipeline, or router to it and select **Save changes**. The node shows no state or statistics, so check that data arrives by querying the remote deployment.

Streams encrypts the API key when you save it, and never shows it again. The destination's details show the **Endpoint**, the index mode under **Routing**, and the **API key** as **Configured**. Destinations can't be edited, so to rotate the key, create a new destination with the new key, reconnect the routing rules to it, and delete the old one.

## What the destination accepts [streams-remote-es-accepts]

The destination accepts logs, metrics, and traces. It doesn't accept documents from a Managed _bulk source, so documents routed to it are dropped. In Fixed mode, a signal you left blank is dropped too.

## How it differs from a Local Elasticsearch destination [streams-remote-es-differences]

Because the credentials and the cluster are yours rather than the project's, a few things work differently:

* **No write patterns.** Streams can't narrow a key you supply, so what the destination may write to is whatever the remote key allows. Scope the key on the remote deployment instead.
* **No statistics and no index list.** The destination node shows the endpoint host, not a rate or a state, and the **Destinations** tab doesn't list the remote data streams or open their details. Manage and inspect them on the remote deployment.
* **No `.otel` suffix in Fixed mode.** As with a Local Elasticsearch destination, a fixed name is used as entered. For OpenTelemetry data, name the data stream `<signal>-<dataset>.otel-<namespace>` so it matches the OpenTelemetry index templates on the remote deployment. Refer to [Fixed index mode](elasticsearch.md#streams-es-destination-fixed).
* **Failures aren't reported to the shipper.** If the remote deployment rejects the key, the version is too old, or the endpoint isn't reachable, the records are dropped and the shipper isn't told. Refer to [When a destination can't store data](../destinations.md#streams-destinations-cant-store).

## Related pages [streams-remote-es-related]

* [Destinations](../destinations.md): Compare the destination types, manage destinations, and learn what happens to data a destination can't store.
* [Local Elasticsearch destination](elasticsearch.md): Write to the project you're in with credentials that Streams creates and scopes for you.
* [Amazon S3 destination](s3.md): Write newline-delimited JSON to a bucket you own instead of indexing it.
* [Privileges and API keys](../security.md#streams-security-remote-s3): Learn how Streams stores the credentials you supply and which role can create destinations.
* [Streams limitations](../limitations.md#streams-limitations-destinations): Check which remote deployments and signals aren't supported.
