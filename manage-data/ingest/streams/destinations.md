---
navigation_title: Destinations
description: Learn what a destination is in Streams, which types exist, how their credentials are created or supplied, and what happens to data a destination can't store.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Destinations

A destination is where a stream ends. It's the place data is written to, together with the credentials used to write it. Every stream needs at least one. A record reaches a destination after it has passed through the pipelines and routers between the source and the destination, and the same record can reach several destinations when a router copies it.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

A destination is a connection, not an index. A Local or Remote Elasticsearch destination is one connection to one {{serverless-short}} project or {{ech}} deployment. The records it carries can land in many data streams and indices, as many as its write patterns allow. An Amazon S3 destination is one connection to one bucket. On the Streams Map, each destination is one node. On the **Destinations** tab, each destination is one row, and you expand the row to see the indices and data streams that match its write patterns.

## Destination types [streams-destinations-types]

When you create a destination, you first answer **Where will this destination's data live?** The three choices differ in where the data goes and who supplies the credentials:

| Choice | Writes to | Credentials | Use it for |
| --- | --- | --- | --- |
| [Local Elasticsearch](destinations/elasticsearch.md) | The {{serverless-short}} project you're working in | Created by Streams and scoped to the destination's write patterns | Data you search and analyze in this project |
| [Remote Elasticsearch](destinations/remote-elasticsearch.md) | Another Elastic Cloud deployment or project on 9.5 or later | An API key from the remote deployment that you supply | A copy in another region, team, or deployment, including {{ech}} |
| [External storage](destinations/s3.md) | An Amazon S3 bucket you own, as newline-delimited JSON | An AWS access key pair that you supply | The complete record, kept on infrastructure you control, while you index only a subset |

**External storage** is the name of the choice in the dialog. Once the destination exists, the Streams Map and the **Destinations** tab show its type as **Amazon S3**, and these pages call it an Amazon S3 destination.

Destinations can't be edited after you create them. To change a destination's name, type, credentials, or index settings, create a new destination, reconnect the routing rules, and delete the old one.

## Signals and index modes [streams-destinations-signals-modes]

Destinations are signal-aware. The signals are logs, metrics, and traces, and documents from a Managed _bulk source, shown as **Documents**. A record of a signal that the destination doesn't accept is dropped at that destination. If a source accepts logs, metrics, and traces and the destination accepts only logs, add a [router](route-data.md) and send the metrics and traces to a destination of their own. A Remote Elasticsearch destination doesn't accept documents.

