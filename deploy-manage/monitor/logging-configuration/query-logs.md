---
applies_to:
  deployment:
    self: 9.4+
---

# Full query logging

{{es}} allows to log every search and query operation performed on the cluster. This supports endpoints like `_search`,
`_msearch`, [{{esql}}](/explore-analyze/discover/try-esql.md), [SQL](elasticsearch://reference/query-languages/sql/sql-rest-format.md#_csv), [EQL](elasticsearch://reference/query-languages/eql/eql-syntax.md)
and other APIs that search or query {{es}} indices.

The following logging modules are available:

- `search`: Logs every search operation performed on the cluster.
- `esql`: Logs every query operation performed on the cluster using {{esql}}.
- `eql`: Logs every query operation performed on the cluster using EQL.
- `sql`: Logs every query operation performed on the cluster using SQL.

By default, the logging is disabled. To enable the logging, set the `elasticsearch.actionlog.<MODULE>.enabled` property
to `true` in the `elasticsearch.yml` configuration file or via the settings API, for example:

```yaml
elasticsearch.actionlog.search.enabled: true
```

By default, search queries that query only system indices are not logged. To enable logging of such queries, use the
`elasticsearch.actionlog.search.include.system_indices` setting described below.

## Configuring query logging

The following configuration options are available:

- `elasticsearch.actionlog.<MODULE>.enabled`: Enables or disables logging for the specified module.
- `elasticsearch.actionlog.<MODULE>.threshold`: Sets the request duration threshold for logging events in the specified
  module. If the threshold is set to the value greater than 0, only the requests that take as much time or longer than
  the threshold are logged.
- `elasticsearch.actionlog.<MODULE>.log_level`: Sets the log level for the specified module.
- `elasticsearch.actionlog.<MODULE>.include.user`: Enables or disables user information logging for the specified
  module.

Additionally, for the search module:

- `elasticsearch.actionlog.search.include.system_indices`: Enables or disables logging of system indices for the search
  module.

## What is included in the log

The logs are output in JSON format, and include the following fields:

- `@timestamp`: The timestamp of the log entry.
- `log.level`: The log level (e.g., WARN, INFO, DEBUG, TRACE).
- `success`: Whether the request was successful (`true`) or not (`false`).
- `error.type` and `error.message`: Error information fields if the request failed.
- `took` and `took_ms`: The duration of the request, in nanoseconds and milliseconds.
- `user.*`: User information fields if enabled.
- `x_opaque_id`: The X-Opaque-ID header value if enabled.
  See [X-Opaque-Id HTTP header](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#x-opaque-id) for
  details and best practices.
- `type`: The type of operation (search, esql, etc.).
- `query`: The query source (depends on the module).
- Additional fields specific to {{es}} environment may be added.

In addition to the fields listed above, each module may include fields specific to the module:

### Search

- `indices`: The indices that were searched in the request, as comma-separated values.
- `hits`: The number of hits returned by the request. Note that there is a maximum of 10000 hits returned per request,
  and this value will also be capped by this limit.
- `is_system`: If system index logging is enabled, indicates whether the request was performed only on a system indices.

### EQL

- `indices`: The indices that were queried in the request,
- `hits`: The number of hits returned by the request. Note that there is a maximum of 10000 hits returned per request,
  and this value will also be capped by this limit.

### SQL

- `rows`: The number of rows returned by the request.

Example log entry:

```js
{
    "@timestamp"
:
    "2026-01-14T21:34:37.988Z",
        "log.level"
:
    "INFO",
        "auth.type"
:
    "REALM",
        "hits"
:
    4,
        "indices"
:
    "my-index-2,my-index",
        "query"
:
    "{\"size\":1,\"fields\":[{\"field\":\"id\"},{\"field\":\"title\"},{\"field\":\"_tier\"}]}",
        "success"
:
    "true",
        "took"
:
    5000000,
        "took_millis"
:
    5,
        "type"
:
    "search",
        "user.name"
:
    "elastic",
        "user.realm"
:
    "reserved",
        "x_opaque_id"
:
    null,
        "ecs.version"
:
    "1.2.0",
        "service.name"
:
    "ES_ECS",
        "event.dataset"
:
    "elasticsearch.search_actionlog",
        "process.thread.name"
:
    "elasticsearch[node-1][transport_worker][T#8]",
        "log.logger"
:
    "search.actionlog",
        "trace.id"
:
    "408bc58c794ae797d6a02a9b62ed1564",
        "elasticsearch.cluster.uuid"
:
    "gjYgb-uQQAuLmDoKlQInZw",
        "elasticsearch.node.id"
:
    "juurGSfgRYGwTP2ttZbtOQ",
        "elasticsearch.node.name"
:
    "node-1",
        "elasticsearch.cluster.name"
:
    "querying"
}
```

## Finding the logs [finding-query-logs]

The logs are always emitted on the node that executed the request. These logs can be viewed in the following locations:

* If [{{es}} monitoring](/deploy-manage/monitor/stack-monitoring.md) is enabled,
  from [Stack Monitoring](/deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md). The query logs have
  the `logger` value of `<MODULE>.actionlog`(e.g. `search.actionlog`).
* From the local {{es}} service logs directory. Slow log files have a suffix of `_<MODULE>_log.json` , e.g.
  `_search_log.json`.

## When and how to use query logging

TODO

## Learn more [_learn_more]

To learn about other ways to optimize your search requests, refer
to [tune for search speed](/deploy-manage/production-guidance/optimize-performance/search-speed.md).