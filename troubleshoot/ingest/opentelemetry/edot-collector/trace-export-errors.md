---
navigation_title: Trace export errors
description: Learn how to resolve trace export failures caused by `sending_queue` overflow and Elasticsearch exporter timeouts in the EDOT Collector.
applies_to:
  serverless: all
  product:
    edot_collector: ga  
products:
  - id: observability
  - id: edot-collector
---

# Trace export errors from the EDOT Collector

During high traffic or load testing scenarios, the EDOT Collector might fail to export trace data to {{es}}. This typically happens when the internal queue for outgoing data fills up faster than it can be drained, resulting in timeouts and dropped data.

## Symptoms

You might see one or more of the following messages in the EDOT Collector logs:

* `bulk indexer flush error: failed to execute the request: context deadline exceeded`
* `Exporting failed. Rejecting data. sending queue is full`
* Repeated `otelcol.signal: "traces"` errors from the exporter

These errors indicate the Collector is overwhelmed and unable to export traces fast enough, leading to queue overflows and data loss.

## Causes

This issue typically occurs when the `sending_queue` configuration is misaligned with the incoming trace volume. Common contributing factors include:

* `sending_queue.block_on_overflow` is not enabled (it defaults to `false`), so data is dropped when the queue is full.
* `num_consumers` is too low to keep up with the incoming trace volume and drain the queue efficiently.
* The queue size (`queue_size`) is too small for the traffic load.
* Export batching is disabled, increasing processing overhead.
* EDOT Collector resources (CPU, memory) are not sufficient for the traffic volume.

:::{note}
Increasing the `timeout` value (for example from 30s to 90s) doesn't help if the queue itself is the bottleneck.
:::

## Resolution

Update the EDOT Collector configuration as follows:

:::::{stepper}

::::{step} Enable `block_on_overflow`

Prevent silent trace drops by enabling blocking behavior when the queue is full:

```yaml
sending_queue:
    enabled: true
    queue_size: 1000
    num_consumers: 10
    block_on_overflow: true
```
::::

::::{step} Increase `num_consumers`

Raise the number of queue consumers to increase parallel processing of queued items. Start with 20–30 and adjust based on throughput and resource usage.

::::

::::{step} Tune `queue_size`

Increase the queue size to handle spikes in trace volume. Ensure sufficient memory is allocated to support the larger buffer.

::::

::::{step} Enable batching

If not already enabled, configure batching to reduce the per-span export cost and improve throughput.

::::

::::{step} Check resource allocation

Verify the EDOT Collector pod has enough CPU and memory. Increase limits or scale out the deployment if necessary.

::::

::::{step} Evaluate {{es}} performance

Check for indexing delays or errors on the {{es}} side. Bottlenecks here can also contribute to timeouts and queue buildup.

::::

:::::


## Resources

* [Upstream documentation - OpenTelemetry Collector configuration](https://opentelemetry.io/docs/collector/configuration)