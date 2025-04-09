---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-tail-based-samling-config.html
applies_to:
  stack: all
---

# Tail-based sampling [apm-tail-based-sampling-config]

::::{note}
![supported deployment methods](/solutions/images/observability-binary-yes-fm-yes.svg "")

Most options on this page are supported by all APM Server deployment methods when writing to {{es}}. If you are using a different [output](configure-output.md), tail-based sampling is *not* supported.

::::

Tail-based sampling configuration options.

:::::::{tab-set}

::::::{tab-item} APM Server binary
**Example config file:**

```yaml
apm-server:
  host: "localhost:8200"
  rum:
    enabled: true

output:
  elasticsearch:
    hosts: ElasticsearchAddress:9200

max_procs: 4
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

See [Tail-based sampling](transaction-sampling.md#apm-tail-based-sampling) to learn more.

### Enable tail-based sampling [sampling-tail-enabled-ref]

Set to `true` to enable tail based sampling. Disabled by default. (bool)

|     |     |
| --- | --- |
| APM Server binary | `sampling.tail.enabled` |
| Fleet-managed | `Enable tail-based sampling` |

### Interval [sampling-tail-interval-ref]

Synchronization interval for multiple APM Servers. Should be in the order of tens of seconds or low minutes. Default: `1m` (1 minute). (duration)

|     |     |
| --- | --- |
| APM Server binary | `sampling.tail.interval` |
| Fleet-managed | `Interval` |

### Policies [sampling-tail-policies-ref]

Criteria used to match a root transaction to a sample rate.

Policies map trace events to a sample rate. Each policy must specify a sample rate. Trace events are matched to policies in the order specified. All policy conditions must be true for a trace event to match. Each policy list should conclude with a policy that only specifies a sample rate. This final policy is used to catch remaining trace events that don’t match a stricter policy. (`[]policy`)

|     |     |
| --- | --- |
| APM Server binary | `sampling.tail.policies` |
| Fleet-managed | `Policies` |

### Storage limit [sampling-tail-storage_limit-ref]

The amount of storage space allocated for trace events matching tail sampling policies. Caution: Setting this limit higher than the allowed space may cause APM Server to become unhealthy.

A value of `0GB` (or equivalent) does not set a concrete limit, but rather allows the APM Server to align its disk usage with the disk size. APM server uses up to 80% of the disk size limit on the disk where the local tail-based sampling database is located. The last 20% of disk will not be used by APM Server. It is the recommended value as it automatically scales with the disk size.

If this is not desired, a concrete `GB` value can be set for the maximum amount of disk used for tail-based sampling.

If the configured storage limit is insufficient, it logs "configured limit reached". The event will bypass sampling and will always be indexed when storage limit is reached.

Default: `0GB`. (text)

|     |     |
| --- | --- |
| APM Server binary | `sampling.tail.storage_limit` |
| Fleet-managed | `Storage limit` |

## Policy-level tail-based sampling settings [apm-configuration-tbs-policy]

See [Tail-based sampling](transaction-sampling.md#apm-tail-based-sampling) to learn more.

### **`sample_rate`** [sampling-tail-sample-rate-ref]

The sample rate to apply to trace events matching this policy. Required in each policy.

The sample rate must be greater than or equal to `0` and less than or equal to `1`. For example, a `sample_rate` of `0.01` means that 1% of trace events matching the policy will be sampled. A `sample_rate` of `1` means that 100% of trace events matching the policy will be sampled. (int)

### **`trace.name`** [sampling-tail-trace-name-ref]

The trace name for events to match a policy. A match occurs when the configured `trace.name` matches the `transaction.name` of the root transaction of a trace. A root transaction is any transaction without a `parent.id`. (string)

### **`trace.outcome`** [sampling-tail-trace-outcome-ref]

The trace outcome for events to match a policy. A match occurs when the configured `trace.outcome` matches a trace’s `event.outcome` field. Trace outcome can be `success`, `failure`, or `unknown`. (string)

### **`service.name`** [sampling-tail-service-name-ref]

The service name for events to match a policy. (string)

### **`service.environment`** [sampling-tail-service-environment-ref]

The service environment for events to match a policy. (string)

## Monitoring tail-based sampling [sampling-tail-monitoring-ref]

APM Server produces metrics to monitor the performance and estimate the workload being processed by tail-based sampling. In order to use these metrics, you need to [enable monitoring for the APM Server](/solutions/observability/apps/monitor-apm-server.md). The following metrics are produced by the tail-based sampler (note that the metrics might have a different prefix,  for example `beat.stats` for ECH deployments, based on how the APM Server is running):

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