An {{es}} destination also has an index mode, which decides the data stream or index each record is written to. **Auto (default)** takes the target from the record itself, and **Fixed index per signal** writes every record of a signal to one index that you name. Refer to [Local Elasticsearch destination](destinations/elasticsearch.md#streams-es-destination-auto).

## Create a destination [streams-destinations-create]

You create a destination from the **Destination** button in the toolbar at the bottom of the [Streams Map](streams-map.md), or from **Add destination** on the **Destinations** tab, which opens the same dialog. You need the **Admin** role. Refer to [Privileges and API keys](security.md#streams-security-view-edit).

The dialog asks where the data will live, for the fields of that type, and for a **Destination name** that must be unique among your destinations and can't be changed later. Streams saves the destination when you select **Create destination**, and it appears on the Map. Connect a source, pipeline, or router to it and select **Save changes**. A Local Elasticsearch destination shows **Data not flowing in** until the first records arrive, then a rate and a write duration. Remote Elasticsearch and Amazon S3 destinations show no state, so check for the data on the remote side. Refer to [Monitor streams](monitor-streams.md).

For the steps and the fields of each type, refer to [Local Elasticsearch destination](destinations/elasticsearch.md#streams-es-destination-create), [Remote Elasticsearch destination](destinations/remote-elasticsearch.md#streams-remote-es-create), or [Amazon S3 destination](destinations/s3.md#streams-s3-destination-create).

## Manage destinations [streams-destinations-manage]

The **Destinations** tab in **Streams** lists every destination as a row, with its **Name** and the signals it accepts, its **Type**, and, for a Local Elasticsearch destination, the number of **Indices** that match its write patterns. Use the tab to find a destination, check the indices it can write to, or delete it:

* **Find a destination**: Type in the search field to filter the list, or open **Type** and select one or more destination types. Select **Refresh** to reload the list.
* **See a destination on the Map**: Select {icon}`waypoint` **Show on map** in its row. The [Streams Map](streams-map.md) opens with the search set to the destination's name, so you see the destination and everything connected to it.
* **View the indices behind a Local Elasticsearch destination**: Expand its row to list every index and data stream in the project that matches the destination's write patterns. The list is based on the patterns, not on what the stream delivered, so with the default patterns it includes data streams that integrations and other shippers write to, and it's filled before the destination writes anything. If nothing matches, the row says **No indices match this destination's write scope yet.** Select an index name to open the index view described in [View the details of an index](#streams-destinations-index). For what the numbers tell you about a running stream, refer to [Monitor streams](monitor-streams.md#streams-monitor-indices).
* **View a Remote Elasticsearch or Amazon S3 destination**: Expand its row to see its configuration. Credentials show as **Configured**, never their value.
* **Delete a destination**: Open the **Destination actions** menu in its row and select **Delete**, then confirm. The deletion is saved immediately. It removes the destination from the Map and invalidates the key Streams created for it. Routing rules that pointed to it must be given a new target before you can save.
* **Add a destination**: Select **Add destination**. It opens the same dialog as **Destination** on the Map. Refer to [Create a destination](#streams-destinations-create).

Each row of the **Destinations** table has these columns:

| Column | What it shows |
| --- | --- |
| **Name** | The name you gave the destination, with a badge for each signal it accepts: **Logs**, **Metrics**, **Traces**, or **Documents**. |
| **Type** | **Local Elasticsearch**, **Remote Elasticsearch**, or **Amazon S3**. |
| **Indices** | For a Local Elasticsearch destination, the number of indices and data streams that match its write patterns. Other types show `-`. |

The expanded row of a Local Elasticsearch destination lists the matching indices with these columns:

| Column | What it shows |
| --- | --- |
| **Index name** | The data stream or index. Select it to open its details. |
| **Documents** | The number of documents in it. |
| **Ingestion** | The current ingestion rate, in documents per second. |
| **Storage** | The size it takes on disk. |
| **Health** | The index health reported by {{es}}: **Green**, **Yellow**, or **Red**. |
| **Data quality** | **Good**, **Degraded**, or **Poor**, based on the share of degraded and failed documents. Refer to [Manage data quality](/solutions/observability/streams/manage-data-quality.md). |
| **Failure store** | **On** or **Off**. The failure store is where {{es}} keeps records that failed to index instead of dropping them. Refer to [Failure stores](../../data-store/data-streams/failure-store.md). |
| **Retention** | The data retention period, or **Indefinite** when none is set. |

**Health**, **Data quality**, and **Failure store** are available for data streams only. An index you named in Fixed index mode that isn't a data stream shows no value for them.

### Open a destination from the Map [streams-destinations-open]

Selecting a destination on the [Streams Map](streams-map.md) opens a panel with the same information as the expanded row on the **Destinations** tab. What's in it depends on the destination type:

* **Remote Elasticsearch or Amazon S3**: The destination's configuration.
* **Local Elasticsearch**: The list of indices and data streams that match the destination's write patterns, with a **Documents** chart above it. In the panel, you can:
  * Pick a time range for the chart and read the **Docs total**, **Docs in time range**, and **Peak ingest rate** figures under it.
  * Search the indices or filter them by **Data quality**.
  * Select an index name to open the [index view](#streams-destinations-index) in the same panel.

**Delete destination** at the bottom of the panel deletes the destination after you confirm.

### View the details of an index [streams-destinations-index]

To open the details of a data stream or index listed for a Local Elasticsearch destination, select its name on the **Destinations** tab or in the destination's panel on the Streams Map. The details are read-only and have two tabs:

* **Overview**: The **Documents** chart for the time range you pick, with **Docs total**, **Docs in time range**, and **Peak ingest rate**. Under it, **Dataset quality** shows the share of **Degraded docs** and **Failed docs**, the number of **Ignored fields**, and the **Top failure reasons**.
* **Retention**: A **Lifecycle summary** with the data retention period, or the ILM policy that manages the data stream, and a **Storage summary** with its size and document count. Under them, **Data lifecycle** shows the data phases, and the daily and monthly ingestion averages sit next to an **Ingestion over time** chart. This tab is available for data streams only.

The header shows two badges, the index's data quality, such as **Degraded quality**, and its retention period. To change retention, mappings, or the ingest pipeline, select **Manage in Stack Management**. To look at the documents, select **View in Discover**.

## When a destination can't store data [streams-destinations-cant-store]

A destination that can't store a record, because the target index is outside the write patterns, the credential is invalid, or the remote deployment isn't reachable, drops it after the retry window. A failing destination doesn't block the stream, so the other destinations connected to the same source keep receiving data. The shipper isn't told about the drop, and the Streams Map doesn't report it. To find out whether data is being stored, refer to [What isn't reported](monitor-streams.md#streams-monitor-not-reported). For what Streams doesn't guarantee, refer to [Streams limitations](limitations.md#streams-limitations-data).

## Related pages [streams-destinations-related]

* [Local Elasticsearch destination](destinations/elasticsearch.md): Write to the project you're in, and choose how data streams are named and what the destination is allowed to write to.
* [Remote Elasticsearch destination](destinations/remote-elasticsearch.md): Write to another Elastic Cloud deployment with an API key you supply.
* [Amazon S3 destination](destinations/s3.md): Write newline-delimited JSON to a bucket you own.
* [Work with the Streams Map](streams-map.md): Connect sources, pipelines, and routers to destinations, and save the result.
* [Route data](route-data.md): Send different records to different destinations, or copy a record to more than one.
* [Privileges and API keys](security.md#streams-security-destinations): Learn how destination credentials are created or stored and which role can create destinations.
* [Streams limitations](limitations.md#streams-limitations-destinations): Check what destinations don't support.
