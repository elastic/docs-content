---
navigation_title: Rate limiting
description: Rate limiting for Elastic Cloud managed inputs.
applies_to:
  serverless: ga
  deployment:
    ech: ga
products:
  - id: cloud-serverless
  - id: cloud-hosted
  - id: observability
  - id: security
---

# Managed inputs rate limiting [rate-limiting]

Rate limiting occurs when a managed input receives data faster than it can process and index into {{es}}. The endpoint responds with HTTP `429` errors until the data volume is reduced.

## How rate limiting works [how-rate-limiting-works]

Rate limiting behavior differs by deployment type:

- **{{ech}}**: Rate limits depend on your {{es}} cluster capacity. If your cluster can't keep up with incoming data, the endpoint starts rejecting requests with `429` errors.
- **{{serverless-full}}**: Elastic manages scaling automatically. Rate limiting is rare and typically indicates a temporary event to protect our system.

## Identifying rate limiting [identifying-rate-limiting]

When rate limiting occurs, the managed input responds with an HTTP `429` Too Many Requests status code.

For the [Managed OTLP Endpoint](managed-otlp-endpoint.md), a log message similar to this can appear in the OpenTelemetry Collector's output:

```
"error": "rpc error: code = ResourceExhausted desc = request exceeded available capacity"
```

For OTLP troubleshooting steps, refer to [Error: too many requests](./troubleshooting.md#error-too-many-requests).

{{es}} output shippers such as {{product.beats}}, {{product.elastic-agent}}, and {{product.logstash}} typically retry `429` responses automatically with backoff. Configure your shipper to queue data so transient rejections don't lose data.

## Resolving rate limiting [resolving-rate-limiting]

### {{ech}} deployments

For {{ech}} deployments, `429` errors typically indicate that your {{es}} cluster is undersized for the current data volume. If [AutoOps](./troubleshooting.md#use-autoops-to-diagnose-issues) is available in your region, use it to check latency, CPU utilization, index queue depth, and node load to confirm whether your cluster is under-resourced. If AutoOps is not available in your region, [contact Elastic Support](/troubleshoot/ingest/opentelemetry/contact-support.md).

When {{es}} latency exceeds 6 seconds, managed inputs reduce concurrency and return HTTP `429` errors.

If metrics confirm the cluster needs more capacity, scale your deployment:

- [Scaling considerations](/deploy-manage/production-guidance/scaling-considerations.md)
- [Resize deployment](/deploy-manage/deploy/cloud-enterprise/resize-deployment.md)
- [Autoscaling in ECE and ECH](/deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md)

Once your {{es}} capacity is scaled up or is able to accept the incoming data volume, requests to managed inputs will be accepted again.

### {{serverless-full}} deployments

For {{serverless-full}} projects, Elastic manages scaling automatically. If you experience persistent `429` errors, [contact Elastic Support](/troubleshoot/ingest/opentelemetry/contact-support.md).
