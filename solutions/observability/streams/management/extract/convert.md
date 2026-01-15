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
1. (Optional) Set **Target field** to write the converted value to a different field.
1. Set **Type** to the output data type.

::::{note}
If you add a **Convert** processor inside a condition group (a **WHERE** block), you must set a **Target field**.
::::

This functionality uses the {{es}} convert pipeline processor. Refer to the [convert processor](elasticsearch://reference/enrich-processor/convert-processor.md) {{es}} documentation for more information.