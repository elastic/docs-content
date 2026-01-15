---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
---
# Set processor [streams-set-processor]

Use the set processor to assign a specific value to a field, creating the field if it doesn’t exist or overwriting its value if it does.

To use a set processor:

1. Select **Create** → **Create processor**.
1. Select **Set** from the **Processor** menu.
1. Set **Source Field** to the field you want to insert, upsert, or update.
1. Set **Value** to the value you want the source field to be set to.

This functionality uses the {{es}} [set processor](elasticsearch://reference/enrich-processor/set-processor.md) internally, but you configure it in Streamlang. Streamlang doesn’t always have 1:1 parity with the ingest processor options and behavior. Refer to [Processor limitations and inconsistencies](../extract.md#streams-processor-inconsistencies).