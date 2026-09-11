---
navigation_title: Switch to OpenTelemetry
description: Migrate from classic Elastic APM agents or Beats-based data collection to Elastic OpenTelemetry.
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

# Switch to OpenTelemetry [switch-to-otel]

This guide helps you move from classic Elastic {{product.apm}} agents, {{beats}}, or {{agent}} to OpenTelemetry-based collection with {{edot}}. Use it to replace classic {{product.apm}} agents, shift log and metric collection to OpenTelemetry, and plan for the data model changes that affect dashboards and queries.

If you're setting up {{product.observability}} for the first time with OpenTelemetry, refer to [Start using OpenTelemetry with Elastic](start-with-otel.md) instead.

## Before you begin [switch-to-otel-before]

Review the version requirements, what you gain, what you trade off, and how the data model changes before you replace agents or collection.

### Version requirements [switch-to-otel-versions]

EDOT SDKs and {{agent}} in OTel mode require {{stack}} 8.16 or later for basic compatibility. For a supported configuration, use:

* {{stack}} 9.x, or
* {{stack}} 8.18 or 8.19 with {{agent}} version 9.x. You have to keep your configuration aligned to your Stack version, not the {{agent}} 9.x defaults.

{{serverless-full}} has no version requirements. On {{ech}}, the {{motlp}} requires a deployment version 9.0 or later.

