---
navigation_title: Managed _bulk
description: Create a Managed _bulk source in Streams and send JSON documents to it with the Elasticsearch bulk API, then process and route them before they're indexed.
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

# Managed _bulk source

A **Managed _bulk** source accepts JSON documents sent with the {{es}} bulk API. Point a script or application that already builds bulk requests at the source instead of at {{es}}, add the source's API key, and the documents go through the pipelines, routers, and destinations you connect on the Streams Map before they're indexed. The source supports only part of the bulk API, and Logstash, Beats, and standalone {{agent}} can't connect to it. Refer to [What the source accepts](#streams-bulk-source-accepts).

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

## Before you begin [streams-bulk-source-prereqs]

To create a Managed _bulk source and send data to it, you need:

* The **Admin** role. Refer to [Privileges and API keys](../security.md#streams-security-view-edit).
* A sender that can send `POST` requests in the bulk format with an `Authorization` header, such as `curl`, a script, or an application you control.

## Create the source [streams-bulk-source-create]

You create the source on the Streams Map, and it exists as soon as you save the dialog:

1. Find **Streams** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Map** tab.
1. Select **Source** in the toolbar at the bottom of the Map.
1. For **Source type**, select **Managed _bulk**, and enter a **Source name**. There's no signal to choose, because the source carries documents only.
1. Select **Continue**, then copy the **Bulk endpoint** and **Bulk endpoint with a target index** URLs and the **API key**. The key isn't shown again. The **cURL** tab under **Send data using** has a complete request with the endpoint and key filled in.
1. Select **Done**, connect the source to a destination on the Map, and select **Save changes**.

The source has two endpoints on the project's ingest host, and both carry the source ID in the path:

```text
https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/elasticsearch/<source-id>/_bulk
https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/elasticsearch/<source-id>/<target>/_bulk
```

The **Bulk endpoint** takes the index from each action's `_index`. The **Bulk endpoint with a target index** also accepts actions without `_index` and sends them to the `<target>` named in the path. Copy the URLs from the source rather than constructing them.

## Send data to the source [streams-bulk-source-send]

Send a `POST` request in the bulk format, with the key in the `Authorization` header. This request creates one document in `logs-myapp-default`:

```bash
curl -X POST "https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/elasticsearch/<source-id>/_bulk" \
  -H "Authorization: ApiKey <key>" \
  -H "Content-Type: application/x-ndjson" \
  --data-binary @- <<EOF
{"create":{"_index":"logs-myapp-default"}}
{"@timestamp":"$(date -u +%Y-%m-%dT%H:%M:%SZ)","message":"hello from _bulk"}
EOF
```

A `201` status on an item means the source queued the document, not that {{es}} indexed it. Indexing happens after the document has passed through the stream, and errors at that stage, such as mapping conflicts, aren't returned to the sender. To confirm that documents arrive, check the destination's indices on the **Destinations** tab or in **Discover**. Refer to [Monitor Streams](../monitor-streams.md).

## What the source accepts [streams-bulk-source-accepts]

The source supports only part of the bulk API. Requests and documents must follow these rules:

* **Actions**: only `create`. Requests that use `index`, `update`, or `delete` are rejected with `400 Bad Request`, and nothing in the request is accepted.
* **Index names**: each document's `_index`, or the `<target>` in the path for documents without one, must start with `logs-`, `metrics-`, or `traces-`. A document with another index name gets a `403` status in its response item, while the rest of the request is accepted and the response is `200 OK`. Check `errors` and the status of each item.
* **Requests**: `POST` bulk requests only. The source has no `GET` routes, so shippers whose {{es}} output checks the server before sending, such as Logstash, Beats, and standalone {{agent}}, hang or fail at that check and never send. Fleet-managed {{agent}} can't be pointed at a source either. Those shippers can keep using the project's existing managed `_bulk` endpoint, whose data isn't processed or routed by Streams. Refer to [Ingest data with the Managed {{es}} _bulk endpoint](opentelemetry://reference/managed-inputs/elasticsearch-bulk.md).
* **Responses**: the response echoes the `_index` you requested, even when a destination in Fixed index mode writes the document somewhere else.
* **Unmatched documents**: a document that matches no routing rule on the Streams Map is dropped. Refer to [Route data](../route-data.md).

## Documents in pipelines and destinations [streams-bulk-source-documents]

A Managed _bulk source carries one signal, **Documents**, which is a signal of its own next to logs, metrics, and traces. A document travels through Streams as the JSON you sent, and a destination stores it as a document rather than as an OpenTelemetry record. Where a processor, a routing rule, or a destination asks which signals it applies to, documents appear as **Documents**. In a processor, address a field of the document with the **Document** location and the field's key, such as `order.status`. A dotted key is one key, not a path into nested objects. Refer to [Process data](../process-data.md).

How a destination handles documents depends on its type:

* A **Local Elasticsearch** destination accepts documents in every index mode. In **Auto** mode, each document is written to its `_index`, within the destination's write patterns, which for documents are `logs-*`, `metrics-*`, and `traces-*` by default. With custom write patterns, the **Documents write patterns** bound what documents can be written to, and each pattern must start with `logs-`, `metrics-`, or `traces-`. In **Fixed index per signal** mode, the **Documents index** field names one index or data stream that every document goes to. It's used as entered, with no signal prefix added, and it replaces the `_index` in each request, which must still start with `logs-`, `metrics-`, or `traces-` to pass the source. Leave the field blank to not send documents to the destination. Refer to [Local Elasticsearch destination](../destinations/elasticsearch.md).
* An **Amazon S3** destination writes documents to the bucket as newline-delimited JSON, like the other signals. Refer to [Amazon S3 destination](../destinations/s3.md).
* A **Remote Elasticsearch** destination doesn't accept documents yet. Documents routed to one are dropped at that destination. Refer to [Remote Elasticsearch destination](../destinations/remote-elasticsearch.md).

## Related pages [streams-bulk-source-related]

* [Sources](../sources.md): Compare the source types and manage sources and their API keys.
* [OTLP source](otlp.md): Send OpenTelemetry logs, metrics, and traces instead of bulk documents.
* [Prometheus Remote Write source](prometheus-remote-write.md): Send Prometheus metrics instead of bulk documents.
* [Ingest data with the Managed {{es}} _bulk endpoint](opentelemetry://reference/managed-inputs/elasticsearch-bulk.md): Learn about the project's shared bulk endpoint, which Logstash, Beats, and standalone {{agent}} can use.
* [Troubleshoot Streams](../troubleshooting.md): Find out what a `401` or `403` response from a source endpoint means.
