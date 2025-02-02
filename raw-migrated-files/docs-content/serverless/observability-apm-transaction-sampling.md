# Transaction sampling [observability-apm-transaction-sampling]

[Distributed tracing](../../../solutions/observability/apps/traces.md) can generate a substantial amount of data. More data can mean higher costs and more noise. Sampling aims to lower the amount of data ingested and the effort required to analyze that data — all while still making it easy to find anomalous patterns in your applications, detect outages, track errors, and lower mean time to recovery (MTTR).


## Head-based sampling [observability-apm-transaction-sampling-head-based-sampling]

In head-based sampling, the sampling decision for each trace is made when the trace is initiated. Each trace has a defined and equal probability of being sampled.

For example, a sampling value of `.2` indicates a transaction sample rate of `20%`. This means that only `20%` of traces will send and retain all of their associated information. The remaining traces will drop contextual information to reduce the transfer and storage size of the trace.

Head-based sampling is quick and easy to set up. Its downside is that it’s entirely random — interesting data might be discarded purely due to chance.


### Distributed tracing [observability-apm-transaction-sampling-distributed-tracing]

In a *distributed* trace, the sampling decision is still made when the trace is initiated. Each subsequent service respects the initial service’s sampling decision, regardless of its configured sample rate; the result is a sampling percentage that matches the initiating service.

In the example in *Figure 1*, `Service A` initiates four transactions and has a sample rate of `.5` (`50%`). The upstream sampling decision is respected, so even if the sample rate is defined and is a different value in `Service B` and `Service C`, the sample rate will be `.5` (`50%`) for all services.

**Figure 1. Upstream sampling decision is respected**

:::{image} ../../../images/serverless-apm-dt-sampling-example-1.png
:alt: Distributed tracing and head based sampling example one
:class: screenshot
:::

In the example in *Figure 2*, `Service A` initiates four transactions and has a sample rate of `1` (`100%`). Again, the upstream sampling decision is respected, so the sample rate for all services will be `1` (`100%`).

**Figure 2. Upstream sampling decision is respected**

:::{image} ../../../images/serverless-apm-dt-sampling-example-2.png
:alt: Distributed tracing and head based sampling example two
:class: screenshot
:::


### Trace continuation strategies with distributed tracing [observability-apm-transaction-sampling-trace-continuation-strategies-with-distributed-tracing]

In addition to setting the sample rate, you can also specify which *trace continuation strategy* to use. There are three trace continuation strategies: `continue`, `restart`, and `restart_external`.

