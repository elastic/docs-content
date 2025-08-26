---
navigation_title: Enable debug logging for SDKs
description: Learn how to enable debug logging for EDOT SDKs to troubleshoot application-level instrumentation issues.
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

# Enable debug logging for EDOT SDKs

You can enable debug logging for Elastic Distributions of OpenTelemetry (EDOT) SDKs to troubleshoot application-level issues.

Enabling debug logging can help surface common problems such as:

* Auto-instrumentation not attaching or being disabled
* Authentication or endpoint misconfigurations
* Unsupported framework or language version
* Sampling rate being set too low (resulting in missing spans)

## General SDK troubleshooting tips

Check your application logs for SDK-specific output and errors. If no logs appear at all, verify that:

* The SDK or agent is correctly installed and loaded
* The application runtime includes the correct path or classpath
* The environment variables are visible to the application process
* The logs are being written to the correct location

:::{{warning}}
Debug logs can be verbose, potentially impacting performance and containing sensitive information such as system paths, variable names, or internal data structures. They shouldn't be enabled in production environments.
:::


## Java

You can enable debug logging using environment variables.

For general EDOT Java agent debugging, try:

```bash
export OTEL_JAVAAGENT_LOG_LEVEL=debug
java -jar your-app.jar
```
The output is captured span information from the agent itself, in a JSON format.

If you need to see and inspect the specific trace data your application is generating, use:


```bash
export OTEL_TRACES_EXPORTER=otlp,logging-otlp
java -jar your-app.jar
```

The output are the application’s traces in a JSON format.
 
By default, logs are written to `stderr`.


## Python

To enable debug logging, set the `OTEL_PYTHON_LOG_LEVEL` variable to `debug`:

```bash
export OTEL_PYTHON_LOG_LEVEL=debug
```

Run your application as usual, for example:

```bash
python your_application.py
```


## .NET

To enable debug logging for the EDOT .NET agent, set:

::::{tab-set}

:::{tab-item} macOS

```bash
export OTEL_LOG_LEVEL=debug
```
:::

:::{tab-item} Windows

```powershell
$env:OTEL_LOG_LEVEL="debug"
```
:::
::::


## Node.js

Set this environment variable before starting your app:

::::{tab-set}

:::{tab-item} macOS

```bash
export OTEL_LOG_LEVEL=debug
node your-app.js
```
:::

:::{tab-item} Windows

```powershell
$env:OTEL_LOG_LEVEL="debug" 
node your-app.js
```
:::
::::


## PHP

Set this environment variable:

::::{tab-set}

:::{tab-item} macOS

```bash
export OTEL_LOG_LEVEL=debug
php your-application.php
```
:::

:::{tab-item} Windows

```powershell
$env:OTEL_LOG_LEVEL="debug"
```
:::
::::

Make sure to rerun your PHP application.


## Resources

To learn how to enable debug logging for the EDOT Collector, refer to [Enable debug logging for EDOT Collector](../edot-collector/enable-debug-logging.md).
