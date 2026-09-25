---
navigation_title: Migrate to Elastic
description: Move logs from another logging platform to Elastic by sending the same logs to both systems, rebuilding searches and alerts, and switching over when they match.
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Migrate logs to Elastic [logs-migrate]

If you already run a logging platform such as Splunk, Datadog, or Grafana Loki, you don't have to switch everything at once. Elastic accepts logs over the OpenTelemetry Protocol (OTLP), from {{agent}} and {{beats}}, from {{ls}}, and through the bulk API, so you can send the same logs to both systems, rebuild what your team relies on in Elastic, and stop the old stream when nothing is missing.

This page covers the sequence. The pages it links to cover each step.

## Before you begin [logs-migrate-prereqs]

- An Elastic deployment that can receive logs, and the collection path for it from [Ingest logs](/solutions/observability/logs/ingest.md).
- An inventory of what you're replacing: the log sources, the searches and dashboards people use, and the alerts that page someone.
- Your existing platform left running. You'll keep sending to it until the last step.

## Migration sequence [logs-migrate-sequence]

:::::{stepper}

::::{step} Send the same logs to Elastic

Add Elastic as a second destination without removing the first:

- **Your logs already pass through an OpenTelemetry Collector.** Add an OTLP exporter that points at Elastic and attach it to the same logs pipeline. The endpoint depends on your deployment type. Refer to [Endpoint by deployment type](/solutions/observability/logs/ingest.md#logs-ingest-endpoints).
- **A vendor agent collects your logs.** Elastic doesn't read another vendor's agent protocol. Install {{agent}} in OTel mode alongside it and collect the same files or sources. Follow [Get started with logs](/solutions/observability/logs/get-started.md) for the quickstart, or [Ingest logs](/solutions/observability/logs/ingest.md) for the full set of paths.
- **You already run {{ls}} or {{beats}}.** Add an {{es}} output next to the existing one. Refer to [Other ways to collect logs](/solutions/observability/logs/ingest.md#logs-ingest-other).

Confirm the logs arrive in **Discover** before you move on. Refer to [Explore logs](/solutions/observability/logs/explore-logs.md).
::::

::::{step} Give the logs the fields your searches need

Field names differ between platforms, so a search that worked before won't match until the same fields exist in Elastic. Parse the logs in Streams or keep the raw message and query it with {{esql}} while you decide. Refer to [Process logs](/solutions/observability/logs/process.md).
::::

::::{step} Rebuild searches, dashboards, and alerts

Elastic has no importer for another platform's saved searches, dashboards, or alert rules. Recreate the ones people still use, starting with the alerts:

- Searches and dashboards: [Explore logs](/solutions/observability/logs/explore-logs.md) and [Create a dashboard](/explore-analyze/dashboards/create-dashboard.md).
- Alerts: the [log threshold rule](/solutions/observability/incident-management/create-log-threshold-rule.md) {applies_to}`serverless: unavailable` and the [custom threshold rule](/solutions/observability/incident-management/create-custom-threshold-rule.md). Refer to [Alert on logs](/solutions/observability/logs/explore-logs.md#logs-explore-alert) for which one fits.
::::

::::{step} Set retention, then switch over

Set retention per stream so the new data streams don't keep everything forever. Refer to [Manage logs storage](/solutions/observability/logs/manage-storage.md). When every alert you kept fires from Elastic and the dashboards your team opens are rebuilt, stop sending to the old platform.
::::

:::::

## Related pages [logs-migrate-related]

- [Ingest logs](/solutions/observability/logs/ingest.md)
- [Migrate from {{beats}} to {{agent}}](/reference/fleet/migrate-from-beats-to-elastic-agent.md)
