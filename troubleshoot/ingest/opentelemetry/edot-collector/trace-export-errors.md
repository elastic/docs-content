---
navigation_title: Export errors from the EDOT Collector
description: Learn how to resolve export failures caused by `sending_queue` overflow and Elasticsearch exporter timeouts in the EDOT Collector.
applies_to:
  serverless: ga
  product:
    edot_collector: ga  
products:
  - id: observability
  - id: edot-collector
---

# Export failures when sending telemetry data from the EDOT Collector

During high traffic or load testing scenarios, the EDOT Collector might fail to export telemetry data (traces, metrics, or logs) to {{es}}. This typically happens when the internal queue for outgoing data fills up faster than it can be drained, resulting in timeouts and dropped data.

If you're experiencing network connectivity issues, refer to [Connectivity issues](/troubleshoot/ingest/opentelemetry/connectivity.md). If no data appears in {{kib}}, refer to [No data visible in {{kib}}](/troubleshoot/ingest/opentelemetry/no-data-in-kibana.md).

## Symptoms

You might see one or more of the following messages in the EDOT Collector logs:

* `bulk indexer flush error: failed to execute the request: context deadline exceeded`
* `Exporting failed. Rejecting data. sending queue is full`

These errors indicate the Collector is overwhelmed and unable to export data fast enough, leading to queue overflows and data loss.

## Causes

This issue typically occurs when the `sending_queue` configuration or the Elasticsearch cluster scaling is misaligned with the incoming telemetry volume.  

:::{important}
{applies_to}`stack: ga 9.0, deprecated 9.3`
The sending queue is turned off by default. Verify that `enabled: true` is explicitly set — otherwise any queue configuration will be ignored.
:::

Common contributing factors include:

* Underscaled Elasticsearch cluster is the most frequent cause of persistent export failures. If Elasticsearch cannot index data fast enough, the Collector’s queue fills up.
* {applies_to}`stack: ga 9.0, deprecated 9.3` `sending_queue.block_on_overflow` is turned off (defaults to `false`), which can lead to data drops.
* Sending queue is enabled but `num_consumers` is too low to keep up with the incoming data volume.
* Sending queue size (`queue_size`) is too small for the traffic load.
* Both internal and sending queue batching are disabled, increasing processing overhead.
* EDOT Collector resources (CPU, memory) are insufficient for the traffic volume.

:::{note}
Increasing the `timeout` value (for example from 30s to 90s) doesn't help if the queue itself or Elasticsearch throughput is the bottleneck.
:::

## Resolution

The resolution approach depends on your {{stack}} version and Collector configuration.

### When the sending queue is not enabled by default
{applies_to}`stack: ga 9.0, deprecated 9.3`

Enable the sending queue and block on overflow to prevent data drops:

```yaml
sending_queue:
  enabled: true
  queue_size: 1000
  num_consumers: 10
  block_on_overflow: true
```

### When the sending queue is enabled by default
{applies_to}`stack: ga 9.3`

The Elasticsearch exporter provides default `sending_queue` parameters (including `block_on_overflow: true`) but these can and often should be tuned for specific workloads.

The following steps can help identify and resolve export bottlenecks:

:::::{stepper}

::::{step} Check the Collector's internal metrics

If internal telemetry is enabled, review these metrics:

* `otelcol.elasticsearch.bulk_requests.latency` — high tail latency suggests Elasticsearch is the bottleneck. Check Elasticsearch cluster metrics and scale if necessary.

* `otelcol.elasticsearch.bulk_requests.count` and `otelcol.elasticsearch.flushed.bytes` — they help assess whether the Collector is sending too many or too large requests. Tune `sending_queue.num_consumers` or batching configuration to balance throughput.

* `otelcol_exporter_queue_size` and `otelcol_exporter_queue_capacity` — if the queue runs near capacity, but Elasticsearch is healthy, increase the queue size or number of consumers.

* `otelcol_enqueue_failed_spans`, `otelcol_enqueue_failed_metric_points`, `otelcol_enqueue_failed_log_records` — persistent enqueue failures indicate undersized queues or slow consumers.

For a complete list of available metrics, refer to the upstream OpenTelemetry metadata files for the [Elasticsearch exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/exporter/elasticsearchexporter/metadata.yaml) and [exporter helper](https://github.com/open-telemetry/opentelemetry-collector/blob/main/exporter/exporterhelper/metadata.yaml).
::::

::::{step} Scale the Collector's resources

* Ensure sufficient CPU and memory for the EDOT Collector.
* Scale vertically (more resources) or horizontally (more replicas) as needed.

For Kubernetes deployments, refer to [Insufficient resources in Kubernetes](/troubleshoot/ingest/opentelemetry/edot-collector/insufficient-resources-kubestack.md) for detailed resource configuration guidance.
::::

::::{step} Optimize Elasticsearch performance

Address indexing delays, rejected bulk requests, or shard imbalances that limit ingestion throughput.
::::

:::::

:::{tip}
{applies_to}`stack: ga 9.3`
Focus tuning efforts on {{es}} performance, Collector resource allocation, and queue sizing informed by the internal telemetry metrics above.
:::


For more detailed diagnostics, refer to [Enable debug logging](/troubleshoot/ingest/opentelemetry/edot-collector/enable-debug-logging.md) to troubleshoot export failures.

## Resources

* [Upstream documentation - OpenTelemetry Collector configuration](https://opentelemetry.io/docs/collector/configuration)
* [Elasticsearch exporter configuration reference](elastic-agent://reference/edot-collector/components/elasticsearchexporter.md)