---
description: Log every search operation on an Elasticsearch cluster including Query DSL, ES|QL, EQL, and SQL query types, with configurable duration thresholds and per-field output control.
applies_to:
  deployment:
    self: ga 9.4
    serverless: unavailable
---

# Query logging [logging]

{{es}} can log every querying operation performed on the cluster. This supports [DSL searches](/explore-analyze/query-filter/languages/querydsl.md), [{{esql}}](/explore-analyze/discover/try-esql.md), [SQL](elasticsearch://reference/query-languages/sql/sql-rest-format.md#_csv), [EQL](elasticsearch://reference/query-languages/eql/eql-syntax.md) and other APIs that search or query {{es}} indices.

## Supported query types

The following query types are supported:

- `dsl`: Logs every search operation performed on using the [Query DSL](/explore-analyze/query-filter/languages/querydsl.md).
- `esql`: Logs every query operation performed on the cluster using [{{esql}}](elasticsearch://reference/query-languages/esql.md).
- `eql`: Logs every query operation performed on the cluster using [EQL](/explore-analyze/query-filter/languages/eql.md).
- `sql`: Logs every query operation performed on the cluster using [SQL](/explore-analyze/query-filter/languages/sql.md).

## Enable query logging

By default, query logging is turned off. To enable logging, set the `elasticsearch.activitylog.enabled` property to `true` in the `elasticsearch.yml` configuration file.

Alternatively, use the [settings API]({{es-apis}}operation/operation-cluster-put-settings):

```yaml
elasticsearch.activitylog.enabled: true
```

`dsl` type queries that query only system indices are not logged by default. To enable logging these queries, use the `elasticsearch.activitylog.search.include.system_indices` setting described in [the configuration section](#configure-query-logging).

## Finding the logs [finding-query-logs]

Query logs are always emitted on the node that executed the request. These logs can be viewed in the following locations:

- If [{{es}} monitoring](/deploy-manage/monitor/stack-monitoring.md) is enabled, from [Stack Monitoring](/deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md). The query logs have the `log.logger` field set to `elasticsearch.querylog`.
- From the local {{es}} service logs directory. Query log files have a suffix of `_querylog.json`. For example: `mycluster_querylog.json`.

## Configure query logging  [configure-query-logging]

The following configuration options are available:

- `elasticsearch.activitylog.enabled`: Enables or disables query logging. Set to `true` to enable. Defaults to `false`.
- `elasticsearch.activitylog.threshold`: Sets the request duration threshold (in milliseconds) for logging events. If greater than 0, only requests with durations equal to or greater than the threshold are logged. The default is 0.
- `elasticsearch.activitylog.include.user`: Enables or disables logging of user information. Set to `false` to disable. Defaults to `true`.
- `elasticsearch.activitylog.search.include.system_indices`: Controls whether `dsl` queries targeting system indices are included in the logs. Set to `true` to include them. Defaults to `false`.

## What is included in the log

Each query log entry is a JSON object with fields from two sources:

- Standard [Elastic Common Schema (ECS)](ecs://reference/index.md) fields present in every entry.
- Query-specific fields under the `elasticsearch.querylog.*` namespace with details about the operation.

### Standard fields

These fields are present regardless of query type. Note that some fields may be present only in specific circumstances, see field descriptions below.

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

Using the parent task and node IDs, it is possible to correlate the log entries for queries that were initiated by other queries. 

### Query logging specific fields

These fields are specific to query logging and common for all query languages.

- `elasticsearch.querylog.type`: The type of operation (`dsl`, `esql`, `sql`, `eql`).
- `elasticsearch.querylog.took`: How long (in nanoseconds) the request took to complete.
- `elasticsearch.querylog.took_millis`: How long (in milliseconds) the request took to complete.
- `elasticsearch.querylog.timed_out`: Boolean specifying whether the query timed out.
- `elasticsearch.querylog.query`: The query text (depending on the query language, could be string or JSON).
- `elasticsearch.querylog.indices`: Array containing the indices that were requested. These may not be fully resolved. May contain wildcards and index expressions, and it is not guaranteed these resolve to any specific index or exist at all. Not supported for `sql` queries.
- `elasticsearch.querylog.result_count`: The number of results actually returned in the response. 
- `elasticsearch.querylog.is_system`: If system index logging is enabled, indicates whether the request was performed only on system indices.
- `elasticsearch.querylog.has_aggregations`: For a `dsl` search result, this boolean flag specifies whether the result has a non-empty aggregations section. 
- `elasticsearch.querylog.shards.successful`, `elasticsearch.querylog.shards.skipped`, `elasticsearch.querylog.shards.failed`: How many shards were successful, skipped and failed during the query execution. 
- `elasticsearch.querylog.remote_count` - For cross-cluster queries, this field indicates the number of remote clusters involved in the query execution. 
- `elasticsearch.querylog.remotes` - For cross-cluster queries, this field enumerates other clusters involved in the query execution.
- `elasticsearch.querylog.is_remote` - For `dsl` queries, indicates whether the query was initiated by a remote cluster.

Additional fields specific to {{es}} environment may be added. 

In addition to the fields listed above, each query language may include fields specific to it, prefixed with `elasticsearch.querylog.`.

### Fields specific to Query DSL (`dsl`)

- `search.total_count`: The “total hits” value, as reported by [the search response](/solutions/search/the-search-api.md). 
- `search.total_count_partial`:  Set to `true` in case the total count does not reflect the full number of matches for some reason (like [`track_total_hits` limitation](/solutions/search/the-search-api.md#track-total-hits)). 

### Fields specific to {{esql}}

- `esql.profile.*.took`: {{esql}} query profiling metrics, in nanoseconds

## Example log entry

Query DSL:

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
  "elasticsearch.querylog.search.total_count": 3,
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

Cross-cluster query:
```json
{
  "@timestamp": "2026-03-13T01:01:58.266Z",
  "log.level": "INFO",
  "auth.type": "REALM",
  "elasticsearch.querylog.clusters.successful": 2,
  "elasticsearch.querylog.clusters.total": 2,
  "elasticsearch.querylog.esql.profile.analysis.took": 388084,
  "elasticsearch.querylog.esql.profile.dependency_resolution.took": 3376250,
  "elasticsearch.querylog.esql.profile.parsing.took": 466125,
  "elasticsearch.querylog.esql.profile.planning.took": 4836167,
  "elasticsearch.querylog.esql.profile.preanalysis.took": 20334,
  "elasticsearch.querylog.esql.profile.query.took": 16403208,
  "elasticsearch.querylog.indices": [
    "remote2:query_log_test_index",
    "remote1:query_log_test_index"
  ],
  "elasticsearch.querylog.query": "FROM *:query_log_test_index | LIMIT 10",
  "elasticsearch.querylog.remote_count": 2,
  "elasticsearch.querylog.remotes": [
    "remote2",
    "remote1"
  ],
  "elasticsearch.querylog.result_count": 2,
  "elasticsearch.querylog.shards.successful": 2,
  "elasticsearch.querylog.took": 16403208,
  "elasticsearch.querylog.took_millis": 16,
  "elasticsearch.querylog.type": "esql",
  "elasticsearch.task.id": 4923,
  "event.duration": 16403208,
  "event.outcome": "success",
  "http.request.headers.x_opaque_id": "opaque-1773363717",
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

Example query failure:
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

## Learn more [_learn_more]

To learn about other ways to optimize your search requests, refer to [tune for search speed](/deploy-manage/production-guidance/optimize-performance/search-speed.md).