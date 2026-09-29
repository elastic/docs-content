---
navigation_title: Logs
description: Collect, process, explore, and store logs in Elastic Observability, with the recommended path for each step and the alternatives that fit specific constraints.
applies_to:
  stack: ga
  serverless:
    observability: ga
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/logs-checklist.html
  - https://www.elastic.co/guide/en/serverless/current/observability-log-monitoring.html
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Logs [logs-checklist]

Elastic lets you collect logs from hosts, containers, cloud services, and applications, give them structure, search them at any scale, and alert on what matters. Use this page to find what you need to set up your logs in Elastic, whether you're starting from new, working with existing data in {{es}}, or migrating an existing logging stack. If you ship logs from a service you own, start with [Application logs](/solutions/observability/logs/ingest.md#logs-ingest-application).

This page covers:

- [Sending logs to Elastic](#logs-send): get a first source flowing, then choose the ingest path for each source and your deployment type.
- [Migrating logs to Elastic](#logs-migrate): move from another logging tool without losing the searches and alerts you rely on.
- [Processing unstructured logs](#logs-process): decide where raw messages get turned into fields and how logs are routed.
- [Working with existing logs](#logs-work-with): explore and alert on logs, and manage how they're stored.

## Send logs to Elastic [logs-send]

For a new setup, collect logs with {{agent}} in OTel mode. [Ingest logs](/solutions/observability/logs/ingest.md) covers the endpoint for your deployment type and when an integration, {{filebeat}}, or {{ls}} is the better fit.

[Get started with logs](/solutions/observability/logs/get-started.md)
:   Get one log source flowing and see it in **Discover** in minutes with a quickstart for your deployment type and environment. Start here if you're evaluating Elastic or want a working pipeline before you plan the full setup, then continue to Ingest logs.

[Ingest logs](/solutions/observability/logs/ingest.md)
:   Choose the collector, endpoint, and schema for each log source, with the recommended path per deployment type and the cases where an alternative fits.

## Migrate logs to Elastic [logs-migrate]

If you already run another logging platform, you don't have to switch everything at once. Elastic accepts logs over OTLP, from {{agent}} and {{beats}}, from {{ls}}, and through the bulk API, so you can send the same logs to both systems while you rebuild what your team depends on.

[Migrate logs to Elastic](/solutions/observability/logs/migrate.md)
:   Move from Splunk, Datadog, Grafana Loki, or another logging tool. Run Elastic alongside it, send the same logs to both, and switch over when your searches and alerts are rebuilt.

## Process unstructured logs [logs-process]

Raw, unstructured logs can't be aggregated, filtered, or alerted on by field. Parse them at the source when you own the application, or parse them in Streams or ingest pipelines when you don't.

[Process logs](/solutions/observability/logs/process.md)
:   Turn unstructured messages into fields you can filter and aggregate on, and route logs into the data streams you want. Determine where to parse your logs and why it matters.

## Explore and manage existing logs [logs-work-with]

Once logs are in {{es}}, **Discover** is where you search, filter, and investigate them. Settings in the data streams they're sent to decide what they cost to keep. Use these pages to find answers in your logs and to keep storage predictable.

[Explore logs](/solutions/observability/logs/explore-logs.md)
:   Search, filter, and tail logs in **Discover**, aggregate them with {{esql}}, find patterns and anomalies, and alert on log conditions.

[Manage logs storage](/solutions/observability/logs/manage-storage.md)
:   Keep storage predictable with {{es}} logsdb index mode, the default `logs` index template, retention per stream, and data set quality monitoring.

## Related pages [logs-related]

The following related pages provide more background on working with logs in Elastic:

- [Start using OpenTelemetry with Elastic](/solutions/observability/get-started/opentelemetry/start-with-otel.md): why {{agent}} in OTel mode is the recommended collector, and when to keep using classic Elastic components.
- [{{obs-serverless}} feature tiers](/solutions/observability/observability-serverless-feature-tiers.md): what the Logs Essentials tier includes compared to {{observability}} Complete.
- [Streams](/solutions/observability/streams/streams.md): the {{kib}} Process, route, and manage data retention from the {{kib}} UI.
- [Troubleshoot logs](/troubleshoot/observability/troubleshoot-logs.md): fixes for errors you might encounter while onboarding logs.
