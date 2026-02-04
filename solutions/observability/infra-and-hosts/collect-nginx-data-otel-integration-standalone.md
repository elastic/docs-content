---
navigation_title: Collect NGINX logs and metrics with hybrid standalone agent
description: Collect NGINX logs and metrics with a hybrid standalone Elastic Agent using Elastic's Nginx integration and NGINX OpenTelemetry Input Package.
applies_to:
  stack: preview 9.2+
  serverless: preview
products:
  - id: fleet
  - id: elastic-agent
---

# Collect NGINX logs and metrics with a hybrid standalone {{agent}}

Follow this guide to learn how to configure a standalone {{agent}} on a Linux host to collect:

- NGINX logs with Elastic's [Nginx integration](https://www.elastic.co/docs/reference/integrations/nginx), based on the [Elastic Common Schema](ecs://reference/index.md) (ECS)
- NGINX metrics with Elastic's [NGINX OpenTelemetry Input Package](https://www.elastic.co/docs/reference/integrations/nginx_otel_input), which uses the [`nginxreceiver`](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/nginxreceiver) OpenTelemetry (OTel) Collector receiver

## Prerequisites [collect-nginx-data-standalone-prereqs]

::::{include} _snippets/collect-nginx-data-prerequisites.md
::::

## Configure the NGINX status endpoint [collect-nginx-data-standalone-status-endpoint]

::::{include} _snippets/collect-nginx-data-status-endpoint.md
::::

## Configure the hybrid standalone agent policy [collect-nginx-data-standalone-policy]

TODO

## Validate your data [collect-nginx-data-standalone-validate]

After you apply the policy changes, validate that both the ECS-based logs and the OTel-based metrics are flowing in.

:::::{stepper}

::::{step} Validate the log collection

1. In {{kib}}, go to **Discover**, then filter the results using the KQL search bar.
2. Search for NGINX data stream datasets such as `nginx.access` and `nginx.error`, or enter:

   ```
   data_stream.dataset : "nginx.access" or "nginx.error"
   ```

3. Go to **Dashboards**, then select **[Logs Nginx] Access and error logs** to view the dashboard installed with the Nginx integration.

::::

::::{step} Validate the metrics collection

Go to **Dashboards**, then select **[Metrics Nginx OTEL] Overview** to view the dashboard for visualizing OTel-based metrics.

This dashboard is provided by the NGINX OpenTelemetry Assets content package, installed automatically when data is ingested through the NGINX OpenTelemetry Input Package.

::::

:::::

## Related pages [collect-nginx-data-standalone-related]

- [Collect OpenTelemetry data with {{agent}} integrations](/reference/fleet/otel-integrations.md)
- [Collect NGINX logs and metrics with a hybrid {{fleet}}-managed {{agent}}](/solutions/observability/infra-and-hosts/collect-nginx-data-otel-integration-fleet-managed.md)
- [Elastic integrations](integration-docs://reference/index.md)
