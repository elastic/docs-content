---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-performance-diagnostic.html
applies_to:
  stack: all
products:
  - id: observability
---

# APM Server performance diagnostic [apm-performance-diagnostic]


## Diagnosing backpressure from {{es}} [apm-es-backpressure]

When {{es}} is under excessive load or indexing pressure, APM Server could experience the downstream backpressure when indexing new documents into {{es}}. Most commonly, backpressure from {{es}} will manifest itself in the form of higher indexing latency and/or rejected requests, which in return could lead APM Server to deny incoming requests. As a result, APM agents connected to the affected APM Server will suffer from throttling and/or request timeout when shipping APM events.

To quickly identify possible issues try looking for similar error logs lines in APM Server logs:

```json
...
{"log.level":"error","@timestamp":"2024-07-27T23:46:28.529Z","log.origin":{"function":"github.com/elastic/go-docappender/v2.(*Appender).flush","file.name":"v2@v2.2.0/appender.go","file.line":370},"message":"bulk indexing request failed","service.name":"apm-server","error":{"message":"flush failed (429): [429 Too Many Requests]"},"ecs.version":"1.6.0"}
{"log.level":"error","@timestamp":"2024-07-27T23:55:38.612Z","log.origin":{"function":"github.com/elastic/go-docappender/v2.(*Appender).flush","file.name":"v2@v2.2.0/appender.go","file.line":370},"message":"bulk indexing request failed","service.name":"apm-server","error":{"message":"flush failed (503): [503 Service Unavailable]"},"ecs.version":"1.6.0"}
...
```

To gain better insight into APM Server health and performance, consider enabling the monitoring feature by following the steps in [Monitor APM Server](/solutions/observability/apm/apm-server/monitor.md). When enabled, APM Server will additionally report a set of vital metrics to help you identify any performance degradation.

Pay careful attention to the next metric fields:

* `beats_stats.metrics.libbeat.output.events.active` that represents the number of buffered pending documents waiting to be ingested; (*if this value is increasing rapidly it may indicate {{es}} backpressure*)
* `beats_stats.metrics.libbeat.output.events.acked` that represents the total number of documents that have been ingested successfully;
* `beats_stats.metrics.libbeat.output.events.failed` that represents the total number of documents that failed to ingest; (*if this value is increasing rapidly it may indicate {{es}} backpressure*)
* `beats_stats.metrics.libbeat.output.events.toomany` that represents the number of documents that failed to ingest due to {{es}} responding with 429 Too many Requests; (*if this value is increasing rapidly it may indicate {{es}} backpressure*)
* `beats_stats.output.elasticsearch.bulk_requests.available` that represents the number of bulk indexers available for making bulk index requests; (*if this value is equal to 0 it may indicate {{es}} backpressure*)
* `beats_stats.output.elasticsearch.bulk_requests.completed` that represents the number of already completed bulk requests;
* `beats_stats.metrics.output.elasticsearch.indexers.active` that represents the number of active bulk indexers that are concurrently processing batches;

See [{{metricbeat}} documentation](beats://reference/metricbeat/exported-fields-beat.md) for the full list of exported metric fields.

One likely cause of excessive indexing pressure or rejected requests is undersized {{es}}. To mitigate this, follow the guidance in [Rejected requests](../../elasticsearch/rejected-requests.md).

(Not recommended) If scaling {{es}} resources up is not an option, you can adjust the `flush_bytes`, `flush_interval`, `max_retries` and `timeout` settings described in [](/solutions/observability/apm/apm-server/configure-elasticsearch-output.md) to reduce APM Server indexing pressure. However, consider that increasing number of buffered documents and/or reducing retries may lead to a higher rate of dropped APM events. Down below a custom configuration example is listed where the number of default buffered documents is roughly doubled while {{es}} indexing retries are decreased simultaneously. This configuration provides a generic example and might not be applicable to your situation. Try adjusting the settings further to see what works for you.

```yaml
output.elasticsearch:
  flush_bytes: "2MB" # double the default value
  flush_interval: "2s" # double the default value
  max_retries: 1 # decrease the default value
  timeout: 60 # decrease the default value
```

