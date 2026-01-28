---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
---
# Dissect processor [streams-dissect-processor]

The **Dissect** processor parses structured log messages and extracts fields from them. It uses a set of delimiters to split the log message into fields instead of predefined patterns to match the log messages.

Dissect is much faster than Grok, and is recommend for log messages that follow a consistent, structured format.

To parse a log message with a dissect processor:

1. Select **Create** → **Create processor**.
1. Select **Dissect** from the **Processor** menu.
1. Set the **Source Field** to the field you want to dissect.
1. Set the delimiters you want to use in the **Pattern** field. Refer to the [example pattern](#streams-dissect-example) for more information on setting delimiters.

This functionality uses the {{es}} [Dissect processor](elasticsearch://reference/enrich-processor/dissect-processor.md) internally, but you configure it in Streamlang. Streamlang doesn’t always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).

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

## Generate patterns [streams-dissect-patterns]
:::{note}
This feature requires a [Generative AI connector](kibana://reference/connectors-kibana/gen-ai-connectors.md).
:::

Instead of writing the dissect patterns by hand, you can select **Generate Patterns** to have AI generate them for you.

Generated patterns work best on semi-structured data. For very custom logs with a lot of text, creating patterns manually generally creates more accurate results.

To add a generated dissect pattern:

1. Select **Create processor**.
1. Select **Dissect** from the **Processor** menu.
1. Select **Generate pattern**.
1. Select **Accept** to add a generated pattern to the list of patterns used by the processor.

### How does **Generate patterns** work? [streams-dissect-pattern-generation]

:::{include} ../../../../_snippets/streams-suggestions.md
:::