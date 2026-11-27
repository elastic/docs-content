---
description: Learn how to monitor a Java application with Elastic Observability using the Elastic Distribution of OpenTelemetry Java SDK and Elastic Agent configured as an OpenTelemetry Collector, sending traces, metrics, and logs to Elastic.
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-java-app.html
applies_to:
  stack: ga 9.4+
  serverless: ga
type: tutorial
products:
  - id: observability
  - id: edot-sdk
  - id: edot-collector
---

# Tutorial: Monitor a Java application [monitor-java-app]

In this tutorial, you monitor a small Java application end-to-end with Elastic {{observability}}. You instrument it with the {{edot}} Java SDK, collect its traces, metrics, and logs with {{agent}} configured as an OpenTelemetry (OTel) Collector, and use {{kib}} to find and fix a real problem in the running application.

It assumes basic familiarity with:

- Running a Java application and shell commands from the command line
- Connecting to a Linux host over SSH

By the end of this tutorial, you can:

- Instrument a Java application with the {{edot}} Java SDK, with no code changes required.
- Run {{agent}} configured as an OpenTelemetry (OTel) Collector, acting as a local collector that forwards application and host telemetry to the {{motlp}}.
- Use the **Applications** UI and **Discover** to confirm your data arrived, and explore traces, metrics, and logs.
- Investigate a slow request and a failing request, and confirm a fix by watching the data change.

## Before you begin [_before_you_begin]

You need:

- An {{ech}} deployment or {{obs-serverless}} project, version 9.4 or later. If you don't have one, refer to [Create an Observability project](/solutions/observability/get-started.md).
- A Linux host (a VM works well) with outbound internet access. You'll run both {{agent}} and the sample application on it.
- Java 17 (or later) installed on that host. The sample application bundles its own Gradle wrapper, so you don't need Gradle or Maven installed separately.
- The sample application source, `java-monitor-demo`.

:::{note}
This tutorial uses a small Spring Boot application built for this tutorial, with three endpoints, so you can see a normal request, a slow request, and a failing request side by side in your data. Get the source from [TODO: link to the published `java-monitor-demo` sample, for example under `elastic/observability-contrib`].
:::

::::::{stepper}

:::::{step} Run {{agent}} configured as an OTel Collector
:anchor: _step_1_run_agent_in_otel_mode

