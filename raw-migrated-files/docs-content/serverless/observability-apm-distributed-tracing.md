# Distributed tracing [observability-apm-distributed-tracing]

A `trace` is a group of [transactions](../../../solutions/observability/apps/learn-about-application-data-types.md) and [spans](../../../solutions/observability/apps/learn-about-application-data-types.md) with a common root. Each `trace` tracks the entirety of a single request. When a `trace` travels through multiple services, as is common in a microservice architecture, it is known as a distributed trace.


## Why is distributed tracing important? [observability-apm-distributed-tracing-why-is-distributed-tracing-important]

Distributed tracing enables you to analyze performance throughout your microservice architecture by tracing the entirety of a request — from the initial web request on your front-end service all the way to database queries made on your back-end services.

Tracking requests as they propagate through your services provides an end-to-end picture of where your application is spending time, where errors are occurring, and where bottlenecks are forming. Distributed tracing eliminates individual service’s data silos and reveals what’s happening outside of service borders.

For supported technologies, distributed tracing works out-of-the-box, with no additional configuration required.


## How distributed tracing works [observability-apm-distributed-tracing-how-distributed-tracing-works]

Distributed tracing works by injecting a custom `traceparent` HTTP header into outgoing requests. This header includes information, like `trace-id`, which is used to identify the current trace, and `parent-id`, which is used to identify the parent of the current span on incoming requests or the current span on an outgoing request.

When a service is working on a request, it checks for the existence of this HTTP header. If it’s missing, the service starts a new trace. If it exists, the service ensures the current action is added as a child of the existing trace, and continues to propagate the trace.


### Trace propagation examples [observability-apm-distributed-tracing-trace-propagation-examples]

In this example, Elastic’s Ruby agent communicates with Elastic’s Java agent. Both support the `traceparent` header, and trace data is successfully propagated.

:::{image} ../../../images/serverless-dt-trace-ex1.png
:alt: How traceparent propagation works
:class: screenshot
:::

In this example, Elastic’s Ruby agent communicates with OpenTelemetry’s Java agent. Both support the `traceparent` header, and trace data is successfully propagated.

:::{image} ../../../images/serverless-dt-trace-ex2.png
:alt: How traceparent propagation works
:class: screenshot
:::

In this example, the trace meets a piece of middleware that doesn’t propagate the `traceparent` header. The distributed trace ends and any further communication will result in a new trace.

:::{image} ../../../images/serverless-dt-trace-ex3.png
:alt: How traceparent propagation works
:class: screenshot
:::


### W3C Trace Context specification [observability-apm-distributed-tracing-w3c-trace-context-specification]

All Elastic agents now support the official W3C Trace Context specification and `traceparent` header. See the table below for the minimum required agent version:

| Agent name | Agent Version |
| --- | --- |
| **Go Agent** | ≥`1.6` |
| **Java Agent** | ≥`1.14` |
| **.NET Agent** | ≥`1.3` |
| **Node.js Agent** | ≥`3.4` |
| **PHP Agent** | ≥`1.0` |
| **Python Agent** | ≥`5.4` |
| **Ruby Agent** | ≥`3.5` |

::::{note}
Older Elastic agents use a unique `elastic-apm-traceparent` header. For backward-compatibility purposes, new versions of Elastic agents still support this header.

::::



## Visualize distributed tracing [observability-apm-distributed-tracing-visualize-distributed-tracing]

APM’s timeline visualization provides a visual deep-dive into each of your application’s traces:

:::{image} ../../../images/serverless-apm-distributed-tracing.png
:alt: Example view of the distributed tracing in Elastic APM
:class: screenshot
:::


## Manual distributed tracing [observability-apm-distributed-tracing-manual-distributed-tracing]

Elastic agents automatically propagate distributed tracing context for supported technologies. If your service communicates over a different, unsupported protocol, you can manually propagate distributed tracing context from a sending service to a receiving service with each agent’s API.


### Add the `traceparent` header to outgoing requests [observability-apm-distributed-tracing-add-the-traceparent-header-to-outgoing-requests]

