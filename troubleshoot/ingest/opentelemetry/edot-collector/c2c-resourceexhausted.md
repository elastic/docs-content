---
navigation_title: ResourceExhausted errors in Collector-to-Collector pipelines
description: Troubleshoot EDOT Collector `ResourceExhausted` errors caused by gRPC message size limits, decompression limits, memory pressure, or backpressure in Collector-to-Collector pipelines.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# `ResourceExhausted` and decompression size errors in Collector-to-Collector pipelines

This troubleshooting guide helps you diagnose and resolve `rpc error: code = ResourceExhausted` errors that occur in Collector-to-Collector pipelines when using {{edot}} (EDOT) Collectors. These errors typically indicate that one or more resource limits, such as gRPC message size, decompression memory, or internal buffering, have been exceeded.

This issue is most often reported in the following setups:

- Agent to Gateway Collector architectures
- Multiple Collectors sending to a single gateway
- {{k8s}} environments with autoscaling workloads
- Large clusters where a single collection interval produces large payloads (for example, cluster-wide metrics)
- Pipelines exporting large batches, such as:
  - Traces with large or numerous attributes
  - Logs with large payloads

## Symptoms

You might observe one or more of the following:

- EDOT Collector logs containing messages similar to:
  - `rpc error: code = ResourceExhausted`
  - Errors mentioning message size, decompression, or resource exhaustion
- Telemetry data (traces, metrics, or logs) partially or completely dropped
- Increased retry activity or growing queues in upstream Collectors
- Downstream Collectors appearing healthy but ingesting less data than expected
- Issues that occur primarily when:
  - Multiple Collectors are chained together
  - Traffic volume increases suddenly (deployments, load tests, traffic spikes)

### Common log pattern

A frequent variant of this error looks like:

`rpc error: code = ResourceExhausted desc = grpc: received message after decompression larger than max (4194305 vs. 4194304)`

This typically means the receiving side enforces the gRPC library default maximum receive message size (commonly ~4 MiB) and the incoming payload exceeded it by a small amount.

This limit is not derived from pod CPU/memory sizing. It is primarily a protocol or configuration limit (unless you explicitly configure different limits).

## Causes

`ResourceExhausted` errors indicate that a configured or implicit limit has been exceeded. In Collector-to-Collector pipelines, this is commonly caused by a combination of gRPC limits, memory pressure, and backpressure propagation:

### gRPC message size limits (OTLP receiver)

When using the standard OTLP/gRPC receiver (`otlpreceiver`):

- The EDOT Collector inherits upstream OpenTelemetry Collector behavior.
- If `max_recv_msg_size_mib` is not explicitly configured, the Collector uses the gRPC library default, which is typically ~4 MiB.
- Messages larger than this limit result in a `ResourceExhausted` error.

This limit is configurable:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        max_recv_msg_size_mib: <value>
```

### Large single exports from high-volume receivers

Even without a `batch` processor, some receivers can produce large payloads per collection interval.
For example, cluster-wide metrics can generate tens of thousands of data points in a single cycle. If a single export attempt exceeds the gRPC receive limit, the sending Collector might drop the entire payload for that attempt.

### Decompression and memory limits (Apache Arrow receiver)

When using OTLP with Apache Arrow (`otelarrowreceiver`), the Collector enforces explicit resource limits:

| Limit | Default | Description |
|-----|--------|-------------|
| `admission.request_limit_mib` | 128 MiB | Maximum uncompressed request size |
| `arrow.memory_limit_mib` | 128 MiB | Concurrent memory used by Arrow buffers |
| `arrow.zstd.memory_limit_mib` | 128 MiB per stream | Memory dedicated to Zstd decompression |
| `admission.waiting_limit_mib` | 32 MiB | Requests waiting for admission (backpressure control) |

Exceeding any of these limits results in a `ResourceExhausted` error. All limits are configurable under `receivers.otelarrow`.

### Backpressure propagation across Collectors

In pipelines with multiple Collectors:

- A downstream Collector might become saturated (CPU, memory, or queue limits)
- Upstream Collectors continue sending data until their sending queues fill, or retry limits are exhausted
- This can surface as `ResourceExhausted` errors even if the downstream Collector appears healthy

### Batching and queue configuration mismatches

- Export payloads that are too large can exceed gRPC receiver limits
- Sending queues might fill faster than they can be drained during sudden traffic increases
- Multiple Collectors competing for shared node resources (common in {{k8s}}) amplify the effect

## Diagnosis

To identify the cause, inspect both the sending and receiving Collectors.

::::::{stepper}

:::::{step} Identify where the error originates

- Inspect logs on both upstream and downstream Collectors
- Note which Collector reports the `ResourceExhausted` error (for example, on the exporter side or the receiver side)

:::::

:::::{step} Confirm the transport and receiver

Determine whether traffic uses:

- OTLP/gRPC (`otlpreceiver`)
- OTLP with Apache Arrow (`otelarrowreceiver`)

:::::

:::::{step} Review configured limits

- For OTLP/gRPC:
  - `max_recv_msg_size_mib` on the receiving Collector
- For Apache Arrow:
  - `admission.request_limit_mib`
  - `arrow.memory_limit_mib`
  - `arrow.zstd.memory_limit_mib`
  - `admission.waiting_limit_mib`

:::::

:::::{step} Use internal telemetry to distinguish sender versus receiver problems

**On the sending Collector (exporter-side)**

Look for evidence that the exporter cannot enqueue or send:

- `otelcol_exporter_queue_size` and `otelcol_exporter_queue_capacity`
- `otelcol_exporter_enqueue_failed_metric_points` / `_spans` / `_log_records`
- `otelcol_exporter_send_failed_metric_points` / `_spans` / `_log_records`

If `queue_size` stays near `queue_capacity` and enqueue failures increase, the sender is under pressure (often because the receiver cannot keep up).

**On the receiving Collector (receiver-side)**

Look for evidence of refusal/backpressure and resource saturation:

- `otelcol_receiver_refused_metric_points` / `_spans` / `_log_records`
- Process resource metrics such as:
  - `otelcol_process_memory_rss`
  - `otelcol_process_runtime_heap_alloc_bytes`
  - `otelcol_process_cpu_seconds`

Also check {{k8s}} signals:
- Pod restarts / `CrashLoopBackOff`
- `OOMKilled` events
- CPU throttling

:::::

:::::{step} Correlate with load patterns

Check whether errors coincide with:

- Deployments
- Traffic spikes
- Load tests
- Large cluster-wide metric collection intervals

:::::

::::::

## Resolution

Apply one or more of the following mitigations, starting with the most likely based on your diagnosis.

### Increase gRPC receiver limits on the receiving Collector

If you observe `received message after decompression larger than max (… versus 4194304)` in your logs, increase the receiver's `max_recv_msg_size_mib` on the receiving Collector (commonly the gateway):

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: ${env:MY_POD_IP}:4317
        max_recv_msg_size_mib: 16  # For example: 16 MiB
```