{{agent}} in [Agent mode](elastic-agent://reference/edot-collector/modes.md#edot-collector-as-agent) runs on the same host as your application. It collects the traces, metrics, and logs your application sends it, picks up host-level logs and metrics on its own, and forwards everything to Elastic.

First, find your {{motlp}} endpoint and create an API key, following [Quickstart: Send OTLP data to Elastic Serverless or Elastic Cloud Hosted](/solutions/observability/get-started/quickstart-elastic-cloud-otel-endpoint.md). Keep both values handy for the next step.

:::{tip}
The collector, the sample application, and the traffic-generation script from Step 3 all stay running in the foreground for the rest of this tutorial. Run each of them in its own terminal or SSH session.
:::

1. Download and extract {{agent}}:

   ```bash
   curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-linux-x86_64.tar.gz
   tar xzf elastic-agent-{{version.stack}}-linux-x86_64.tar.gz
   cd elastic-agent-{{version.stack}}-linux-x86_64
   ```

   :::{tip}
   Use the `elastic-agent-{{version.stack}}-linux-arm64.tar.gz` package instead if your host is ARM-based. See [all available packages](https://www.elastic.co/downloads/elastic-agent) if you need a different OS or architecture.
   :::

2. Configure it to send data to the {{motlp}}:

   {{agent}} ships with a ready-made configuration for exactly this setup, under `otel_samples/managed_otlp/logs_metrics_traces.yml`. It defines:

   - An OTLP (OpenTelemetry Protocol) receiver, so your application's {{edot}} SDK can send it traces, metrics, and logs over gRPC (port `4317`) or HTTP (port `4318`).
   - A host metrics receiver (CPU, memory, disk, filesystem, network).
   - A log file receiver reading `/var/log/*.log`.
   - Exporters that forward everything to the {{motlp}}.

   Copy it and fill in your endpoint and API key:

   ```bash
   ELASTIC_OTLP_ENDPOINT=<your endpoint> && \
   ELASTIC_API_KEY=<your API key> && \
   cp ./otel_samples/managed_otlp/logs_metrics_traces.yml ./otel.yml && \
   mkdir -p ./data/otelcol && \
   sed -i "s#\${env:STORAGE_DIR}#${PWD}/data/otelcol#g" ./otel.yml && \
   sed -i "s#\${env:ELASTIC_OTLP_ENDPOINT}#${ELASTIC_OTLP_ENDPOINT}#g" ./otel.yml && \
   sed -i "s#\${env:ELASTIC_API_KEY}#${ELASTIC_API_KEY}#g" ./otel.yml && \
   chmod 600 ./otel.yml
   ```

   :::{important}
   `chmod 600` matters here: the previous command writes your API key in plain text into `otel.yml`.
   :::

3. Run it:

   ```bash
   sudo ./otelcol --config otel.yml
   ```

   `sudo` is required because the log file receiver reads `/var/log/*.log`, which is root-owned on most distributions.

**Result:** the collector logs that it started its pipelines, with no export errors. Leave it running. If you want it to survive logging out, restart it under `nohup`, `screen`, or a systemd unit; that part isn't specific to this tutorial.

:::::

:::::{step} Instrument and run the Java application
:anchor: _step_2_instrument_and_run_the_application

The {{edot}} Java SDK auto-instruments your application: there's no code to change, only a Java Virtual Machine (JVM) flag.

1. Build the sample application:

   ```bash
   cd java-monitor-demo
   ./gradlew -q bootJar
   ```

2. Download the {{edot}} Java agent from [Maven Central](https://repo1.maven.org/maven2/co/elastic/otel/elastic-otel-javaagent/), picking the [latest release](https://github.com/elastic/elastic-otel-java/releases/latest):

   ```bash
   curl -L -O https://repo1.maven.org/maven2/co/elastic/otel/elastic-otel-javaagent/<version>/elastic-otel-javaagent-<version>.jar
   ```

3. Run the application with the agent attached:

   ```bash
   OTEL_SERVICE_NAME=java-monitor-demo \
     java -javaagent:./elastic-otel-javaagent-<version>.jar -jar build/libs/java-monitor-demo-1.0.0.jar <1>
   ```
   1. No `OTEL_EXPORTER_OTLP_ENDPOINT` is needed here: when a local collector is running on its default ports, as yours is from Step 1, the {{edot}} Java SDK sends data to it automatically.

**Result:** the application starts and logs that it's listening on port 8080. Confirm it's responding:

```bash
curl "http://localhost:8080/greeting?item=mug"
```

:::::

:::::{step} Generate traffic
:anchor: _step_3_generate_traffic

The sample application has three endpoints that give you something interesting to look at:

- `/greeting?item=mug`: a normal request.
- `/slow?item=mug`: an artificially slow request (simulates a slow downstream dependency).
- `/error?item=mug`: a request that fails with a `503`, until you fix it in [Step 7](#_step_7_investigate_the_failing_request_and_confirm_the_fix).

Run the included script to generate a steady mix of all three:

```bash
cd java-monitor-demo
bash scripts/generate-traffic.sh localhost:8080
```

Leave it running in the background for the rest of this tutorial, so there's always fresh data to look at.

:::::

:::::{step} Confirm your data arrived
:anchor: _step_4_confirm_your_data_arrived

Find **Discover** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), and check the following data streams for incoming data:

- `traces-generic.otel-default`
- `logs-generic.otel-default`
- `metrics-generic.otel-default`

:::{image} /solutions/images/observability-monitor-java-app-otel-discover-logs.png
:alt: Discover view showing incoming documents in the logs-generic.otel-default data stream
:screenshot:
:::

If nothing appears after a few minutes, refer to [No logs, metrics, or traces visible in {{kib}}](/troubleshoot/ingest/opentelemetry/no-data-in-kibana.md).

:::::

:::::{step} View application performance
:anchor: _step_5_view_application_performance

Find **Applications** in the navigation menu, go to **Services**, and select **java-monitor-demo**. Select the **Transactions** tab, and then **GET /slow**.

:::{image} /solutions/images/observability-monitor-java-app-otel-apm-overview-slow.png
:alt: Latency and throughput charts for the GET /slow transaction in the Applications UI
:screenshot:
:::

Latency and throughput update as `generate-traffic.sh` keeps sending requests. Compare this against **GET /greeting** and **GET /error** to see how the three endpoints differ.

:::::

:::::{step} Investigate the slow request
:anchor: _step_6_investigate_the_slow_request

Still on **GET /slow**, scroll down to **Trace samples**, and open one of the listed samples.

:::{image} /solutions/images/observability-monitor-java-app-otel-trace-waterfall.png
:alt: Trace waterfall for a slow GET /slow request, showing a single long span
:screenshot:
:::

The single long span under `java-monitor-demo` is the simulated warehouse lookup from the sample application's `/slow` endpoint. In a real application, this is where you'd look for a slow downstream call, an inefficient query, or lock contention.

:::::

:::::{step} Investigate the failing request and confirm the fix
:anchor: _step_7_investigate_the_failing_request_and_confirm_the_fix

Go to **GET /error** and look at **Latency distribution**. The failed transactions are highlighted separately from successful ones.

:::{image} /solutions/images/observability-monitor-java-app-otel-apm-latency-distribution-error.png
:alt: Latency distribution for GET /error showing failed transactions highlighted
:screenshot:
:::

To see why they're failing, correlate with logs. Find **Discover** in the navigation menu, select the `logs-*` data view, and search for `service.name: java-monitor-demo`. Filter out `INFO` logs to cut the noise:

:::{image} /solutions/images/observability-monitor-java-app-otel-discover-logs-error-correlation.png
:alt: Discover view filtered to WARN and ERROR logs, showing "Pricing service lookup failed" messages
:screenshot:
:::

The `ERROR` log lines, `Pricing service lookup failed for item [mug]: service not enabled`, point to the cause: the application's pricing lookup is turned off.

To fix it, stop the application on its host (press Ctrl+C) and restart it with the pricing lookup turned on:

```bash
OTEL_SERVICE_NAME=java-monitor-demo \
PRICING_SERVICE_ENABLED=true \
  java -javaagent:./elastic-otel-javaagent-<version>.jar -jar build/libs/java-monitor-demo-1.0.0.jar
```

**Result:** within a few request cycles, `/error` starts returning `200` instead of `503`. Back in the Applications UI, **GET /error**'s failed transaction rate drops to zero, and in Discover, the `ERROR` log lines stop appearing.

:::::

:::::{step} View metrics in Discover
:anchor: _step_8_view_metrics_in_discover

{applies_to}`stack: deprecated 9.4+` Metrics Explorer is deprecated and planned for removal. Use **Discover** instead, which has a dedicated experience for metrics data.

Find **Discover**, switch to {{esql}} mode, and run:

```esql
TS metrics-*otel-default*
```

:::{image} /solutions/images/observability-monitor-java-app-otel-discover-metrics.png
:alt: Discover's metrics chart grid, showing metrics.http.server.request.duration and JVM metrics
:screenshot:
:::

`metrics.http.server.request.duration` is the most directly useful chart here: it's the same request latency you saw in the Applications UI, but alongside JVM-level metrics like buffer usage, class counts, and CPU. Refer to [Explore metrics data with Discover in {{kib}}](/solutions/observability/infra-and-hosts/discover-metrics.md) to learn more about this view, including breaking metrics down by dimension.

:::::

::::::

## Summary [_summary]

In this tutorial, you:

- Instrumented a Java application with the {{edot}} Java SDK and ran {{agent}} configured as an OTel Collector to collect its telemetry.
- Confirmed traces, metrics, and logs arrived in {{kib}}.
- Used the Applications UI and Discover to investigate a slow request and a failing request, fixed the failure, and watched the fix show up in the data.

## Next steps [_next_steps]

- [Start using OpenTelemetry with Elastic](/solutions/observability/get-started/opentelemetry/start-with-otel.md), if you want to understand the broader decision between an OTel-native setup and other ingest paths.
- [OpenTelemetry quickstarts](/solutions/observability/get-started/opentelemetry/quickstart/index.md), for install guides covering other deployment models, such as Kubernetes and Docker.
- [Drill down into data](/solutions/observability/apm/drill-down-into-data.md), to go deeper into transactions and spans than this tutorial covers.

## Related pages [_related_pages]

- [{{motlp}}](opentelemetry://reference/motlp.md)
- [{{agent}} as an OpenTelemetry Collector](/reference/fleet/elastic-agent-as-otel-collector.md)
- [EDOT Java SDK setup](elastic-otel-java://reference/edot-java/setup/index.md)
- [Explore metrics data with Discover in {{kib}}](/solutions/observability/infra-and-hosts/discover-metrics.md)
- [No logs, metrics, or traces visible in {{kib}}](/troubleshoot/ingest/opentelemetry/no-data-in-kibana.md)
