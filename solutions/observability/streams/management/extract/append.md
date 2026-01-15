---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
---
# Append processor [streams-append-processor]
% Need use cases

Use the append processor to add a value to an existing array field, or create the field as an array if it doesn’t exist.

To use an append processor:

1. Select **Create** → **Create processor**.
1. Select **Append** from the **Processor** menu.
1. Set **Source Field** to the field you want append values to.
1. Set **Target field** to the values you want to append to the **Source Field**.

This functionality uses the {{es}} [append processor](elasticsearch://reference/enrich-processor/append-processor.md) internally, but you configure it in Streamlang. Streamlang doesn’t always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).