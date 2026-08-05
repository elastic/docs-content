---
navigation_title: Columnar storage
description: Learn when to use columnar index mode to store data once for analytics and search with a smaller storage footprint.
applies_to:
  stack: preview 9.5
  serverless: preview
products:
  - id: elasticsearch
---

# Columnar index mode [columnar-index-mode]

Columnar index mode turns {{es}} into an analytical and search columnar store for the indices where you enable it.
Instead of keeping multiple copies of each field for different query paths, columnar mode stores fields once as [doc values](elasticsearch://reference/elasticsearch/mapping-reference/doc-values.md) by default.
This strategy can reduce storage cost for high-volume, analytics-heavy data while keeping the same APIs, dashboards, and integrations.

Columnar mode ships alongside existing index modes such as `standard`, [`logsdb`](/manage-data/data-store/data-streams/logs-data-stream.md), and [`time_series`](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md).
You choose it per index (or in a template) at creation time; you can't change the mode after the index has been created.

This page explains what columnar index mode is, when to use it, and how it fits with the rest of the {{es}} data store.
<!--
TO-DO after https://github.com/elastic/elasticsearch/pull/151739 merges
For enablement steps, sorting, `_source` modes, and limitations, refer to [Columnar index mode](elasticsearch://reference/columnar/index.md) in the {{es}} reference.
-->

## When to use columnar index mode [when-to-use-columnar]

Choose columnar index mode when your data is written in volume, queried analytically (filters, aggregations, and dashboards), and retained for a long time. Typical fits include:

* Logs, traces and observability at scale: High ingest rates where storage and aggregation cost dominate, and you still need full-text search on message fields.
* Security telemetry and threat hunting: Faceted exploration and historical lookups over large event stores, without giving up search behavior for pivot and lookup workflows.
* Operational and business analytics: Dashboards and aggregations over application events, transactions, or IoT readings that would otherwise push you to a separate analytics store.

Columnar mode isn't a universal default.

Prefer a `standard` index (or another specialized mode) when your workload is document-centric search that needs the original JSON `_source` as submitted, or when you rely on inverted indexes and related structures on most fields by default.

For metrics that need time series dimensions and metric field semantics, use a [time series data stream](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) instead.

For logs that should keep the current `logsdb` defaults without switching to a fully columnar store, use a [logs data stream](/manage-data/data-store/data-streams/logs-data-stream.md).

## Columnar modes [columnar-modes]

Two values of [`index.mode`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-mode-setting) enable columnar storage:

`columnar`
:   A general-purpose columnar store with no use-case-specific defaults.
:   Use it for bare indices and data streams that aren't log-oriented.

`logsdb_columnar`
:   The same columnar storage behavior with logging-oriented defaults, including a default `@timestamp` mapping and index sorting when `@timestamp` and `host.name` are present.
:   Use it for log data when you want columnar storage rather than the default [`logsdb`](/manage-data/data-store/data-streams/logs-data-stream.md) mode.

Both modes apply to indices and to data stream backing indices configured through templates.

## How it works [how-columnar-works]

At a high level, columnar index mode changes storage defaults while leaving the document and query model familiar:

* Store once, by field: Non-text fields are stored as doc values and aren't indexed by default, which avoids paying for structures your analytics workload may not need.
* Keep search where it matters: Text fields remain indexed by default so full-text search continues to work on fields such as log messages.
* Flat field layout: Object and passthrough mappings are flattened to leaf fields, which matches how columnar systems organize data for efficient scanning and compression.

Index sorting remains important for compression and query performance.
`logsdb_columnar` sets sensible sort defaults for logs; for `columnar`, you choose sort fields that match your access patterns.
<!--
TO-DO: Wait for related PR to merge
Details are in the [reference](elasticsearch://reference/columnar/index.md#index-sorting).
-->

Columnar mode doesn't replace the [core data store concepts](/manage-data/data-store/index-basics.md):

* You still store JSON documents in indices (or data streams), define mappings, and target indices by name, alias, or stream.
* Shards, replicas, and near real-time search behave as they do for other index modes.
* Existing query languages, {{kib}} visualizations, alerts, and ingest integrations continue to work against columnar indices.

What changes is how {{es}} lays data out on disk and which structures it builds by default, not how you interact with the cluster day to day.

## Next steps [columnar-next-steps]

<!--
TO-DO: Wait for related PR to merge
* [Enable and configure columnar index mode](elasticsearch://reference/columnar/index.md): Create indices or templates with `columnar` or `logsdb_columnar`, configure index sorting, and review `_source` modes and limitations. -->
* [Logs data streams](/manage-data/data-store/data-streams/logs-data-stream.md): Use `logsdb` for efficient log storage with current defaults, or move to `logsdb_columnar` when you're ready for the columnar logs profile.
* [Time series data streams](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md): Choose TSDS when your data is metrics with dimensions, not a general columnar analytics workload.
* [Index fundamentals](/manage-data/data-store/index-basics.md): Review documents, mappings, settings, and shards if you're new to {{es}} storage concepts.

## Related pages [columnar-related-pages]

<!--
TO-DPO: Wait for related PR to merge
* [Columnar index mode reference](elasticsearch://reference/columnar/index.md)
-->
* [`index.mode` setting](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-mode-setting)
* [The {{es}} data store](/manage-data/data-store.md)