Increase this cautiously:
- Larger limits allow larger payloads but might increase memory usage
- Validate gateway stability (CPU/memory) after the change

### Reduce payload size from the sending Collector

If the sending Collector is exporting payloads that exceed receiver limits, reduce the payload size by adding batching or filtering unnecessary data:

#### Add batching to high-volume pipelines

If a sender exports large metric payloads per cycle, add a batch processor to split exports into smaller requests. Because batching limits are count-based (data points, log records, or spans), you might need to tune iteratively.

Example (adding batching to a cluster-stats metrics pipeline):

```yaml
processors:
  batch/metrics:
    timeout: 1s
    send_batch_size: 2048 # `send_batch_size` is both the target and the maximum batch size.

service:
  pipelines:
    metrics:
      receivers: [otlp]
      processors:
        - batch/metrics
        - k8sattributes
        - resourcedetection/eks
        - resourcedetection/gcp
        - resourcedetection/aks
        - resource/k8s
        - resource/hostname
      exporters: [otlp/gateway]
```

#### Reduce high-volume or high-cardinality content

If possible, reduce payload size by:
- Turn off unnecessary metrics in receivers
- Filtering high-cardinality labels/attributes early in the pipeline
- Removing large attributes when safe for your use case

### Tune exporter queue and retry behavior to reduce drops during transient overload

If drops happen during sudden traffic increases or temporary downstream slowdowns, turn on and tune queued retry on the sending exporter.

Configuration keys depend on the exporter and distribution, but commonly include:

```yaml
exporters:
  otlp/gateway:
    endpoint: "<gateway-service>:4317" # OTLP/gRPC endpoint (port 4317)
    tls:
      insecure: true
    sending_queue:
      enabled: true
      queue_size: 10000
    retry_on_failure:
      enabled: true
```

### Address backpressure by scaling and properly sizing the receiving Collector

If the gateway is restarting, `OOMKilled`, or cannot export fast enough:

- Increase gateway CPU/memory limits
- Increase gateway replicas
- Ensure environment limits align with container memory

Backpressure commonly originates at the receiver when its own exporters (for example, {{es}} exporters) cannot keep up.

### Protect against memory exhaustion

- Configure the `memory_limiter` processor early in the pipeline
- Set limits based on available memory and workload characteristics

The OpenTelemetry Collector doesn't provide a memory ballast or heap pre-allocation mechanism. Memory protection relies on the `memory_limiter` processor and careful tuning of batching, queues, and receiver limits.

## Best practices

To prevent `ResourceExhausted` errors in Collector-to-Collector architectures:

- Design pipelines with sufficient capacity at each Collector in the pipeline
- Test under realistic peak load conditions (including burst traffic patterns)
- Monitor both sides:
  - Exporter queue utilization and send failures on the sender
  - Receiver refused metrics and resource usage on the receiver
- Standardize batch and queue settings across environments
- Minimize unnecessary Collector chaining

## Resources

- [Contrib OpenTelemetry Collector troubleshooting (official)](https://opentelemetry.io/docs/collector/troubleshooting/)—guidance on debugging Collector health, pipelines, exporters, and more.
- [Contrib OpenTelemetry Collector internal telemetry docs](https://opentelemetry.io/docs/collector/internal-telemetry/)—learn how to configure and interpret internal Collector logs & metrics.
- [Contrib OpenTelemetry Collector configuration reference](https://opentelemetry.io/docs/collector/configuration/)—includes OTLP receiver configuration and general component docs.
- [OTel-Arrow receiver in OpenTelemetry Collector contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/otelarrowreceiver/README.md)—canonical upstream reference for Apache Arrow receiver configuration and resource limits.
- [OTel-Arrow exporter in OpenTelemetry Collector contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/exporter/otelarrowexporter/README.md)—canonical upstream reference for Apache Arrow exporter configuration.