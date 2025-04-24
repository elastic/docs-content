---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-sampling.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-transaction-sampling.html
applies_to:
  stack:
  serverless:
---

# Transaction sampling [apm-sampling]

:::{include} _snippets/apm-server-vs-mis.md
:::

[Distributed tracing](/solutions/observability/apm/traces.md) can generate a substantial amount of data. More data can mean higher costs and more noise. Sampling aims to lower the amount of data ingested and the effort required to analyze that data — all while still making it easy to find anomalous patterns in your applications, detect outages, track errors, and lower mean time to recovery (MTTR).

Elastic APM supports two types of sampling:

% Stateful only for Tail-based sampling

* [Head-based sampling](/solutions/observability/apm/transaction-sampling.md#apm-head-based-sampling)
* [Tail-based sampling](/solutions/observability/apm/transaction-sampling.md#apm-tail-based-sampling)

## Head-based sampling [apm-head-based-sampling]

```{applies_to}
stack:
serverless:
```

In head-based sampling, the sampling decision for each trace is made when the trace is initiated. Each trace has a defined and equal probability of being sampled.

For example, a sampling value of `.2` indicates a transaction sample rate of `20%`. This means that only `20%` of traces will send and retain all of their associated information. The remaining traces will drop contextual information to reduce the transfer and storage size of the trace.

Head-based sampling is quick and easy to set up. Its downside is that it’s entirely random — interesting data might be discarded purely due to chance.

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
stack:
serverless: unavailable
```

::::{note}
**Support for tail-based sampling**

Tail-based sampling is only supported when writing to {{es}}. If you are using a different [output](/solutions/observability/apm/configure-output.md), tail-based sampling is *not* supported.
::::

In tail-based sampling, the sampling decision for each trace is made after the trace has completed. This means all traces will be analyzed against a set of rules, or policies, which will determine the rate at which they are sampled.

Unlike head-based sampling, each trace does not have an equal probability of being sampled. Because slower traces are more interesting than faster ones, tail-based sampling uses weighted random sampling — so traces with a longer root transaction duration are more likely to be sampled than traces with a fast root transaction duration.

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

Due to [OpenTelemetry tail-based sampling limitations](/solutions/observability/apm/limitations.md#apm-open-telemetry-tbs) when using [tailsamplingprocessor](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor), we recommend using APM Server tail-based sampling instead.

### Tail-based sampling performance and requirements [_tail_based_sampling_performance_and_requirements]

Tail-based sampling (TBS), by definition, requires storing events locally temporarily, such that they can be retrieved and forwarded when a sampling decision is made.

In an APM Server implementation, the events are stored temporarily on disk instead of in memory for better scalability. Therefore, it requires local disk storage proportional to the APM event ingestion rate and additional memory to facilitate disk reads and writes. If the [storage limit](#sampling-tail-storage_limit) is insufficient, sampling will be bypassed.

It is recommended to use fast disks, ideally Solid State Drives (SSD) with high I/O per second (IOPS), when enabling tail-based sampling. Disk throughput and I/O may become performance bottlenecks for tail-based sampling and APM event ingestion overall. Disk writes are proportional to the event ingest rate, while disk reads are proportional to both the event ingest rate and the sampling rate.

To demonstrate the performance overhead and requirements, here are some reference numbers from a standalone APM Server deployed on AWS EC2 under full load that is receiving APM events containing only traces. These numbers assume no backpressure from Elasticsearch and a **10% sample rate in the tail sampling policy**.

:::{important}
These figures are for reference only and may vary depending on factors such as sampling rate, average event size, and the average number of events per distributed trace.
:::

Terminology:

* Event Ingestion Rate: The throughput from the APM agent to the APM Server using the Intake v2 protocol (the protocol used by Elastic APM agents), measured in events per second.
* Event Indexing Rate: The throughput from the APM Server to Elasticsearch, measured in events per second or documents per second. Note that it should roughly be equal to Event Ingestion Rate * Sampling Rate.
* Memory Usage: The maximum Resident Set Size (RSS) of APM Server process observed throughout the benchmark.

#### APM Server 9.0

| EC2 instance size | TBS and disk configuration                     | Event ingestion rate (events/s) | Event indexing rate (events/s) | Memory usage (GB) | Disk usage (GB) |
|-------------------|------------------------------------------------|---------------------------------|--------------------------------|-------------------|-----------------|
| c6id.2xlarge      | TBS disabled                                   | 47220                           | 47220 (100% sampling)          | 0.98              | 0               |
| c6id.2xlarge      | TBS enabled, EBS gp3 volume with 3000 IOPS     | 21310                           | 2360                           | 1.41              | 13.1            |
| c6id.2xlarge      | TBS enabled, local NVMe SSD from c6id instance | 21210                           | 2460                           | 1.34              | 12.9            |
| c6id.4xlarge      | TBS disabled                                   | 142200                          | 142200 (100% sampling)         | 1.12              | 0               |
| c6id.4xlarge      | TBS enabled, EBS gp3 volume with 3000 IOPS     | 32410                           | 3710                           | 1.71              | 19.4            |
| c6id.4xlarge      | TBS enabled, local NVMe SSD from c6id instance | 37040                           | 4110                           | 1.73              | 23.6            |

#### APM Server 8.18

| EC2 instance size | TBS and disk configuration                     | Event ingestion rate (events/s) | Event indexing rate (events/s) | Memory usage (GB) | Disk usage (GB) |
|-------------------|------------------------------------------------|---------------------------------|--------------------------------|-------------------|-----------------|
| c6id.2xlarge      | TBS disabled                                   | 50260                           | 50270 (100% sampling)          | 0.98              | 0               |
| c6id.2xlarge      | TBS enabled, EBS gp3 volume with 3000 IOPS     | 10960                           | 50                             | 5.24              | 24.3            |
| c6id.2xlarge      | TBS enabled, local NVMe SSD from c6id instance | 11450                           | 820                            | 7.19              | 30.6            |
| c6id.4xlarge      | TBS disabled                                   | 149200                          | 149200 (100% sampling)         | 1.14              | 0               |
| c6id.4xlarge      | TBS enabled, EBS gp3 volume with 3000 IOPS     | 11990                           | 530                            | 26.57             | 33.6            |
| c6id.4xlarge      | TBS enabled, local NVMe SSD from c6id instance | 43550                           | 2940                           | 28.76             | 109.6           |

When interpreting these numbers, note that:

* The metrics are inter-related. For example, it is reasonable to see higher memory usage and disk usage when the event ingestion rate is higher.
* The event ingestion rate and event indexing rate competes for disk IO. This is why there is an outlier data point where APM Server version 8.18 with a 32GB NVMe SSD shows a higher ingest rate but a slower event indexing rate than in 9.0.

The tail-based sampling implementation in version 9.0 offers significantly better performance compared to version 8.18, primarily due to a rewritten storage layer. This new implementation compresses data, as well as cleans up expired data more reliably, resulting in reduced load on disk, memory, and compute resources. This improvement is particularly evident in the event indexing rate on slower disks. In version 8.18, as the database grows larger, the performance slowdown can become disproportionate.

## Sampled data and visualizations [_sampled_data_and_visualizations]

```{applies_to}
stack:
serverless:
```

A sampled trace retains all data associated with it. A non-sampled trace drops all [span](/solutions/observability/apm/spans.md) and [transaction](/solutions/observability/apm/transactions.md) data.[^1^](#footnote-1) Regardless of the sampling decision, all traces retain [error](/solutions/observability/apm/errors.md) data.

Some visualizations in the {{apm-app}}, like latency, are powered by aggregated transaction and span [metrics](/solutions/observability/apm/metrics.md). The way these metrics are calculated depends on the sampling method used:

* **Head-based sampling**: Metrics are calculated based on all sampled events.
* **Tail-based sampling**: Metrics are calculated based on all events, regardless of whether they are ultimately sampled or not.
* **Both head and tail-based sampling**: When both methods are used together, metrics are calculated based on all events that were sampled by the head-based sampling policy.

For all sampling methods, metrics are weighted by the inverse sampling rate of the head-based sampling policy to provide an estimate of the total population. For example, if your head-based sampling rate is 5%, each sampled trace is counted as 20. As the variance of latency increases or the head-based sampling rate decreases, the level of error in these calculations may increase.

These calculation methods ensure that the APM app provides the most accurate metrics possible given the sampling strategy in use, while also accounting for the head-based sampling rate to estimate the full population of traces.

^1^ $$$footnote-1$$$ Real User Monitoring (RUM) traces are an exception to this rule. The {{kib}} apps that utilize RUM data depend on transaction events, so non-sampled RUM traces retain transaction data — only span data is dropped.

## Sample rates [_sample_rates]

```{applies_to}
stack:
serverless:
```

What’s the best sampling rate? Unfortunately, there isn’t one. Sampling is dependent on your data, the throughput of your application, data retention policies, and other factors. A sampling rate from `.1%` to `100%` would all be considered normal. You’ll likely decide on a unique sample rate for different scenarios. Here are some examples:

* Services with considerably more traffic than others might be safe to sample at lower rates
* Routes that are more important than others might be sampled at higher rates
* A production service environment might warrant a higher sampling rate than a development environment
* Failed trace outcomes might be more interesting than successful traces — thus requiring a higher sample rate

Regardless of the above, cost conscious customers are likely to be fine with a lower sample rate.

## Configure head-based sampling [apm-configure-head-based-sampling]

```{applies_to}
stack:
serverless:
```

There are three ways to adjust the head-based sampling rate of your APM agents:

### Dynamic configuration [_dynamic_configuration]

The transaction sample rate can be changed dynamically (no redeployment necessary) on a per-service and per-environment basis with [{{apm-agent}} Configuration](/solutions/observability/apm/apm-agent-central-configuration.md) in {{kib}}.

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
stack:
serverless: unavailable
```

::::{note}
Enhanced privileges are required to use tail-based sampling. For more information, refer to [Create a tail-based sampling role](/solutions/observability/apm/create-assign-feature-roles-to-apm-server-users.md#apm-privileges-tail-based-sampling).
::::

Enable tail-based sampling with [Enable tail-based sampling](/solutions/observability/apm/tail-based-sampling.md#sampling-tail-enabled-ref). When enabled, trace events are mapped to sampling policies. Each sampling policy must specify a sample rate, and can optionally specify other conditions. All of the policy conditions must be true for a trace event to match it.

Trace events are matched to policies in the order specified. Each policy list must conclude with a default policy — one that only specifies a sample rate. This default policy is used to catch remaining trace events that don’t match a stricter policy. Requiring this default policy ensures that traces are only dropped intentionally. If you enable tail-based sampling and send a transaction that does not match any of the policies, APM Server will reject the transaction with the error `no matching policy`.

::::{important}
Note that from version `9.0.0` APM Server has an unlimited storage limit, but will stop writing when the disk where the database resides reaches 80% usage. Due to how the limit is calculated and enforced, the actual disk space may still grow slightly over this disk usage based limit, or any configured storage limit.
::::

### Example configuration [_example_configuration]

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

### Configuration reference [_configuration_reference]

#### Top-level tail-based sampling settings [_top_level_tail_based_sampling_settings]

##### Enable tail-based sampling [sampling-tail-enabled]

Set to `true` to enable tail based sampling. Disabled by default. (bool)

|     |     |
| --- | --- |
| APM Server binary | `sampling.tail.enabled` |
| Fleet-managed | `Enable tail-based sampling` |

##### Interval [sampling-tail-interval]

Synchronization interval for multiple APM Servers. Should be in the order of tens of seconds or low minutes. Default: `1m` (1 minute). (duration)

|     |     |
| --- | --- |
| APM Server binary | `sampling.tail.interval` |
| Fleet-managed | `Interval` |

##### Policies [sampling-tail-policies]

Criteria used to match a root transaction to a sample rate.

Policies map trace events to a sample rate. Each policy must specify a sample rate. Trace events are matched to policies in the order specified. All policy conditions must be true for a trace event to match. Each policy list should conclude with a policy that only specifies a sample rate. This final policy is used to catch remaining trace events that don’t match a stricter policy. (`[]policy`)

|     |     |
| --- | --- |
| APM Server binary | `sampling.tail.policies` |
| Fleet-managed | `Policies` |

##### Storage limit [sampling-tail-storage_limit]

The amount of storage space allocated for trace events matching tail sampling policies. Caution: Setting this limit higher than the allowed space may cause APM Server to become unhealthy.

A value of `0GB` (or equivalent) does not set a concrete limit, but rather allows the APM Server to align its disk usage with the disk size. APM server uses up to 80% of the disk size limit on the disk where the local tail-based sampling database is located. The last 20% of disk will not be used by APM Server. It is the recommended value as it automatically scales with the disk size.

If this is not desired, a concrete `GB` value can be set for the maximum amount of disk used for tail-based sampling.

If the configured storage limit is insufficient, it logs "configured limit reached". The event will bypass sampling and will always be indexed when storage limit is reached.

Default: `0GB`. (text)

|     |     |
| --- | --- |
| APM Server binary | `sampling.tail.storage_limit` |
| Fleet-managed | `Storage limit` |

#### Policy settings [_policy_settings]

##### **`sample_rate`** [sampling-tail-sample-rate]

The sample rate to apply to trace events matching this policy. Required in each policy.

The sample rate must be greater than or equal to `0` and less than or equal to `1`. For example, a `sample_rate` of `0.01` means that 1% of trace events matching the policy will be sampled. A `sample_rate` of `1` means that 100% of trace events matching the policy will be sampled. (int)

##### **`trace.name`** [sampling-tail-trace-name]

The trace name for events to match a policy. A match occurs when the configured `trace.name` matches the `transaction.name` of the root transaction of a trace. A root transaction is any transaction without a `parent.id`. (string)

##### **`trace.outcome`** [sampling-tail-trace-outcome]

The trace outcome for events to match a policy. A match occurs when the configured `trace.outcome` matches a trace’s `event.outcome` field. Trace outcome can be `success`, `failure`, or `unknown`. (string)

##### **`service.name`** [sampling-tail-service-name]

The service name for events to match a policy. (string)

##### **`service.environment`** [sampling-tail-service-environment]

The service environment for events to match a policy. (string)
