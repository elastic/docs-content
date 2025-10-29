---
navigation_title: 429 errors when using the mOTLP endpoint
description: Resolve HTTP 429 `Too Many Requests` errors when sending data through the Elastic Cloud Managed OTLP (mOTLP) endpoint in Elastic Cloud Serverless or Elastic Cloud Hosted (ECH).
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_collector:
products:
  - id: cloud-serverless
  - id: cloud-hosted
  - id: observability
  - id: edot-collector
---

# 429 errors when using the Elastic Cloud Managed OTLP Endpoint

When sending telemetry data through the {{motlp}} (mOTLP), you might encounter HTTP `429 Too Many Requests` errors. These indicate that your ingest rate has temporarily exceeded the rate or burst limits configured for your Elastic Cloud project.

This issue can occur in both Elastic Cloud Serverless and {{ech}} (ECH) environments.

## Symptoms

You might see log messages similar to the following in your EDOT Collector output or SDK logs:

```json
{
  "code": 8,
  "message": "error exporting items, request to <ingest endpoint> responded with HTTP Status Code 429"
}
```

In some cases, you may also see warnings or backpressure metrics increase in your Collector’s internal telemetry (for example, queue length or failed send count).

## Causes

A 429 status means that the rate of requests sent to the Managed OTLP endpoint has exceeded allowed thresholds. This can happen for several reasons:

* Your telemetry pipeline is sending data faster than the allowed ingest rate.
* Bursts of telemetry data exceed the short-term burst limit, even if your sustained rate is within limits.

    The specific limits depend on your environment:

    | Deployment type | Rate limit | Burst limit |
    |-----------------|------------|-------------|
    | Serverless      | 15 MB/s    | 30 MB/s     |
    | ECH             | Depends on deployment size and available {{es}} capacity | Depends on deployment size and available {{es}} capacity |

    Exact limits depend on your subscription tier.
    Refer to the [Rate limiting section](opentelemetry://reference/motlp.md#rate-limiting) in the mOTLP reference documentation for details.

* In {{ech}}, the {{es}} capacity for your deployment might be underscaled for the current ingest rate.
* In Elastic Cloud Serverless, rate limiting should not result from {{es}} capacity, since the platform automatically scales ingest capacity. If you suspect a scaling issue, [contact Elastic Support](contact-support.md).
* Multiple Collectors or SDKs are sending data concurrently without load balancing or backoff mechanisms.

## Resolution

To resolve 429 errors, identify whether the bottleneck is caused by ingest limits or {{es}} capacity.

### Scale your deployment or request higher limits

If you’ve confirmed that your ingest configuration is stable but still encounter 429 errors:

* Elastic Cloud Serverless: [Contact Elastic Support](contact-support.md) to request an increase in ingest limits.
* {{ech}} (ECH): Increase your {{es}} capacity by scaling or resizing your deployment:
  * [Scaling considerations](../../../deploy-manage/production-guidance/scaling-considerations.md)
  * [Resize deployment](../../../deploy-manage/deploy/cloud-enterprise/resize-deployment.md)
  * [Autoscaling in ECE and ECH](../../../deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md)

After scaling, monitor your ingest metrics to verify that the rate of accepted requests increases and 429 responses stop appearing.

### Reduce ingest rate or enable backpressure

Lower the telemetry export rate by enabling batching and retry mechanisms in your EDOT Collector or SDK configuration. For example:

```yaml
processors:
  batch:
    send_batch_size: 1000
    timeout: 5s

exporters:
  otlp:
    retry_on_failure:
      enabled: true
      initial_interval: 1s
      max_interval: 30s
      max_elapsed_time: 300s
```

These settings help smooth out spikes and automatically retry failed exports after rate-limit responses.

### Enable retry logic and queueing

To minimize data loss during temporary throttling, configure your exporter to use a sending queue and retry logic. For example:

```yaml
exporters:
  otlp:
    sending_queue:
      enabled: true
      num_consumers: 10
      queue_size: 1000
    retry_on_failure:
      enabled: true
```

This ensures the Collector buffers data locally while waiting for the ingest endpoint to recover from throttling.

## Best practices

To prevent 429 errors and maintain reliable telemetry data flow, implement these best practices:

* Monitor internal Collector metrics (such as `otelcol_exporter_send_failed` and `otelcol_exporter_queue_capacity`) to detect backpressure early.
* Distribute telemetry load evenly across multiple Collectors instead of sending all data through a single instance.
* When possible, enable batching and compression to reduce payload size.
* Keep retry and backoff intervals conservative to avoid overwhelming the endpoint after a temporary throttle.

## Resources

* [{{motlp}} reference](opentelemetry://reference/motlp.md)
* [Quickstart: Send OTLP data to Elastic Serverless or {{ech}}](../../../solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md)