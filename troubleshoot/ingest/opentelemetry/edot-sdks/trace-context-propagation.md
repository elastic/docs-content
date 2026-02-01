---
navigation_title: Trace context header propagation  
description: Troubleshoot trace propagation when migrating from Elastic APM agents to OpenTelemetry.
applies_to:  
  stack:  
  serverless:  
    observability:  
products:  
  - id: cloud-serverless  
  - id: observability  
  - id: edot-sdk  
---

# Trace context headers not propagating between OpenTelemetry and Elastic {{product.apm}}

Use this guide to troubleshoot missing or broken distributed traces when combining OpenTelemetry instrumentation with Elastic {{product.apm}} agents.

:::{important}
Mixing OpenTelemetry and non-OpenTelemetry (Elastic {{product.apm}} agent) configurations is not officially supported. This guide is only intended for troubleshooting trace context propagation during gradual migrations or partial instrumentation. 
:::

The recommended path is to adopt an OpenTelemetry-native strategy using {{edot}}. However, if you are in a transition period, this page helps you diagnose and mitigate trace context propagation issues (`traceparent` / `tracestate`) until you can complete the migration.

## Symptoms

You might observe one or more of the following issues:

- Distributed traces are broken across service boundaries.
- Downstream spans start new traces instead of continuing the existing one.
- Traces appear split or uncorrelated in the UI.
- Parent–child relationships are missing when traffic crosses between:
  - OpenTelemetry-instrumented services and Elastic {{product.apm}} agents
  - New and legacy Elastic {{product.apm}} agents in the same call chain
  - Different versions of {{product.apm}} agents in the same call chain

## Causes

In mixed OpenTelemetry and Elastic {{product.apm}} environments, propagation issues typically stem from header or configuration mismatches.

OpenTelemetry uses the [W3C Trace Context](https://www.w3.org/TR/trace-context/) standard headers:

- `traceparent`
- `tracestate`

All modern Elastic {{product.apm}} agents support W3C Trace Context by default.

For backward compatibility, Elastic agents also support a legacy proprietary header (`elastic-apm-traceparent`) and operate in dual‑propagation mode:

- **Inbound**: Agents first read W3C headers; if missing, they fall back to the legacy header.
- **Outbound**: Agents inject both W3C headers and the legacy header to support mixed environments.

Propagation issues often occur when:

- Older (pre‑W3C) Elastic agents are still in use.
- Legacy propagation is turned off prematurely.
- Trace continuation is misconfigured to restart traces.
- Two tracing SDKs run in the same process and compete for instrumentation or context.

## Recommended and migration-only patterns

Before going fully OTel-native, you can use the OpenTelemetry Bridge offered by Elastic agents as a transitional solution:

### OpenTelemetry Bridge (temporary)

The bridge lets you use the OpenTelemetry API for manual instrumentation while still using an Elastic {{apm-agent}} for auto‑instrumentation and exporting.

With the bridge:

- The Elastic agent implements the OpenTelemetry API.
- Spans created through the OTel API become native Elastic spans.
- Parent–child relationships are preserved across manual and auto‑instrumentation.

The bridge is available in major Elastic agents (Java, .NET, Node.js, Python). Prefer moving to {{edot}} (OTel-native) when you can.

### Avoid running a full OpenTelemetry SDK alongside an Elastic agent

Do not run a full OpenTelemetry SDK in the same process as an Elastic {{apm-agent}}.

This setup causes:

- Duplicate instrumentation and added overhead.
- Trace fragmentation (conflicting trace IDs).
- Startup conflicts (instrumentation, exporters, environment variables).

Each SDK might try to manage propagation independently, breaking distributed tracing. For an OpenTelemetry-native setup, use {{edot}} instead of mixing SDKs.

## Resolution

The preferred resolution is to complete your migration to OpenTelemetry and use {{edot}} (OTel-native). However, if you are still in a gradual migration and need traces to connect across mixed services, the following steps might help.

::::::{stepper}

::::{step} Ensure all services support W3C Trace Context

If you still have Elastic agents in the call path, verify that they support W3C Trace Context.

| Agent          | Minimum version |
| -------------- | --------------- |
| Java           | 1.14.0          |
| .NET           | 1.3.0           |
| Node.js        | 3.4.0           |
| Python         | 5.4.0           |
| Go             | 1.6.0           |
| Ruby           | 3.5.0           |
| PHP            | 1.0.0           |
| RUM (JS)       | 5.0.0           |

All recent releases prefer W3C propagation by default.

::::

::::{step} Verify propagation and trace continuation settings

Ensure agents:

- Have W3C propagation turned on (default).
- Retain legacy propagation if older agents are still present.
- Are not misconfigured to restart traces unexpectedly.

Some agents expose a trace continuation strategy (for example, .NET):

- `continue` (default): Continue incoming traces.
- `restart`: Always start a new trace.
- `restart_external`: Restart only for non-Elastic sources.

Unexpected trace restarts might indicate incorrect strategy settings.

::::

::::{step} Use the OpenTelemetry Bridge

If you're in transition and still use the OpenTelemetry API with an Elastic agent:

- Turn on the OpenTelemetry Bridge in the agent.
- Do not install a separate OpenTelemetry SDK in the same process.

This can help maintain context propagation during the migration. Plan to move to {{edot}} (OTel-native) when possible.

::::

::::{step} Keep dual‑propagation active during migrations

In mixed environments with OpenTelemetry SDKs (W3C only) and older Elastic agents, keep the default dual‑propagation mode turned on so that:

- New services read W3C headers.
- Legacy services read the `elastic-apm-traceparent` header.

Turning off the legacy header too early can break trace continuity.

::::

::::{step} Turn off legacy headers after full migration

When all services support W3C Trace Context, you might turn off emission of the legacy header to reduce header size and network overhead.

Refer to agent-specific documentation to turn off legacy header output.

::::

::::::

## Best practices

- Use {{edot}} for full OTel support and to avoid mixed-configuration issues.
- If you are in a gradual migration: standardize on W3C Trace Context across services and upgrade older agents early.
- Use one tracing implementation per process (Elastic agent or OpenTelemetry SDK). Avoid mixing SDKs.
- If you must mix APIs during a transition, use the OpenTelemetry Bridge temporarily and plan to move to {{edot}}.
- Validate cross-service tracing in staging before partial rollouts.

## Resources

- [W3C Trace Context specification](https://www.w3.org/TR/trace-context/)
- [Contrib OpenTelemetry context propagation documentation](https://opentelemetry.io/docs/concepts/context-propagation/)
- [Elastic {{product.apm}} OpenTelemetry Bridge (Java)](apm-agent-java://reference/opentelemetry-bridge.md)
- [Elastic {{product.apm}} OpenTelemetry Bridge (.NET)](apm-agent-dotnet://reference/opentelemetry-bridge.md)
- [Elastic {{product.apm}} OpenTelemetry Bridge (Node.js)](apm-agent-nodejs://reference/opentelemetry-bridge.md)
- [Elastic {{product.apm}} OpenTelemetry Bridge (Python)](apm-agent-python://reference/opentelemetry-api-bridge.md)