Refer to [{{agent}} and {{stack}} compatibility](opentelemetry://reference/compatibility/collectors.md) for the full matrix.

### What you gain [switch-to-otel-gain]

Switching to {{edot}} brings several advantages over classic Elastic {{product.apm}} agents. You can:

- Use standardized OpenTelemetry APIs and conventions, which means you're not tied to a single vendor's instrumentation API.
- Leverage the OpenTelemetry community's growing library of instrumentation packages.
- Use a single {{agent}} instance to run OTel-native receivers alongside existing Beat-based inputs, collecting traces, metrics, and logs through one process.
- Optimize storage. OTel-native data is stored in LogsDB (logs and traces) and Time Series Data Streams (metrics), which are designed for scalable observability workloads.

### What you lose or trade off [switch-to-otel-tradeoffs]

Not every feature from the classic stack is available with {{edot}} yet. Review these gaps before switching:

| Feature | Status | Notes |
|---|---|---|
| Real User Monitoring (RUM) / Browser | Preview {applies_to}`edot_browser: preview` | For production RUM, continue using the classic Elastic {{product.apm}} browser agent. |
| Universal Profiling | Not available | Only supported with classic Elastic ingestion (using the classic {{agent}}). |
| Span compression | Not available | |
| Breakdown metrics | Not available | The **Time spent by span type** chart on the transaction views doesn't populate. |
| Managed tail-based sampling | Not available | {applies_to}`edot_collector: preview 9.2+` You can run TBS in a self-managed {{agent}} in OTel mode or any OTel-compatible Collector, with reduced metric accuracy, service map coverage, and SLO precision. Refer to [Limitations](opentelemetry://reference/compatibility/limitations.md#tail-based-sampling-tbs). |
| Language runtime metrics | Available with changes | Metric names and attributes change. Existing dashboards built on classic metric names need updates. |
| Central and dynamic configuration | Partial {applies_to}`stack: preview 9.1+` {applies_to}`serverless: unavailable` | [Central configuration](opentelemetry://reference/central-configuration.md) manages a limited set of EDOT SDK settings from {{kib}} and propagates changes at runtime through OpAMP. EDOT .NET applies changes at startup. Settings from classic {{apm-agent}} central configuration don't carry over. |
| Centralized log parsing using ingest pipelines | Not available | Process logs in the Collector instead. Refer to [Limitations](opentelemetry://reference/compatibility/limitations.md#centralized-parsing-and-processing-of-data). |
| Agent health and overhead metrics | Not available | Metrics such as `agent.events.*` have no equivalent. |

### When to wait [switch-to-otel-wait]

Consider waiting if:

- You need production real user monitoring. EDOT Browser is in technical preview.
- You depend on breakdown metrics to power the **Time spent by span type** chart on your transaction views.
- You need managed tail-based sampling without additional operational complexity.
- You have many custom dashboards or alerts built on classic {{product.apm}} field names (`labels.*`, `numeric_labels.*`) and can't absorb the query update work yet.

### Data model impact [switch-to-otel-data-model]

Migrating to {{edot}} changes how your data is stored in {{es}}, which affects existing queries, dashboards, and alerts. The key differences are:

- Custom span and transaction attributes move from `labels.*` and `numeric_labels.*` (dots replaced by underscores) to `attributes.*` (dots preserved). For example, `labels.customer_id` becomes `attributes.customer.id`.
- Resource attributes such as host name and service name move under `resource.attributes.*`. Many remain queryable with their ECS names (for example, `service.name`), but alias coverage isn't complete.
- Data streams change from `apm.app.<service>` to `generic.otel`.
- Runtime metric names change. For Java, `jvm.memory.heap.used` becomes `jvm.memory.used` filtered by `jvm.memory.type = heap`. Dashboards that target the old names don't show the relevant data.

For a complete comparison of field names and storage structures, refer to [OpenTelemetry data streams compared to classic {{product.apm}}](opentelemetry://reference/compatibility/data-streams.md).

## Migrate app instrumentation [switch-to-otel-sdks]

Replace each classic {{apm-agent}} with the corresponding EDOT SDK. Dedicated migration guides cover package replacement, manual instrumentation API changes, and configuration mapping. For languages without a dedicated guide, use the EDOT SDK setup docs.

### Language migration guides [switch-to-otel-sdk-matrix]

| Language | Migration guide | Key caveats |
|---|---|---|
| Java | [Migrate to EDOT Java](elastic-otel-java://reference/edot-java/migration.md) | Breakdown metrics, span compression, and remote attach not available. JVM runtime metric names changed. LDAP client instrumentation missing. Micrometer off by default. |
| Python | [Migrate to EDOT Python](elastic-otel-python://reference/edot-python/migration.md) | Breakdown metrics and span compression not available. Custom {{aws}} Lambda layer not available. Several libraries missing (`aiobotocore`, `Sanic`, `pyodbc`, and others). No structlog integration. |
| Node.js | [Migrate to EDOT Node.js](elastic-otel-node://reference/edot-node/migration.md) | Requires Node.js ^18.19.0 \|\| >=20.6.0 (classic agent supports >=14.17.0). No built-in {{aws}} Lambda or Azure Functions instrumentation. Span compression not available. |
| .NET | [Migrate to EDOT .NET](elastic-otel-dotnet://reference/edot-dotnet/migration.md) | Stacktrace capture and span compression not available. Central configuration available since EDOT .NET 1.4.0; configuration changes apply at startup, not at runtime. |
| PHP | [Migrate to EDOT PHP](elastic-otel-php://reference/edot-php/migration.md) | Span compression, breakdown metrics, `capture_errors`, and `sanitize_field_names` not available. |
| iOS | No dedicated guide | Use the [EDOT iOS](apm-agent-ios://reference/edot-ios/index.md) setup docs to replace the classic Elastic iOS {{apm-agent}}. |
| Android | No dedicated guide | Use the [EDOT Android](apm-agent-android://reference/edot-android/index.md) setup docs to replace the classic Elastic Android {{apm-agent}}. |
| Browser / RUM | No dedicated guide | {applies_to}`edot_browser: preview` Use the [EDOT Browser](elastic-otel-rum-js://reference/edot-browser/index.md) setup docs. For production RUM, continue using the [classic Elastic {{product.apm}} browser agent](apm-agent-rum-js://reference/index.md). |

### If you use contrib OpenTelemetry SDKs or Jaeger [switch-to-otel-upstream]

If your applications already use contrib (upstream) OpenTelemetry SDKs that send data to the {{apm-server}} OTLP intake, you don't need to change your instrumentation. That intake is a legacy path: point your OTLP exporter at the {{motlp}} or an {{agent}} gateway instead, as described in [Ingestion path change](#switch-to-otel-ingestion). You can optionally move to the corresponding EDOT SDK to get Elastic support and opinionated defaults.

If you send traces through the deprecated [Jaeger integration](../../apm/ingest/jaeger.md), migrate your applications to OpenTelemetry SDKs. Jaeger clients are deprecated upstream in favor of OpenTelemetry.

### Configuration changes that apply to all languages [switch-to-otel-common-config]

EDOT SDKs use standard OpenTelemetry environment variables to replace the classic {{apm-agent}}'s connection and identity settings. Most mappings are the same in every language. Exceptions are called out in the table:

| Classic {{apm-agent}} setting | OpenTelemetry equivalent |
|---|---|
| `server_url` / `SERVER_URL` | `OTEL_EXPORTER_OTLP_ENDPOINT` |
| `secret_token` | `OTEL_EXPORTER_OTLP_HEADERS=Authorization=Bearer <token>` |
| `api_key` | `OTEL_EXPORTER_OTLP_HEADERS=Authorization=ApiKey <key>` |
| `service_name` | `OTEL_SERVICE_NAME` |
| `service_version` | `OTEL_RESOURCE_ATTRIBUTES=service.version=<version>` |
| `environment` | `OTEL_RESOURCE_ATTRIBUTES=deployment.environment.name=<env>` |
| `global_labels` | `OTEL_RESOURCE_ATTRIBUTES=key1=value1,key2=value2` |
| `hostname` | `OTEL_RESOURCE_ATTRIBUTES=host.name=<hostname>` |
| `service_node_name` / `serviceNodeName` | `OTEL_RESOURCE_ATTRIBUTES=service.instance.id=<id>` |
| `enabled` / `active` | `OTEL_SDK_DISABLED` — set to `true` to turn the SDK off (`enabled=false` / `active=false`). Applies to Python and Node.js. Java uses `OTEL_JAVAAGENT_ENABLED=false`; PHP uses `OTEL_PHP_ENABLED=false`. |

For detailed configuration mappings, refer to your language's migration guide.

### Ingestion path change [switch-to-otel-ingestion]

Classic {{product.apm}} agents send data directly to {{apm-server}}. EDOT SDKs use OTLP and must send data to one of these endpoints:

- **{{serverless-full}}**: Set `OTEL_EXPORTER_OTLP_ENDPOINT` to the Managed OTLP endpoint for your {{serverless-short}} project. You can copy the endpoint and generate a pre-configured API key from your project's **Add data** wizard. Refer to [{{motlp}}](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md) for details.
- **{{ech}}**: Set `OTEL_EXPORTER_OTLP_ENDPOINT` to the Managed OTLP endpoint for your deployment (requires version 9.0 or later). {{agent}} is not required for application telemetry. You can copy the endpoint from the **Application endpoints, cluster and component IDs** section of your deployment in the {{ecloud}} Console. Refer to [{{motlp}}](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md) for details.
- **Self-managed, ECE, or ECK**: Deploy {{agent}} in OTel mode as a [gateway](elastic-agent://reference/edot-collector/modes.md), then set `OTEL_EXPORTER_OTLP_ENDPOINT` to the gateway's OTLP receiver address.

:::{important}
Direct {{apm-server}} ingestion of OTel-native data from EDOT SDKs is not supported. EDOT SDKs work only when sending data through {{agent}} in OTel mode or the {{motlp}}.

If you previously used unmapped resource attributes that {{apm-server}} stored under `labels.*`, those attributes are not automatically mapped by {{agent}} in OTel mode. To preserve mappings for queries or filters, use the [resource processor](../../apm/opentelemetry/attributes.md#elastic-distribution-of-opentelemetry-collector-edot-collector) to rename or insert resource attributes. For span, metric, or log attributes, use the [attributes processor](elastic-agent://reference/edot-collector/components/attributesprocessor.md).
:::

## Migrate log and metric collection [switch-to-otel-collection]

How you switch logs and metrics depends on whether you collect with {{fleet}}-managed {{agent}}, standalone {{agent}}, {{beats}}, or {{agent}} in OTel mode.

### If you use {{agent}} ({{fleet}}-managed) [switch-to-otel-fleet]

If you use {{fleet}}-managed {{agent}} to collect logs and metrics, you don't need to replace your setup to get the benefits of the OTel architecture. Starting with {{agent}} 9.2, {{agent}} runs an embedded OTel Collector. Beat inputs are migrated to run as _Beat receivers_ inside that Collector incrementally across releases (self-monitoring data in 9.2, some metrics inputs in 9.3, all metrics inputs in 9.4). Log inputs continue to use the previous architecture until a future release.

What this means in practice:

- Existing {{fleet}}-managed integrations continue to work without any configuration changes. Beat receivers run the same inputs and produce ECS-formatted data. Assets such as dashboards, alerts, and ingest pipelines remain unchanged.
- Data collected by Beat receivers remains ECS-formatted, not OTel-native. If you want OTel-native log and metric collection, you need to replace Beat inputs with OTel-native receivers.
- You can run both in the same {{agent}} instance. A single `elastic-agent.yml` can contain an `inputs`/`outputs` section for Beat-based data alongside `receivers`/`exporters`/`service.pipelines` sections for OTel-native data.

For a practical reference on the {{agent}} OTel architecture, the Beat receiver rollout across versions, and the collector type comparison, refer to [{{agent}} as an OpenTelemetry Collector](/reference/fleet/elastic-agent-as-otel-collector.md).

For OTel-native collection through {{agent}} integrations (preview), refer to [Collect OpenTelemetry data with {{agent}} integrations](/reference/fleet/otel-integrations.md).

### If you use {{beats}} directly [switch-to-otel-beats]

{{beats}} ({{filebeat}}, {{metricbeat}}, and others) are not replaced by {{agent}} in OTel mode in a single step. The recommended path is to migrate from {{beats}} to {{fleet}}-managed {{agent}}, which then uses Beat receivers internally. This preserves your existing data structure and integrations while positioning you to adopt OTel-native receivers incrementally.

### If you use standalone {{agent}} [switch-to-otel-standalone]

If you run standalone {{agent}} (not {{fleet}}-managed) and want to switch to OTel-native receivers, refer to [{{agent}} as an OpenTelemetry Collector](/reference/fleet/elastic-agent-as-otel-collector.md) for standalone configuration options. You can migrate incrementally: a single `elastic-agent.yml` can run your existing Beat-based inputs alongside OTel-native pipelines.

### If you already run {{agent}} in OTel mode [switch-to-otel-collector-migration]

If you're already running {{agent}} in OTel mode (formerly the standalone EDOT Collector) and need to update deprecated components or older Collector configurations, refer to [Components included in {{agent}}](elastic-agent://reference/edot-collector/components.md).

## Verify your migrated data [switch-to-otel-verify]

After migration, confirm that data is flowing correctly and that key views in {{kib}} are working as expected.

If a migrated service keeps the same service name (`OTEL_SERVICE_NAME` matching the previous `service.name`), it appears as the same service in the Applications UI, and its history spans both instrumentation periods.

:::{note}
:applies_to: {"stack": "ga 9.3+", "serverless": "ga"}
The service's **Metrics** tab shows callouts when it detects an instrumentation change or overlapping classic and OpenTelemetry data in the selected time range. Refer to [Instrumentation changes during migration](../../apm/metrics-ui.md#instrumentation-change).
:::

:::::{stepper}

::::{step} Check signal ingestion

1. In {{kib}}, go to **{{product.observability}} → Applications → Service inventory** (or use the global search to find **Service inventory**) and confirm your service appears.
2. Open the service and verify that traces, metrics, and logs are present in each tab.
3. Check the service's **Metrics** tab for runtime metrics. Metric names have changed. For example, for Java, `jvm.memory.heap.used` is now `jvm.memory.used` with a `jvm.memory.type = heap` attribute filter.

::::

::::{step} Check dashboards and saved searches

Review custom dashboards, alerts, and saved searches that query {{product.apm}} or log data. Fields stored under `labels.*` or `numeric_labels.*` in classic {{product.apm}} are now under `attributes.*` in OTel-native data. Not all ECS fields have aliases in the OTel data streams, so some queries might need updating.

::::

::::{step} Check alerts and SLOs

If you have alerts or SLOs based on request volume, error rates, or metric thresholds, verify them after migration. Metric renames and sampling differences can affect baseline values and alert behavior.

::::

:::::

If data is missing, refer to [Troubleshoot {{edot}}](/troubleshoot/ingest/opentelemetry/index.md).

## After the migration [switch-to-otel-after]

You can run classic and EDOT instrumentation in parallel during a phased rollout, then remove the classic agents after you've verified the new path.

### Running both agents during transition [switch-to-otel-parallel]

You can run a classic {{apm-agent}} and an EDOT SDK simultaneously during a phased rollout, as long as they serve different service instances or use distinct `OTEL_SERVICE_NAME` values. Both ingestion paths ({{apm-server}} for classic agents, and the {{motlp}} or {{agent}} in OTel mode for EDOT SDKs) can be active at the same time, so you can migrate one service at a time and verify before switching the rest.

:::{note}
Don't run both a classic {{apm-agent}} and an EDOT SDK inside the same process instance. Use one or the other per service instance.
:::

### Clean up after migration [switch-to-otel-cleanup]

Once you've verified that your migrated services are sending data correctly:

:::::{stepper}

::::{step} Remove the classic {{apm-agent}} packages

Remove the classic {{apm-agent}} packages and startup arguments from your applications.

::::

::::{step} Remove {{apm-agent}} configuration

Remove your previous {{apm-agent}} configuration, including environment variables, configuration files, and language-specific configuration sections such as `appsettings.json` for .NET or `elasticapm` sections for Python.

::::

::::{step} Update saved searches, dashboards, and alerts

Review and update {{kib}} saved searches, dashboards, and alerts that referenced classic {{product.apm}} field names (`labels.*`, `numeric_labels.*`, `apm.app.*` data streams).

::::

::::{step} Confirm the OTLP endpoint

If you were previously sending OTel data directly to {{apm-server}} (not supported), confirm the `OTEL_EXPORTER_OTLP_ENDPOINT` now points to the {{motlp}} or {{agent}} in OTel mode.

::::

::::{step} Decommission {{apm-server}} when nothing depends on it

Keep {{apm-server}} or the {{fleet}}-managed {{product.apm}} integration running while any classic {{apm-agent}} still sends data to it, including the classic browser agent if you kept it for production RUM. After the last classic agent is gone, remove the {{product.apm}} integration from your {{fleet}} policies or shut down your standalone {{apm-server}}.

::::

:::::

## Related pages [switch-to-otel-related]

- [Limitations of {{edot}}](opentelemetry://reference/compatibility/limitations.md) — full list of gaps compared to classic Elastic ingestion, including when to prefer the classic stack
- [Elastic features available with {{edot}}](opentelemetry://reference/compatibility/features.md) — feature compatibility matrix
- [OpenTelemetry data streams compared to classic {{product.apm}}](opentelemetry://reference/compatibility/data-streams.md) — how field names and storage structures differ
- [{{agent}} as an OpenTelemetry Collector](/reference/fleet/elastic-agent-as-otel-collector.md) — {{fleet}}-managed and standalone OTel collection architecture
- [{{agent}} in OpenTelemetry mode](elastic-agent://reference/edot-collector/index.md) — setup and configuration
- [Managed OTLP endpoint](opentelemetry://reference/managed-inputs/managed-otlp-endpoint.md) — {{serverless-short}} and {{ech}} ingestion reference
- [Troubleshoot {{edot}}](/troubleshoot/ingest/opentelemetry/index.md) — troubleshooting for EDOT SDKs and {{agent}} in OTel mode
