---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-tail-based-samling-config.html
applies_to:
  stack: all
---

# Tail-based sampling [apm-tail-based-samling-config]

::::{note}
![supported deployment methods](../../../images/observability-binary-yes-fm-yes.svg "")

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

If the configured storage limit is insufficient, it logs "configured storage limit reached". The event will bypass sampling and will always be indexed when storage limit is reached.

Default: `3GB`. (text)

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
