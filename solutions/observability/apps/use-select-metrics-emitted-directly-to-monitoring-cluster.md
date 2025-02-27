---
navigation_title: "Use local collection"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-monitoring-local-collection.html
applies_to:
  stack: all
---

# Use the select metrics emitted directly to your monitoring cluster [apm-monitoring-local-collection]


In 8.11 and later, we emit a selected set of metrics directly to the monitoring cluster. The benefit of using local collection instead of internal collection is that the metrics are sent directly to your main monitoring index, making it easier to view shared data.

## The select metrics [apm-select-metrics]

We only ship a select list of metrics, to avoid overwhelming your monitoring cluster. If you need the entire set of metrics and traces we can expose, you should use [Self Instrumentation](configure-apm-instrumentation.md) instead of local collection.

Here is the list of every metrics we currently expose:

* http.server.request.count
* http.server.request.duration
* http.server.response.valid.count
* http.server.response.errors.count
* http.server.errors.timeout
* http.server.errors.ratelimit
* grpc.server.request.count
* grpc.server.request.duration
* grpc.server.response.valid.count
* grpc.server.response.errors.count
* grpc.server.errors.timeout
* grpc.server.errors.ratelimit