---
navigation_title: Troubleshoot Collector sampling configuration
description: Learn how to troubleshoot missing or incomplete traces in the EDOT Collector caused by sampling configuration.
applies_to:
  serverless: all
  product:
    edot_collector: ga  
products:
  - id: observability
  - id: edot-collector
---

# Missing or incomplete traces due to Collector sampling

If traces or spans are missing in Kibana, the issue might be related to the Collector’s sampling configuration. Tail-based sampling in the Collector can reduce trace volume if policies are too strict or misconfigured.

Both Collector-based and SDK-level sampling can lead to gaps in telemetry if not configured correctly. See [Missing or incomplete traces due to SDK sampling](../edot-sdks/misconfigured-sampling-sdk.md) for more information.

## Symptoms

- Only a small subset of traces reaches Elasticsearch/Kibana, even though SDKs are exporting spans.
- Error traces are missing because they’re not explicitly included in the `sampling_policy`.
- Collector logs show dropped spans.

## Causes

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

:::{step} Differentiate head vs. tail sampling

- Review if SDKs apply head sampling, which reduces traces available for tail sampling
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
- [Missing or incomplete traces due to SDK sampling](../edot-sdks/misconfigured-sampling-sdk.md)