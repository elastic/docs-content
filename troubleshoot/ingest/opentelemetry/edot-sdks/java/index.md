---
navigation_title: EDOT Java
description: Troubleshooting guide for the EDOT Java agent, covering connectivity, agent identification, and debugging.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_java: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Troubleshooting the EDOT Java agent [troubleshooting-the-edot-java-agent]

Use the information in this section to troubleshoot common problems. As a first step, make sure your stack is compatible with the [supported technologies](elastic-otel-java://reference/edot-java/supported-technologies.md) for EDOT Java and the OpenTelemetry SDK.

If you need help and you're an existing Elastic customer with a support contract, create a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/). Other users can post in the [APM discuss forum](https://discuss.elastic.co/c/apm) or [open a GitHub issue](https://github.com/elastic/elastic-otel-node/issues)

## General troubleshooting

Make you have set a service name, for example `-Dotel.service.name=Service1` or the environment variable `OTEL_SERVICE_NAME` set to `Service1`. Otherwise, by default the data will be sent to `unknown_service_java`. You may be getting data but it may all be under that service.

## Connectivity to endpoint

Check from the host, VM, pod, container, or image running the app that connectivity is available to the Collector. For more detailed connectivity troubleshooting, refer to [Connectivity issues](/troubleshoot/ingest/opentelemetry/connectivity.md).

The following examples use a default URL, `http://127.0.0.1:4318/`, which you should replace with the endpoint you are using:

- OpenTelemetry or {{agent}} without authentication: `curl -i http://127.0.0.1:4318/v1/traces -X POST -d '{}' -H content-type:application/json`
- OpenTelemetry or {{agent}} with API key authentication: `curl -i http://127.0.0.1:4318/v1/traces -X POST -d '{}' -H content-type:application/json -H "Authorization:ApiKey <api_key>"`

The Collector should produce output similar to the following:

```
{"partialSuccess":{}}
```

## Agent troubleshooting

Determine if the issue is related to the EDOT agent, other agents, extensions, or connectivity issues by following these steps:

:::::{stepper}

::::{step} Run the application without the EDOT agent
Start the application with no agent (remove `-javaagent:` argument) and restart the application.
- If the issue is still present without the EDOT agent, then the problem is likely related to the application or its environment.
- If the issue is resolved, then re-adding the EDOT agent should let you confirm that the issue is related to the agent.
::::

::::{step} Remove other agents
If more than one instrumentation agent is being used on the application (multiple `-javaagent:` JVM arguments), remove other agents and restart the application. Multiple instrumentation agents can conflict with each other and are a known cause of unpredictable behavior.

- If the issue is still present with only the EDOT agent, then it indicates the problem is likely related to the EDOT agent.
- If the issue is resolved, then it indicates the problem might be related to interactions between instrumentation agents.
::::

::::{step} Remove instrumentation extensions
If [instrumentation extensions](https://opentelemetry.io/docs/zero-code/java/agent/extensions/) are being used with the `otel.javaagent.extensions` JVM system property or the `OTEL_JAVAAGENT_EXTENSIONS` environment variable, remove them and restart the application.
- If the issue is still present without the extensions, then the problem is likely related to the EDOT agent.
- If the issue is resolved, then it indicates the problem might be related to the extensions.
::::

::::{step} Check end-to-end connectivity
Check end-to-end connectivity without the EDOT agent by running one or more of the example apps in [elastic-otel-java](https://github.com/elastic/elastic-otel-java/blob/main/examples/troubleshooting/README.md). These use the OpenTelemetry SDK rather than the auto-instrumentation. They can help confirm whether the issue is specific to the EDOT agent or caused by something else.
::::

:::::

## Agent debug logging

As debugging output is verbose and might produce noticeable overhead on the application, follow one of these strategies when you need logging: 

- In case of a technical issue or exception with the agent, use [agent debugging](#agent-debugging).
- If you need details on the captured data, use [per-signal debugging](#per-signal-debugging).

For more information, refer to [Enable debug logging for EDOT SDKs](/troubleshoot/ingest/opentelemetry/edot-sdks/enable-debug-logging.md).

In case of missing data, check first that the technology used in the application is supported in [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md) and in [EDOT Java](elastic-otel-java://reference/edot-java/supported-technologies.md). For more troubleshooting guidance, refer to [No application-level telemetry visible in {{kib}}](/troubleshoot/ingest/opentelemetry/edot-sdks/missing-app-telemetry.md).

### Agent debugging

To turn on agent debug logging you can either:

- Set the `ELASTIC_OTEL_JAVAAGENT_LOG_LEVEL` environment variable or the `elastic.otel.javaagent.log_level` JVM system property to `debug`.
- Set the `OTEL_JAVAAGENT_DEBUG` environment variable or the `otel.javaagent.debug` JVM system property to `true`

Both options require a JVM restart.

The `otel.javaagent.debug` / `OTEL_JAVAAGENT_DEBUG` configuration options are inherited from the upstream
agent. Setting them to `true` also produce span information in plain text format.

When `elastic.otel.javaagent.log_level` or `ELASTIC_OTEL_JAVAAGENT_LOG_LEVEL` are set to `debug`, the span information is included in JSON format.

If only captured data details are needed, [per-signal debugging](#per-signal-debugging) is a lighter alternative.

### Per-signal debugging

Each supported signal can be logged independently. This allows limiting the amount of captured data and reducing the overhead compared
to [agent debugging](#agent-debugging).

This is configured through the `OTEL_{SIGNAL}_EXPORTER` environment variable or `otel.{signal}.exporter` JVM system property
from the [OpenTelemetry SDK](https://opentelemetry.io/docs/languages/java/configuration/#properties-exporters) by adding any of the following exporters to the default `otlp` value:
- `otlp,logging-otlp`: JSON logging (recommended)
- `otlp,logging`: plain text logging

Both options require a JVM restart.

## Access or modification of application code

The agent modifies the Java application binaries in bytecode form and does not requires original code nor recompiling or re-packaging the application.

## How to deactivate the agent

There are two ways to deactivate the instrumentation agent:

- Remove the `-javaagent:` JVM argument.
- Set the `OTEL_JAVAAGENT_ENABLED` environment variable or the `otel.javaagent.enabled` Java system property to `false`.

In both cases you need to restart the JVM.

## Partial activation or deactivation of the agent

You can partially deactivate the agent, or only selectively activate a limited set of instrumentations by following instructions in the [upstream documentation](https://opentelemetry.io/docs/zero-code/java/agent/disable/).

## Check if {{edot}} is attached to a running JVM [check-if-edot-is-attached-to-a-running-jvm]

There are a few ways you can detect if the agent has been attached to a JVM:

- In JVM logs, agent startup log message might be included.
- In JVM arguments, Run `ps -ef|grep javaagent`.
- In environment variables, for example `JAVA_TOOL_OPTIONS`. Check by inspecting the output of `export|grep javaagent`.

## Identify the version of EDOT agent [identify-the-version-of-edot-agent]

When the agent starts, a log message in the standard error provides the agent version: 

```
INFO io.opentelemetry.javaagent.tooling.VersionLogger - opentelemetry-javaagent - version: 1.2.3
```

In addition, the `-javaagent:` JVM argument can provide the path to the agent file name, which might also contain
the agent version, for example `-javaagent:elastic-otel-javaagent-1.2.3.jar`.

Executing the agent jar as an application with `java -jar elastic-otel-javaagent.jar` provides the agent version on standard output, which could be relevant to use when the jar file has been renamed.

Also, you can inspect the `Implementation-Version` entry in `META-INF/MANIFEST.MF` file of the agent jar, for example with `unzip -p elastic-otel-javaagent.jar META-INF/MANIFEST.MF|grep 'Implementation-Version'`.

## Versions of the OpenTelemetry contrib dependencies

Because EDOT Java is a distribution of [OpenTelemetry Java instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation), it includes the following dependencies:

- [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation)
- [OpenTelemetry Java SDK](https://github.com/open-telemetry/opentelemetry-java)
- [Semantic Conventions Java mappings](https://github.com/open-telemetry/semantic-conventions-java)
- [OpenTelemetry Java Contrib](https://github.com/open-telemetry/opentelemetry-java-contrib)

The versions of those included in {{edot}} are usually aligned with the OpenTelemetry Java Instrumentation. For reference, check the [EDOT Java release notes](elastic-otel-java://release-notes/index.md) details of versions included in each release.

## When and how to update {{edot}} [when-and-how-to-update-edot]

The general recommendation is to update the EDOT agent to the latest version when possible to benefit from:

- Bug fixes and technical improvements.
- Support of new features and instrumentation.
- Evolution of semantic conventions.
- Frequent and regular updates usually makes reviewing and handling changes easier.

Updating to the latest {{edot}} version involves reviewing changes of the included dependencies:

- [OpenTelemetry Java Instrumentation](https://github.com/open-telemetry/opentelemetry-java-instrumentation)
- [OpenTelemetry Java SDK](https://github.com/open-telemetry/opentelemetry-java)
- [Semantic Conventions Java mappings](https://github.com/open-telemetry/semantic-conventions-java)
- [OpenTelemetry Java Contrib](https://github.com/open-telemetry/opentelemetry-java-contrib)

To review each of those individually, you can use the [EDOT Java release notes](elastic-otel-java://release-notes/index.md) for links to the respective versions of each component.

### OpenTelemetry API/SDK update

To implement manual instrumentation, some applications use the OpenTelemetry API and/or SDK which allows them to capture custom spans, metrics or even send data without any instrumentation agent.

Updates of the OpenTelemetry API/SDK in the application and the EDOT Java agent can be done independently.

- EDOT Java is backward-compatible with all previous versions of OpenTelemetry API/SDK.
- Using a more recent version of API/SDK than the one in {{edot}} should usually work without problem, however to ensure maximum compatibility keeping OpenTelemetry API/SDK version ≤ {{edot}} OpenTelemetry API/SDK version is recommended.

### How to update

Updating the EDOT Java agent is done by replacing the agent binary `.jar` that has been [added during setup](elastic-otel-java://reference/edot-java/setup/index.md).
