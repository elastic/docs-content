---

applies_to:
  deployment:
self: ga 9.4

---

# Full query logging [logging]

{{es}} allows to log every querying operation performed on the cluster. This supports endpoints like `_search`, `_msearch`, [{{esql}}](/explore-analyze/discover/try-esql.md), [SQL](elasticsearch://reference/query-languages/sql/sql-rest-format.md#_csv), [EQL](elasticsearch://reference/query-languages/eql/eql-syntax.md) and other APIs that search or query {{es}} indices.

The following query types are supported:

- `dsl`: Logs every search operation performed on the cluster.
- `esql`: Logs every query operation performed on the cluster using {{esql}}.
- `eql`: Logs every query operation performed on the cluster using EQL.
- `sql`: Logs every query operation performed on the cluster using SQL.

By default, the logging is turned off. To enable the logging, set the `elasticsearch.actionlog.enabled` property to `true` in the `elasticsearch.yml` configuration file or using the [settings API]({{es-apis}}operation/operation-cluster-put-settings):

```yaml
elasticsearch.actionlog.enabled: true
```

By default, search (`dsl`) queries that query only system indices are not logged. To enable logging of such queries, use the `elasticsearch.actionlog.search.include.system_indices` setting described below.

## Configuring query logging

The following configuration options are available:

- `elasticsearch.activitylog.enabled`: Enables or disables query logging.
- `elasticsearch.activitylog.threshold`: Sets the request duration threshold for logging events. If the threshold is set to the value greater than 0, only the requests that take as much time or longer than the threshold are logged.
- `elasticsearch.activitylog.include.user`: Enables or disables the user information logging.
- `elasticsearch.activitylog.search.include.system_indices`: Enables or disables logging of system indices for the DSL search module.

## What is included in the log

The logs are output in JSON format, and include the following fields:

- `@timestamp`: The timestamp of the log entry.
- `event.outcome`: Whether the request was successful (`success`) or not (`failure`).
- `event.duration`: How long (in nanoseconds) the request took to complete.
- `error.type` and `error.message`: Error information fields if the request failed.
- `user.*`: User information fields if enabled.
- `http.request.headers.x_opaque_id`: The X-Opaque-Id header value if enabled. See [X-Opaque-Id HTTP header](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#x-opaque-id) for details and best practices.
- `trace.id`: [Trace ID](ecs://ecs/ecs-tracing#field-trace-id) information.

### Query logging specific fields

- `elasticsearch.querylog.type`: The type of operation (`dsl`, `esql`, and so on).
- `elasticsearch.querylog.took`: How long (in nanoseconds) the request took to complete.
- `elasticsearch.querylog.took_millis`: How long (in milliseconds) the request took to complete.
- `elasticsearch.querylog.timed_out`: Boolean specifying whether the query timed out.
- `elasticsearch.querylog.query`: The query text (depending on the query language, could be string or JSON).
- `elasticsearch.querylog.indices`: Array containing the indices that were requested. These may not be fully resolved. May contain wildcards and index expressions, and it is not guaranteed these resolve to any specific index or exist at all. Note that for some queries (like {{esql}}) indices are part of the query text and will not be available as separate field. 
- `elasticsearch.querylog.result_count`: The number of results actually returned by the request. There is a maximum of 10000 hits returned per DSL request, and there may be other caps on the returned result size. 
- `elasticsearch.querylog.is_system`: If system index logging is enabled, indicates whether the request was performed only on a system indices.
- `elasticsearch.querylog.has_aggregations`: For a search result, this boolean flag specifies whether the result has a non-empty aggregations section. 
- `elasticsearch.querylog.shards.successful`, `elasticsearch.querylog.shards.skipped`, `elasticsearch.querylog.shards.failed`: How many shards were successful, skipped and failed during the query execution. 

Additional fields specific to {{es}} environment may be added. 

In addition to the fields listed above, each query language may include fields specific to it, prefixed with `elasticsearch.querylog.`

### DSL Search specific fields

- `search.total_count`: The “total hits” value, as reported by [the search response](/solutions/search/the-search-api). 
- `search.total_count_partial`:  Set to `true` in case the total count does not reflect the full amount of matches for some reason (like `track_total_hits` limitation). 

### {{esql}}

- `esql.profile.*.took`: ESQL query profiling metrics, in ns

### Example log entry

```js
{
  "@timestamp": "2026-03-04T19:40:34.736Z",
  "log.level": "INFO",
  "auth.type": "REALM",
  "elasticsearch.querylog.indices": [
    "query_log_test_index"
  ],
  "elasticsearch.querylog.query": "{\"size\":10,\"query\":{\"match_all\":{\"boost\":1.0}}}",
  "elasticsearch.querylog.result_count": 3,
  "elasticsearch.querylog.search.total_count": 3,
  "elasticsearch.querylog.shards.successful": 1,
  "elasticsearch.querylog.took": 1000000,
  "elasticsearch.querylog.took_millis": 1,
  "elasticsearch.querylog.type": "dsl",
  "event.duration": 1000000,
  "event.outcome": "success",
  "http.request.headers.x_opaque_id": "opaque-1772653234",
  "user.name": "elastic",
  "user.realm": "reserved",
  "ecs.version": "1.2.0",
  "service.name": "ES_ECS",
  "event.dataset": "elasticsearch.querylog",
  "process.thread.name": "elasticsearch[node-1][search][T#3]",
  "log.logger": "elasticsearch.querylog",
  "elasticsearch.cluster.uuid": "gjYgb-uQQAuLmDoKlQInZw",
  "elasticsearch.node.id": "juurGSfgRYGwTP2ttZbtOQ",
  "elasticsearch.node.name": "node-1",
  "elasticsearch.cluster.name": "querying"
}
```

Example failure entry:

```js
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

## Finding the logs [finding-query-logs]

The logs are always emitted on the node that executed the request. These logs can be viewed in the following locations:

- If [{{es}} monitoring](/deploy-manage/monitor/stack-monitoring.md) is enabled, from [Stack Monitoring](/deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md). The query logs have the `logger` value of elasticsearch.querylog`.
- From the local {{es}} service logs directory. Slow log files have a suffix of `_querylog.json` , e.g. `mycluster_querylog.json`.

## When and how to use query logging

While query logging is designed to have as little impact on the performance of your cluster as possible, it will necessarily consume resources needed to create and store the logs. Thus, it is advised to enable query logging only when necessary for troubleshooting or monitoring purposes, and to disable it after the investigation is complete. It is also recommended to set the threshold to avoid logging very quick queries that are of little consequence for cluster performance. 

Query logging uses an asynchronous logging mechanism that does not block query execution. As a result, if there are too many incoming queries and the logging system can not store all the logs fast enough, some log entries may be lost. If that is a problem, consider increasing the thresholds to only log the most impactful queries. 

## Learn more [_learn_more]

To learn about other ways to optimize your search requests, refer to [tune for search speed](/deploy-manage/production-guidance/optimize-performance/search-speed.md).