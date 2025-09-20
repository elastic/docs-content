---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-tail-based-samling-config.html
applies_to:
  stack: all
products:
  - id: observability
  - id: apm
---

# Tail-based sampling [apm-tail-based-sampling-config]

::::{note}
![supported deployment methods](/solutions/images/observability-binary-yes-fm-yes.svg "")

Most options on this page are supported by all APM Server deployment methods when writing to {{es}}. If you are using a different [output](/solutions/observability/apm/apm-server/configure-output.md), tail-based sampling is *not* supported.
::::

::::{note}
Enhanced privileges are required to use tail-based sampling. For more information, refer to [Create a tail-based sampling role](/solutions/observability/apm/create-assign-feature-roles-to-apm-server-users.md#apm-privileges-tail-based-sampling).
::::

Tail-based sampling configuration options.

:::::::{tab-set}

::::::{tab-item} APM Server binary
**Example config file:**

```yaml
apm-server:
  sampling:
    tail:
      enabled: true
      interval: 1m
      storage_limit: 0GB
      policies:
        - sample_rate: 1.0
          trace.outcome: failure
        - sample_rate: 0.1
```
::::::

::::::{tab-item} Fleet-managed
Configure and customize Fleet-managed APM settings directly in {{kib}}:

1. In {{kib}}, find **Fleet** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under the **Agent policies** tab, select the policy you would like to configure.
3. Find the Elastic APM integration and select **Actions** > **Edit integration**.
4. Look for these options under **Tail-based sampling**.
::::::

:::::::

## Top-level tail-based sampling settings [apm-configuration-tbs]

See [Tail-based sampling](/solutions/observability/apm/transaction-sampling.md#apm-tail-based-sampling) to learn more.

### Enable tail-based sampling [sampling-tail-enabled-ref]

Set to `true` to enable tail based sampling. Disabled by default. (bool)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.sampling.tail.enabled` |
| Fleet-managed | `Enable tail-based sampling` |

### Interval [sampling-tail-interval-ref]

Synchronization interval for multiple APM Servers. Should be in the order of tens of seconds or low minutes. Default: `1m` (1 minute). (duration)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.sampling.tail.interval` |
| Fleet-managed | `Interval` |

### TTL [sampling-tail-ttl-ref]

Time-to-live (TTL) for trace events stored in the local storage of the APM Server during tail-based sampling. This TTL determines how long trace events are retained in the local storage while waiting for a sampling decision to be made. A greater TTL value increases storage space requirements. Should be at least 2 * Interval (`apm-server.sampling.tail.interval`).

Default: `30m` (30 minutes). (duration)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.sampling.tail.ttl` |
| Fleet-managed {applies_to}`stack: ga 9.1` | `TTL` |


### Policies [sampling-tail-policies-ref]

Criteria used to match a root transaction to a sample rate.

Policies map trace events to a sample rate. Each policy must specify a sample rate. Trace events are matched to policies in the order specified. All policy conditions must be true for a trace event to match. Each policy list should conclude with a policy that only specifies a sample rate. This final policy is used to catch remaining trace events that don’t match a stricter policy. (`[]policy`)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.sampling.tail.policies` |
| Fleet-managed | `Policies` |

### Discard On Write Failure [sampling-tail-discard-on-write-failure-ref]

Defines the indexing behavior when trace events fail to be written to storage (for example, when the storage limit is reached). When set to `false`, traces bypass sampling and are always indexed, which significantly increases the indexing load. When set to `true`, traces are discarded, causing data loss which can result in broken traces. The default is `false`.

Default: `false`. (bool)

|                              |                                          |
|------------------------------|------------------------------------------|
| APM Server binary            | `apm-server.sampling.tail.discard_on_write_failure` |
| Fleet-managed {applies_to}`stack: ga 9.1` | `Discard On Write Failure`               |


### Storage limit [sampling-tail-storage_limit-ref]

The amount of storage space allocated for trace events matching tail sampling policies. Caution: Setting this limit higher than the allowed space may cause APM Server to become unhealthy.

A value of `0GB` (or equivalent) does not set a concrete limit, but rather allows the APM Server to align its disk usage with the disk size. APM server uses up to 80% of the disk size limit on the disk where the local tail-based sampling database is located. The last 20% of disk will not be used by APM Server. It is the recommended value as it automatically scales with the disk size.

If this is not desired, a concrete `GB` value can be set for the maximum amount of disk used for tail-based sampling.

If the configured storage limit is insufficient, it logs "configured limit reached". When the storage limit is reached, the event will be indexed or discarded based on the [Discard On Write Failure](#sampling-tail-discard-on-write-failure-ref) configuration.

Default: `0GB`. (text)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.sampling.tail.storage_limit` |
| Fleet-managed | `Storage limit` |

## Policy-level tail-based sampling settings [apm-configuration-tbs-policy]

See [Tail-based sampling](/solutions/observability/apm/transaction-sampling.md#apm-tail-based-sampling) to learn more.

### **`sample_rate`** [sampling-tail-sample-rate-ref]

The sample rate to apply to trace events matching this policy. Required in each policy.

The sample rate must be greater than or equal to `0` and less than or equal to `1`. For example, a `sample_rate` of `0.01` means that 1% of trace events matching the policy will be sampled. A `sample_rate` of `1` means that 100% of trace events matching the policy will be sampled. (float)

### **`trace.name`** [sampling-tail-trace-name-ref]

The trace name for events to match a policy. A match occurs when the configured `trace.name` matches the `transaction.name` of the root transaction of a trace. A root transaction is any transaction without a `parent.id`. (string)

### **`trace.outcome`** [sampling-tail-trace-outcome-ref]

The trace outcome for events to match a policy. A match occurs when the configured `trace.outcome` matches a trace’s `event.outcome` field. Trace outcome can be `success`, `failure`, or `unknown`. (string)

### **`service.name`** [sampling-tail-service-name-ref]

The service name for events to match a policy. (string)

### **`service.environment`** [sampling-tail-service-environment-ref]

The service environment for events to match a policy. (string)

## Monitoring tail-based sampling [sampling-tail-monitoring-ref]

APM Server produces metrics to monitor the performance and estimate the workload being processed by tail-based sampling. In order to use these metrics, you need to [enable monitoring for the APM Server](/solutions/observability/apm/apm-server/monitor.md). The following metrics are produced by the tail-based sampler (note that the metrics might have a different prefix,  for example `beat.stats` for ECH deployments, based on how the APM Server is running):

### `apm-server.sampling.tail.dynamic_service_groups` [sampling-tail-monitoring-dynamic-service-group-ref]

This metric tracks the number of dynamic services that the tail-based sampler is tracking per policy. Dynamic services are created for tail-based sampling policies that are defined without a `service.name`.

This is a counter metric so, should be visualized with `counter_rate`.

### `apm-server.sampling.tail.events.processed` [sampling-tail-monitoring-events-processed-ref]

This metric tracks the total number of events (including both transaction and span) processed by the tail-based sampler.

This is a counter metric so, should be visualized with `counter_rate`.

### `apm-server.sampling.tail.events.stored` [sampling-tail-monitoring-events-stored-ref]

This metric tracks the total number of events stored by the tail-based sampler in the database. Events are stored when the full trace is not yet available to make the sampling decision. This value is directly proportional to the storage required by the tail-based sampler to function.

This is a counter metric so, should be visualized with `counter_rate`.

### `apm-server.sampling.tail.events.dropped` [sampling-tail-monitoring-events-dropped-ref]

This metric tracks the total number of events dropped by the tail-based sampler. Only the events that are actually dropped by the tail-based sampler are reported as dropped. Additionally, any events that were stored by the processor but never indexed will not be counted by this metric.

This is a counter metric so, should be visualized with `counter_rate`.

### `apm-server.sampling.tail.storage.lsm_size` [sampling-tail-monitoring-storage-lsm-size-ref]

This metric tracks the storage size of the log-structured merge trees used by the tail-based sampling database in bytes. Starting in version 9.0.0, this metric is effectively equal to the total storage size used by the database. This is the most crucial metric to track storage requirements for tail-based sampler, especially for big deployments with large distributed traces. Deployments using tail-based sampling extensively should set up alerts and monitoring on this metric.

This metric can also be used to get an estimate of the storage requirements for tail-based sampler before increasing load by extrapolating the metric based on the current usage. It is important to note that before doing any estimation the tail-based sampler should be allowed to run for at least a few TTL cycles and that the estimate will only be useful for similar load patterns.

### `apm-server.sampling.tail.storage.value_log_size` [sampling-tail-monitoring-storage-value-log-size-ref]

This metric tracks the storage size for value log files used by the previous implementation of a tail-based sampler. This metric was deprecated in 9.0.0 and should always report `0`.

## Frequently Asked Questions (FAQ) [sampling-tail-faq-ref]

:::{dropdown} Why doesn't the sampling rate shown in Storage Explorer match the configured tail sampling rate?

In APM Server, the tail sampling policy applied to a distributed trace is determined by evaluating the configured policies in order against the root transaction (the transaction without a parent). To learn more about how tail sampling policies are applied, see the examples in [Configure Tail-based sampling](/solutions/observability/apm/transaction-sampling.md#apm-configure-tail-based-sampling).

In contrast, the APM UI Storage Explorer calculates the effective average sampling rate for each service using a different method. It considers both head-based and tail-based sampling, but does not account for root transactions. As a result, the sampling rate displayed in Storage Explorer may differ from the configured tail sampling rate, which can give the false impression that tail-based sampling is not functioning correctly.

For more information, check the related [Kibana issue](https://github.com/elastic/kibana/issues/226600).
:::

:::{dropdown} Why do transactions disappear after enabling tail-based sampling?

If a transaction is consistently not sampled after enabling tail-based sampling, verify that your instrumentation is not missing root transactions (transactions without a parent). APM Server makes sampling decisions when a distributed trace ends, which occurs when the root transaction ends. If the root transaction is not received by APM Server, it cannot make a sampling decision and will silently drop all associated trace events.

This issue often arises when it is assumed that a particular service (e.g., service A) always produces the root transaction, but in reality, another service (e.g., service B) may precede it. If service B is not instrumented or sends data to a different APM Server cluster, the root transaction will be missing. To resolve this, ensure that all relevant services are instrumented and send data to the same APM Server cluster, or adjust the trace continuation strategy accordingly.

To identify traces missing a root transaction, run the following {{esql}} query during a period when tail-based sampling is disabled. Use a short time range to limit the number of results:

```
FROM "traces-apm-*"
| STATS total_docs = COUNT(*), total_child_docs = COUNT(parent.id) BY trace.id, transaction.id
| WHERE total_docs == total_child_docs
| KEEP trace.id, transaction.id
```
:::

:::{dropdown} Why is the configured tail sampling rate ignored and why are traces always sampled, causing unexpected load to Elasticsearch?

When the storage limit for tail-based sampling is reached, APM Server will log "configured limit reached" (or "configured storage limit reached" in version 8) as it cannot store new trace events for sampling. By default, traces bypass sampling and are always indexed (sampling rate becomes 100%). This can cause a sudden increase in indexing load, potentially overloading Elasticsearch, as it must process all incoming traces instead of only the sampled subset.

To mitigate this risk, enable the [`discard_on_write_failure`](#sampling-tail-discard-on-write-failure-ref) setting. When set to `true`, APM Server discards traces that cannot be written due to storage or indexing failures, rather than indexing them all. This helps protect Elasticsearch from excessive load. Note that enabling this option can result in data loss and broken traces, so it should be used with caution and only when system stability is a priority.

For more information, refer to the [Discard On Write Failure](#sampling-tail-discard-on-write-failure-ref) section.
:::
