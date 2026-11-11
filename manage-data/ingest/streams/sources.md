---
navigation_title: Sources
description: Learn what a source is in Streams, which source types and signals exist, how endpoints and API keys are issued, and how to point a shipper at a source.
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

# Sources

A source is how data enters Streams. It's an endpoint of a given type, with its own API keys, that your shippers send to. Everything connected downstream of a source on the Streams Map, the pipelines, routers, and destinations, applies to all the data that enters through it. Create a separate source for each kind of traffic you want to process or route differently.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

## Source types [streams-sources-types]

Streams offers three source types, each for a different protocol:

| Source type | Protocol | Signals | Typical senders |
| --- | --- | --- | --- |
| [OTLP endpoint](sources/otlp.md) | OpenTelemetry Protocol over HTTP | Logs, metrics, traces, chosen at creation | OpenTelemetry Collectors, including {{agent}} in OpenTelemetry mode, OpenTelemetry SDKs, the OpenTelemetry Kubernetes Operator |
| [Prometheus Remote Write](sources/prometheus-remote-write.md) | Prometheus Remote Write 1.0 | Metrics | Prometheus, Grafana Alloy, and other Remote Write senders |
| [Managed _bulk](sources/elasticsearch-bulk.md) | {{es}} bulk API | Documents | Scripts and applications that send bulk requests directly, such as with `curl` |

An OTLP endpoint source accepts only the signals selected when it's created. Prometheus Remote Write and Managed _bulk sources each carry one signal, so there's nothing to select. A source's type and name can't be changed after you create it. To change either, create a new source and point your shippers at it.
## Endpoints and API keys [streams-sources-endpoints-keys]

When you create a source, Streams generates an API key for it and shows the key once, together with the endpoint URLs and ready-made configuration snippets for common senders. The key allows writing to that source and nothing else. Senders send it in every request as the HTTP header `Authorization: ApiKey <key>`.

Each source gets its own endpoint URLs on the project's ingest host, which carry the source ID:

```text
https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/otlp/<source-id>/v1/<signal>
https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/prometheus-remote-write/<source-id>/api/v1/write
https://<project>.ingest.<region>.<provider>.elastic.cloud/inputs/elasticsearch/<source-id>/_bulk
```

Streams derives the source ID from the name you enter. It lowercases the name and replaces each run of other characters with a hyphen, so `My OTLP source` becomes `my-otlp-source`. If another source already has that ID, Streams adds a number to the end. Copy the URLs from the source rather than constructing them.

For what a source key can and can't do, refer to [Privileges and API keys](security.md#streams-security-source-keys).

## Create a source [streams-sources-create]

You create a source from the **Source** button in the toolbar at the bottom of the [Streams Map](streams-map.md), or from **Add source** on the **Sources** tab, which opens the same dialog. You need the **Admin** role. Refer to [Privileges and API keys](security.md#streams-security-view-edit).

The dialog asks for the **Source type** and a **Source name**, neither of which can be changed later, and for an OTLP endpoint source, the **Signals** it accepts. Streams saves the source when you select **Continue**, generates its API key, and shows the key once with the endpoint URLs and configuration snippets for common senders. The source then appears on the Map. Before you send data, connect the source to a destination and select **Save changes**. A source that isn't connected to anything accepts records and drops them.

For the steps and the fields of each type, refer to [OTLP source](sources/otlp.md#streams-otlp-source-create), [Prometheus Remote Write source](sources/prometheus-remote-write.md#streams-prw-source-create), or [Managed _bulk source](sources/elasticsearch-bulk.md#streams-bulk-source-create).

## Manage sources [streams-sources-manage]

The **Sources** tab in **Streams** lists every source as a row, with its **Name**, its **Type**, and the **Destinations** its data is sent to, or **Not connected** if it isn't connected to anything yet. Use the tab to find a source, inspect it, manage its API keys, or delete it:

* **Find a source**: Type in the search field to filter the list, or open **Type** and select one or more source types. Select **Refresh** to reload the list.
* **See a source on the Map**: Select {icon}`waypoint` **Show on map** in its row. The [Streams Map](streams-map.md) opens with the search set to the source's name, so you see the source and everything connected to it.
* **Open a source**: Select its name. The details list the destinations it's connected to and its endpoint URLs, each with a copy button. An OTLP endpoint source has one URL for each signal it accepts, and a Managed _bulk source has one with and one without a target index in the path.
* **Manage its API keys**: Under **API key**, select **Generate key** to create a new key, for example after a key is lost or needs rotating. The key is shown once. More than one key can be valid at a time, so you can switch senders over before you delete the old key. Select **Delete** next to a key to revoke it. Applications using that key can no longer send data.
* **Delete a source**: Open the **Source actions** menu in its row and select **Delete**, or select **Delete source** under **Danger area** in its details, then confirm. To delete several sources at once, select their checkboxes and select **Delete selected sources**. The deletion is saved immediately. It removes the source from the Map and invalidates its keys.
* **Add a source**: Select **Add source**. It opens the same dialog as **Source** on the Map. Refer to [Create a source](#streams-sources-create).

Each row of the **Sources** table has these columns:

| Column | What it shows |
| --- | --- |
| **Name** | The name you gave the source. Select it to open the source's details. |
| **Type** | **OTLP endpoint**, **Prometheus Remote Write**, or **Managed _bulk**. |
| **Destinations** | The destinations the source's data reaches, through any pipelines and routers on the way, or **Not connected** if the source isn't connected to anything yet. |

## Related pages [streams-sources-related]

* [OTLP source](sources/otlp.md): Send OpenTelemetry logs, metrics, and traces from a collector, an SDK, or the Kubernetes Operator.
* [Prometheus Remote Write source](sources/prometheus-remote-write.md): Send metrics from Prometheus or Grafana Alloy.
* [Managed _bulk source](sources/elasticsearch-bulk.md): Send JSON documents with the {{es}} bulk API from a script or application.
* [Work with the Streams Map](streams-map.md): Connect a source to pipelines, routers, and destinations, and save the result.
* [Privileges and API keys](security.md): Learn what a source key can do and how to rotate and revoke keys.
* [Streams limitations](limitations.md#streams-limitations-sources): Check which shippers and protocols sources don't support.
