---
navigation_title: Local Elasticsearch
description: Write data from a stream to the Serverless project you're in. Choose Auto or Fixed index mode, set write patterns, and find the data streams it creates.
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

# Local Elasticsearch destination

A **Local Elasticsearch** destination writes data from a stream to the {{serverless-short}} project you're working in. It's the destination for anything you want to search, visualize, and alert on in this project, and the one that most streams end at. One destination is one connection to the project, and the records it carries can land in many data streams, as many as its write patterns allow. Streams creates and manages the destination's credentials for you, so the only decisions are how the target data streams are named and what the destination is allowed to write to.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

## Create the destination [streams-es-destination-create]

To create a Local Elasticsearch destination, you need the **Admin** role, because Streams creates the destination's API key as you. Refer to [Privileges and API keys](../security.md#streams-security-local).

You create the destination on the Streams Map, and it exists as soon as you save the dialog:

1. Find **Streams** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Map** tab.
1. Select **Destination** in the toolbar at the bottom of the Map.
1. Under **Where will this destination's data live?**, select **Local Elasticsearch**.
1. Under **Index mode**, select **Auto (default)** or **Fixed index per signal**, and complete the fields for that mode. The next two sections explain each.
1. Enter a **Destination name** and, optionally, a **Description**. The name must be unique among your destinations and can't be changed later.
1. Select **Create destination**.

The destination appears on the Map showing **Auto** or the index name you entered, and the number of indices and data streams that match its write patterns. Connect a source, pipeline, or router to it and select **Save changes**. The node shows **Data not flowing in** until the first records arrive, then a rate and a write duration. Refer to [Monitor streams](../monitor-streams.md).

## Auto index mode [streams-es-destination-auto]

In **Auto (default)** mode, each record chooses its own data stream, within the destination's write patterns. Keep this mode unless you have a reason not to. It's how the project's existing endpoints behave, and it keeps OpenTelemetry and integration data in the data streams that dashboards and other features expect.

### How Auto mode picks a data stream [streams-es-destination-auto-data-stream]

For each record, in order:

1. If the record names a target, that target is used. For a document from a Managed _bulk source, the target is the `_index` in its bulk `create` action, which the source has already checked starts with `logs-`, `metrics-`, or `traces-`. For an OTLP or Prometheus record, the target is built from the record's signal and its `data_stream.dataset` and `data_stream.namespace` attributes as `<signal>-<dataset>.otel-<namespace>`. The `.otel` suffix marks data streams that hold OpenTelemetry-formatted documents, and Streams adds it for you. A log record with `data_stream.dataset` set to `demo` and `data_stream.namespace` set to `audit` goes to `logs-demo.otel-audit`.
1. Otherwise the record goes to the default data stream for its signal, such as `logs-generic.otel-default` for OTLP logs.
1. If the resulting name falls outside the destination's write patterns, {{es}} rejects the write and the record is dropped. It isn't redirected into an allowed pattern.

Processors in a pipeline upstream of the destination can set or change the `data_stream.*` attributes, which is how you route records to a dataset of your choice without leaving Auto mode.

### Write patterns [streams-es-destination-write-patterns]

Write patterns bound what the destination's API key can write to. By default they're `logs-*-*`, `metrics-*-*`, and `traces-*-*`, one per signal, which is every data stream named `<signal>-<dataset>-<namespace>`. For documents from a Managed _bulk source, the defaults are `logs-*`, `metrics-*`, and `traces-*`, so a document can go to any index whose name starts with one of those prefixes. They don't route data. A pattern of `logs-billing.otel-*` lets a record targeting `logs-billing.otel-prod` through and drops one targeting `logs-checkout.otel-prod`.

To narrow them, turn on **Use custom write patterns**, select the signals the destination should accept, and enter one pattern for each. Signals you don't select aren't sent to this destination. For **Logs**, **Metrics**, and **Traces**, the signal prefix is fixed, so you enter the remainder, for example `billing.otel-*` to allow `logs-billing.otel-*`. Remember the `.otel` suffix that Auto mode adds to the dataset of OTLP and Prometheus records. A pattern of `billing-*` doesn't match `logs-billing.otel-prod`, so those records are dropped. For **Documents**, enter one or more full patterns under **Documents write patterns**, each starting with `logs-`, `metrics-`, or `traces-`.

