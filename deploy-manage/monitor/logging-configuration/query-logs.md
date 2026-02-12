---
applies_to:
  deployment:
    self: ga 9.4
---

# Full query logging [logging]

{{es}} allows to log every search and query operation performed on the cluster. This supports endpoints like `_search`, `_msearch`, [{{esql}}](/explore-analyze/discover/try-esql.md), [SQL](elasticsearch://reference/query-languages/sql/sql-rest-format.md#_csv), [EQL](elasticsearch://reference/query-languages/eql/eql-syntax.md) and other APIs that search or query {{es}} indices.

The following logging modules are available:

- `search`: Logs every search operation performed on the cluster.
- `esql`: Logs every query operation performed on the cluster using {{esql}}.
- `eql`: Logs every query operation performed on the cluster using EQL.
- `sql`: Logs every query operation performed on the cluster using SQL.

By default, the logging is disabled. To enable the logging, set the `elasticsearch.activitylog.<MODULE>.enabled` property to `true` in the `elasticsearch.yml` configuration file or using the settings API, for example:

```yaml
elasticsearch.activitylog.search.enabled: true
```

By default, search queries that query only system indices are not logged. To enable logging of such queries, use the `elasticsearch.activitylog.search.include.system_indices` setting described below.

## Configuring query logging

The following configuration options are available:

- `elasticsearch.activitylog.<MODULE>.enabled`: Enables or disables logging for the specified module.
- `elasticsearch.activitylog.<MODULE>.threshold`: Sets the request duration threshold for logging events in the specified module. If the threshold is set to the value greater than 0, only the requests that take as much time or longer than the threshold are logged.
- `elasticsearch.activitylog.<MODULE>.include.user`: Enables or disables the user information logging for the specified module.

Additionally, for the search module:

- `elasticsearch.activitylog.search.include.system_indices`: Enables or disables logging of system indices for the search module.

## What is included in the log

The logs are output in JSON format, and include the following fields:

- `@timestamp`: The timestamp of the log entry.
- `log.level`: The log level (e.g., `WARN`, `INFO`, `DEBUG`, `TRACE`).
- `event.outcome`: Whether the request was successful (`success`) or not (`failure`).
- `event.duration`: How long (in nanoseconds) the request took to complete.
- `error.type` and `error.message`: Error information fields if the request failed.
- `user.*`: User information fields if enabled.
- `http.request.headers.x_opaque_id`: The X-Opaque-ID header value if enabled. See [X-Opaque-Id HTTP header](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#x-opaque-id) for details and best practices.
- `elasticsearch.activitylog.type`: The type of operation (`search`, `esql`, etc.).
- `elasticsearch.activitylog.took`: How long (in nanoseconds) the request took to complete.
- `elasticsearch.activitylog.took_millis`: How long (in milliseconds) the request took to complete.
- Additional fields specific to {{es}} environment may be added, for example:
    - `elasticsearch.activitylog.query`: The query source (depends on the module).

In addition to the fields listed above, each module may include fields specific to the module, prefixed with `elasticsearch.activitylog.`

### Search

- `indices`: The indices that were searched in the request, as comma-separated values.
- `hits`: The number of hits returned by the request. There is a maximum of 10000 hits returned per request, and this value will also be capped by this limit.
- `is_system`: If system index logging is enabled, indicates whether the request was performed only on a system indices.

### EQL

- `indices`: The indices that were queried in the request,
- `hits`: The number of hits returned by the request. There is a maximum of 10000 hits returned per request, and this value will also be capped by this limit.

### SQL

- `rows`: The number of rows returned by the request.

Example log entry:

```js
{
	"@timestamp": "2026-02-06T20:22:41.345Z",
	"log.level": "INFO",
	"auth.type": "REALM",
	"elasticsearch.activitylog.hits": 3,
	"elasticsearch.activitylog.indices": "my-index",
	"elasticsearch.activitylog.query": "{\"size\":1,\"fields\":[{\"field\":\"id\"},{\"field\":\"title\"},{\"field\":\"_tier\"}]}",
	"elasticsearch.activitylog.took": 1000000,
	"elasticsearch.activitylog.took_millis": 1,
	"elasticsearch.activitylog.type": "search",
	"event.duration": 1000000,
	"event.outcome": "success",
	"user.name": "elastic",
	"user.realm": "reserved",
	"ecs.version": "1.2.0",
	"service.name": "ES_ECS",
	"event.dataset": "elasticsearch.search_log",
	"process.thread.name": "elasticsearch[node-1][search][T#8]",
	"log.logger": "search.activitylog",
	"elasticsearch.cluster.uuid": "gjYgb-uQQAuLmDoKlQInZw",
	"elasticsearch.node.id": "juurGSfgRYGwTP2ttZbtOQ",
	"elasticsearch.node.name": "node-1",
	"elasticsearch.cluster.name": "querying"
}
```

Example failure entry:
```js
{
	"@timestamp": "2026-02-12T20:57:55.058Z",
	"log.level": "INFO",
	"auth.type": "REALM",
	"elasticsearch.activitylog.query": "\nfrom my-missing\n",
	"elasticsearch.activitylog.took": 1757709,
	"elasticsearch.activitylog.took_millis": 1,
	"elasticsearch.activitylog.type": "esql",
	"error.message": "Unknown index [my-missing]",
	"error.type": "org.elasticsearch.xpack.esql.VerificationException",
	"event.duration": 1757709,
	"event.outcome": "failure",
	"user.name": "elastic",
	"user.realm": "reserved",
	"ecs.version": "1.2.0",
	"service.name": "ES_ECS",
	"event.dataset": "elasticsearch.esql_log",
	"process.thread.name": "elasticsearch[node-1][search_coordination][T#4]",
	"log.logger": "esql.activitylog",
	"elasticsearch.cluster.uuid": "gjYgb-uQQAuLmDoKlQInZw",
	"elasticsearch.node.id": "juurGSfgRYGwTP2ttZbtOQ",
	"elasticsearch.node.name": "node-1",
	"elasticsearch.cluster.name": "querying"
}
```

## Finding the logs [finding-query-logs]

The logs are always emitted on the node that executed the request. These logs can be viewed in the following locations:

* If [{{es}} monitoring](/deploy-manage/monitor/stack-monitoring.md) is enabled, from [Stack Monitoring](/deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md). The query logs have the `logger` value of `<MODULE>.activitylog`(e.g. `search.activitylog`).
* From the local {{es}} service logs directory. Slow log files have a suffix of `_<MODULE>_log.json` , e.g. `mycluster_search_log.json`.

## When and how to use query logging

While query logging is designed to have as little impact on the performance of your cluster as possible, it will necessarily consume resources needed to create and store the logs. Thus, it is advised to enable query logging only when necessary for troubleshooting or monitoring purposes, and to disable it after the investigation is complete. It is also recommended to set the threshold to avoid logging very fast queries that are of little consequence for cluster performance. 

Query logging uses an asynchronous logging mechanism that does not block query execution. As a result, if there are too many incoming queries and the logging system can log store all the logs, some log entries may be lost. If that is a problem, consider increasing the thresholds to only log the most impactful queries. 

## Learn more [_learn_more]

To learn about other ways to optimize your search requests, refer to [tune for search speed](/deploy-manage/production-guidance/optimize-performance/search-speed.md).