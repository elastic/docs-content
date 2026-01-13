---
applies_to:
  serverless: ga
  stack: ga 9.3+
---

# Convert processor [streams-convert-processor]
The convert processor converts a field to a different data type. For example, you could convert a string to an integer.

To convert a field to a different data type:

1. Select **Create** → **Create processor**.
1. Select **Convert** from the **Processor** menu.
1. Set the **Source Field** to the field you want to convert.
1. Set **Type** to the output data type.

This functionality uses the {{es}} convert pipeline processor. Refer to the [convert processor](elasticsearch://reference/enrich-processor/convert-processor.md) {{es}} documentation for more information.