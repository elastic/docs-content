---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-data-model.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-data-types.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Application data types [observability-apm-data-types]

Elastic APM agents capture different types of information from within their instrumented applications. These are known as events, and can be spans, transactions, traces, errors, or metrics.

Elastic APM helps you see what happens from start to finish when a request is made to an application:

* [**Spans**](/solutions/observability/apm/spans.md): A span contain information about the execution of a specific code path. They are the building blocks of *transactions* and *traces*.
* [**Transactions**](/solutions/observability/apm/transactions.md): A transaction describes an event captured by an Elastic APM agent instrumenting a service. A transaction is technically a type of span that has additional attributes associated with it and often contains multiple child *spans*. You can think of transactions as the highest level of work you’re measuring within a service.
* [**Traces**](/solutions/observability/apm/traces.md#apm-distributed-tracing): A trace is a group of *transactions* and *spans* with a common root. Each trace tracks the entirety of a single request. When a trace travels through multiple services, it is known as a *distributed trace*.

:::{image} /solutions/images/observability-spans-transactions-and-traces.png
:alt: Diagram illustrating the relationship between spans
:::

In addition to the building blocks of traces, Elastic APM agents also capture:

* [**Errors**](/solutions/observability/apm/errors.md): An error is created when something goes wrong with a request to an application. This event contains information to help you determine where and why an error occurred, often including in which *transaction* the error occurred.
* [**Metrics**](/solutions/observability/apm/metrics.md): Metrics measure the state of a system by gathering information on a regular interval.

Events can contain additional [metadata](/solutions/observability/apm/metadata.md) which further enriches your data.