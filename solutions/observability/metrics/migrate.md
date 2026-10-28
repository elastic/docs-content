---
navigation_title: Migrate to Elastic
description: Move an existing Prometheus or Datadog metrics stack to Elastic by running both systems side by side and switching over gradually.
applies_to:
  stack: ga
  serverless:
    observability:
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Migrate metrics to Elastic [metrics-migrate]

Elastic supports migration paths from Prometheus and Datadog. Because Elastic accepts OpenTelemetry Protocol (OTLP) and Prometheus remote write, you can run Elastic alongside your existing setup and migrate gradually, without switching everything at once. Follow the guide for the stack you're moving from:

[Migrate from Prometheus](/solutions/observability/metrics/migrate/prometheus.md)
:   Keep Prometheus scraping and add Elastic as a remote write target. Explore the metrics in {{kib}} while your Grafana dashboards and PromQL keep working.

[Migrate from Datadog](/solutions/observability/metrics/migrate/datadog.md)
:   Send OpenTelemetry metrics to Elastic, replace Datadog Agent host and {{k8s}} collection, and rebuild the dashboards and monitors you still need.

If you collect metrics with {{metricbeat}} or {{agent}} integrations and want to move to OpenTelemetry, refer to [Move from {{metricbeat}} or {{agent}} integrations](#metrics-migrate-metricbeat) for the migration steps.

## Move from {{metricbeat}} or {{agent}} integrations [metrics-migrate-metricbeat]

{{metricbeat}} and {{agent}} integrations produce ECS data and aren't deprecated, so you don't have to move. If you want OpenTelemetry-native metrics, first move standalone {{beats}} to {{fleet}}-managed {{agent}}. {{agent}} runs Beat inputs as Beat receivers inside its embedded Collector, so your ECS data, dashboards, and alerts keep working. Then replace Beat receivers with OTel-native receivers one data source at a time. Data from Beat receivers stays ECS. Only OTel-native receivers produce OpenTelemetry data.

Refer to [Migrate from {{beats}} to {{agent}}](/reference/fleet/migrate-from-beats-to-elastic-agent.md) for the first step and to [{{agent}} as an OpenTelemetry Collector](/reference/fleet/elastic-agent-as-otel-collector.md) for the Beat receiver rollout and OTel-native receivers.
