---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
---
# Rename processor [streams-rename-processor]

Use the rename processor to change the name of a field, moving its value to a new field name and removing the original.

To use a rename processor:

1. Select **Create** → **Create processor**.
1. Select **Rename** from the **Processor** menu.
1. Set **Source Field** to the field you want to rename.
1. Set **Target field** to the new name you want to use for the **Source Field**.

This functionality uses the {{es}} [rename processor](elasticsearch://reference/enrich-processor/rename-processor.md) internally, but you configure it in Streamlang. Streamlang doesn’t always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).