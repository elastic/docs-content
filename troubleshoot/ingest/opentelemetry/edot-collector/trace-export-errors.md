---
navigation_title: Export errors from the EDOT Collector
description: Learn how to resolve export failures caused by `sending_queue` overflow and Elasticsearch exporter timeouts in the EDOT Collector.
applies_to:
  serverless: all
  product:
    edot_collector: ga  
products:
  - id: observability
  - id: edot-collector
---

# Export failures when sending telemetry data from the EDOT Collector

During high traffic or load testing scenarios, the EDOT Collector might fail to export telemetry data (traces, metrics, or logs) to {{es}}. This typically happens when the internal queue for outgoing data fills up faster than it can be drained, resulting in timeouts and dropped data.

## Symptoms

You might see one or more of the following messages in the EDOT Collector logs:

* `bulk indexer flush error: failed to execute the request: context deadline exceeded`
* `Exporting failed. Rejecting data. sending queue is full`

These errors indicate the Collector is overwhelmed and unable to export data fast enough, leading to queue overflows and data loss.

## Causes

This issue typically occurs when the `sending_queue` configuration is misaligned with the incoming telemetry volume. 

:::{important}
The sending queue is disabled by default in versions earlier than **v0.138.0** and enabled by default from **v0.138.0** onward. If you're using an earlier version, verify that `enabled: true` is explicitly set — otherwise any queue configuration will be ignored.
:::

Common contributing factors include:

* `sending_queue.block_on_overflow` is not enabled (it defaults to `false`), so data is dropped when the queue is full.
* `num_consumers` is too low to keep up with the incoming data volume.
* The queue size (`queue_size`) is too small for the traffic load.
* Export batching is disabled, increasing processing overhead.
* EDOT Collector resources (CPU, memory) are not sufficient for the traffic volume.

:::{note}
Increasing the `timeout` value (for example from 30s to 90s) doesn't help if the queue itself is the bottleneck.
:::

## Resolution

The resolution approach depends on which EDOT Collector version you're using.

### For EDOT Collector versions earlier than v0.138.0

Enable the sending queue and block on overflow to prevent silent data drops:

```yaml
sending_queue:
  enabled: true
  queue_size: 1000
  num_consumers: 10
  block_on_overflow: true
```

### For EDOT Collector v0.138.0 and later

The `sending_queue` behavior is managed internally by the exporter. Adjusting its parameters has a limited effect on throughput. In these versions, the most effective optimizations are:

* Increase Collector resources by ensuring the EDOT Collector pod has enough CPU and memory. Scale vertically (more resources) or horizontally (more replicas) if you experience backpressure.

* Optimize Elasticsearch performance by checking for indexing delays, rejected bulk requests, or cluster resource limits. Bottlenecks in {{es}} often manifest as Collector export timeouts.

:::{tip}
Focus tuning efforts on the Collector’s resource allocation and the downstream Elasticsearch cluster rather than queue parameters for v0.138.0+.
:::

## Resources

* [Upstream documentation - OpenTelemetry Collector configuration](https://opentelemetry.io/docs/collector/configuration)
* [Elasticsearch exporter configuration reference](elastic-agent://reference/edot-collector/components/elasticsearchexporter.md)