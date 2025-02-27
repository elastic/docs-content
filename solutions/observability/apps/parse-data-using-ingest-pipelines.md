---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-ingest-pipelines.html
---

# Parse data using ingest pipelines [apm-ingest-pipelines]

Ingest pipelines preprocess and enrich APM documents before indexing them. For example, a pipeline might define one processor that removes a field, one that transforms a field, and another that renames a field.

The default APM pipelines are defined in {{es}} apm-data plugin index templates. {{es}} then uses the index pattern in these index templates to match pipelines to APM data streams.


## Custom ingest pipelines [custom-ingest-pipelines]

Elastic APM supports custom ingest pipelines. A custom pipeline allows you to transform data to better match your specific use case. This can be useful, for example, to ensure data security by removing or obfuscating sensitive information.

Each data stream ships with a default pipeline. This default pipeline calls an initially non-existent and non-versioned "`@custom`" ingest pipeline. If left uncreated, this pipeline has no effect on your data. However, if utilized, this pipeline can be used for custom data processing, adding fields, sanitizing data, and more.

In addition, ingest pipelines can also be used to direct application metrics (`metrics-apm.app.*`) to a data stream with a different dataset, e.g. to combine metrics for two applications. Sending other APM data to alternate data streams, like traces (`traces-apm.*`), logs (`logs-apm.*`), and internal metrics (`metrics-apm.internal*`) is not currently supported.


## `@custom` ingest pipeline naming convention [custom-ingest-pipeline-naming]

`@custom` pipelines are specific to each data stream and follow a similar naming convention: `<type>-<dataset>@custom`. As a reminder, the default APM data streams are:

* Application traces: `traces-apm-<namespace>`
* RUM and iOS agent application traces (Elastic Stack only): `traces-apm.rum-<namespace>`
* APM internal metrics: `metrics-apm.internal-<namespace>`
* APM transaction metrics: `metrics-apm.transaction.<metricset.interval>-<namespace>`
* APM service destination metrics: `metrics-apm.service_destination.<metricset.interval>-<namespace>`
* APM service transaction metrics: `metrics-apm.service_transaction.<metricset.interval>-<namespace>`
* APM service summary metrics: `metrics-apm.service_summary.<metricset.interval>-<namespace>`
* Application metrics: `metrics-apm.app.<service.name>-<namespace>`
* APM error/exception logging: `logs-apm.error-<namespace>`
* Applications UI logging: `logs-apm.app.<service.name>-<namespace>`

To match a custom ingest pipeline with a data stream, follow the `<type>-<dataset>@custom` template, or replace `-namespace` with `@custom` in the table above. For example, to target application traces, you’d create a pipeline named `traces-apm@custom`.

The `@custom` pipeline can directly contain processors or you can use the pipeline processor to call other pipelines that can be shared across multiple data streams or integrations. The `@custom` pipeline will persist across all version upgrades.


## Create a `@custom` ingest pipeline [custom-ingest-pipeline-create]

The process for creating a custom ingest pipeline is as follows:

* Create a pipeline with processors specific to your use case
* Add the newly created pipeline to an `@custom` pipeline that matches an APM data stream

If you prefer more guidance, see one of these tutorials:

* [Ingest pipeline filters](custom-filters.md#apm-filters-ingest-pipeline) — Learn how to obfuscate passwords stored in the `http.request.body.original` field.
* [APM data stream rerouting](data-streams.md#apm-data-stream-rerouting) — Learn how to reroute APM data to user-defined APM data streams.

