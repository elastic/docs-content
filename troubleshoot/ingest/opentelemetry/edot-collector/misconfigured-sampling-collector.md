---
navigation_title: Collector sampling issues
description: Learn how to troubleshoot missing or incomplete traces in the EDOT Collector caused by sampling configuration.
applies_to:
  serverless: ga
  product:
    edot_collector: ga  
products:
  - id: observability
  - id: edot-collector
---

# Missing or incomplete traces due to Collector sampling

If traces or spans are missing in {{kib}}, the issue might be related to the Collector's sampling configuration. For general troubleshooting when no data appears in {{kib}}, refer to [No data visible in {{kib}}](/troubleshoot/ingest/opentelemetry/no-data-in-kibana.md). 

{applies_to}`stack: ga 9.2` Tail-based sampling (TBS) allows the Collector to evaluate entire traces before deciding whether to keep them. If TBS policies are too strict or not aligned with your workloads, traces you expect to see may be dropped.

Both Collector-based and SDK-level sampling can lead to gaps in telemetry if not configured correctly. Refer to [Missing or incomplete traces due to SDK sampling](/troubleshoot/ingest/opentelemetry/edot-sdks/misconfigured-sampling-sdk.md) for more information.

## Symptoms

When Collector-based tail sampling is misconfigured or too restrictive, you might observe the following:

- Only a small subset of traces reaches {{es}}/{{kib}}, even though SDKs are exporting spans.
- Error traces are missing because they’re not explicitly included in the `sampling_policy`.
- Collector logs show dropped spans.

## Causes

The following conditions can lead to missing or incomplete traces when using tail-based sampling in the Collector:

- Tail sampling policies in the Collector are too narrow or restrictive.
- The default rule set excludes key transaction types (for example long-running requests, non-error transactions).
- Differences between head sampling (SDK) and tail sampling (Collector) can lead to fewer traces being available for evaluation.
- Conflicting or overlapping `sampling_policy` rules might result in unexpected drops.
- High load: the Collector might drop traces if it can’t evaluate policies fast enough.

## Resolution

Follow these steps to resolve sampling configuration issues:

::::{stepper}

:::{step} Review `sampling_policy` configuration

- Check the `processor/tailsampling` section of your Collector configuration
- Ensure policies are broad enough to capture the traces you need
:::

:::{step} Add explicit rules for critical traces

- Create specific rules for important trace types
- Example: keep all error traces, 100% of login requests, and 10% of everything else
- Use attributes like `status_code`, `operation`, or `service.name` to fine-tune rules
:::

:::{step} Validate Collector logs

- Review Collector logs for messages about dropped spans, and determine whether drops are due to sampling policy outcomes or resource limits
:::

:::{step} Differentiate head and tail sampling

- Review if SDKs already applies head sampling, which reduces traces available for tail sampling in the Collector
- Consider setting SDKs to `always_on` and managing sampling centrally in the Collector for more flexibility
:::

:::{step} Test in staging

- Adjust sampling policies incrementally in a staging environment
- Monitor trace volume before and after changes
- Validate that critical traces are captured as expected
:::

::::

## Resources

- [Tail sampling processor (Collector)](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor)
- [OpenTelemetry sampling concepts - contrib documentation](https://opentelemetry.io/docs/concepts/sampling/) 
- [Missing or incomplete traces due to SDK sampling](/troubleshoot/ingest/opentelemetry/edot-sdks/misconfigured-sampling-sdk.md)