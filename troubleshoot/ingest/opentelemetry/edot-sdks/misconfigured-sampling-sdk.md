---
navigation_title: SDK sampling issues
description: Learn how to troubleshoot missing or incomplete traces in EDOT SDKs caused by head sampling configuration.
applies_to:
  serverless: all
  product:
    elastic-otel-sdk: ga
products:
  - id: observability
  - id: edot-sdk
---

# Missing or incomplete traces due to SDK sampling

If traces or spans are missing in Kibana, the issue might be related to SDK-level sampling configuration. By default, SDKs use head-based sampling, meaning the decision to record or drop a trace is made when the trace is first created.

Both SDK-level and Collector-based sampling can result in gaps in telemetry if misconfigured. Refer to [Missing or incomplete traces due to Collector sampling](../edot-collector/misconfigured-sampling-collector.md) for more details.

## Symptoms

You might notice one or more of the following behaviors when SDK-level sampling is impacting your traces:

- Only a small subset of traces reaches {{es}} or {{kib}}, even though SDKs are exporting spans.
- Transactions look incomplete because some spans are missing.
- Trace volume is unexpectedly low compared to logs or metrics.

## Causes

These factors can result in missing spans or traces when sampling is configured at the SDK level:

- Head sampling at the SDK level drops traces before they're exported.
- Default sampling rates (for example `1/100` or `1/1000`) might be too low for your workload.
- Environment variables like `OTEL_TRACES_SAMPLER` or `OTEL_TRACES_SAMPLER_ARG` are not set, not recognized, or formatted in a way the SDK doesn't support.
- Inconsistent configuration across services can lead to fragmented or incomplete traces.
- Some SDKs enforce stricter formats for sampler arguments, which can cause values to be ignored if not matched precisely.

## Resolution

Follow these steps to resolve SDK sampling configuration issues:

::::{stepper}

:::{step} Check SDK environment variables

- Confirm that `OTEL_TRACES_SAMPLER` and `OTEL_TRACES_SAMPLER_ARG` are set correctly.
- For testing, you can temporarily set:

  ```bash
  export OTEL_TRACES_SAMPLER=always_on
  ```
- In production, consider using `parentbased_traceidratio` with an explicit ratio.
:::

:::{step} Align configuration across services

- Use consistent sampling configuration across all instrumented services to help avoid dropped child spans or fragmented traces.
:::

:::{step} Adjust sampling ratios for your traffic

- For low-traffic applications, avoid extremely low ratios (such as `1/1000`). 

    For example, the following configuration samples ~20% of traces:

  ```bash
  export OTEL_TRACES_SAMPLER=parentbased_traceidratio
  export OTEL_TRACES_SAMPLER_ARG=0.2
  ```
:::

:::{step} Use Collector tail sampling for advanced scenarios

- Head sampling can't evaluate the full trace context before making a decision.
- For more control (for example "keep all errors, sample 10% of successes"), use Collector tail sampling.

    For more information, refer to [Missing or incomplete traces due to Collector sampling](../edot-collector/misconfigured-sampling-collector.md).
:::

::::

## Resources

- [OTEL_TRACES_SAMPLER environment variable specifications](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#otel_traces_sampler)
- [OpenTelemetry sampling concepts - contrib documentation](https://opentelemetry.io/docs/concepts/sampling/)
- [Missing or incomplete traces due to Collector sampling](../edot-collector/misconfigured-sampling-collector.md)
