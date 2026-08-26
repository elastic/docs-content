---
navigation_title: Start using OpenTelemetry
description: A decision-first guide for adopting OpenTelemetry with Elastic. Choose your ingestion path based on your deployment, then follow the right quickstart for your environment.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_collector: ga
products:
  - id: cloud-serverless
  - id: cloud-hosted
  - id: observability
  - id: edot-collector
---

# Start using OpenTelemetry with Elastic [start-with-otel]

This guide helps you choose the right setup for your environment so you can start sending metrics, logs, and traces to Elastic using {{edot}}. {{edot}} is Elastic's fully supported, pre-configured distribution of the upstream OpenTelemetry tools, optimized for Elastic ingest and analysis.

## Before you begin [start-with-otel-prereqs]

EDOT SDKs and {{agent}} in OTel mode require {{stack}} 8.16 or later for basic compatibility. For a supported configuration, use:

* {{stack}} 9.x, or
* {{stack}} 8.18 or 8.19 with {{agent}} version 9.x. You have to keep your configuration aligned to your Stack version, not the {{agent}} 9.x defaults.

{{serverless-full}} has no version requirements.

Refer to [{{agent}} and {{stack}} compatibility](opentelemetry://reference/compatibility/collectors.md) for the full matrix.

## What you want to observe [start-with-otel-what-to-send]

Your setup depends on the telemetry you collect:

* **Application telemetry** (traces, metrics, and logs from your code): use an EDOT language SDK. It auto-instruments your application with zero or minimal code changes.
* **Infrastructure telemetry** (host metrics, logs, {{k8s}} signals): use {{agent}} to collect system-level data from your hosts, containers, or cluster.
* **Both application and infrastructure telemetry**: most production setups collect application and infrastructure telemetry together. You can run an EDOT SDK and {{agent}} on the same host.

## Your Elastic deployment [start-with-otel-ingestion-path]

The recommended ingestion path depends on your Elastic deployment type. Select your deployment to see the recommended setup.

::::{important}
Regardless of your deployment, do not point EDOT SDKs directly at the {{product.apm-server}} OpenTelemetry intake endpoint, as this configuration is [not supported](opentelemetry://reference/edot-sdks/index.md). EDOT SDKs work only when sending data through {{agent}} or the {{motlp}}.
::::

:::::{applies-switch}

::::{applies-item} serverless:

**Send data to the {{motlp}}.**

The {{motlp}} is GA for {{serverless-full}} {{observability}} and Security projects. {{agent}} is not required for application telemetry, you can just point your EDOT SDK or any OTLP-compatible exporter directly at the managed endpoint.

For infrastructure telemetry (host metrics, logs, {{k8s}}), run {{agent}} on your hosts or cluster and configure it to export data to the {{motlp}} using the OTLP exporter.

Before committing to this path, note these {{motlp}} limitations:

* Tail-based sampling (TBS) is not available. Configure head-based sampling at the edge before sending data.
* Universal Profiling is not available.

Refer to [{{motlp}}](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md) for the full list of limitations and configuration details.
::::

::::{applies-item} ess:

**Send data to the {{motlp}}.**

The {{motlp}} is GA on {{ech}}. For application telemetry only, send directly from your EDOT SDK or any OTLP-compatible exporter to the endpoint, with no {{agent}} required. For infrastructure telemetry, run {{agent}} on your hosts or cluster and configure it to export to the {{motlp}} using the OTLP exporter.

:::{note}
The current {{ech}} quickstarts use a different path: an {{agent}} running on a host and writing directly to {{es}} using the `elasticsearch` exporter. This alternative works, but for new setups, use the mOTLP path. For more information, refer to [Send OTLP data to the {{motlp}}](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md).
:::

Before committing to this path, note these {{motlp}} limitations:

* Tail-based sampling (TBS) is not available. Configure head-based sampling at the edge before sending data.
* Universal Profiling is not available.

Refer to [{{motlp}}](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md) for the full list of limitations and configuration details.
::::

::::{applies-item} self:

**Run {{agent}} in gateway mode.**

The {{motlp}} is not available for self-managed Elastic, ECE, or ECK deployments. You need an {{agent}} running as a [gateway](elastic-agent://reference/edot-collector/modes.md).

{{agent}} running as a gateway is required for full {{product.apm}} functionality. It:

* Exposes an OTLP endpoint that edge collectors, EDOT SDKs, and other OTLP sources send data to.
* {applies_to}`edot_collector: ga 9.2+` Runs the `elasticapm` processor to enrich trace data with attributes the {{product.observability}} UIs rely on.
* {applies_to}`edot_collector: ga 9.0-9.1` Runs the `elastictrace` processor to enrich trace data with attributes.
* Runs the `elasticapm` connector to generate pre-aggregated {{product.apm}} metrics from traces.
* Routes telemetry to the correct data streams and writes to {{es}} using the `elasticsearch` exporter in the `otel` mapping mode.

For edge collectors running on your hosts, Kubernetes nodes, or alongside your applications, use the OTLP exporter to forward data to the gateway. The `elasticsearch` exporter is only recommended for the gateway itself, not for edge collectors.

Refer to [{{agent}} modes](elastic-agent://reference/edot-collector/modes.md) and [Default standalone configurations](elastic-agent://reference/edot-collector/config/default-config-standalone.md) for step-by-step setup.
::::

:::::

## Quickstart for your environment [start-with-otel-quickstarts]

Use the quickstart that matches your deployment and environment:

| Deployment model | Kubernetes | Docker | Hosts or VMs |
|---|---|---|---|
| {{product.self}} Stack | [K8s on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/k8s.md) | [Docker on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/docker.md) | [Hosts on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/hosts_vms.md) |
| {{serverless-full}} | [K8s on serverless](/solutions/observability/get-started/opentelemetry/quickstart/serverless/k8s.md) | [Docker on serverless](/solutions/observability/get-started/opentelemetry/quickstart/serverless/docker.md) | [Hosts on serverless](/solutions/observability/get-started/opentelemetry/quickstart/serverless/hosts_vms.md) |
| {{ech}} | [K8s on hosted](/solutions/observability/get-started/opentelemetry/quickstart/ech/k8s.md) | [Docker on hosted](/solutions/observability/get-started/opentelemetry/quickstart/ech/docker.md) | [Hosts on hosted](/solutions/observability/get-started/opentelemetry/quickstart/ech/hosts_vms.md) |

To send OTLP data directly to {{serverless-full}} or {{ech}} without running {{agent}}, follow [Send OTLP data to the {{motlp}}](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md).

## Instrument your applications [start-with-otel-sdks]

After setting up an ingestion path, add an EDOT language SDK to your application. Each SDK auto-instruments your application and sends OTLP data to your configured endpoint.

:::{important}
Avoid running an EDOT SDK alongside any other {{product.apm}} agent in the same application process. Running multiple agents can cause conflicting instrumentation, duplicate telemetry, or other unexpected behavior.
:::

Available EDOT SDKs (all GA unless noted):

* [EDOT Java](elastic-otel-java://reference/edot-java/setup/index.md)
* [EDOT .NET](elastic-otel-dotnet://reference/edot-dotnet/setup/index.md)
* [EDOT Node.js](elastic-otel-node://reference/edot-node/setup/index.md)
* [EDOT Python](elastic-otel-python://reference/edot-python/setup/index.md)
* [EDOT PHP](elastic-otel-php://reference/edot-php/setup/index.md)
* [EDOT Android](apm-agent-android://reference/edot-android/index.md)
* [EDOT iOS](apm-agent-ios://reference/edot-ios/index.md)
* {applies_to}`edot_browser: preview` [EDOT Browser](elastic-otel-rum-js://reference/edot-browser/index.md). For production real user monitoring, continue using the [classic Elastic {{product.apm}} browser agent](apm-agent-rum-js://reference/index.md).

For languages without an EDOT SDK (Go, C++, Ruby, and others), you can use the [contrib OpenTelemetry SDKs](/solutions/observability/apm/opentelemetry/upstream-opentelemetry-collectors-language-sdks.md). These work with Elastic over OTLP but receive community support only.

## Known limitations [start-with-otel-caveats]

### Use the OTLP exporter at the edge [start-with-otel-otlp-exporter]

Configure your EDOT SDKs and edge {{agent}} instances to use the OTLP exporter. Elastic recommends the `elasticsearch` exporter only for the {{agent}} gateway in a self-managed deployment. Using it at the edge can lead to data loss or incorrect mapping.

### Know when to keep using classic Elastic components [start-with-otel-when-classic]

{{edot}} covers most core {{observability}} use cases, but the following scenarios still work better with classic Elastic ingestion:

* **Web real user monitoring (RUM)**: OTel-native RUM data is not yet available for production use. EDOT Browser is in Technical Preview. For production RUM, use the [classic Elastic {{product.apm}} browser agent](apm-agent-rum-js://reference/index.md).
* **Universal Profiling**: Only available with classic Elastic ingestion, and not through OTel-native data.
* **Existing ECS integrations and dashboards**: Many prebuilt integrations and dashboards use ECS-formatted data and may not work with OpenTelemetry semantic conventions without customization. Install OpenTelemetry content packs from the {{kib}} {{integrations}} UI (search for `otel`) to get OTel-compatible dashboards.
* **Tail-based sampling (TBS)**: {{edot}} does not provide managed TBS. The {{motlp}} has no TBS support, so you have to configure sampling at the edge before sending. You can configure self-managed TBS, with [some caveats](opentelemetry://reference/compatibility/limitations.md#tail-based-sampling-tbs), in:
  * {applies_to}`edot_collector: preview 9.2+` {{agent}}
  * Any OTel-compatible Collector
* **Centrally managed log processing**: Elastic doesn't provide curated, centralized {{es}} ingest pipelines for OTel-native data. Process logs in the Collector instead, or define your own ingest pipeline. For dotted field names in user-defined pipelines, you can:
  * Use the [dot expander processor](elasticsearch://reference/enrich-processor/dot-expand-processor.md)
  * {applies_to}`stack: ga 9.2+` {applies_to}`serverless: ga` Set `field_access_pattern` to [`flexible`](/manage-data/ingest/transform-enrich/ingest-pipelines.md#access-source-pattern-flexible)

Refer to [Limitations of {{edot}}](opentelemetry://reference/compatibility/limitations.md) for the full list.

## Verify your data [start-with-otel-verify]

After completing your quickstart, confirm that data is flowing:

1. Open {{kib}} and go to **{{product.observability}} → Applications → Services** (or use the global search to find **Services**) to confirm your application traces appear.
2. Go to **{{product.observability}} → Infrastructure** (or search for **Infrastructure**) to confirm host and container metrics are visible.
3. Go to **Logs** and filter by your service name to confirm log data is flowing.

If data is missing, refer to [Troubleshoot {{edot}}](/troubleshoot/ingest/opentelemetry/index.md).

## Next steps [start-with-otel-next-steps]

* Explore [OpenTelemetry use cases](/solutions/observability/get-started/opentelemetry/use-cases/index.md) for Kubernetes and LLM observability.
* Learn about [{{edot}} compared to the upstream OpenTelemetry distributions](opentelemetry://reference/compatibility/edot-vs-upstream.md).
* Review the [{{edot}} feature compatibility matrix](opentelemetry://reference/compatibility/features.md).
* {applies_to}`stack: preview 9.1+` {applies_to}`serverless: unavailable` Set up [central configuration for EDOT SDKs](opentelemetry://reference/central-configuration.md) to manage SDK settings from {{kib}}.
* Read about [data streams and the OTel-native data format](opentelemetry://reference/compatibility/data-streams.md) if you plan to write custom queries or build dashboards.

## Related pages [start-with-otel-related]

* [Use OpenTelemetry with Elastic APM](/solutions/observability/apm/opentelemetry/index.md) — detailed reference on integration options
* [Limitations of {{edot}}](opentelemetry://reference/compatibility/limitations.md)
* [{{edot}} vs upstream OpenTelemetry](opentelemetry://reference/compatibility/edot-vs-upstream.md)
* [{{agent}} reference](elastic-agent://reference/edot-collector/index.md)
* [Managed inputs](opentelemetry://reference/managed-inputs/index.md) — {{motlp}} and other managed endpoints