Sending services must add the `traceparent` header to outgoing requests.

:::::::{tab-set}

::::::{tab-item} Go
1. Start a transaction with [`StartTransaction`](https://www.elastic.co/guide/en/apm/agent/go/current/api.html#tracer-api-start-transaction) or a span with [`StartSpan`](https://www.elastic.co/guide/en/apm/agent/go/current/api.html#transaction-start-span).
2. Get the active `TraceContext`.
3. Send the `TraceContext` to the receiving service.

Example:

```go
transaction := apm.DefaultTracer.StartTransaction("GET /", "request")   <1>
traceContext := transaction.TraceContext()   <2>

// Send TraceContext to receiving service
traceparent := apmhttp.FormatTraceparentHeader(traceContext))   <3>
tracestate := traceContext.State.String()
```

1. Start a transaction
2. Get `TraceContext` from current Transaction
3. Format the `TraceContext` or `tracestate` as a `traceparent` header.
::::::

::::::{tab-item} Java
1. Start a transaction with [`startTransaction`](https://www.elastic.co/guide/en/apm/agent/java/current/public-api.html#api-start-transaction), or a span with [`startSpan`](https://www.elastic.co/guide/en/apm/agent/java/current/public-api.html#api-span-start-span).
2. Inject the `traceparent` header into the request object with [`injectTraceHeaders`](https://www.elastic.co/guide/en/apm/agent/java/current/public-api.html#api-transaction-inject-trace-headers)

Example of manually instrumenting an RPC framework:

```java
// Hook into a callback provided by the RPC framework that is called on outgoing requests
public Response onOutgoingRequest(Request request) throws Exception {
  Span span = ElasticApm.currentSpan()   <1>
          .startSpan("external", "http", null)
          .setName(request.getMethod() + " " + request.getHost());
  try (final Scope scope = transaction.activate()) {
      span.injectTraceHeaders((name, value) -> request.addHeader(name, value));   <2>
      return request.execute();
  } catch (Exception e) {
      span.captureException(e);
      throw e;
  } finally {
      span.end();   <3>
  }
}
```

1. Create a span representing an external call
2. Inject the `traceparent` header into the request object
3. End the span
::::::

::::::{tab-item} .NET
1. Serialize the distributed tracing context of the active transaction or span with [`CurrentTransaction`](https://www.elastic.co/guide/en/apm/agent/dotnet/current/public-api.html#api-current-transaction) or [`CurrentSpan`](https://www.elastic.co/guide/en/apm/agent/dotnet/current/public-api.html#api-current-span).
2. Send the serialized context the receiving service.

Example:

```csharp
string outgoingDistributedTracingData =
    (Agent.Tracer.CurrentSpan?.OutgoingDistributedTracingData
        ?? Agent.Tracer.CurrentTransaction?.OutgoingDistributedTracingData)?.SerializeToString();
// Now send `outgoingDistributedTracingData` to the receiving service
```
::::::

::::::{tab-item} Node.js
1. Start a transaction with [`apm.startTransaction()`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/agent-api.html#apm-start-transaction), or a span with [`apm.startSpan()`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/agent-api.html#apm-start-span).
2. Get the serialized `traceparent` string of the started transaction/span with [`currentTraceparent`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/agent-api.html#apm-current-traceparent).
3. Encode the `traceparent` and send it to the receiving service inside your regular request.

Example using raw UDP to communicate between two services, A and B:

```js
agent.startTransaction('my-service-a-transaction');   <1>
const traceparent = agent.currentTraceparent;   <2>
sendMetadata(`traceparent: ${traceparent}\n`);   <3>
```

1. Start a transaction
2. Get the current `traceparent`
3. Send the `traceparent` as a header to service B.
::::::

::::::{tab-item} PHP
1. On the client side (i.e., the side sending the request) get the current distributed tracing context.
2. Serialize the current distributed tracing context to a format supported by the request’s transport and send it to the server side (i.e., the side receiving the request).

Example:

```php
$distDataAsString = ElasticApm::getSerializedCurrentDistributedTracingData();   <1>
```

1. Get the current distributed tracing data serialized as string
::::::

::::::{tab-item} Python
1. Start a transaction with [`begin_transaction()`](https://www.elastic.co/guide/en/apm/agent/python/current/api.html#client-api-begin-transaction).
2. Get the `trace_parent` of the active transaction.
3. Send the `trace_parent` to the receiving service.

Example:

```python
client.begin_transaction('new-transaction')  <1>

elasticapm.get_trace_parent_header('new-transaction')   <2>

# Send `trace_parent_str` to another service
```

1. Start a new transaction
2. Return the string representation of the current transaction’s `TraceParent` object
::::::

::::::{tab-item} Ruby
1. Start a span with [`with_span`](https://www.elastic.co/guide/en/apm/agent/ruby/current/api.html#api-agent-with_span).
2. Get the active `TraceContext`.
3. Send the `TraceContext` to the receiving service.

Example:

```ruby
ElasticAPM.with_span "Name" do |span|   <1>
  header = span.trace_context.traceparent.to_header   <2>
  # send the TraceContext Header to a receiving service...
end
```

1. Start a span
2. Get the `TraceContext`
::::::

:::::::

### Parse the `traceparent` header on incoming requests [distributed-tracing-incoming]

Receiving services must parse the incoming `traceparent` header, and start a new transaction or span as a child of the received context.

:::::::{tab-set}

::::::{tab-item} Go
1. Parse the incoming `TraceContext` with [`ParseTraceparentHeader`](https://godoc.org/go.elastic.co/apm/module/apmhttp#ParseTraceparentHeader) or [`ParseTracestateHeader`](https://godoc.org/go.elastic.co/apm/module/apmhttp#ParseTracestateHeader).
2. Start a new transaction or span as a child of the incoming transaction with [`StartTransactionOptions`](https://www.elastic.co/guide/en/apm/agent/go/current/api.html#tracer-api-start-transaction-options) or [`StartSpanOptions`](https://www.elastic.co/guide/en/apm/agent/go/current/api.html#transaction-start-span-options).

Example:

```go
// Receive incoming TraceContext
traceContext, _ := apmhttp.ParseTraceparentHeader(r.Header.Get("Traceparent"))   <1>
traceContext.State, _ = apmhttp.ParseTracestateHeader(r.Header["Tracestate"]...)   <2>

opts := apm.TransactionOptions{
&#x9;TraceContext: traceContext,   <3>
}
transaction := apm.DefaultTracer.StartTransactionOptions("GET /", "request", opts)   <4>
```

1. Parse the `TraceParent` header
2. Parse the `Tracestate` header
3. Set the parent trace context
4. Start a new transaction as a child of the received `TraceContext`
::::::

::::::{tab-item} Java
1. Create a transaction as a child of the incoming transaction with [`startTransactionWithRemoteParent()`](https://www.elastic.co/guide/en/apm/agent/java/current/public-api.html#api-transaction-inject-trace-headers).
2. Start and name the transaction with [`activate()`](https://www.elastic.co/guide/en/apm/agent/java/current/public-api.html#api-transaction-activate) and [`setName()`](https://www.elastic.co/guide/en/apm/agent/java/current/public-api.html#api-set-name).

Example:

```java
// Hook into a callback provided by the framework that is called on incoming requests
public Response onIncomingRequest(Request request) throws Exception {
    // creates a transaction representing the server-side handling of the request
    Transaction transaction = ElasticApm.startTransactionWithRemoteParent(request::getHeader, request::getHeaders);   <1>
    try (final Scope scope = transaction.activate()) {   <2>
        String name = "a useful name like ClassName#methodName where the request is handled";
        transaction.setName(name);   <3>
        transaction.setType(Transaction.TYPE_REQUEST);   <4>
        return request.handle();
    } catch (Exception e) {
        transaction.captureException(e);
        throw e;
    } finally {
        transaction.end();   <5>
    }
}
```

1. Create a transaction as the child of a remote parent
2. Activate the transaction
3. Name the transaction
4. Add a transaction type
5. Eventually, end the transaction
::::::

::::::{tab-item} .NET
Deserialize the incoming distributed tracing context, and pass it to any of the [`StartTransaction`](https://www.elastic.co/guide/en/apm/agent/dotnet/current/public-api.html#api-start-transaction) or [`CaptureTransaction`](https://www.elastic.co/guide/en/apm/agent/dotnet/current/public-api.html#convenient-capture-transaction) APIs — all of which have an optional `DistributedTracingData` parameter. This will create a new transaction or span as a child of the incoming trace context.

Example starting a new transaction:

```csharp
var transaction2 = Agent.Tracer.StartTransaction("Transaction2", "TestTransaction",
     DistributedTracingData.TryDeserializeFromString(serializedDistributedTracingData));
```
::::::

::::::{tab-item} Node.js
1. Decode and store the `traceparent` in the receiving service.
2. Pass in the `traceparent` as the `childOf` option to manually start a new transaction as a child of the received `traceparent` with [`apm.startTransaction()`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/agent-api.html#apm-start-transaction).

Example receiving a `traceparent` over raw UDP:

```js
const traceparent = readTraceparentFromUDPPacket()   <1>
agent.startTransaction('my-service-b-transaction', { childOf: traceparent })   <2>
```

1. Read the `traceparent` from the incoming request.
2. Use the `traceparent` to initialize a new transaction that is a child of the original `traceparent`.
::::::

::::::{tab-item} PHP
1. Receive the distributed tracing data on the server side.
2. Begin a new transaction using the agent’s public API. For example, use [`ElasticApm::beginCurrentTransaction`](https://www.elastic.co/guide/en/apm/agent/php/current/public-api.html#api-elasticapm-class-begin-current-transaction) and pass the received distributed tracing data (serialized as string) as a parameter. This will create a new transaction as a child of the incoming trace context.
3. Don’t forget to eventually end the transaction on the server side.

Example:

```php
$receiverTransaction = ElasticApm::beginCurrentTransaction(   <1>
    'GET /data-api',
    'data-layer',
    /* timestamp */ null,
    $distDataAsString   <2>
);
```

1. Start a new transaction
2. Pass in the received distributed tracing data (serialized as string)


Once this new transaction has been created in the receiving service, you can create child spans, or use any other agent API methods as you typically would.
::::::

::::::{tab-item} Python
1. Create a `TraceParent` object from a string or HTTP header.
2. Start a new transaction as a child of the `TraceParent` by passing in a `TraceParent` object.

Example using HTTP headers:

```python
parent = elasticapm.trace_parent_from_headers(headers_dict)   <1>
client.begin_transaction('processors', trace_parent=parent)   <2>
```

1. Create a `TraceParent` object from HTTP headers formed as a dictionary
2. Begin a new transaction as a child of the received `TraceParent`


::::{tip}
See the [`TraceParent` API](https://www.elastic.co/guide/en/apm/agent/python/current/api.html#traceparent-api) for additional examples.

::::
::::::

::::::{tab-item} Ruby
Start a new transaction or span as a child of the incoming transaction or span with [`with_transaction`](https://www.elastic.co/guide/en/apm/agent/ruby/current/api.html#api-agent-with_transaction) or [`with_span`](https://www.elastic.co/guide/en/apm/agent/ruby/current/api.html#api-agent-with_span).

Example:

```ruby
# env being a Rack env
context = ElasticAPM::TraceContext.parse(env: env)   <1>

ElasticAPM.with_transaction("Do things", trace_context: context) do   <2>
  ElasticAPM.with_span("Do nested thing", trace_context: context) do   <3>
  end
end
```

1. Parse the incoming `TraceContext`
2. Create a transaction as a child of the incoming `TraceContext`
3. Create a span as a child of the newly created transaction. `trace_context` is optional here, as spans are automatically created as a child of their parent’s transaction’s `TraceContext` when none is passed.
::::::

:::::::
