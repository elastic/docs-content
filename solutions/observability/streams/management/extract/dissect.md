---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
---
# Dissect processor [streams-dissect-processor]

The dissect processor parses structured log messages and extracts fields from them. It uses a set of delimiters to split the log message into fields instead of predefined patterns to match the log messages.

Dissect is much faster than Grok, and is recommend for log messages that follow a consistent, structured format.

To parse a log message with a dissect processor:

1. Select **Create** → **Create processor**.
1. Select **Dissect** from the **Processor** menu.
1. Set the **Source Field** to the field you want to dissect
1. Set the delimiters you want to use in the **Pattern** field. Refer to the [example pattern](#streams-dissect-example) for more information on setting delimiters.

This functionality uses the {{es}} dissect pipeline processor. Refer to the [dissect processor](elasticsearch://reference/enrich-processor/dissect-processor.md) {{es}} documentation for more information.

## Example dissect pattern [streams-dissect-example]

The following example shows the dissect pattern for an unstructured log message.

**Log message:**
```
2025-04-04T09:04:45+00:00 ERROR 160.200.87.105 127.79.135.127 21582
```

**Dissect Pattern:**
```
%{timestamp} %{log.level} %{source.ip} %{destination.ip} %{destination.port}
```