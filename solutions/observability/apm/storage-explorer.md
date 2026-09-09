---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-storage-explorer.html
applies_to:
  stack: all
products:
  - id: observability
  - id: apm
---

# Storage Explorer [apm-storage-explorer]

Analyze your APM data and manage costs with **storage explorer**. For example, analyze the storage footprint of each of your services to see which are producing large amounts of data, then change the sample rate of a service to lower the amount of data ingested. Or, expand the time filter to visualize data trends over time so that you can better forecast and prepare for future storage needs.

:::{image} /solutions/images/observability-storage-explorer-overview.png
:alt: APM Storage Explorer
:screenshot:
:::

## Index lifecycle phases [_index_lifecycle_phases]

A default [index lifecycle policy](/solutions/observability/apm/index-lifecycle-management.md) is applied to each APM data stream, but can be customized depending on your business needs. Use the **Index lifecycle phase** dropdown to visualize and analyze your storage by phase.

Customizing the default APM index lifecycle policies can save money by specifying things like:

* The point at which an index can be moved to less performant hardware.
* The point at which availability is not as critical and the number of replicas can be reduced.
* When the index can be safely deleted.

See [Index lifecycle management](/solutions/observability/apm/index-lifecycle-management.md) to learn more about customizing the default APM index lifecycle policies.

## Service size chart [_service_size_chart]

The service size chart displays the estimated size of each service over time. Expand the time filter to visualize data trends and estimate daily data generation.

## Service statistics table [_service_statistics_table]

The service statistics table provides detailed information on each service:

* A list of **service environments**.
* The **sampling rate**. This is the observed sampling rate, which is the number of sampled transactions divided by total throughput. It is based on documents that actually reached {{es}}. It can differ from your configured rate. Refer to [Why the observed sampling rate might differ](#why-the-observed-sampling-rate-might-differ) for more information.
* The estimated **size on disk**. This storage size includes both primary and replica shards and is calculated by prorating the total size of your indices by the service’s document count divided by the total number of documents.
* Number of **transactions**, **spans**, **errors**, and **metrics** — doc count and size on disk.

:::{image} /solutions/images/observability-storage-explorer-expanded.png
:alt: APM Storage Explorer service breakdown
:screenshot:
:::

As you explore your service statistics, you might want to take action to reduce the number of documents and therefore storage size of a particular service.

### Reduce the number of transactions [_reduce_the_number_of_transactions]

To reduce the number of transactions a service generates, configure a more aggressive [transaction sampling policy](/solutions/observability/apm/transaction-sampling.md). Transaction sampling lowers the amount of data ingested without negatively impacting the usefulness of your data.

### Reduce the number of spans [_reduce_the_number_of_spans]

To reduce the number of spans a service generates, enable [span compression](/solutions/observability/apm/spans.md#apm-spans-span-compression). Span compression saves on data and transfer costs by compressing multiple, similar spans into a single span.

### Reduce the number of metrics [_reduce_the_number_of_metrics]

To reduce the number of system, runtime, and application metrics, tune the APM agent or agents that are collecting the data. You can disable the collection of specific metrics with the **disable metrics** configuration. Or, you can set the **metrics interval** to zero seconds to deactivate metrics entirely. Most APM agents support both options. See the relevant [APM agent configuration options](/reference/apm-agents/index.md) for more details.

### Reduce the number of errors [_reduce_the_number_of_errors]

To reduce the number of errors a service generate, work with your developers to change how exceptions are handled in your code.

### Why the observed sampling rate might differ [why-the-observed-sampling-rate-might-differ]

The observed sampling rate reflects what actually reached {{es}}, and not necessarily what you configured. Several factors can cause a difference:

* **Errors are never sampled**

  Errors are always stored regardless of your sampling configuration. If a service generates a high volume of errors, the observed rate will be higher than the configured sampling rate.

* **Head-based sampling**

  With [head-based sampling](/solutions/observability/apm/transaction-sampling.md), the sampling decision happens at the root service and is propagated to downstream services through distributed tracing headers. Configuring a sampling rate on a non-root service has no effect, as it will always respect the upstream decision.

  Non-sampled transactions are not sent to {{apm-server}}, so they don't appear in storage. The exception is the RUM JS Agent, which always sends transaction events regardless of whether they are sampled.

  On low-throughput services, the observed rate might be a less precise approximation of the configured rate because the representative value used to scale sampled transactions can introduce statistical error.

* **Tail-based sampling**

  With [tail-based sampling](/solutions/observability/apm/apm-server/tail-based-sampling.md), {{apm-server}} buffers events locally before making the sampling decision. If the local buffer reaches its storage limit, {{apm-server}} either sends all buffered events (raising the observed rate) or drops them (lowering the observed rate), depending on how overflow is configured.

* **Third-party tracing headers**

  If a gateway or third-party service injects distributed tracing headers that include a sampling decision before the request reaches your root service, {{apm-agent}}s respect those headers instead of the configured rate. You can override this behavior using the [trace continuation strategies](/solutions/observability/apm/transaction-sampling.md#_trace_continuation_strategies_with_distributed_tracing) settings in your {{apm-agent}}.


For the best approximation of your configured sampling rate, filter the time range to a period when your sampling settings were stable and your service was not experiencing an unusually high error rate.

## Privileges [_privileges]

Storage Explorer requires expanded privileges to view. See [Create a storage explorer user](/solutions/observability/apm/ui-user-storage-explorer.md) for more information.

## Limitations [_limitations_4]

Multi-cluster deployments are not supported.
