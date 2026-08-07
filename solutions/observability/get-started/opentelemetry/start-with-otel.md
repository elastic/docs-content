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

This guide helps you choose the right setup for your environment so you can start sending metrics, logs, and traces to Elastic using {{edot}}. Rather than repeating the step-by-step install instructions that are already in the quickstarts, it walks you through the decisions you need to make first.

## Before you begin [start-with-otel-prereqs]

EDOT SDKs and {{agent}} require Elastic Stack 8.16 or later for basic compatibility. For a **supported** configuration:

* Use Elastic Stack 9.x, or
* Use Elastic Stack 8.18 or 8.19 with {{agent}} version 9.x — and keep your configuration aligned to your Stack version, not the {{agent}} 9.x defaults.

{{serverless-full}} has no version requirements.

Refer to [{{agent}} and Elastic Stack compatibility](opentelemetry://reference/compatibility/collectors.md) for the full matrix.

## Decide what to send [start-with-otel-what-to-send]

Identify what you want to observe before picking a setup:

* **Application telemetry** (traces, metrics, and logs from your code): use an EDOT language SDK. It auto-instruments your application with zero or minimal code changes.
* **Infrastructure telemetry** (host metrics, logs, Kubernetes signals): use {{agent}} to collect system-level data from your hosts, containers, or cluster.
* **Both**: most production setups collect application and infrastructure telemetry together. You can run an EDOT SDK and {{agent}} on the same host.

## Choose your ingestion path [start-with-otel-ingestion-path]

The right ingestion path depends on your Elastic deployment type. Select your deployment to see the recommended setup.

::::{important}
Regardless of your deployment, do **not** point EDOT SDKs directly at the {{product.apm-server}} OpenTelemetry intake endpoint — this configuration is [not supported](opentelemetry://reference/edot-sdks/index.md). EDOT SDKs work only when sending data through {{agent}} or the {{motlp}}.
::::

::::{applies-switch}

:::{applies-item} serverless:

**Send data to the {{motlp}}.**

The {{motlp}} is GA for {{serverless-full}} Observability and Security projects. No {{agent}} is required for application telemetry — point your EDOT SDK or any OTLP-compatible exporter directly at the managed endpoint.

For infrastructure telemetry (host metrics, logs, Kubernetes), run {{agent}} on your hosts or cluster and configure it to export data to the {{motlp}} using the OTLP exporter.

**Before committing to this path**, note these {{motlp}} limitations:

* Tail-based sampling (TBS) is not available. Configure head-based sampling at the edge before sending data.
* The endpoint drops histograms with cumulative temporality. Use delta temporality or add the `cumulativetodelta` processor at the edge.
* Universal Profiling is not available.

Refer to [{{motlp}}](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md) for the full list of limitations and configuration details.
:::

:::{applies-item} ess:

**Send data to the {{motlp}}** (requires {{ech}} deployment version 9.0 or later).

The {{motlp}} is GA on {{ech}}. For application telemetry only, send directly from your EDOT SDK or any OTLP-compatible exporter to the endpoint, with no {{agent}} required. For infrastructure telemetry, run {{agent}} on your hosts or cluster and configure it to export to the {{motlp}} using the OTLP exporter.

:::{note}
The current {{ech}} quickstarts use a different path: an {{agent}} running on a host and writing directly to {{es}} using the `elasticsearch` exporter. This alternative works and is documented, but Elastic recommends the {{motlp}} path for new setups on {{ech}} 9.0+.
:::

**Before committing to this path**, note these {{motlp}} limitations:

* Tail-based sampling (TBS) is not available. Configure head-based sampling at the edge before sending data.
* The endpoint drops histograms with cumulative temporality. Use delta temporality or add the `cumulativetodelta` processor at the edge.
* Universal Profiling is not available.

Refer to [{{motlp}}](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md) for the full list of limitations and configuration details.
:::

:::{applies-item} self:

**Run {{agent}} in gateway mode.**

The {{motlp}} is not available for self-managed Elastic, ECE, or ECK deployments. You need an {{agent}} running in [gateway mode](elastic-agent://reference/edot-collector/modes.md).

{{agent}} in gateway mode is required for full {{product.apm}} functionality. It:

* Exposes an OTLP endpoint that edge collectors, EDOT SDKs, and other OTLP sources send data to.
* Runs the `elasticapm` processor {applies_to}`edot_collector: ga 9.2+` to enrich trace data with attributes the {{product.observability}} UIs rely on. On Elastic Stack 8.18–8.19, use the `elastictrace` processor instead.
* Runs the `elasticapm` connector to generate pre-aggregated {{product.apm}} metrics from traces.
* Routes telemetry to the correct data streams and writes to {{es}} using the `elasticsearch` exporter in `otel` mapping mode.

For edge collectors running on your hosts, Kubernetes nodes, or alongside your applications, use the OTLP exporter to forward data to the gateway. The `elasticsearch` exporter is only recommended for the gateway itself — not for edge collectors.

Refer to [{{agent}} modes](elastic-agent://reference/edot-collector/modes.md) and [Default standalone configurations](elastic-agent://reference/edot-collector/config/default-config-standalone.md) for step-by-step setup.
:::

::::

## Pick your quickstart [start-with-otel-quickstarts]

Once you know your ingestion path, select the quickstart for your environment:

| Deployment model | Kubernetes | Docker | Hosts or VMs |
|---|---|---|---|
| {{product.self}} Stack | [K8s on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/k8s.md) | [Docker on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/docker.md) | [Hosts on self-managed](/solutions/observability/get-started/opentelemetry/quickstart/self-managed/hosts_vms.md) |
| {{serverless-full}} | [K8s on serverless](/solutions/observability/get-started/opentelemetry/quickstart/serverless/k8s.md) | [Docker on serverless](/solutions/observability/get-started/opentelemetry/quickstart/serverless/docker.md) | [Hosts on serverless](/solutions/observability/get-started/opentelemetry/quickstart/serverless/hosts_vms.md) |
| {{ech}} | [K8s on hosted](/solutions/observability/get-started/opentelemetry/quickstart/ech/k8s.md) | [Docker on hosted](/solutions/observability/get-started/opentelemetry/quickstart/ech/docker.md) | [Hosts on hosted](/solutions/observability/get-started/opentelemetry/quickstart/ech/hosts_vms.md) |

To send OTLP data directly to {{serverless-full}} or {{ech}} (9.0+) without running {{agent}}, follow [Send OTLP data to the {{motlp}}](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md).

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
* [EDOT Browser](elastic-otel-rum-js://reference/edot-browser/index.md) — Technical Preview. For production real user monitoring, continue using the [classic Elastic APM browser agent](apm-agent-rum-js://reference/index.md).

For languages without an EDOT SDK (Go, C++, Ruby, and others), use the [contrib OpenTelemetry SDKs](/solutions/observability/apm/opentelemetry/upstream-opentelemetry-collectors-language-sdks.md). These work with Elastic over OTLP but receive community support only.

## Things to know before you go live [start-with-otel-caveats]

### Use the OTLP exporter at the edge [start-with-otel-otlp-exporter]

Configure your EDOT SDKs and edge {{agent}} instances to use the OTLP exporter. Elastic recommends the `elasticsearch` exporter only for the {{agent}} gateway in a self-managed deployment. Using it at the edge can lead to data loss or incorrect mapping.

### Know when to keep using classic Elastic components [start-with-otel-when-classic]

{{edot}} covers most core Observability use cases, but the following scenarios still work better with classic Elastic ingestion:

* **Real user monitoring (RUM)**: OTel-native RUM data is not yet available for production use. EDOT Browser is in Technical Preview. For production RUM, use the [classic Elastic APM browser agent](apm-agent-rum-js://reference/index.md).
* **Universal Profiling**: Only available with classic Elastic ingestion — not through OTel-native data.
* **Existing ECS integrations and dashboards**: Many prebuilt integrations and dashboards use ECS-formatted data and may not work with OpenTelemetry semantic conventions without customization. Install OpenTelemetry content packs from the {{kib}} Integrations UI (search for `otel`) to get OTel-compatible dashboards.
* **Tail-based sampling (TBS)**: {{edot}} does not provide managed TBS. You can configure self-managed TBS in {{agent}} (Technical Preview, Stack 9.2+) or in any OTel-compatible Collector, with caveats. The {{motlp}} has no TBS support — configure sampling at the edge before sending.
* **Centrally managed log processing**: {{es}} ingest pipelines don't reliably process OTel-native data due to dotted field names. Use Collector processors for log parsing, routing, and enrichment instead. User-defined ingest pipelines are compatible from Stack 9.2+, but Elastic doesn't provide managed pipelines for OTel-native data.

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
* Set up [central configuration for EDOT SDKs](opentelemetry://reference/central-configuration.md) to manage SDK settings from {{kib}} — Technical Preview on Stack 9.1+, not available on {{serverless-full}}.
* Read about [data streams and the OTel-native data format](opentelemetry://reference/compatibility/data-streams.md) if you plan to write custom queries or build dashboards.

## Related pages [start-with-otel-related]

* [Use OpenTelemetry with Elastic APM](/solutions/observability/apm/opentelemetry/index.md) — detailed reference on integration options
* [Limitations of {{edot}}](opentelemetry://reference/compatibility/limitations.md)
* [{{edot}} vs upstream OpenTelemetry](opentelemetry://reference/compatibility/edot-vs-upstream.md)
* [{{agent}} reference](elastic-agent://reference/edot-collector/index.md)
* [Managed inputs](opentelemetry://reference/managed-inputs/index.md) — {{motlp}} and other managed endpoints
