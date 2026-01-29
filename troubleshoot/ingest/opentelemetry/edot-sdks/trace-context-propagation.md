---
navigation_title: Troubleshoot trace context header propagation
description: Learn how to troubleshoot missing or broken distributed traces when combining OpenTelemetry instrumentation with Elastic APM agents.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Trace context headers not propagating between OpenTelemetry and Elastic APM

Use this guide to troubleshoot missing or broken distributed traces when combining OpenTelemetry instrumentation with Elastic {{product.apm}} agents during gradual migrations or partial rollouts.

This page focuses on propagation issues (`traceparent` / `tracestate`) and clarifies which mixing patterns are supported and which are discouraged.

## Symptoms

You might observe one or more of the following:

* Distributed traces are broken across service boundaries.
* Downstream spans start new traces instead of continuing the existing one.
* Traces appear split or uncorrelated in the UI.
* Parent–child relationships between spans are missing when traffic crosses between:

  * OpenTelemetry-instrumented services and Elastic {{product.apm}} agents.
  * New and very old Elastic {{product.apm}} agents in the same call chain.

## Causes

OpenTelemetry propagates trace context using the W3C Trace Context standard headers:

* `traceparent`
* `tracestate`

All modern Elastic {{product.apm}} agents use W3C Trace Context as the primary propagation standard by default.

Elastic {{product.apm}} agents also support a legacy proprietary header (`elastic-apm-traceparent`) for backward compatibility and operate in a dual‑propagation mode by default:

* **Inbound**: Agents first read the W3C headers. If those are missing, they fall back to the legacy `elastic-apm-traceparent` header.
* **Outbound**: Agents inject both W3C headers and the legacy header to support mixed fleets during migrations.

Propagation problems typically occur when:

* Very old Elastic {{apm-agent}} versions (pre‑W3C) are still present.
* Legacy propagation was turned off too early.
* Trace continuation is misconfigured to restart traces.
* Two independent tracing SDKs run in the same process and compete for instrumentation and context.

## Supported and problematic mixing patterns

When combining OpenTelemetry with Elastic {{product.apm}} agents, some patterns work well while others can cause propagation issues.

### Supported: Elastic APM agent with the OpenTelemetry Bridge

Elastic {{product.apm}} agents provide an OpenTelemetry Bridge, which allows you to use the OpenTelemetry API for manual instrumentation while keeping the Elastic {{apm-agent}} as the active tracer and exporter.

With the bridge:

* The Elastic {{apm-agent}} implements the OpenTelemetry API.
* Spans created through the OTel API become native Elastic spans.
* Parent–child relationships are preserved between Elastic auto‑instrumentation and OTel manual spans.

This pattern is available in most major agents (Java, .NET, Node.js, Python).

Use this option when you:

* Want to write vendor‑neutral manual instrumentation using the OTel API.
* Still rely on Elastic {{apm-agent}} auto‑instrumentation and features.

### Avoid: Running a full OpenTelemetry SDK alongside an Elastic APM agent

Avoid running a complete OpenTelemetry SDK implementation together with an Elastic {{apm-agent}} in the same process. This pattern is unnecessary and causes problems.

Running both together leads to:

* Double instrumentation and increased overhead.
* Trace fragmentation (two different trace IDs for the same request).
* Conflicts during startup (bytecode instrumentation, environment variables, exporters).

In this setup, each SDK might attempt to manage context and propagation independently, breaking distributed tracing.

If you want a fully OpenTelemetry‑native setup, use {{edot}} (EDOT) instead of the Elastic {{apm-agent}}.

## Resolution

::::::{stepper}

::::{step} Ensure all services support W3C Trace Context

Verify that all Elastic {{apm-agent}}s in the request path are running versions that support W3C Trace Context.

Minimum versions that introduced W3C support:

| Agent    | Minimum version |
| -------- | --------------- |
| Java     | 1.14.0          |
| .NET     | 1.3.0           |
| Node.js  | 3.4.0           |
| Python   | 5.4.0           |
| Go       | 1.6.0           |
| Ruby     | 3.5.0           |
| PHP      | 1.0.0           |
| RUM (JS) | 5.0.0           |

All current releases prefer W3C Trace Context by default.

::::

::::{step} Verify propagation and trace continuation settings

Check that your agents are not configured to turn off W3C propagation or are not misconfigured to restart traces unexpectedly.

Key behaviors to verify:

* W3C propagation is active (default in all modern agents).
* Legacy propagation is still active if older agents remain in the fleet.
* Trace continuation is not misconfigured to restart traces.

Some agents expose a trace continuation strategy (for example .NET):

* `continue` (default): Continue the incoming trace when valid context is present.
* `restart`: Ignore incoming headers and start a new trace.
* `restart_external`: Restart only when the incoming trace is not from an Elastic‑monitored service.

If traces unexpectedly restart, ensure this setting is not configured to `restart` or `restart_external`, unless explicitly intended.

::::

::::{step} Use the OpenTelemetry Bridge when mixing APIs

If your application uses the OpenTelemetry API for manual instrumentation and an Elastic {{apm-agent}} for auto‑instrumentation:

* Turn on or keep active the OpenTelemetry Bridge in the agent.
* Do not run a separate OpenTelemetry SDK implementation in the same process.

This ensures a single tracer manages context, propagation, and exporting.

::::

::::{step} Keep dual‑propagation active during migrations

If your environment contains a mix of:

* OpenTelemetry SDKs (W3C only), and
* Older Elastic {{apm-agent}}s

keep the default dual‑propagation mode active so that:

* New services can read W3C headers, and
* Older services can still read `elastic-apm-traceparent`.

Turning off the legacy header too early can break trace continuity.

::::

::::{step} Optionally turn off legacy headers after full migration

Once all services are confirmed to support W3C Trace Context, you might turn off emission of the legacy `elastic-apm-traceparent` header to reduce header size and network overhead.

Refer to the agent‑specific configuration documentation for how to disable legacy header emission in your agent.

::::

::::::

## Best practices

* Standardize on W3C Trace Context across all services.
* Upgrade old agents early in migration projects.
* Use only one tracing implementation per process (Elastic {{apm-agent}} or OpenTelemetry SDK, not both).
* Use the OpenTelemetry Bridge when combining OTel API with Elastic agents.
* Prefer EDOT for fully OpenTelemetry‑native deployments.
* Validate cross-service tracing in staging before rolling out partially.

## Resources

* [W3C Trace Context specification](https://www.w3.org/TR/trace-context/) — Official W3C spec defining `traceparent` and `tracestate` headers for distributed trace context propagation.
* [Contrib OpenTelemetry propagation documentation](https://opentelemetry.io/docs/concepts/context-propagation/) — OpenTelemetry guide on context propagation and how W3C Trace Context is used.
* [Elastic {{product.apm}} OpenTelemetry Bridge documentation (Java)](apm-agent-java://reference/opentelemetry-bridge.md) — Example Elastic {{product.apm}} OpenTelemetry Bridge docs; similar per‑agent pages exist (for example, .NET).