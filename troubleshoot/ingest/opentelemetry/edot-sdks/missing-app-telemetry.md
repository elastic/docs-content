---
navigation_title: No app-level telemetry in Kibana
description: Diagnose lack of telemetry flow due to issues with EDOT SDKs.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_sdk: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# No application-level telemetry visible in Kibana

This page helps you diagnose why application-level telemetry doesn’t appear when using {{edot}} (EDOT) SDKs:

* [The SDK is turned off (`OTEL_SDK_DISABLED`)](#sdk-disabled)
* [Auto-instrumentation or SDK initialization runs at the wrong time](#auto-instrumentation-not-attached)
* [The runtime or framework isn’t supported, or is only partially supported](#framework-not-supported)


## Quick triage checklist

Use this table to quickly spot the usual causes and fixes.

| What you see                     | Check                                   | Likely fix |
|----------------------------------|-----------------------------------------------|------------|
| No telemetry at all              | `OTEL_SDK_DISABLED`, exporters = `none`, sampler `always_off` | Unset `OTEL_SDK_DISABLED`, pick an exporter, use a non-zero sampler |
| No/partial data from web requests | Loader order (preload/agent flags early)     | Move loader earlier and restart the process |
| Only custom code shows spans     | Framework not supported/recognized           | Align versions or add manual instrumentation |
| Works locally, not on prod       | Different environment/flags in container or service  | Match prod environment settings and restart |
| Still unsure                     | Enable debug logging                         | Inspect logs for disabled/unsupported/delayed initialization hints |

### EDOT central configuration toggles at a glance

If you use central configuration using OpAMP, these options can mute or change signals even when local `OTEL_*` looks correct.

| Toggle                                        | Effect                                                  | Typical symptom |
|-----------------------------------------------|---------------------------------------------------------|-----------------|
| `deactivate_all_instrumentations`             | Disables all auto-instrumentations                  | No spans/metrics/logs from instrumented libraries |
| `deactivate_instrumentations`                 | Disables selected instrumentation packages              | Missing spans from specific frameworks/libraries  |
| `send_traces` / `send_metrics` / `send_logs`  | Per-signal send switch                                  | Only some signals arrive |
| `elastic_otel_context_propagation_only` (Node.js) | Propagates context, doesn’t send it to the Collector         | Cross-service context but nothing in Elastic |
| `sampling_rate`                               | Adjusts trace sampling ratio                            | Fewer/more spans than expected               |
| `logging_level`                               | Changes SDK log verbosity                               | Affects debugging output only                |


## No telemetry and logs mention `SDK disabled` [sdk-disabled]

If the logs mention `SDK disabled` or nothing at all, the SDK is likely deactivated in the configuration.

Check the following:

* **Environment variable**  

	Many SDKs honor `OTEL_SDK_DISABLED=true`, or the equivalent in configuration files or flags. You can print the current value of the variable, for example: `printenv OTEL_SDK_DISABLED`.

	For SDK-specific details, see:
	* [Java](opentelemetry://reference/edot-sdks/java/setup/index.md)
	* [.NET](opentelemetry://reference/edot-sdks/dotnet/setup/index.md)
	* [Node.js](opentelemetry://reference/edot-sdks/nodejs/setup/index.md)
	* [Python](opentelemetry://reference/edot-sdks/python/setup/index.md)
	* [PHP](opentelemetry://reference/edot-sdks/php/setup/index.md)

* **Exporter settings that effectively turn off signals**  

	* `OTEL_TRACES_EXPORTER=none`, `OTEL_METRICS_EXPORTER=none`, or `OTEL_LOGS_EXPORTER=none`
	* Sampler turned off: `OTEL_TRACES_SAMPLER=always_off` or sampling probability set to `0.0`

* **Multiple configuration sources**  

	CI/CD pipelines or container manifests, such as Kubernetes `env:` blocks, might override local settings. These environments often require setting variables at deployment time.

### Resolution [res-sdk-disabled]

To fix the issue, try the following:

* **Enable the SDK**

	Unset `OTEL_SDK_DISABLED` or set it to `false`.

* **Enable exporters/sampler**

	Choose a valid exporter (for example `otlp`) and a sampling strategy with a non-zero probability (for example, `parentbased_traceidratio` with a ratio > 0).

* **Restart the process**

	Restart after changing any configuration. Some SDKs only read environment variables at startup.

If telemetry is still missing, you can enable debug logging. Refer to [Enable debug logging for EDOT SDKs](enable-debug-logging.md) for guidance. Make sure to [verify that you're looking at the right logs](enable-debug-logging.md#verify-youre-looking-at-the-right-logs).

## Auto-instrumentation isn’t attaching [auto-instrumentation-not-attached]

If auto-instrumentation isn’t attaching, or only partial data appears, the SDK or loader might be initializing too late, after the app or framework has already started.

Check the following:

* **What runs first**

	Ensure the SDK or auto-instrumentation loader runs before your app code, web server, or worker framework.

	**Using the OpenTelemetry Operator?**

	If you deploy using the OpenTelemetry Operator, verify that auto-instrumentation is injected correctly:

	1. **Instrumentation resource**: Confirm the `Instrumentation` CR matches your runtime (Java/.NET/Node/Python/PHP) and sets the intended options (for example `java.javaAgent`, `dotnet.env`, or `node.env`).
	2. **Pod injection**: Check that your workload has the expected annotations (or namespace injection enabled) and that new Pods were rolled to pick up injection.
	3. **Environment variables and startup flags present**: Run `kubectl describe pod/<pod>`. In the output, under Containers, the Environment section should list the expected loader flags (for example `JAVA_TOOL_OPTIONS`, `DOTNET_*`, or `NODE_OPTIONS`) and volume mounts for agents.
	4. **Webhook and injector logs**: Inspect the Operator and injector webhook logs for errors or skipped injections.
	5. **Restart and rollout**: After changing the `Instrumentation` or annotations, perform a rollout so containers start with the updated environment variables and startup flags.

	If you use EDOT-specific images or settings, align the Instrumentation configuration with EDOT’s SDK guidance for that language (see links below).


* **Start-up mechanism by language**

	* **Java:** Use the `-javaagent:` flag as early as possible so it loads before `main()`. Refer to [Java SDK setup](opentelemetry://reference/edot-sdks/java/setup/index.md).

	* **.NET:** Set the profiler/auto-instrumentation environment variables before starting the process. Refer to [.NET SDK setup](opentelemetry://reference/edot-sdks/dotnet/setup/index.md).

	* **Node.js:** Use a preloader (for example `NODE_OPTIONS=--require <entry>`) or import the SDK before bootstrapping the app. Refer to [Node.js SDK setup](opentelemetry://reference/edot-sdks/nodejs/setup/index.md).

	* **Python:** Use the launcher (for example `opentelemetry-instrument …`) or import/initialize the SDK before the framework starts. Refer to [Python SDK setup](opentelemetry://reference/edot-sdks/python/setup/index.md).

	* **PHP:** Ensure the extension is loaded and restart PHP-FPM/Apache so bootstrap hooks are active. Refer to [PHP SDK setup](opentelemetry://reference/edot-sdks/php/setup/index.md).

	If using Docker or Kubernetes confirm preloading flags or environment variables are placed where the actual process starts.

### Resolution [res-instrumentation]

To fix the issue, try the following steps:

1. Move agent/loader flags to the earliest possible point in your startup chain.
2. Confirm the loader runs. Debug logs should show detected instrumentations or patched modules.
3. Fully restart the service, as reloads are often insufficient for preloaders/agents.

:::{tip}
In debug logs, look for lines that mention `installing instrumentation for …` or `detected framework … version …`. Lack of these hints usually means the loader didn’t run early enough.
:::

## App starts, SDK loads, but no telemetry for your framework [framework-not-supported]

If the app and SDK load correctly but no spans, metrics, or logs appear for your framework, the runtime, framework, or library may not be supported or are only partially instrumented.

Check the following:

* **Compatibility tables**

	Verify that your runtime and frameworks are supported by the SDK. Refer to the [EDOT SDK compatibility reference](opentelemetry://reference/compatibility/sdks.md) for more information.

* **Major version mismatches**

	New major versions of frameworks may not yet be supported and can break auto-instrumentation.

* **Partial coverage**

	Some scenarios may require manual instrumentation.

### Resolution [res-framework]

To fix the issue, try the following:

* **Align versions**

	Upgrade or downgrade the SDK or framework to a supported combination.

* **Add manual instrumentation**

	Instrument code paths not covered by the agent.

* **Retest with a minimal app**

	Strip down to core dependencies to rule out issues introduced by third-party libraries.
