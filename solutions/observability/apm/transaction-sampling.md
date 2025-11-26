---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-sampling.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-transaction-sampling.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Transaction sampling [apm-sampling]

:::{include} _snippets/apm-server-vs-mis.md
:::

[Distributed tracing](/solutions/observability/apm/traces.md) can generate a substantial amount of data. More data can mean higher costs and more noise. Sampling aims to lower the amount of data ingested and the effort required to analyze that data — all while still making it easy to find anomalous patterns in your applications, detect outages, track errors, and lower mean time to recovery (MTTR).

Elastic APM supports two types of sampling:

% Stateful only for Tail-based sampling

* [Head-based sampling](/solutions/observability/apm/transaction-sampling.md#apm-head-based-sampling)
* [Tail-based sampling](/solutions/observability/apm/transaction-sampling.md#apm-tail-based-sampling)

## Head-based sampling [apm-head-based-sampling]

```{applies_to}
stack: ga
serverless: ga
```

In head-based sampling, the sampling decision for each trace is made when the trace is initiated. Each trace has a defined and equal probability of being sampled.

For example, a sampling value of `.2` indicates a transaction sample rate of `20%`. This means that only `20%` of traces will send and retain all of their associated information. The remaining traces will drop contextual information to reduce the transfer and storage size of the trace.

Head-based sampling is quick and easy to set up. Its downside is that it’s entirely random — interesting data might be discarded purely due to chance.

See [Configure head-based sampling](/solutions/observability/apm/transaction-sampling.md#apm-configure-head-based-sampling) to get started.

### Distributed tracing [distributed-tracing-examples]

In a distributed trace, the sampling decision is still made when the trace is initiated. Each subsequent service respects the initial service’s sampling decision, regardless of its configured sample rate; the result is a sampling percentage that matches the initiating service.

In the example in *Figure 1*, `Service A` initiates four transactions and has sample rate of `.5` (`50%`). The upstream sampling decision is respected, so even if the sample rate is defined and is a different value in `Service B` and `Service C`, the sample rate will be `.5` (`50%`) for all services.

**Figure 1. Upstream sampling decision is respected**

:::{image} /solutions/images/observability-dt-sampling-example-1.png
:alt: Distributed tracing and head based sampling example one
:screenshot:
:::

In the example in *Figure 2*, `Service A` initiates four transactions and has a sample rate of `1` (`100%`). Again, the upstream sampling decision is respected, so the sample rate for all services will be `1` (`100%`).

**Figure 2. Upstream sampling decision is respected**

:::{image} /solutions/images/observability-dt-sampling-example-2.png
:alt: Distributed tracing and head based sampling example two
:screenshot:
:::

#### Trace continuation strategies with distributed tracing [_trace_continuation_strategies_with_distributed_tracing]

In addition to setting the sample rate, you can also specify which *trace continuation strategy* to use. There are three trace continuation strategies: `continue`, `restart`, and `restart_external`.

The **`continue`** trace continuation strategy is the default and will behave similar to the examples in the [Distributed tracing section](/solutions/observability/apm/transaction-sampling.md#distributed-tracing-examples).

Use the **`restart_external`** trace continuation strategy on an Elastic-monitored service to start a new trace if the previous service did not have a `traceparent` header with `es` vendor data. This can be helpful if a transaction includes an Elastic-monitored service that is receiving requests from an unmonitored service.

In the example in *Figure 3*, `Service A` is an Elastic-monitored service that initiates four transactions with a sample rate of `.25` (`25%`). Because `Service B` is unmonitored, the traces started in `Service A` will end there. `Service C` is an Elastic-monitored service that initiates four transactions that start new traces with a new sample rate of `.5` (`50%`). Because `Service D` is also Elastic-monitored service, the upstream sampling decision defined in `Service C` is respected. The end result will be three sampled traces.

**Figure 3. Using the `restart_external` trace continuation strategy**

:::{image} /solutions/images/observability-dt-sampling-continuation-strategy-restart_external.png
:alt: Distributed tracing and head based sampling with restart_external continuation strategy
:screenshot:
:::

Use the **`restart`** trace continuation strategy on an Elastic-monitored service to start a new trace regardless of whether the previous service had a `traceparent` header. This can be helpful if an Elastic-monitored service is publicly exposed, and you do not want tracing data to possibly be spoofed by user requests.

In the example in *Figure 4*, `Service A` and `Service B` are Elastic-monitored services that use the default trace continuation strategy. `Service A` has a sample rate of `.25` (`25%`), and that sampling decision is respected in `Service B`. `Service C` is an Elastic-monitored service that uses the `restart` trace continuation strategy and has a sample rate of `1` (`100%`). Because it uses `restart`, the upstream sample rate is *not* respected in `Service C` and all four traces will be sampled as new traces in `Service C`. The end result will be five sampled traces.

:::{image} /solutions/images/observability-dt-sampling-continuation-strategy-restart.png
:alt: Distributed tracing and head based sampling with restart continuation strategy
:title: Using the `restart` trace continuation strategy
:::

### OpenTelemetry [_opentelemetry]

Head-based sampling is implemented directly in the APM agents and SDKs. The sample rate must be propagated between services and the managed intake service in order to produce accurate metrics.

OpenTelemetry offers multiple samplers. However, most samplers do not propagate the sample rate. This results in inaccurate span-based metrics, like APM throughput, latency, and error metrics.

For accurate span-based metrics when using head-based sampling with OpenTelemetry, you must use a [consistent probability sampler](https://opentelemetry.io/docs/specs/otel/trace/tracestate-probability-sampling/). These samplers propagate the sample rate between services and the managed intake service, resulting in accurate metrics.

::::{note}
OpenTelemetry does not offer consistent probability samplers in all languages. OpenTelemetry users should consider using tail-based sampling instead.

Refer to the documentation of your favorite OpenTelemetry agent or SDK for more information on the availability of consistent probability samplers.

::::

% Stateful only for tail-based sampling

## Tail-based sampling [apm-tail-based-sampling]

```{applies_to}
stack: ga
serverless: unavailable
```

::::{note}
**Support for tail-based sampling**

Tail-based sampling is only supported when writing to {{es}}. If you are using a different [output](/solutions/observability/apm/apm-server/configure-output.md), tail-based sampling is *not* supported.
::::

In tail-based sampling, the sampling decision for each trace is made after the trace has completed. This means all traces will be analyzed against a set of rules, or policies, which will determine the rate at which they are sampled.

Unlike head-based sampling, each trace does not have an equal probability of being sampled. Because slower traces are more interesting than faster ones, tail-based sampling uses weighted random sampling — so traces with a longer root transaction duration are more likely to be sampled than traces with a fast root transaction duration.

A downside of tail-based sampling is that it results in more data being sent from APM agents to the APM Server. The APM Server will therefore use more CPU, memory, and disk than with head-based sampling. However, because the tail-based sampling decision happens in APM Server, there is less data to transfer from APM Server to {{es}}. So running APM Server close to your instrumented services can reduce any increase in transfer costs that tail-based sampling brings.

See [Configure tail-based sampling](/solutions/observability/apm/transaction-sampling.md#apm-configure-tail-based-sampling) to get started.

### Distributed tracing with tail-based sampling [_distributed_tracing_with_tail_based_sampling]

With tail-based sampling, all traces are observed and a sampling decision is only made once a trace completes.

In this example, `Service A` initiates four transactions. If our sample rate is `.5` (`50%`) for traces with a `success` outcome, and `1` (`100%`) for traces with a `failure` outcome, the sampled traces would look something like this:

:::{image} /solutions/images/observability-dt-sampling-example-3.png
:alt: Distributed tracing and tail based sampling example one
:::

### OpenTelemetry with tail-based sampling [_opentelemetry_with_tail_based_sampling]

Tail-based sampling is implemented entirely in APM Server, and will work with traces sent by either Elastic APM agents or OpenTelemetry SDKs.

Due to [OpenTelemetry tail-based sampling limitations](/solutions/observability/apm/opentelemetry/limitations.md#apm-open-telemetry-tbs) when using [tailsamplingprocessor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor), we recommend using APM Server tail-based sampling instead.

### Tail-based sampling performance and requirements [_tail_based_sampling_performance_and_requirements]

Tail-based sampling (TBS), by definition, requires storing events locally temporarily, such that they can be retrieved and forwarded when a sampling decision is made.

In an APM Server implementation, the events are stored temporarily on disk instead of in memory for better scalability. Therefore, it requires local disk storage proportional to the APM event ingestion rate and additional memory to facilitate disk reads and writes. If the [storage limit](/solutions/observability/apm/apm-server/tail-based-sampling.md#sampling-tail-storage_limit-ref) is insufficient, trace events are indexed or discarded based on the [discard on write failure](/solutions/observability/apm/apm-server/tail-based-sampling.md#sampling-tail-discard-on-write-failure-ref) configuration.

It is recommended to use fast disks, ideally Solid State Drives (SSD) with high I/O per second (IOPS), when enabling tail-based sampling. Disk throughput and I/O may become performance bottlenecks for tail-based sampling and APM event ingestion overall. Disk writes are proportional to the event ingest rate, while disk reads are proportional to both the event ingest rate and the sampling rate.

To demonstrate the performance overhead and requirements, here are some reference numbers from a standalone APM Server deployed on AWS EC2 under full load that is receiving APM events containing only traces. These numbers assume no backpressure from Elasticsearch, a **uniform 10% sample rate in the tail sampling policy**, events being sent from 1024 agents concurrently, and sufficient disk space.

:::{important}
These figures are for reference only and may vary depending on factors such as sampling rate, average event size, and the average number of events per distributed trace.
:::

Terminology:

* Event Ingestion Rate: The throughput from the APM agent to the APM Server using the Intake v2 protocol (the protocol used by Elastic APM agents), measured in events per second.
* Event Indexing Rate: The throughput from the APM Server to Elasticsearch, measured in events per second or documents per second. Note that it should roughly be equal to Event Ingestion Rate * Sampling Rate.
* Memory Usage: The maximum Resident Set Size (RSS) of APM Server process observed throughout the benchmark.
* TBS: Tail-based sampling.
* IOPS: Input/Output Operations Per Second, which is a measure of disk performance.

#### APM Server 9.2

| EC2 instance size | TBS and disk configuration                     | Event ingestion rate (events/s) | Event indexing rate (events/s) | Memory usage (GB) | Disk usage (GB) |
|-------------------|------------------------------------------------|---------------------------------|--------------------------------|-------------------|-----------------|
| c6gd.2xlarge      | TBS disabled                                   | 45120                           | 45120 (100% sampling)          | 0.95              | 0               |
| c6gd.2xlarge      | TBS enabled, EBS gp3 volume with 3000 IOPS     | 17120                           | 1527                           | 1.48              | 11.3            |
| c6gd.2xlarge      | TBS enabled, local NVMe SSD from c6gd instance | 19490                           | 1661                           | 1.48              | 12.3            |
| c6gd.4xlarge      | TBS disabled                                   | 63460                           | 63460 (100% sampling)          | 1.45              | 0               |
| c6gd.4xlarge      | TBS enabled, EBS gp3 volume with 3000 IOPS     | 26340                           | 2248                           | 2.09              | 17.8            |
| c6gd.4xlarge      | TBS enabled, local NVMe SSD from c6gd instance | 36620                           | 3041                           | 2.22              | 21.8            |
| c6gd.8xlarge      | TBS disabled                                   | 119800                          | 119800 (100% sampling)         | 1.44              | 0               |
| c6gd.8xlarge      | TBS enabled, EBS gp3 volume with 3000 IOPS     | 27620                           | 2485                           | 2.49              | 16.6            |
| c6gd.8xlarge      | TBS enabled, local NVMe SSD from c6gd instance | 46260                           | 3909                           | 2.43              | 25.8            |

#### APM Server 8.19

| EC2 instance size | TBS and disk configuration                     | Event ingestion rate (events/s) | Event indexing rate (events/s) | Memory usage (GB) | Disk usage (GB) |
|-------------------|------------------------------------------------|---------------------------------|--------------------------------|-------------------|-----------------|
| c6gd.2xlarge      | TBS disabled                                   | 45480                           | 45480 (100% sampling)          | 0.95              | 0               |
| c6gd.2xlarge      | TBS enabled, EBS gp3 volume with 3000 IOPS     | 11420                           | 11.55                          | 5.92              | 30.81           |
| c6gd.2xlarge      | TBS enabled, local NVMe SSD from c6gd instance | 12630                           | 86.52                          | 5.82              | 27.70           |
| c6gd.4xlarge      | TBS disabled                                   | 61900                           | 61900 (100% sampling)          | 1.45              | 0               |
| c6gd.4xlarge      | TBS enabled, EBS gp3 volume with 3000 IOPS     | 12920                           | 37.31                          | 11.31             | 30.98           |
| c6gd.4xlarge      | TBS enabled, local NVMe SSD from c6gd instance | 23300                           | 574                            | 13.31             | 50.99           |
| c6gd.8xlarge      | TBS disabled                                   | 122800                          | 122800 (100% sampling)         | 1.45              | 0               |
| c6gd.8xlarge      | TBS enabled, EBS gp3 volume with 3000 IOPS     | 13280                           | 34.20                          | 22.61             | 32.01           |
| c6gd.8xlarge      | TBS enabled, local NVMe SSD from c6gd instance | 35810                           | 2480                           | 30.41             | 86.86           |

When interpreting these numbers, note that:

* The metrics are inter-related. For example, it is reasonable to see higher memory usage and disk usage when the event ingestion rate is higher.
* Under normal operation, the event indexing rate divided by the event ingestion rate should approximate the configured sampling rate (10% in this case). However, in the version 8.19 numbers above, as APM Server is under full load, sampling decision handling lags behind due to disk read operations that compete with ingest path writes for disk I/O resources, resulting in a significantly lower event indexing rate than expected.
* Memory usage measurements differ between versions: version 9.2 numbers reflect only the APM Server process RSS (excluding OS cache), while version 8.19 numbers include OS cache because the database is memory-mapped. Despite this measurement difference, version 9.0+ typically uses less memory overall due to its significantly smaller database footprint.

The tail-based sampling implementation in version 9.0 offers significantly better performance compared to version 8.18, primarily due to a rewritten storage layer. This new implementation compresses data, as well as cleans up expired data more reliably, resulting in reduced load on disk, memory, and compute resources. This improvement is particularly evident in the event indexing rate on slower disks. In version 8.18, as the database grows larger, the performance slowdown can become disproportionate.

## Sampled data and visualizations [_sampled_data_and_visualizations]

```{applies_to}
stack: ga
serverless: ga
```

A sampled trace retains all data associated with it. A non-sampled trace drops all [span](/solutions/observability/apm/spans.md) and [transaction](/solutions/observability/apm/transactions.md) data.[^1^](#footnote-1) Regardless of the sampling decision, all traces retain [error](/solutions/observability/apm/errors.md) data.

Some visualizations in the {{apm-app}}, like latency, are powered by aggregated transaction and span [metrics](/solutions/observability/apm/metrics.md). The way these metrics are calculated depends on the sampling method used:

* **Head-based sampling**: Metrics are calculated based on all sampled events.
* **Tail-based sampling**: Metrics are calculated based on all events, regardless of whether they are ultimately sampled or not.
* **Both head and tail-based sampling**: When both methods are used together, metrics are calculated based on all events that were sampled by the head-based sampling policy.

For all sampling methods, metrics are weighted by the inverse sampling rate of the head-based sampling policy to provide an estimate of the total population. For example, if your head-based sampling rate is 5%, each sampled trace is counted as 20. As the variance of latency increases or the head-based sampling rate decreases, the level of error in these calculations may increase.

These calculation methods ensure that the APM app provides the most accurate metrics possible given the sampling strategy in use, while also accounting for the head-based sampling rate to estimate the full population of traces.

^1^ $$$footnote-1$$$ Real User Monitoring (RUM) traces are an exception to this rule. The {{kib}} apps that utilize RUM data depend on transaction events, so non-sampled RUM traces retain transaction data — only span data is dropped.

## Sample rates [_sample_rates]

```{applies_to}
stack: ga
serverless: ga
```

What’s the best sampling rate? Unfortunately, there isn’t one. Sampling is dependent on your data, the throughput of your application, data retention policies, and other factors. A sampling rate from `.1%` to `100%` would all be considered normal. You’ll likely decide on a unique sample rate for different scenarios. Here are some examples:

* Services with considerably more traffic than others might be safe to sample at lower rates
* Routes that are more important than others might be sampled at higher rates
* A production service environment might warrant a higher sampling rate than a development environment
* Failed trace outcomes might be more interesting than successful traces — thus requiring a higher sample rate

Regardless of the above, cost conscious customers are likely to be fine with a lower sample rate.

## Configure head-based sampling [apm-configure-head-based-sampling]

```{applies_to}
stack: ga
serverless: ga
```

There are three ways to adjust the head-based sampling rate of your APM agents:

### Dynamic configuration [_dynamic_configuration]

The transaction sample rate can be changed dynamically (no redeployment necessary) on a per-service and per-environment basis with [{{apm-agent}} Configuration](/solutions/observability/apm/apm-server/apm-agent-central-configuration.md) in {{kib}}.

### {{kib}} API configuration [_kib_api_configuration]

{{apm-agent}} configuration exposes an API that can be used to programmatically change your agents' sampling rate. For examples, refer to the [Agent configuration API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-apm-agent-configuration).

### {{apm-agent}} configuration [_apm_agent_configuration]

Each agent provides a configuration value used to set the transaction sample rate. See the relevant agent’s documentation for more details:

* Go: [`ELASTIC_APM_TRANSACTION_SAMPLE_RATE`](apm-agent-go://reference/configuration.md#config-transaction-sample-rate)
* Java: [`transaction_sample_rate`](apm-agent-java://reference/config-core.md#config-transaction-sample-rate)
* .NET: [`TransactionSampleRate`](apm-agent-dotnet://reference/config-core.md#config-transaction-sample-rate)
* Node.js: [`transactionSampleRate`](apm-agent-nodejs://reference/configuration.md#transaction-sample-rate)
* PHP: [`transaction_sample_rate`](apm-agent-php://reference/configuration-reference.md#config-transaction-sample-rate)
* Python: [`transaction_sample_rate`](apm-agent-python://reference/configuration.md#config-transaction-sample-rate)
* Ruby: [`transaction_sample_rate`](apm-agent-ruby://reference/configuration.md#config-transaction-sample-rate)

## Configure tail-based sampling [apm-configure-tail-based-sampling]

```{applies_to}
stack: ga
serverless: unavailable
```

::::{note}
Enhanced privileges are required to use tail-based sampling. For more information, refer to [Create a tail-based sampling role](/solutions/observability/apm/create-assign-feature-roles-to-apm-server-users.md#apm-privileges-tail-based-sampling).
::::

Enable tail-based sampling with [Enable tail-based sampling](/solutions/observability/apm/apm-server/tail-based-sampling.md#sampling-tail-enabled-ref). When enabled, trace events are mapped to sampling policies. Each sampling policy must specify a sample rate, and can optionally specify other conditions. All of the policy conditions must be true for a trace event to match it.

Trace events are matched to policies in the order specified. Each policy list must conclude with a default policy — one that only specifies a sample rate. This default policy is used to catch remaining trace events that don’t match a stricter policy. Requiring this default policy ensures that traces are only dropped intentionally. If you enable tail-based sampling and send a transaction that does not match any of the policies, APM Server will reject the transaction with the error `no matching policy`.

::::{important}
Note that from version `9.0.0` APM Server has an unlimited storage limit, but will stop writing when the disk where the database resides reaches 80% usage. Due to how the limit is calculated and enforced, the actual disk space may still grow slightly over this disk usage based limit, or any configured storage limit.
::::

### Example configuration 1 [_example_configuration_1]

This example defines three tail-based sampling polices:

```yaml
- sample_rate: 1 <1>
  service.environment: production
  trace.name: "GET /very_important_route"
- sample_rate: .01 <2>
  service.environment: production
  trace.name: "GET /not_important_route"
- sample_rate: .1 <3>
```

1. Samples 100% of traces in `production` with the trace name `"GET /very_important_route"`
2. Samples 1% of traces in `production` with the trace name `"GET /not_important_route"`
3. Default policy to sample all remaining traces at 10%, e.g. traces in a different environment, like `dev`, or traces with any other name

### Example configuration 2 [_example_configuration_2]

When a trace originates in Service A and then calls Service B, the sampling rate is determined by the service where the trace starts:

```yaml
- sample_rate: 0.3
  service.name: B
- sample_rate: 0.5
  service.name: A
- sample_rate: 0.1  # Fallback: always set a default
```

- Because Service A is the root of the trace, its policy (0.5) is applied while Service B's policy (0.3) is ignored.
- If instead the trace began in Service B (and then passed to Service A), the policy for Service B would apply.

:::{note}
Tail‑based sampling rules are evaluated at the *trace level* based on which service initiated the distributed trace, not the service of the transaction or span.
:::

### Example configuration 3 [_example_configuration_3]

Policies are evaluated **in order** and the first one that meets all match conditions is applied. That means, in practice, order policies from most specific (narrow matchers) to most general, ending with a catch-all (fallback).

```yaml
# Example A: prioritize service origin, then failures
- sample_rate: 0.2
  service.name: A
- sample_rate: 0.5
  trace.outcome: failure
- sample_rate: 0.1  # catch-all
```

```yaml
# Example B: prioritize failures, then a specific service
- sample_rate: 0.2
  trace.outcome: failure
- sample_rate: 0.5
  service.name: A
- sample_rate: 0.1
```

- In Example A, traces from Service A are sampled at 20%, and all other failed traces (regardless of service) are sampled at 50%.
- In Example B, every failed trace is sampled at 20%, including those originating from Service A.

### Configuration reference [_configuration_reference]

For a complete reference of tail-based sampling configuration options, refer to [](/solutions/observability/apm/apm-server/tail-based-sampling.md).