The **`continue`** trace continuation strategy is the default and will behave similar to the examples in the [Distributed tracing section](../../../solutions/observability/apps/transaction-sampling.md#observability-apm-transaction-sampling-distributed-tracing).

Use the **`restart_external`** trace continuation strategy on an Elastic-monitored service to start a new trace if the previous service did not have a `traceparent` header with `es` vendor data. This can be helpful if a transaction includes an Elastic-monitored service that is receiving requests from an unmonitored service.

In the example in *Figure 3*, `Service A` is an Elastic-monitored service that initiates four transactions with a sample rate of `.25` (`25%`). Because `Service B` is unmonitored, the traces started in `Service A` will end there. `Service C` is an Elastic-monitored service that initiates four transactions that start new traces with a new sample rate of `.5` (`50%`). Because `Service D` is also Elastic-monitored service, the upstream sampling decision defined in `Service C` is respected. The end result will be three sampled traces.

**Figure 3. Using the `restart_external` trace continuation strategy**

:::{image} ../../../images/serverless-apm-dt-sampling-continuation-strategy-restart_external.png
:alt: Distributed tracing and head based sampling with restart_external continuation strategy
:class: screenshot
:::

Use the **`restart`** trace continuation strategy on an Elastic-monitored service to start a new trace regardless of whether the previous service had a `traceparent` header. This can be helpful if an Elastic-monitored service is publicly exposed, and you do not want tracing data to possibly be spoofed by user requests.

In the example in *Figure 4*, `Service A` and `Service B` are Elastic-monitored services that use the default trace continuation strategy. `Service A` has a sample rate of `.25` (`25%`), and that sampling decision is respected in `Service B`. `Service C` is an Elastic-monitored service that uses the `restart` trace continuation strategy and has a sample rate of `1` (`100%`). Because it uses `restart`, the upstream sample rate is *not* respected in `Service C` and all four traces will be sampled as new traces in `Service C`. The end result will be five sampled traces.

**Figure 4. Using the `restart` trace continuation strategy**

:::{image} ../../../images/serverless-apm-dt-sampling-continuation-strategy-restart.png
:alt: Distributed tracing and head based sampling with restart continuation strategy
:class: screenshot
:::


### OpenTelemetry [observability-apm-transaction-sampling-opentelemetry]

Head-based sampling is implemented directly in the APM agents and SDKs. The sample rate must be propagated between services and the managed intake service in order to produce accurate metrics.

OpenTelemetry offers multiple samplers. However, most samplers do not propagate the sample rate. This results in inaccurate span-based metrics, like APM throughput, latency, and error metrics.

For accurate span-based metrics when using head-based sampling with OpenTelemetry, you must use a [consistent probability sampler](https://opentelemetry.io/docs/specs/otel/trace/tracestate-probability-sampling/). These samplers propagate the sample rate between services and the managed intake service, resulting in accurate metrics.

::::{note}
OpenTelemetry does not offer consistent probability samplers in all languages. Refer to the documentation of your favorite OpenTelemetry agent or SDK for more information.

::::



## Sampled data and visualizations [observability-apm-transaction-sampling-sampled-data-and-visualizations]

A sampled trace retains all data associated with it. A non-sampled trace drops all [span](../../../solutions/observability/apps/learn-about-application-data-types.md) and [transaction](../../../solutions/observability/apps/learn-about-application-data-types.md) data. Regardless of the sampling decision, all traces retain [error](../../../solutions/observability/apps/learn-about-application-data-types.md) data.

Some visualizations in the Applications UI, like latency, are powered by aggregated transaction and span [metrics](../../../solutions/observability/apps/learn-about-application-data-types.md). Metrics are based on sampled traces and weighted by the inverse sampling rate. For example, if you sample at 5%, each trace is counted as 20. As a result, as the variance of latency increases, or the sampling rate decreases, your level of error will increase.


## Sample rates [observability-apm-transaction-sampling-sample-rates]

What’s the best sampling rate? Unfortunately, there isn’t one. Sampling is dependent on your data, the throughput of your application, data retention policies, and other factors. A sampling rate from `.1%` to `100%` would all be considered normal. You’ll likely decide on a unique sample rate for different scenarios. Here are some examples:

* Services with considerably more traffic than others might be safe to sample at lower rates
* Routes that are more important than others might be sampled at higher rates
* A production service environment might warrant a higher sampling rate than a development environment
* Failed trace outcomes might be more interesting than successful traces — thus requiring a higher sample rate

Regardless of the above, cost conscious customers are likely to be fine with a lower sample rate.


## Configure head-based sampling [observability-apm-transaction-sampling-configure-head-based-sampling]

Each APM agent provides a configuration value used to set the transaction sample rate. Refer to the relevant agent’s documentation for more details:

* Go: [`ELASTIC_APM_TRANSACTION_SAMPLE_RATE`](https://www.elastic.co/guide/en/apm/agent/go/{{apm-go-branch}}/configuration.html#config-transaction-sample-rate)
* Java: [`transaction_sample_rate`](https://www.elastic.co/guide/en/apm/agent/java/{{apm-java-branch}}/config-core.html#config-transaction-sample-rate)
* .NET: [`TransactionSampleRate`](https://www.elastic.co/guide/en/apm/agent/dotnet/{{apm-dotnet-branch}}/config-core.html#config-transaction-sample-rate)
* Node.js: [`transactionSampleRate`](https://www.elastic.co/guide/en/apm/agent/nodejs/{{apm-node-branch}}/configuration.html#transaction-sample-rate)
* PHP: [`transaction_sample_rate`](https://www.elastic.co/guide/en/apm/agent/php/current/configuration-reference.html#config-transaction-sample-rate)
* Python: [`transaction_sample_rate`](https://www.elastic.co/guide/en/apm/agent/python/{{apm-py-branch}}/configuration.html#config-transaction-sample-rate)
* Ruby: [`transaction_sample_rate`](https://www.elastic.co/guide/en/apm/agent/ruby/{{apm-ruby-branch}}/configuration.html#config-transaction-sample-rate)

Each APM agent provides a configuration value used to set the transaction sample rate. Refer to the relevant agent’s documentation for more details:

* Go: [`ELASTIC_APM_TRANSACTION_SAMPLE_RATE`](https://www.elastic.co/guide/en/apm/agent/go/{{apm-go-branch}}/configuration.html#config-transaction-sample-rate)
* Java: [`transaction_sample_rate`](https://www.elastic.co/guide/en/apm/agent/java/{{apm-java-branch}}/config-core.html#config-transaction-sample-rate)
* .NET: [`TransactionSampleRate`](https://www.elastic.co/guide/en/apm/agent/dotnet/{{apm-dotnet-branch}}/config-core.html#config-transaction-sample-rate)
* Node.js: [`transactionSampleRate`](https://www.elastic.co/guide/en/apm/agent/nodejs/{{apm-node-branch}}/configuration.html#transaction-sample-rate)
* PHP: [`transaction_sample_rate`](https://www.elastic.co/guide/en/apm/agent/php/current/configuration-reference.html#config-transaction-sample-rate)
* Python: [`transaction_sample_rate`](https://www.elastic.co/guide/en/apm/agent/python/{{apm-py-branch}}/configuration.html#config-transaction-sample-rate)
* Ruby: [`transaction_sample_rate`](https://www.elastic.co/guide/en/apm/agent/ruby/{{apm-ruby-branch}}/configuration.html#config-transaction-sample-rate)
