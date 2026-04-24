---
description: Log every search operation on an Elasticsearch cluster including Query DSL, ES|QL, EQL, and SQL query types, with configurable duration thresholds and per-field output control.
applies_to:
  deployment:
    self: ga 9.4
    serverless: unavailable
---

# Query logging [logging]

{{es}} can log every querying operation performed on the cluster. This supports [DSL searches](elasticsearch://reference/query-languages/querydsl.md), [{{esql}}](elasticsearch://reference/query-languages/esql.md), [SQL](elasticsearch://reference/query-languages/sql.md), [EQL](elasticsearch://reference/query-languages/eql/eql-syntax.md) and other APIs that search or query {{es}} indices.

## Supported query types

The following query types are supported:

- `dsl`: Logs every search operation performed on the cluster using [Query DSL](elasticsearch://reference/query-languages/querydsl.md).
- `esql`: Logs every query operation performed on the cluster using [{{esql}}](elasticsearch://reference/query-languages/esql.md).
- `eql`: Logs every query operation performed on the cluster using [EQL](elasticsearch://reference/query-languages/eql/eql-syntax.md).
- `sql`: Logs every query operation performed on the cluster using [SQL](elasticsearch://reference/query-languages/sql.md).

## Enable query logging

By default, query logging is turned off. To enable logging, set the `elasticsearch.querylog.enabled` property to `true` in the `elasticsearch.yml` configuration file:

```yaml
elasticsearch.querylog.enabled: true
```
Alternatively, use the [cluster settings API]({{es-apis}}operation/operation-cluster-put-settings).

Queries that query only system indices are not logged by default. To enable logging these queries, use the `elasticsearch.querylog.include.system_indices` setting described in [the configuration section](#configure-query-logging).

## Finding the logs [finding-query-logs]

Query log entries are written on the **coordinating** node for the request: the node that received the client request, not on every data node that participates in the search. If you are unsure what that means in your topology, start with [Node roles and the data path](https://www.elastic.co/docs/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles).

The log is a file in the {{es}} [log directory](https://www.elastic.co/docs/deploy-manage/monitor/logging-configuration) on that node. Filenames use the `*_querylog.json` pattern (for example, `mycluster_querylog.json`). Each line in that log file is a JSON object for one query. [Enable query logging](#enable-query-logging) to start writing the file, and [Configure query logging](#configure-query-logging) to set the duration threshold, user information, system index coverage, and other `elasticsearch.querylog` options.

From 9.4 onward, the subsections that follow also describe a managed `logs-elasticsearch.querylog` data stream, shippers, and what to open in {{kib}}. Earlier releases do not include that managed index template and data stream. Collect `*_querylog.json` on disk and ship and map those events with your own pipeline if you need a similar experience on an older version.

### Managed data stream and index template (9.4+)

9.4 ships a managed index template, `logs-elasticsearch.querylog@template`, for the `logs-elasticsearch.querylog-*` data stream. The template provides mappings and data stream options so that shipped events land in a single, ECS-aligned destination you can use with {{kib}} and the Elastic Agent / {{beats}} assets that ship together with the product.

* **Index mode:** the data stream uses LogsDB indexing.
* **Query volume:** when logging is on, the default for `elasticsearch.querylog.threshold` is 0 (in [time units](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#time-units)), so every request can be eligible, depending on other options. A busy cluster can produce a very large number of lines; [raise the threshold in Configure query logging](#configure-query-logging) if you need to cap volume.
* **Retention and failure handling:** a default [data stream lifecycle](https://www.elastic.co/docs/manage-data/lifecycle/data-stream) is attached with a 2 day retention window so the data stream does not grow without bound. The [failure store](https://www.elastic.co/docs/manage-data/data-store/data-streams/failure-store) is on, with a 7 day retention for failed ingest.
* **Management UI:** you can also work with the data stream (lifecycle, routing, and related controls) in the **Streams** app.

### {{ech}} [ech-query-logs]

On 9.4+ Elastic Cloud (hosted) deployments, [turn on Logs and metrics](https://www.elastic.co/docs/deploy-manage/monitor/stack-monitoring/ece-ech-stack-monitoring#enable-logging-and-monitoring-steps) for the deployment first so it can ship logs to your monitoring or log destination cluster. Then [enable query logging for the {{es}} cluster](#enable-query-logging) so the coordinated query log file can be collected and shipped. The receiving cluster should run a 9.4+ stack for a fully supported end-to-end path.

### Self-managed

On a 9.4+ cluster, [enable query logging](#enable-query-logging) and [configure](#configure-query-logging) the `elasticsearch.querylog` settings first. The subsections that follow cover [Filebeat](#self-managed-filebeat), the [Elastic Agent](#self-managed-elastic-agent) integration, [bundled Kibana assets](#self-managed-bundled-assets) from the integration, and the [destination cluster version](#self-managed-destination-cluster) to target.

* **Default / single-cluster:** Use either [Filebeat](#self-managed-filebeat) or [Elastic Agent](#self-managed-elastic-agent) to collect and index your query logs.
* **[{{eck}} (ECK)](https://www.elastic.co/docs/deploy-manage/deploy/cloud-on-k8s):** default recipes wire the shipper to the `*_querylog.json` path; see [Filebeat](#self-managed-filebeat) for the `querylog` fileset behavior, subject to the ECK and {{es}} [version you run](https://www.elastic.co/docs/deploy-manage/deploy/cloud-on-k8s).
* **ECE (Elastic Cloud Enterprise):** in-product, fully guided collection for the managed data stream in the ECE UI is planned in an upcoming minor release. When that ships, the experience will match [{{ech}}](#ech-query-logs). Until then, use the same [Filebeat](#self-managed-filebeat) or [Elastic Agent](#self-managed-elastic-agent) path as a default self-managed install.

#### Filebeat [self-managed-filebeat]

[Filebeat](https://www.elastic.co/docs/reference/beats/filebeat) 9.4 extends the [{{es}}](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-module-elasticsearch) module with a `querylog` [fileset](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-module-elasticsearch#_querylog_log_fileset_settings) that reads the `*_querylog.json` files and sends events to the `logs-elasticsearch.querylog-default` data stream. Configure Filebeat on the nodes that emit query logs and enable the `querylog` fileset.

#### Elastic Agent [self-managed-elastic-agent]

The [`elasticsearch` Elastic Agent integration](https://www.elastic.co/docs/reference/integrations/elasticsearch) (1.21.0+) can also collect and ship the same file to the data stream. Follow the [query log settings](https://www.elastic.co/docs/reference/integrations/elasticsearch#querylog) in the integration to enable collection.

#### Bundled assets (integration 1.21.0+) [self-managed-bundled-assets]

The integration bundles the following Kibana assets that you can install even if you do not use the Agent to ship the query logs, including:

* A data view, “Elasticsearch query logs,” for `logs-elasticsearch.querylog-*`
* A dashboard, “Elasticsearch query analytics,” for analyzing your historical queries

Install the assets from Fleet (or the integration’s Assets tab) when you are ready to explore the indexed stream.

#### Destination (monitoring) cluster version [self-managed-destination-cluster]

The cluster that ingests the query log stream (often your monitoring or logging cluster) should run 9.4+ to match the managed template, data stream, and field model. We do not support sending this stream to older {{es}} versions: ingest can fail, or the cluster can only apply part of the index mappings and settings.

:::{important}
**Index privileges for the user that Filebeat or Agent uses**

The `logs-elasticsearch.querylog-default` data stream is a separate destination from `filebeat-*` indices that often store [{{stack}} monitoring](https://www.elastic.co/docs/deploy-manage/monitor/stack-monitoring) metrics and logs. Grant the output user in {{es}} the index and ingest privileges the managed data stream needs for `logs-elasticsearch.querylog-*`, in addition to anything you allow for `filebeat-*` or other indices. The exact role name is your choice; the critical part is the extra privilege on the querylog data stream. That applies to the shippers described in [Filebeat](#self-managed-filebeat) and [Elastic Agent](#self-managed-elastic-agent) above.
:::

### View query logs in {{kib}} (on the destination cluster)

After the shipper is ingesting into `logs-elasticsearch.querylog-*` on the cluster you use for log analysis:

* Open the “Elasticsearch query analytics” dashboard if you installed the integration’s saved objects.
* Or [create a data view](https://www.elastic.co/docs/explore-analyze/find-and-organize/data-views) on `logs-elasticsearch.querylog-*` and in **Discover** filter to `event.dataset: elasticsearch.querylog` to work with the raw field set.

## Configure query logging  [configure-query-logging]

The following configuration options are available:

- `elasticsearch.querylog.enabled`: Enables or disables query logging. Set to `true` to enable. Defaults to `false`.
- `elasticsearch.querylog.threshold`: Sets the request duration threshold (in [time units](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#time-units), like `100ms` or `5s`) for logging events. If greater than 0, only requests with durations equal to or greater than the threshold are logged. The default is 0.
- `elasticsearch.querylog.include.user`: Enables or disables logging of user information. Set to `false` to disable. Defaults to `true`.
- `elasticsearch.querylog.include.system_indices`: Controls whether queries targeting only system indices are included in the logs. Set to `true` to include them. Defaults to `false`.

## Log field reference

Each query log entry is a JSON object with fields from two sources:

- Standard [Elastic Common Schema (ECS)](ecs://reference/index.md) fields present in every entry.
- Query-specific fields under the `elasticsearch.querylog.*` namespace with details about the operation.

### Standard fields

These fields are present regardless of query type. Some fields may be present only in specific circumstances, see field descriptions below.

- `@timestamp`: The timestamp of the log entry.
- `event.outcome`: Whether the request was successful (`success`) or not (`failure`).
- `event.duration`: How long (in nanoseconds) the request took to complete.
- `error.type` and `error.message`: Error information fields if the request failed.
- `user.*`: User information fields if enabled.
- `http.request.headers.x_opaque_id`: The X-Opaque-Id header value if enabled. See [X-Opaque-Id HTTP header](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#x-opaque-id) for details and best practices.
- `trace.id`: [Trace ID](ecs://reference/ecs-tracing.md#field-trace-id) information, if provided by the client.
- `elasticsearch.task.id`: The task ID of the request.
- `elasticsearch.node.id`: The node ID of the request.
- `elasticsearch.parent.task.id`: The task ID of the parent task, if this request is a child of another request.
- `elasticsearch.parent.node.id`: The node ID of the parent task, if this request is a child of another request.

Using parent task and node IDs, you can correlate the log entries of queries initiated by other queries.

### Query logging specific fields

These fields are specific to query logging and common for all query languages.

- `elasticsearch.querylog.type`: The type of operation (`dsl`, `esql`, `sql`, `eql`).
- `elasticsearch.querylog.took`: How long (in nanoseconds) the request took to complete (this is the same as `event.duration`, for convenience).
- `elasticsearch.querylog.took_millis`: How long (in milliseconds) the request took to complete.
- `elasticsearch.querylog.timed_out`: Boolean specifying whether the query timed out.
- `elasticsearch.querylog.query`: The query text (depending on the query language, could be string or JSON).
- `elasticsearch.querylog.indices`: Array containing the indices that were requested. These may not be fully resolved. May contain wildcards and index expressions, and it is not guaranteed these resolve to any specific index or exist at all. Not supported for `sql` queries.
- `elasticsearch.querylog.result_count`: The number of results actually returned in the response. 
- `elasticsearch.querylog.is_system`: If system index logging is enabled, indicates whether the request was performed only on system indices.
- `elasticsearch.querylog.has_aggregations`: For a `dsl` search result, this boolean flag specifies whether the result has a non-empty aggregations section. 
- `elasticsearch.querylog.shards.successful`, `elasticsearch.querylog.shards.skipped`, `elasticsearch.querylog.shards.failed`: How many shards were successful, skipped and failed during the query execution. 

#### Cross-cluster query fields

When the query is cross-cluster, the following fields are available:

- `elasticsearch.querylog.clusters.total` - Indicates the total number of clusters involved in the query execution. Note that this field does not include the local cluster if no indices from it were involved in the query.
- `elasticsearch.querylog.clusters.remote_count` - Indicates the number of remote clusters involved in the query execution. 
- `elasticsearch.querylog.clusters.successful` - Indicates the number of clusters involved where the query execution was successful.
- `elasticsearch.querylog.clusters.failed` - Indicates the number of clusters involved in which the query execution failed. Only set if there were any failed clusters.
- `elasticsearch.querylog.clusters.partial` - Indicates the number of clusters involved in which the query execution was partially successful. Only set if there were any partially successful clusters.
- `elasticsearch.querylog.clusters.remotes` - Enumerates other clusters or projects involved in the query execution.
- `elasticsearch.querylog.is_remote` - For `dsl` queries, indicates whether the query was initiated by another cluster.

Additional fields specific to {{es}} environment may be added. See below for the examples of full query log entries. 

In addition to the fields listed above, each query language may include fields specific to it, prefixed with `elasticsearch.querylog.`.

### Fields specific to Query DSL

- `dsl.total_count`: The “total hits” value, as reported by [the search response](/solutions/search/the-search-api.md). 
- `dsl.total_count_partial`: Set to `true` in case the total count does not reflect the full number of matches for some reason (like [`track_total_hits` limitation](/solutions/search/the-search-api.md#track-total-hits)). 

### Fields specific to {{esql}}

- `esql.profile.*.took`: {{esql}} query profiling metrics, in nanoseconds

## Example log entry

### Query DSL

```json
{
  "@timestamp": "2026-03-13T01:01:57.391Z",
  "log.level": "INFO",
  "auth.type": "REALM",
  "elasticsearch.querylog.indices": [
    "query_log_test_index"
  ],
  "elasticsearch.querylog.query": "{\"size\":10,\"query\":{\"match_all\":{\"boost\":1.0}}}",
  "elasticsearch.querylog.result_count": 3,
  "elasticsearch.querylog.dsl.total_count": 3,
  "elasticsearch.querylog.shards.successful": 1,
  "elasticsearch.querylog.took": 2465042,
  "elasticsearch.querylog.took_millis": 2,
  "elasticsearch.querylog.type": "dsl",
  "elasticsearch.task.id": 4839,
  "event.duration": 2465042,
  "event.outcome": "success",
  "http.request.headers.x_opaque_id": "opaque-1773363717",
  "trace.id": "0af7651916cd43dd8448eb211c80319c",
  "user.name": "elastic",
  "user.realm": "reserved",
  "ecs.version": "1.2.0",
  "service.name": "ES_ECS",
  "event.dataset": "elasticsearch.querylog",
  "process.thread.name": "elasticsearch[node-1][search][T#6]",
  "log.logger": "elasticsearch.querylog",
  "elasticsearch.cluster.uuid": "gjYgb-uQQAuLmDoKlQInZw",
  "elasticsearch.node.id": "juurGSfgRYGwTP2ttZbtOQ",
  "elasticsearch.node.name": "node-1",
  "elasticsearch.cluster.name": "querying"
}
```

### Cross-cluster query
```json
{
  "@timestamp": "2026-03-23T16:59:53.538Z",
  "log.level": "INFO",
  "auth.type": "REALM",
  "elasticsearch.querylog.clusters.remote_count": 2,
  "elasticsearch.querylog.clusters.remotes": [
    "remote2",
    "remote1"
  ],
  "elasticsearch.querylog.clusters.successful": 3,
  "elasticsearch.querylog.clusters.total": 3,
  "elasticsearch.querylog.esql.profile.analysis.took": 1121750,
  "elasticsearch.querylog.esql.profile.dependency_resolution.took": 5040750,
  "elasticsearch.querylog.esql.profile.parsing.took": 989417,
  "elasticsearch.querylog.esql.profile.planning.took": 8038459,
  "elasticsearch.querylog.esql.profile.preanalysis.took": 30417,
  "elasticsearch.querylog.esql.profile.query.took": 40847750,
  "elasticsearch.querylog.indices": [
    "query_log_test_index",
    "remote2:query_log_test_index",
    "remote1:query_log_test_index"
  ],
  "elasticsearch.querylog.query": "FROM query_log_test_index,*:query_log_test_index | LIMIT 11",
  "elasticsearch.querylog.result_count": 5,
  "elasticsearch.querylog.shards.successful": 3,
  "elasticsearch.querylog.took": 40847750,
  "elasticsearch.querylog.took_millis": 40,
  "elasticsearch.querylog.type": "esql",
  "elasticsearch.task.id": 7215,
  "event.duration": 40847750,
  "event.outcome": "success",
  "http.request.headers.x_opaque_id": "opaque-1774285192",
  "trace.id": "0af7651916cd43dd8448eb211c80319c",
  "user.name": "elastic",
  "user.realm": "reserved",
  "ecs.version": "1.2.0",
  "service.name": "ES_ECS",
  "event.dataset": "elasticsearch.querylog",
  "process.thread.name": "elasticsearch[node-1][esql_worker][T#11]",
  "log.logger": "elasticsearch.querylog",
  "elasticsearch.cluster.uuid": "gjYgb-uQQAuLmDoKlQInZw",
  "elasticsearch.node.id": "juurGSfgRYGwTP2ttZbtOQ",
  "elasticsearch.node.name": "node-1",
  "elasticsearch.cluster.name": "querying"
}

```

### Example query failure
```json
{
  "@timestamp": "2026-03-04T19:40:35.271Z",
  "log.level": "INFO",
  "auth.type": "REALM",
  "elasticsearch.querylog.indices": [
    "nonexistent_index_xyz"
  ],
  "elasticsearch.querylog.query": "any where true",
  "elasticsearch.querylog.result_count": 0,
  "elasticsearch.querylog.took": 1326334,
  "elasticsearch.querylog.took_millis": 1,
  "elasticsearch.querylog.type": "eql",
  "error.message": "no such index [Unknown index [nonexistent_index_xyz]]",
  "error.type": "org.elasticsearch.index.IndexNotFoundException",
  "event.duration": 1326334,
  "event.outcome": "failure",
  "http.request.headers.x_opaque_id": "opaque-1772653234",
  "user.name": "elastic",
  "user.realm": "reserved",
  "ecs.version": "1.2.0",
  "service.name": "ES_ECS",
  "event.dataset": "elasticsearch.querylog",
  "process.thread.name": "elasticsearch[node-1][search_coordination][T#6]",
  "log.logger": "elasticsearch.querylog",
  "elasticsearch.cluster.uuid": "gjYgb-uQQAuLmDoKlQInZw",
  "elasticsearch.node.id": "juurGSfgRYGwTP2ttZbtOQ",
  "elasticsearch.node.name": "node-1",
  "elasticsearch.cluster.name": "querying"
}
```

## When and how to use query logging

While query logging is designed to have as little impact on the performance of your cluster as possible, it will necessarily consume resources needed to create and store the logs. Thus, it is advised to enable query logging only when necessary for troubleshooting or monitoring purposes, and to disable it after the investigation is complete. It is also recommended to set the threshold to avoid logging very quick queries that are of little consequence for the cluster performance. 

Query logging uses an asynchronous logging mechanism that does not block query execution. As a result, if there are too many incoming queries and the logging system can not store all the logs fast enough, some log entries may be lost. If that is a problem, consider increasing the thresholds to only log the most impactful queries. 

### Migrating from other logging solutions

Query logging provides functionality that supersedes the functionality of [slow logs](/deploy-manage/monitor/logging-configuration/slow-logs.md) and [ESQL query logging](elasticsearch://reference/query-languages/esql/esql-query-log.md). Thus, we recommend migrating from using those features to query logging, which provides more comprehensive and robust logging. Migrating to query logging is as simple as [enabling query logging](#configure-query-logging), setting the thresholds (for slow logs), and disabling the old logging, and then switching to use [the new logs](#finding-query-logs). The format of the logs is still JSON, though there may be slight differences in the field names - refer to the documentation and examples above for details. The following differences exist between the old logging features and the new query logging:
- Only query operations are presently supported, and not indexing operations, unlike slow logs.
- There is no option to enable logging per-index.  
- Only one threshold level is supported, there is no multi-level logging depending on multiple thresholds.


## Learn more [_learn_more]

To learn about other ways to optimize your search requests, refer to [tune for search speed](/deploy-manage/production-guidance/optimize-performance/search-speed.md).