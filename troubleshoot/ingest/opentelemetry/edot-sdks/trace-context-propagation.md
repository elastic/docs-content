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

## Migration strategy overview

Completing a move to OpenTelemetry removes the mixed propagation issues described below. A typical path includes the following steps:

1. Add an OTLP endpoint and make it reachable from your applications (for example, in {{ecloud}} or your cluster).
2. Update your application to use the OpenTelemetry API instead of the Elastic {{product.apm}} API. The [OpenTelemetry Bridge](#about-the-opentelemetry-bridge) (when turned on for an Elastic agent) lets you do this while keeping the agent in place.
3. Replace Elastic {{product.apm}} agents with OpenTelemetry-based instrumentation ({{edot}} or contrib OpenTelemetry SDKs) when you are ready to go fully OTel-native.

For setup and options, refer to [OpenTelemetry with Elastic {{product.apm}}](/solutions/observability/apm/opentelemetry/index.md).

### About the OpenTelemetry Bridge

Elastic {{product.apm}} agents provide an OpenTelemetry API bridge that allows applications to emit traces and metrics using the OpenTelemetry API while still relying on an Elastic agent. However, the OpenTelemetry Bridge doesn't handle context propagation. It only provides API compatibility for manual instrumentation.

Use the bridge only as a short-term compatibility layer during migrations. For full OpenTelemetry support, including native propagation behavior, migrate to {{edot}}.

## Symptoms

If you are still in a mixed environment, you might observe one or more of the following issues:

- Distributed traces are broken across service boundaries.
- Downstream spans start new traces instead of continuing the existing one.
- Traces appear split or uncorrelated in the UI.
- Parent–child relationships are missing when traffic crosses between:
  - OpenTelemetry-instrumented services (including EDOT-based and contrib OpenTelemetry SDKs) and Elastic {{product.apm}} agents
  - Elastic {{product.apm}} agents that support W3C Trace Context and older, pre-W3C agents in the same call chain

## Causes

In mixed OpenTelemetry and Elastic {{product.apm}} environments, propagation issues typically stem from header handling or configuration mismatches.

OpenTelemetry uses the [W3C Trace Context](https://www.w3.org/TR/trace-context/) standard headers:

- `traceparent`
- `tracestate`

All modern Elastic {{product.apm}} agents support W3C Trace Context by default.

For backward compatibility, Elastic agents also support a legacy proprietary header (`elastic-apm-traceparent`) and operate in dual‑propagation mode:

- **Inbound**: Agents first read W3C headers; if missing, they fall back to the legacy header.
- **Outbound**: Agents inject both W3C headers and the legacy header to support mixed environments.

Propagation issues often occur when:

- Elastic agents older than **version 1.14.0** (pre-W3C) are still in use.
- Legacy propagation is turned off prematurely.
- Trace continuation is misconfigured to restart traces.
- Two tracing SDKs run in the same process and compete for instrumentation or context.

## Elastic {{product.apm}}–specific trace continuation behavior

Elastic {{product.apm}} agents expose a trace continuation strategy that controls how incoming trace headers are handled:

- `continue` (default): Continue incoming traces.
- `restart`: Always start a new trace.
- `restart_external`: Restart traces only if the contrib service is not using an Elastic {{product.apm}} agent.

The `restart_external` strategy is useful when a contrib service propagates W3C headers but sends its traces to a different backend, which otherwise results in missing or misleading parent transactions.

:::{note}
This trace continuation behavior is specific to Elastic {{product.apm}} agents. There is currently no equivalent feature in OpenTelemetry or EDOT.
:::

### Workaround for OpenTelemetry / EDOT

If you need to force a downstream OpenTelemetry-instrumented service to start a new trace independently:

- Strip or reset incoming trace context headers (`traceparent`, `tracestate`) at the ingress layer (for example, in an HTTP proxy or gateway).

This prevents the downstream service from attempting to continue an incompatible contrib trace.

## Resolution

The preferred resolution is to complete your migration to an OpenTelemetry-native setup using {{edot}}.
If you are still operating in a mixed environment, the following steps can help maintain trace continuity.

::::::{stepper}

::::{step} Ensure all Elastic agents support W3C Trace Context

Verify that any Elastic {{product.apm}} agents in the call path meet the minimum W3C-compatible versions:

| Agent    | Minimum version |
|--------- |---------------- |
| Java     | 1.14.0 |
| .NET     | 1.3.0 |
| Node.js  | 3.4.0 |
| Python   | 5.4.0 |
| Go       | 1.6.0 |
| Ruby     | 3.5.0 |
| PHP      | 1.0.0 |
| RUM (JS) | 5.0.0 |

Upgrading agents is often the most effective first step to reduce compatibility issues.

::::

::::{step} Keep dual-propagation turned on in mixed environments

In environments where OpenTelemetry SDKs (W3C-only) coexist with Elastic agents:

- Keep `elastic-apm-traceparent` turned on for Elastic agents.
- Allow agents to emit both W3C and legacy headers.

This maximizes compatibility and has negligible overhead.

If you use an HTTP proxy, gateway, or load balancer, ensure that the following are forwarded unchanged:

- `traceparent`
- `tracestate`
- `elastic-apm-traceparent`

Some proxies require explicit configuration to allow custom headers.

::::

::::{step} Review trace continuation settings on Elastic agents

If traces unexpectedly restart:

- Confirm the trace continuation strategy (`continue`, `restart`, `restart_external`).
- Ensure the chosen strategy matches your contrib service topology.

Misconfigured continuation settings can cause valid traces to be intentionally restarted.

::::

::::::

## Best practices

- Upgrade Elastic {{product.apm}} agents to the latest available versions.
- Standardize on W3C Trace Context across all services.
- Keep `elastic-apm-traceparent` turned on for as long as mixed agents exist.
- Ensure gateways and proxies forward trace headers unchanged.
- Use one tracing implementation per process.
- Plan and validate migrations in staging environments before partial rollouts.

## Resources

- [W3C Trace Context specification](https://www.w3.org/TR/trace-context/)
- [Contrib OpenTelemetry context propagation documentation](https://opentelemetry.io/docs/concepts/context-propagation/)