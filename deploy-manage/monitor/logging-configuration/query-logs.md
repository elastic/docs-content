---
description: Log every search operation on an Elasticsearch cluster including Query DSL, ES|QL, EQL, and SQL query types, with configurable duration thresholds and per-field output control.
applies_to:
  stack: preview 9.4
  serverless: unavailable
products:
  - id: "elasticsearch"
  - id: "cloud-hosted"
  - id: "cloud-kubernetes"
  - id: "cloud-enterprise"
---

# Query logging in {{es}}

{{es}} can log every query operation performed on the cluster. 

The following query types are supported:

- `dsl`: [Query DSL](elasticsearch://reference/query-languages/querydsl.md) searches
- `esql`: [{{esql}}](elasticsearch://reference/query-languages/esql.md) queries
- `eql`: [EQL](elasticsearch://reference/query-languages/eql/eql-syntax.md) queries
- `sql`: [SQL](elasticsearch://reference/query-languages/sql.md) queries

## When to use query logging

Query logging helps you answer questions like:

- **Which queries are slow or expensive?** Use the duration and shard fields to find queries that take the longest or touch the most shards.
- **What does the query workload look like?** Analyze query types, frequency, and timing to understand traffic patterns across the cluster.
- **Why did a query fail or return unexpected results?** Inspect the full query text, error details, and targeted indices to debug issues.
- **Where is a query coming from?** Use the `X-Opaque-Id` header and trace ID fields to identify the originating application or request.
- **Who is running queries?** When user logging is enabled, trace queries back to specific users or API keys.

Query logging is designed to minimize performance impact, but it does consume resources to create and store log entries. Enable it when you need it, and disable it when the investigation is complete. Use the [threshold setting](#configure-query-logging) to filter out fast queries that are not relevant to your analysis.

Query logging uses an asynchronous mechanism that does not block query execution. If the volume of incoming queries exceeds the logging system's write capacity, some entries may be dropped. If that happens, raise the threshold to log only the most impactful queries.

### Migrate to query logging

Query logging supersedes [slow logs](/deploy-manage/monitor/logging-configuration/slow-logs.md) and [ES|QL query logging](elasticsearch://reference/query-languages/esql/esql-query-log.md). We recommend migrating to query logging for more comprehensive and robust logging.

To migrate:

1. [Enable query logging](#set-up-query-logging).
2. Set the [threshold](#configure-query-logging) to match your previous slow log or {{esql}} query log levels.
3. Disable the old logging.
4. Switch to the new query log output.

The log format remains JSON, but some field names differ. To compare field names, refer to the [field reference](#log-field-reference) and [examples](#example-query-log-entries).

Query logging differs from slow logs and ES|QL query logging in the following ways:

- Query logs capture the end-to-end request duration as measured by {{es}}, while slow logs only capture shard-level execution time.
- Only query operations are supported, not indexing operations.
- Per-index logging is not available.
- Only one threshold level is supported, not multiple threshold levels.

## Set up query logging

By default, query logging is turned off. The setup to enable, collect, and ship query logs depends on your deployment type. In all cases, query log entries are written on the [coordinating node](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#coordinating-only-node-role) for each request as `*_querylog.json` files in the {{es}} [log directory](/deploy-manage/monitor/logging-configuration.md).

:::{important}
If you ship query logs to a separate destination cluster, that cluster must run {{es}} 9.4 or later. Sending this stream to pre-9.4 {{es}} versions is not supported. Ingest can fail, or the cluster may only apply some of the index mappings and settings.
:::

### Configuration options [configure-query-logging]

The following configuration options are available. Set them in `elasticsearch.yml` or use the [cluster settings API]({{es-apis}}operation/operation-cluster-put-settings).

- `elasticsearch.querylog.enabled`: Enables or disables query logging. Set to `true` to enable. Defaults to `false`.
- `elasticsearch.querylog.threshold`: Sets the request duration threshold (in [time units](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#time-units), like `100ms` or `5s`) for logging events. If greater than 0, only requests with durations equal to or greater than the threshold are logged. The default is 0.
- `elasticsearch.querylog.include.user`: Enables or disables logging of user information. Set to `false` to disable. Defaults to `true`.
- `elasticsearch.querylog.include.system_indices`: Controls whether queries targeting only system indices are included in the logs. Set to `true` to include them. Defaults to `false`.

### Set up by deployment type

::::::{applies-switch}

% TODO: Update ECH and ECE tabs when Cloud UI supports configuring query logging settings directly.

:::::{applies-item} ess:

To set up query logging on {{ech}} deployments:

1. [Turn on Logs and metrics](/deploy-manage/monitor/stack-monitoring/ece-ech-stack-monitoring.md#enable-logging-and-monitoring-steps) for the deployment so it can ship logs to your monitoring or log destination cluster.
2. Enable query logging using the [cluster settings API]({{es-apis}}operation/operation-cluster-put-settings):

:::{include} /deploy-manage/monitor/logging-configuration/_snippets/enable-query-logging.md
:::

:::::

:::::{applies-item} eck:

ECK clusters automatically collect from the `*_querylog.json` path using the default configuration. Set `elasticsearch.querylog.enabled` to `true` in `elasticsearch.yml` or using the [cluster settings API]({{es-apis}}operation/operation-cluster-put-settings):

:::{include} /deploy-manage/monitor/logging-configuration/_snippets/enable-query-logging.md
:::

:::::

:::::{applies-item} { self:, ece: }

To set up query logging on self-managed or ECE clusters:

1. Set `elasticsearch.querylog.enabled` to `true` in `elasticsearch.yml` or using the [cluster settings API]({{es-apis}}operation/operation-cluster-put-settings):

    :::{include} /deploy-manage/monitor/logging-configuration/_snippets/enable-query-logging.md
    :::

2. Set up a shipper to collect and index the log files:

- **Filebeat**: The [Filebeat](https://www.elastic.co/docs/reference/beats/filebeat) [{{es}} module](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-module-elasticsearch) includes a `querylog` [fileset](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-module-elasticsearch#_querylog_log_fileset_settings) that reads the `*_querylog.json` files and sends events to the `logs-elasticsearch.querylog-default` data stream. Configure Filebeat on the nodes that emit query logs and enable the `querylog` fileset.
- **Elastic Agent**: The [`elasticsearch` Elastic Agent integration](https://www.elastic.co/docs/reference/integrations/elasticsearch) (1.21.0+) can also collect and ship the same file to the data stream. To enable collection, refer to the [query log settings](https://www.elastic.co/docs/reference/integrations/elasticsearch#querylog) in the integration.

:::{important}
**Index privileges for the user that Filebeat or Agent uses**

The `logs-elasticsearch.querylog-default` data stream is a separate destination from `filebeat-*` indices that often store [{{stack}} monitoring](/deploy-manage/monitor/stack-monitoring.md) metrics and logs. Grant the output user in {{es}} the index and ingest privileges the managed data stream needs for `logs-elasticsearch.querylog-*`, in addition to anything you allow for `filebeat-*` or other indices. The exact role name is your choice. The critical part is the extra privilege on the querylog data stream.
:::

:::::

::::::

### Managed data stream and index template

The managed index template, `logs-elasticsearch.querylog@template`, is used for the `logs-elasticsearch.querylog-*` data stream. The template provides mappings and data stream options to ensure shipped events land in a single, ECS-aligned destination you can use with {{kib}} and the Elastic Agent or {{beats}} assets that ship with the product.

The `logs-elasticsearch.querylog-*` data stream is initialized with the following configurations and default behaviors:

* **Index mode:** The data stream uses [LogsDB](/manage-data/data-store/data-streams/logs-data-stream.md) indexing.
* **Query volume:** When logging is enabled, the default `elasticsearch.querylog.threshold` is `0` in [time units](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#time-units), so every request can be eligible depending on other options. A busy cluster can produce a very large number of lines. [Raise the threshold](#configure-query-logging) if you need to cap volume.
* **Retention and failure handling:** A default [data stream lifecycle](/manage-data/lifecycle/data-stream.md) is attached with a 2 day retention window so the data stream does not grow without bound. The [failure store](/manage-data/data-store/data-streams/failure-store.md) is on, with a 7 day retention for failed ingest.
* **Management UI:** You can also manage the data stream lifecycle, routing, and related controls in the [Streams](/solutions/observability/streams/streams.md) app.

## View query logs in {{kib}}

Once the shipper starts ingesting into `logs-elasticsearch.querylog-*` on the destination cluster, you can explore the logs in {{kib}}.

The [`elasticsearch` Elastic Agent integration](https://www.elastic.co/docs/reference/integrations/elasticsearch) (1.21.0+) bundles the following {{kib}} assets, which you can install even if you do not use the Agent to ship the query logs:

* A data view, "Elasticsearch query logs," for `logs-elasticsearch.querylog-*`
* A dashboard, "Elasticsearch query analytics," for analyzing your historical queries

Install the assets from Fleet (or the integration's Assets tab) when you are ready to explore the indexed stream.

Alternatively, [create a data view](/explore-analyze/find-and-organize/data-views.md) for `logs-elasticsearch.querylog-*` and use **Discover** to filter on `event.dataset: elasticsearch.querylog`.

## Example query log entries

The following examples show the JSON structure of query log entries for different query types and scenarios.

### Query DSL

This example shows a standard search request using Query DSL. The log entry includes the JSON-escaped query body, execution duration in nanoseconds and milliseconds, and the security context of the user who initiated the request.

```json
{
  "@timestamp": "2026-03-13T01:01:57.391Z",
  "log.level": "INFO",
  "auth.type": "REALM",
  "elasticsearch.querylog.indices": [
    "query_log_test_index"
  ],
  "elasticsearch.querylog.query": "{\"size\":10,\"query\":{\"match_all\":{\"boost\":1.0}}}", <1>
  "elasticsearch.querylog.result_count": 3,
  "elasticsearch.querylog.dsl.total_count": 3,
  "elasticsearch.querylog.shards.successful": 1,
  "elasticsearch.querylog.took": 2465042,
  "elasticsearch.querylog.took_millis": 2, <2>
  "elasticsearch.querylog.type": "dsl", <3>
  "elasticsearch.task.id": 4839,
  "event.duration": 2465042,
  "event.outcome": "success", <4>
  "http.request.headers.x_opaque_id": "opaque-1773363717",
  "trace.id": "0af7651916cd43dd8448eb211c80319c",
  "user.name": "elastic", <5>
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
1. The full Query DSL body, JSON-escaped
2. Request duration in milliseconds
3. Query language identifier
4. Whether the request succeeded or failed
5. User information, included when `elasticsearch.querylog.include.user` is `true`

### Cross-cluster query

This example shows a query that targets indices on remote clusters. The entry includes additional fields for remote cluster counts, remote cluster names, and per-phase profiling metrics for the request execution.

```json
{
  "@timestamp": "2026-03-23T16:59:53.538Z",
  "log.level": "INFO",
  "auth.type": "REALM",
  "elasticsearch.querylog.clusters.remote_count": 2, <1>
  "elasticsearch.querylog.clusters.remotes": [
    "remote2",
    "remote1"
  ],
  "elasticsearch.querylog.clusters.successful": 3,
  "elasticsearch.querylog.clusters.total": 3,
  "elasticsearch.querylog.esql.profile.analysis.took": 1121750, <2>
  "elasticsearch.querylog.esql.profile.dependency_resolution.took": 5040750,
  "elasticsearch.querylog.esql.profile.parsing.took": 989417,
  "elasticsearch.querylog.esql.profile.planning.took": 8038459,
  "elasticsearch.querylog.esql.profile.preanalysis.took": 30417,
  "elasticsearch.querylog.esql.profile.query.took": 40847750,
  "elasticsearch.querylog.indices": [
    "query_log_test_index",
    "remote2:query_log_test_index", <3>
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
1. Number of remote clusters involved in the query
2. ES|QL profiling metrics, broken down by query phase, in nanoseconds
3. Remote indices are prefixed with the cluster name

### Example query failure

This example shows a log entry for a request that did not complete successfully. When a query fails, the log includes the `error.type` and `error.message` fields to provide the exception class and a description of the failure.

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
  "error.message": "no such index [Unknown index [nonexistent_index_xyz]]", <1>
  "error.type": "org.elasticsearch.index.IndexNotFoundException", <2>
  "event.duration": 1326334,
  "event.outcome": "failure", <3>
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
1. Human-readable error description
2. Java exception class for programmatic error handling
3. Set to `failure` when the request errors

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
- `http.request.headers.x_opaque_id`: The X-Opaque-Id header value if enabled. To learn more, refer to [X-Opaque-Id HTTP header](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#x-opaque-id).
- `trace.id`: [Trace ID](ecs://reference/ecs-tracing.md#field-trace-id) information, if provided by the client.
- `elasticsearch.task.id`: The task ID of the request.
- `elasticsearch.node.id`: The node ID of the request.
- `elasticsearch.parent.task.id`: The task ID of the parent task, if this request is a child of another request.
- `elasticsearch.parent.node.id`: The node ID of the parent task, if this request is a child of another request.

Using parent task and node IDs, you can correlate the log entries of queries initiated by other queries.

### Fields specific to query logging

These fields are specific to query logging and common for all query languages.

- `elasticsearch.querylog.type`: The type of operation (`dsl`, `esql`, `sql`, `eql`).
- `elasticsearch.querylog.took`: How long the request took to complete, in nanoseconds. This is the same value as `event.duration`.
- `elasticsearch.querylog.took_millis`: How long (in milliseconds) the request took to complete.
- `elasticsearch.querylog.timed_out`: Boolean specifying whether the query timed out.
- `elasticsearch.querylog.query`: The query text (depending on the query language, could be string or JSON).
- `elasticsearch.querylog.indices`: Array containing the indices that were requested. These may not be fully resolved. May contain wildcards and index expressions, and it is not guaranteed these resolve to any specific index or exist at all. Not supported for `sql` or `esql` queries.
- `elasticsearch.querylog.result_count`: The number of results actually returned in the response.
- `elasticsearch.querylog.is_system`: If system index logging is enabled, indicates whether the request was performed only on system indices.
- `elasticsearch.querylog.has_aggregations`: For a `dsl` search result, this boolean flag specifies whether the result has a non-empty aggregations section.
- `elasticsearch.querylog.shards.successful`, `elasticsearch.querylog.shards.skipped`, `elasticsearch.querylog.shards.failed`: How many shards were successful, skipped, and failed during the query execution.

#### Cross-cluster query fields

When the query is cross-cluster, the following fields are available:

- `elasticsearch.querylog.clusters.total`: Indicates the total number of clusters involved in the query execution. Note that this field does not include the local cluster if no indices from it were involved in the query.
- `elasticsearch.querylog.clusters.remote_count`: Indicates the number of remote clusters involved in the query execution. 
- `elasticsearch.querylog.clusters.successful`: Indicates the number of clusters involved where the query execution was successful.
- `elasticsearch.querylog.clusters.failed`: Indicates the number of clusters involved in which the query execution failed. Only set if there were any failed clusters.
- `elasticsearch.querylog.clusters.partial`: Indicates the number of clusters involved in which the query execution was partially successful. Only set if there were any partially successful clusters.
- `elasticsearch.querylog.clusters.remotes`: Enumerates other clusters or projects involved in the query execution.
- `elasticsearch.querylog.is_remote`: For `dsl` queries, indicates whether the query was initiated by another cluster.

Additional fields specific to the {{es}} environment may appear in log entries. To view complete examples, refer to [Example query log entries](#example-query-log-entries).

Each query language may also include its own fields, prefixed with `elasticsearch.querylog.`.

### Fields specific to Query DSL

- `elasticsearch.querylog.dsl.total_count`: The “total hits” value, as reported by [the search response](/solutions/search/the-search-api.md).
- `elasticsearch.querylog.dsl.total_count_partial`: Set to `true` when the total count does not reflect the full number of matches, for example due to the [`track_total_hits` limitation](/solutions/search/the-search-api.md#track-total-hits).

### Fields specific to {{esql}}

- `elasticsearch.querylog.esql.profile.*.took`: {{esql}} query profiling metrics, in nanoseconds


## Related pages 

- [Query activity](/deploy-manage/monitor/query-activity.md)
- [Tune for search speed](/deploy-manage/production-guidance/optimize-performance/search-speed.md)