Patterns follow these rules:

* A pattern for logs, metrics, or traces keeps the `<signal>-<dataset>-<namespace>` shape, so the remainder you enter has exactly one `-` between the dataset part and the namespace part. Use `*` as a wildcard in either part.
* Patterns must be lowercase and can't contain `\ / ? " < > | , # :` or spaces.
* A destination can have at most 32 write patterns across all signals.

Narrowing write patterns is a security boundary as much as a tidiness one, because anyone who can connect a source to this destination can send data anywhere the patterns allow. Refer to [Privileges and API keys](../security.md#streams-security-local).

## Fixed index mode [streams-es-destination-fixed]

In **Fixed index per signal** mode, every record of a signal is written to one data stream that you name, and any target the record itself carries is ignored. Use it when a stream's data should land in exactly one place regardless of what the shippers send, for example a single `logs-audit.otel-prod` data stream for a dedicated audit source.

Under **Fixed index naming**, choose how to name the data streams:

* **Name all OTel signals**: one `dataset-namespace` value applied to logs, metrics, and traces as `<signal>-<dataset>-<namespace>`, so `audit.otel-prod` writes logs to `logs-audit.otel-prod`, metrics to `metrics-audit.otel-prod`, and traces to `traces-audit.otel-prod`.
* **Name signals individually**: a name per signal. Leave a signal blank to not send it to this destination.

Names follow the data stream naming scheme. The signal prefix is fixed, and the dataset and namespace can't contain `-`. Names must be lowercase, can't start with a `.`, and can't be built from field values, so templated index names aren't supported.

Fixed mode doesn't add the `.otel` suffix that Auto mode adds. The OpenTelemetry index templates match only data streams named `<signal>-<dataset>.otel-<namespace>`, so a name like `logs-audit-prod` gets the default mappings rather than the OpenTelemetry ones, and for metrics it isn't a time series data stream. For OTLP and Prometheus Remote Write data, end the dataset with `.otel`, as in the examples above.

Documents from a Managed _bulk source have their own field, **Documents index**, in both choices. Enter any index or data stream name. It's used as entered, with no signal prefix added, and it replaces the `_index` in each request. The request's `_index` must still start with `logs-`, `metrics-`, or `traces-` to pass the source, and the bulk response echoes it, not the index the destination wrote to. Leave the field blank to not send documents to this destination.

## The destination's API key [streams-es-destination-api-key]

When you create the destination, Streams creates an {{es}} API key for it that grants `create_doc` and `auto_configure` on the write patterns, limited to what you yourself can do. If your account can't write to those patterns, the dialog reports **Could not create an API key for this destination** and nothing is saved. Streams stores the key encrypted, and you never see it. Deleting the destination invalidates it. Refer to [Privileges and API keys](../security.md#streams-security-destinations).

## Find and manage the data streams [streams-es-destination-data-streams]

The destination node on the Streams Map shows how many indices and data streams in the project match the destination's write patterns, and the **Destinations** tab lists them. The list is based on the patterns, so it also includes data streams that other shippers write to. Select an index to open its read-only **Overview** and **Retention** tabs. Refer to [View the details of an index](../destinations.md#streams-destinations-index).

The data streams a destination writes to are ordinary {{es}} data streams. Manage their retention, mappings, ingest pipelines, and data quality where you do today, as [classic streams](/solutions/observability/streams/streams.md) in Streams or in **Stack Management**. An ingest pipeline attached to a data stream still runs when Streams hands the data to {{es}}, after any processing you added on the Map.

## Related pages [streams-es-destination-related]

* [Destinations](../destinations.md): Compare the destination types, manage destinations, and learn what happens to data a destination can't store.
* [Remote Elasticsearch destination](remote-elasticsearch.md): Write to another Elastic Cloud deployment with an API key you supply.
* [Amazon S3 destination](s3.md): Write newline-delimited JSON to a bucket you own instead of indexing it.
* [Privileges and API keys](../security.md#streams-security-local): Learn what the destination's API key can do and why the **Admin** role is needed to create one.
* [Monitor streams](../monitor-streams.md): Read the destination's rate, write duration, and index list on the Streams Map.
