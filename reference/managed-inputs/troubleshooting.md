---
navigation_title: Troubleshooting
description: Resolve common issues when sending data to the Elastic Cloud Managed OTLP Endpoint.
applies_to:
  serverless:
    observability: ga
    security: ga
  deployment:
    ech: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Managed OTLP Endpoint troubleshooting

The following sections provide troubleshooting information for the Elastic Cloud Managed OTLP Endpoint.

## You don't have a collector or SDK running

### Symptoms

- No telemetry data appears in Elastic.
- You haven't set up an OpenTelemetry collector or SDK yet.

### Resolution

Set up an {{agent}} using one of the quickstart guides:

- [Kubernetes Quickstart](https://www.elastic.co/docs/solutions/observability/get-started/opentelemetry/quickstart/serverless/k8s)
- [Hosts & VMs Quickstart](https://www.elastic.co/docs/solutions/observability/get-started/opentelemetry/quickstart/serverless/hosts_vms)
- [Docker Quickstart](https://www.elastic.co/docs/solutions/observability/get-started/opentelemetry/quickstart/serverless/docker)

## API key prefix not found

### Symptoms

The following error appears in your collector or SDK logs:

```txt
Exporting failed. Dropping data.
{"kind": "exporter", "data_type": }
"Unauthenticated desc = ApiKey prefix not found"
```

### Resolution

Format your API key correctly. The format depends on whether you're using a collector or SDK:

- **Collector configuration**: `"Authorization": "ApiKey <api-key-value-here>"`
- **SDK environment variable**: `"Authorization=ApiKey <api-key>"`

## Error: Too many requests

### Symptoms

- HTTP `429 Too Many Requests` errors appear when sending data.
- Log messages indicate rate limiting from the mOTLP endpoint.

### Resolution

Your project might be hitting ingest rate limits. Refer to the dedicated [429 errors when using the Elastic Cloud Managed OTLP Endpoint](https://www.elastic.co/docs/troubleshoot/ingest/opentelemetry/429-errors-motlp) troubleshooting guide for details on causes, rate limits, and solutions.

## Error: Payload too large

### Symptoms

- HTTP `413 Payload Too Large` errors appear when sending data.
- gRPC errors indicate the request or response exceeded the maximum message size.
- Errors happen more often when traffic spikes, or when individual telemetry items are large.

### Resolution

Reduce the payload size sent by your collector by lowering batching limits. In the {{agent}} (and upstream or contrib collectors), you can reduce the maximum batch size (in uncompressed bytes) so each request stays smaller.

For configuration guidance and the recommended batching settings for sending data to the Elastic Cloud Managed OTLP Endpoint, refer to [Batching configuration for contrib OpenTelemetry Collector](elastic-agent://reference/edot-collector/config/default-config-standalone.md#batching-configuration-for-contrib-opentelemetry-collector).

## Server errors (5XX)

```{applies_to}
ech:
```

### Symptoms

- HTTP `5XX` errors (such as `500`, `502`, or `503`) appear when sending data.
- Data ingestion is intermittent or fails completely.
- Errors might correlate with periods of high traffic.

### Resolution

Server errors can indicate that your {{es}} cluster is undersized for the current workload. Use [AutoOps](#use-autoops-to-diagnose-issues) to check:

- **CPU usage**: High CPU utilization suggests the cluster needs more processing capacity.
- **Memory usage**: High memory pressure can cause instability and errors.
- **Active alerts**: Check for events indicating resource constraints.

If metrics confirm the cluster is under-resourced, scale your deployment:

- [Scaling considerations](/deploy-manage/production-guidance/scaling-considerations.md)
- [Resize deployment](/deploy-manage/deploy/cloud-enterprise/resize-deployment.md)
- [Autoscaling in ECE and ECH](/deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md)

## Use AutoOps to diagnose issues

```{applies_to}
ech:
```

[AutoOps](/deploy-manage/monitor/autoops.md) is a diagnostic tool available for {{ech}} deployments that analyzes cluster metrics, provides root-cause analysis, and suggests resolution paths. 

AutoOps can help you identify and resolve issues that affect mOTLP data ingestion, including 429 rate limiting errors and 5XX server errors caused by undersized clusters.

### Diagnose traffic and resource issues

When your deployment receives excessive traffic or lacks sufficient resources, AutoOps detects patterns that often precede or accompany ingestion errors:

- **Index queue is high**: Usually the first indicator that your deployment lacks sufficient resources for the current data volume.
- **CPU utilization is high**: Often follows high index queue, as processing incoming telemetry data is CPU-intensive.
- **Unbalanced node load**: Some data nodes are more loaded than others, indicating potential scaling or routing issues.

### Access AutoOps

AutoOps is accessible from the {{ecloud}} console. From your deployment, select **AutoOps** in the navigation menu to view cluster status, active events, and resource metrics.

To check node-level metrics like CPU, memory, and write queue, go to **AutoOps Monitoring → Nodes**.

:::{note}
AutoOps availability depends on your cloud provider and region. Refer to [AutoOps regions](/deploy-manage/monitor/autoops.md#regions-where-autoops-is-available) for details.
:::

### Set up notifications

AutoOps can alert you when events occur in your cluster. To get started:

1. Add at least one connector (Slack, PagerDuty, MS Teams, or webhook).
2. Configure notification filters to include or exclude specific events.

AutoOps delivers all events occurring across your deployments through the configured connectors.

For more information, refer to [AutoOps](/deploy-manage/monitor/autoops.md).

## Provide feedback

Help improve the Elastic Cloud Managed OTLP Endpoint by sending us feedback in our [discussion forum](https://discuss.elastic.co/c/apm) or [community Slack](https://elasticstack.slack.com/signup#/domain-signup).

For {{agent}} feedback, open an issue in the [elastic-agent repository](https://github.com/elastic/elastic-agent/issues).
