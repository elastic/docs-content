---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-slowlog.html
applies_to:
  stack: all
---

# Slow query and index logging

The slow log records search and indexing operations that exceed time thresholds you define.
You can use slow logs to investigate, analyze or audit heavy operations, or troubleshoot your cluster’s historical search and indexing performance.

Slow logs report task duration at the **shard level** for searches, and at the **index level** for indexing, but might not encompass the full task execution time observed on the client. For example, slow logs don’t surface HTTP network delays or the impact of [task queues](/troubleshoot/elasticsearch/task-queue-backlog.md). For more information about the higher-level operations affecting response times, refer to [Reading and writing documents](/deploy-manage/distributed-architecture/reading-and-writing-documents.md).

Slow log thresholds can be enabled for these logging levels (in order of increasing verbosity): 

* `WARN`
* `INFO`
* `DEBUG`
* `TRACE`

You can mimic setting log level thresholds by disabling more verbose levels.

Because logging every event or operation generates a high volume of log entries, slow logs are deactivated by default (all thresholds are set to `-1`). Activate only when needed and avoid setting low thresholds in production.

Refer to [slow log settings](elasticsearch://reference/elasticsearch/index-settings/slow-log.md) to learn more about configuration options you can adjust to capture search and indexing details.


## Finding slow logs [finding-slow-logs]

Events that meet the specified threshold are emitted into [{{es}} logging](/deploy-manage/monitor/logging-configuration/update-elasticsearch-logging-levels.md) under the `fileset.name` of `slowlog`. These logs can be viewed in the following locations:

* If [{{es}} monitoring](/deploy-manage/monitor/stack-monitoring.md) is enabled, from [Stack Monitoring](/deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md). Slow log events have a `logger` value of `index.search.slowlog` or `index.indexing.slowlog`.
* From the local {{es}} service logs directory. Slow log files have a suffix of `_index_search_slowlog.json` or `_index_indexing_slowlog.json`.

Refer to [this video](https://www.youtube.com/watch?v=ulUPJshB5bU) for a walkthrough of setting and reviewing slow logs.


## What's included in slow logs [slow-log-format]

Depending on the settings you configure, slow logs can record:
* the operation (searching or indexing)
* phase for searches (query or fetch)
* how long the operation took
* number of hits
* which shard or index is affected
* optional metadata (such as the `_source` request body or `user.*` fields)

::::{tip}
If a call was initiated with an `X-Opaque-ID` header, then the ID is automatically included in Search slow logs in the **elasticsearch.slowlog.id** field. See [X-Opaque-Id HTTP header](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#x-opaque-id) for details and best practices.
::::

The following are examples of a search and an indexing operation in the slow log respectively:

::::{tab-set}
:group: slow-logs
:::{tab-item} Search operations
:sync: search

```js
{
  "@timestamp": "2024-12-21T12:42:37.255Z",
  "auth.type": "REALM",
  "ecs.version": "1.2.0",
  "elasticsearch.cluster.name": "distribution_run",
  "elasticsearch.cluster.uuid": "Ui23kfF1SHKJwu_hI1iPPQ",
  "elasticsearch.node.id": "JK-jn-XpQ3OsDUsq5ZtfGg",
  "elasticsearch.node.name": "node-0",
  "elasticsearch.slowlog.id": "tomcat-123",
  "elasticsearch.slowlog.message": "[index6][0]",
  "elasticsearch.slowlog.search_type": "QUERY_THEN_FETCH",
  "elasticsearch.slowlog.source": "{\"query\":{\"match_all\":{\"boost\":1.0}}}",
  "elasticsearch.slowlog.stats": "[]",
  "elasticsearch.slowlog.took": "747.3micros",
  "elasticsearch.slowlog.took_millis": 0,
  "elasticsearch.slowlog.total_hits": "1 hits",
  "elasticsearch.slowlog.total_shards": 1,
  "event.dataset": "elasticsearch.index_search_slowlog",
  "fileset.name" : "slowlog",
  "log.level": "WARN",
  "log.logger": "index.search.slowlog.query",
  "process.thread.name": "elasticsearch[runTask-0][search][T#5]",
  "service.name": "ES_ECS",
  "user.name": "elastic",
  "user.realm": "reserved"
}
```
% NOTCONSOLE

:::

:::{tab-item} Indexing operations
:sync: index

```js
{
  "@timestamp" : "2024-12-11T22:34:22.613Z",
  "auth.type": "REALM",
  "ecs.version": "1.2.0",
  "elasticsearch.cluster.name" : "41bd111609d849fc9bf9d25b5df9ce96",
  "elasticsearch.cluster.uuid" : "BZTn4I9URXSK26imlia0QA",
  "elasticsearch.index.id" : "3VfGR7wRRRKmMCEn7Ii58g",
  "elasticsearch.index.name": "my-index-000001",
  "elasticsearch.node.id" : "GGiBgg21S3eqPDHzQiCMvQ",
  "elasticsearch.node.name" : "instance-0000000001",
  "elasticsearch.slowlog.id" : "RCHbt5MBT0oSsCOu54AJ",
  "elasticsearch.slowlog.source": "{\"key\":\"value\"}"
  "elasticsearch.slowlog.took" : "0.01ms",
  "event.dataset": "elasticsearch.index_indexing_slowlog",
  "fileset.name" : "slowlog",
  "log.level" : "TRACE",
  "log.logger" : "index.indexing.slowlog.index",
  "service.name" : "ES_ECS",
  "user.name": "elastic",
  "user.realm": "reserved"
}
```
% NOTCONSOLE

:::
::::


## Enabling slow logs [enable-slow-log]

You enable slow logs by configuring thresholds. Thresholds can be aggressive, such as `0ms` to log everything, or conservative, such as `5s`.

You can enable slow logging at the following levels:

* At the index level, using the [update indices settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) API.
* For all indices (cluster-wide) under the [{{es}} `log4j2.properties` configuration file](/deploy-manage/deploy/self-managed/configure-elasticsearch.md). This method requires a node restart.

To view the current slow log settings, use the [get index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) API:

```console
GET _all/_settings?expand_wildcards=all&filter_path=*.settings.index.*.slowlog
```

To enable slow logging for a single index, use the [update indices settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings):

::::{tab-set}
:group: slow-logs
:::{tab-item} Search operations
:sync: search
Search slow logs emit per shard. They must be enabled separately for the shard’s [query and fetch search phases](https://www.elastic.co/blog/understanding-query-then-fetch-vs-dfs-query-then-fetch).

```console
PUT /my-index-000001/_settings
{
  "index.search.slowlog.threshold.query.warn": "10s",
  "index.search.slowlog.threshold.query.info": "5s",
  "index.search.slowlog.threshold.query.debug": "2s",
  "index.search.slowlog.threshold.query.trace": "500ms",
  "index.search.slowlog.threshold.fetch.warn": "1s",
  "index.search.slowlog.threshold.fetch.info": "800ms",
  "index.search.slowlog.threshold.fetch.debug": "500ms",
  "index.search.slowlog.threshold.fetch.trace": "200ms",
  "index.search.slowlog.include.user": true <1>
}
```

1. You can use the `index.search.slowlog.include.user` setting for search operations or the `index.indexing.slowlog.include.user` setting for indexing operations to append `user.*` and `auth.type` fields to slow log entries. These fields contain information about the user who triggered the request.

For more information about slow log settings, refer to [slow log settings](elasticsearch://reference/elasticsearch/index-settings/slow-log.md).

:::

:::
:::{tab-item} Indexing operations
:sync: index

Indexing slow logs emit per index document.

```console
PUT /my-index-000001/_settings
{
  "index.indexing.slowlog.threshold.index.warn": "10s",
  "index.indexing.slowlog.threshold.index.info": "5s",
  "index.indexing.slowlog.threshold.index.debug": "2s",
  "index.indexing.slowlog.threshold.index.trace": "500ms",
  "index.indexing.slowlog.source": "1000", <2>
  "index.indexing.slowlog.reformat": true,
  "index.indexing.slowlog.include.user": true <1>
}
```

1. You can use the `index.search.slowlog.include.user` setting for search operations or the `index.indexing.slowlog.include.user` setting for indexing operations to append `user.*` and `auth.type` fields to slow log entries. These fields contain information about the user who triggered the request. 

2. Slow logs can record the `_source` of documents involved in slow queries. Use this setting only while actively troubleshooting as it can significantly increase log size and might expose sensitive data.

For more information about slow log settings, refer to [slow log settings](elasticsearch://reference/elasticsearch/index-settings/slow-log.md).

:::
::::




To adjust slow log settings across all indices (cluster-wide), use the following settings in your [`log4j2.properties` configuration file](/deploy-manage/deploy/self-managed/configure-elasticsearch.md):

::::{tab-set}
:group: slow-logs
:::{tab-item} Search operations
:sync: search

```yaml
index.search.slowlog.threshold.query.warn: 10s
index.search.slowlog.threshold.query.info: 5s
index.search.slowlog.threshold.query.debug: 2s
index.search.slowlog.threshold.query.trace: 500ms

index.search.slowlog.threshold.fetch.warn: 1s
index.search.slowlog.threshold.fetch.info: 800ms
index.search.slowlog.threshold.fetch.debug: 500ms
index.search.slowlog.threshold.fetch.trace: 200ms

index.search.slowlog.include.user: true
```

:::
:::
:::{tab-item} Indexing operations
:sync: index

```yaml
index.indexing.slowlog.threshold.index.warn: 10s
index.indexing.slowlog.threshold.index.info: 5s
index.indexing.slowlog.threshold.index.debug: 2s
index.indexing.slowlog.threshold.index.trace: 500ms

index.indexing.slowlog.source: 1000
index.indexing.slowlog.reformat: true

index.indexing.slowlog.include.user: true
```

:::
::::


## When and how to use slow logs [troubleshoot-slow-log]

Logging slow requests can be resource intensive to your {{es}} cluster depending on the qualifying traffic’s volume. For example, emitted logs might increase the index disk usage of your [{{es}} monitoring](/deploy-manage/monitor/stack-monitoring.md) cluster. 

To reduce the impact of slow logs, consider the following:

* Enable slow logs only when troubleshooting.
* Enable slow logs against specific indices rather than across all indices.
* Set high thresholds to reduce the number of logged events.

If you aren’t sure how to start investigating traffic issues, consider enabling the `warn` threshold with a high `30s` threshold at the index level using the [update indices settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings) API:

::::{tab-set}
:group: slow-logs
:::{tab-item} Search operations
:sync: search

```console
PUT /*/_settings
{
  "index.search.slowlog.include.user": true,
  "index.search.slowlog.threshold.fetch.warn": "30s",
  "index.search.slowlog.threshold.query.warn": "30s"
}
```

:::
:::{tab-item} Indexing operations
:sync: index

```console
PUT /*/_settings
{
  "index.indexing.slowlog.include.user": true,
  "index.indexing.slowlog.threshold.index.warn": "30s"
}
```

:::
::::


Slow log thresholds being met does not guarantee cluster performance issues. Slow logs can provide helpful data to diagnose upstream traffic patterns or sources to resolve client-side issues. For example, you can use data included in `X-Opaque-ID`, the `_source` request body, or `user.*` fields to identify the source of your issue. This is similar to troubleshooting [live expensive tasks](/troubleshoot/elasticsearch/task-queue-backlog.md).

If you’re experiencing search performance issues, then you might want to consider investigating searches flagged for their query durations using the [profile API](elasticsearch://reference/elasticsearch/rest-apis/search-profile.md). You can then use the profiled query to investigate optimization options using the [query profiler](/explore-analyze/query-filter/tools/search-profiler.md). This type of investigation should usually take place in a non-production environment.

Slow logging checks each event against the reporting threshold when the event is complete. This means that it can’t report if events trigger [circuit breaker errors](/troubleshoot/elasticsearch/circuit-breaker-errors.md). If you suspect circuit breaker errors, then you should also consider enabling [audit logging](/deploy-manage/security/logging-configuration/enabling-audit-logs.md), which logs events before they are executed.

## Learn more [_learn_more]

To learn about other ways to optimize your search and indexing requests, refer to [tune for search speed](/deploy-manage/production-guidance/optimize-performance/search-speed.md) and [tune for indexing speed](/deploy-manage/production-guidance/optimize-performance/indexing-speed.md).