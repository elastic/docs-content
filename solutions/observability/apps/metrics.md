---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-data-model-metrics.html
---

# Metrics [apm-data-model-metrics]

**Metrics** measure the state of a system by gathering information on a regular interval. There are two types of APM metrics:

* **System metrics**: Basic infrastructure and application metrics.
* **Calculated metrics**: Aggregated trace event metrics used to power visualizations in the Applications UI.


## System metrics [_system_metrics]

APM agents automatically pick up basic host-level metrics, including system and process-level CPU and memory metrics. Agent specific metrics are also available, like [JVM metrics](asciidocalypse://docs/apm-agent-java/docs/reference/metrics.md) in the Java Agent, and [Go runtime](asciidocalypse://docs/apm-agent-go/docs/reference/metrics.md) metrics in the Go Agent.

Infrastructure and application metrics are important sources of information when debugging production systems, which is why we’ve made it easy to filter metrics for specific hosts or containers in the {{kib}} [metrics overview](metrics-2.md).

::::{tip}
Most agents limit keyword fields to 1024 characters, non-keyword fields (e.g. `system.memory.total`) to 10,000 characters.
::::


Metrics are stored in metric indices.

For a full list of tracked metrics, see the relevant agent documentation:

* [Go](asciidocalypse://docs/apm-agent-go/docs/reference/metrics.md)
* [Java](asciidocalypse://docs/apm-agent-java/docs/reference/metrics.md)
* [Node.js](asciidocalypse://docs/apm-agent-nodejs/docs/reference/metrics.md)
* [Python](asciidocalypse://docs/apm-agent-python/docs/reference/metrics.md)
* [Ruby](asciidocalypse://docs/apm-agent-ruby/docs/reference/metrics.md)


### Example system metric document [_example_system_metric_document]

This example shows what system metric documents can look like when indexed in {{es}}.

::::{dropdown} Expand {{es}} document
This example contains JVM metrics produced by the {{apm-java-agent}}. and contains two related metrics: `jvm.gc.time` and `jvm.gc.count`. These are accompanied by various fields describing the environment in which the metrics were captured: service name, host name, Kubernetes pod UID, container ID, process ID, and more. These fields make it possible to search and aggregate across various dimensions, such as by service, host, and Kubernetes pod.

```json
{
  "container": {
    "id": "a47ed147c6ee269400f7ea4e296b3d01ec7398471bb2951907e4ea12f028bc69"
  },
  "kubernetes": {
    "pod": {
      "uid": "b0cb3baa-4619-4b82-bef5-84cc87b5f853",
      "name": "opbeans-java-7c68f48dc6-n6mzc"
    }
  },
  "process": {
    "pid": 8,
    "title": "/opt/java/openjdk/bin/java",
    "parent": {
      "pid": 1
    }
  },
  "agent": {
    "name": "java",
    "ephemeral_id": "29a27947-ed3a-4d87-b2e6-28f7a940ec2d",
    "version": "1.25.1-SNAPSHOT.UNKNOWN"
  },
  "jvm.gc.time": 11511,
  "processor": {
    "name": "metric",
    "event": "metric"
  },
  "labels": {
    "name": "Copy"
  },
  "metricset.name": "app",
  "observer": {
    "hostname": "3c5ac040e8f9",
    "name": "instance-0000000002",
    "type": "apm-server",
    "version": "7.15.0"
  },
  "@timestamp": "2021-09-14T09:52:49.454Z",
  "ecs": {
    "version": "1.11.0"
  },
  "service": {
    "node": {
      "name": "a47ed147c6ee269400f7ea4e296b3d01ec7398471bb2951907e4ea12f028bc69"
    },
    "environment": "production",
    "name": "opbeans-java",
    "runtime": {
      "name": "Java",
      "version": "11.0.11"
    },
    "language": {
      "name": "Java",
      "version": "11.0.11"
    },
    "version": "2021-09-08 03:55:06"
  },
  "jvm.gc.count": 2224,
  "host": {
    "os": {
      "platform": "Linux"
    },
    "ip": ["35.240.52.17"],
    "architecture": "amd64"
  },
  "event": {
    "ingested": "2021-09-14T09:53:00.834276431Z"
  }
}
```

::::



## Calculated metrics [_calculated_metrics]

APM agents and APM Server calculate metrics from trace events to power visualizations in the Applications UI.

Calculated metrics are an implementation detail and while we aim for stability for these data models, the dimensions and concrete limits for aggregations are subject to change within minor version updates.

These metrics are described below.


### Breakdown metrics [_breakdown_metrics]

To power the [Time spent by span type](transactions-2.md) graph, agents collect summarized metrics about the timings of spans and transactions, broken down by span type.

**`span.self_time.count`** and **`span.self_time.sum.us`**
:   These metrics measure the "self-time" for a span type, and optional subtype, within a transaction group. Together these metrics can be used to calculate the average duration and percentage of time spent on each type of operation within a transaction group.

These metric documents can be identified by searching for `metricset.name: span_breakdown`.

You can filter and group by these dimensions:

* `transaction.name`: The name of the enclosing transaction group, for example `GET /`
* `transaction.type`: The type of the enclosing transaction, for example `request`
* `span.type`: The type of the span, for example `app`, `template` or `db`
* `span.subtype`: The sub-type of the span, for example `mysql` (optional)



### Example breakdown metric document [_example_breakdown_metric_document]

This example shows what breakdown metric documents can look like when indexed in {{es}}.

::::{dropdown} Expand {{es}} document
```json
{
  "@timestamp": "2022-02-28T13:41:14.594Z",
  "agent": {
    "name": "ruby",
    "version": "4.5.0"
  },
  "data_stream": {
    "dataset": "apm.internal",
    "namespace": "default",
    "type": "metrics"
  },
  "ecs": {
    "version": "8.6.0-dev"
  },
  "event": {
    "agent_id_status": "missing",
    "ingested": "2023-06-20T09:45:03Z"
  },
  "host": {
    "architecture": "x86_64",
    "hostname": "19887b56414b",
    "ip": "127.0.0.1",
    "name": "19887b56414b",
    "os": {
      "platform": "linux"
    }
  },
  "metricset": {
    "name": "span_breakdown"
  },
  "observer": {
    "hostname": "hostname",
    "type": "apm-server",
    "version": "8.8.2"
  },
  "process": {
    "args": [
      "-C",
      "config/puma.rb"
    ],
    "pid": 150,
    "title": "/usr/local/bundle/bin/puma"
  },
  "processor": {
    "event": "metric",
    "name": "metric"
  },
  "service": {
    "environment": "production",
    "framework": {
      "name": "Ruby on Rails",
      "version": "6.1.4.1"
    },
    "language": {
      "name": "ruby",
      "version": "2.7.3"
    },
    "name": "opbeans-ruby",
    "node": {
      "name": "19887b56414b"
    },
    "runtime": {
      "name": "ruby",
      "version": "2.7.3"
    },
    "version": "None"
  },
  "span": {
    "self_time": {
      "count": 1,
      "sum": {
        "us": 3473
      }
    },
    "subtype": "controller",
    "type": "app"
  },
  "transaction": {
    "name": "Api::OrdersController#create",
    "type": "request"
  }
}
```

::::



### Transaction metrics [_transaction_metrics]

To power [{{kib}} Applications UI](overviews.md) visualizations, APM Server aggregates transaction events into latency distribution metrics.

**`transaction.duration.summary`** and **`transaction.duration.histogram`**
:   These metrics represent the latency summary and latency distribution of transaction groups, used to power transaction-oriented visualizations and analytics in Elastic APM.

These metric documents can be identified by searching for `metricset.name: transaction`.

You can filter and group by these dimensions (some of which are optional, for example `container.id`):

* `agent.name`: The name of the {{apm-agent}} that instrumented the transaction, for example `java`
* `cloud.account.id`: The cloud account id of the service that served the transaction
* `cloud.account.name`: The cloud account name of the service that served the transaction
* `cloud.availability_zone`: The cloud availability zone hosting the service instance that served the transaction
* `cloud.machine.type`: The cloud machine type or instance type of the service that served the transaction
* `cloud.project.id`: The cloud project identifier of the service that served the transaction
* `cloud.project.name`: The cloud project name of the service that served the transaction
* `cloud.provider`: The cloud provider hosting the service instance that served the transaction
* `cloud.region`: The cloud region hosting the service instance that served the transaction
* `cloud.service.name`: The cloud service name of the service that served the transaction
* `container.id`: The container ID of the service that served the transaction
* `event.outcome`: The outcome of the transaction, for example `success`
* `faas.coldstart`: Whether the *serverless* service that served the transaction had a cold start
* `faas.id`: The unique identifier of the invoked serverless function
* `faas.name`: The name of the lambda function
* `faas.trigger.type`: The trigger type that the lambda function was executed by of the service that served the transaction
* `faas.version`: The version of the lambda function
* `host.hostname`: The detected hostname of the service that served the transaction
* `host.name`: The user-defined name of the host or the detected hostname of the service that served the transaction
* `host.os.platform`: The platform name of the service that served the transaction, for example `linux`
* `kubernetes.pod.name`: The name of the Kubernetes pod running the service that served the transaction
* `labels`: Key-value object containing string labels set globally by the APM agents. This dimension is not present for RUM agents.
* `metricset.interval`: A string with the aggregation interval the metricset represents.
* `numeric_labels`: Key-value object containing numeric labels set globally by the APM agents. This dimension is not present for RUM agents.
* `service.environment`: The environment of the service that served the transaction
* `service.language.name`: The language name of the service that served the transaction, for example `Go`
* `service.language.version`: The language version of the service that served the transaction
* `service.name`: The name of the service that served the transaction
* `service.node.name`: The name of the service instance that served the transaction
* `service.runtime.name`: The runtime name of the service that served the transaction, for example `jRuby`
* `service.runtime.version`: The runtime version that served the transaction
* `service.version`: The version of the service that served the transaction
* `transaction.name`: The name of the transaction, for example `GET /`
* `transaction.result`: The result of the transaction, for example `HTTP 2xx`
* `transaction.root`: A boolean flag indicating whether the transaction is the root of a trace
* `transaction.type`: The type of the transaction, for example `request`


The `@timestamp` field of these documents holds the start of the aggregation interval.


### Example transaction document [_example_transaction_document_2]

This example shows what transaction documents can look like when indexed in {{es}}.

::::{dropdown} Expand {{es}} document
```json
{
  "@timestamp": "2022-02-28T13:39:00.000Z",
  "_doc_count": 2421,
  "agent": {
    "name": "ruby"
  },
  "data_stream": {
    "dataset": "apm.transaction.1m",
    "namespace": "default",
    "type": "metrics"
  },
  "ecs": {
    "version": "8.6.0-dev"
  },
  "event": {
    "agent_id_status": "missing",
    "ingested": "2023-06-20T09:49:53Z",
    "outcome": "success",
    "success_count": {
      "sum": 2421.0,
      "value_count": 2421
    }
  },
  "host": {
    "hostname": "19887b56414b",
    "name": "19887b56414b",
    "os": {
      "platform": "linux"
    }
  },
  "metricset": {
    "interval": "1m",
    "name": "transaction"
  },
  "observer": {
    "hostname": "hostname",
    "type": "apm-server",
    "version": "8.8.2"
  },
  "processor": {
    "event": "metric",
    "name": "metric"
  },
  "service": {
    "environment": "production",
    "language": {
      "name": "ruby",
      "version": "2.7.3"
    },
    "name": "opbeans-ruby",
    "node": {
      "name": "19887b56414b"
    },
    "runtime": {
      "name": "ruby",
      "version": "2.7.3"
    },
    "version": "None"
  },
  "transaction": {
    "duration": {
      "histogram": {
        "values": [
          16255.0,
          20095.0,
          20351.0,
          24447.0,
          24703.0,
          25087.0,
          25471.0,
          26111.0,
          26623.0,
          28287.0,
          29695.0,
          30847.0,
          31231.0,
          31871.0,
          33023.0,
          36351.0,
          41727.0,
          44287.0,
          46847.0,
          56575.0,
          61695.0,
          81407.0,
          88575.0,
          107519.0
        ],
        "counts": [
          90,
          89,
          90,
          90,
          90,
          180,
          180,
          90,
          89,
          90,
          90,
          90,
          90,
          89,
          90,
          90,
          89,
          89,
          90,
          179,
          89,
          89,
          90,
          89
        ]
      },
      "summary": {
        "sum": 9.5487371E7,
        "value_count": 2421
      }
    },
    "name": "Api::CustomersController#index",
    "result": "HTTP 2xx",
    "root": true,
    "type": "request"
  }
}
```

::::



### Service-transaction metrics [_service_transaction_metrics]

To power [{{kib}} Applications UI](overviews.md) visualizations, APM Server aggregates transaction events into service-transaction metrics. Service-transaction metrics are similar to transaction metrics, but they usually have a much lower cardinality as they have significantly fewer dimensions. The UI uses them when fewer details of the transactions are needed.

**`transaction.duration.summary`** and **`transaction.duration.histogram`**
:   These metrics represent the latency summary and latency distribution of service transaction groups, used to power service-oriented visualizations and analytics in Elastic APM.

These metric documents can be identified by searching for `metricset.name: service_transaction`.

You can filter and group by these dimensions:

* `agent.name`: The name of the {{apm-agent}} that instrumented the operation, for example `java`
* `labels`: Key-value object containing string labels set globally by the APM agents. This dimension is not present for RUM agents.
* `metricset.interval`: A string with the aggregation interval the metricset represents.
* `numeric_labels`: Key-value object containing numeric labels set globally by the APM agents. This dimension is not present for RUM agents.
* `service.environment`: The environment of the service that made the request
* `service.language.name`: The language name of the service that served the transaction, for example `Go`
* `service.name`: The name of the service that made the request
* `transaction.type`: The type of the enclosing transaction, for example `request`


The `@timestamp` field of these documents holds the start of the aggregation interval.


### Example service-transaction document [_example_service_transaction_document]

This example shows what service-transaction documents can look like when indexed in {{es}}.

::::{dropdown} Expand {{es}} document
```json
{
  "@timestamp": "2022-02-28T13:40:00.000Z",
  "_doc_count": 2677,
  "agent": {
    "name": "ruby"
  },
  "data_stream": {
    "dataset": "apm.service_transaction.1m",
    "namespace": "default",
    "type": "metrics"
  },
  "ecs": {
    "version": "8.6.0-dev"
  },
  "event": {
    "agent_id_status": "missing",
    "ingested": "2023-06-20T09:59:52Z",
    "success_count": {
      "sum": 2567.0,
      "value_count": 2677
    }
  },
  "metricset": {
    "interval": "1m",
    "name": "service_transaction"
  },
  "observer": {
    "hostname": "hostname",
    "type": "apm-server",
    "version": "8.8.2"
  },
  "processor": {
    "event": "metric",
    "name": "metric"
  },
  "service": {
    "environment": "production",
    "language": {
      "name": "ruby"
    },
    "name": "opbeans-ruby"
  },
  "transaction": {
    "duration": {
      "histogram": {
        "values": [
          9215.0,
          9279.0,
          10047.0,
          10687.0,
          10751.0,
          11263.0,
          12991.0,
          13631.0,
          14335.0,
          14399.0,
          15167.0,
          15295.0,
          15935.0,
          16063.0,
          16767.0,
          18047.0,
          18175.0,
          18303.0,
          18431.0,
          18559.0,
          18943.0,
          19199.0,
          19583.0,
          19711.0,
          19839.0,
          20479.0,
          20735.0,
          20863.0,
          20991.0,
          21119.0,
          21375.0,
          22143.0,
          22399.0,
          22527.0,
          22655.0,
          23167.0,
          23807.0,
          24319.0,
          24575.0,
          24959.0,
          25855.0,
          26239.0,
          26367.0,
          26623.0,
          26751.0,
          27007.0,
          27135.0,
          27263.0,
          27647.0,
          28031.0,
          28287.0,
          28543.0,
          28671.0,
          28927.0,
          29951.0,
          30079.0,
          30335.0,
          30463.0,
          31231.0,
          31487.0,
          31615.0,
          31743.0,
          32127.0,
          32383.0,
          32767.0,
          33023.0,
          33279.0,
          33535.0,
          34047.0,
          34303.0,
          34815.0,
          35071.0,
          35327.0,
          35583.0,
          36351.0,
          37631.0,
          38143.0,
          38911.0,
          39167.0,
          39679.0,
          40447.0,
          40703.0,
          40959.0,
          41215.0,
          41471.0,
          41983.0,
          42495.0,
          43007.0,
          43263.0,
          43519.0,
          43775.0,
          44799.0,
          45311.0,
          46591.0,
          46847.0,
          47103.0,
          48127.0,
          48383.0,
          48639.0,
          48895.0,
          49151.0,
          49407.0,
          49919.0,
          50431.0,
          50687.0,
          51455.0,
          51711.0,
          52223.0,
          53759.0,
          54271.0,
          54527.0,
          55039.0,
          55807.0,
          56063.0,
          56319.0,
          57087.0,
          57343.0,
          57599.0,
          58879.0,
          59647.0,
          59903.0,
          60927.0,
          61695.0,
          62719.0,
          63743.0,
          64255.0,
          64767.0,
          66559.0,
          67071.0,
          68095.0,
          68607.0,
          69119.0,
          69631.0,
          70655.0,
          71679.0,
          72191.0,
          72703.0,
          73727.0,
          74239.0,
          75775.0,
          76287.0,
          76799.0,
          77311.0,
          77823.0,
          82943.0,
          83967.0,
          84991.0,
          86015.0,
          87551.0,
          89087.0,
          89599.0,
          91647.0,
          92671.0,
          95231.0,
          95743.0,
          97279.0,
          98815.0,
          99327.0,
          99839.0,
          100863.0,
          101887.0,
          102399.0,
          102911.0,
          103423.0,
          103935.0,
          105983.0,
          109055.0,
          111615.0,
          112127.0,
          118271.0,
          119295.0,
          122879.0,
          129023.0,
          129535.0,
          132095.0,
          133119.0,
          137215.0,
          139263.0,
          140287.0,
          146431.0,
          147455.0,
          148479.0,
          152575.0,
          158719.0,
          159743.0,
          161791.0,
          165887.0,
          171007.0,
          173055.0,
          174079.0,
          178175.0,
          181247.0,
          182271.0,
          190463.0,
          193535.0,
          195583.0,
          198655.0,
          201727.0,
          212991.0,
          224255.0,
          240639.0,
          250879.0,
          262143.0,
          329727.0,
          1236991.0,
          2097151.0,
          2408447.0,
          2424831.0,
          3801087.0,
          3850239.0,
          4063231.0,
          4177919.0,
          4390911.0,
          4947967.0,
          5275647.0,
          5832703.0,
          5898239.0,
          5931007.0,
          6324223.0,
          6455295.0,
          6488063.0,
          8454143.0
        ],
        "counts": [
          9,
          9,
          9,
          9,
          10,
          9,
          9,
          9,
          9,
          9,
          10,
          10,
          18,
          9,
          10,
          18,
          9,
          10,
          9,
          9,
          18,
          19,
          9,
          19,
          9,
          9,
          9,
          9,
          19,
          9,
          10,
          18,
          9,
          9,
          18,
          10,
          9,
          9,
          9,
          9,
          10,
          18,
          10,
          18,
          9,
          18,
          9,
          9,
          10,
          9,
          10,
          9,
          9,
          9,
          9,
          9,
          9,
          27,
          9,
          9,
          10,
          9,
          10,
          9,
          19,
          9,
          19,
          9,
          9,
          19,
          9,
          18,
          28,
          9,
          27,
          18,
          18,
          10,
          10,
          9,
          10,
          9,
          10,
          10,
          18,
          29,
          18,
          9,
          9,
          9,
          10,
          9,
          9,
          9,
          9,
          19,
          19,
          10,
          10,
          10,
          18,
          19,
          9,
          9,
          10,
          18,
          10,
          19,
          9,
          9,
          9,
          10,
          10,
          10,
          9,
          9,
          18,
          9,
          9,
          9,
          9,
          19,
          18,
          18,
          10,
          18,
          9,
          38,
          9,
          9,
          18,
          19,
          9,
          9,
          18,
          9,
          18,
          9,
          9,
          9,
          10,
          19,
          27,
          10,
          18,
          28,
          19,
          9,
          20,
          18,
          18,
          10,
          9,
          9,
          9,
          28,
          9,
          10,
          9,
          9,
          19,
          28,
          9,
          18,
          9,
          9,
          9,
          9,
          9,
          9,
          9,
          9,
          10,
          9,
          9,
          10,
          9,
          29,
          9,
          10,
          10,
          18,
          9,
          10,
          9,
          19,
          10,
          9,
          18,
          10,
          9,
          9,
          10,
          10,
          9,
          9,
          10,
          9,
          10,
          9,
          9,
          10,
          9,
          9,
          9,
          9,
          9,
          9,
          9,
          9,
          9,
          9,
          9,
          9,
          9,
          9,
          10,
          9,
          10,
          10,
          10,
          18
        ]
      },
      "summary": {
        "sum": 1.027476555E9,
        "value_count": 2677
      }
    },
    "type": "request"
  }
}
```

::::



### Service-destination metrics [_service_destination_metrics]

To power [{{kib}} Applications UI](overviews.md) visualizations, APM Server aggregates span events into service-destination metrics.

**`span.destination.service.response_time.count`** and **`span.destination.service.response_time.sum.us`**
:   These metrics measure the count and total duration of requests from one service to another service. These are used to calculate the throughput and latency of requests to backend services such as databases in [Service maps](service-map.md).

These metric documents can be identified by searching for `metricset.name: service_destination`.

You can filter and group by these dimensions:

* `agent.name`: The name of the {{apm-agent}} that instrumented the operation, for example `java`
* `event.outcome`: The outcome of the operation, for example `success`
* `labels`: Key-value object containing string labels set globally by the APM agents. This dimension is not present for RUM agents.
* `metricset.interval`: A string with the aggregation interval the metricset represents.
* `numeric_labels`: Key-value object containing numeric labels set globally by the APM agents. This dimension is not present for RUM agents.
* `service.environment`: The environment of the service that made the request
* `service.language.name`: The language name of the service that served the transaction, for example `Go`
* `service.name`: The name of the service that made the request
* `service.target.name`: The target service name, for example `customer_db`
* `service.target.type`: The target service type, for example `mysql`
* `span.destination.service.resource`: The destination service resource, for example `mysql`
* `span.name`: The name of the operation, for example `SELECT FROM table_name`.


The `@timestamp` field of these documents holds the start of the aggregation interval.


### Example service-destination document [_example_service_destination_document]

This example shows what service-destination documents can look like when indexed in {{es}}.

::::{dropdown} Expand {{es}} document
```json
{
  "@timestamp": "2022-02-28T13:41:00.000Z",
  "_doc_count": 7488,
  "agent": {
    "name": "ruby"
  },
  "data_stream": {
    "dataset": "apm.service_destination.1m",
    "namespace": "default",
    "type": "metrics"
  },
  "ecs": {
    "version": "8.6.0-dev"
  },
  "event": {
    "agent_id_status": "missing",
    "ingested": "2023-06-20T09:45:53Z",
    "outcome": "unknown"
  },
  "metricset": {
    "interval": "1m",
    "name": "service_destination"
  },
  "observer": {
    "hostname": "hostname",
    "type": "apm-server",
    "version": "8.8.2"
  },
  "processor": {
    "event": "metric",
    "name": "metric"
  },
  "service": {
    "environment": "production",
    "language": {
      "name": "ruby"
    },
    "name": "opbeans-ruby",
    "target": {
      "type": "postgresql"
    }
  },
  "span": {
    "destination": {
      "service": {
        "resource": "postgresql",
        "response_time": {
          "count": 7488,
          "sum": {
            "us": 21309833
          }
        }
      }
    },
    "name": "SELECT FROM product_kinds"
  }
}
```

::::



### Service-summary metrics [_service_summary_metrics]

To power [{{kib}} Applications UI](overviews.md) visualizations, APM Server aggregates transaction, error, log, and metric events into service-summary metrics.

These metric documents can be identified by searching for `metricset.name: service_summary`.

You can filter and group by these dimensions:

* `agent.name`: The name of the {{apm-agent}} that instrumented the operation, for example `java`
* `labels`: Key-value object containing string labels set globally by the APM agents. This dimension is not present for RUM agents.
* `metricset.interval`: A string with the aggregation interval the metricset represents.
* `numeric_labels`: Key-value object containing numeric labels set globally by the APM agents. This dimension is not present for RUM agents.
* `service.environment`: The environment of the service that made the request
* `service.language.name`: The language name of the service that served the transaction, for example `Go`
* `service.name`: The name of the service that made the request

The `@timestamp` field of these documents holds the start of the aggregation interval.


### Example service-summary document [_example_service_summary_document]

This example shows what service-summary documents can look like when indexed in {{es}}.

::::{dropdown} Expand {{es}} document
```json
{
  "@timestamp": "2022-02-28T13:37:00.000Z",
  "agent": {
    "name": "nodejs"
  },
  "data_stream": {
    "dataset": "apm.service_summary.1m",
    "namespace": "default",
    "type": "metrics"
  },
  "ecs": {
    "version": "8.6.0-dev"
  },
  "event": {
    "agent_id_status": "missing",
    "ingested": "2023-06-20T09:45:53Z"
  },
  "metricset": {
    "interval": "1m",
    "name": "service_summary"
  },
  "observer": {
    "hostname": "hostname",
    "type": "apm-server",
    "version": "8.8.2"
  },
  "processor": {
    "event": "metric",
    "name": "metric"
  },
  "service": {
    "environment": "production",
    "language": {
      "name": "javascript"
    },
    "name": "opbeans-node"
  }
}
```

::::



## Data streams [_data_streams_4]

Metrics are stored in the following data streams:

* APM internal metrics: `metrics-apm.internal-<namespace>`
* APM transaction metrics: `metrics-apm.transaction.<metricset.interval>-<namespace>`
* APM service destination metrics: `metrics-apm.service_destination.<metricset.interval>-<namespace>`
* APM service transaction metrics: `metrics-apm.service_transaction.<metricset.interval>-<namespace>`
* APM service summary metrics: `metrics-apm.service_summary.<metricset.interval>-<namespace>`
* Application metrics: `metrics-apm.app.<service.name>-<namespace>`

See [Data streams](data-streams.md) to learn more.


## Aggregated metrics: limits and overflows [_aggregated_metrics_limits_and_overflows]

For all aggregated metrics, namely transaction, service-transaction, service-destination, and service-summary metrics, there are limits on the number of unique groups tracked at any given time.


### Limits [_limits]

Note that all the below limits may change in the future with further improvements.

* For all the following metrics, they share a limit of 1000 services per GB of APM Server.

    * For transaction metrics, there is an additional limit of 5000 total transaction groups per GB of APM Server, and each service may only consume up to 10% of the transaction groups, which is 500 transaction groups per service per GB of APM Server.
    * For service-transaction metrics, there is an additional limit of 1000 total service transaction groups per GB of APM Server, and each service may only consume up to 10% of the service transaction groups, which is 100 service transaction groups per service per GB of APM Server.
    * For service-destination metrics, there is an additional limit of 5000 total service destination groups per GB of APM Server starting with 10000 service destination groups for 1 GB APM Server, and each service may only consume up to 10% of the service destination groups, which is 1000 service destination groups for 1GB APM Server with 500 increment per GB of APM Server.
    * For service-summary metrics, there is no additional limit.


In the previous metrics, a service is defined as a combination of `service.name`, `service.environment`, `service.language.name` and `agent.name`.


### Overflows [_overflows]

When a dimension has a high cardinality and exceeds the limit, the metrics will be aggregated under a dedicated overflow bucket.

For example, when `transaction.name` has a lot of unique values and reaches the limit of unique transaction groups tracked, any transactions with new `transaction.name` will be aggregated under `transaction.name`: `_other`.

Another example of how the transaction group limit may be reached is if `transaction.name` contains just a few unique values, but the service is deployed on a lot of different hosts. As `host.name` is part of the aggregation key for transaction metrics, the max transaction group limit is reached for a service that has 100 instances, 10 different transaction names, and 4 transaction results per transaction name when connected to an APM Server with 8GB of RAM. Once this limit is reached, any new combinations of `transaction.name`, `transaction.result`, and `host.name` for that service will be aggregated under `transaction.name`: `_other`.

This issue can be resolved by increasing memory available to APM Server, or by ensuring that the dimensions do not use values that are based on parameters that can change. For example, user ids, product ids, order numbers, query parameters, etc., should be stripped away from the dimensions. For the same reason, avoid high cardinality global labels (`labels.\*` and `numeric_labels.*`).

Aggregated metrics do not consider global labels from RUM agents in order to protect APM server from using too much memory.
