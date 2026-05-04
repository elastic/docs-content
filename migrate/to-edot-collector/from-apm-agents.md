---
navigation_title: Move APM agents using the Collector
applies_to:
  stack: ga 9.2+
  serverless:
    observability:
products:
  - id: observability
  - id: edot-collector
---

# Move classic {{product.apm}} agents using the {{edot}} Collector

If you're using classic Elastic {{product.apm}} agents and want to move to an OpenTelemetry-based pipeline, the {{edot}} Collector provides a migration bridge through the [Elastic {{product.apm}} intake receiver](elastic-agent://reference/edot-collector/components/elasticapmintakereceiver.md). This lets your existing {{product.apm}} agents continue sending data unchanged while you gradually re-instrument your applications with OpenTelemetry SDKs.

## How it works

The Elastic {{product.apm}} intake receiver implements the Elastic Intake v2 protocol, making the {{edot}} Collector behave like {{apm-server}} from the perspective of your agents. Telemetry is stored in the same format and indices as before. There is no change required to your agents during the transition.

:::{important}
Real user monitoring (RUM) intake and older Elastic {{product.apm}} intake protocols are not supported by this receiver.
:::

## Before you begin

- Your {{stack}} must be running version 9.2 or later.
- You must have an {{edot}} Collector deployment. Refer to the [{{edot}} Collector documentation](elastic-agent://reference/edot-collector/index.md) for setup instructions.

## Steps

1. Add the `elasticapmintake` receiver to your {{edot}} Collector configuration:

   ```yaml
   receivers:
     elasticapmintake:
       agent_config:
         enabled: false
   ```

2. Point your existing {{product.apm}} agents at the {{edot}} Collector endpoint instead of the {{apm-server}} URL.

3. Verify that telemetry data (traces, metrics, logs) appears correctly in the {{observability}} UIs in {{kib}}.

4. Gradually re-instrument your applications using the language-specific [EDOT SDK migration guides](/migrate/apm-agents-to-edot/index.md) as your migration timeline allows.

## Next steps

Once your applications are re-instrumented with EDOT SDKs, you can remove the `elasticapmintake` receiver from your Collector configuration and route data directly through the standard OpenTelemetry pipeline.

For full configuration options including TLS, mTLS, and API key authentication, refer to the [Elastic {{product.apm}} intake receiver reference](elastic-agent://reference/edot-collector/components/elasticapmintakereceiver.md).
