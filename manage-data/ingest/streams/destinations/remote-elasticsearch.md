---
navigation_title: Remote Elasticsearch
description: Write data from a stream to another Elastic Cloud deployment or Serverless project, using an endpoint and API key that you supply. Streams checks both when you save.
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
  * An Elastic Cloud deployment: either an {{ech}} deployment running 9.5.0 or later, or a {{serverless-short}} project. Self-managed clusters aren't supported.
  * Reachable at its public `https://` endpoint, whose host ends in `.elastic.cloud`, `.elastic-cloud.com`, or `.cloud.es.io`. Copy it from the Elastic Cloud console. Deployments behind traffic filters or private link aren't reachable from Streams.
* An API key created on the remote deployment, in its encoded form, with write access to the target data streams. Give it the least privilege the destination needs: the `create_doc` and `auto_configure` index privileges on the data streams you intend to write to, as for a [Local Elasticsearch destination](elasticsearch.md#streams-es-destination-api-key). The key must also be allowed to write Prometheus metrics to the remote deployment, because that's how Streams checks it when you save, as the next section explains.

## Create the destination [streams-remote-es-create]

You create the destination on the Streams Map, and it exists as soon as you save the dialog:

1. Find **Streams** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Map** tab.
1. Select **Destination** in the toolbar at the bottom of the Map.
1. Under **Where will this destination's data live?**, select **Remote Elasticsearch**.
1. Under **Connect your remote cluster**, enter the remote deployment's **Endpoint** as an `https://` URL without credentials, a query, or a fragment, for example `https://my-cluster.es.us-central1.gcp.elastic.cloud:443`, and paste the encoded **API key**.
1. Under **How should its documents be written?**, choose how records are placed on the remote deployment:
   * **Automatic**: each record is written to the data stream its `data_stream.*` fields name, or to the default data stream for its signal. Documents from a Managed _bulk source go to the `_index` in their request.
   * **Fixed index per signal**: under **Fixed index naming**, choose **One name for all signals** or **Name each signal**, and enter a dataset and a namespace. Streams composes `<signal>-<dataset>.otel-<namespace>` for logs, metrics, and traces, and `metrics-<dataset>.prometheus-<namespace>` for Prometheus Remote Write metrics, exactly as for a Local Elasticsearch destination. Leave a signal's dataset empty to not send that signal. Documents have their own **Documents index** field, used as entered. Refer to [Fixed writing](elasticsearch.md#streams-es-destination-fixed) for the naming rules.
1. Under **Destination details**, enter a **Name** and, optionally, a **Description**. The name must be unique among your destinations and can't be changed later.
1. Select **Create destination**.

The destination appears on the Map with the host of its endpoint under its name. Connect a source, pipeline, or router to it and select **Save changes**. Once records flow, the node shows a rate and a write duration like a Local Elasticsearch destination does. Refer to [Monitor streams](../monitor-streams.md).

Streams encrypts the API key when you save it, and never shows it again. The destination's details show the **Endpoint**, the writing mode under **Routing**, the **API key** as **Configured**, and a **Delivery failures** panel. Destinations can't be edited, so to rotate the key, create a new destination with the new key, reconnect the routing rules to it, and delete the old one.

### What Streams checks when you save [streams-remote-es-check]

Before the destination is saved, Streams checks the endpoint and the key, so that a typo or an unsupported cluster doesn't silently drop data later:

1. The endpoint must be an `https://` URL on `.elastic.cloud`, `.elastic-cloud.com`, or `.cloud.es.io`. Anything else, including a self-managed cluster or a lookalike host, is rejected with **Remote Elasticsearch destinations must use an https:// Elastic Cloud endpoint on .elastic.cloud, .elastic-cloud.com or .cloud.es.io.** before any request goes out.
1. Streams sends an empty Prometheus remote write request to the endpoint with your key. Nothing is indexed. The response decides the outcome:
   * Success: the destination is saved.
   * The cluster has no Prometheus remote write endpoint: rejected with **does not support Prometheus remote write. The remote cluster must run Elasticsearch 9.5.0 or later.** This is how a deployment older than 9.5.0 is detected.
   * The key is invalid, expired, or not allowed to write: rejected with the HTTP status and what to check.
   * The cluster can't be reached, times out, or returns a server error: the destination is saved anyway, with the toast **Could not verify the remote cluster**. Check that the cluster is reachable and that the key can write, because records are dropped until it is.

The check runs when you create a destination. It isn't repeated later, so a key that expires or a deployment that's deleted shows up as delivery failures on the Map instead. Refer to [Monitor streams](../monitor-streams.md#streams-monitor-failures).

## What the destination accepts [streams-remote-es-accepts]

The destination accepts logs, metrics, traces, and documents from a Managed _bulk source. In Fixed mode, a signal you left unnamed is dropped, and documents are dropped when the **Documents index** field is empty.

## How it differs from a Local Elasticsearch destination [streams-remote-es-differences]

Because the credentials and the cluster are yours rather than the project's, a few things work differently:

* **No write patterns.** Streams can't narrow a key you supply, so what the destination may write to is whatever the remote key allows. Scope the key on the remote deployment instead.
* **No index list.** The **Destinations** tab doesn't list the remote data streams or open their details. Manage and inspect them on the remote deployment. The node's rate and write duration, and the **Delivery failures** panel in its details, are the only view of the destination from this project.
* **Failures aren't reported to the shipper.** If the remote deployment rejects the key or the endpoint stops being reachable after the destination was saved, the records are dropped and the shipper isn't told. The destination shows a **Failures** badge on the Map. Refer to [When a destination can't store data](../destinations.md#streams-destinations-cant-store).

## Related pages [streams-remote-es-related]

* [Destinations](../destinations.md): Compare the destination types, manage destinations, and learn what happens to data a destination can't store.
* [Local Elasticsearch destination](elasticsearch.md): Write to the project you're in with credentials that Streams creates and scopes for you.
* [Amazon S3 destination](s3.md): Write newline-delimited JSON to a bucket you own instead of indexing it.
* [Privileges and API keys](../security.md#streams-security-remote-s3): Learn how Streams stores the credentials you supply and which role can create destinations.
* [Streams limitations](../limitations.md#streams-limitations-destinations): Check which remote deployments and signals aren't supported.
